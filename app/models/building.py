from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")
