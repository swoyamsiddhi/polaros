"""Polar Ops Commander — FastAPI Application Entry Point.

A centralised digital platform for polar expedition logistics,
built for SIH26062. NCPOR context.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db, SessionLocal
from app.routers.auth import router as auth_router
from app.routers.core import (
    dashboard_router,
    stations_router,
    expeditions_router,
    inventory_router,
    assets_router,
    shipments_router,
    personnel_router,
    alerts_router,
    weather_router,
    risk_router,
    planner_router,
    assistant_router,
    events_router,
    missions_router,
    simulation_router,
    leaderboard_router,
    demo_router,
    explorer_router,
    recommendations_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and seed data on startup."""
    # Import all models so tables are created
    import app.models  # noqa: F401

    init_db()

    # Seed database
    from app.seed.seed_data import seed_all
    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title="Polar Ops Commander API",
    description="Centralised polar expedition logistics, intelligence, and simulation platform. SIH26062.",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(stations_router)
app.include_router(expeditions_router)
app.include_router(inventory_router)
app.include_router(assets_router)
app.include_router(shipments_router)
app.include_router(personnel_router)
app.include_router(alerts_router)
app.include_router(weather_router)
app.include_router(risk_router)
app.include_router(planner_router)
app.include_router(assistant_router)
app.include_router(events_router)
app.include_router(missions_router)
app.include_router(simulation_router)
app.include_router(leaderboard_router)
app.include_router(demo_router)
app.include_router(explorer_router)
app.include_router(recommendations_router)


@app.get("/")
def root():
    return {
        "name": "Polar Ops Commander",
        "version": settings.APP_VERSION,
        "description": "Polar Expedition Logistics & Decision Support Platform",
        "status": "operational",
        "docs": "/docs",
        "data_notice": "DEMONSTRATION DATA — NOT LIVE GOVERNMENT OPERATIONS DATA",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
