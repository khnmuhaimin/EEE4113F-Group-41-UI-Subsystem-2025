import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from auth.auth import hash_password
from database.models.base import Base
# import all tables so they can be created
from database.models.admin import Admin
from database.models.session import Session as AdminSession

def get_database_path() -> str:
    server_mode = os.environ["SERVER_MODE"]
    return os.environ[f"{server_mode}_DATABASE_PATH"]

database_engine = create_engine(f"sqlite:///{get_database_path()}")  
Base.metadata.create_all(database_engine)


# will always be present
# not a good idea for production but itll work for now
try:
    name = os.environ["ADMIN_NAME"]
    email = os.environ["ADMIN_EMAIL"]
    password = os.environ["ADMIN_PASSWORD"]
except KeyError:
    raise Exception("Default admin details missing from environement variables.")

with Session(database_engine) as session:
    admin = Admin(
        name=name,
        email=email
    )
    admin.hashed_password = hash_password(password)
    session.add(admin)
    session.commit()