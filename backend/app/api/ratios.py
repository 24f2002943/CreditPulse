from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import Company, FinancialRatio, FinancialStatement
from backend.app.models.schemas import FinancialRatioOut, RatioBenchmarkOut
from backend.app.services.ratio_engine import ratio_engine

router = APIRouter(prefix="/ratios", tags=["Financial Ratios"])

@router.get("/{company_id}", response_model=List[FinancialRatioOut])
def get_company_ratios(company_id: int, db: Session = Depends(get_db)):
    ratios = db.query(FinancialRatio).filter(FinancialRatio.company_id == company_id).order_by(FinancialRatio.fiscal_year.desc()).all()
    return ratios

@router.get("/{company_id}/benchmarks")
def get_company_ratio_benchmarks(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    latest_ratio = db.query(FinancialRatio).filter(
        FinancialRatio.company_id == company_id
    ).order_by(FinancialRatio.fiscal_year.desc()).first()

    if not latest_ratio:
        # Check if there is a statement
        latest_stmt = db.query(FinancialStatement).filter(
            FinancialStatement.company_id == company_id
        ).order_by(FinancialStatement.fiscal_year.desc()).first()
        if latest_stmt and latest_stmt.parsed_json:
            calc = ratio_engine.compute_ratios(latest_stmt.parsed_json, company.sector)
            return {"benchmarks": calc["benchmarks"], "ratios": calc["ratios"]}
        raise HTTPException(status_code=404, detail="No financial statements or ratios found for this company.")

    # Convert model to dict
    ratio_dict = {c.name: getattr(latest_ratio, c.name) for c in latest_ratio.__table__.columns}
    benchmarks = ratio_engine.compute_sector_benchmarks(ratio_dict, company.sector)

    return {
        "company_id": company_id,
        "company_name": company.name,
        "sector": company.sector,
        "fiscal_year": latest_ratio.fiscal_year,
        "benchmarks": benchmarks,
        "ratios": ratio_dict
    }
