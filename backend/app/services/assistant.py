"""NL Operations Assistant — deterministic keyword→query mapping.

Works WITHOUT any LLM API. Maps natural language queries to structured
backend function calls and returns formatted responses.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.expedition import Expedition
from app.models.shipment import Shipment
from app.models.asset import Asset
from app.models.inventory import Inventory
from app.models.item import Item
from app.models.station import Station
from app.models.weather import WeatherObservation
from app.models.risk import Recommendation


INTENT_KEYWORDS = {
    "risk": ["risk", "risky", "danger", "threat", "at risk"],
    "fuel": ["fuel", "fuel reserve", "fuel level", "fuel shortage"],
    "shipment": ["shipment", "delivery", "shipping", "transport", "delayed"],
    "maintenance": ["maintenance", "repair", "broken", "fix", "service"],
    "inventory": ["inventory", "stock", "supply", "shortage", "low stock"],
    "weather": ["weather", "storm", "blizzard", "temperature", "wind"],
    "expedition": ["expedition", "mission", "deploy"],
    "station": ["station", "base", "maitri", "bharati", "himadri", "himansh"],
    "personnel": ["personnel", "team", "crew", "scientist", "who is"],
    "asset": ["asset", "generator", "vehicle", "aircraft", "equipment"],
}


def process_query(db: Session, query: str) -> dict:
    """Process a natural language query and return structured response."""
    query_lower = query.lower().strip()

    # Detect intent
    intent = detect_intent(query_lower)

    handlers = {
        "risk": handle_risk_query,
        "fuel": handle_fuel_query,
        "shipment": handle_shipment_query,
        "maintenance": handle_maintenance_query,
        "inventory": handle_inventory_query,
        "weather": handle_weather_query,
        "expedition": handle_expedition_query,
        "station": handle_station_query,
        "personnel": handle_personnel_query,
        "asset": handle_asset_query,
    }

    handler = handlers.get(intent, handle_general_query)
    return handler(db, query_lower)


def detect_intent(query: str) -> str:
    """Simple keyword-based intent detection."""
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in query)
        if score > 0:
            scores[intent] = score

    if not scores:
        return "general"

    return max(scores, key=scores.get)


def handle_risk_query(db: Session, query: str) -> dict:
    """Handle risk-related queries."""
    expeditions = db.query(Expedition).filter(
        Expedition.status.in_(["PLANNED", "APPROVED", "PREPARING", "ACTIVE"]),
        Expedition.risk_score > 40,
    ).order_by(Expedition.risk_score.desc()).all()

    if not expeditions:
        return {
            "answer": "No expeditions are currently at elevated risk. All active expeditions have risk scores below 40%.",
            "data": {"at_risk_count": 0},
            "sources": ["Risk Engine"],
            "suggestions": ["Show all expeditions", "Check weather conditions"],
        }

    lines = [f"**{len(expeditions)} expedition(s) at elevated risk:**\n"]
    for exp in expeditions:
        level = "🔴 CRITICAL" if exp.risk_score >= 75 else "🟠 HIGH" if exp.risk_score >= 50 else "🟡 MEDIUM"
        lines.append(f"- **{exp.code}** ({exp.name}) — {level} {exp.risk_score:.0f}%")

    return {
        "answer": "\n".join(lines),
        "data": {"at_risk_count": len(expeditions), "expeditions": [
            {"code": e.code, "name": e.name, "risk": e.risk_score} for e in expeditions
        ]},
        "sources": ["Risk Engine", "Expedition Database"],
        "suggestions": [f"Why is {expeditions[0].code} risky?" if expeditions else "Check inventory levels"],
    }


def handle_fuel_query(db: Session, query: str) -> dict:
    """Handle fuel-related queries."""
    fuel_inventory = (
        db.query(Inventory, Item, Station)
        .join(Item, Inventory.item_id == Item.id)
        .join(Station, Inventory.station_id == Station.id)
        .filter(Item.category == "FUEL")
        .order_by(Inventory.quantity)
        .all()
    )

    if not fuel_inventory:
        return {"answer": "No fuel inventory data available.", "data": {}, "sources": ["Inventory Database"], "suggestions": []}

    lines = ["**Fuel reserves across stations:**\n"]
    lowest = None
    for inv, item, station in fuel_inventory:
        status = "🔴" if inv.quantity <= item.min_stock else "🟡" if inv.quantity <= item.min_stock * 2 else "🟢"
        lines.append(f"- {status} **{station.name}**: {inv.quantity:,.0f} {item.unit} (min: {item.min_stock:,.0f})")
        if lowest is None or inv.quantity < lowest[0]:
            lowest = (inv.quantity, station.name)

    if lowest:
        lines.append(f"\n⚠ **Lowest reserve**: {lowest[1]} with {lowest[0]:,.0f}L")

    return {
        "answer": "\n".join(lines),
        "data": {"stations": [{"station": s.name, "fuel": inv.quantity} for inv, _, s in fuel_inventory]},
        "sources": ["Inventory Database"],
        "suggestions": ["Forecast fuel at " + lowest[1] if lowest else "Check inventory alerts"],
    }


def handle_shipment_query(db: Session, query: str) -> dict:
    """Handle shipment-related queries."""
    if "delay" in query:
        delayed = db.query(Shipment).filter(Shipment.status == "DELAYED").all()
        if delayed:
            lines = [f"**{len(delayed)} shipment(s) currently delayed:**\n"]
            for s in delayed:
                lines.append(f"- **{s.code}**: {s.origin} → {s.destination} (Priority: {s.priority})")
            answer = "\n".join(lines)
        else:
            answer = "No shipments are currently delayed."
    else:
        active = db.query(Shipment).filter(Shipment.status.in_(["IN_TRANSIT", "LOADED", "BOOKED"])).all()
        lines = [f"**{len(active)} active shipment(s):**\n"]
        for s in active:
            lines.append(f"- **{s.code}**: {s.origin} → {s.destination} [{s.status}]")
        answer = "\n".join(lines)

    return {
        "answer": answer,
        "data": {},
        "sources": ["Shipment Tracking"],
        "suggestions": ["Show delayed shipments", "Track shipment S-204"],
    }


def handle_maintenance_query(db: Session, query: str) -> dict:
    """Handle maintenance-related queries."""
    assets = db.query(Asset).filter(
        Asset.status.in_(["MAINTENANCE_REQUIRED", "MAINTENANCE"])
    ).all()

    if assets:
        lines = [f"**{len(assets)} asset(s) require maintenance:**\n"]
        for a in assets:
            lines.append(f"- **{a.code}** ({a.name}) at {a.station.name if a.station else 'Unknown'} — {a.status}")
        answer = "\n".join(lines)
    else:
        answer = "No assets currently require immediate maintenance."

    return {"answer": answer, "data": {}, "sources": ["Asset Registry"], "suggestions": ["Check asset utilisation", "View maintenance schedule"]}


def handle_inventory_query(db: Session, query: str) -> dict:
    lines = ["**Low stock items:**\n"]
    low_stock = (
        db.query(Inventory, Item, Station)
        .join(Item, Inventory.item_id == Item.id)
        .join(Station, Inventory.station_id == Station.id)
        .filter(Inventory.quantity <= Item.min_stock * 1.5)
        .order_by(Inventory.quantity)
        .limit(10)
        .all()
    )
    for inv, item, station in low_stock:
        lines.append(f"- ⚠ **{item.name}** at {station.name}: {inv.quantity:.0f} {item.unit} (min: {item.min_stock})")

    return {"answer": "\n".join(lines) if low_stock else "All inventory levels are adequate.", "data": {}, "sources": ["Inventory Database"], "suggestions": []}


def handle_weather_query(db: Session, query: str) -> dict:
    stations = db.query(Station).all()
    lines = ["**Current weather conditions:**\n"]
    for station in stations:
        weather = db.query(WeatherObservation).filter(
            WeatherObservation.station_id == station.id
        ).order_by(WeatherObservation.timestamp.desc()).first()
        if weather:
            icon = {"NORMAL": "🟢", "WATCH": "🟡", "WARNING": "🟠", "SEVERE": "🔴", "EXTREME": "⛔"}.get(weather.severity, "⚪")
            lines.append(f"- {icon} **{station.name}**: {weather.severity} | {weather.temperature}°C | Wind: {weather.wind_speed}km/h | Vis: {weather.visibility}km")

    return {"answer": "\n".join(lines), "data": {}, "sources": ["Weather System"], "suggestions": []}


def handle_expedition_query(db: Session, query: str) -> dict:
    exps = db.query(Expedition).filter(Expedition.status.in_(["PLANNED", "APPROVED", "PREPARING", "ACTIVE"])).all()
    lines = [f"**{len(exps)} active expedition(s):**\n"]
    for e in exps:
        lines.append(f"- **{e.code}** ({e.name}) — Status: {e.status} | Readiness: {e.readiness_score:.0f}% | Risk: {e.risk_score:.0f}%")
    return {"answer": "\n".join(lines), "data": {}, "sources": ["Expedition Database"], "suggestions": []}


def handle_station_query(db: Session, query: str) -> dict:
    stations = db.query(Station).all()
    lines = ["**Station status:**\n"]
    for s in stations:
        icon = {"OPERATIONAL": "🟢", "LIMITED": "🟡", "MAINTENANCE": "🟠", "CLOSED": "🔴"}.get(s.status, "⚪")
        lines.append(f"- {icon} **{s.name}** ({s.type}) — {s.status} | Occupancy: {s.current_occupancy}/{s.capacity}")
    return {"answer": "\n".join(lines), "data": {}, "sources": ["Station Management"], "suggestions": []}


def handle_personnel_query(db: Session, query: str) -> dict:
    from app.models.personnel import Personnel
    personnel = db.query(Personnel).all()
    by_status = {}
    for p in personnel:
        by_status.setdefault(p.travel_status, []).append(p)
    lines = [f"**{len(personnel)} personnel tracked:**\n"]
    for status, people in by_status.items():
        lines.append(f"- **{status}**: {len(people)} personnel")
    return {"answer": "\n".join(lines), "data": {}, "sources": ["Personnel Database"], "suggestions": []}


def handle_asset_query(db: Session, query: str) -> dict:
    assets = db.query(Asset).all()
    by_status = {}
    for a in assets:
        by_status.setdefault(a.status, []).append(a)
    lines = [f"**{len(assets)} assets tracked:**\n"]
    for status, items in sorted(by_status.items()):
        lines.append(f"- **{status}**: {len(items)}")
    return {"answer": "\n".join(lines), "data": {}, "sources": ["Asset Registry"], "suggestions": []}


def handle_general_query(db: Session, query: str) -> dict:
    return {
        "answer": "I can help you with information about expeditions, inventory, shipments, assets, weather, personnel, and risk analysis. Try asking:\n\n- 'Which expeditions are at risk?'\n- 'What's the fuel level at Bharati?'\n- 'Which assets need maintenance?'\n- 'Show delayed shipments'\n- 'What's the weather at Maitri?'",
        "data": {},
        "sources": [],
        "suggestions": ["Which expeditions are at risk?", "Show fuel levels", "Check weather"],
    }
