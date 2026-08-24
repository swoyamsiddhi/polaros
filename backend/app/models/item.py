"""Item model — catalog of trackable supply/equipment items."""
import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database import Base


class ItemCategory(str, enum.Enum):
    FUEL = "FUEL"
    FOOD = "FOOD"
    MEDICAL = "MEDICAL"
    COMMUNICATION = "COMMUNICATION"
    SCIENTIFIC = "SCIENTIFIC"
    SPARE_PARTS = "SPARE_PARTS"
    CLOTHING = "CLOTHING"
    SHELTER = "SHELTER"
    TOOLS = "TOOLS"
    SAFETY = "SAFETY"
    POWER = "POWER"
    WATER = "WATER"


class Criticality(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(20), nullable=False)
    unit = Column(String(20), nullable=False)  # L, kg, units, pcs
    criticality = Column(String(10), default=Criticality.MEDIUM.value)
    min_stock = Column(Integer, default=10)
    max_stock = Column(Integer, default=1000)
    expiry_required = Column(Boolean, default=False)
    description = Column(String(300))
    weight_per_unit = Column(Integer, default=1)  # kg

    inventory_records = relationship("Inventory", back_populates="item")
