import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "CreditPulse"

def test_companies_list():
    response = client.get("/api/companies/")
    assert response.status_code == 200
    companies = response.json()
    assert isinstance(companies, list)
    assert len(companies) > 0

def test_company_ratios_and_benchmarks():
    response = client.get("/api/ratios/1/benchmarks")
    assert response.status_code == 200
    data = response.json()
    assert "benchmarks" in data
    assert "ratios" in data
    assert len(data["benchmarks"]) > 0

def test_company_credit_score_and_shap():
    response = client.get("/api/scores/1")
    assert response.status_code == 200
    data = response.json()
    assert "composite_score" in data
    assert "risk_band" in data
    assert "shap_explanation" in data
    assert len(data["shap_explanation"]) > 0

def test_msme_health_report():
    response = client.get("/api/scores/1/health-report")
    assert response.status_code == 200
    data = response.json()
    assert "credit_readiness_score" in data
    assert "key_strengths" in data
    assert "actionable_recommendations" in data

def test_portfolio_overview():
    response = client.get("/api/scores/portfolio/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_assessed_companies" in data
    assert "risk_distribution" in data
