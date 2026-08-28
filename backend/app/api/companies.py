from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import Company
from backend.app.models.schemas import CompanyCreate, CompanyOut

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.get("/", response_model=List[CompanyOut])
def get_companies(
    sector: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Company)
    if sector:
        query = query.filter(Company.sector == sector)
    if search:
        query = query.filter(Company.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

@router.get("/{company_id}", response_model=CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.post("/", response_model=CompanyOut, status_code=201)
def create_company(company_in: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(
        name=company_in.name,
        sector=company_in.sector,
        registration_number=company_in.registration_number
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
