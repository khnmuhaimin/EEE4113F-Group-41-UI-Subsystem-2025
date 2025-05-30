from http import HTTPStatus
from uuid import UUID
from flask import jsonify, make_response, request
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth.auth import verify_secret, is_password_correct
from database.models.admin import Admin
from database.models.weighing_node import WeighingNode
from database.database import DatabaseEngineProvider
from database.models.session import DEFAULT_SESSION_DURATION, Session as AdminSession
from database.utils.utils import utc_timestamp
from log.log import logger


def authenticate_weighing_node(func):
    """
    @authenticate

    Decorator to enforce authentication for API endpoints.

    It checks for the following HTTP headers:
    - "Authorization": must contain the API key.
    - "Node-ID": must contain the node identifier.

    Returns:
    - 401 if "Node-ID" or "Authorization" header is missing.
    - 401 if the API key is not valid
    """
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        if api_key is None:
            return ("Authorization header is missing.", HTTPStatus.UNAUTHORIZED)
        node_id = request.headers.get("Node-ID")
        if node_id is None:
            return ("Node ID header is missing.", HTTPStatus.UNAUTHORIZED)
        with Session(DatabaseEngineProvider.get_database_engine()) as session:
            node = session.scalar(select(WeighingNode).where(WeighingNode.uuid == UUID(node_id)))
            if node is None:
                return ("Unauthorized.", HTTPStatus.UNAUTHORIZED)
            correct_api_key = verify_secret(api_key, node.hashed_api_key)
            if not correct_api_key:
                return ("Unauthorized.", HTTPStatus.UNAUTHORIZED)
        result = func(*args, **kwargs)
        return result
    return wrapper


def authenticate_with_session_id(func):
    """
    @authenticate_admin

    Decorator to authenticate admin users via session cookie.

    Returns:
    - 400 if "session_id" cookie is missing.
    - 401 if session is invalid or expired.
    """
    def wrapper(*args, **kwargs):
        # make sure session ID exists
        session_id = request.cookies.get("session_id")
        if session_id is None:
            response_body = {
                "message": "The session ID cookie is missing."
            }
            return jsonify(response_body), HTTPStatus.BAD_REQUEST
        
        try:
            session_id = UUID(str(session_id))
        except ValueError:
            response_body = {
                    "message": "The session ID is invalid."
                }
            return jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY
        
        with Session(DatabaseEngineProvider.get_database_engine()) as session:
            # make sure the session ID exists in the database
            admin_session = session.scalar(select(AdminSession).where(AdminSession.session_id == session_id))
            if admin_session is None:
                response_body = {
                    "message": "Unauthorized"
                }
                response = make_response(jsonify(response_body), HTTPStatus.UNAUTHORIZED)
                return response
            # make sure the session ID is not expired
            session_start = admin_session.created_at
            now = utc_timestamp()
            expires_at = session_start + DEFAULT_SESSION_DURATION
            if now > expires_at:
                response_body = {
                    "message": "The session is expired. Log in again."
                }
                response = make_response(jsonify(response_body), HTTPStatus.UNAUTHORIZED)
                return response
        response = func(*args, **kwargs)
        return response
    return wrapper


def authenticate_with_password(func):
    """
    Decorator to authenticate a user by verifying their login credentials.

    Returns:
        Response: 
            - If login credentials are missing, returns a 400 Bad Request response with a message indicating the missing credentials.
            - If login details are invalid (incorrect email or password), returns a 401 Unauthorized response with a message indicating unauthorized access.
            - If login details are valid, proceeds with the original view function and returns the response from that function.
    """
    def wrapper(*args, **kwargs):
        # make sure login details exist
        try:
            request_body = request.get_json(True)
            email = request_body["email"]
            password = request_body["password"]
        except KeyError:
            response_body = {"message": "Request body is missing login credentials."}
            return jsonify(response_body), HTTPStatus.BAD_REQUEST
        
        # make sure login details are correct
        with Session(DatabaseEngineProvider.get_database_engine()) as session:
            admin = session.scalar(select(Admin).where(Admin.email == email))
            logger.debug(admin)
            if (admin is None
                or not is_password_correct(password, admin.hashed_password)):
                response_body = {"message": "Unauthorized."}
                return jsonify(response_body), HTTPStatus.UNAUTHORIZED
            
        # execute inner function
        response = func(*args, **kwargs)
        return response
    return wrapper


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