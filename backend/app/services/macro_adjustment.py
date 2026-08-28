import os
import pandas as pd
from typing import Dict, Any, Optional

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sector_elasticity.csv")

class MacroAdjustmentEngine:
    """
    Computes sector demand elasticity risk adjustments for MSME credit scoring.
    Fuses sector demand price elasticity, cyclicality index, margin sensitivity,
    and macroeconomic growth trends into a calibrated multiplier.
    """
    def __init__(self, data_path: str = DATA_PATH):
        self.data_path = data_path
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.data_path):
            self.df = pd.read_csv(self.data_path)
            # Create a normalized sector lookup key (lowercase, alphanumeric)
            self.df["lookup_key"] = self.df["sector"].str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
        else:
            self.df = pd.DataFrame()

    def get_sector_data(self, sector: str) -> Optional[Dict[str, Any]]:
        if self.df.empty:
            return None
        lookup = sector.lower().replace(" ", "").replace("&", "").replace("-", "")
        matches = self.df[self.df["lookup_key"].str.contains(lookup) | (self.df["sector"].str.lower() == sector.lower())]
        if not matches.empty:
            return matches.iloc[0].to_dict()
        # Fallback to the first sector or average
        return self.df.iloc[0].to_dict()

    def compute_macro_adjustment(
        self,
        sector: str,
        interest_rate_trend: float = 0.0, # e.g. +0.02 for +200bps rate tightening
        inflation_pressure: float = 0.0   # e.g. +0.03 for elevated input inflation
    ) -> Dict[str, Any]:
        """
        Calculates the risk multiplier and adjustment score for a company's sector.
        - High elasticity (> 1.2) + High cyclicality + Rate hikes = Higher Default Vulnerability (Risk Multiplier > 1.0)
        - Inelastic demand (< 0.6) + Stable growth = Lower Vulnerability (Risk Multiplier < 1.0)
        
        Returns:
            Dict containing:
            - macro_adjustment: float (e.g. 0.85 to 1.35)
            - macro_score: float (0 - 100, where 100 is best / lowest macro risk)
            - elasticity: float
            - cyclicality: float
            - sector_growth_rate: float
            - rationale: str
        """
        sector_info = self.get_sector_data(sector)
        if not sector_info:
            # Default neutral adjustment
            return {
                "macro_adjustment": 1.0,
                "macro_score": 70.0,
                "elasticity": 1.0,
                "cyclicality": 0.5,
                "sector_growth_rate": 0.05,
                "rationale": f"Neutral baseline applied; specific data for '{sector}' unavailable."
            }

        elasticity = float(sector_info.get("demand_elasticity", 1.0))
        cyclicality = float(sector_info.get("cyclicality_index", 0.5))
        growth_rate = float(sector_info.get("growth_rate_yoy", 0.05))
        margin_sensitivity = float(sector_info.get("margin_sensitivity", 0.6))
        base_default_rate = float(sector_info.get("default_base_rate", 0.04))

        # Core Risk Multiplier Formula:
        # Base vulnerability is driven by elasticity and cyclicality dampened by sector growth.
        # Macro shocks (inflation, interest rates) amplify vulnerable sectors proportionally to elasticity and margin sensitivity.
        macro_shock_impact = (interest_rate_trend * 1.5 * cyclicality) + (inflation_pressure * 2.0 * margin_sensitivity)
        growth_cushion = max(-0.15, min(0.15, growth_rate - 0.06))

        raw_multiplier = 1.0 + (elasticity - 1.0) * 0.25 + (cyclicality - 0.5) * 0.20 - (growth_cushion * 1.2) + macro_shock_impact
        # Bound multiplier between 0.70 (very favorable) and 1.45 (severe macro headwind)
        multiplier = max(0.70, min(1.45, round(raw_multiplier, 4)))

        # Convert multiplier to a 0-100 macro resilience score (where lower multiplier = higher score)
        # Multiplier 0.70 -> Score 95; Multiplier 1.0 -> Score 70; Multiplier 1.45 -> Score 35
        macro_score = max(10.0, min(99.0, round(100.0 - (multiplier - 0.70) * (90.0 / 0.75), 1)))

        # Qualitative Rationale Generator
        if elasticity > 1.2:
            elasticity_desc = f"high price elasticity ({elasticity:.2f}), making revenue sensitive to price shifts"
        elif elasticity < 0.6:
            elasticity_desc = f"inelastic essential demand ({elasticity:.2f}), providing resilient pricing power"
        else:
            elasticity_desc = f"moderate demand elasticity ({elasticity:.2f})"

        rationale = (
            f"Sector '{sector_info.get('sector')}' exhibits {elasticity_desc} and a "
            f"cyclicality index of {cyclicality:.2f} with YoY growth of {growth_rate*100:.1f}%. "
            f"Overall macro risk multiplier is {multiplier:.2f} (Resilience score: {macro_score}/100)."
        )

        return {
            "sector": sector_info.get("sector"),
            "macro_adjustment": multiplier,
            "macro_score": macro_score,
            "elasticity": elasticity,
            "cyclicality": cyclicality,
            "sector_growth_rate": growth_rate,
            "margin_sensitivity": margin_sensitivity,
            "default_base_rate": base_default_rate,
            "rationale": rationale
        }

macro_engine = MacroAdjustmentEngine()
