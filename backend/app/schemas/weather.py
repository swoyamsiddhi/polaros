"""Weather schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WeatherResponse(BaseModel):
    id: int
    station_id: int
    station_name: str = ""
    temperature: Optional[float] = None
    wind_speed: Optional[float] = None
    visibility: Optional[float] = None
    precipitation: Optional[str] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    severity: str = "NORMAL"
    forecast_summary: Optional[str] = None
    forecast_window: int = 24
    timestamp: datetime

    class Config:
        from_attributes = True
