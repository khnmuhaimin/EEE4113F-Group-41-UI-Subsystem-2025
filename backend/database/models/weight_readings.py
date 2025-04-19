from sqlalchemy import BigInteger, ForeignKey
from backend.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column



class WeightReadings(Base):
    __tablename__ = "weight_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    node_id: Mapped[int] = mapped_column(ForeignKey("weighing_nodes.id"))
    penguin_rfid: Mapped[int] = mapped_column(BigInteger)
    towards_ocean: Mapped[bool]
    weight: Mapped[float]
    created_at: Mapped[int] = mapped_column(BigInteger)
