import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import Company, FinancialStatement, FinancialRatio
from backend.app.models.schemas import FinancialStatementOut
from backend.app.services.excel_parser import excel_parser
from backend.app.services.ocr_pipeline import ocr_pipeline
from backend.app.services.accounting_validator import accounting_validator
from backend.app.services.ratio_engine import ratio_engine
from backend.app.core.config import settings

router = APIRouter(prefix="/statements", tags=["Financial Statements"])

@router.post("/upload")
async def upload_statement(
    company_id: int = Form(...),
    statement_type: str = Form("combined"),
    fiscal_year: Optional[int] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_ext = os.path.splitext(file.filename)[1].lower()
    saved_filename = f"comp_{company_id}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        if file_ext in [".xlsx", ".xls", ".csv"]:
            parse_res = excel_parser.parse_file(file_path)
            line_items = parse_res["line_items"]
            fy = fiscal_year or parse_res.get("fiscal_year", 2024)
            validation_res = accounting_validator.validate(line_items)
        elif file_ext in [".pdf"]:
            parse_res = ocr_pipeline.parse_pdf(file_path)
            line_items = parse_res["line_items"]
            fy = fiscal_year or parse_res.get("fiscal_year", 2024)
            validation_res = parse_res["validation"]
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_ext}")

        # Store financial statement
        statement = FinancialStatement(
            company_id=company_id,
            statement_type=statement_type,
            fiscal_year=fy,
            raw_file_path=file_path,
            parsed_json=line_items
        )
        db.add(statement)
        db.commit()
        db.refresh(statement)

        # Automatically compute and store/update ratios
        ratios_calc = ratio_engine.compute_ratios(line_items, company.sector)
        r = ratios_calc["ratios"]

        existing_ratio = db.query(FinancialRatio).filter(
            FinancialRatio.company_id == company_id,
            FinancialRatio.fiscal_year == fy
        ).first()

        if existing_ratio:
            for k, v in r.items():
                if hasattr(existing_ratio, k):
                    setattr(existing_ratio, k, v)
        else:
            ratio_obj = FinancialRatio(
                company_id=company_id,
                fiscal_year=fy,
                **r
            )
            db.add(ratio_obj)
        db.commit()

        return {
            "message": "Financial statement processed successfully.",
            "statement_id": statement.id,
            "company_id": company_id,
            "fiscal_year": fy,
            "line_items_count": len(line_items),
            "line_items": line_items,
            "validation": validation_res,
            "ratios": r
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process statement: {str(e)}")

@router.get("/company/{company_id}", response_model=List[FinancialStatementOut])
def get_company_statements(company_id: int, db: Session = Depends(get_db)):
    return db.query(FinancialStatement).filter(FinancialStatement.company_id == company_id).all()
