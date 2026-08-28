import os
import pickle
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score

from backend.app.ml.synthetic_generator import synthetic_generator
from backend.app.services.ratio_engine import ratio_engine
from backend.app.services.cost_analysis import cost_analyzer
from backend.app.services.macro_adjustment import macro_engine

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_FILE = os.path.join(MODEL_DIR, "xgboost_credit_model.pkl")
BACKGROUND_DATA_FILE = os.path.join(MODEL_DIR, "shap_background.pkl")

FEATURE_NAMES = [
    "current_ratio",
    "quick_ratio",
    "debt_to_equity",
    "interest_coverage_ratio",
    "gross_margin",
    "net_margin",
    "roa",
    "dso_days",
    "macro_adjustment",
    "operating_leverage",
    "margin_of_safety_pct"
]

FEATURE_DISPLAY_NAMES = {
    "current_ratio": "Current Ratio (Liquidity)",
    "quick_ratio": "Quick Ratio (Immediate Liquidity)",
    "debt_to_equity": "Debt-to-Equity (Leverage)",
    "interest_coverage_ratio": "Interest Coverage (Solvency)",
    "gross_margin": "Gross Margin (Pricing Power)",
    "net_margin": "Net Margin (Profitability)",
    "roa": "Return on Assets (Asset Efficiency)",
    "dso_days": "Days Sales Outstanding (Debtor Collection)",
    "macro_adjustment": "Sector Macro Risk Multiplier",
    "operating_leverage": "Operating Leverage (Fixed Cost Sensitivity)",
    "margin_of_safety_pct": "Margin of Safety (%)"
}

class CreditRiskModel:
    """
    XGBoost-based default risk classifier for MSMEs.
    Extracts structured financial ratios, cost structure, and sector elasticity
    to predict Probability of Default (PD) and Financial Health Score (0-100).
    """

    def __init__(self):
        os.makedirs(MODEL_DIR, exist_ok=True)
        self.model: Optional[xgb.XGBClassifier] = None
        self.background_data: Optional[np.ndarray] = None
        self.metrics: Dict[str, float] = {}
        self._load_or_train()

    def extract_features(self, line_items: Dict[str, float], sector: str) -> pd.DataFrame:
        """
        Converts line items into feature vector matching model schema.
        """
        ratios_dict = ratio_engine.compute_ratios(line_items, sector)["ratios"]
        cost_dict = cost_analyzer.analyze(line_items, sector)
        macro_dict = macro_engine.compute_macro_adjustment(sector)

        row = {
            "current_ratio": ratios_dict.get("current_ratio") or 1.5,
            "quick_ratio": ratios_dict.get("quick_ratio") or 1.0,
            "debt_to_equity": ratios_dict.get("debt_to_equity") or 1.2,
            "interest_coverage_ratio": min(50.0, max(-10.0, ratios_dict.get("interest_coverage_ratio") or 3.0)),
            "gross_margin": ratios_dict.get("gross_margin") or 0.25,
            "net_margin": ratios_dict.get("net_margin") or 0.05,
            "roa": ratios_dict.get("roa") or 0.06,
            "dso_days": ratios_dict.get("dso_days") or 60.0,
            "macro_adjustment": macro_dict.get("macro_adjustment") or 1.0,
            "operating_leverage": min(20.0, max(0.5, cost_dict.get("operating_leverage") or 2.0)),
            "margin_of_safety_pct": cost_dict.get("margin_of_safety_pct") or 20.0
        }
        return pd.DataFrame([row])[FEATURE_NAMES]

    def build_dataset_from_synthetic(self, df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        feature_rows = []
        labels = []

        for _, row in df_raw.iterrows():
            line_items = row.to_dict()
            sector = row["sector"]
            df_feat = self.extract_features(line_items, sector)
            feature_rows.append(df_feat.iloc[0])
            labels.append(row["defaulted"])

        X = pd.DataFrame(feature_rows)
        y = pd.Series(labels)
        return X, y

    def train(self, n_samples: int = 2500):
        print(f"Generating {n_samples} synthetic MSME profiles for model training...")
        raw_df = synthetic_generator.generate_synthetic_dataset(n_samples=n_samples)
        X, y = self.build_dataset_from_synthetic(raw_df)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        self.model = xgb.XGBClassifier(
            n_estimators=120,
            max_depth=4,
            learning_rate=0.08,
            subsample=0.85,
            colsample_bytree=0.85,
            eval_metric="logloss",
            random_state=42
        )
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]

        self.metrics = {
            "roc_auc": round(roc_auc_score(y_test, y_prob), 4),
            "precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
            "recall": round(recall_score(y_test, y_pred, zero_division=0), 4),
            "f1_score": round(f1_score(y_test, y_pred, zero_division=0), 4),
            "train_samples": len(X_train),
            "test_samples": len(X_test)
        }

        # Save model and background summary
        self.background_data = X_train.sample(n=min(150, len(X_train)), random_state=42).values
        with open(MODEL_FILE, "wb") as f:
            pickle.dump({"model": self.model, "metrics": self.metrics}, f)
        with open(BACKGROUND_DATA_FILE, "wb") as f:
            pickle.dump(self.background_data, f)

        print(f"Model trained successfully. ROC-AUC: {self.metrics['roc_auc']}, F1: {self.metrics['f1_score']}")

    def _load_or_train(self):
        if os.path.exists(MODEL_FILE) and os.path.exists(BACKGROUND_DATA_FILE):
            try:
                with open(MODEL_FILE, "rb") as f:
                    data = pickle.load(f)
                    self.model = data["model"]
                    self.metrics = data.get("metrics", {})
                with open(BACKGROUND_DATA_FILE, "rb") as f:
                    self.background_data = pickle.load(f)
                return
            except Exception:
                pass
        self.train()

    def predict(self, line_items: Dict[str, float], sector: str) -> Dict[str, Any]:
        """
        Predicts Probability of Default and Financial Health Score (0-100).
        """
        X = self.extract_features(line_items, sector)
        prob_default = float(self.model.predict_proba(X)[0, 1])

        # Financial Score is 0 - 100 where 100 is best / minimal default risk
        financial_score = round(max(5.0, min(98.0, (1.0 - prob_default) * 100.0)), 1)

        return {
            "probability_of_default": round(prob_default, 4),
            "financial_score": financial_score,
            "feature_values": X.iloc[0].to_dict(),
            "metrics": self.metrics
        }

risk_model = CreditRiskModel()
