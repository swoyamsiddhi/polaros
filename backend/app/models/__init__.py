"""SQLAlchemy models — all models imported here for metadata registration."""
from app.models.user import User, Role
from app.models.station import Station
from app.models.personnel import Personnel
from app.models.item import Item
from app.models.inventory import Inventory, InventoryTransaction
from app.models.asset import Asset, MaintenanceTask
from app.models.expedition import Expedition, ExpeditionPersonnel, ExpeditionCargo
from app.models.shipment import Shipment, ShipmentLeg
from app.models.event import Event
from app.models.weather import WeatherObservation
from app.models.risk import RiskPrediction, Recommendation
from app.models.mission import Mission, MissionInstance, MissionEvent
from app.models.gamification import Score, Badge, UserBadge

__all__ = [
    "User", "Role",
    "Station",
    "Personnel",
    "Item", "Inventory", "InventoryTransaction",
    "Asset", "MaintenanceTask",
    "Expedition", "ExpeditionPersonnel", "ExpeditionCargo",
    "Shipment", "ShipmentLeg",
    "Event",
    "WeatherObservation",
    "RiskPrediction", "Recommendation",
    "Mission", "MissionInstance", "MissionEvent",
    "Score", "Badge", "UserBadge",
]
