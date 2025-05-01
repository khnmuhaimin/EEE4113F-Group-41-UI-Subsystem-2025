from typing import Generator
from flask.testing import FlaskClient
import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from auth.auth import hash_password
from server.server import server
from database.models.admin import Admin
from database.database import DatabaseEngineProvider
from config.config import Config


@pytest.fixture
def database_engine() -> Generator[Engine, None, None]:
    engine = create_engine(f"sqlite:///{Config.DATABASE_PATH}")
    DatabaseEngineProvider.set_database_engine(engine)
    yield engine


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    server.config["TESTING"] = True
    with server.test_client() as client:
        yield client


@pytest.fixture
def default_admin_client(database_engine: Engine) -> Generator[FlaskClient, None, None]:
    insert_default_admin(database_engine)
    server.config["TESTING"] = True
    with server.test_client() as client:
        login_default_admin(client)
        yield client


def insert_default_admin(database_engine: Engine) -> None:
    name = Config.ADMIN_NAME
    email = Config.ADMIN_EMAIL
    password = Config.ADMIN_PASSWORD

    with Session(database_engine) as session:
        admin = Admin(
            name=name,
            email=email
        )
        admin.hashed_password = hash_password(password)
        session.add(admin)
        session.commit()


def login_default_admin(client: FlaskClient) -> None:
    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD

    client.post("/api/admins/login", json={
        "email": admin_email,
        "password": admin_password
    })