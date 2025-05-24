from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.utils.utils import utc_timestamp
from database.models.base import Base



class WeightReading(Base):
    __tablename__ = "weight_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    node_id: Mapped[int] = mapped_column(ForeignKey("weighing_nodes.id"))
    penguin_rfid: Mapped[int] = mapped_column(BigInteger)
    weight: Mapped[float] = mapped_column()
    created_at: Mapped[int] = mapped_column(BigInteger, default=utc_timestamp)
