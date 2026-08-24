"""Seed data — rich, realistic demonstration data for Polar Ops Commander.

All operational data is clearly SIMULATED DEMONSTRATION DATA.
Station names and locations use VERIFIED PUBLIC INFORMATION from NCPOR/MoES.
"""
import json
from datetime import date, datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.auth.jwt import hash_password
from app.models import *


def seed_all(db: Session):
    """Seed the entire database with demonstration data."""
    # Check if already seeded
    if db.query(User).count() > 0:
        print("Database already seeded. Skipping.")
        return

    print("🌍 Seeding Polar Ops Commander database...")

    # === ROLES ===
    roles = [
        Role(id=1, name="ADMIN", description="Full system access"),
        Role(id=2, name="LOGISTICS_OFFICER", description="Expedition and shipment management"),
        Role(id=3, name="STATION_MANAGER", description="Station-level operations"),
        Role(id=4, name="ASSET_MANAGER", description="Asset lifecycle management"),
        Role(id=5, name="EXPEDITION_COMMANDER", description="Expedition execution"),
        Role(id=6, name="FIELD_OPERATOR", description="Field updates and reporting"),
        Role(id=7, name="ANALYST", description="Analytics and reporting"),
        Role(id=8, name="TRAINER", description="Training and simulation management"),
        Role(id=9, name="STUDENT", description="Education environment only"),
    ]
    db.add_all(roles)
    db.flush()

    # === STATIONS ===
    stations = [
        Station(id=1, name="Maitri", code="MAITRI", type="ANTARCTIC", latitude=-70.766, longitude=11.733, altitude=123, capacity=25, current_occupancy=18, status="OPERATIONAL", comm_status="ONLINE", description="India's second permanent Antarctic research station in Schirmacher Oasis", established_year=1989, region="Queen Maud Land, Antarctica"),
        Station(id=2, name="Bharati", code="BHARATI", type="ANTARCTIC", latitude=-69.407, longitude=76.200, altitude=35, capacity=47, current_occupancy=24, status="OPERATIONAL", comm_status="ONLINE", description="India's newest Antarctic station at Larsemann Hills", established_year=2012, region="Larsemann Hills, East Antarctica"),
        Station(id=3, name="Himadri", code="HIMADRI", type="ARCTIC", latitude=78.925, longitude=11.933, altitude=8, capacity=20, current_occupancy=8, status="OPERATIONAL", comm_status="ONLINE", description="India's Arctic research base at Ny-Ålesund, Svalbard", established_year=2008, region="Svalbard, Norway"),
        Station(id=4, name="Himansh", code="HIMANSH", type="HIMALAYAN", latitude=32.383, longitude=77.567, altitude=4200, capacity=15, current_occupancy=6, status="OPERATIONAL", comm_status="INTERMITTENT", description="High-altitude Himalayan research station at Sutri Dhaka", established_year=2016, region="Chandra Basin, Himachal Pradesh"),
        Station(id=5, name="Field Camp Alpha", code="FC-ALPHA", type="FIELD_CAMP", latitude=-69.5, longitude=76.3, altitude=50, capacity=8, current_occupancy=4, status="OPERATIONAL", comm_status="INTERMITTENT", description="Temporary field camp near Bharati for geological surveys", region="Near Bharati"),
        Station(id=6, name="Field Camp Bravo", code="FC-BRAVO", type="FIELD_CAMP", latitude=-70.9, longitude=11.8, altitude=200, capacity=6, current_occupancy=3, status="LIMITED", comm_status="INTERMITTENT", description="Remote glaciology camp near Maitri", region="Near Maitri"),
        Station(id=7, name="NCPOR HQ Warehouse", code="GOA-WH", type="WAREHOUSE", latitude=15.395, longitude=73.878, altitude=5, capacity=500, current_occupancy=0, status="OPERATIONAL", comm_status="ONLINE", description="Central logistics warehouse at NCPOR headquarters, Goa", region="Vasco da Gama, Goa"),
    ]
    db.add_all(stations)
    db.flush()

    # === USERS ===
    pwd = hash_password("polarops2026")
    users = [
        User(id=1, name="Dr. Rajesh Kumar", email="admin@polarops.demo", password_hash=pwd, role_id=1, station_id=7),
        User(id=2, name="Cmdr. Anil Sharma", email="logistics@polarops.demo", password_hash=pwd, role_id=2, station_id=7),
        User(id=3, name="Dr. Priya Nair", email="station@polarops.demo", password_hash=pwd, role_id=3, station_id=2),
        User(id=4, name="Eng. Vikram Patel", email="asset@polarops.demo", password_hash=pwd, role_id=4, station_id=1),
        User(id=5, name="Col. Deepak Rao", email="commander@polarops.demo", password_hash=pwd, role_id=5, station_id=7),
        User(id=6, name="Tech. Sunil Mehra", email="field@polarops.demo", password_hash=pwd, role_id=6, station_id=5),
        User(id=7, name="Dr. Anita Desai", email="analyst@polarops.demo", password_hash=pwd, role_id=7, station_id=7),
        User(id=8, name="Capt. Ravi Menon", email="trainer@polarops.demo", password_hash=pwd, role_id=8, station_id=7),
        User(id=9, name="Student User", email="student@polarops.demo", password_hash=pwd, role_id=9),
    ]
    db.add_all(users)
    db.flush()

    # === PERSONNEL ===
    personnel = [
        Personnel(id=1, name="Dr. Priya Nair", role="Station Commander", organisation="NCPOR", specialisation="Polar Science", station_id=2, travel_status="AT_STATION"),
        Personnel(id=2, name="Eng. Vikram Patel", role="Chief Engineer", organisation="NCPOR", specialisation="Mechanical Engineering", station_id=1, travel_status="AT_STATION"),
        Personnel(id=3, name="Dr. Meera Joshi", role="Glaciologist", organisation="GSI", specialisation="Glaciology", station_id=2, travel_status="AT_STATION"),
        Personnel(id=4, name="Dr. Arjun Reddy", role="Atmospheric Scientist", organisation="NCAOR", specialisation="Atmospheric Sciences", station_id=1, travel_status="AT_STATION"),
        Personnel(id=5, name="Dr. Kavitha Iyer", role="Marine Biologist", organisation="NIO", specialisation="Marine Biology", station_id=3, travel_status="AT_STATION"),
        Personnel(id=6, name="Tech. Sunil Mehra", role="Field Technician", organisation="NCPOR", specialisation="Field Operations", station_id=5, travel_status="AT_FIELD_CAMP"),
        Personnel(id=7, name="Dr. Rahul Menon", role="Medical Officer", organisation="AFMS", specialisation="Polar Medicine", station_id=2, travel_status="AT_STATION"),
        Personnel(id=8, name="Eng. Pooja Sharma", role="Communications Engineer", organisation="ISRO", specialisation="Satellite Communications", station_id=1, travel_status="AT_STATION"),
        Personnel(id=9, name="Dr. Amit Kulkarni", role="Geologist", organisation="GSI", specialisation="Geology", station_id=5, travel_status="AT_FIELD_CAMP"),
        Personnel(id=10, name="Tech. Rajan Thomas", role="Vehicle Operator", organisation="NCPOR", specialisation="Snow Vehicle Operations", station_id=2, travel_status="AT_STATION"),
        Personnel(id=11, name="Cmdr. Anil Sharma", role="Logistics Officer", organisation="Indian Navy", specialisation="Naval Logistics", station_id=7, travel_status="AT_STATION"),
        Personnel(id=12, name="Dr. Sonia Ghosh", role="Biologist", organisation="ZSI", specialisation="Antarctic Biology", station_id=1, travel_status="AT_STATION"),
        Personnel(id=13, name="Eng. Manoj Tiwari", role="Power Systems Engineer", organisation="BHEL", specialisation="Power Generation", station_id=2, travel_status="AT_STATION"),
        Personnel(id=14, name="Dr. Neha Agarwal", role="Climate Researcher", organisation="IITM", specialisation="Climate Science", station_id=3, travel_status="AT_STATION"),
        Personnel(id=15, name="Tech. Dinesh Kumar", role="IT Specialist", organisation="NIC", specialisation="IT Systems", station_id=2, travel_status="AT_STATION"),
        Personnel(id=16, name="Dr. Ritu Verma", role="Meteorologist", organisation="IMD", specialisation="Polar Meteorology", station_id=1, travel_status="AT_STATION"),
        Personnel(id=17, name="Pilot Ajay Singh", role="Helicopter Pilot", organisation="IAF", specialisation="Polar Aviation", station_id=2, travel_status="AT_STATION"),
        Personnel(id=18, name="Cook Ramesh Yadav", role="Chef", organisation="NCPOR", specialisation="Polar Catering", station_id=1, travel_status="AT_STATION"),
        Personnel(id=19, name="Dr. Anand Mishra", role="Oceanographer", organisation="INCOIS", specialisation="Physical Oceanography", station_id=7, destination_id=2, travel_status="IN_TRANSIT", expected_arrival=datetime(2026, 12, 15, tzinfo=timezone.utc)),
        Personnel(id=20, name="Eng. Karthik Nambiar", role="Structural Engineer", organisation="CPWD", specialisation="Polar Construction", station_id=7, destination_id=2, travel_status="IN_TRANSIT", expected_arrival=datetime(2026, 12, 15, tzinfo=timezone.utc)),
        Personnel(id=21, name="Dr. Sunita Das", role="Physicist", organisation="PRL", specialisation="Upper Atmosphere Physics", station_id=1, travel_status="AT_STATION"),
        Personnel(id=22, name="Tech. Govind Raj", role="Mechanic", organisation="NCPOR", specialisation="Vehicle Maintenance", station_id=6, travel_status="AT_FIELD_CAMP"),
        Personnel(id=23, name="Dr. Farhan Ali", role="Geophysicist", organisation="NGRI", specialisation="Geophysics", station_id=4, travel_status="AT_STATION"),
        Personnel(id=24, name="Dr. Lakshmi Rajan", role="Cryosphere Scientist", organisation="SAC-ISRO", specialisation="Remote Sensing", station_id=4, travel_status="AT_STATION"),
        Personnel(id=25, name="Tech. Bhanu Pratap", role="Field Assistant", organisation="NCPOR", specialisation="Field Support", station_id=4, travel_status="AT_STATION"),
        Personnel(id=26, name="Dr. Vivek Saxena", role="Environmental Scientist", organisation="MoEFCC", specialisation="Environmental Monitoring", station_id=3, travel_status="AT_STATION"),
        Personnel(id=27, name="Nurse Anita Kaur", role="Paramedic", organisation="AFMS", specialisation="Emergency Medicine", station_id=1, travel_status="AT_STATION"),
        Personnel(id=28, name="Eng. Sanjay Gupta", role="Electrical Engineer", organisation="NCPOR", specialisation="Power Systems", station_id=1, travel_status="AT_STATION"),
        Personnel(id=29, name="Dr. Pankaj Jha", role="Seismologist", organisation="NCS", specialisation="Seismology", station_id=2, travel_status="AT_STATION"),
        Personnel(id=30, name="Eng. Naveen Pillai", role="Water Systems Engineer", organisation="NCPOR", specialisation="Water Treatment", station_id=2, travel_status="AT_STATION"),
        Personnel(id=31, name="Tech. Asha Rawat", role="Lab Technician", organisation="NCPOR", specialisation="Sample Analysis", station_id=1, travel_status="AT_STATION"),
        Personnel(id=32, name="Dr. Mohan Das", role="Research Scientist", organisation="NCPOR", specialisation="Polar Ecology", station_id=7, destination_id=1, travel_status="DELAYED", expected_arrival=datetime(2026, 12, 20, tzinfo=timezone.utc)),
        Personnel(id=33, name="Col. Deepak Rao", role="Expedition Commander", organisation="Indian Army", specialisation="Polar Expeditions", station_id=7, travel_status="AT_STATION"),
        Personnel(id=34, name="Dr. Shreya Mehta", role="Botanist", organisation="BSI", specialisation="Polar Botany", station_id=3, travel_status="AT_STATION"),
        Personnel(id=35, name="Tech. Rajiv Nair", role="Radio Operator", organisation="NCPOR", specialisation="Communications", station_id=6, travel_status="AT_FIELD_CAMP"),
    ]
    db.add_all(personnel)
    db.flush()

    # === ITEMS ===
    items = [
        Item(id=1, name="Diesel Fuel", category="FUEL", unit="L", criticality="CRITICAL", min_stock=2000, max_stock=20000),
        Item(id=2, name="Aviation Fuel (JET-A1)", category="FUEL", unit="L", criticality="CRITICAL", min_stock=1000, max_stock=10000),
        Item(id=3, name="Kerosene", category="FUEL", unit="L", criticality="HIGH", min_stock=500, max_stock=5000),
        Item(id=4, name="Ration Packs (30-day)", category="FOOD", unit="packs", criticality="CRITICAL", min_stock=30, max_stock=200, expiry_required=True),
        Item(id=5, name="Fresh Food Supplies", category="FOOD", unit="kg", criticality="MEDIUM", min_stock=100, max_stock=1000, expiry_required=True),
        Item(id=6, name="Drinking Water", category="WATER", unit="L", criticality="CRITICAL", min_stock=500, max_stock=5000),
        Item(id=7, name="First Aid Kits", category="MEDICAL", unit="units", criticality="CRITICAL", min_stock=10, max_stock=50),
        Item(id=8, name="Emergency Medication", category="MEDICAL", unit="units", criticality="CRITICAL", min_stock=20, max_stock=100, expiry_required=True),
        Item(id=9, name="Surgical Supplies", category="MEDICAL", unit="units", criticality="HIGH", min_stock=5, max_stock=30),
        Item(id=10, name="Satellite Phone", category="COMMUNICATION", unit="units", criticality="CRITICAL", min_stock=3, max_stock=15),
        Item(id=11, name="HF Radio Equipment", category="COMMUNICATION", unit="units", criticality="HIGH", min_stock=2, max_stock=10),
        Item(id=12, name="GPS Units", category="COMMUNICATION", unit="units", criticality="HIGH", min_stock=5, max_stock=20),
        Item(id=13, name="Weather Station Sensors", category="SCIENTIFIC", unit="units", criticality="HIGH", min_stock=3, max_stock=15),
        Item(id=14, name="Ice Core Drilling Equipment", category="SCIENTIFIC", unit="units", criticality="MEDIUM", min_stock=1, max_stock=5),
        Item(id=15, name="Seismograph Components", category="SCIENTIFIC", unit="units", criticality="MEDIUM", min_stock=2, max_stock=8),
        Item(id=16, name="Generator Spare Parts", category="SPARE_PARTS", unit="sets", criticality="CRITICAL", min_stock=3, max_stock=15),
        Item(id=17, name="Vehicle Engine Parts", category="SPARE_PARTS", unit="sets", criticality="HIGH", min_stock=4, max_stock=20),
        Item(id=18, name="Electrical Components", category="SPARE_PARTS", unit="sets", criticality="HIGH", min_stock=5, max_stock=25),
        Item(id=19, name="Extreme Cold Weather Gear", category="CLOTHING", unit="sets", criticality="CRITICAL", min_stock=20, max_stock=100),
        Item(id=20, name="Snow Boots", category="CLOTHING", unit="pairs", criticality="HIGH", min_stock=15, max_stock=60),
        Item(id=21, name="Emergency Flares", category="SAFETY", unit="units", criticality="CRITICAL", min_stock=20, max_stock=100),
        Item(id=22, name="Fire Extinguishers", category="SAFETY", unit="units", criticality="CRITICAL", min_stock=10, max_stock=40),
        Item(id=23, name="Rescue Equipment", category="SAFETY", unit="sets", criticality="HIGH", min_stock=3, max_stock=15),
        Item(id=24, name="Solar Panels", category="POWER", unit="units", criticality="MEDIUM", min_stock=5, max_stock=30),
        Item(id=25, name="Battery Packs", category="POWER", unit="units", criticality="HIGH", min_stock=10, max_stock=50),
        Item(id=26, name="Portable Shelter Units", category="SHELTER", unit="units", criticality="HIGH", min_stock=2, max_stock=10),
        Item(id=27, name="Tool Kits", category="TOOLS", unit="sets", criticality="MEDIUM", min_stock=5, max_stock=25),
        Item(id=28, name="Water Purification Tablets", category="WATER", unit="packs", criticality="HIGH", min_stock=50, max_stock=300, expiry_required=True),
        Item(id=29, name="Cooking Gas Cylinders", category="FUEL", unit="units", criticality="HIGH", min_stock=10, max_stock=50),
        Item(id=30, name="Research Sample Containers", category="SCIENTIFIC", unit="units", criticality="MEDIUM", min_stock=50, max_stock=500),
    ]
    db.add_all(items)
    db.flush()

    # === INVENTORY (distributed across stations) ===
    inventory_data = [
        # Maitri
        (1, 1, 12000, 2000, 700), (1, 2, 4500, 500, 150), (1, 3, 2800, 200, 80),
        (1, 4, 90, 0, 1), (1, 5, 350, 0, 12), (1, 6, 3000, 0, 120),
        (1, 7, 25, 0, 0.1), (1, 8, 45, 0, 0.2), (1, 10, 8, 2, 0),
        (1, 16, 8, 2, 0.02), (1, 17, 12, 0, 0.05), (1, 19, 40, 5, 0.1),
        (1, 21, 60, 0, 0.1), (1, 22, 20, 0, 0), (1, 25, 30, 5, 0.2),
        # Bharati
        (2, 1, 8400, 1500, 600), (2, 2, 3200, 300, 100), (2, 3, 1500, 0, 50),
        (2, 4, 65, 0, 1), (2, 5, 220, 0, 10), (2, 6, 2500, 0, 100),
        (2, 7, 18, 0, 0.1), (2, 8, 35, 0, 0.15), (2, 10, 6, 1, 0),
        (2, 13, 8, 0, 0), (2, 14, 3, 1, 0), (2, 16, 5, 1, 0.02),
        (2, 19, 35, 3, 0.1), (2, 21, 45, 0, 0.05), (2, 24, 12, 0, 0),
        # Himadri
        (3, 1, 3500, 500, 200), (3, 4, 40, 0, 0.5), (3, 7, 10, 0, 0),
        (3, 10, 4, 0, 0), (3, 13, 5, 0, 0), (3, 19, 15, 0, 0.05),
        # Himansh
        (4, 1, 2200, 300, 150), (4, 4, 25, 0, 0.5), (4, 7, 6, 0, 0),
        (4, 10, 3, 0, 0), (4, 19, 12, 0, 0.05), (4, 29, 18, 0, 0.3),
        # Field Camp Alpha
        (5, 1, 1800, 0, 500), (5, 4, 15, 0, 0.5), (5, 7, 4, 0, 0),
        (5, 21, 15, 0, 0.05),
        # Field Camp Bravo
        (6, 1, 1200, 0, 400), (6, 4, 10, 0, 0.5), (6, 7, 3, 0, 0),
        # Goa Warehouse
        (7, 1, 50000, 10000, 0), (7, 2, 20000, 5000, 0), (7, 4, 500, 50, 0),
        (7, 5, 2000, 0, 0), (7, 7, 100, 10, 0), (7, 8, 200, 20, 0),
        (7, 10, 30, 5, 0), (7, 13, 20, 5, 0), (7, 16, 40, 10, 0),
        (7, 17, 50, 10, 0), (7, 19, 200, 30, 0), (7, 21, 300, 0, 0),
    ]
    for sid, iid, qty, reserved, consumption in inventory_data:
        db.add(Inventory(station_id=sid, item_id=iid, quantity=qty, reserved_quantity=reserved, avg_daily_consumption=consumption))
    db.flush()

    # === ASSETS ===
    today = date.today()
    assets = [
        Asset(id=1, code="GEN-M01", name="Primary Diesel Generator", category="GENERATOR", serial_number="DG-2019-001", station_id=1, custodian="Eng. Vikram Patel", status="IN_USE", utilisation_pct=92, engine_hours=4820, maintenance_threshold_hours=5000, last_maintenance=today - timedelta(days=45), next_maintenance=today + timedelta(days=15), replacement_cost=250000),
        Asset(id=2, code="GEN-M02", name="Backup Generator", category="GENERATOR", serial_number="DG-2020-002", station_id=1, custodian="Eng. Vikram Patel", status="AVAILABLE", utilisation_pct=30, engine_hours=1200, last_maintenance=today - timedelta(days=30), next_maintenance=today + timedelta(days=60), replacement_cost=250000),
        Asset(id=3, code="GEN-B01", name="Primary Generator Bharati", category="GENERATOR", serial_number="DG-2021-003", station_id=2, custodian="Eng. Manoj Tiwari", status="IN_USE", utilisation_pct=85, engine_hours=3600, last_maintenance=today - timedelta(days=60), next_maintenance=today + timedelta(days=30), replacement_cost=300000),
        Asset(id=4, code="GEN-B02", name="Backup Generator Bharati", category="GENERATOR", serial_number="DG-2021-004", station_id=2, status="AVAILABLE", utilisation_pct=20, engine_hours=800, replacement_cost=300000),
        Asset(id=5, code="SV-M01", name="Snow Cat Maitri-1", category="SNOW_VEHICLE", serial_number="SC-2020-001", station_id=1, custodian="Tech. Rajan Thomas", status="IN_USE", utilisation_pct=78, engine_hours=3200, last_maintenance=today - timedelta(days=20), replacement_cost=450000),
        Asset(id=6, code="SV-M02", name="Snow Cat Maitri-2", category="SNOW_VEHICLE", serial_number="SC-2020-002", station_id=1, status="AVAILABLE", utilisation_pct=45, engine_hours=1800, replacement_cost=450000),
        Asset(id=7, code="SV-B01", name="PistenBully Bharati-1", category="SNOW_VEHICLE", serial_number="PB-2022-001", station_id=2, custodian="Tech. Rajan Thomas", status="IN_USE", utilisation_pct=70, engine_hours=2800, replacement_cost=500000),
        Asset(id=8, code="SV-B02", name="PistenBully Bharati-2", category="SNOW_VEHICLE", serial_number="PB-2022-002", station_id=2, status="MAINTENANCE_REQUIRED", utilisation_pct=88, engine_hours=4200, maintenance_threshold_hours=4500, replacement_cost=500000),
        Asset(id=9, code="HELI-01", name="Chetak Helicopter", category="HELICOPTER", serial_number="CH-2019-001", station_id=2, custodian="Pilot Ajay Singh", status="AVAILABLE", utilisation_pct=55, engine_hours=2100, replacement_cost=1200000),
        Asset(id=10, code="AC-01", name="Polar Transport Aircraft", category="AIRCRAFT", serial_number="PA-2020-001", station_id=7, status="ASSIGNED", utilisation_pct=60, engine_hours=3400, replacement_cost=5000000),
        Asset(id=11, code="COMM-M01", name="VSAT Terminal Maitri", category="COMMUNICATION", serial_number="VS-2021-001", station_id=1, status="IN_USE", utilisation_pct=95, engine_hours=8000, replacement_cost=150000),
        Asset(id=12, code="COMM-B01", name="VSAT Terminal Bharati", category="COMMUNICATION", serial_number="VS-2021-002", station_id=2, status="IN_USE", utilisation_pct=90, replacement_cost=150000),
        Asset(id=13, code="SCI-M01", name="Automatic Weather Station", category="SCIENTIFIC", serial_number="AWS-2020-001", station_id=1, status="IN_USE", utilisation_pct=100, replacement_cost=80000),
        Asset(id=14, code="SCI-B01", name="Ice Core Drill", category="SCIENTIFIC", serial_number="ICD-2022-001", station_id=2, status="DEPLOYED", utilisation_pct=65, replacement_cost=200000),
        Asset(id=15, code="SCI-B02", name="Seismograph Array", category="SCIENTIFIC", serial_number="SA-2021-001", station_id=2, custodian="Dr. Pankaj Jha", status="IN_USE", utilisation_pct=100, replacement_cost=120000),
        Asset(id=16, code="NAV-01", name="GPS Base Station", category="NAVIGATION", serial_number="GPS-2021-001", station_id=2, status="IN_USE", utilisation_pct=100, replacement_cost=50000),
        Asset(id=17, code="REF-M01", name="Cold Storage Unit Maitri", category="REFRIGERATION", serial_number="CS-2019-001", station_id=1, status="IN_USE", utilisation_pct=80, engine_hours=6000, maintenance_threshold_hours=6500, replacement_cost=95000),
        Asset(id=18, code="PWR-B01", name="Solar Array Bharati", category="POWER", serial_number="SOL-2022-001", station_id=2, status="IN_USE", utilisation_pct=40, replacement_cost=180000),
        Asset(id=19, code="SV-FC01", name="Field Cat Alpha", category="SNOW_VEHICLE", serial_number="FC-2023-001", station_id=5, status="IN_USE", utilisation_pct=80, engine_hours=1600, replacement_cost=350000),
        Asset(id=20, code="GEN-H01", name="Generator Himadri", category="GENERATOR", serial_number="DG-2018-005", station_id=3, status="IN_USE", utilisation_pct=60, engine_hours=2800, replacement_cost=200000),
    ]
    db.add_all(assets)
    db.flush()

    # === MAINTENANCE TASKS ===
    maintenance = [
        MaintenanceTask(asset_id=1, type="ROUTINE", status="SCHEDULED", description="5000-hour engine service", scheduled_date=today + timedelta(days=15)),
        MaintenanceTask(asset_id=1, type="REPAIR", status="COMPLETED", description="Coolant system repair", scheduled_date=today - timedelta(days=45), completed_date=today - timedelta(days=43)),
        MaintenanceTask(asset_id=1, type="REPAIR", status="COMPLETED", description="Fuel injector replacement", scheduled_date=today - timedelta(days=90), completed_date=today - timedelta(days=88)),
        MaintenanceTask(asset_id=8, type="REPAIR", status="SCHEDULED", description="Track replacement and engine inspection", scheduled_date=today + timedelta(days=5)),
        MaintenanceTask(asset_id=5, type="INSPECTION", status="COMPLETED", description="Annual inspection", scheduled_date=today - timedelta(days=20), completed_date=today - timedelta(days=20)),
        MaintenanceTask(asset_id=17, type="ROUTINE", status="SCHEDULED", description="Compressor maintenance", scheduled_date=today + timedelta(days=10)),
    ]
    db.add_all(maintenance)
    db.flush()

    # === EXPEDITIONS ===
    expeditions = [
        Expedition(id=1, code="EXP-2026-014", name="Antarctic Scientific Expedition", description="Multi-disciplinary scientific expedition to Bharati station", origin="Goa, India", destination_station_id=2, start_date=date(2026, 12, 10), end_date=date(2027, 1, 25), priority="HIGH", status="PLANNED", mission_objectives="Geological surveys, ice core sampling, atmospheric monitoring, biological specimen collection", readiness_score=88, risk_score=34),
        Expedition(id=2, code="EXP-2026-015", name="Maitri Resupply Mission", description="Annual resupply to Maitri research station", origin="Goa, India", destination_station_id=1, start_date=date(2026, 11, 15), end_date=date(2027, 1, 10), priority="HIGH", status="APPROVED", mission_objectives="Annual resupply of fuel, food, medical supplies, and equipment", readiness_score=92, risk_score=28),
        Expedition(id=3, code="EXP-2026-016", name="Arctic Climate Study", description="Climate monitoring at Himadri", origin="New Delhi", destination_station_id=3, start_date=date(2026, 6, 1), end_date=date(2026, 8, 30), priority="MEDIUM", status="ACTIVE", readiness_score=95, risk_score=15),
        Expedition(id=4, code="EXP-2026-017", name="Himalayan Glacier Survey", description="Glacier mass balance study at Himansh", origin="New Delhi", destination_station_id=4, start_date=date(2026, 7, 1), end_date=date(2026, 9, 30), priority="MEDIUM", status="IN_PROGRESS", readiness_score=90, risk_score=20),
        Expedition(id=5, code="EXP-2026-018", name="Bharati Winter Crew Rotation", description="Winter team deployment and summer team return", origin="Goa, India", destination_station_id=2, start_date=date(2027, 2, 1), end_date=date(2027, 3, 15), priority="CRITICAL", status="PLANNED", readiness_score=45, risk_score=55),
        Expedition(id=6, code="EXP-2025-012", name="Southern Ocean Research", description="Oceanographic research cruise", origin="Goa, India", destination_station_id=2, start_date=date(2026, 1, 10), end_date=date(2026, 3, 20), priority="HIGH", status="COMPLETED", readiness_score=100, risk_score=0),
        Expedition(id=7, code="EXP-2026-019", name="Field Camp Establishment", description="Establish new field camp for deep ice studies", origin="Bharati", destination_station_id=5, start_date=date(2026, 12, 20), end_date=date(2027, 1, 15), priority="MEDIUM", status="DRAFT", readiness_score=30, risk_score=40),
        Expedition(id=8, code="EXP-2026-020", name="Emergency Medical Evacuation Preparedness", description="Medical readiness drill and equipment positioning", origin="Goa, India", destination_station_id=1, start_date=date(2026, 11, 1), end_date=date(2026, 11, 20), priority="HIGH", status="PREPARING", readiness_score=75, risk_score=30),
    ]
    db.add_all(expeditions)
    db.flush()

    # === EXPEDITION PERSONNEL ===
    exp_personnel = [
        ExpeditionPersonnel(expedition_id=1, personnel_id=3, role_in_expedition="Lead Scientist"),
        ExpeditionPersonnel(expedition_id=1, personnel_id=7, role_in_expedition="Medical Officer"),
        ExpeditionPersonnel(expedition_id=1, personnel_id=10, role_in_expedition="Vehicle Operator"),
        ExpeditionPersonnel(expedition_id=1, personnel_id=13, role_in_expedition="Power Engineer"),
        ExpeditionPersonnel(expedition_id=1, personnel_id=19, role_in_expedition="Oceanographer"),
        ExpeditionPersonnel(expedition_id=1, personnel_id=20, role_in_expedition="Construction"),
        ExpeditionPersonnel(expedition_id=1, personnel_id=29, role_in_expedition="Seismologist"),
        ExpeditionPersonnel(expedition_id=2, personnel_id=2, role_in_expedition="Chief Engineer"),
        ExpeditionPersonnel(expedition_id=2, personnel_id=4, role_in_expedition="Scientist"),
        ExpeditionPersonnel(expedition_id=2, personnel_id=12, role_in_expedition="Biologist"),
        ExpeditionPersonnel(expedition_id=2, personnel_id=32, role_in_expedition="Ecologist"),
        ExpeditionPersonnel(expedition_id=3, personnel_id=5, role_in_expedition="Lead Researcher"),
        ExpeditionPersonnel(expedition_id=3, personnel_id=14, role_in_expedition="Climate Researcher"),
        ExpeditionPersonnel(expedition_id=4, personnel_id=23, role_in_expedition="Lead Scientist"),
        ExpeditionPersonnel(expedition_id=4, personnel_id=24, role_in_expedition="Remote Sensing"),
    ]
    db.add_all(exp_personnel)
    db.flush()

    # === EXPEDITION CARGO ===
    exp_cargo = [
        ExpeditionCargo(expedition_id=1, item_id=1, required_quantity=15000, fulfilled_quantity=13500),
        ExpeditionCargo(expedition_id=1, item_id=2, required_quantity=5000, fulfilled_quantity=5000),
        ExpeditionCargo(expedition_id=1, item_id=4, required_quantity=60, fulfilled_quantity=60),
        ExpeditionCargo(expedition_id=1, item_id=7, required_quantity=10, fulfilled_quantity=8),
        ExpeditionCargo(expedition_id=1, item_id=10, required_quantity=5, fulfilled_quantity=5),
        ExpeditionCargo(expedition_id=1, item_id=13, required_quantity=4, fulfilled_quantity=3),
        ExpeditionCargo(expedition_id=1, item_id=16, required_quantity=5, fulfilled_quantity=5),
        ExpeditionCargo(expedition_id=1, item_id=19, required_quantity=20, fulfilled_quantity=18),
        ExpeditionCargo(expedition_id=2, item_id=1, required_quantity=20000, fulfilled_quantity=20000),
        ExpeditionCargo(expedition_id=2, item_id=4, required_quantity=100, fulfilled_quantity=95),
        ExpeditionCargo(expedition_id=2, item_id=5, required_quantity=500, fulfilled_quantity=500),
        ExpeditionCargo(expedition_id=2, item_id=16, required_quantity=8, fulfilled_quantity=8),
    ]
    db.add_all(exp_cargo)
    db.flush()

    # === SHIPMENTS ===
    now = datetime.now(timezone.utc)
    shipments_data = [
        # EXP-2026-014 shipments
        Shipment(id=1, code="S-204", expedition_id=1, origin="Goa, India", destination="Bharati", status="IN_TRANSIT", priority="HIGH", total_weight=45000, cargo_description="Scientific equipment, fuel, provisions, spare parts"),
        Shipment(id=2, code="S-205", expedition_id=1, origin="Goa, India", destination="Bharati", status="PLANNED", priority="MEDIUM", total_weight=30000, cargo_description="Construction materials, additional provisions"),
        Shipment(id=3, code="S-206", expedition_id=1, origin="Bharati", destination="Field Camp Alpha", status="PLANNED", priority="HIGH", total_weight=5000, cargo_description="Field equipment, fuel, rations"),
        # EXP-2026-015 shipments
        Shipment(id=4, code="S-207", expedition_id=2, origin="Goa, India", destination="Maitri", status="LOADED", priority="HIGH", total_weight=60000, cargo_description="Annual resupply — fuel, food, medical, equipment"),
        Shipment(id=5, code="S-208", expedition_id=2, origin="Goa, India", destination="Maitri", status="PLANNED", priority="MEDIUM", total_weight=25000, cargo_description="Scientific instruments, spare parts"),
        # Other shipments
        Shipment(id=6, code="S-209", expedition_id=3, origin="New Delhi", destination="Himadri", status="ARRIVED", priority="MEDIUM", total_weight=2000, cargo_description="Climate monitoring equipment"),
        Shipment(id=7, code="S-210", expedition_id=4, origin="New Delhi", destination="Himansh", status="IN_TRANSIT", priority="MEDIUM", total_weight=3000, cargo_description="Glacier survey equipment"),
        Shipment(id=8, code="S-211", expedition_id=None, origin="Goa, India", destination="Bharati", status="BOOKED", priority="LOW", total_weight=15000, cargo_description="Non-critical supplies and comfort items"),
        Shipment(id=9, code="S-212", expedition_id=5, origin="Goa, India", destination="Bharati", status="PLANNED", priority="CRITICAL", total_weight=40000, cargo_description="Winter crew rotation supplies"),
        Shipment(id=10, code="S-213", expedition_id=8, origin="Goa, India", destination="Maitri", status="PLANNED", priority="HIGH", total_weight=8000, cargo_description="Emergency medical equipment"),
    ]
    db.add_all(shipments_data)
    db.flush()

    # === SHIPMENT LEGS ===
    legs = [
        # S-204 legs (multi-leg to Bharati)
        ShipmentLeg(shipment_id=1, sequence=1, origin="Mormugao Port, Goa", destination="Cape Town, South Africa", mode="SEA", vehicle="MV Polar Quest", planned_departure=now - timedelta(days=10), planned_arrival=now - timedelta(days=2), actual_departure=now - timedelta(days=10), actual_arrival=now - timedelta(days=2), status="ARRIVED", cargo_description="Full cargo container", distance_km=8200),
        ShipmentLeg(shipment_id=1, sequence=2, origin="Cape Town, South Africa", destination="Antarctic Gateway (Crown Bay)", mode="SEA", vehicle="MV Polar Quest", planned_departure=now - timedelta(days=1), planned_arrival=now + timedelta(days=6), actual_departure=now - timedelta(days=1), status="IN_TRANSIT", cargo_description="Full cargo", distance_km=5500),
        ShipmentLeg(shipment_id=1, sequence=3, origin="Antarctic Gateway", destination="Bharati Station", mode="HELICOPTER", vehicle="Chetak HELI-01", planned_departure=now + timedelta(days=7), planned_arrival=now + timedelta(days=7, hours=4), status="PLANNED", cargo_description="Priority scientific equipment", distance_km=120),
        ShipmentLeg(shipment_id=1, sequence=4, origin="Antarctic Gateway", destination="Bharati Station", mode="SNOW_VEHICLE", vehicle="PistenBully SV-B01", planned_departure=now + timedelta(days=7), planned_arrival=now + timedelta(days=9), status="PLANNED", cargo_description="Bulk cargo and fuel", distance_km=120),
        # S-207 legs
        ShipmentLeg(shipment_id=4, sequence=1, origin="Mormugao Port, Goa", destination="Cape Town", mode="SEA", vehicle="ORV Sagar Kanya", planned_departure=now + timedelta(days=5), planned_arrival=now + timedelta(days=17), status="BOOKED", distance_km=8200),
        ShipmentLeg(shipment_id=4, sequence=2, origin="Cape Town", destination="Maitri Station", mode="SEA", vehicle="ORV Sagar Kanya", planned_departure=now + timedelta(days=18), planned_arrival=now + timedelta(days=26), status="PLANNED", distance_km=5500),
        ShipmentLeg(shipment_id=4, sequence=3, origin="Maitri Station", destination="Field Camp Bravo", mode="SNOW_VEHICLE", vehicle="Snow Cat SV-M01", planned_departure=now + timedelta(days=27), planned_arrival=now + timedelta(days=28), status="PLANNED", distance_km=80),
        # S-209 legs (completed)
        ShipmentLeg(shipment_id=6, sequence=1, origin="New Delhi", destination="Oslo", mode="AIR", vehicle="Commercial Flight", planned_departure=now - timedelta(days=30), planned_arrival=now - timedelta(days=29), actual_departure=now - timedelta(days=30), actual_arrival=now - timedelta(days=29), status="ARRIVED", distance_km=5700),
        ShipmentLeg(shipment_id=6, sequence=2, origin="Oslo", destination="Longyearbyen", mode="AIR", vehicle="SAS Flight", planned_departure=now - timedelta(days=28), planned_arrival=now - timedelta(days=28), actual_departure=now - timedelta(days=28), actual_arrival=now - timedelta(days=28), status="ARRIVED", distance_km=2000),
        ShipmentLeg(shipment_id=6, sequence=3, origin="Longyearbyen", destination="Ny-Ålesund (Himadri)", mode="AIR", vehicle="Local Aircraft", planned_departure=now - timedelta(days=27), planned_arrival=now - timedelta(days=27), actual_departure=now - timedelta(days=27), actual_arrival=now - timedelta(days=27), status="ARRIVED", distance_km=120),
        # S-210 legs
        ShipmentLeg(shipment_id=7, sequence=1, origin="New Delhi", destination="Manali", mode="ROAD", vehicle="Transport Truck", planned_departure=now - timedelta(days=3), planned_arrival=now - timedelta(days=2), actual_departure=now - timedelta(days=3), actual_arrival=now - timedelta(days=2), status="ARRIVED", distance_km=550),
        ShipmentLeg(shipment_id=7, sequence=2, origin="Manali", destination="Himansh Station", mode="ROAD", vehicle="4x4 Vehicle", planned_departure=now - timedelta(days=1), planned_arrival=now + timedelta(days=1), actual_departure=now - timedelta(days=1), status="IN_TRANSIT", distance_km=120),
        # S-206 legs (field camp)
        ShipmentLeg(shipment_id=3, sequence=1, origin="Bharati Station", destination="Field Camp Alpha", mode="SNOW_VEHICLE", vehicle="PistenBully SV-B01", planned_departure=now + timedelta(days=12), planned_arrival=now + timedelta(days=13), status="PLANNED", distance_km=45),
    ]
    db.add_all(legs)
    db.flush()

    # === WEATHER OBSERVATIONS ===
    weather = [
        WeatherObservation(station_id=1, temperature=-28, wind_speed=45, visibility=5, precipitation="light_snow", humidity=65, pressure=980, severity="WATCH", forecast_summary="Moderate conditions with light snow. Wind increasing over next 12 hours.", timestamp=now - timedelta(hours=2)),
        WeatherObservation(station_id=2, temperature=-22, wind_speed=30, visibility=8, precipitation="none", humidity=55, pressure=990, severity="NORMAL", forecast_summary="Clear conditions. Good visibility. Suitable for operations.", timestamp=now - timedelta(hours=1)),
        WeatherObservation(station_id=3, temperature=-12, wind_speed=20, visibility=10, precipitation="none", humidity=70, pressure=1005, severity="NORMAL", forecast_summary="Clear Arctic conditions. Stable for research activities.", timestamp=now - timedelta(hours=3)),
        WeatherObservation(station_id=4, temperature=-8, wind_speed=35, visibility=4, precipitation="heavy_snow", humidity=80, pressure=970, severity="WARNING", forecast_summary="Heavy snowfall expected. Road access may be affected within 6 hours.", timestamp=now - timedelta(hours=1)),
        WeatherObservation(station_id=5, temperature=-25, wind_speed=50, visibility=2, precipitation="blizzard", humidity=75, pressure=975, severity="SEVERE", forecast_summary="Blizzard conditions developing. All field operations suspended.", timestamp=now - timedelta(minutes=30)),
        WeatherObservation(station_id=6, temperature=-30, wind_speed=55, visibility=1, precipitation="blizzard", humidity=70, pressure=972, severity="SEVERE", forecast_summary="Severe blizzard. No movement recommended.", timestamp=now - timedelta(minutes=45)),
    ]
    db.add_all(weather)
    db.flush()

    # === EVENTS ===
    events = [
        Event(event_type="SHIPMENT_DEPARTED", severity="INFO", entity_type="shipment", entity_id=1, title="Shipment S-204 departed Goa", description="Main expedition cargo departed Mormugao Port", timestamp=now - timedelta(days=10), processed=True),
        Event(event_type="SHIPMENT_ARRIVED", severity="INFO", entity_type="shipment", entity_id=1, title="S-204 arrived Cape Town", description="First leg completed. Refueling and resupply before Antarctic transit.", timestamp=now - timedelta(days=2), processed=True),
        Event(event_type="SHIPMENT_DEPARTED", severity="INFO", entity_type="shipment", entity_id=1, title="S-204 departed Cape Town", description="Shipment now en route to Antarctic gateway", timestamp=now - timedelta(days=1), processed=True),
        Event(event_type="WEATHER_DETERIORATION", severity="WARNING", entity_type="station", entity_id=5, title="Weather deterioration at Field Camp Alpha", description="Blizzard conditions developing at field camp", payload=json.dumps({"severity": "SEVERE", "wind_speed": 50}), timestamp=now - timedelta(minutes=30), processed=True),
        Event(event_type="ASSET_MAINTENANCE_DUE", severity="WARNING", entity_type="asset", entity_id=1, title="Generator GEN-M01 approaching maintenance threshold", description="Engine hours at 4820/5000. Schedule maintenance within 2 weeks.", timestamp=now - timedelta(hours=6), processed=True),
        Event(event_type="ASSET_MAINTENANCE_DUE", severity="HIGH", entity_type="asset", entity_id=8, title="PistenBully SV-B02 requires maintenance", description="Track system showing wear. Maintenance required before next deployment.", timestamp=now - timedelta(hours=12), processed=True),
        Event(event_type="PERSONNEL_DELAYED", severity="WARNING", entity_type="personnel", entity_id=32, title="Dr. Mohan Das travel delayed", description="Connecting flight cancelled. New arrival estimate: 20 Dec 2026.", timestamp=now - timedelta(hours=8), processed=True),
        Event(event_type="STOCK_LOW", severity="WARNING", entity_type="inventory", entity_id=None, title="Low stock: First Aid Kits at Bharati", description="First aid kit inventory approaching minimum threshold", payload=json.dumps({"item_name": "First Aid Kits", "station_name": "Bharati"}), timestamp=now - timedelta(hours=4), processed=True),
        Event(event_type="EXPEDITION_READINESS_CHANGED", severity="INFO", entity_type="expedition", entity_id=1, title="EXP-2026-014 readiness updated", description="Readiness score: 88%. Cargo fulfillment at 90%.", timestamp=now - timedelta(hours=2), processed=True),
    ]
    db.add_all(events)
    db.flush()

    # === MISSIONS ===
    missions = [
        Mission(id=1, name="Whiteout Resupply", code="MSN-001", description="Field Camp Alpha is running critically low on fuel during a severe blizzard. Deliver critical supplies before stock reaches zero.", difficulty="HARD", category="RESUPPLY", time_limit=300, station_id=5,
            objectives=json.dumps(["Deliver fuel to Field Camp Alpha", "Maintain safety above 70%", "Complete within 48 hours"]),
            constraints=json.dumps(["Severe weather conditions", "Limited aircraft availability", "Reduced visibility"]),
            initial_state=json.dumps({"fuel": 2800, "inventory": {"medical": 50, "food": 200, "equipment": 30}, "aircraft_available": True, "vehicles_available": 2, "weather_severity": "SEVERE", "time_remaining": 48, "cargo_delivered": 0, "cargo_target": 100, "risk": 40, "safety": 100, "efficiency": 100, "cost": 0, "decisions_made": 0, "events_encountered": 0}),
            events_script=json.dumps([{"turn": 1, "type": "AIRCRAFT_DELAY"}, {"turn": 3, "type": "FUEL_LEAK"}]),
        ),
        Mission(id=2, name="Emergency Evacuation", code="MSN-002", description="A team member at Field Camp Bravo requires emergency medical evacuation. Coordinate rescue while managing deteriorating weather.", difficulty="EXTREME", category="RESCUE", time_limit=180, station_id=6,
            objectives=json.dumps(["Evacuate injured personnel", "Maintain medical supplies", "Keep all other personnel safe"]),
            constraints=json.dumps(["Deteriorating weather", "Limited helicopter fuel", "Night operations"]),
            initial_state=json.dumps({"fuel": 3500, "inventory": {"medical": 30, "food": 100, "equipment": 20}, "aircraft_available": True, "vehicles_available": 1, "weather_severity": "WARNING", "time_remaining": 24, "cargo_delivered": 0, "cargo_target": 50, "risk": 55, "safety": 100, "efficiency": 100, "cost": 0, "decisions_made": 0, "events_encountered": 0}),
        ),
        Mission(id=3, name="Supply Chain Challenge", code="MSN-003", description="Plan and execute a multi-leg supply route from Goa to Bharati. Optimise for cost, time, and safety.", difficulty="MEDIUM", category="LOGISTICS", time_limit=600, station_id=2,
            objectives=json.dumps(["Deliver all cargo to Bharati", "Stay within fuel budget", "Minimise total transit time"]),
            constraints=json.dumps(["Budget limit", "Aircraft capacity", "Weather windows"]),
            initial_state=json.dumps({"fuel": 5000, "inventory": {"medical": 100, "food": 500, "equipment": 80}, "aircraft_available": True, "vehicles_available": 3, "weather_severity": "WATCH", "time_remaining": 72, "cargo_delivered": 0, "cargo_target": 200, "risk": 25, "safety": 100, "efficiency": 100, "cost": 0, "decisions_made": 0, "events_encountered": 0}),
        ),
        Mission(id=4, name="Generator Crisis", code="MSN-004", description="Primary generator at Maitri has failed. Manage backup power while arranging repair or replacement.", difficulty="HARD", category="MAINTENANCE", time_limit=240, station_id=1,
            objectives=json.dumps(["Restore primary power within 36 hours", "Maintain critical systems on backup", "Prevent fuel waste"]),
            constraints=json.dumps(["Backup generator at 30% capacity", "Spare parts may not be available", "Freezing conditions affect repair time"]),
            initial_state=json.dumps({"fuel": 4000, "inventory": {"medical": 40, "food": 150, "equipment": 60, "spare_parts": 3}, "aircraft_available": False, "vehicles_available": 2, "weather_severity": "WATCH", "time_remaining": 36, "cargo_delivered": 0, "cargo_target": 80, "risk": 60, "safety": 85, "efficiency": 100, "cost": 0, "decisions_made": 0, "events_encountered": 0}),
        ),
        Mission(id=5, name="Scientific Survey", code="MSN-005", description="Deploy a team to conduct ice core sampling at 3 locations near Bharati. Manage logistics while collecting scientific data.", difficulty="EASY", category="SCIENTIFIC", time_limit=600, station_id=2,
            objectives=json.dumps(["Complete sampling at 3 locations", "Return all samples safely", "Document findings"]),
            constraints=json.dumps(["Limited fuel for field vehicles", "Sample containers have limited capacity", "Weather windows vary by location"]),
            initial_state=json.dumps({"fuel": 6000, "inventory": {"medical": 60, "food": 300, "equipment": 100, "sample_containers": 50}, "aircraft_available": True, "vehicles_available": 2, "weather_severity": "NORMAL", "time_remaining": 96, "cargo_delivered": 0, "cargo_target": 150, "risk": 15, "safety": 100, "efficiency": 100, "cost": 0, "decisions_made": 0, "events_encountered": 0}),
        ),
    ]
    db.add_all(missions)
    db.flush()

    # === BADGES ===
    badges = [
        Badge(code="ZERO_STOCKOUT", name="Zero Stockout", description="Complete a mission without any critical shortage", icon="🏆", category="LOGISTICS"),
        Badge(code="ASSET_GUARDIAN", name="Asset Guardian", description="Protect all critical equipment through a mission", icon="🛡️", category="ASSETS"),
        Badge(code="WEATHER_COMMANDER", name="Weather Commander", description="Successfully handle multiple weather disruptions", icon="🌨️", category="WEATHER"),
        Badge(code="LOGISTICS_MASTER", name="Logistics Master", description="Score over 1200 points in a single mission", icon="⭐", category="LOGISTICS"),
        Badge(code="FUEL_SAVER", name="Fuel Saver", description="Complete mission with over 50% fuel remaining", icon="⛽", category="EFFICIENCY"),
        Badge(code="EMERGENCY_COMMANDER", name="Emergency Commander", description="Handle 3+ events and still score over 800", icon="🚨", category="EMERGENCY"),
        Badge(code="RISK_ANALYST", name="Risk Analyst", description="Complete 3 missions without safety dropping below 60%", icon="📊", category="ANALYSIS"),
        Badge(code="POLAR_VETERAN", name="Polar Veteran", description="Complete all 5 missions", icon="🎖️", category="ACHIEVEMENT"),
    ]
    db.add_all(badges)

    # === RECOMMENDATIONS (initial) ===
    recs = [
        Recommendation(expedition_id=1, title="Advance Field Camp Alpha resupply", description="Fuel at Field Camp Alpha projected to reach critical level before next scheduled delivery.", action="Schedule emergency fuel resupply via snow vehicle from Bharati. Target: 3 days earlier than planned.", priority="HIGH", status="PENDING"),
        Recommendation(expedition_id=1, title="Generator GEN-M01 approaching threshold", description="Primary generator at Maitri nearing 5000-hour maintenance threshold.", action="Schedule maintenance during the next personnel rotation window. Prepare backup generator for primary duty.", priority="MEDIUM", status="PENDING"),
    ]
    db.add_all(recs)

    db.commit()
    print("✅ Seed data loaded successfully!")
    print(f"   Stations: {db.query(Station).count()}")
    print(f"   Users: {db.query(User).count()}")
    print(f"   Personnel: {db.query(Personnel).count()}")
    print(f"   Items: {db.query(Item).count()}")
    print(f"   Inventory records: {db.query(Inventory).count()}")
    print(f"   Assets: {db.query(Asset).count()}")
    print(f"   Expeditions: {db.query(Expedition).count()}")
    print(f"   Shipments: {db.query(Shipment).count()}")
    print(f"   Shipment legs: {db.query(ShipmentLeg).count()}")
    print(f"   Events: {db.query(Event).count()}")
    print(f"   Missions: {db.query(Mission).count()}")
    print(f"   Badges: {db.query(Badge).count()}")
