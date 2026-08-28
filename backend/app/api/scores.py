from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import Company, FinancialStatement, InteractionLog, RiskScore
from backend.app.models.schemas import RiskScoreOut, HealthReportOut
from backend.app.services.composite_scorer import composite_scorer

router = APIRouter(prefix="/scores", tags=["Risk Scoring & Health Reports"])

@router.get("/{company_id}")
def get_company_credit_score(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Fetch latest financial statement
    latest_stmt = db.query(FinancialStatement).filter(
        FinancialStatement.company_id == company_id
    ).order_by(FinancialStatement.fiscal_year.desc()).first()

    if not latest_stmt or not latest_stmt.parsed_json:
        raise HTTPException(status_code=400, detail="No parsed financial statements available for scoring.")

    # Fetch interactions
    logs = db.query(InteractionLog).filter(
        InteractionLog.company_id == company_id
    ).all()
    history = [
        {"transcript_text": l.transcript_text, "interaction_type": l.interaction_type}
        for l in logs
    ]

    # Compute composite risk
    score_result = composite_scorer.compute_composite_risk(
        line_items=latest_stmt.parsed_json,
        sector=company.sector,
        interaction_history=history
    )

    # Save or update in database
    existing_score = db.query(RiskScore).filter(
        RiskScore.company_id == company_id,
        RiskScore.fiscal_year == latest_stmt.fiscal_year
    ).first()

    if existing_score:
        existing_score.financial_score = score_result["financial_score"]
        existing_score.relationship_score = score_result["relationship_score"]
        existing_score.macro_adjustment = score_result["macro_adjustment"]
        existing_score.composite_score = score_result["composite_score"]
        existing_score.risk_band = score_result["risk_band"]
        existing_score.shap_explanation = score_result["shap_explanation"]
    else:
        score_entry = RiskScore(
            company_id=company_id,
            fiscal_year=latest_stmt.fiscal_year,
            financial_score=score_result["financial_score"],
            relationship_score=score_result["relationship_score"],
            macro_adjustment=score_result["macro_adjustment"],
            composite_score=score_result["composite_score"],
            risk_band=score_result["risk_band"],
            shap_explanation=score_result["shap_explanation"]
        )
        db.add(score_entry)
    db.commit()

    return {
        "company_id": company_id,
        "company_name": company.name,
        "sector": company.sector,
        "fiscal_year": latest_stmt.fiscal_year,
        **score_result
    }

@router.get("/{company_id}/health-report")
def get_msme_health_report(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    latest_stmt = db.query(FinancialStatement).filter(
        FinancialStatement.company_id == company_id
    ).order_by(FinancialStatement.fiscal_year.desc()).first()

    if not latest_stmt or not latest_stmt.parsed_json:
        raise HTTPException(status_code=400, detail="No parsed financial statement available.")

    logs = db.query(InteractionLog).filter(InteractionLog.company_id == company_id).all()
    history = [{"transcript_text": l.transcript_text, "interaction_type": l.interaction_type} for l in logs]

    score_result = composite_scorer.compute_composite_risk(
        line_items=latest_stmt.parsed_json,
        sector=company.sector,
        interaction_history=history
    )

    return {
        "company_id": company_id,
        "company_name": company.name,
        "sector": company.sector,
        "credit_readiness_score": score_result["composite_score"],
        "risk_band": score_result["risk_band"],
        "risk_band_label": score_result["risk_band_label"],
        "key_strengths": score_result["key_strengths"],
        "critical_vulnerabilities": score_result["critical_vulnerabilities"],
        "actionable_recommendations": score_result["actionable_recommendations"],
        "ratio_benchmarks": score_result["benchmarks"],
        "cost_structure": score_result["cost_structure"],
        "relationship_summary": score_result["relationship_summary"]
    }

@router.get("/portfolio/overview")
def get_portfolio_overview(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    total_companies = len(companies)

    low_risk = 0
    med_risk = 0
    high_risk = 0
    scores_list = []

    for comp in companies:
        latest_score = db.query(RiskScore).filter(
            RiskScore.company_id == comp.id
        ).order_by(RiskScore.fiscal_year.desc()).first()

        if latest_score:
            scores_list.append(latest_score.composite_score)
            if latest_score.risk_band == "low":
                low_risk += 1
            elif latest_score.risk_band == "medium":
                med_risk += 1
            else:
                high_risk += 1

    avg_score = round(sum(scores_list) / len(scores_list), 1) if scores_list else 72.0

    return {
        "total_assessed_companies": total_companies,
        "average_portfolio_score": avg_score,
        "risk_distribution": {
            "low_risk_count": low_risk,
            "medium_risk_count": med_risk,
            "high_risk_count": high_risk
        },
        "approval_rate_estimate": round((low_risk + (med_risk * 0.5)) / max(total_companies, 1) * 100, 1)
    }
