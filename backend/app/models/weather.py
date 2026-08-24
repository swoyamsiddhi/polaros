"""Weather observation model."""
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class WeatherSeverity(str, enum.Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    WARNING = "WARNING"
    SEVERE = "SEVERE"
    EXTREME = "EXTREME"


class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    temperature = Column(Float)  # Celsius
    wind_speed = Column(Float)  # km/h
    visibility = Column(Float)  # km
    precipitation = Column(String(30))  # none, light_snow, heavy_snow, blizzard, rain
    humidity = Column(Float)  # %
    pressure = Column(Float)  # hPa
    severity = Column(String(10), default=WeatherSeverity.NORMAL.value)
    forecast_summary = Column(String(300))
    forecast_window = Column(Integer, default=24)  # hours
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    station = relationship("Station", back_populates="weather_observations")
