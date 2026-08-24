"""Score, Badge, and UserBadge models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer, ForeignKey("mission_instances.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total = Column(Integer, default=0)
    safety = Column(Float, default=0)  # 0-100
    efficiency = Column(Float, default=0)  # 0-100
    accuracy = Column(Float, default=0)  # 0-100
    resource_usage = Column(Float, default=0)  # 0-100
    breakdown = Column(Text)  # JSON: [{action, points, reason}]
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    instance = relationship("MissionInstance", back_populates="score")
    user = relationship("User", back_populates="scores")


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(30), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(200))
    icon = Column(String(50))  # emoji or icon name
    criteria = Column(Text)  # JSON: conditions for earning
    category = Column(String(30))

    user_badges = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    instance_id = Column(Integer, ForeignKey("mission_instances.id"), nullable=True)
    earned_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="user_badges")
    badge = relationship("Badge", back_populates="user_badges")
