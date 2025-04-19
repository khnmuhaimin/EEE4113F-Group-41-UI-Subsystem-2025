from http import HTTPStatus
from flask import jsonify, make_response, request
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.auth.auth import verify_secret, is_password_correct
from backend.database.models.admin import Admin
from backend.database.models.weighing_node import WeighingNode
from backend.database.database import database_engine
from backend.database.models.session import DEFAULT_SESSION_DURATION, Session as AdminSession
from backend.database.utils.utils import utc_timestamp


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
        with Session(database_engine) as session:
            node = session.scalars(select(WeighingNode.uuid == node_id)).one_or_none()
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
        session_id = request.cookies.get('session_id')
        if session_id is None:
            return ("The session ID cookie is missing.", HTTPStatus.BAD_REQUEST)
        with Session(database_engine) as session:
            # make sure the session ID exists in the database
            admin_session = session.scalars(select(AdminSession.session_id == session_id)).one_or_none()
            if admin_session is None:
                return ("Unauthorized", HTTPStatus.UNAUTHORIZED)
            # make sure the session ID is not expired
            session_start = admin_session.created_at
            now = utc_timestamp()
            expires_at = session_start + DEFAULT_SESSION_DURATION
            if now > expires_at:
                return ("The session is expired. Log in again.", HTTPStatus.UNAUTHORIZED)
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
            response_body = {
                "message": "Request body is missing login credentials."
            }
            return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST)
        
        # make sure login details are correct
        with Session(database_engine) as session:
            admin = session.scalars(select(Admin.email == email)).one_or_none()
            if (admin is None
                or not is_password_correct(password, admin.hashed_password)):
                response_body = {
                    "message": "Unauthorized."
                }
                return make_response(jsonify(response_body), HTTPStatus.UNAUTHORIZED)
            
        # execute inner function
        response = func(*args, **kwargs)
        return response
    return wrapper