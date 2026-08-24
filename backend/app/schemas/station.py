"""Station schemas."""
from pydantic import BaseModel
from typing import Optional


class StationResponse(BaseModel):
    id: int
    name: str
    code: str
    type: str
    latitude: float
    longitude: float
    altitude: float = 0
    capacity: int
    current_occupancy: int = 0
    status: str
    comm_status: str = "ONLINE"
    description: Optional[str] = None
    established_year: Optional[int] = None
    country: str = "India"
    region: Optional[str] = None
    personnel_count: int = 0
    asset_count: int = 0
    alert_count: int = 0

    class Config:
        from_attributes = True


class StationDetail(StationResponse):
    personnel: list = []
    assets: list = []
    inventory: list = []
    weather: Optional[dict] = None
    active_expeditions: list = []
