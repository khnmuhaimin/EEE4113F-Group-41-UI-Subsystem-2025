from flask.testing import FlaskClient
from sqlalchemy import Engine

from config.config import Config
from tests.utils import client, database_engine, insert_default_admin, default_admin_client


def test_successful_admin_login(client: FlaskClient, database_engine: Engine):
    """
    Verifies that login with correct admin credentials returns 200 and sets the session_id cookie.
    """
    insert_default_admin(database_engine)
    admin_name = Config.ADMIN_NAME
    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD
    response = client.post("/api/admins/login", json={
        "email": admin_email,
        "password": admin_password
    })

    assert response.status_code == 200
    assert client.get_cookie("session_id") is not None
    assert response.json["name"] == admin_name


def test_admin_login_failed_due_to_missing_credentials(client: FlaskClient):
    """
    Checks that requests missing login fields return 400 with a relevant message and no session cookie.
    """

    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD

    bodies = [
        {
        },
        {
            "email": admin_email
        },
        {
            "password": admin_password
        }
    ]
    for body in bodies:
        response = client.post("/api/admins/login", json=body)
        assert response.status_code == 400
        assert client.get_cookie("session_id") is None
        assert response.json["message"] == "Request body is missing login credentials."


def test_admin_login_failed_due_to_invalid_credentials(client: FlaskClient, database_engine: Engine):
    """
    Ensures that login attempts with incorrect email/password return 401 and no session cookie.
    """
    insert_default_admin(database_engine)
    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD
    
    bodies = [
        {
            "email": admin_email,
            "password": "this is the wrong password"
        },
        {
            "email": "this is the wrong email",
            "password": admin_password
        },
        {
            "email": "this is the wrong email",
            "password": "and the password is wrong too"
        }
    ]
    for body in bodies:
        response = client.post("/api/admins/login", json=body)
        assert response.status_code == 401
        assert client.get_cookie("session_id") is None
        assert response.json["message"] == "Unauthorized."
    


def test_successful_logout(default_admin_client: FlaskClient, database_engine: Engine):
    response = default_admin_client.post("/api/admins/logout")
    assert response.status_code == 204
    assert default_admin_client.get_cookie("session_id") is None


def test_unsuccessful_logout_due_to_missing_session_id(client: FlaskClient, database_engine: Engine):
    response = client.post("/api/admins/logout")
    assert response.status_code == 400
    assert response.json["message"] == "The session ID cookie is missing."


def test_unsuccessful_logout_due_to_invalid_session_id(client: FlaskClient, database_engine: Engine):
    client.set_cookie("session_id", "just a random string")
    response = client.post("/api/admins/logout")
    assert response.status_code == 422
    assert response.json["message"] == "The session ID is invalid."