"""Expedition schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class ExpeditionResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    origin: str = "Goa, India"
    destination_station_id: int
    destination_name: str = ""
    start_date: date
    end_date: date
    priority: str = "MEDIUM"
    status: str = "PLANNED"
    readiness_score: float = 0
    risk_score: float = 0
    risk_level: str = "LOW"
    personnel_count: int = 0
    cargo_items: int = 0
    shipment_count: int = 0
    mission_objectives: Optional[str] = None

    class Config:
        from_attributes = True


class ExpeditionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    origin: str = "Goa, India"
    destination_station_id: int
    start_date: date
    end_date: date
    priority: str = "MEDIUM"
    mission_objectives: Optional[str] = None


class CargoItem(BaseModel):
    id: int
    item_id: int
    item_name: str
    category: str
    unit: str
    required_quantity: float
    fulfilled_quantity: float
    fulfillment_pct: float = 0


class ExpeditionDetail(ExpeditionResponse):
    personnel: list = []
    cargo: list[CargoItem] = []
    shipments: list = []
    readiness_breakdown: dict = {}
    risk_breakdown: list = []
    recommendations: list = []
    timeline: list = []
