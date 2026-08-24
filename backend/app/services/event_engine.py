"""Event Engine — the backbone of Polar Ops Commander.

Every operational change produces an event.
The engine propagates consequences to affected systems.
"""
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.event import Event, EventType, Severity
from app.models.shipment import Shipment, ShipmentLeg
from app.models.expedition import Expedition
from app.models.inventory import Inventory
from app.models.asset import Asset
from app.models.weather import WeatherObservation
from app.models.risk import Recommendation


def create_event(
    db: Session,
    event_type: str,
    entity_type: str = None,
    entity_id: int = None,
    severity: str = "INFO",
    title: str = "",
    description: str = "",
    payload: dict = None,
    actor_id: int = None,
) -> Event:
    """Create an event and trigger processing."""
    event = Event(
        event_type=event_type,
        severity=severity,
        entity_type=entity_type,
        entity_id=entity_id,
        title=title,
        description=description,
        payload=json.dumps(payload) if payload else None,
        actor_id=actor_id,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    # Process the event — propagate consequences
    process_event(db, event)

    return event


def process_event(db: Session, event: Event):
    """Dispatch event to appropriate handlers."""
    handlers = {
        "SHIPMENT_DELAYED": handle_shipment_delay,
        "WEATHER_DETERIORATION": handle_weather_deterioration,
        "WEATHER_EXTREME": handle_weather_deterioration,
        "ASSET_FAILURE": handle_asset_failure,
        "STOCK_LOW": handle_stock_alert,
        "STOCK_CRITICAL": handle_stock_alert,
        "VEHICLE_BREAKDOWN": handle_asset_failure,
        "AIRCRAFT_DELAYED": handle_aircraft_delay,
        "FUEL_LEAK": handle_fuel_leak,
    }

    handler = handlers.get(event.event_type)
    if handler:
        handler(db, event)

    event.processed = True
    db.commit()


def handle_shipment_delay(db: Session, event: Event):
    """Propagate shipment delay to affected expedition, cargo, and station."""
    payload = json.loads(event.payload) if event.payload else {}
    shipment_id = event.entity_id
    delay_hours = payload.get("delay_hours", 6)

    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        return

    # Update shipment status
    shipment.status = "DELAYED"

    # Update current in-transit leg
    for leg in shipment.legs:
        if leg.status == "IN_TRANSIT":
            leg.status = "DELAYED"
            break

    # If shipment is tied to an expedition, recalculate risk
    if shipment.expedition_id:
        expedition = db.query(Expedition).filter(
            Expedition.id == shipment.expedition_id
        ).first()
        if expedition:
            # Increase risk score
            expedition.risk_score = min(100, expedition.risk_score + 15)

            # Create recommendation
            rec = Recommendation(
                event_id=event.id,
                expedition_id=expedition.id,
                title=f"Shipment {shipment.code} delayed by {delay_hours}h",
                description=f"Shipment delay affects expedition {expedition.code}. Critical cargo may arrive late.",
                action=f"Consider rerouting critical cargo via alternative transport. Move priority items to air freight.",
                priority="HIGH",
                status="PENDING",
            )
            db.add(rec)

            # Create risk recalculation event
            risk_event = Event(
                event_type="RISK_RECALCULATED",
                severity="WARNING",
                entity_type="expedition",
                entity_id=expedition.id,
                title=f"Risk recalculated for {expedition.code}",
                description=f"Risk increased from {expedition.risk_score - 15:.0f}% to {expedition.risk_score:.0f}% due to shipment delay",
                timestamp=datetime.now(timezone.utc),
                processed=True,
            )
            db.add(risk_event)

    db.commit()


def handle_weather_deterioration(db: Session, event: Event):
    """Propagate weather change to affected shipments, aircraft, and expeditions."""
    payload = json.loads(event.payload) if event.payload else {}
    station_id = payload.get("station_id", event.entity_id)
    new_severity = payload.get("severity", "SEVERE")

    # Update weather observation
    weather = WeatherObservation(
        station_id=station_id,
        temperature=payload.get("temperature", -35),
        wind_speed=payload.get("wind_speed", 80),
        visibility=payload.get("visibility", 0.5),
        precipitation=payload.get("precipitation", "blizzard"),
        severity=new_severity,
        forecast_summary=f"Severe weather conditions. Wind speeds up to {payload.get('wind_speed', 80)}km/h. Visibility below 1km.",
        timestamp=datetime.now(timezone.utc),
    )
    db.add(weather)

    # Delay affected shipments heading to/from this station
    from app.models.station import Station
    station = db.query(Station).filter(Station.id == station_id).first()
    if station:
        shipments = db.query(Shipment).filter(
            (Shipment.destination == station.name) | (Shipment.origin == station.name),
            Shipment.status.in_(["IN_TRANSIT", "PLANNED", "BOOKED", "LOADED"]),
        ).all()

        for shp in shipments:
            delay_event = Event(
                event_type="SHIPMENT_DELAYED",
                severity="HIGH",
                entity_type="shipment",
                entity_id=shp.id,
                title=f"Shipment {shp.code} delayed due to weather",
                description=f"Weather deterioration at {station.name} affecting shipment routes",
                payload=json.dumps({"delay_hours": 12, "cause": "weather"}),
                timestamp=datetime.now(timezone.utc),
                processed=True,
            )
            db.add(delay_event)
            shp.status = "DELAYED"

        # Update affected expeditions
        expeditions = db.query(Expedition).filter(
            Expedition.destination_station_id == station_id,
            Expedition.status.in_(["PLANNED", "APPROVED", "PREPARING", "ACTIVE"]),
        ).all()

        for exp in expeditions:
            weather_risk_increase = 24 if new_severity == "EXTREME" else 18 if new_severity == "SEVERE" else 10
            exp.risk_score = min(100, exp.risk_score + weather_risk_increase)
            exp.readiness_score = max(0, exp.readiness_score - 15)

            rec = Recommendation(
                event_id=event.id,
                expedition_id=exp.id,
                title=f"Weather alert for {exp.code}",
                description=f"Severe weather at {station.name}. Transport operations may be affected.",
                action="Delay non-critical shipments. Prioritise critical scientific equipment and dispatch via Snow Vehicle Route B while holding non-critical cargo.",
                priority="CRITICAL" if new_severity in ("EXTREME", "SEVERE") else "HIGH",
                status="PENDING",
            )
            db.add(rec)

    db.commit()


def handle_asset_failure(db: Session, event: Event):
    """Handle asset failure — mark asset, check expedition dependencies."""
    asset_id = event.entity_id
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        return

    asset.status = "MAINTENANCE_REQUIRED"

    # Create recommendation
    rec = Recommendation(
        event_id=event.id,
        title=f"Asset {asset.code} requires maintenance",
        description=f"{asset.name} at {asset.station.name if asset.station else 'Unknown'} has failed. Immediate maintenance required.",
        action=f"Schedule emergency maintenance for {asset.name}. Check for backup equipment.",
        priority="HIGH",
        status="PENDING",
    )
    db.add(rec)
    db.commit()


def handle_aircraft_delay(db: Session, event: Event):
    """Handle aircraft delay — affects transport capacity."""
    payload = json.loads(event.payload) if event.payload else {}
    delay_hours = payload.get("delay_hours", 6)

    rec = Recommendation(
        event_id=event.id,
        title=f"Aircraft delayed by {delay_hours} hours",
        description="Aircraft unavailable for scheduled transport. Consider alternative routing.",
        action="Dispatch snow vehicles for priority cargo. Hold non-critical items for next aircraft window.",
        priority="HIGH",
        status="PENDING",
    )
    db.add(rec)
    db.commit()


def handle_stock_alert(db: Session, event: Event):
    """Handle low/critical stock alert."""
    payload = json.loads(event.payload) if event.payload else {}
    item_name = payload.get("item_name", "Unknown item")
    station_name = payload.get("station_name", "Unknown station")

    rec = Recommendation(
        event_id=event.id,
        title=f"Stock alert: {item_name} at {station_name}",
        description=f"Stock levels for {item_name} are {event.event_type.replace('STOCK_', '').lower()} at {station_name}.",
        action=f"Advance resupply schedule. Check alternative stations for emergency transfer.",
        priority="CRITICAL" if event.event_type == "STOCK_CRITICAL" else "HIGH",
        status="PENDING",
    )
    db.add(rec)
    db.commit()


def handle_fuel_leak(db: Session, event: Event):
    """Handle fuel leak — reduce inventory, create alert."""
    payload = json.loads(event.payload) if event.payload else {}
    station_id = payload.get("station_id")
    fuel_lost = payload.get("fuel_lost", 500)

    if station_id:
        fuel_inv = db.query(Inventory).join(Inventory.item).filter(
            Inventory.station_id == station_id,
        ).first()

        if fuel_inv:
            fuel_inv.quantity = max(0, fuel_inv.quantity - fuel_lost)

    rec = Recommendation(
        event_id=event.id,
        title="Fuel leak detected",
        description=f"Approximately {fuel_lost}L of fuel lost. Emergency fuel management required.",
        action="Seal leak source. Assess remaining fuel reserves. Request emergency resupply if below critical threshold.",
        priority="CRITICAL",
        status="PENDING",
    )
    db.add(rec)
    db.commit()


def get_recent_events(db: Session, limit: int = 50) -> list[Event]:
    """Get most recent events."""
    return db.query(Event).order_by(Event.timestamp.desc()).limit(limit).all()


def get_entity_events(db: Session, entity_type: str, entity_id: int) -> list[Event]:
    """Get events for a specific entity."""
    return db.query(Event).filter(
        Event.entity_type == entity_type,
        Event.entity_id == entity_id,
    ).order_by(Event.timestamp.desc()).all()
