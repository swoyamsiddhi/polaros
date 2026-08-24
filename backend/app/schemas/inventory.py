"""Inventory schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class InventoryResponse(BaseModel):
    id: int
    station_id: int
    station_name: str = ""
    item_id: int
    item_name: str = ""
    item_category: str = ""
    item_unit: str = ""
    criticality: str = "MEDIUM"
    quantity: float
    reserved_quantity: float = 0
    available_quantity: float = 0
    batch_number: Optional[str] = None
    expiry_date: Optional[date] = None
    avg_daily_consumption: float = 0
    min_stock: int = 0
    max_stock: int = 0
    stock_status: str = "NORMAL"  # NORMAL, LOW, CRITICAL, EXPIRING

    class Config:
        from_attributes = True


class InventoryAlert(BaseModel):
    id: int
    alert_type: str  # LOW_STOCK, CRITICAL_STOCK, EXPIRING, MISSION_CONFLICT, UNAVAILABLE
    severity: str
    title: str
    description: str
    station_name: str
    item_name: str
    current_quantity: float
    threshold: float
    recommendation: str
    timestamp: datetime


class InventoryForecast(BaseModel):
    item_name: str
    station_name: str
    current_stock: float
    unit: str
    daily_consumption: float
    critical_threshold: float
    days_to_critical: float
    projected_critical_date: Optional[date] = None
    next_resupply: Optional[date] = None
    risk: str  # LOW, MEDIUM, HIGH, CRITICAL
    recommendation: str
    projection_data: list = []  # [{day, projected_stock, threshold}]
