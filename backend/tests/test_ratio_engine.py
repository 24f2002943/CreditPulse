import pytest
from backend.app.services.ratio_engine import ratio_engine

def test_financial_ratios_calculation():
    line_items = {
        "total_current_assets": 500000.0,
        "total_current_liabilities": 250000.0,
        "inventory": 100000.0,
        "cash_and_equivalents": 80000.0,
        "total_assets": 1200000.0,
        "total_liabilities": 500000.0,
        "short_term_debt": 150000.0,
        "long_term_debt": 250000.0,
        "total_equity": 700000.0,
        "revenue": 1800000.0,
        "cost_of_goods_sold": 1200000.0,
        "gross_profit": 600000.0,
        "ebit": 300000.0,
        "interest_expense": 40000.0,
        "net_income": 195000.0,
        "accounts_receivable": 300000.0
    }

    res = ratio_engine.compute_ratios(line_items, sector="Light Manufacturing & Engineering")
    r = res["ratios"]

    # Current ratio = 500k / 250k = 2.0
    assert r["current_ratio"] == 2.0
    # Quick ratio = (500k - 100k) / 250k = 1.6
    assert r["quick_ratio"] == 1.6
    # Working capital = 500k - 250k = 250k
    assert r["working_capital"] == 250000.0
    # Debt to equity = (150k + 250k) / 700k = 0.571
    assert abs(r["debt_to_equity"] - 0.571) < 0.01
    # Interest coverage = 300k / 40k = 7.5
    assert r["interest_coverage_ratio"] == 7.5
    # Gross margin = 600k / 1800k = 0.3333
    assert abs(r["gross_margin"] - 0.3333) < 0.001
    # Receivables turnover = 1800k / 300k = 6.0 -> DSO = 365 / 6 = 60.8 days
    assert r["receivables_turnover"] == 6.0
    assert abs(r["dso_days"] - 60.8) < 0.2

    # Benchmarks should be populated
    assert len(res["benchmarks"]) > 0
