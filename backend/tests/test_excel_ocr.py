import pytest
from backend.app.services.accounting_validator import accounting_validator
from backend.app.services.ocr_pipeline import ocr_pipeline
from backend.app.services.excel_parser import excel_parser

def test_accounting_validator_balanced():
    balanced_items = {
        "total_assets": 1000000.0,
        "total_current_assets": 600000.0,
        "total_liabilities": 400000.0,
        "total_current_liabilities": 250000.0,
        "total_equity": 600000.0,
        "revenue": 1200000.0,
        "cost_of_goods_sold": 800000.0,
        "gross_profit": 400000.0,
        "operating_expenses": 200000.0,
        "ebit": 200000.0,
        "interest_expense": 20000.0,
        "tax_expense": 45000.0,
        "net_income": 135000.0
    }
    res = accounting_validator.validate(balanced_items)
    assert res["is_valid"] is True
    assert res["accounting_equation_balanced"] is True
    assert res["confidence_score"] >= 90.0
    assert len(res["errors"]) == 0

def test_accounting_validator_unbalanced():
    unbalanced_items = {
        "total_assets": 1000000.0,
        "total_liabilities": 300000.0,
        "total_equity": 400000.0 # Missing 300,000!
    }
    res = accounting_validator.validate(unbalanced_items)
    assert res["is_valid"] is False
    assert res["accounting_equation_balanced"] is False
    assert len(res["errors"]) > 0

def test_raw_text_ocr_parser():
    sample_text = """
    Apex Engineering Balance Sheet 2024
    Cash and equivalents: $150,000
    Accounts Receivable: $350,000
    Inventory: $400,000
    Total Current Assets: $900,000
    Property Plant and Equipment: $600,000
    Total Assets: $1,500,000
    Accounts Payable: $200,000
    Short Term Debt: $150,000
    Total Current Liabilities: $350,000
    Long Term Debt: $250,000
    Total Liabilities: $600,000
    Total Equity: $900,000
    """
    res = ocr_pipeline.parse_raw_text(sample_text)
    items = res["line_items"]
    assert items["total_assets"] == 1500000.0
    assert items["total_liabilities"] == 600000.0
    assert items["total_equity"] == 900000.0
    assert res["validation"]["accounting_equation_balanced"] is True
