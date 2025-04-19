import os
import pytest
from sqlalchemy.orm import Session
from flask.testing import FlaskClient
from sqlalchemy import create_engine

from config.config import Config
from database.database import DatabaseEngineProvider
from auth.auth import hash_password
from database.models.admin import Admin
from server.server import server


@pytest.fixture
def database_with_test_data():

    engine = create_engine(f"sqlite:///{Config.DATABASE_PATH}")
    DatabaseEngineProvider.set_database_engine(engine)

    try:
        name = Config.ADMIN_NAME
        email = Config.ADMIN_EMAIL
        password = Config.ADMIN_PASSWORD
    except KeyError:
        raise Exception("Default admin details missing from environement variables.")

    with Session(engine) as session:
        admin = Admin(
            name=name,
            email=email
        )
        admin.hashed_password = hash_password(password)
        session.add(admin)
        session.commit()

    yield engine


@pytest.fixture
def client(database_with_test_data):
    server.config["TESTING"] = True
    with server.test_client() as client:
        yield client


@pytest.fixture
def logged_in_client(database_with_test_data):
    server.config["TESTING"] = True
    with server.test_client() as client:
        admin_email = Config.ADMIN_EMAIL
        admin_password = Config.ADMIN_PASSWORD

        client.post("/admins/login", json={
            "email": admin_email,
            "password": admin_password
        })
        yield client


def test_successful_admin_login(client: FlaskClient, database_with_test_data):
    """
    Verifies that login with correct admin credentials returns 200 and sets the session_id cookie.
    """
    admin_name = Config.ADMIN_NAME
    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD
    response = client.post("/admins/login", json={
        "email": admin_email,
        "password": admin_password
    })

    assert response.status_code == 200
    assert client.get_cookie('session_id') is not None
    assert response.json["name"] == admin_name


def test_admin_login_failed_due_to_missing_credentials(client: FlaskClient, database_with_test_data):
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
        response = client.post("/admins/login", json=body)
        assert response.status_code == 400
        assert client.get_cookie("session_id") is None
        assert response.json["message"] == "Request body is missing login credentials."


def test_admin_login_failed_due_to_invalid_credentials(client: FlaskClient, database_with_test_data):
    """
    Ensures that login attempts with incorrect email/password return 401 and no session cookie.
    """

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
        response = client.post("/admins/login", json=body)
        assert response.status_code == 401
        assert client.get_cookie("session_id") is None
        assert response.json["message"] == "Unauthorized."
    


def test_successful_logout(logged_in_client: FlaskClient, database_with_test_data):
    response = logged_in_client.post("/admins/logout")
    assert response.status_code == 204
    assert logged_in_client.get_cookie("session_id") is None


def test_unsuccessful_logout_due_to_missing_session_id(client: FlaskClient, database_with_test_data):
    response = client.post("/admins/logout")
    assert response.status_code == 400
    assert response.json["message"] == "The session ID cookie is missing."


def test_unsuccessful_logout_due_to_invalid_session_id(client: FlaskClient, database_with_test_data):
    client.set_cookie("session_id", "just a random string")
    response = client.post("/admins/logout")
    assert response.status_code == 422
    assert response.json["message"] == "The session ID is invalid."