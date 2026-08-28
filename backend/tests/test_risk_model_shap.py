import pytest
from backend.app.ml.risk_model import risk_model
from backend.app.ml.shap_explainer import shap_engine

def test_ml_risk_prediction():
    line_items = {
        "revenue": 3000000.0,
        "cost_of_goods_sold": 2000000.0,
        "gross_profit": 1000000.0,
        "operating_expenses": 500000.0,
        "ebit": 500000.0,
        "interest_expense": 50000.0,
        "net_income": 337500.0,
        "total_assets": 2500000.0,
        "total_current_assets": 1600000.0,
        "cash_and_equivalents": 300000.0,
        "inventory": 600000.0,
        "accounts_receivable": 700000.0,
        "total_liabilities": 900000.0,
        "total_current_liabilities": 600000.0,
        "short_term_debt": 250000.0,
        "long_term_debt": 300000.0,
        "total_equity": 1600000.0
    }

    pred = risk_model.predict(line_items, sector="Light Manufacturing & Engineering")
    assert "probability_of_default" in pred
    assert 0.0 <= pred["probability_of_default"] <= 1.0
    assert 0.0 <= pred["financial_score"] <= 100.0
    assert pred["financial_score"] > 60.0  # Healthy MSME should have a strong score

def test_shap_explanation():
    line_items = {
        "revenue": 3000000.0,
        "cost_of_goods_sold": 2000000.0,
        "gross_profit": 1000000.0,
        "operating_expenses": 500000.0,
        "ebit": 500000.0,
        "interest_expense": 50000.0,
        "net_income": 337500.0,
        "total_assets": 2500000.0,
        "total_current_assets": 1600000.0,
        "total_liabilities": 900000.0,
        "total_current_liabilities": 600000.0,
        "short_term_debt": 250000.0,
        "total_equity": 1600000.0
    }

    shap_exp = shap_engine.explain(line_items, sector="Light Manufacturing & Engineering")
    assert isinstance(shap_exp, list)
    assert len(shap_exp) > 0
    top_feature = shap_exp[0]
    assert "feature" in top_feature
    assert "shap_value" in top_feature
    assert "impact_direction" in top_feature
