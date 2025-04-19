from http import HTTPStatus
from flask import Blueprint, jsonify, request
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from auth.auth import generate_secret, hash_secret, verify_preshared_key
from database.utils.utils import is_ip_address
from database.models.weighing_node import WeighingNode

from routes.auth import authenticate_with_session_id, authenticate_weighing_node
from database.database import DatabaseEngineProvider


weighing_node_blueprint = Blueprint("weighing_node", __name__)


def enforce_registration_in_progress_value(in_progress: bool):
    """
    @enforce_registration_in_progress_value

    Decorator to enforce registration status for a node. Can be configured for either registration in progress or complete.

    Parameters:
    - `in_progress` (bool): 
    - `True`: Enforces that the node's registration is still in progress.
    - `False`: Enforces that the node's registration is complete.

    Returns:
    - 401 if "Node-ID" header is missing.
    - 404 if the node is not found.
    - 400 if the nodes registration status does not match the required state (either in progress or complete).
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            node_id = request.headers.get("Node-ID")
            if node_id is None:
                return ("Node ID header is missing.", HTTPStatus.UNAUTHORIZED)
            with Session(DatabaseEngineProvider.get_database_engine()) as session:
                node = session.scalars(select(WeighingNode.uuid == node_id)).first()
                if node is None:
                    return ("Weighing node not found.", HTTPStatus.NOT_FOUND)
                if in_progress and not node.registration_in_progress:
                    return ("Registration is complete.", HTTPStatus.UNPROCESSABLE_ENTITY)
                elif not in_progress and node.registration_in_progress:
                    return ("Registration is in progress.", HTTPStatus.UNPROCESSABLE_ENTITY)
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


enforce_registration_in_progress = enforce_registration_in_progress_value(in_progress=True)
enforce_registration_complete = enforce_registration_in_progress_value(in_progress=False)


@weighing_node_blueprint.route("/ip-address", methods=["PUT"], endpoint="update_ip_address")
@authenticate_weighing_node
@enforce_registration_in_progress
def update_ip_address():
    """
    @update_ip_address

    Route to update the IP address of a weighing node.

    Returns:
    - 400 (Unprocessable Entity) if the IP address is missing.
    - 404 (Not Found) if the node with the specified "Node-ID" is not found.
    - 204 (No Content) on successful update, with no response body.
    """
    ip_address = request.remote_addr
    if ip_address is None:
        return ("IP Address not found", HTTPStatus.BAD_REQUEST)
    with Session(DatabaseEngineProvider.get_database_engine()) as session:
        node_id = request.headers.get("Node-ID")
        node = session.scalar(select(WeighingNode.uuid == node_id))
        node.ip_address = ip_address
        session.commit()
    return ("", HTTPStatus.NO_CONTENT)


@weighing_node_blueprint.route("/registration/start", methods=["POST"], endpoint="start_registration")
def start_registration():
    """
    @start_registration

    Description:
    Initiates the registration process for a new weighing node. Authenticates with a preshared key, validates the IP address, and creates a new weighing node in the database.

    Returned Values:
    - 200 OK: Returns the newly created node's UUID and API key.
    - 401 Unauthorized: If the Authorization header is missing or the key is invalid.
    - 400 Bad Request: If the IP address is missing or invalid.

    """
    # authenticate node using the preshared key
    # different from the standard auth protocol for weighing nodes
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return ("Authorization header is missing.", HTTPStatus.UNAUTHORIZED)
    correct_key = verify_preshared_key(auth_header)
    if not correct_key:
        return ("Invalid key.", HTTPStatus.UNAUTHORIZED)
    
    # confirm presence of IP address
    ip_address = request.remote_addr
    if ip_address is None:
        return ("IP Address not found.", HTTPStatus.BAD_REQUEST)
    if not is_ip_address(ip_address):
        return ("IP Address is invalid.", HTTPStatus.UNPROCESSABLE_ENTITY)
    
    # create the new node
    try:
        with Session(DatabaseEngineProvider.get_database_engine()) as session:
            node = WeighingNode(
                ip_address=ip_address,
            )
            node.api_key = generate_secret()
            node.hashed_api_key = hash_secret(node.api_key)
            session.add(node)
            session.commit()
            # TODO: alert admin
            return (f"{node.uuid}\n{node.api_key}\n", HTTPStatus.OK)
    except IntegrityError as e:
        error_message = str(e.orig)
        if error_message == "UNIQUE constraint failed: weighing_nodes.ip_address":
            return ("The IP address is already in use.", HTTPStatus.CONFLICT)


@weighing_node_blueprint.route("/registration/in-progress", methods=["GET"], endpoint="get_registration_tasks")
@authenticate_with_session_id
def get_registration_tasks():
    """
    GET /registration/in-progress

    Returns a list of weighing nodes currently in the registration process.

    Returns:
    - 200 OK with a JSON list of nodes (can be empty).
    - 400 if session cookie is missing.
    - 401 if session is invalid or expired.
    """
    with Session(DatabaseEngineProvider.get_database_engine()) as session:
        nodes_in_registration = session.scalars(select(WeighingNode).where(WeighingNode.registration_in_progress == True)).all()
        nodes_in_registration = list(map(lambda t: t.registration_in_progress_view(), nodes_in_registration))
        nodes_in_registration.sort(key=lambda t: t["created_at"])
        response = jsonify(nodes_in_registration)
        response.status_code = HTTPStatus.OK
        return response


    