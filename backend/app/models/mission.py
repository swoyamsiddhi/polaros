"""Mission, MissionInstance, and MissionEvent models."""
import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class MissionDifficulty(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXTREME = "EXTREME"


class MissionStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class InstanceStatus(str, enum.Enum):
    BRIEFING = "BRIEFING"
    RESOURCE_ALLOCATION = "RESOURCE_ALLOCATION"
    ROUTE_SELECTION = "ROUTE_SELECTION"
    EXECUTING = "EXECUTING"
    RANDOM_EVENT = "RANDOM_EVENT"
    DECISION = "DECISION"
    RESULT = "RESULT"
    DEBRIEF = "DEBRIEF"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(30), unique=True)
    description = Column(String(500))
    difficulty = Column(String(10), default=MissionDifficulty.MEDIUM.value)
    objectives = Column(Text)  # JSON
    constraints = Column(Text)  # JSON
    initial_state = Column(Text)  # JSON - starting resources
    events_script = Column(Text)  # JSON - scripted random events
    time_limit = Column(Integer, default=300)  # seconds
    category = Column(String(30))  # RESUPPLY, RESCUE, MAINTENANCE, SCIENTIFIC
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=True)

    instances = relationship("MissionInstance", back_populates="mission")


class MissionInstance(Base):
    __tablename__ = "mission_instances"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(25), default=InstanceStatus.BRIEFING.value)
    state = Column(Text)  # JSON - current game state (fuel, inventory, vehicles, etc.)
    phase = Column(String(25), default="BRIEFING")
    turn = Column(Integer, default=0)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    mission = relationship("Mission", back_populates="instances")
    user = relationship("User", back_populates="mission_instances")
    events = relationship("MissionEvent", back_populates="instance")
    score = relationship("Score", back_populates="instance", uselist=False)


class MissionEvent(Base):
    __tablename__ = "mission_events"

    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer, ForeignKey("mission_instances.id"), nullable=False)
    turn = Column(Integer, default=0)
    event_type = Column(String(40), nullable=False)
    title = Column(String(200))
    description = Column(String(500))
    options = Column(Text)  # JSON - available choices
    player_choice = Column(String(50), nullable=True)
    outcome = Column(Text)  # JSON - consequences of the choice
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    instance = relationship("MissionInstance", back_populates="events")
