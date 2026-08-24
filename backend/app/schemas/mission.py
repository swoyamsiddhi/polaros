"""Mission and gamification schemas."""
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class MissionResponse(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    difficulty: str = "MEDIUM"
    category: Optional[str] = None
    time_limit: int = 300
    objectives: Optional[Any] = None
    constraints: Optional[Any] = None
    station_id: Optional[int] = None
    station_name: str = ""

    class Config:
        from_attributes = True


class MissionInstanceResponse(BaseModel):
    id: int
    mission_id: int
    mission_name: str = ""
    user_id: int
    status: str = "BRIEFING"
    state: Optional[Any] = None
    phase: str = "BRIEFING"
    turn: int = 0
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MissionAction(BaseModel):
    instance_id: int
    action: str  # dispatch_vehicle, prioritize_cargo, wait, reroute, etc.
    choice: Optional[str] = None  # A, B, C, D
    parameters: Optional[dict] = None


class MissionEventResponse(BaseModel):
    id: int
    turn: int
    event_type: str
    title: Optional[str] = None
    description: Optional[str] = None
    options: Optional[Any] = None
    player_choice: Optional[str] = None
    outcome: Optional[Any] = None
    timestamp: datetime

    class Config:
        from_attributes = True


class ScoreResponse(BaseModel):
    id: int
    instance_id: int
    user_id: int
    user_name: str = ""
    total: int = 0
    safety: float = 0
    efficiency: float = 0
    accuracy: float = 0
    resource_usage: float = 0
    breakdown: Optional[Any] = None
    mission_name: str = ""
    timestamp: datetime

    class Config:
        from_attributes = True


class BadgeResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    earned: bool = False
    earned_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DebriefResponse(BaseModel):
    score: ScoreResponse
    events: list[MissionEventResponse] = []
    badges_earned: list[BadgeResponse] = []
    successes: list[str] = []
    improvements: list[str] = []
    recommended_lesson: str = ""
    decision_timeline: list[dict] = []


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    user_name: str
    total_score: int
    missions_completed: int
    badges_count: int
    best_safety: float = 0
    best_efficiency: float = 0
