from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from auth.auth import hash_password
from config.config import Config
from database.models.base import Base
from database.models import admin, session, weighing_node, weight_reading  # import all tables so they can be created


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