from sqlalchemy import BigInteger, ForeignKey, String
from backend.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column



class WeighingNodes(Base):
    __tablename__ = "weighing_nodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    api_key: str = None
    hashed_api_key: Mapped[str | None] = mapped_column(String(64))
    location: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[int] = mapped_column(BigInteger)
