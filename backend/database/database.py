from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from auth.auth import generate_secret, hash_password, hash_secret
from database.utils.utils import utc_timestamp
from config.config import Config
from database.models.base import Base
from database.models import admin, session, weighing_node, weight_reading  # import all tables so they can be created
from database.models.weighing_node import WeighingNode


class DatabaseEngineProvider:

    database_engine = None

    @classmethod
    def set_database_engine(cls, engine):
        cls.database_engine = engine
        Base.metadata.create_all(engine)

    @classmethod
    def get_database_engine(cls):
        if cls.database_engine is None:
            engine = create_engine(f"sqlite:///{Config.DATABASE_PATH}")
            cls.set_database_engine(engine)
        return cls.database_engine
    
    @classmethod
    def load_default_database(cls):
        cls.get_database_engine()


class DefaultDataProvider:

    @classmethod
    def load_default_admin(cls, engine: Engine):
        with Session(engine) as session:
            default_admin = admin.Admin(
                name=Config.ADMIN_NAME,
                email=Config.ADMIN_EMAIL,
                hashed_password=hash_password(Config.ADMIN_PASSWORD)
            )
            session.add(default_admin)
            session.commit()


    @classmethod
    def load_default_nodes(cls, engine: Engine):
        mock_nodes = [
            {
                "ip_address": "192.168.0.2",
                "location": "Warehouse A",
                "registration_in_progress": False,
                "api_key": generate_secret(),
                "leds_flashing": False,
                "created_at": utc_timestamp(86400)  # one day ago
            },
            {
                "ip_address": "192.168.0.3",
                "location": None,
                "registration_in_progress": True,
                "api_key": generate_secret(),
                "leds_flashing": True,
                "created_at": utc_timestamp(86400 * 7),  # one week ago
            },
            {
                "ip_address": "fe80::1",
                "location": "Dock 3",
                "registration_in_progress": False,
                "api_key": generate_secret(),
                "leds_flashing": False,
                "created_at": utc_timestamp(86400 * 365) # one year ago
            }
        ]
        for node in mock_nodes:
            node["hashed_api_key"] = hash_secret(node["api_key"])
        with Session(engine) as session:
            for node in mock_nodes:
                session.add(
                    WeighingNode(**node)
                )
            session.commit()