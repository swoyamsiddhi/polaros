"""Dashboard schemas."""
from pydantic import BaseModel
from typing import Optional


class DashboardSummary(BaseModel):
    active_expeditions: int = 0
    total_assets: int = 0
    critical_assets: int = 0
    active_shipments: int = 0
    delayed_shipments: int = 0
    critical_alerts: int = 0
    total_personnel: int = 0
    personnel_in_field: int = 0
    overall_readiness: float = 0
    stations: list = []
    recent_alerts: list = []
    recent_events: list = []
    expedition_summary: list = []


class PlannerRequest(BaseModel):
    destination_station_id: int
    personnel_count: int
    duration_days: int
    cargo_requirements: list[dict] = []  # [{item_id, quantity}]
    constraints: Optional[dict] = None  # {max_aircraft, max_vehicles, fuel_limit}


class PlanOption(BaseModel):
    plan_id: str  # A, B, C
    name: str
    strategy: str
    estimated_duration_days: int
    risk_score: float
    cost_estimate: float
    fuel_consumption: float
    transport_plan: list[dict] = []
    cargo_allocation: list[dict] = []
    warnings: list[str] = []


class PlannerResponse(BaseModel):
    plans: list[PlanOption]
    destination: str
    constraints_applied: dict = {}


class AssistantQuery(BaseModel):
    query: str


class AssistantResponse(BaseModel):
    answer: str
    data: Optional[dict] = None
    sources: list[str] = []
    suggestions: list[str] = []
