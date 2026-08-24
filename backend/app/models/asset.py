"""Asset and MaintenanceTask models."""
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class AssetCategory(str, enum.Enum):
    GENERATOR = "GENERATOR"
    SNOW_VEHICLE = "SNOW_VEHICLE"
    AIRCRAFT = "AIRCRAFT"
    HELICOPTER = "HELICOPTER"
    COMMUNICATION = "COMMUNICATION"
    SCIENTIFIC = "SCIENTIFIC"
    NAVIGATION = "NAVIGATION"
    REFRIGERATION = "REFRIGERATION"
    POWER = "POWER"
    VESSEL = "VESSEL"


class AssetStatus(str, enum.Enum):
    REGISTERED = "REGISTERED"
    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    DEPLOYED = "DEPLOYED"
    IN_USE = "IN_USE"
    MAINTENANCE_REQUIRED = "MAINTENANCE_REQUIRED"
    MAINTENANCE = "MAINTENANCE"
    READY = "READY"
    REDEPLOYED = "REDEPLOYED"
    RETIRED = "RETIRED"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(20), nullable=False)
    serial_number = Column(String(50))
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    custodian = Column(String(100))
    status = Column(String(25), default=AssetStatus.AVAILABLE.value)
    utilisation_pct = Column(Float, default=0)
    engine_hours = Column(Float, default=0)
    maintenance_threshold_hours = Column(Float, default=5000)
    last_maintenance = Column(Date, nullable=True)
    next_maintenance = Column(Date, nullable=True)
    replacement_cost = Column(Float, default=0)
    description = Column(String(300))
    commissioned_date = Column(Date, nullable=True)

    station = relationship("Station", back_populates="assets")
    maintenance_tasks = relationship("MaintenanceTask", back_populates="asset")


class MaintenanceStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"


class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    type = Column(String(50), nullable=False)  # ROUTINE, REPAIR, INSPECTION, OVERHAUL
    status = Column(String(20), default=MaintenanceStatus.SCHEDULED.value)
    description = Column(String(300))
    scheduled_date = Column(Date, nullable=False)
    completed_date = Column(Date, nullable=True)
    technician = Column(String(100))
    notes = Column(String(500))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    asset = relationship("Asset", back_populates="maintenance_tasks")
