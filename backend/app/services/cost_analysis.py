from typing import Dict, Any, Optional

class CostStructureAnalyzer:
    """
    Analyzes fixed vs variable cost classification, operating leverage, and break-even point.
    Crucial for assessing MSME vulnerability to top-line revenue contractions.
    """

    def analyze(self, line_items: Dict[str, float], sector: Optional[str] = None) -> Dict[str, Any]:
        rev = float(line_items.get("revenue", 0.0))
        cogs = float(line_items.get("cost_of_goods_sold", 0.0))
        opex = float(line_items.get("operating_expenses", 0.0))
        ebit = float(line_items.get("ebit", 0.0))

        if rev <= 0:
            return {
                "variable_costs": 0.0,
                "fixed_costs": 0.0,
                "contribution_margin": 0.0,
                "contribution_margin_ratio": 0.0,
                "break_even_revenue": 0.0,
                "margin_of_safety_pct": 0.0,
                "operating_leverage": 1.0,
                "vulnerability_tier": "unknown"
            }

        # Estimation heuristics:
        # COGS is primarily variable (~85% variable materials/labor, 15% fixed factory overhead)
        # OpEx is primarily fixed (~75% fixed rent/salaries/depreciation, 25% variable sales commission/freight)
        variable_costs = (cogs * 0.85) + (opex * 0.25)
        fixed_costs = (cogs * 0.15) + (opex * 0.75)

        contribution_margin = rev - variable_costs
        cm_ratio = contribution_margin / rev if rev > 0 else 0.0

        # Break-Even Revenue = Fixed Costs / Contribution Margin Ratio
        break_even_rev = (fixed_costs / cm_ratio) if cm_ratio > 0 else (rev * 2.0)
        
        # Margin of Safety = (Actual Revenue - Break Even Revenue) / Actual Revenue
        margin_of_safety = ((rev - break_even_rev) / rev) if rev > 0 else -1.0

        # Degree of Operating Leverage (DOL) = Contribution Margin / EBIT
        if ebit > 0:
            operating_leverage = min(15.0, round(contribution_margin / ebit, 2))
        else:
            operating_leverage = 20.0  # High operational risk when operating at a loss

        # Vulnerability classification
        if margin_of_safety > 0.30 and operating_leverage < 3.5:
            vulnerability_tier = "low_cost_risk"
        elif margin_of_safety > 0.10:
            vulnerability_tier = "moderate_cost_risk"
        else:
            vulnerability_tier = "high_fixed_cost_vulnerability"

        return {
            "variable_costs": round(variable_costs, 2),
            "fixed_costs": round(fixed_costs, 2),
            "contribution_margin": round(contribution_margin, 2),
            "contribution_margin_ratio": round(cm_ratio, 4),
            "break_even_revenue": round(break_even_rev, 2),
            "margin_of_safety_pct": round(margin_of_safety * 100, 2),
            "operating_leverage": operating_leverage,
            "vulnerability_tier": vulnerability_tier
        }

cost_analyzer = CostStructureAnalyzer()
