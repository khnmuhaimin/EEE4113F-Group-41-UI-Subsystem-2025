from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlalchemy import BigInteger, ForeignKey, String
from database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column

from database.utils.utils import utc_timestamp



class WeighingNode(Base):
    __tablename__ = "weighing_nodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID] = mapped_column(default=uuid4, unique=True)
    location: Mapped[str | None] = mapped_column(String(50), default=None)  # null during registration
    registration_in_progress: Mapped[bool] = mapped_column(default=True)
    leds_flashing: Mapped[bool] = mapped_column(default=False)
    api_key: str = None
    hashed_api_key: Mapped[str | None] = mapped_column(String(64))
    last_pinged_at: Mapped[int] = mapped_column(BigInteger, default=utc_timestamp)
    created_at: Mapped[int] = mapped_column(BigInteger, default=utc_timestamp)

    def registration_in_progress_view(self):
        result = {}
        result["id"] = self.uuid
        result["location"] = self.location
        result["leds_flashing"] = self.leds_flashing
        result["created_at"] = datetime.fromtimestamp(self.created_at, tz=timezone.utc)
        return result
    
    def admin_view(self):
        result = {}
        result["id"] = self.uuid
        result["location"] = self.location
        result["registration_in_progress"] = self.registration_in_progress
        result["leds_flashing"] = self.leds_flashing
        result["last_pinged_at"] = datetime.fromtimestamp(self.last_pinged_at, tz=timezone.utc)
        result["created_at"] = datetime.fromtimestamp(self.created_at, tz=timezone.utc)
        return result
    
    def node_view(self):
        lines = [
            str(self.uuid),
            "null" if self.location is None else str(self.location),
            str(self.registration_in_progress).lower(),
            str(self.leds_flashing).lower(),
            self.last_pinged_at,
            self.created_at,
        ]
        return "\n".join(lines)