from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime

# --- Company Schemas ---
class CompanyBase(BaseModel):
    name: str = Field(..., example="Apex Precision Engineering Ltd")
    sector: str = Field(..., example="Light Manufacturing & Engineering")
    registration_number: Optional[str] = Field(None, example="U28910MH2018PTC304891")

class CompanyCreate(CompanyBase):
    pass

class CompanyOut(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Financial Statement Schemas ---
class FinancialStatementBase(BaseModel):
    statement_type: str = Field(..., example="balance_sheet")
    fiscal_year: int = Field(..., example=2024)

class FinancialStatementCreate(FinancialStatementBase):
    company_id: int
    parsed_json: Optional[Dict[str, Any]] = None

class FinancialStatementOut(FinancialStatementBase):
    id: int
    company_id: int
    raw_file_path: Optional[str] = None
    parsed_json: Optional[Dict[str, Any]] = None
    uploaded_at: datetime

    class Config:
        from_attributes = True

# --- Financial Ratios Schemas ---
class FinancialRatioOut(BaseModel):
    id: int
    company_id: int
    fiscal_year: int
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None
    interest_coverage_ratio: Optional[float] = None
    inventory_turnover: Optional[float] = None
    receivables_turnover: Optional[float] = None
    gross_margin: Optional[float] = None
    net_margin: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    price_to_book: Optional[float] = None
    computed_at: datetime

    class Config:
        from_attributes = True

class RatioBenchmarkOut(BaseModel):
    ratio_name: str
    company_value: Optional[float]
    sector_median: float
    status: str  # 'healthy', 'warning', 'critical'
    percentile: float

# --- Interaction Logs Schemas ---
class InteractionLogBase(BaseModel):
    interaction_type: str = Field(..., example="negotiation")  # 'negotiation', 'service_failure', 'service_recovery'
    transcript_text: str = Field(..., example="Customer expressed concern over delivery delays and requested a 15% price discount.")
    interaction_date: Optional[date] = None

class InteractionLogCreate(InteractionLogBase):
    company_id: int

class InteractionLogOut(InteractionLogBase):
    id: int
    company_id: int
    sentiment_score: Optional[float] = None
    risk_flag_score: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

# --- Risk Score & SHAP Schemas ---
class ShapFeatureImpact(BaseModel):
    feature: str
    feature_name_display: str
    value: float
    shap_value: float
    impact_direction: str  # 'increases_risk', 'decreases_risk'

class RiskScoreOut(BaseModel):
    id: int
    company_id: int
    fiscal_year: int
    financial_score: float
    relationship_score: float
    macro_adjustment: float
    composite_score: float
    risk_band: str  # 'low', 'medium', 'high'
    shap_explanation: Optional[List[Dict[str, Any]]] = None
    generated_at: datetime

    class Config:
        from_attributes = True

class HealthReportOut(BaseModel):
    company: CompanyOut
    credit_readiness_score: float
    risk_band: str
    key_strengths: List[str]
    critical_vulnerabilities: List[str]
    actionable_recommendations: List[str]
    ratio_benchmarks: List[RatioBenchmarkOut]
    relationship_health_summary: Dict[str, Any]

# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field("lender", example="lender")  # 'lender' or 'msme_owner'
    company_id: Optional[int] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    email: str
    company_id: Optional[int] = None

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    company_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

