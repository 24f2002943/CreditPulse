from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import Company, InteractionLog
from backend.app.models.schemas import InteractionLogCreate, InteractionLogOut
from backend.app.ml.nlp_engine import nlp_engine

router = APIRouter(prefix="/interactions", tags=["Interaction Logs & NLP"])

@router.get("/company/{company_id}", response_model=List[InteractionLogOut])
def get_interactions_for_company(company_id: int, db: Session = Depends(get_db)):
    return db.query(InteractionLog).filter(
        InteractionLog.company_id == company_id
    ).order_by(InteractionLog.created_at.desc()).all()

@router.post("/", response_model=InteractionLogOut, status_code=201)
def create_interaction_log(log_in: InteractionLogCreate, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == log_in.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Run NLP Analysis on transcript text
    nlp_res = nlp_engine.analyze_transcript(log_in.transcript_text, log_in.interaction_type)

    log_entry = InteractionLog(
        company_id=log_in.company_id,
        interaction_type=log_in.interaction_type,
        transcript_text=log_in.transcript_text,
        sentiment_score=nlp_res["sentiment_score"],
        risk_flag_score=nlp_res["risk_flag_score"],
        interaction_date=log_in.interaction_date
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

@router.get("/company/{company_id}/relationship-analysis")
def get_relationship_analysis(company_id: int, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    logs = db.query(InteractionLog).filter(
        InteractionLog.company_id == company_id
    ).order_by(InteractionLog.created_at.asc()).all()

    history = [
        {
            "transcript_text": log.transcript_text,
            "interaction_type": log.interaction_type,
            "sentiment_score": log.sentiment_score,
            "risk_flag_score": log.risk_flag_score,
            "date": str(log.interaction_date or log.created_at)
        }
        for log in logs
    ]

    analysis = nlp_engine.compute_relationship_score(history)
    return {
        "company_id": company_id,
        "company_name": company.name,
        "analysis": analysis,
        "history_count": len(history),
        "history": history
    }
