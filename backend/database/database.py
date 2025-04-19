from sqlalchemy import create_engine
from config.config import Config
from database.models.base import Base
# import all tables so they can be created
from database.models.admin import *
from database.models.session import *
from database.models.weighing_node import *
from database.models.weight_reading import *


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
