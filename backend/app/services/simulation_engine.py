"""Simulation Engine — state machine for Mission Mode.

Manages mission lifecycle: BRIEFING → RESOURCE_ALLOCATION → ROUTE_SELECTION
→ EXECUTING → RANDOM_EVENT → DECISION → RESULT → DEBRIEF
"""
import json
import random
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.mission import Mission, MissionInstance, MissionEvent


RANDOM_EVENTS = [
    {
        "type": "WHITEOUT",
        "title": "⚠ WHITEOUT CONDITIONS",
        "description": "Sudden whiteout conditions reduce visibility to near zero. All ground transport halted.",
        "options": [
            {"id": "A", "text": "Wait for conditions to clear (lose 6 hours)", "impact": {"time": -6, "fuel": -50, "risk": 5}},
            {"id": "B", "text": "Navigate using GPS instruments (risky)", "impact": {"time": -2, "fuel": -100, "risk": 20, "safety": -15}},
            {"id": "C", "text": "Return to base and reschedule", "impact": {"time": -24, "fuel": -200, "risk": -10, "safety": 10}},
        ],
    },
    {
        "type": "AIRCRAFT_DELAY",
        "title": "✈ AIRCRAFT DELAYED",
        "description": "Aircraft grounded for 6 hours due to crosswinds. Critical cargo waiting for airlift.",
        "options": [
            {"id": "A", "text": "Wait for aircraft (safest)", "impact": {"time": -6, "fuel": -30, "risk": 0}},
            {"id": "B", "text": "Dispatch snow vehicles instead", "impact": {"time": -3, "fuel": -150, "risk": 10, "vehicles": -1}},
            {"id": "C", "text": "Reduce cargo and fly priority supplies only", "impact": {"time": -1, "fuel": -80, "risk": 5, "cargo_delivered": 60}},
            {"id": "D", "text": "Request emergency military airlift", "impact": {"time": -2, "fuel": -50, "risk": -5, "cost": 5000}},
        ],
    },
    {
        "type": "VEHICLE_BREAKDOWN",
        "title": "🚗 VEHICLE BREAKDOWN",
        "description": "Snow vehicle #2 has a mechanical failure. Cargo capacity reduced.",
        "options": [
            {"id": "A", "text": "Attempt field repair (2 hours)", "impact": {"time": -2, "fuel": -20, "risk": 10}},
            {"id": "B", "text": "Transfer cargo to remaining vehicle", "impact": {"time": -1, "fuel": -50, "risk": 15, "vehicles": -1}},
            {"id": "C", "text": "Call for replacement vehicle from station", "impact": {"time": -8, "fuel": -30, "risk": 5}},
        ],
    },
    {
        "type": "FUEL_LEAK",
        "title": "⛽ FUEL LEAK DETECTED",
        "description": "Fuel storage at field camp shows a leak. Approximately 300L lost.",
        "options": [
            {"id": "A", "text": "Seal leak and conserve remaining fuel", "impact": {"fuel": -300, "risk": 15}},
            {"id": "B", "text": "Emergency fuel transfer from main station", "impact": {"time": -4, "fuel": 200, "risk": 5}},
            {"id": "C", "text": "Ration fuel across all operations", "impact": {"fuel": -300, "risk": 20, "efficiency": -10}},
        ],
    },
    {
        "type": "COMMUNICATION_LOSS",
        "title": "📡 COMMUNICATION LOSS",
        "description": "Satellite uplink failed. Field camp cannot communicate with base.",
        "options": [
            {"id": "A", "text": "Dispatch repair team to comm antenna", "impact": {"time": -3, "risk": 10}},
            {"id": "B", "text": "Use backup HF radio (limited capability)", "impact": {"time": 0, "risk": 15}},
            {"id": "C", "text": "Continue mission without comms (dangerous)", "impact": {"time": 0, "risk": 30, "safety": -20}},
        ],
    },
    {
        "type": "WEATHER_IMPROVEMENT",
        "title": "☀ WEATHER WINDOW OPENING",
        "description": "Clear skies detected. A 4-hour weather window has opened for air operations.",
        "options": [
            {"id": "A", "text": "Launch immediate air resupply", "impact": {"time": 2, "fuel": -100, "risk": -15, "cargo_delivered": 40}},
            {"id": "B", "text": "Wait for confirmed extended window", "impact": {"time": -2, "risk": -5}},
        ],
    },
]


def start_mission(db: Session, mission_id: int, user_id: int) -> MissionInstance:
    """Start a new mission instance with initial state."""
    mission = db.query(Mission).filter(Mission.id == mission_id).first()
    if not mission:
        raise ValueError("Mission not found")

    initial_state = json.loads(mission.initial_state) if mission.initial_state else {
        "fuel": 2800,
        "inventory": {"medical": 50, "food": 200, "equipment": 30},
        "aircraft_available": True,
        "vehicles_available": 2,
        "weather_severity": "SEVERE",
        "time_remaining": 48,
        "cargo_delivered": 0,
        "cargo_target": 100,
        "risk": 40,
        "safety": 100,
        "efficiency": 100,
        "cost": 0,
        "decisions_made": 0,
        "events_encountered": 0,
    }

    instance = MissionInstance(
        mission_id=mission_id,
        user_id=user_id,
        status="BRIEFING",
        state=json.dumps(initial_state),
        phase="BRIEFING",
        turn=0,
    )
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def process_action(db: Session, instance_id: int, action: str, choice: str = None) -> dict:
    """Process a player action and return updated state."""
    instance = db.query(MissionInstance).filter(MissionInstance.id == instance_id).first()
    if not instance:
        raise ValueError("Mission instance not found")

    state = json.loads(instance.state)
    result = {"phase": instance.phase, "state": state, "event": None, "mission_complete": False}

    if action == "start":
        instance.phase = "RESOURCE_ALLOCATION"
        instance.status = "ACTIVE"
        state["phase"] = "RESOURCE_ALLOCATION"

    elif action == "allocate_resources":
        instance.phase = "ROUTE_SELECTION"
        state["phase"] = "ROUTE_SELECTION"

    elif action == "select_route":
        instance.phase = "EXECUTING"
        state["phase"] = "EXECUTING"
        instance.turn += 1

        # Maybe trigger a random event
        if random.random() < 0.7:  # 70% chance
            event_template = random.choice(RANDOM_EVENTS)
            mission_event = MissionEvent(
                instance_id=instance.id,
                turn=instance.turn,
                event_type=event_template["type"],
                title=event_template["title"],
                description=event_template["description"],
                options=json.dumps(event_template["options"]),
            )
            db.add(mission_event)
            instance.phase = "DECISION"
            state["phase"] = "DECISION"
            state["events_encountered"] += 1
            result["event"] = {
                "type": event_template["type"],
                "title": event_template["title"],
                "description": event_template["description"],
                "options": event_template["options"],
            }

    elif action == "make_decision" and choice:
        # Find the current event
        current_event = (
            db.query(MissionEvent)
            .filter(MissionEvent.instance_id == instance.id, MissionEvent.player_choice == None)
            .order_by(MissionEvent.timestamp.desc())
            .first()
        )

        if current_event and current_event.options:
            options = json.loads(current_event.options)
            selected = next((o for o in options if o["id"] == choice), None)
            if selected:
                impact = selected.get("impact", {})

                # Apply impact to state
                state["fuel"] = max(0, state["fuel"] + impact.get("fuel", 0))
                state["time_remaining"] = max(0, state["time_remaining"] + impact.get("time", 0))
                state["risk"] = max(0, min(100, state["risk"] + impact.get("risk", 0)))
                state["safety"] = max(0, min(100, state["safety"] + impact.get("safety", 0)))
                state["efficiency"] = max(0, min(100, state["efficiency"] + impact.get("efficiency", 0)))
                state["cost"] += impact.get("cost", 0)
                state["cargo_delivered"] += impact.get("cargo_delivered", 0)

                if impact.get("vehicles", 0) < 0:
                    state["vehicles_available"] = max(0, state["vehicles_available"] + impact["vehicles"])

                state["decisions_made"] += 1
                current_event.player_choice = choice
                current_event.outcome = json.dumps(impact)

        instance.phase = "EXECUTING"
        state["phase"] = "EXECUTING"
        instance.turn += 1

        # Progress delivery
        state["cargo_delivered"] = min(state["cargo_target"], state["cargo_delivered"] + 20)

        # Check if another event should fire
        if instance.turn < 5 and random.random() < 0.5:
            event_template = random.choice(RANDOM_EVENTS)
            mission_event = MissionEvent(
                instance_id=instance.id,
                turn=instance.turn,
                event_type=event_template["type"],
                title=event_template["title"],
                description=event_template["description"],
                options=json.dumps(event_template["options"]),
            )
            db.add(mission_event)
            instance.phase = "DECISION"
            state["phase"] = "DECISION"
            state["events_encountered"] += 1
            result["event"] = {
                "type": event_template["type"],
                "title": event_template["title"],
                "description": event_template["description"],
                "options": event_template["options"],
            }

    elif action == "continue":
        instance.turn += 1
        state["cargo_delivered"] = min(state["cargo_target"], state["cargo_delivered"] + 25)
        state["fuel"] = max(0, state["fuel"] - 100)
        state["time_remaining"] = max(0, state["time_remaining"] - 4)

        # Check win/lose conditions
        if state["cargo_delivered"] >= state["cargo_target"]:
            instance.phase = "RESULT"
            instance.status = "COMPLETED"
            state["phase"] = "RESULT"
            result["mission_complete"] = True
        elif state["fuel"] <= 0 or state["time_remaining"] <= 0:
            instance.phase = "RESULT"
            instance.status = "FAILED"
            state["phase"] = "RESULT"
            result["mission_complete"] = True
        elif random.random() < 0.4:
            event_template = random.choice(RANDOM_EVENTS)
            mission_event = MissionEvent(
                instance_id=instance.id,
                turn=instance.turn,
                event_type=event_template["type"],
                title=event_template["title"],
                description=event_template["description"],
                options=json.dumps(event_template["options"]),
            )
            db.add(mission_event)
            instance.phase = "DECISION"
            state["phase"] = "DECISION"
            state["events_encountered"] += 1
            result["event"] = {
                "type": event_template["type"],
                "title": event_template["title"],
                "description": event_template["description"],
                "options": event_template["options"],
            }

    instance.state = json.dumps(state)
    result["state"] = state
    result["phase"] = instance.phase

    if result["mission_complete"]:
        instance.completed_at = datetime.now(timezone.utc)

    db.commit()
    return result
