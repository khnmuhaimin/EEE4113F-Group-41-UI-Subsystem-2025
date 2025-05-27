import csv
import random
from uuid import UUID, uuid4
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
                "location": "Penguin Beach",
                "registration_in_progress": True,
                "uuid": UUID('46c34751-96b2-49e5-bfae-b730be5e00a3'),
                "api_key": "1234",
                "leds_flashing": False
            },
            {
                "location": None,
                "registration_in_progress": True,
                "api_key": generate_secret(),
                "leds_flashing": False,
                "last_pinged_at": utc_timestamp(-86400 * 6),  # one week ago
                "created_at": utc_timestamp(-86400 * 7),  # one week ago
            },
            {
                "location": "Dock 3",
                "registration_in_progress": False,
                "api_key": generate_secret(),
                "leds_flashing": False,
                "created_at": utc_timestamp(-86400 * 365) # one year ago
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
        NUM_READINGS = 100
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

    @classmethod
    def export_weighing_nodes_to_csv(cls, engine):
        with Session(engine) as session:
            nodes = session.scalars(select(WeighingNode)).all()
        with open('weighing-nodes.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'location', 'registration_in_progress', 'hashed_api_key', 'leds_flashing', 'created_at'])
            for node in nodes:
                writer.writerow([
                    node.uuid if node.uuid is not None else 'null',
                    node.location if node.location is not None else 'null',
                    'true' if node.registration_in_progress else 'false',
                    node.hashed_api_key if node.hashed_api_key is not None else 'null',
                    'true' if node.leds_flashing else 'false',
                    node.created_at if node.created_at is not None else 'null',
                ])

    @classmethod
    def export_weight_readings_to_csv(cls, engine):
        with Session(engine) as session:
            readings = session.scalars(select(WeightReading)).all()
        with open('weight-readings.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'node_id', 'penguin_rfid', 'weight', 'created_at'])
            for r in readings:
                writer.writerow([
                    r.node_id if r.node_id is not None else 'null',
                    r.penguin_rfid if r.penguin_rfid is not None else 'null',
                    r.weight if r.weight is not None else 'null',
                    r.created_at if r.created_at is not None else 'null',
                ])

