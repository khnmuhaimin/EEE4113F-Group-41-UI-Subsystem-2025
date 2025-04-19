from datetime import datetime
from http import HTTPStatus
from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import select
from sqlalchemy.orm import Session as DatabaseSession

from auth.auth import is_password_correct
from backend.routes.auth import authenticate_with_password, authenticate_with_session_id
from database.database import database_engine
from database.models.admin import Admin
from database.models.session import DEFAULT_SESSION_DURATION, Session as AdminSession
from database.utils.utils import utc_timestamp
from log.log import logger


admin_blueprint = Blueprint("admin", __name__, url_prefix="/admins")


@admin_blueprint.route("/login", methods=["POST"])
@authenticate_with_password
def login():
    """
    Authenticates an admin and creates or updates their session.

    Returns:
        Response:
            - 200 OK with admin name in the response body and a session cookie set.
    """
    email = request.json()["email"]

    with DatabaseSession(database_engine) as database_session:
        admin = database_session.scalars(select(Admin.email == email)).one_or_none()

        # Check if session already exists
        admin_session = database_session.scalars(select(AdminSession).where(AdminSession.admin_id == admin.id)).one_or_none()
        session_exists = admin_session is not None

        if session_exists:
            # update existing session
            now = utc_timestamp()
            admin_session.assign_new_session_id()
            admin_session.expires_at = now + DEFAULT_SESSION_DURATION
        
        else:  
            # Create and return new session
            admin_session = AdminSession(admin_id=admin.id)
            database_session.add(admin_session)
            
        database_session.commit()

        response_body = {
            "name": admin.name,
        }
        response = make_response(jsonify(response_body), HTTPStatus.OK)
        response.set_cookie(
            "session_id",
            str(admin_session.session_id),
            expires=admin_session.expires_at, 
            httponly=True,
            secure=True
        )
        return response


@admin_blueprint.route("/logout", methods=["POST"])
@authenticate_with_session_id
def logout():
    """
    Logs out the currently authenticated admin.

    Description:
        Deletes the admin session associated with the session ID cookie.

    Returns:
        Response:
            - 204 No Content on successful logout.
    """
    session_id = request.cookies.get("session_id")
    with DatabaseSession(database_engine) as database_session:
        admin_session = database_session.scalars(select(AdminSession.session_id == session_id)).one_or_none()
        database_session.delete(admin_session)
        return ("", HTTPStatus.NO_CONTENT)
