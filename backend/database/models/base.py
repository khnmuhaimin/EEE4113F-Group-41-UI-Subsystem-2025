from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    __allow_unmapped__ = True  # allows fields to be any kind of data