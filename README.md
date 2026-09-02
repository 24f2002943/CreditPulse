# CreditPulse 💳⚡
### Relationship-Aware MSME Multi-Modal Credit Scoring & Risk Intelligence Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.111-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js_14_App_Router-000000.svg?logo=next.js&logoColor=white)](https://nextjs.org)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost_SHAP-FF6F00.svg?logo=scikitlearn&logoColor=white)](https://xgboost.readthedocs.io)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript_5-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Python](https://img.shields.io/badge/Language-Python_3.11+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview

**CreditPulse** is a next-generation AI-powered credit underwriting and financial intelligence platform built specifically for **Micro, Small, and Medium Enterprises (MSMEs)**.

Traditional credit bureaus rely almost exclusively on lagging, static balance-sheet ratios and collateral requirements, systematically underscoring creditworthy MSMEs. **CreditPulse solves this by pioneering a composite multi-modal credit scoring architecture** that fuses three complementary risk dimensions:

1. **Structured Financial Health (60%)** — Advanced ratio analysis (liquidity, leverage, profitability, debt-service coverage, DSO) benchmarked against sector distributions, plus operating leverage and fixed/variable cost structure vulnerability.
2. **Unstructured Commercial Relationship Signals (25%)** — NLP-powered sentiment, negotiation tone, and dispute resolution tracking extracted from real-world B2B buyer-supplier communication logs.
3. **Macroeconomic & Sector Demand Elasticity (15%)** — Dynamic macro multiplier adjusting risk exposure based on industry cyclicality, price elasticity, and sectoral GDP growth rates.

Every prediction is fully audited via an interpretable **SHAP (SHapley Additive exPlanations)** layer, providing complete transparency into which positive and negative drivers influenced the underwriting decision.

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   CreditPulse Platform                                 │
└────────────────────────────────────┬───────────────────────────────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│ Financial Ratios │       │  B2B Interaction │       │  Macro Elasticity│
│   & Cost Engine  │       │    NLP Engine    │       │     Dynamics     │
│   (Weight: 60%)  │       │   (Weight: 25%)  │       │   (Weight: 15%)  │
└────────┬─────────┘       └────────┬─────────┘       └────────┬─────────┘
         │                          │                          │
         └──────────────────────────┼──────────────────────────┘
                                    ▼
                 ┌──────────────────────────────────────┐
                 │ Composite Credit Risk Scoring Engine │
                 │    (XGBoost + Calibrated PD Score)   │
                 └──────────────────┬───────────────────┘
                                    │
         ┌──────────────────────────┴──────────────────────────┐
         ▼                                                     ▼
┌──────────────────────────────────┐         ┌──────────────────────────────────┐
│   Explainability & Audit Layer   │         │       Next.js 14 Dashboard       │
│    (SHAP Waterfall & Drivers)    │         │ (Lender Analyst & MSME Portals)  │
└──────────────────────────────────┘         └──────────────────────────────────┘
```

---

## ✨ Key Features

### 🏦 For Lenders & Credit Analysts
- **Portfolio Health Dashboard**: Instant visibility into aggregate portfolio score (0–100), risk band distribution (Low, Medium, High), and estimated loan approval rates.
- **Explainable Underwriting (SHAP)**: High-resolution waterfall analysis detailing the exact positive or negative contribution of each metric to default probability.
- **Financial Statement Parsing (Excel & OCR)**: Automated ingestion and accounting equation balance validation (`Assets = Liabilities + Equity`).
- **Cost Structure & Operating Leverage**: Marginal cost breakdown, contribution margin ratio, break-even revenue, and fixed cost vulnerability tiers.
- **B2B Commercial Sentiment Timeline**: Natural language processing on negotiation transcripts, concession patterns, and dispute resolution rates.

### 🏢 For MSME Owners
- **Credit Readiness Portal**: Clean, transparent score breakdown showing where the business stands before applying for bank loans.
- **Interactive "What-If" Scenario Simulator**: Real-time slider simulator estimating score impact when paying down debt, speeding up receivable collections, or cutting fixed overhead.
- **Prioritized Action Plan**: Ranked, human-readable guidance to help business owners remediate vulnerabilities and secure favorable lending terms.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, high-performance async REST API framework with automatic OpenAPI/Swagger documentation.
- **XGBoost & Scikit-learn**: Machine learning credit risk classification and probability-of-default calibration.
- **SHAP (SHapley Additive exPlanations)**: Game-theoretic feature attribution for transparent risk scoring.
- **SQLAlchemy & SQLite**: ORM data layer for companies, financial statements, and interaction logs.
- **PyPDF / OpenPyXL / Tesseract OCR**: Multi-format document ingestion pipeline.
- **Pytest**: Complete unit and integration test suite across all scoring modules.

### Frontend
- **Next.js 14 (App Router)**: High-performance React framework with server-side rendering and static optimization.
- **Tailwind CSS**: Custom dark fintech design system with glassmorphic cards, luminous gradients, and responsive layouts.
- **Lucide Icons**: Crisp, modern icon set.
- **TypeScript**: Strict type safety across all API interfaces and data models.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** / **npm 9+**
- *(Optional)* **Docker & Docker Compose**

---

### Method 1: Local Development

#### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/CreditPulse.git
cd CreditPulse
```

#### 2. Backend Setup
```bash
cd backend
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend will be live at `http://localhost:8000` (Swagger UI at `http://localhost:8000/docs`).

#### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Frontend will be live at `http://localhost:3000`.

---

### Method 2: Docker Compose (One-Click)
```bash
docker-compose up --build
```
Access the application at `http://localhost:3000`.

---

## 🧪 Running Tests

Execute the comprehensive Pytest suite:
```bash
cd backend
pytest -v
```

Test coverage includes:
- Multi-format Excel and OCR statement parsing
- Accounting equation balance validation
- Financial ratios calculation and sector benchmarking
- Fixed vs variable cost structure and break-even analysis
- XGBoost credit default model and SHAP feature attributions
- Macro elasticity sector multiplier adjustments
- B2B interaction NLP sentiment and dispute resolution analysis
- End-to-end composite scoring API

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/companies/` | List all registered MSMEs with sector metadata |
| `POST` | `/api/companies/` | Register a new MSME entity |
| `POST` | `/api/statements/upload` | Upload & parse balance sheet / income statement (Excel/PDF) |
| `GET` | `/api/scores/{company_id}` | Compute multi-modal composite credit score + SHAP explanation |
| `GET` | `/api/scores/portfolio/overview` | Aggregated portfolio risk distribution and metrics |
| `GET` | `/api/interactions/company/{company_id}` | Retrieve historical B2B communication logs |
| `POST` | `/api/interactions/` | Record new interaction transcript with NLP sentiment analysis |
| `GET` | `/api/macro/sectors` | Retrieve sectoral price elasticity & macro growth indicators |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
