from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.app.db.session import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    sector = Column(String(100), nullable=False)
    registration_number = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    financial_statements = relationship("FinancialStatement", back_populates="company", cascade="all, delete-orphan")
    financial_ratios = relationship("FinancialRatio", back_populates="company", cascade="all, delete-orphan")
    interaction_logs = relationship("InteractionLog", back_populates="company", cascade="all, delete-orphan")
    risk_scores = relationship("RiskScore", back_populates="company", cascade="all, delete-orphan")
    users = relationship("User", back_populates="company")


class FinancialStatement(Base):
    __tablename__ = "financial_statements"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    statement_type = Column(String(50), nullable=False)  # 'balance_sheet', 'income_statement', 'cash_flow', 'combined'
    fiscal_year = Column(Integer, nullable=False)
    raw_file_path = Column(Text, nullable=True)
    parsed_json = Column(JSON, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="financial_statements")


class FinancialRatio(Base):
    __tablename__ = "financial_ratios"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    current_ratio = Column(Float, nullable=True)
    quick_ratio = Column(Float, nullable=True)
    cash_ratio = Column(Float, nullable=True)
    working_capital = Column(Float, nullable=True)
    debt_to_equity = Column(Float, nullable=True)
    debt_to_assets = Column(Float, nullable=True)
    interest_coverage_ratio = Column(Float, nullable=True)
    inventory_turnover = Column(Float, nullable=True)
    receivables_turnover = Column(Float, nullable=True)
    dso_days = Column(Float, nullable=True)
    asset_turnover = Column(Float, nullable=True)
    gross_margin = Column(Float, nullable=True)
    operating_margin = Column(Float, nullable=True)
    net_margin = Column(Float, nullable=True)
    roe = Column(Float, nullable=True)
    roa = Column(Float, nullable=True)
    price_to_book = Column(Float, nullable=True)
    computed_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="financial_ratios")


class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    interaction_type = Column(String(50), nullable=False)  # 'negotiation', 'service_failure', 'service_recovery'
    transcript_text = Column(Text, nullable=False)
    sentiment_score = Column(Float, nullable=True)  # Range: -1.0 (very negative) to +1.0 (very positive)
    risk_flag_score = Column(Float, nullable=True)  # Range: 0.0 (no risk) to 1.0 (critical risk)
    interaction_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="interaction_logs")


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    financial_score = Column(Float, nullable=False)       # 0 - 100
    relationship_score = Column(Float, nullable=False)    # 0 - 100
    macro_adjustment = Column(Float, nullable=False)      # multiplier / adjustment factor
    composite_score = Column(Float, nullable=False)       # 0 - 100
    risk_band = Column(String(20), nullable=False)        # 'low', 'medium', 'high'
    shap_explanation = Column(JSON, nullable=True)        # Feature impact breakdown
    generated_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="risk_scores")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)  # 'lender' or 'msme_owner'
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="users")
