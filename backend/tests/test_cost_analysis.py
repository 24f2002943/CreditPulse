import pytest
from backend.app.services.cost_analysis import cost_analyzer

def test_cost_classification_and_breakeven():
    line_items = {
        "revenue": 1000000.0,
        "cost_of_goods_sold": 600000.0,
        "operating_expenses": 200000.0,
        "ebit": 200000.0
    }
    res = cost_analyzer.analyze(line_items)
    
    assert res["contribution_margin"] > 0
    assert res["break_even_revenue"] < 1000000.0
    assert res["margin_of_safety_pct"] > 0
    assert res["operating_leverage"] > 0
    assert res["vulnerability_tier"] in ["low_cost_risk", "moderate_cost_risk"]
