from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base
from database.utils.utils import utc_timestamp



class RegistrationTask(Base):
    __tablename__ = "registration_task"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[UUID] = mapped_column(default=uuid4, unique=True)  # used externally
    ip_address: Mapped[str] = mapped_column(String(39))  # to enable two-way communication
    api_key: str = None
    hashed_api_key: Mapped[Optional[str]] = mapped_column(String(64))
    leds_flashing: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[int] = mapped_column(default=utc_timestamp)


    def admin_view(self) -> dict:
        return {
            "registration_task_id": self.task_id,
            "leds_flashing": self.leds_flashing,
            "created_at": datetime.fromtimestamp(self.created_at, tz=timezone.utc).isoformat()
        }


    def __repr__(self) -> str:
        return (f"<RegistrationTask(id={self.id!r}, task_id={self.task_id!r}, "
                f"ip_address={self.ip_address!r}, api_key={self.api_key!r}, "
                f"hashed_api_key={self.hashed_api_key!r}, leds_flashing={self.leds_flashing!r}, "
                f"created_at={self.created_at!r})>")