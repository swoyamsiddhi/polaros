"""Shipment and ShipmentLeg models."""
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class ShipmentStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    BOOKED = "BOOKED"
    LOADED = "LOADED"
    IN_TRANSIT = "IN_TRANSIT"
    DELAYED = "DELAYED"
    ARRIVED = "ARRIVED"
    CANCELLED = "CANCELLED"


class TransportMode(str, enum.Enum):
    SEA = "SEA"
    AIR = "AIR"
    HELICOPTER = "HELICOPTER"
    SNOW_VEHICLE = "SNOW_VEHICLE"
    TRACKED_VEHICLE = "TRACKED_VEHICLE"
    ROAD = "ROAD"


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, nullable=False)
    expedition_id = Column(Integer, ForeignKey("expeditions.id"), nullable=True)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    status = Column(String(20), default=ShipmentStatus.PLANNED.value)
    priority = Column(String(10), default="MEDIUM")
    total_weight = Column(Float, default=0)
    cargo_description = Column(String(500))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    expedition = relationship("Expedition", back_populates="shipments")
    legs = relationship("ShipmentLeg", back_populates="shipment", order_by="ShipmentLeg.sequence")


class ShipmentLeg(Base):
    __tablename__ = "shipment_legs"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    mode = Column(String(20), nullable=False)
    vehicle = Column(String(100))
    planned_departure = Column(DateTime, nullable=True)
    planned_arrival = Column(DateTime, nullable=True)
    actual_departure = Column(DateTime, nullable=True)
    actual_arrival = Column(DateTime, nullable=True)
    status = Column(String(20), default=ShipmentStatus.PLANNED.value)
    cargo_description = Column(String(300))
    distance_km = Column(Float, default=0)

    shipment = relationship("Shipment", back_populates="legs")
