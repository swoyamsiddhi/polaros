"""Personnel model — expedition team members."""
import enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class TravelStatus(str, enum.Enum):
    AT_STATION = "AT_STATION"
    IN_TRANSIT = "IN_TRANSIT"
    AT_FIELD_CAMP = "AT_FIELD_CAMP"
    DEPARTED = "DEPARTED"
    DELAYED = "DELAYED"
    RETURNING = "RETURNING"


class Personnel(Base):
    __tablename__ = "personnel"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    organisation = Column(String(100), default="NCPOR")
    specialisation = Column(String(100))
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    destination_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    travel_status = Column(String(20), default=TravelStatus.AT_STATION.value)
    expected_arrival = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    contact = Column(String(100))

    station = relationship("Station", back_populates="personnel", foreign_keys=[station_id])
    destination = relationship("Station", foreign_keys=[destination_id])
    expedition_assignments = relationship("ExpeditionPersonnel", back_populates="personnel")
