"""Forecasting Engine — inventory projection and resupply recommendations."""
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.models.item import Item
from app.models.shipment import Shipment, ShipmentLeg
from app.schemas.inventory import InventoryForecast


def forecast_inventory(db: Session, station_id: int, item_id: int) -> dict:
    """Project future stock levels and identify risk dates."""
    inv = db.query(Inventory).filter(
        Inventory.station_id == station_id,
        Inventory.item_id == item_id,
    ).first()

    if not inv:
        return {}

    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return {}

    current = inv.quantity
    consumption = inv.avg_daily_consumption or 0
    threshold = item.min_stock
    today = date.today()

    # Calculate days to critical
    if consumption > 0:
        days_to_critical = max(0, (current - threshold) / consumption)
        critical_date = today + timedelta(days=int(days_to_critical))
    else:
        days_to_critical = 999
        critical_date = None

    # Find next incoming shipment with this item
    next_resupply = None
    # Simple heuristic: look for planned/in-transit shipments to this station
    from app.models.station import Station
    station = db.query(Station).filter(Station.id == station_id).first()
    if station:
        legs = (
            db.query(ShipmentLeg)
            .filter(
                ShipmentLeg.destination == station.name,
                ShipmentLeg.status.in_(["PLANNED", "BOOKED", "LOADED", "IN_TRANSIT"]),
            )
            .order_by(ShipmentLeg.planned_arrival)
            .all()
        )
        if legs and legs[0].planned_arrival:
            next_resupply = legs[0].planned_arrival.date()

    # Determine risk
    if critical_date and next_resupply:
        if critical_date < next_resupply:
            risk = "HIGH"
            gap_days = (next_resupply - critical_date).days
            recommendation = f"Resupply should be brought forward by approximately {gap_days} days. Current trajectory reaches critical level before next scheduled delivery."
        else:
            risk = "LOW"
            recommendation = "Resupply schedule is adequate. Stock will remain above critical threshold."
    elif critical_date and days_to_critical < 14:
        risk = "HIGH"
        recommendation = f"Stock reaches critical level in {int(days_to_critical)} days. Schedule emergency resupply."
    elif critical_date and days_to_critical < 30:
        risk = "MEDIUM"
        recommendation = f"Stock projected to reach critical level in {int(days_to_critical)} days. Plan resupply."
    else:
        risk = "LOW"
        recommendation = "Stock levels adequate for foreseeable future."

    # Generate projection data points (30 days)
    projection_data = []
    for day in range(31):
        proj_date = today + timedelta(days=day)
        projected_stock = max(0, current - (consumption * day))

        # Add resupply bump if applicable
        if next_resupply and proj_date == next_resupply:
            projected_stock += item.max_stock * 0.5  # Assume 50% restock

        projection_data.append({
            "day": day,
            "date": proj_date.isoformat(),
            "projected_stock": round(projected_stock, 1),
            "threshold": threshold,
        })

    return {
        "item_name": item.name,
        "station_name": station.name if station else "",
        "current_stock": current,
        "unit": item.unit,
        "daily_consumption": consumption,
        "critical_threshold": threshold,
        "days_to_critical": round(days_to_critical, 1),
        "projected_critical_date": critical_date.isoformat() if critical_date else None,
        "next_resupply": next_resupply.isoformat() if next_resupply else None,
        "risk": risk,
        "recommendation": recommendation,
        "projection_data": projection_data,
    }
