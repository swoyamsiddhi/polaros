"""Risk Engine — explainable risk scoring for expeditions.

risk = weather * 0.25 + inventory * 0.20 + asset * 0.20
     + shipment * 0.15 + transport * 0.10 + personnel * 0.10

Every component returns a score + explanation.
"""
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.expedition import Expedition, ExpeditionCargo, ExpeditionPersonnel
from app.models.shipment import Shipment
from app.models.asset import Asset
from app.models.inventory import Inventory
from app.models.item import Item
from app.models.weather import WeatherObservation
from app.models.risk import RiskPrediction


RISK_WEIGHTS = {
    "weather": 0.25,
    "inventory": 0.20,
    "asset": 0.20,
    "shipment": 0.15,
    "transport": 0.10,
    "personnel": 0.10,
}


def calculate_risk(db: Session, expedition_id: int) -> dict:
    """Calculate explainable risk score for an expedition."""
    expedition = db.query(Expedition).filter(Expedition.id == expedition_id).first()
    if not expedition:
        return {"risk_score": 0, "risk_level": "LOW", "factors": []}

    station_id = expedition.destination_station_id
    factors = []

    # --- Weather risk ---
    latest_weather = (
        db.query(WeatherObservation)
        .filter(WeatherObservation.station_id == station_id)
        .order_by(WeatherObservation.timestamp.desc())
        .first()
    )
    weather_risk_map = {"NORMAL": 10, "WATCH": 30, "WARNING": 55, "SEVERE": 80, "EXTREME": 100}
    if latest_weather:
        w_score = weather_risk_map.get(latest_weather.severity, 30)
        w_explanation = f"Weather at destination: {latest_weather.severity}. Wind: {latest_weather.wind_speed}km/h, Visibility: {latest_weather.visibility}km"
    else:
        w_score = 30
        w_explanation = "No recent weather data available — moderate uncertainty"
    factors.append({"name": "Weather", "score": w_score, "weight": RISK_WEIGHTS["weather"], "explanation": w_explanation})

    # --- Inventory risk ---
    critical_items = (
        db.query(Inventory)
        .join(Item, Inventory.item_id == Item.id)
        .filter(
            Inventory.station_id == station_id,
            Item.criticality.in_(["HIGH", "CRITICAL"]),
        )
        .all()
    )
    if critical_items:
        low_stock_count = sum(1 for inv in critical_items if inv.quantity <= inv.item.min_stock)
        i_score = (low_stock_count / len(critical_items)) * 100
        i_explanation = f"{low_stock_count}/{len(critical_items)} critical items below minimum stock"
    else:
        i_score = 20
        i_explanation = "No critical inventory items tracked at destination"
    factors.append({"name": "Inventory", "score": i_score, "weight": RISK_WEIGHTS["inventory"], "explanation": i_explanation})

    # --- Asset risk ---
    station_assets = db.query(Asset).filter(Asset.station_id == station_id).all()
    if station_assets:
        maint_needed = sum(1 for a in station_assets if a.status in ("MAINTENANCE_REQUIRED", "MAINTENANCE"))
        a_score = (maint_needed / len(station_assets)) * 100
        a_explanation = f"{maint_needed}/{len(station_assets)} assets require or undergoing maintenance"
    else:
        a_score = 15
        a_explanation = "No assets tracked at destination station"
    factors.append({"name": "Assets", "score": a_score, "weight": RISK_WEIGHTS["asset"], "explanation": a_explanation})

    # --- Shipment risk ---
    shipments = db.query(Shipment).filter(
        Shipment.expedition_id == expedition_id
    ).all()
    if shipments:
        delayed = sum(1 for s in shipments if s.status == "DELAYED")
        s_score = (delayed / len(shipments)) * 100
        s_explanation = f"{delayed}/{len(shipments)} shipments delayed"
    else:
        s_score = 10
        s_explanation = "No associated shipments"
    factors.append({"name": "Shipment", "score": s_score, "weight": RISK_WEIGHTS["shipment"], "explanation": s_explanation})

    # --- Transport risk ---
    transport_assets = db.query(Asset).filter(
        Asset.station_id == station_id,
        Asset.category.in_(["AIRCRAFT", "HELICOPTER", "SNOW_VEHICLE", "VESSEL"]),
    ).all()
    if transport_assets:
        unavailable = sum(1 for a in transport_assets if a.status not in ("AVAILABLE", "ASSIGNED", "IN_USE", "READY"))
        t_score = (unavailable / len(transport_assets)) * 100
        t_explanation = f"{unavailable}/{len(transport_assets)} transport assets unavailable"
    else:
        t_score = 40
        t_explanation = "No transport assets tracked at destination"
    factors.append({"name": "Transport", "score": t_score, "weight": RISK_WEIGHTS["transport"], "explanation": t_explanation})

    # --- Personnel risk ---
    exp_personnel = db.query(ExpeditionPersonnel).filter(
        ExpeditionPersonnel.expedition_id == expedition_id
    ).all()
    if exp_personnel:
        delayed = sum(
            1 for ep in exp_personnel
            if ep.personnel and ep.personnel.travel_status in ("DELAYED", "IN_TRANSIT")
        )
        p_score = (delayed / len(exp_personnel)) * 100
        p_explanation = f"{delayed}/{len(exp_personnel)} personnel delayed or in transit"
    else:
        p_score = 5
        p_explanation = "No assigned personnel"
    factors.append({"name": "Personnel", "score": p_score, "weight": RISK_WEIGHTS["personnel"], "explanation": p_explanation})

    # Calculate weighted total
    risk_score = sum(f["score"] * f["weight"] for f in factors)
    risk_score = round(min(100, max(0, risk_score)), 1)

    # Determine level
    if risk_score >= 75:
        risk_level = "CRITICAL"
    elif risk_score >= 50:
        risk_level = "HIGH"
    elif risk_score >= 25:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Calculate contribution percentages
    total_weighted = sum(f["score"] * f["weight"] for f in factors) or 1
    for f in factors:
        f["contribution_pct"] = round((f["score"] * f["weight"] / total_weighted) * 100, 1)

    # Save prediction
    prediction = RiskPrediction(
        expedition_id=expedition_id,
        risk_score=risk_score,
        risk_level=risk_level,
        factors=json.dumps([{
            "name": f["name"],
            "score": round(f["score"], 1),
            "contribution_pct": f["contribution_pct"],
            "explanation": f["explanation"],
        } for f in factors]),
        timestamp=datetime.now(timezone.utc),
    )
    db.add(prediction)

    # Update expedition
    expedition.risk_score = risk_score
    db.commit()

    return {
        "expedition_id": expedition_id,
        "expedition_name": expedition.name,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "factors": [{
            "name": f["name"],
            "score": round(f["score"], 1),
            "contribution_pct": f["contribution_pct"],
            "explanation": f["explanation"],
        } for f in factors],
    }
