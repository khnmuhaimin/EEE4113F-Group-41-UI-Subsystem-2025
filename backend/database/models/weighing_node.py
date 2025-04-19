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
    ip_address: Mapped[str] = mapped_column(String(39), unique=True)  # to enable two-way communication during registration. can be null afterwards.
    location: Mapped[str | None] = mapped_column(String(50), default=None)  # null during registration
    registration_in_progress: Mapped[bool] = mapped_column(default=True)
    leds_flashing: Mapped[bool] = mapped_column(default=False)
    api_key: str = None
    hashed_api_key: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[int] = mapped_column(BigInteger, default=utc_timestamp)

    def registration_in_progress_view(self):
        result = {}
        result["id"] = self.uuid
        result["location"] = self.location
        result["leds_flashing"] = self.leds_flashing
        result["created_at"] = datetime.fromtimestamp(self.created_at, tz=timezone.utc)
        return result
