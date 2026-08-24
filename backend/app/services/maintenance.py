"""Maintenance prediction — rules-based scoring for MVP.

Honestly labelled as rules/statistical, not "AI/ML prediction".
"""
from datetime import date
from sqlalchemy.orm import Session
from app.models.asset import Asset, MaintenanceTask


def predict_maintenance_risk(db: Session, asset_id: int) -> dict:
    """Calculate maintenance risk using transparent rules."""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        return {}

    factors = []
    risk_score = 0

    # Factor 1: Engine hours vs threshold
    if asset.maintenance_threshold_hours > 0:
        hours_ratio = asset.engine_hours / asset.maintenance_threshold_hours
        if hours_ratio >= 0.95:
            factor_score = 35
            explanation = f"Engine hours ({asset.engine_hours:.0f}) at {hours_ratio*100:.0f}% of maintenance threshold ({asset.maintenance_threshold_hours:.0f})"
        elif hours_ratio >= 0.80:
            factor_score = 20
            explanation = f"Engine hours ({asset.engine_hours:.0f}) at {hours_ratio*100:.0f}% of threshold"
        else:
            factor_score = 5
            explanation = f"Engine hours ({asset.engine_hours:.0f}) within normal range"
        factors.append({"name": "Engine Hours", "score": factor_score, "explanation": explanation})
        risk_score += factor_score

    # Factor 2: Utilisation percentage
    if asset.utilisation_pct >= 90:
        factor_score = 25
        explanation = f"High utilisation ({asset.utilisation_pct:.0f}%) — accelerated wear expected"
    elif asset.utilisation_pct >= 70:
        factor_score = 15
        explanation = f"Moderate utilisation ({asset.utilisation_pct:.0f}%)"
    else:
        factor_score = 5
        explanation = f"Low utilisation ({asset.utilisation_pct:.0f}%)"
    factors.append({"name": "Utilisation", "score": factor_score, "explanation": explanation})
    risk_score += factor_score

    # Factor 3: Recent fault events
    recent_faults = db.query(MaintenanceTask).filter(
        MaintenanceTask.asset_id == asset_id,
        MaintenanceTask.type.in_(["REPAIR", "EMERGENCY"]),
    ).count()
    if recent_faults >= 3:
        factor_score = 25
        explanation = f"{recent_faults} recent fault/repair events — pattern suggests underlying issue"
    elif recent_faults >= 1:
        factor_score = 10
        explanation = f"{recent_faults} recent fault event(s)"
    else:
        factor_score = 0
        explanation = "No recent fault events"
    factors.append({"name": "Recent Faults", "score": factor_score, "explanation": explanation})
    risk_score += factor_score

    # Factor 4: Days since last maintenance
    if asset.last_maintenance:
        days_since = (date.today() - asset.last_maintenance).days
        if days_since > 180:
            factor_score = 15
            explanation = f"{days_since} days since last maintenance — overdue"
        elif days_since > 90:
            factor_score = 8
            explanation = f"{days_since} days since last maintenance"
        else:
            factor_score = 2
            explanation = f"Maintained {days_since} days ago — recent"
    else:
        factor_score = 10
        explanation = "No maintenance history recorded"
    factors.append({"name": "Maintenance Recency", "score": factor_score, "explanation": explanation})
    risk_score += factor_score

    risk_score = min(100, risk_score)

    if risk_score >= 70:
        risk_level = "HIGH"
        recommendation = f"Schedule immediate maintenance for {asset.name}. High risk of failure."
    elif risk_score >= 40:
        risk_level = "MEDIUM"
        recommendation = f"Plan maintenance for {asset.name} within the next 2 weeks."
    else:
        risk_level = "LOW"
        recommendation = f"{asset.name} is in acceptable condition. Continue regular monitoring."

    return {
        "asset_id": asset.id,
        "asset_name": asset.name,
        "category": asset.category,
        "engine_hours": asset.engine_hours,
        "threshold": asset.maintenance_threshold_hours,
        "utilisation_pct": asset.utilisation_pct,
        "recent_faults": recent_faults,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "factors": factors,
        "recommendation": recommendation,
    }
