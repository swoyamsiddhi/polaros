"""Inventory and InventoryTransaction models."""
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Float, default=0)
    reserved_quantity = Column(Float, default=0)
    batch_number = Column(String(50))
    expiry_date = Column(Date, nullable=True)
    avg_daily_consumption = Column(Float, default=0)
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    station = relationship("Station", back_populates="inventory")
    item = relationship("Item", back_populates="inventory_records")
    transactions = relationship("InventoryTransaction", back_populates="inventory")

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity


class TransactionType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"
    RESERVE = "RESERVE"
    RELEASE = "RELEASE"
    ADJUST = "ADJUST"
    CONSUME = "CONSUME"


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    type = Column(String(10), nullable=False)
    quantity = Column(Float, nullable=False)
    reference = Column(String(100))  # e.g., "EXP-2026-014", "SHP-204"
    notes = Column(String(300))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    inventory = relationship("Inventory", back_populates="transactions")
