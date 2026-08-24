"""Asset schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class AssetResponse(BaseModel):
    id: int
    code: str
    name: str
    category: str
    serial_number: Optional[str] = None
    station_id: Optional[int] = None
    station_name: str = ""
    custodian: Optional[str] = None
    status: str = "AVAILABLE"
    utilisation_pct: float = 0
    engine_hours: float = 0
    maintenance_threshold_hours: float = 5000
    last_maintenance: Optional[date] = None
    next_maintenance: Optional[date] = None
    replacement_cost: float = 0
    description: Optional[str] = None
    maintenance_risk: float = 0  # 0-100

    class Config:
        from_attributes = True


class MaintenanceTaskResponse(BaseModel):
    id: int
    asset_id: int
    asset_name: str = ""
    type: str
    status: str
    description: Optional[str] = None
    scheduled_date: date
    completed_date: Optional[date] = None
    technician: Optional[str] = None

    class Config:
        from_attributes = True


class MaintenancePrediction(BaseModel):
    asset_id: int
    asset_name: str
    category: str
    engine_hours: float
    threshold: float
    utilisation_pct: float
    recent_faults: int
    risk_score: float  # 0-100
    risk_level: str
    factors: list[dict]
    recommendation: str
