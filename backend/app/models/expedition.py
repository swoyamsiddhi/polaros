"""Expedition, ExpeditionPersonnel, and ExpeditionCargo models."""
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class ExpeditionStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    APPROVED = "APPROVED"
    PREPARING = "PREPARING"
    READY = "READY"
    ACTIVE = "ACTIVE"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Priority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Expedition(Base):
    __tablename__ = "expeditions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    origin = Column(String(100), default="Goa, India")
    destination_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    priority = Column(String(10), default=Priority.MEDIUM.value)
    status = Column(String(20), default=ExpeditionStatus.PLANNED.value)
    mission_objectives = Column(String(1000))
    readiness_score = Column(Float, default=0)
    risk_score = Column(Float, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    destination = relationship("Station")
    personnel = relationship("ExpeditionPersonnel", back_populates="expedition")
    cargo = relationship("ExpeditionCargo", back_populates="expedition")
    shipments = relationship("Shipment", back_populates="expedition")


class ExpeditionPersonnel(Base):
    __tablename__ = "expedition_personnel"

    id = Column(Integer, primary_key=True, index=True)
    expedition_id = Column(Integer, ForeignKey("expeditions.id"), nullable=False)
    personnel_id = Column(Integer, ForeignKey("personnel.id"), nullable=False)
    role_in_expedition = Column(String(50))

    expedition = relationship("Expedition", back_populates="personnel")
    personnel = relationship("Personnel", back_populates="expedition_assignments")


class ExpeditionCargo(Base):
    __tablename__ = "expedition_cargo"

    id = Column(Integer, primary_key=True, index=True)
    expedition_id = Column(Integer, ForeignKey("expeditions.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    required_quantity = Column(Float, nullable=False)
    fulfilled_quantity = Column(Float, default=0)

    expedition = relationship("Expedition", back_populates="cargo")
    item = relationship("Item")
