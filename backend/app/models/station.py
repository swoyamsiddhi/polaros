"""Station model — research stations and field camps."""
import enum
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class StationType(str, enum.Enum):
    ANTARCTIC = "ANTARCTIC"
    ARCTIC = "ARCTIC"
    HIMALAYAN = "HIMALAYAN"
    FIELD_CAMP = "FIELD_CAMP"
    WAREHOUSE = "WAREHOUSE"
    PORT = "PORT"


class StationStatus(str, enum.Enum):
    OPERATIONAL = "OPERATIONAL"
    LIMITED = "LIMITED"
    MAINTENANCE = "MAINTENANCE"
    CLOSED = "CLOSED"


class CommStatus(str, enum.Enum):
    ONLINE = "ONLINE"
    INTERMITTENT = "INTERMITTENT"
    OFFLINE = "OFFLINE"


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    type = Column(String(20), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude = Column(Float, default=0)
    capacity = Column(Integer, default=50)
    current_occupancy = Column(Integer, default=0)
    status = Column(String(20), default=StationStatus.OPERATIONAL.value)
    comm_status = Column(String(20), default=CommStatus.ONLINE.value)
    description = Column(String(500))
    established_year = Column(Integer)
    country = Column(String(50), default="India")
    region = Column(String(100))
    image_url = Column(String(300))

    users = relationship("User", back_populates="station")
    personnel = relationship("Personnel", back_populates="station", foreign_keys="[Personnel.station_id]")
    inventory = relationship("Inventory", back_populates="station")
    assets = relationship("Asset", back_populates="station")
    weather_observations = relationship("WeatherObservation", back_populates="station")
