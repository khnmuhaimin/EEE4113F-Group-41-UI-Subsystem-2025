import random
from uuid import uuid4
import numpy as np
from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session
from log.log import logger

from auth.auth import generate_secret, hash_password, hash_secret
from database.utils.utils import utc_timestamp
from config.config import Config
from database.models.base import Base
from database.models import admin, session, weighing_node, weight_reading  # import all tables so they can be created
from database.models.weighing_node import WeighingNode
from database.models.weight_reading import WeightReading


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
                "location": "Warehouse A",
                "registration_in_progress": False,
                "api_key": generate_secret(),
                "leds_flashing": False,
                "created_at": utc_timestamp(86400)  # one day ago
            },
            {
                "location": None,
                "registration_in_progress": True,
                "api_key": generate_secret(),
                "leds_flashing": False,
                "created_at": utc_timestamp(86400 * 7),  # one week ago
            },
            {
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

    @classmethod
    def load_default_weight_readings(cls, engine: Engine):
        NUM_READINGS = 50
        NUM_PENGUINS = 10
        penguin_rfids = [str(uuid4()) for _ in range(NUM_PENGUINS)]
        node_ids = []
        with Session(engine) as session:
            node_ids = [node.id for node in session.scalars(select(WeighingNode)).all()]
        readings = []
        for _ in range(NUM_READINGS):
            reading = {
                "node_id": random.choice(node_ids),
                "penguin_rfid": random.choice(penguin_rfids),
                "weight": round(np.random.normal(loc=3100, scale=500), 2),
                "created_at": utc_timestamp(offset=random.randint(-1_000_000, 0))
            }
            readings.append(reading)
        with Session(engine) as session:
            for reading in readings:
                session.add(
                    WeightReading(**reading)
                )
            session.commit()
        with Session(engine) as session:
            readings = session.scalars(select(WeightReading).order_by(WeightReading.created_at)).all()
