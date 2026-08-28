import shap
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from backend.app.ml.risk_model import risk_model, FEATURE_NAMES, FEATURE_DISPLAY_NAMES

class SHAPExplainerEngine:
    """
    Computes exact Shapley Additive exPlanations (SHAP) for credit risk predictions.
    Provides auditable, transparent explanations for loan underwriters and regulatory compliance.
    """

    def __init__(self):
        self.explainer: Optional[shap.TreeExplainer] = None
        self._init_explainer()

    def _init_explainer(self):
        if risk_model.model is not None:
            self.explainer = shap.TreeExplainer(risk_model.model)

    def explain(self, line_items: Dict[str, float], sector: str) -> List[Dict[str, Any]]:
        if self.explainer is None:
            self._init_explainer()

        X = risk_model.extract_features(line_items, sector)
        shap_values = self.explainer.shap_values(X)

        # Handle 1D or 2D shap output
        if isinstance(shap_values, list):
            sv = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
        elif len(shap_values.shape) > 1:
            sv = shap_values[0]
        else:
            sv = shap_values

        explanations: List[Dict[str, Any]] = []
        for feat_name, shap_val in zip(FEATURE_NAMES, sv):
            feat_val = float(X[feat_name].iloc[0])
            shap_v = float(shap_val)

            # Impact direction on default risk:
            # Positive SHAP value increases log-odds of default (increases risk)
            # Negative SHAP value decreases log-odds of default (protects / decreases risk)
            if shap_v > 0.005:
                direction = "increases_risk"
                effect_label = "Elevates Risk"
            elif shap_v < -0.005:
                direction = "decreases_risk"
                effect_label = "Lowers Risk"
            else:
                direction = "neutral"
                effect_label = "Neutral Impact"

            explanations.append({
                "feature": feat_name,
                "feature_name_display": FEATURE_DISPLAY_NAMES.get(feat_name, feat_name),
                "value": round(feat_val, 3),
                "shap_value": round(shap_v, 4),
                "impact_direction": direction,
                "effect_label": effect_label,
                "importance_magnitude": round(abs(shap_v), 4)
            })

        # Sort by absolute importance (highest impact first)
        explanations.sort(key=lambda x: x["importance_magnitude"], reverse=True)
        return explanations

shap_engine = SHAPExplainerEngine()
