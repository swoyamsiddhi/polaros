"""User and Role models."""
import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    LOGISTICS_OFFICER = "LOGISTICS_OFFICER"
    STATION_MANAGER = "STATION_MANAGER"
    ASSET_MANAGER = "ASSET_MANAGER"
    EXPEDITION_COMMANDER = "EXPEDITION_COMMANDER"
    FIELD_OPERATOR = "FIELD_OPERATOR"
    ANALYST = "ANALYST"
    TRAINER = "TRAINER"
    STUDENT = "STUDENT"


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))
    permissions = Column(String(500))  # JSON string of permissions

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    role = relationship("Role", back_populates="users")
    station = relationship("Station", back_populates="users")
    mission_instances = relationship("MissionInstance", back_populates="user")
    scores = relationship("Score", back_populates="user")
    user_badges = relationship("UserBadge", back_populates="user")
