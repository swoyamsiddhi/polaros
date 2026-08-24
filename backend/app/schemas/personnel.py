"""Personnel schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PersonnelResponse(BaseModel):
    id: int
    name: str
    role: str
    organisation: str = "NCPOR"
    specialisation: Optional[str] = None
    station_id: Optional[int] = None
    station_name: Optional[str] = None
    destination_id: Optional[int] = None
    destination_name: Optional[str] = None
    travel_status: str = "AT_STATION"
    expected_arrival: Optional[datetime] = None
    expedition_name: Optional[str] = None

    class Config:
        from_attributes = True
