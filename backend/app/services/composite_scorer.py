from typing import Dict, Any, List, Optional, Tuple
from backend.app.ml.risk_model import risk_model
from backend.app.ml.shap_explainer import shap_engine
from backend.app.ml.nlp_engine import nlp_engine
from backend.app.services.macro_adjustment import macro_engine
from backend.app.services.ratio_engine import ratio_engine
from backend.app.services.cost_analysis import cost_analyzer
from backend.app.core.config import settings

class CompositeCreditScorer:
    """
    Fuses Multi-Modal Credit Risk Signals:
    - 60% Structured Financial ML Score (Ratios, Cost Structure, XGBoost Default Probability)
    - 25% Unstructured NLP Relationship Score (Negotiation tone, Friction, Service Recovery)
    - 15% Macro/Sector Elasticity Resilience Score (Demand elasticity, cyclicality cushion)
    """

    def compute_composite_risk(
        self,
        line_items: Dict[str, float],
        sector: str,
        interaction_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        # 1. Financial Risk Model & SHAP
        fin_res = risk_model.predict(line_items, sector)
        financial_score = fin_res["financial_score"]
        shap_breakdown = shap_engine.explain(line_items, sector)
        ratios_data = ratio_engine.compute_ratios(line_items, sector)
        cost_data = cost_analyzer.analyze(line_items, sector)

        # 2. Relationship NLP Analysis
        rel_data = nlp_engine.compute_relationship_score(interaction_history or [])
        relationship_score = rel_data["relationship_score"]

        # 3. Macro Sector Elasticity
        macro_data = macro_engine.compute_macro_adjustment(sector)
        macro_score = macro_data["macro_score"]
        macro_mult = macro_data["macro_adjustment"]

        # 4. Weighted Composite Fusion
        w_fin = settings.WEIGHT_FINANCIAL_SCORE        # 0.60
        w_rel = settings.WEIGHT_RELATIONSHIP_SCORE    # 0.25
        w_mac = settings.WEIGHT_MACRO_ADJUSTMENT      # 0.15

        raw_composite = (financial_score * w_fin) + (relationship_score * w_rel) + (macro_score * w_mac)
        composite_score = round(max(5.0, min(99.0, raw_composite)), 1)

        # 5. Risk Band Classification
        if composite_score >= 75.0:
            risk_band = "low"
            risk_band_label = "Low Risk (Grade A)"
            recommendation = "Approved for standard unsecured or secured working capital facilities."
        elif composite_score >= 50.0:
            risk_band = "medium"
            risk_band_label = "Medium Risk (Grade B/C)"
            recommendation = "Conditional approval recommended with enhanced covenants, receivables pledge, or monitoring."
        else:
            risk_band = "high"
            risk_band_label = "High Risk (Grade D/F)"
            recommendation = "Elevated credit risk. Additional collateral, personal guarantee, or restructuring required."

        # 6. Actionable MSME Health Improvement Insights
        actionable_tips = self._generate_actionable_recommendations(ratios_data["ratios"], cost_data, rel_data)

        # 7. Key Strengths & Vulnerabilities
        strengths, vulnerabilities = self._extract_strengths_vulnerabilities(shap_breakdown, rel_data, macro_data)

        return {
            "composite_score": composite_score,
            "risk_band": risk_band,
            "risk_band_label": risk_band_label,
            "probability_of_default": fin_res["probability_of_default"],
            "financial_score": financial_score,
            "relationship_score": relationship_score,
            "macro_score": macro_score,
            "macro_adjustment": macro_mult,
            "weight_distribution": {
                "financial_weight": int(w_fin * 100),
                "relationship_weight": int(w_rel * 100),
                "macro_weight": int(w_mac * 100)
            },
            "recommendation": recommendation,
            "shap_explanation": shap_breakdown,
            "financial_ratios": ratios_data["ratios"],
            "benchmarks": ratios_data["benchmarks"],
            "cost_structure": cost_data,
            "relationship_summary": rel_data,
            "macro_summary": macro_data,
            "key_strengths": strengths,
            "critical_vulnerabilities": vulnerabilities,
            "actionable_recommendations": actionable_tips
        }

    def _generate_actionable_recommendations(
        self,
        ratios: Dict[str, Any],
        cost_data: Dict[str, Any],
        rel_data: Dict[str, Any]
    ) -> List[str]:
        tips: List[str] = []

        cr = ratios.get("current_ratio") or 1.0
        if cr < 1.2:
            tips.append(f"Improve Liquidity Buffer: Current ratio is {cr:.2f} (Target: >1.50). Consider refinancing short-term supplier dues into a structured term facility.")

        dso = ratios.get("dso_days") or 60.0
        if dso > 70:
            tips.append(f"Accelerate Debtor Collections: Average collection cycle is {dso:.0f} days. Implementing 2% early-payment cash discounts could reduce DSO by 15-20 days.")

        de = ratios.get("debt_to_equity") or 1.0
        if de > 1.8:
            tips.append(f"De-leverage Capital Structure: Debt-to-Equity is {de:.2f}. Retaining higher quarterly earnings will strengthen net worth and borrowing capacity.")

        if cost_data.get("vulnerability_tier") == "high_fixed_cost_vulnerability":
            tips.append("Variable Cost Optimization: Fixed overheads represent a high share of costs. Shifting certain fixed contracts to variable/usage-based can improve break-even safety.")

        if rel_data.get("average_sentiment", 0.0) < 0:
            tips.append("B2B Relationship Repair: Recent commercial interactions exhibit payment friction. Formalizing milestone-linked agreements can stabilize partner trust.")

        if not tips:
            tips.append("Maintain Current Trajectory: Financial ratios and relationship signals meet investment grade benchmarks.")

        return tips

    def _extract_strengths_vulnerabilities(
        self,
        shap_items: List[Dict[str, Any]],
        rel_data: Dict[str, Any],
        macro_data: Dict[str, Any]
    ) -> Tuple[List[str], List[str]]:
        strengths = []
        vulnerabilities = []

        for item in shap_items:
            if item["impact_direction"] == "decreases_risk" and len(strengths) < 3:
                strengths.append(f"Strong {item['feature_name_display']} (Value: {item['value']}) reduces credit risk profile.")
            elif item["impact_direction"] == "increases_risk" and len(vulnerabilities) < 3:
                vulnerabilities.append(f"Elevated risk from {item['feature_name_display']} (Value: {item['value']}).")

        if rel_data.get("relationship_score", 70) >= 80:
            strengths.append("High B2B partner satisfaction with proven service recovery record.")
        elif rel_data.get("relationship_score", 70) < 60:
            vulnerabilities.append("Unresolved B2B dispute and delivery friction indicators.")

        if macro_data.get("macro_adjustment", 1.0) < 0.90:
            strengths.append(f"Favorable sector tailwinds in {macro_data.get('sector')}.")
        elif macro_data.get("macro_adjustment", 1.0) > 1.15:
            vulnerabilities.append(f"Sector cyclicality and demand elasticity headwinds.")

        return strengths[:4], vulnerabilities[:4]

composite_scorer = CompositeCreditScorer()
