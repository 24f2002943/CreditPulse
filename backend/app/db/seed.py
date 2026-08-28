import json
import os
from datetime import datetime, date
from backend.app.db.session import SessionLocal, Base, engine
from backend.app.models.entities import Company, FinancialStatement, FinancialRatio, InteractionLog, RiskScore, User
from backend.app.core.security import get_password_hash
from backend.app.services.ratio_engine import ratio_engine
from backend.app.services.composite_scorer import composite_scorer

SEED_COMPANIES = [
    {
        "name": "Apex Precision Engineering Ltd",
        "sector": "Light Manufacturing & Engineering",
        "registration_number": "U28910MH2018PTC304891",
        "financials": {
            "revenue": 4500000.0,
            "cost_of_goods_sold": 3150000.0,
            "gross_profit": 1350000.0,
            "operating_expenses": 650000.0,
            "ebit": 700000.0,
            "interest_expense": 85000.0,
            "tax_expense": 153750.0,
            "net_income": 461250.0,
            "total_assets": 3200000.0,
            "total_current_assets": 2100000.0,
            "cash_and_equivalents": 380000.0,
            "accounts_receivable": 820000.0,
            "inventory": 900000.0,
            "property_plant_equipment": 1100000.0,
            "total_liabilities": 1350000.0,
            "total_current_liabilities": 950000.0,
            "accounts_payable": 520000.0,
            "short_term_debt": 430000.0,
            "long_term_debt": 400000.0,
            "total_equity": 1850000.0
        }
    },
    {
        "name": "Zenith Logistics & Transport",
        "sector": "Logistics & Freight Services",
        "registration_number": "U60200DL2019PTC345129",
        "financials": {
            "revenue": 2800000.0,
            "cost_of_goods_sold": 2240000.0,
            "gross_profit": 560000.0,
            "operating_expenses": 420000.0,
            "ebit": 140000.0,
            "interest_expense": 95000.0,
            "tax_expense": 11250.0,
            "net_income": 33750.0,
            "total_assets": 2100000.0,
            "total_current_assets": 850000.0,
            "cash_and_equivalents": 60000.0,
            "accounts_receivable": 580000.0,
            "inventory": 210000.0,
            "property_plant_equipment": 1250000.0,
            "total_liabilities": 1550000.0,
            "total_current_liabilities": 920000.0,
            "accounts_payable": 480000.0,
            "short_term_debt": 440000.0,
            "long_term_debt": 630000.0,
            "total_equity": 550000.0
        }
    },
    {
        "name": "Nova BioTech Pharmaceuticals",
        "sector": "Pharmaceuticals & Healthcare",
        "registration_number": "U24230GJ2016PTC091234",
        "financials": {
            "revenue": 6200000.0,
            "cost_of_goods_sold": 3720000.0,
            "gross_profit": 2480000.0,
            "operating_expenses": 1200000.0,
            "ebit": 1280000.0,
            "interest_expense": 60000.0,
            "tax_expense": 305000.0,
            "net_income": 915000.0,
            "total_assets": 4800000.0,
            "total_current_assets": 3200000.0,
            "cash_and_equivalents": 850000.0,
            "accounts_receivable": 1150000.0,
            "inventory": 1200000.0,
            "property_plant_equipment": 1600000.0,
            "total_liabilities": 1400000.0,
            "total_current_liabilities": 900000.0,
            "accounts_payable": 600000.0,
            "short_term_debt": 300000.0,
            "long_term_debt": 500000.0,
            "total_equity": 3400000.0
        }
    },
    {
        "name": "Skyline Infra & Construction",
        "sector": "Construction & Subcontracting",
        "registration_number": "U45200KA2017PTC102938",
        "financials": {
            "revenue": 5100000.0,
            "cost_of_goods_sold": 4200000.0,
            "gross_profit": 900000.0,
            "operating_expenses": 650000.0,
            "ebit": 250000.0,
            "interest_expense": 180000.0,
            "tax_expense": 17500.0,
            "net_income": 52500.0,
            "total_assets": 4100000.0,
            "total_current_assets": 2600000.0,
            "cash_and_equivalents": 120000.0,
            "accounts_receivable": 1850000.0,
            "inventory": 630000.0,
            "property_plant_equipment": 1500000.0,
            "total_liabilities": 3100000.0,
            "total_current_liabilities": 2150000.0,
            "accounts_payable": 1250000.0,
            "short_term_debt": 900000.0,
            "long_term_debt": 950000.0,
            "total_equity": 1000000.0
        }
    },
    {
        "name": "Kaveri Organic Foods & Spices",
        "sector": "Food Processing & FMCG",
        "registration_number": "U15400TN2020PTC134812",
        "financials": {
            "revenue": 3400000.0,
            "cost_of_goods_sold": 2650000.0,
            "gross_profit": 750000.0,
            "operating_expenses": 410000.0,
            "ebit": 340000.0,
            "interest_expense": 45000.0,
            "tax_expense": 73750.0,
            "net_income": 221250.0,
            "total_assets": 2400000.0,
            "total_current_assets": 1650000.0,
            "cash_and_equivalents": 290000.0,
            "accounts_receivable": 480000.0,
            "inventory": 880000.0,
            "property_plant_equipment": 750000.0,
            "total_liabilities": 980000.0,
            "total_current_liabilities": 680000.0,
            "accounts_payable": 450000.0,
            "short_term_debt": 230000.0,
            "long_term_debt": 300000.0,
            "total_equity": 1420000.0
        }
    }
]

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(Company).count() > 0:
            print("Database already contains data. Skipping initial seeding.")
            return

        print("Seeding demo companies, financials, and users...")

        # 1. Create Default Users
        lender_user = User(
            email="analyst@creditpulse.bank",
            password_hash=get_password_hash("Lender@123"),
            role="lender"
        )
        db.add(lender_user)

        msme_user = User(
            email="owner@apexprecision.com",
            password_hash=get_password_hash("Owner@123"),
            role="msme_owner",
            company_id=1
        )
        db.add(msme_user)
        db.commit()

        # 2. Seed Companies & Financials
        for c_data in SEED_COMPANIES:
            comp = Company(
                name=c_data["name"],
                sector=c_data["sector"],
                registration_number=c_data["registration_number"]
            )
            db.add(comp)
            db.commit()
            db.refresh(comp)

            # Statement
            stmt = FinancialStatement(
                company_id=comp.id,
                statement_type="combined",
                fiscal_year=2024,
                parsed_json=c_data["financials"]
            )
            db.add(stmt)
            db.commit()

            # Ratios
            r_calc = ratio_engine.compute_ratios(c_data["financials"], comp.sector)["ratios"]
            ratio_obj = FinancialRatio(
                company_id=comp.id,
                fiscal_year=2024,
                **r_calc
            )
            db.add(ratio_obj)
            db.commit()

        # 3. Seed Interaction Logs
        interactions_path = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_interactions.json")
        if os.path.exists(interactions_path):
            with open(interactions_path, "r") as f:
                logs_data = json.load(f)

            for item in logs_data:
                comp = db.query(Company).filter(Company.name == item["company_name"]).first()
                if comp:
                    log_entry = InteractionLog(
                        company_id=comp.id,
                        interaction_type=item["interaction_type"],
                        transcript_text=item["transcript_text"],
                        sentiment_score=item.get("sentiment_score"),
                        risk_flag_score=item.get("risk_flag_score"),
                        interaction_date=date.fromisoformat(item["interaction_date"]) if item.get("interaction_date") else None
                    )
                    db.add(log_entry)
            db.commit()

        # 4. Compute Initial Risk Scores for all companies
        for comp in db.query(Company).all():
            stmt = db.query(FinancialStatement).filter(FinancialStatement.company_id == comp.id).first()
            logs = db.query(InteractionLog).filter(InteractionLog.company_id == comp.id).all()
            history = [{"transcript_text": l.transcript_text, "interaction_type": l.interaction_type} for l in logs]

            if stmt and stmt.parsed_json:
                res = composite_scorer.compute_composite_risk(stmt.parsed_json, comp.sector, history)
                score_obj = RiskScore(
                    company_id=comp.id,
                    fiscal_year=2024,
                    financial_score=res["financial_score"],
                    relationship_score=res["relationship_score"],
                    macro_adjustment=res["macro_adjustment"],
                    composite_score=res["composite_score"],
                    risk_band=res["risk_band"],
                    shap_explanation=res["shap_explanation"]
                )
                db.add(score_obj)
        db.commit()

        print("Database seeded successfully with 5 MSME profiles, interaction logs, and composite risk scores.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
