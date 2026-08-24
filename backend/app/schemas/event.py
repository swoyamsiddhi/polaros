"""Event schemas."""
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class EventResponse(BaseModel):
    id: int
    event_type: str
    severity: str = "INFO"
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    payload: Optional[Any] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    id: int
    event_type: str
    severity: str
    title: str
    description: str
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    recommendation: str = ""
    status: str = "ACTIVE"
    timestamp: datetime

    class Config:
        from_attributes = True
