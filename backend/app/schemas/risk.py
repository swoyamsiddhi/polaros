"""Risk schemas."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RiskFactor(BaseModel):
    name: str
    score: float
    contribution_pct: float
    explanation: str


class RiskResponse(BaseModel):
    expedition_id: int
    expedition_name: str = ""
    risk_score: float
    risk_level: str
    factors: list[RiskFactor] = []
    recommendations: list[dict] = []
    timestamp: Optional[datetime] = None


class RecommendationResponse(BaseModel):
    id: int
    event_id: Optional[int] = None
    expedition_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    action: Optional[str] = None
    priority: str = "MEDIUM"
    status: str = "PENDING"
    timestamp: datetime

    class Config:
        from_attributes = True
