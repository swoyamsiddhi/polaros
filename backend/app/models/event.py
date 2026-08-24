"""Event model — the backbone of the event-driven architecture."""
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from datetime import datetime, timezone
from app.database import Base


class EventType(str, enum.Enum):
    # Shipment events
    SHIPMENT_CREATED = "SHIPMENT_CREATED"
    SHIPMENT_LOADED = "SHIPMENT_LOADED"
    SHIPMENT_DEPARTED = "SHIPMENT_DEPARTED"
    SHIPMENT_DELAYED = "SHIPMENT_DELAYED"
    SHIPMENT_ARRIVED = "SHIPMENT_ARRIVED"
    SHIPMENT_CANCELLED = "SHIPMENT_CANCELLED"
    # Weather events
    WEATHER_DETERIORATION = "WEATHER_DETERIORATION"
    WEATHER_IMPROVEMENT = "WEATHER_IMPROVEMENT"
    WEATHER_EXTREME = "WEATHER_EXTREME"
    # Asset events
    ASSET_FAILURE = "ASSET_FAILURE"
    ASSET_MAINTENANCE_DUE = "ASSET_MAINTENANCE_DUE"
    ASSET_REPAIRED = "ASSET_REPAIRED"
    # Inventory events
    STOCK_LOW = "STOCK_LOW"
    STOCK_CRITICAL = "STOCK_CRITICAL"
    STOCK_EXPIRING = "STOCK_EXPIRING"
    STOCK_REPLENISHED = "STOCK_REPLENISHED"
    # Personnel events
    PERSONNEL_DELAYED = "PERSONNEL_DELAYED"
    PERSONNEL_ARRIVED = "PERSONNEL_ARRIVED"
    # Expedition events
    EXPEDITION_RISK_CHANGED = "EXPEDITION_RISK_CHANGED"
    EXPEDITION_READINESS_CHANGED = "EXPEDITION_READINESS_CHANGED"
    # System events
    ALERT_CREATED = "ALERT_CREATED"
    RECOMMENDATION_CREATED = "RECOMMENDATION_CREATED"
    RISK_RECALCULATED = "RISK_RECALCULATED"
    # Vehicle events
    VEHICLE_BREAKDOWN = "VEHICLE_BREAKDOWN"
    AIRCRAFT_DELAYED = "AIRCRAFT_DELAYED"
    # Misc
    CARGO_MISSING = "CARGO_MISSING"
    COMMUNICATION_LOSS = "COMMUNICATION_LOSS"
    FUEL_LEAK = "FUEL_LEAK"
    EMERGENCY_MEDICAL = "EMERGENCY_MEDICAL"


class Severity(str, enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(40), nullable=False, index=True)
    severity = Column(String(10), default=Severity.INFO.value)
    entity_type = Column(String(30))  # shipment, asset, inventory, expedition, station
    entity_id = Column(Integer)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(200))
    description = Column(String(500))
    payload = Column(Text)  # JSON string
    processed = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
