from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import select
from sqlalchemy.orm import Session as DatabaseSession

from auth.auth import is_password_correct
from database.database import database_engine
from database.models.admin import Admin
from database.models.session import DEFAULT_SESSION_DURATION, Session as AdminSession
from database.utils.utils import utc_timestamp
from log.log import logger


admin_blueprint = Blueprint("admin", __name__, url_prefix="/admins")

@admin_blueprint.route("/login", methods=["POST"])
def login():
    # confirm that the login details are present
    try:
        request_body = request.get_json(True)
        email = request_body["email"]
        password = request_body["password"]
    except KeyError:
        response_body = {
            "message": "Request body is missing login credentials."
        }
        return make_response(jsonify(response_body), 400)
    

    with DatabaseSession(database_engine) as database_session:
        # confirm that login details are correct
        admin = database_session.scalars(select(Admin).where(Admin.email == email)).one_or_none()
        
        # If not authorized
        if admin is None or not is_password_correct(password, admin.hashed_password):
            response_body = {
                "message": "Unauthorized."
            }
            return make_response(jsonify(response_body), 401)

        # Check if session already exists
        admin_session = database_session.scalars(select(AdminSession).where(AdminSession.admin_id == admin.id)).one_or_none()
        session_exists = admin_session is not None

        if session_exists:
            # update existing session
            now = utc_timestamp()
            admin_session.assign_new_session_id()
            admin_session.expires_at = now + DEFAULT_SESSION_DURATION
            database_session.commit()
        
        else:  
            # Create and return new session
            admin_session = AdminSession(admin_id=admin.id)
            database_session.add(admin_session)
            database_session.commit()

        response = make_response("", 204)
        response.set_cookie("session_id", str(admin_session.session_id), httponly=True, secure=True)
        return response
