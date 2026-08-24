"""Readiness Engine — computes expedition readiness from real operational data.

readiness = cargo * 0.20 + fuel * 0.15 + personnel * 0.15
           + transport * 0.15 + assets * 0.15 + weather * 0.20
"""
from sqlalchemy.orm import Session
from app.models.expedition import Expedition, ExpeditionCargo, ExpeditionPersonnel
from app.models.shipment import Shipment, ShipmentLeg
from app.models.asset import Asset
from app.models.weather import WeatherObservation
from app.models.inventory import Inventory
from app.models.item import Item


WEIGHTS = {
    "cargo": 0.20,
    "fuel": 0.15,
    "personnel": 0.15,
    "transportation": 0.15,
    "assets": 0.15,
    "weather": 0.20,
}


def calculate_readiness(db: Session, expedition_id: int) -> dict:
    """Calculate full readiness breakdown for an expedition."""
    expedition = db.query(Expedition).filter(Expedition.id == expedition_id).first()
    if not expedition:
        return {"overall": 0, "breakdown": {}}

    scores = {}

    # --- Cargo score ---
    cargo_items = db.query(ExpeditionCargo).filter(
        ExpeditionCargo.expedition_id == expedition_id
    ).all()
    if cargo_items:
        total_fulfillment = sum(
            min(c.fulfilled_quantity / max(c.required_quantity, 1), 1.0) * 100
            for c in cargo_items
        )
        scores["cargo"] = total_fulfillment / len(cargo_items)
    else:
        scores["cargo"] = 100.0

    # --- Fuel score ---
    station_id = expedition.destination_station_id
    fuel_items = (
        db.query(Inventory)
        .join(Item, Inventory.item_id == Item.id)
        .filter(
            Inventory.station_id == station_id,
            Item.category == "FUEL",
        )
        .all()
    )
    if fuel_items:
        fuel_score = sum(
            min(inv.quantity / max(inv.item.max_stock, 1), 1.0) * 100
            for inv in fuel_items
        ) / len(fuel_items)
        scores["fuel"] = fuel_score
    else:
        scores["fuel"] = 100.0

    # --- Personnel score ---
    required_personnel = len(
        db.query(ExpeditionPersonnel)
        .filter(ExpeditionPersonnel.expedition_id == expedition_id)
        .all()
    )
    if required_personnel > 0:
        # Check how many are at station or ready
        ready = sum(
            1 for ep in db.query(ExpeditionPersonnel).filter(
                ExpeditionPersonnel.expedition_id == expedition_id
            ).all()
            if ep.personnel and ep.personnel.travel_status in ("AT_STATION", "AT_FIELD_CAMP")
        )
        scores["personnel"] = (ready / required_personnel) * 100
    else:
        scores["personnel"] = 100.0

    # --- Transportation score ---
    shipments = db.query(Shipment).filter(
        Shipment.expedition_id == expedition_id
    ).all()
    if shipments:
        total_legs = 0
        booked_legs = 0
        for shp in shipments:
            for leg in shp.legs:
                total_legs += 1
                if leg.status in ("BOOKED", "LOADED", "IN_TRANSIT", "ARRIVED"):
                    booked_legs += 1
        scores["transportation"] = (booked_legs / max(total_legs, 1)) * 100
    else:
        scores["transportation"] = 90.0  # No specific shipments needed

    # --- Asset score ---
    # Check assets at destination station
    assets = db.query(Asset).filter(
        Asset.station_id == station_id,
        Asset.status.in_(["AVAILABLE", "ASSIGNED", "DEPLOYED", "IN_USE", "READY"]),
    ).all()
    total_assets = db.query(Asset).filter(Asset.station_id == station_id).count()
    if total_assets > 0:
        scores["assets"] = (len(assets) / total_assets) * 100
    else:
        scores["assets"] = 80.0

    # --- Weather score ---
    latest_weather = (
        db.query(WeatherObservation)
        .filter(WeatherObservation.station_id == station_id)
        .order_by(WeatherObservation.timestamp.desc())
        .first()
    )
    weather_scores = {
        "NORMAL": 100,
        "WATCH": 80,
        "WARNING": 60,
        "SEVERE": 30,
        "EXTREME": 10,
    }
    if latest_weather:
        scores["weather"] = weather_scores.get(latest_weather.severity, 70)
    else:
        scores["weather"] = 70.0

    # Calculate overall
    overall = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)

    # Update expedition
    expedition.readiness_score = round(overall, 1)
    db.commit()

    return {
        "overall": round(overall, 1),
        "breakdown": {k: round(v, 1) for k, v in scores.items()},
    }
