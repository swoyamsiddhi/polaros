"""Risk prediction and Recommendation models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from datetime import datetime, timezone
from app.database import Base


class RiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    expedition_id = Column(Integer, ForeignKey("expeditions.id"), nullable=False)
    risk_score = Column(Float, nullable=False)  # 0-100
    risk_level = Column(String(10), nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    factors = Column(Text)  # JSON: [{name, score, contribution_pct, explanation}]
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=True)
    expedition_id = Column(Integer, ForeignKey("expeditions.id"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500))
    action = Column(String(300))
    priority = Column(String(10), default="MEDIUM")
    status = Column(String(20), default="PENDING")  # PENDING, ACCEPTED, DISMISSED
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
