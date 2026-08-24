"""Shipment schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ShipmentLegResponse(BaseModel):
    id: int
    shipment_id: int
    sequence: int
    origin: str
    destination: str
    mode: str
    vehicle: Optional[str] = None
    planned_departure: Optional[datetime] = None
    planned_arrival: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    status: str = "PLANNED"
    cargo_description: Optional[str] = None
    distance_km: float = 0

    class Config:
        from_attributes = True


class ShipmentResponse(BaseModel):
    id: int
    code: str
    expedition_id: Optional[int] = None
    expedition_code: str = ""
    origin: str
    destination: str
    status: str = "PLANNED"
    priority: str = "MEDIUM"
    total_weight: float = 0
    cargo_description: Optional[str] = None
    legs_count: int = 0
    completed_legs: int = 0
    current_leg: Optional[ShipmentLegResponse] = None
    created_at: Optional[datetime] = None
    predicted_delay: Optional[float] = None
    delay_confidence: Optional[float] = None

    class Config:
        from_attributes = True


class ShipmentDetail(ShipmentResponse):
    legs: list[ShipmentLegResponse] = []
    timeline: list = []
    delay_prediction: Optional[dict] = None
