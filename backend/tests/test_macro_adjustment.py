import pytest
from backend.app.services.macro_adjustment import macro_engine

def test_sector_lookup():
    data = macro_engine.get_sector_data("Retail & E-commerce")
    assert data is not None
    assert "demand_elasticity" in data
    assert float(data["demand_elasticity"]) > 1.0

def test_inelastic_vs_elastic_adjustment():
    # Inelastic sector (Healthcare/Pharma) should have lower risk multiplier (< 1.0)
    pharma_adj = macro_engine.compute_macro_adjustment("Pharmaceuticals & Healthcare")
    assert pharma_adj["macro_adjustment"] < 1.0
    assert pharma_adj["macro_score"] > 70.0

    # Highly elastic & cyclical sector (Construction) should have higher risk multiplier (> 1.0)
    constr_adj = macro_engine.compute_macro_adjustment("Construction & Subcontracting")
    assert constr_adj["macro_adjustment"] > 1.0
    assert constr_adj["macro_score"] < 70.0

def test_interest_rate_shock():
    base_adj = macro_engine.compute_macro_adjustment("Automotive Components", interest_rate_trend=0.0)
    shocked_adj = macro_engine.compute_macro_adjustment("Automotive Components", interest_rate_trend=0.04)
    # Rate shock increases risk multiplier
    assert shocked_adj["macro_adjustment"] >= base_adj["macro_adjustment"]
