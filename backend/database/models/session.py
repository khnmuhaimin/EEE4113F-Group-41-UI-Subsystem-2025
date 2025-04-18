from uuid import UUID, uuid4
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base
from database.utils.utils import utc_timestamp



DEFAULT_SESSION_DURATION = 1800  # 1800 seconds = 30 minutes

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("admins.id"), unique=True)
    session_id: Mapped[UUID] = mapped_column(default=uuid4, unique=True)  # used externally
    expires_at: Mapped[int] = mapped_column(BigInteger, default=lambda: utc_timestamp(offset=DEFAULT_SESSION_DURATION))  # expires after 30 minutes
    created_at: Mapped[int] = mapped_column(BigInteger, default=utc_timestamp)

    def assign_new_session_id(self):
        self.session_id = uuid4()