"""Intelligent Planner — generates 3 ranked expedition plans.

Plan A: Lowest Risk
Plan B: Lowest Cost
Plan C: Fastest Delivery
"""
from sqlalchemy.orm import Session
from app.models.station import Station
from app.models.asset import Asset
from app.models.inventory import Inventory
from app.models.item import Item
from app.models.weather import WeatherObservation


def generate_plans(db: Session, request: dict) -> dict:
    """Generate 3 ranked plans for an expedition."""
    dest_id = request.get("destination_station_id")
    personnel_count = request.get("personnel_count", 10)
    duration = request.get("duration_days", 30)
    constraints = request.get("constraints", {})

    station = db.query(Station).filter(Station.id == dest_id).first()
    if not station:
        return {"plans": [], "destination": "Unknown"}

    # Get current weather
    weather = (
        db.query(WeatherObservation)
        .filter(WeatherObservation.station_id == dest_id)
        .order_by(WeatherObservation.timestamp.desc())
        .first()
    )
    weather_severity = weather.severity if weather else "WATCH"

    # Get transport assets
    aircraft = db.query(Asset).filter(
        Asset.category.in_(["AIRCRAFT", "HELICOPTER"]),
        Asset.status.in_(["AVAILABLE", "ASSIGNED", "READY"]),
    ).count()
    vehicles = db.query(Asset).filter(
        Asset.category == "SNOW_VEHICLE",
        Asset.status.in_(["AVAILABLE", "ASSIGNED", "READY"]),
    ).count()

    base_fuel = personnel_count * duration * 25  # 25L per person per day

    plans = []

    # --- PLAN A: Lowest Risk ---
    plans.append({
        "plan_id": "A",
        "name": "Lowest Risk",
        "strategy": "Conservative routing with maximum reserves. Uses proven sea + ground routes. Extra fuel and medical reserves. Redundant transport.",
        "estimated_duration_days": duration + 10,
        "risk_score": 22,
        "cost_estimate": 85000,
        "fuel_consumption": base_fuel * 1.4,
        "transport_plan": [
            {"leg": 1, "mode": "SEA", "from": "Goa", "to": "Cape Town", "days": 12},
            {"leg": 2, "mode": "SEA", "from": "Cape Town", "to": station.name, "days": 8},
            {"leg": 3, "mode": "SNOW_VEHICLE", "from": station.name, "to": "Field Camp", "days": 2},
        ],
        "cargo_allocation": [
            {"priority": "CRITICAL", "method": "Primary vessel + backup reserves"},
            {"priority": "HIGH", "method": "Primary vessel"},
            {"priority": "MEDIUM", "method": "Secondary shipment"},
        ],
        "warnings": [
            "Longer transit time (+10 days)",
            "Higher fuel consumption due to reserve margins",
        ] if weather_severity in ("SEVERE", "EXTREME") else [
            "Slightly longer transit time than Plan C",
        ],
    })

    # --- PLAN B: Lowest Cost ---
    plans.append({
        "plan_id": "B",
        "name": "Lowest Cost",
        "strategy": "Consolidated bulk shipping via sea route. Minimal air transport. Standard reserves only.",
        "estimated_duration_days": duration + 15,
        "risk_score": 45,
        "cost_estimate": 52000,
        "fuel_consumption": base_fuel * 1.1,
        "transport_plan": [
            {"leg": 1, "mode": "SEA", "from": "Goa", "to": station.name, "days": 18},
            {"leg": 2, "mode": "SNOW_VEHICLE", "from": station.name, "to": "Field Camp", "days": 3},
        ],
        "cargo_allocation": [
            {"priority": "ALL", "method": "Single consolidated sea shipment"},
        ],
        "warnings": [
            "Longest transit time",
            "No air transport backup",
            "Weather-dependent — high risk if storms occur during transit",
        ],
    })

    # --- PLAN C: Fastest ---
    plans.append({
        "plan_id": "C",
        "name": "Fastest Delivery",
        "strategy": "Air-priority dispatch for critical cargo. Parallel sea+air routing. Pre-positioned snow vehicles.",
        "estimated_duration_days": duration + 3,
        "risk_score": 38,
        "cost_estimate": 120000,
        "fuel_consumption": base_fuel * 1.6,
        "transport_plan": [
            {"leg": 1, "mode": "AIR", "from": "Goa", "to": "Gateway", "days": 2},
            {"leg": 2, "mode": "AIR", "from": "Gateway", "to": station.name, "days": 1},
            {"leg": 3, "mode": "SEA", "from": "Goa", "to": station.name, "days": 18, "note": "Non-critical cargo follows by sea"},
        ],
        "cargo_allocation": [
            {"priority": "CRITICAL", "method": "Air freight — immediate dispatch"},
            {"priority": "HIGH", "method": "Air freight — next window"},
            {"priority": "MEDIUM", "method": "Sea freight — bulk shipment"},
        ],
        "warnings": [
            "Highest cost option",
            f"Aircraft availability: {aircraft} available",
            "Weather may affect air operations" if weather_severity in ("WARNING", "SEVERE", "EXTREME") else "Good air conditions expected",
        ],
    })

    # Adjust risk scores based on weather
    if weather_severity in ("SEVERE", "EXTREME"):
        plans[1]["risk_score"] += 25  # Sea-only plan very risky
        plans[2]["risk_score"] += 15  # Air plan affected too
        plans[2]["warnings"].append("⚠ Severe weather may ground aircraft")

    return {
        "plans": plans,
        "destination": station.name,
        "constraints_applied": {
            "personnel": personnel_count,
            "duration": duration,
            "aircraft_available": aircraft,
            "vehicles_available": vehicles,
            "weather": weather_severity,
        },
    }
