from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base
from database.utils.utils import utc_timestamp



class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(254), unique=True)
    password: str = None
    hashed_password: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[int] = mapped_column(default=utc_timestamp)


    def __repr__(self) -> str:
        return (f"<RegistrationTask(id={self.id}, "
                f"name={self.name}, "
                f"email={self.email}, "
                f"created_at={self.created_at})>")