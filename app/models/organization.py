from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id")),
    Column("activity_id", ForeignKey("activities.id")),
)

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    phones: Mapped[str] = mapped_column(String, nullable=False)  
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))

    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary=organization_activity)
