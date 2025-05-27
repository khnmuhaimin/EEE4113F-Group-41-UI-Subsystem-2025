from datetime import datetime, timezone
from http import HTTPStatus
from uuid import UUID
from flask import Blueprint, jsonify, request
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.auth import generate_secret, hash_secret
from backend.websockets.notifications_manager import NotificationsManager
from database.utils.utils import is_ip_address
from database.models.weighing_node import WeighingNode

from routes.auth import authenticate_with_session_id, authenticate_weighing_node
from database.database import DatabaseEngineProvider


weighing_node_blueprint = Blueprint("weighing_node", __name__)


@weighing_node_blueprint.route("/flash-leds", methods=["PUT"], endpoint="make_node_flash_leds")
@authenticate_with_session_id
def make_node_flash_leds():
    # perform validation checks
    if "weighing_node_id" not in request.json:
        return jsonify({"message": "The weighing node's ID is missing."}), HTTPStatus.BAD_REQUEST
    if "flash_leds" not in request.json:
        return jsonify({"message": "The flash LEDs flag is missing."}), HTTPStatus.BAD_REQUEST
    node_id = request.json["weighing_node_id"]
    try:
        node_id = UUID(str(node_id))
    except ValueError:
        return jsonify({"message": "The weighing node's ID is invalid."}), HTTPStatus.UNPROCESSABLE_ENTITY
    flash_leds = request.json["flash_leds"]
    if not isinstance(flash_leds, bool):
        return jsonify({"message": "The flash LEDs flag must be a boolean."}), HTTPStatus.UNPROCESSABLE_ENTITY
    

    with Session(DatabaseEngineProvider.get_database_engine()) as session:
        node = session.scalar(select(WeighingNode).where(WeighingNode.uuid == node_id))
        if node is None:
            return jsonify({"message": "The weighing node was not found."}), HTTPStatus.NOT_FOUND
        if flash_leds != node.leds_flashing:
            node.leds_flashing = flash_leds
            session.commit()
        return ("", HTTPStatus.NO_CONTENT)


@weighing_node_blueprint.route("/registration/start", methods=["POST"], endpoint="start_registration")
def start_registration():
    """
    @start_registration

    Description:
    Initiates the registration process for a new weighing node.

    Returned Values:
    - 200 OK: Returns the newly created node's UUID and API key.

    """    
    # create the new node
    with Session(DatabaseEngineProvider.get_database_engine()) as session:
        node = WeighingNode()
        node.api_key = generate_secret()
        node.hashed_api_key = hash_secret(node.api_key)
        session.add(node)
        session.commit()
        NotificationsManager.push_notification("FETCH_WEIGHING_NODES")
        return (f"{node.uuid}\n{node.api_key}\n", HTTPStatus.OK)
        

@weighing_node_blueprint.route("", endpoint="get_weighing_node")
@authenticate_weighing_node
def get_weighing_node():
    node_id = UUID(request.headers.get("Node-ID"))
    with Session(DatabaseEngineProvider.get_database_engine()) as session:
        node = session.scalars(select(WeighingNode).where(WeighingNode.uuid == node_id).order_by(WeighingNode.created_at)).one_or_none()
        # guaranteed to not be None
        response = f"""{str(node.uuid)}
{"null" if node.location is None else node.location }
{str(node.registration_in_progress).lower()}
{str(node.leds_flashing).lower()}
{datetime.fromtimestamp(node.created_at, tz=timezone.utc).isoformat()}"""
        return response, HTTPStatus.OK


@weighing_node_blueprint.route("/registration/approve", methods=["POST"], endpoint="approve_weighing_node_registration")
@authenticate_with_session_id
def approve_weighing_node_registration():
    """
    Approve the registration of a weighing node by updating its status.

    Responses:
        - 204 No Content: The weighing node's registration was successfully approved or already completed.
        - 400 Bad Request: The `weighing_node_id` is missing from the request body.
        - 422 Unprocessable Entity: The provided `weighing_node_id` is invalid (not a valid UUID).
    """
    try:
        node_id = request.json["weighing_node_id"]
        node_id = UUID(str(node_id))
    except KeyError:
        response = jsonify({
            "message": "The weighing node's ID is missing."
        })
        response.status_code = HTTPStatus.BAD_REQUEST
        return response
    except ValueError:
        response = jsonify({
            "message": "The weighing node's ID is invalid."
        })
        response.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        return response
    
    with Session(DatabaseEngineProvider.get_database_engine()) as session:
        node = session.scalar(select(WeighingNode).where(WeighingNode.uuid == node_id))
        if not node.registration_in_progress:
             return ("", HTTPStatus.NO_CONTENT)
        node.registration_in_progress = False
        if node.leds_flashing:
            node.leds_flashing = False
        session.commit()
        return ("", HTTPStatus.NO_CONTENT)
    


@weighing_node_blueprint.route("all", endpoint="get_weighing_nodes")
@authenticate_with_session_id
def get_weighing_nodes():
    with Session(DatabaseEngineProvider.get_database_engine()) as session:
        weighing_nodes = session.scalars(select(WeighingNode).order_by(WeighingNode.created_at)).all()
        weighing_nodes = list(map(lambda t: t.admin_view(), weighing_nodes))
        response = jsonify(weighing_nodes)
        response.status_code = HTTPStatus.OK
        return response