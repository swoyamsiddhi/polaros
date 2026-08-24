"""Scoring Engine — calculates mission scores and evaluates badges."""
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.mission import MissionInstance, MissionEvent
from app.models.gamification import Score, Badge, UserBadge


SCORING_RULES = {
    "cargo_delivered": {"max": 500, "description": "Successful delivery"},
    "fuel_efficiency": {"max": 200, "description": "Fuel efficiency"},
    "on_time": {"max": 300, "description": "On-time arrival"},
    "safety": {"max": 250, "description": "Safety maintained"},
    "decisions_quality": {"max": 150, "description": "Decision quality"},
}

PENALTY_RULES = {
    "late_delivery": -200,
    "fuel_waste": -100,
    "asset_damage": -300,
    "critical_stockout": -500,
    "unsafe_decision": -500,
}


def calculate_score(db: Session, instance_id: int) -> dict:
    """Calculate mission score from instance state and decisions."""
    instance = db.query(MissionInstance).filter(MissionInstance.id == instance_id).first()
    if not instance:
        return {}

    state = json.loads(instance.state) if instance.state else {}
    events = db.query(MissionEvent).filter(MissionEvent.instance_id == instance_id).all()

    breakdown = []
    total = 0

    # Cargo delivery score
    cargo_pct = (state.get("cargo_delivered", 0) / max(state.get("cargo_target", 100), 1)) * 100
    if cargo_pct >= 100:
        points = 500
        breakdown.append({"action": "Successful delivery", "points": 500, "reason": "All cargo delivered"})
    elif cargo_pct >= 75:
        points = 300
        breakdown.append({"action": "Partial delivery", "points": 300, "reason": f"{cargo_pct:.0f}% cargo delivered"})
    else:
        points = -200
        breakdown.append({"action": "Late/incomplete delivery", "points": -200, "reason": f"Only {cargo_pct:.0f}% cargo delivered"})
    total += points

    # On-time bonus
    time_left = state.get("time_remaining", 0)
    if time_left > 12 and cargo_pct >= 100:
        total += 300
        breakdown.append({"action": "On-time arrival", "points": 300, "reason": f"{time_left}h remaining"})
    elif time_left > 0:
        total += 100
        breakdown.append({"action": "Completed within time", "points": 100, "reason": f"{time_left}h remaining"})

    # Fuel efficiency
    fuel_remaining = state.get("fuel", 0)
    if fuel_remaining > 1500:
        total += 200
        breakdown.append({"action": "Fuel efficiency", "points": 200, "reason": f"{fuel_remaining}L remaining"})
    elif fuel_remaining > 500:
        total += 100
        breakdown.append({"action": "Adequate fuel management", "points": 100, "reason": f"{fuel_remaining}L remaining"})
    else:
        total -= 100
        breakdown.append({"action": "Fuel waste/shortage", "points": -100, "reason": f"Only {fuel_remaining}L remaining"})

    # Safety score
    safety = state.get("safety", 100)
    if safety >= 80:
        total += 250
        breakdown.append({"action": "Safety maintained", "points": 250, "reason": f"Safety at {safety}%"})
    elif safety >= 50:
        total += 100
        breakdown.append({"action": "Acceptable safety", "points": 100, "reason": f"Safety at {safety}%"})
    else:
        total -= 500
        breakdown.append({"action": "Unsafe operations", "points": -500, "reason": f"Safety dropped to {safety}%"})

    # Emergency response bonus
    events_handled = state.get("events_encountered", 0)
    if events_handled >= 3:
        total += 250
        breakdown.append({"action": "Emergency response", "points": 250, "reason": f"Handled {events_handled} events"})
    elif events_handled >= 1:
        total += 150
        breakdown.append({"action": "Event handling", "points": 150, "reason": f"Handled {events_handled} event(s)"})

    total = max(0, total)

    # Calculate category scores
    safety_score = min(100, safety)
    efficiency_score = min(100, (fuel_remaining / 2800) * 100) if state.get("fuel") is not None else 50
    accuracy_score = min(100, cargo_pct)
    resource_score = min(100, (
        (state.get("vehicles_available", 2) / 2) * 50 +
        (1 if state.get("aircraft_available", True) else 0) * 50
    ))

    # Save score
    score = Score(
        instance_id=instance_id,
        user_id=instance.user_id,
        total=total,
        safety=round(safety_score, 1),
        efficiency=round(efficiency_score, 1),
        accuracy=round(accuracy_score, 1),
        resource_usage=round(resource_score, 1),
        breakdown=json.dumps(breakdown),
    )
    db.add(score)

    # Evaluate badges
    badges_earned = evaluate_badges(db, instance, state, total)

    db.commit()

    # Generate debrief
    successes = []
    improvements = []
    for item in breakdown:
        if item["points"] > 0:
            successes.append(item["reason"])
        elif item["points"] < 0:
            improvements.append(item["reason"])

    return {
        "score": {
            "total": total,
            "safety": round(safety_score, 1),
            "efficiency": round(efficiency_score, 1),
            "accuracy": round(accuracy_score, 1),
            "resource_usage": round(resource_score, 1),
            "breakdown": breakdown,
        },
        "badges_earned": badges_earned,
        "successes": successes if successes else ["Completed the mission"],
        "improvements": improvements if improvements else ["No significant issues"],
        "recommended_lesson": "Multi-Leg Polar Logistics" if total < 800 else "Advanced Weather Operations",
    }


def evaluate_badges(db: Session, instance: MissionInstance, state: dict, total: int) -> list:
    """Check and award earned badges."""
    badges_earned = []
    badges = db.query(Badge).all()

    badge_checks = {
        "ZERO_STOCKOUT": state.get("cargo_delivered", 0) >= state.get("cargo_target", 100),
        "ASSET_GUARDIAN": state.get("vehicles_available", 0) >= 2 and state.get("aircraft_available", True),
        "WEATHER_COMMANDER": state.get("events_encountered", 0) >= 2 and state.get("safety", 0) >= 70,
        "LOGISTICS_MASTER": total >= 1200,
        "FUEL_SAVER": state.get("fuel", 0) >= 1500,
        "EMERGENCY_COMMANDER": state.get("events_encountered", 0) >= 3 and total >= 800,
    }

    for badge in badges:
        if badge.code in badge_checks and badge_checks[badge.code]:
            # Check not already earned for this instance
            existing = db.query(UserBadge).filter(
                UserBadge.user_id == instance.user_id,
                UserBadge.badge_id == badge.id,
                UserBadge.instance_id == instance.id,
            ).first()
            if not existing:
                ub = UserBadge(
                    user_id=instance.user_id,
                    badge_id=badge.id,
                    instance_id=instance.id,
                )
                db.add(ub)
                badges_earned.append({
                    "code": badge.code,
                    "name": badge.name,
                    "description": badge.description,
                    "icon": badge.icon,
                })

    return badges_earned
