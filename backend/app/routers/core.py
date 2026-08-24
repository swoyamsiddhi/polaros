"""Core API routers — stations, expeditions, inventory, assets, shipments, personnel, alerts, weather, dashboard."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.database import get_db
from app.auth.dependencies import get_current_user, get_optional_user
from app.models import *
from app.services.readiness_engine import calculate_readiness
from app.services.risk_engine import calculate_risk
from app.services.forecasting import forecast_inventory
from app.services.maintenance import predict_maintenance_risk
from app.services.planner import generate_plans
from app.services.assistant import process_query
from app.services.event_engine import create_event, get_recent_events
from app.services.simulation_engine import start_mission, process_action
from app.services.scoring_engine import calculate_score
import json


# === DASHBOARD ===
dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@dashboard_router.get("/summary")
def get_dashboard(db: Session = Depends(get_db)):
    active_exps = db.query(Expedition).filter(Expedition.status.in_(["PLANNED", "APPROVED", "PREPARING", "ACTIVE", "IN_PROGRESS"])).all()
    total_assets = db.query(Asset).count()
    critical_assets = db.query(Asset).filter(Asset.status.in_(["MAINTENANCE_REQUIRED", "MAINTENANCE"])).count()
    active_shipments = db.query(Shipment).filter(Shipment.status.in_(["IN_TRANSIT", "LOADED", "BOOKED"])).count()
    delayed_shipments = db.query(Shipment).filter(Shipment.status == "DELAYED").count()
    total_personnel = db.query(Personnel).count()
    field_personnel = db.query(Personnel).filter(Personnel.travel_status.in_(["IN_TRANSIT", "AT_FIELD_CAMP"])).count()

    # Critical alerts
    critical_events = db.query(Event).filter(Event.severity.in_(["HIGH", "CRITICAL"])).order_by(Event.timestamp.desc()).limit(10).all()

    # Calculate average readiness
    avg_readiness = 0
    if active_exps:
        avg_readiness = sum(e.readiness_score for e in active_exps) / len(active_exps)

    stations = db.query(Station).all()
    station_data = []
    for s in stations:
        weather = db.query(WeatherObservation).filter(WeatherObservation.station_id == s.id).order_by(WeatherObservation.timestamp.desc()).first()
        station_data.append({
            "id": s.id, "name": s.name, "code": s.code, "type": s.type,
            "latitude": s.latitude, "longitude": s.longitude,
            "status": s.status, "comm_status": s.comm_status,
            "occupancy": s.current_occupancy, "capacity": s.capacity,
            "weather_severity": weather.severity if weather else "NORMAL",
            "temperature": weather.temperature if weather else None,
        })

    return {
        "active_expeditions": len(active_exps),
        "total_assets": total_assets,
        "critical_assets": critical_assets,
        "active_shipments": active_shipments,
        "delayed_shipments": delayed_shipments,
        "critical_alerts": len(critical_events),
        "total_personnel": total_personnel,
        "personnel_in_field": field_personnel,
        "overall_readiness": round(avg_readiness, 1),
        "stations": station_data,
        "recent_alerts": [{
            "id": e.id, "event_type": e.event_type, "severity": e.severity,
            "title": e.title, "description": e.description,
            "timestamp": e.timestamp.isoformat() if e.timestamp else None,
        } for e in critical_events],
        "expedition_summary": [{
            "id": e.id, "code": e.code, "name": e.name, "status": e.status,
            "readiness": e.readiness_score, "risk": e.risk_score,
            "destination": e.destination.name if e.destination else "",
            "priority": e.priority,
        } for e in active_exps],
    }


# === STATIONS ===
stations_router = APIRouter(prefix="/stations", tags=["Stations"])

@stations_router.get("")
def list_stations(db: Session = Depends(get_db)):
    stations = db.query(Station).all()
    result = []
    for s in stations:
        personnel_count = db.query(Personnel).filter(Personnel.station_id == s.id).count()
        asset_count = db.query(Asset).filter(Asset.station_id == s.id).count()
        weather = db.query(WeatherObservation).filter(WeatherObservation.station_id == s.id).order_by(WeatherObservation.timestamp.desc()).first()
        result.append({
            "id": s.id, "name": s.name, "code": s.code, "type": s.type,
            "latitude": s.latitude, "longitude": s.longitude, "altitude": s.altitude,
            "capacity": s.capacity, "current_occupancy": s.current_occupancy,
            "status": s.status, "comm_status": s.comm_status,
            "description": s.description, "established_year": s.established_year,
            "region": s.region, "personnel_count": personnel_count,
            "asset_count": asset_count,
            "weather_severity": weather.severity if weather else "NORMAL",
            "temperature": weather.temperature if weather else None,
        })
    return result

@stations_router.get("/{station_id}")
def get_station(station_id: int, db: Session = Depends(get_db)):
    s = db.query(Station).filter(Station.id == station_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Station not found")

    personnel = db.query(Personnel).filter(Personnel.station_id == s.id).all()
    assets = db.query(Asset).filter(Asset.station_id == s.id).all()
    inventory = db.query(Inventory).join(Item).filter(Inventory.station_id == s.id).all()
    weather = db.query(WeatherObservation).filter(WeatherObservation.station_id == s.id).order_by(WeatherObservation.timestamp.desc()).first()
    expeditions = db.query(Expedition).filter(Expedition.destination_station_id == s.id, Expedition.status.in_(["PLANNED", "APPROVED", "PREPARING", "ACTIVE"])).all()

    return {
        "id": s.id, "name": s.name, "code": s.code, "type": s.type,
        "latitude": s.latitude, "longitude": s.longitude, "altitude": s.altitude,
        "capacity": s.capacity, "current_occupancy": s.current_occupancy,
        "status": s.status, "comm_status": s.comm_status,
        "description": s.description, "established_year": s.established_year,
        "region": s.region,
        "personnel": [{"id": p.id, "name": p.name, "role": p.role, "travel_status": p.travel_status, "specialisation": p.specialisation} for p in personnel],
        "assets": [{"id": a.id, "code": a.code, "name": a.name, "category": a.category, "status": a.status, "utilisation_pct": a.utilisation_pct} for a in assets],
        "inventory": [{"id": inv.id, "item_name": inv.item.name, "category": inv.item.category, "quantity": inv.quantity, "unit": inv.item.unit, "criticality": inv.item.criticality, "min_stock": inv.item.min_stock} for inv in inventory],
        "weather": {"temperature": weather.temperature, "wind_speed": weather.wind_speed, "visibility": weather.visibility, "severity": weather.severity, "precipitation": weather.precipitation, "forecast": weather.forecast_summary} if weather else None,
        "active_expeditions": [{"id": e.id, "code": e.code, "name": e.name, "status": e.status} for e in expeditions],
    }


# === EXPEDITIONS ===
expeditions_router = APIRouter(prefix="/expeditions", tags=["Expeditions"])

@expeditions_router.get("")
def list_expeditions(db: Session = Depends(get_db)):
    exps = db.query(Expedition).all()
    result = []
    for e in exps:
        personnel_count = db.query(ExpeditionPersonnel).filter(ExpeditionPersonnel.expedition_id == e.id).count()
        cargo_count = db.query(ExpeditionCargo).filter(ExpeditionCargo.expedition_id == e.id).count()
        shipment_count = db.query(Shipment).filter(Shipment.expedition_id == e.id).count()
        result.append({
            "id": e.id, "code": e.code, "name": e.name, "description": e.description,
            "origin": e.origin, "destination_station_id": e.destination_station_id,
            "destination_name": e.destination.name if e.destination else "",
            "start_date": e.start_date.isoformat(), "end_date": e.end_date.isoformat(),
            "priority": e.priority, "status": e.status,
            "readiness_score": e.readiness_score, "risk_score": e.risk_score,
            "risk_level": "CRITICAL" if e.risk_score >= 75 else "HIGH" if e.risk_score >= 50 else "MEDIUM" if e.risk_score >= 25 else "LOW",
            "personnel_count": personnel_count, "cargo_items": cargo_count,
            "shipment_count": shipment_count,
        })
    return result

@expeditions_router.get("/{expedition_id}")
def get_expedition(expedition_id: int, db: Session = Depends(get_db)):
    e = db.query(Expedition).filter(Expedition.id == expedition_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Expedition not found")

    # Calculate readiness
    readiness = calculate_readiness(db, expedition_id)
    # Calculate risk
    risk = calculate_risk(db, expedition_id)

    # Get cargo
    cargo = db.query(ExpeditionCargo).filter(ExpeditionCargo.expedition_id == expedition_id).all()
    cargo_list = [{
        "id": c.id, "item_id": c.item_id, "item_name": c.item.name if c.item else "",
        "category": c.item.category if c.item else "", "unit": c.item.unit if c.item else "",
        "required_quantity": c.required_quantity, "fulfilled_quantity": c.fulfilled_quantity,
        "fulfillment_pct": round((c.fulfilled_quantity / max(c.required_quantity, 1)) * 100, 1),
    } for c in cargo]

    # Get personnel
    personnel = db.query(ExpeditionPersonnel).filter(ExpeditionPersonnel.expedition_id == expedition_id).all()
    personnel_list = [{
        "id": ep.id, "name": ep.personnel.name if ep.personnel else "",
        "role": ep.role_in_expedition or (ep.personnel.role if ep.personnel else ""),
        "travel_status": ep.personnel.travel_status if ep.personnel else "",
    } for ep in personnel]

    # Get shipments
    shipments = db.query(Shipment).filter(Shipment.expedition_id == expedition_id).all()
    shipment_list = [{
        "id": s.id, "code": s.code, "origin": s.origin, "destination": s.destination,
        "status": s.status, "priority": s.priority,
    } for s in shipments]

    # Get recommendations
    recs = db.query(Recommendation).filter(Recommendation.expedition_id == expedition_id).order_by(Recommendation.timestamp.desc()).limit(5).all()

    # Get timeline events
    events = db.query(Event).filter(Event.entity_type == "expedition", Event.entity_id == expedition_id).order_by(Event.timestamp.desc()).limit(20).all()

    return {
        "id": e.id, "code": e.code, "name": e.name, "description": e.description,
        "origin": e.origin, "destination_station_id": e.destination_station_id,
        "destination_name": e.destination.name if e.destination else "",
        "start_date": e.start_date.isoformat(), "end_date": e.end_date.isoformat(),
        "priority": e.priority, "status": e.status,
        "readiness_score": readiness["overall"], "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"], "mission_objectives": e.mission_objectives,
        "readiness_breakdown": readiness["breakdown"],
        "risk_breakdown": risk["factors"],
        "personnel": personnel_list, "cargo": cargo_list,
        "shipments": shipment_list,
        "recommendations": [{"id": r.id, "title": r.title, "description": r.description, "action": r.action, "priority": r.priority, "status": r.status} for r in recs],
        "timeline": [{"id": ev.id, "type": ev.event_type, "title": ev.title, "description": ev.description, "severity": ev.severity, "timestamp": ev.timestamp.isoformat()} for ev in events],
    }


# === INVENTORY ===
inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])

@inventory_router.get("")
def list_inventory(station_id: int = None, category: str = None, db: Session = Depends(get_db)):
    q = db.query(Inventory).join(Item).join(Station, Inventory.station_id == Station.id)
    if station_id:
        q = q.filter(Inventory.station_id == station_id)
    if category:
        q = q.filter(Item.category == category)
    records = q.all()

    return [{
        "id": inv.id, "station_id": inv.station_id,
        "station_name": inv.station.name if inv.station else "",
        "item_id": inv.item_id, "item_name": inv.item.name if inv.item else "",
        "item_category": inv.item.category if inv.item else "",
        "item_unit": inv.item.unit if inv.item else "",
        "criticality": inv.item.criticality if inv.item else "MEDIUM",
        "quantity": inv.quantity, "reserved_quantity": inv.reserved_quantity,
        "available_quantity": inv.quantity - inv.reserved_quantity,
        "avg_daily_consumption": inv.avg_daily_consumption,
        "min_stock": inv.item.min_stock if inv.item else 0,
        "max_stock": inv.item.max_stock if inv.item else 0,
        "expiry_date": inv.expiry_date.isoformat() if inv.expiry_date else None,
        "stock_status": "CRITICAL" if inv.quantity <= (inv.item.min_stock if inv.item else 0) else "LOW" if inv.quantity <= (inv.item.min_stock * 1.5 if inv.item else 0) else "NORMAL",
    } for inv in records]

@inventory_router.get("/alerts")
def get_inventory_alerts(db: Session = Depends(get_db)):
    alerts = []
    records = db.query(Inventory).join(Item).join(Station, Inventory.station_id == Station.id).all()
    for inv in records:
        if inv.quantity <= inv.item.min_stock:
            alerts.append({
                "id": inv.id, "alert_type": "CRITICAL_STOCK",
                "severity": "CRITICAL", "title": f"Critical stock: {inv.item.name}",
                "description": f"{inv.item.name} at {inv.station.name} is below minimum stock ({inv.quantity:.0f} {inv.item.unit} vs min {inv.item.min_stock})",
                "station_name": inv.station.name, "item_name": inv.item.name,
                "current_quantity": inv.quantity, "threshold": inv.item.min_stock,
                "recommendation": f"Immediate resupply required for {inv.item.name} at {inv.station.name}",
            })
        elif inv.quantity <= inv.item.min_stock * 1.5:
            alerts.append({
                "id": inv.id, "alert_type": "LOW_STOCK",
                "severity": "HIGH", "title": f"Low stock: {inv.item.name}",
                "description": f"{inv.item.name} at {inv.station.name} approaching minimum ({inv.quantity:.0f} {inv.item.unit})",
                "station_name": inv.station.name, "item_name": inv.item.name,
                "current_quantity": inv.quantity, "threshold": inv.item.min_stock,
                "recommendation": f"Schedule resupply for {inv.item.name} at {inv.station.name}",
            })
    return sorted(alerts, key=lambda x: x["severity"] == "CRITICAL", reverse=True)

@inventory_router.get("/forecast/{station_id}/{item_id}")
def get_forecast(station_id: int, item_id: int, db: Session = Depends(get_db)):
    result = forecast_inventory(db, station_id, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return result


# === ASSETS ===
assets_router = APIRouter(prefix="/assets", tags=["Assets"])

@assets_router.get("")
def list_assets(station_id: int = None, category: str = None, db: Session = Depends(get_db)):
    q = db.query(Asset)
    if station_id:
        q = q.filter(Asset.station_id == station_id)
    if category:
        q = q.filter(Asset.category == category)
    assets = q.all()
    return [{
        "id": a.id, "code": a.code, "name": a.name, "category": a.category,
        "serial_number": a.serial_number, "station_id": a.station_id,
        "station_name": a.station.name if a.station else "",
        "custodian": a.custodian, "status": a.status,
        "utilisation_pct": a.utilisation_pct, "engine_hours": a.engine_hours,
        "last_maintenance": a.last_maintenance.isoformat() if a.last_maintenance else None,
        "next_maintenance": a.next_maintenance.isoformat() if a.next_maintenance else None,
        "replacement_cost": a.replacement_cost,
    } for a in assets]

@assets_router.get("/{asset_id}")
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    a = db.query(Asset).filter(Asset.id == asset_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Asset not found")

    maint_tasks = db.query(MaintenanceTask).filter(MaintenanceTask.asset_id == asset_id).order_by(MaintenanceTask.scheduled_date.desc()).all()
    prediction = predict_maintenance_risk(db, asset_id)

    return {
        "id": a.id, "code": a.code, "name": a.name, "category": a.category,
        "serial_number": a.serial_number, "station_id": a.station_id,
        "station_name": a.station.name if a.station else "",
        "custodian": a.custodian, "status": a.status,
        "utilisation_pct": a.utilisation_pct, "engine_hours": a.engine_hours,
        "maintenance_threshold_hours": a.maintenance_threshold_hours,
        "last_maintenance": a.last_maintenance.isoformat() if a.last_maintenance else None,
        "next_maintenance": a.next_maintenance.isoformat() if a.next_maintenance else None,
        "replacement_cost": a.replacement_cost, "description": a.description,
        "maintenance_tasks": [{"id": t.id, "type": t.type, "status": t.status, "description": t.description, "scheduled_date": t.scheduled_date.isoformat(), "completed_date": t.completed_date.isoformat() if t.completed_date else None} for t in maint_tasks],
        "maintenance_prediction": prediction,
    }


# === SHIPMENTS ===
shipments_router = APIRouter(prefix="/shipments", tags=["Shipments"])

@shipments_router.get("")
def list_shipments(db: Session = Depends(get_db)):
    shipments = db.query(Shipment).all()
    return [{
        "id": s.id, "code": s.code, "expedition_id": s.expedition_id,
        "expedition_code": s.expedition.code if s.expedition else "",
        "origin": s.origin, "destination": s.destination,
        "status": s.status, "priority": s.priority,
        "total_weight": s.total_weight,
        "legs_count": len(s.legs),
        "completed_legs": sum(1 for l in s.legs if l.status == "ARRIVED"),
        "cargo_description": s.cargo_description,
    } for s in shipments]

@shipments_router.get("/{shipment_id}")
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    s = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Shipment not found")

    legs = [{
        "id": l.id, "sequence": l.sequence, "origin": l.origin, "destination": l.destination,
        "mode": l.mode, "vehicle": l.vehicle,
        "planned_departure": l.planned_departure.isoformat() if l.planned_departure else None,
        "planned_arrival": l.planned_arrival.isoformat() if l.planned_arrival else None,
        "actual_departure": l.actual_departure.isoformat() if l.actual_departure else None,
        "actual_arrival": l.actual_arrival.isoformat() if l.actual_arrival else None,
        "status": l.status, "cargo_description": l.cargo_description,
        "distance_km": l.distance_km,
    } for l in s.legs]

    events = db.query(Event).filter(Event.entity_type == "shipment", Event.entity_id == shipment_id).order_by(Event.timestamp).all()

    return {
        "id": s.id, "code": s.code, "expedition_id": s.expedition_id,
        "expedition_code": s.expedition.code if s.expedition else "",
        "origin": s.origin, "destination": s.destination,
        "status": s.status, "priority": s.priority,
        "total_weight": s.total_weight, "cargo_description": s.cargo_description,
        "legs": legs,
        "timeline": [{"id": e.id, "type": e.event_type, "title": e.title, "description": e.description, "severity": e.severity, "timestamp": e.timestamp.isoformat()} for e in events],
    }


# === PERSONNEL ===
personnel_router = APIRouter(prefix="/personnel", tags=["Personnel"])

@personnel_router.get("")
def list_personnel(db: Session = Depends(get_db)):
    people = db.query(Personnel).all()
    return [{
        "id": p.id, "name": p.name, "role": p.role, "organisation": p.organisation,
        "specialisation": p.specialisation,
        "station_id": p.station_id,
        "station_name": p.station.name if p.station else "",
        "travel_status": p.travel_status,
        "destination_name": p.destination.name if p.destination else "",
        "expected_arrival": p.expected_arrival.isoformat() if p.expected_arrival else None,
    } for p in people]


# === ALERTS ===
alerts_router = APIRouter(prefix="/alerts", tags=["Alerts"])

@alerts_router.get("")
def list_alerts(db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.severity.in_(["WARNING", "HIGH", "CRITICAL"])).order_by(Event.timestamp.desc()).limit(50).all()
    recs = db.query(Recommendation).order_by(Recommendation.timestamp.desc()).limit(20).all()
    rec_map = {r.event_id: r for r in recs if r.event_id}

    return [{
        "id": e.id, "event_type": e.event_type, "severity": e.severity,
        "title": e.title or e.event_type.replace("_", " ").title(),
        "description": e.description or "",
        "entity_type": e.entity_type, "entity_id": e.entity_id,
        "recommendation": rec_map[e.id].action if e.id in rec_map else "",
        "timestamp": e.timestamp.isoformat(),
    } for e in events]


# === WEATHER ===
weather_router = APIRouter(prefix="/weather", tags=["Weather"])

@weather_router.get("")
def list_weather(db: Session = Depends(get_db)):
    stations = db.query(Station).all()
    result = []
    for s in stations:
        w = db.query(WeatherObservation).filter(WeatherObservation.station_id == s.id).order_by(WeatherObservation.timestamp.desc()).first()
        if w:
            result.append({
                "id": w.id, "station_id": s.id, "station_name": s.name,
                "temperature": w.temperature, "wind_speed": w.wind_speed,
                "visibility": w.visibility, "precipitation": w.precipitation,
                "humidity": w.humidity, "pressure": w.pressure,
                "severity": w.severity, "forecast_summary": w.forecast_summary,
                "timestamp": w.timestamp.isoformat(),
            })
    return result


# === RISK ===
risk_router = APIRouter(prefix="/risk", tags=["Risk"])

@risk_router.get("/expeditions/{expedition_id}")
def get_expedition_risk(expedition_id: int, db: Session = Depends(get_db)):
    return calculate_risk(db, expedition_id)


# === PLANNER ===
planner_router = APIRouter(prefix="/planner", tags=["Planner"])

@planner_router.post("/generate")
def generate_expedition_plans(request: dict, db: Session = Depends(get_db)):
    return generate_plans(db, request)


# === ASSISTANT ===
assistant_router = APIRouter(prefix="/assistant", tags=["Assistant"])

@assistant_router.post("/query")
def query_assistant(request: dict, db: Session = Depends(get_db)):
    query = request.get("query", "")
    return process_query(db, query)


# === EVENTS STREAM ===
events_router = APIRouter(prefix="/events", tags=["Events"])

@events_router.get("/stream")
def get_event_stream(limit: int = 50, db: Session = Depends(get_db)):
    events = get_recent_events(db, limit)
    return [{
        "id": e.id, "event_type": e.event_type, "severity": e.severity,
        "title": e.title, "description": e.description,
        "entity_type": e.entity_type, "entity_id": e.entity_id,
        "timestamp": e.timestamp.isoformat(),
        "payload": json.loads(e.payload) if e.payload else None,
    } for e in events]


# === MISSIONS ===
missions_router = APIRouter(prefix="/missions", tags=["Missions"])

@missions_router.get("")
def list_missions(db: Session = Depends(get_db)):
    missions = db.query(Mission).all()
    return [{
        "id": m.id, "name": m.name, "code": m.code, "description": m.description,
        "difficulty": m.difficulty, "category": m.category,
        "time_limit": m.time_limit,
        "objectives": json.loads(m.objectives) if m.objectives else [],
        "station_name": "",
    } for m in missions]

@missions_router.get("/{mission_id}")
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    m = db.query(Mission).filter(Mission.id == mission_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mission not found")
    return {
        "id": m.id, "name": m.name, "code": m.code, "description": m.description,
        "difficulty": m.difficulty, "category": m.category,
        "time_limit": m.time_limit,
        "objectives": json.loads(m.objectives) if m.objectives else [],
        "constraints": json.loads(m.constraints) if m.constraints else [],
        "initial_state": json.loads(m.initial_state) if m.initial_state else {},
    }


# === SIMULATION ===
simulation_router = APIRouter(prefix="/simulation", tags=["Simulation"])

@simulation_router.post("/start")
def start_sim(request: dict, db: Session = Depends(get_db)):
    instance = start_mission(db, request["mission_id"], request.get("user_id", 1))
    return {"instance_id": instance.id, "status": instance.status, "phase": instance.phase, "state": json.loads(instance.state)}

@simulation_router.post("/action")
def sim_action(request: dict, db: Session = Depends(get_db)):
    result = process_action(db, request["instance_id"], request["action"], request.get("choice"))
    return result

@simulation_router.get("/{instance_id}")
def get_sim(instance_id: int, db: Session = Depends(get_db)):
    inst = db.query(MissionInstance).filter(MissionInstance.id == instance_id).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Instance not found")
    events = db.query(MissionEvent).filter(MissionEvent.instance_id == instance_id).order_by(MissionEvent.timestamp).all()
    return {
        "id": inst.id, "mission_id": inst.mission_id,
        "mission_name": inst.mission.name if inst.mission else "",
        "status": inst.status, "phase": inst.phase, "turn": inst.turn,
        "state": json.loads(inst.state) if inst.state else {},
        "events": [{
            "id": e.id, "turn": e.turn, "type": e.event_type, "title": e.title,
            "description": e.description, "player_choice": e.player_choice,
            "options": json.loads(e.options) if e.options else [],
            "outcome": json.loads(e.outcome) if e.outcome else {},
        } for e in events],
    }

@simulation_router.get("/{instance_id}/debrief")
def get_debrief(instance_id: int, db: Session = Depends(get_db)):
    return calculate_score(db, instance_id)


# === LEADERBOARD ===
leaderboard_router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@leaderboard_router.get("")
def get_leaderboard(db: Session = Depends(get_db)):
    scores = db.query(Score).order_by(Score.total.desc()).limit(20).all()
    entries = []
    for i, s in enumerate(scores, 1):
        user = db.query(User).filter(User.id == s.user_id).first()
        mission_inst = db.query(MissionInstance).filter(MissionInstance.id == s.instance_id).first()
        entries.append({
            "rank": i,
            "user_id": s.user_id,
            "user_name": user.name if user else "Unknown",
            "total_score": s.total,
            "safety": s.safety,
            "efficiency": s.efficiency,
            "mission_name": mission_inst.mission.name if mission_inst and mission_inst.mission else "",
            "timestamp": s.timestamp.isoformat(),
        })
    return entries


# === DEMO ===
demo_router = APIRouter(prefix="/demo", tags=["Demo"])

@demo_router.post("/trigger-event")
def trigger_demo_event(request: dict, db: Session = Depends(get_db)):
    event_type = request.get("event_type", "WEATHER_DETERIORATION")
    station_id = request.get("station_id", 2)  # Default to Bharati

    handlers = {
        "WEATHER_DETERIORATION": lambda: create_event(
            db, "WEATHER_DETERIORATION", "station", station_id, "CRITICAL",
            "Severe weather deterioration detected",
            f"Extreme weather conditions developing at station. Wind speeds exceeding 80km/h.",
            {"station_id": station_id, "severity": "SEVERE", "temperature": -45, "wind_speed": 95, "visibility": 0.3, "precipitation": "blizzard"},
        ),
        "SHIPMENT_DELAYED": lambda: create_event(
            db, "SHIPMENT_DELAYED", "shipment",
            db.query(Shipment).filter(Shipment.status == "IN_TRANSIT").first().id if db.query(Shipment).filter(Shipment.status == "IN_TRANSIT").first() else 1,
            "HIGH", "Shipment delayed due to severe conditions",
            "Shipment experiencing significant delay. Revised ETA pending.",
            {"delay_hours": 24, "cause": "weather"},
        ),
        "ASSET_FAILURE": lambda: create_event(
            db, "ASSET_FAILURE", "asset",
            db.query(Asset).filter(Asset.station_id == station_id).first().id if db.query(Asset).filter(Asset.station_id == station_id).first() else 1,
            "HIGH", "Generator failure at station",
            "Primary generator has experienced a critical failure. Backup power engaged.",
            {"asset_type": "GENERATOR", "station_id": station_id},
        ),
        "STOCK_CRITICAL": lambda: create_event(
            db, "STOCK_CRITICAL", "inventory", None, "CRITICAL",
            "Critical fuel shortage",
            "Fuel levels have dropped below critical threshold.",
            {"item_name": "Diesel Fuel", "station_id": station_id, "station_name": "Bharati"},
        ),
        "AIRCRAFT_DELAYED": lambda: create_event(
            db, "AIRCRAFT_DELAYED", "asset", None, "HIGH",
            "Aircraft grounded",
            "Aircraft grounded due to extreme crosswinds. All air operations suspended.",
            {"delay_hours": 12, "cause": "crosswinds"},
        ),
        "FUEL_LEAK": lambda: create_event(
            db, "FUEL_LEAK", "station", station_id, "CRITICAL",
            "Fuel leak detected",
            "Fuel storage leak detected. Emergency response initiated.",
            {"station_id": station_id, "fuel_lost": 500},
        ),
    }

    handler = handlers.get(event_type)
    if not handler:
        raise HTTPException(status_code=400, detail=f"Unknown event type: {event_type}")

    event = handler()
    return {
        "status": "Event triggered",
        "event_id": event.id,
        "event_type": event.event_type,
        "severity": event.severity,
        "title": event.title,
    }

@demo_router.post("/reset")
def reset_demo(db: Session = Depends(get_db)):
    """Reset the demo scenario to initial state."""
    # Reset expeditions
    for exp in db.query(Expedition).all():
        if exp.code == "EXP-2026-014":
            exp.risk_score = 34
            exp.readiness_score = 88
        elif exp.code == "EXP-2026-015":
            exp.risk_score = 28
            exp.readiness_score = 92
    # Reset shipments
    for shp in db.query(Shipment).all():
        if shp.status == "DELAYED":
            shp.status = "IN_TRANSIT"
    # Reset assets
    for asset in db.query(Asset).filter(Asset.status == "MAINTENANCE_REQUIRED").all():
        asset.status = "IN_USE"
    # Clear recent events
    db.query(Event).filter(Event.severity.in_(["HIGH", "CRITICAL"])).delete()
    db.query(Recommendation).filter(Recommendation.status == "PENDING").delete()
    db.commit()
    return {"status": "Demo scenario reset to initial state"}


# === EXPLORER ===
explorer_router = APIRouter(prefix="/explorer", tags=["Explorer"])

STATION_EDUCATION = {
    "MAITRI": {
        "name": "Maitri",
        "full_name": "Maitri Research Station",
        "location": "Schirmacher Oasis, Queen Maud Land, Antarctica",
        "coordinates": "70°46'S, 11°44'E",
        "established": 1989,
        "where": "Located on the rocky Schirmacher Oasis between the continental ice sheet and the shelf ice on the Princess Astrid Coast of Queen Maud Land, East Antarctica.",
        "why": "India's second permanent Antarctic research station, serving as the primary operational base for Indian Antarctic expeditions. It replaced Dakshin Gangotri as the main station after it was buried under ice.",
        "research": "Atmospheric sciences, geological and biological studies, environmental monitoring, upper atmosphere studies, glaciology, and Earth sciences research. Houses multiple laboratories and observation equipment.",
        "logistics": "Supplied primarily by sea from India via ice-capable vessels. Summer season operations from November to March. Personnel rotated annually. Station has its own power generation, water recycling, and communication systems.",
        "challenges": "Extreme temperatures (-35°C), high wind speeds (up to 100km/h katabatic winds), limited daylight in winter (polar night), isolation from civilisation, logistical challenges of resupply across 10,000+ km.",
        "facts": ["Named after the Hindi word for 'friendship'", "Can accommodate up to 25 personnel in summer", "Built with a design suited to withstand Antarctic conditions", "Connected to Bharati via aerial and overland routes"],
    },
    "BHARATI": {
        "name": "Bharati",
        "full_name": "Bharati Research Station",
        "location": "Larsemann Hills, Prydz Bay, East Antarctica",
        "coordinates": "69°24'S, 76°12'E",
        "established": 2012,
        "where": "Situated on the Larsemann Hills, an ice-free rocky area on the coast of Prydz Bay in East Antarctica. The terrain is characterised by exposed granulite-grade metamorphic rocks.",
        "why": "India's third and newest Antarctic research station, built to expand India's research capability and reduce pressure on Maitri. It is a state-of-the-art facility designed to operate in extreme conditions.",
        "research": "Ocean and atmospheric sciences, geology, glaciology, cold region engineering, biological sciences. Features modern laboratories, satellite communication, and environmental monitoring systems.",
        "logistics": "Supplied by sea. The station uses modular construction designed to be assembled in the short Antarctic summer window. Power from diesel generators with plans for renewable energy integration.",
        "challenges": "Extremely harsh environment, temperatures dropping below -40°C, strong blizzards, pack ice limiting ship access, narrow summer window for construction and major logistics operations.",
        "facts": ["Named after the ancient Indian name for India", "Designed with 134 shipping containers forming the foundation", "Can accommodate up to 47 personnel", "One of the most modern Antarctic stations"],
    },
    "HIMADRI": {
        "name": "Himadri",
        "full_name": "Himadri Research Station",
        "location": "Ny-Ålesund, Svalbard, Norway (Arctic)",
        "coordinates": "78°55'N, 11°56'E",
        "established": 2008,
        "where": "Located at the International Arctic Research base in Ny-Ålesund on the island of Spitsbergen in Svalbard, Norway. One of the northernmost civilian settlements in the world.",
        "why": "India's first Arctic research station, established to study the effects of Arctic climate change on the Indian monsoon system and global climate patterns.",
        "research": "Arctic glaciology, atmospheric sciences, biological sciences, studies on Arctic warming and its impact on Indian monsoon patterns, GPS-based studies, microbiology, and geology.",
        "logistics": "Accessible year-round via flights to Longyearbyen and then to Ny-Ålesund. Shared international research infrastructure reduces individual logistics burden.",
        "challenges": "Extreme cold (down to -30°C), polar night in winter, polar bear encounters, permafrost conditions, rapid Arctic warming changing research conditions and safety parameters.",
        "facts": ["Named after the Sanskrit word for 'abode of snow' (Himalayas)", "India was granted Observer status in the Arctic Council in 2013", "Part of an international research community at Ny-Ålesund"],
    },
    "HIMANSH": {
        "name": "Himansh",
        "full_name": "Himansh Research Station",
        "location": "Sutri Dhaka Glacier, Chandra Basin, Himachal Pradesh, India",
        "coordinates": "32°23'N, 77°34'E",
        "established": 2016,
        "where": "Located at an altitude of over 4,000 metres in the Chandra Basin of the western Himalayas in Himachal Pradesh, near the Sutri Dhaka glacier.",
        "why": "India's high-altitude research station for studying Himalayan glaciers and climate, critical for understanding water resources and climate change impacts on the Indian subcontinent.",
        "research": "Glaciology, climate change monitoring, permafrost studies, glacier mass balance studies, water resource assessment, atmospheric sciences in high-altitude conditions.",
        "logistics": "Accessible by road (when roads are open, typically June-October). Supplies must be transported over mountain passes. Generator-powered. Limited connectivity.",
        "challenges": "High altitude (>4,000m), limited oxygen, extreme cold, heavy snowfall, roads blocked for months, avalanche risk, difficulty of carrying heavy equipment to high altitude.",
        "facts": ["Highest research station managed by NCPOR", "Critical for monitoring Himalayan glacier retreat", "Provides data on water resources for millions of people downstream"],
    },
}

@explorer_router.get("/stations")
def list_explorer_stations():
    return [{"code": code, **{k: v for k, v in data.items() if k in ("name", "full_name", "location", "established", "coordinates")}} for code, data in STATION_EDUCATION.items()]

@explorer_router.get("/stations/{station_code}")
def get_explorer_station(station_code: str):
    data = STATION_EDUCATION.get(station_code.upper())
    if not data:
        raise HTTPException(status_code=404, detail="Station not found")
    return data


# === RECOMMENDATIONS ===
recommendations_router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@recommendations_router.get("")
def list_recommendations(db: Session = Depends(get_db)):
    recs = db.query(Recommendation).order_by(Recommendation.timestamp.desc()).limit(20).all()
    return [{
        "id": r.id, "title": r.title, "description": r.description,
        "action": r.action, "priority": r.priority, "status": r.status,
        "expedition_id": r.expedition_id,
        "timestamp": r.timestamp.isoformat(),
    } for r in recs]

@recommendations_router.post("/{rec_id}/accept")
def accept_recommendation(rec_id: int, db: Session = Depends(get_db)):
    rec = db.query(Recommendation).filter(Recommendation.id == rec_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    rec.status = "ACCEPTED"
    db.commit()
    return {"status": "Recommendation accepted", "id": rec.id}
