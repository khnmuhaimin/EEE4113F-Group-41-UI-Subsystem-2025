import os
from sqlalchemy import create_engine
from database.models.base import Base
# import all tables so they can be created
import database.models.registration_task

def get_database_path() -> str:
    try:
        server_mode = os.environ["SERVER_MODE"]
    except KeyError:
        raise KeyError("Server mode was not found in the environment variables.")
    if server_mode != "TEST":
        return ":memory:"
    else:
        try:
            return os.environ["DATABASE_PATH"]
        except KeyError as e:
            raise KeyError("Database path was not found in the environment variables.")


database_engine = create_engine(f"sqlite:///{get_database_path()}")  
Base.metadata.create_all(database_engine)