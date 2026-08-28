from typing import Dict, Any, Optional, List
from backend.app.services.macro_adjustment import macro_engine

class FinancialRatioEngine:
    """
    Computes comprehensive financial ratios across Liquidity, Solvency, Operating Efficiency,
    and Profitability for MSMEs. Generates sector benchmark comparisons against sector medians.
    """

    def compute_ratios(self, line_items: Dict[str, float], sector: Optional[str] = None) -> Dict[str, Any]:
        """
        Computes all financial ratios from normalized balance sheet and income statement line items.
        Safe division prevents division by zero.
        """
        ca = line_items.get("total_current_assets") or 0.0
        cl = line_items.get("total_current_liabilities") or 0.0
        inv = line_items.get("inventory") or 0.0
        cash = line_items.get("cash_and_equivalents") or 0.0
        
        ta = line_items.get("total_assets") or 0.0
        tl = line_items.get("total_liabilities") or 0.0
        st_debt = line_items.get("short_term_debt") or 0.0
        lt_debt = line_items.get("long_term_debt") or 0.0
        total_debt = (st_debt + lt_debt) if (st_debt + lt_debt) > 0 else (tl * 0.7 if tl > 0 else 0.0)
        
        eq = line_items.get("total_equity") or (ta - tl if ta > tl else 1.0)
        
        rev = line_items.get("revenue") or 0.0
        cogs = line_items.get("cost_of_goods_sold") or 0.0
        gp = line_items.get("gross_profit") or (rev - cogs if rev > 0 else 0.0)
        ebit = line_items.get("ebit") or 0.0
        interest = line_items.get("interest_expense") or 0.0
        ni = line_items.get("net_income") or 0.0
        ar = line_items.get("accounts_receivable") or 0.0

        # --- 1. Liquidity Ratios ---
        current_ratio = round(ca / cl, 3) if cl > 0 else (3.0 if ca > 0 else None)
        quick_ratio = round((ca - inv) / cl, 3) if cl > 0 else (2.5 if (ca - inv) > 0 else None)
        cash_ratio = round(cash / cl, 3) if cl > 0 else (1.0 if cash > 0 else None)
        working_capital = round(ca - cl, 2)

        # --- 2. Solvency & Leverage Ratios ---
        debt_to_equity = round(total_debt / eq, 3) if eq > 0 else (5.0 if total_debt > 0 else 0.0)
        debt_to_assets = round(total_debt / ta, 3) if ta > 0 else None
        
        if interest > 0:
            interest_coverage = round(ebit / interest, 2)
        elif ebit > 0 and interest == 0:
            interest_coverage = 20.0  # Safe high coverage if zero debt interest
        else:
            interest_coverage = 0.0

        # --- 3. Efficiency & Activity Ratios ---
        inventory_turnover = round(cogs / inv, 2) if inv > 0 and cogs > 0 else None
        receivables_turnover = round(rev / ar, 2) if ar > 0 and rev > 0 else None
        dso_days = round(365.0 / receivables_turnover, 1) if (receivables_turnover and receivables_turnover > 0) else None
        asset_turnover = round(rev / ta, 3) if ta > 0 and rev > 0 else None

        # --- 4. Profitability Ratios ---
        gross_margin = round(gp / rev, 4) if rev > 0 else None
        operating_margin = round(ebit / rev, 4) if rev > 0 else None
        net_margin = round(ni / rev, 4) if rev > 0 else None
        roe = round(ni / eq, 4) if eq > 0 else None
        roa = round(ni / ta, 4) if ta > 0 else None

        ratios = {
            "current_ratio": current_ratio,
            "quick_ratio": quick_ratio,
            "cash_ratio": cash_ratio,
            "working_capital": working_capital,
            "debt_to_equity": debt_to_equity,
            "debt_to_assets": debt_to_assets,
            "interest_coverage_ratio": interest_coverage,
            "inventory_turnover": inventory_turnover,
            "receivables_turnover": receivables_turnover,
            "dso_days": dso_days,
            "asset_turnover": asset_turnover,
            "gross_margin": gross_margin,
            "operating_margin": operating_margin,
            "net_margin": net_margin,
            "roe": roe,
            "roa": roa,
            "price_to_book": 1.5  # MSME standard baseline
        }

        # Benchmarks
        benchmarks = self.compute_sector_benchmarks(ratios, sector)

        return {
            "ratios": ratios,
            "benchmarks": benchmarks,
            "sector": sector
        }

    def compute_sector_benchmarks(self, ratios: Dict[str, Any], sector: Optional[str]) -> List[Dict[str, Any]]:
        benchmarks: List[Dict[str, Any]] = []
        sector_data = macro_engine.get_sector_data(sector or "Light Manufacturing & Engineering")
        if not sector_data:
            return benchmarks

        benchmark_map = [
            ("Current Ratio", "current_ratio", float(sector_data.get("median_current_ratio", 1.5)), True),
            ("Quick Ratio", "quick_ratio", float(sector_data.get("median_quick_ratio", 1.0)), True),
            ("Debt-to-Equity", "debt_to_equity", float(sector_data.get("median_debt_to_equity", 1.2)), False), # Lower is better
            ("Gross Margin", "gross_margin", float(sector_data.get("median_gross_margin", 0.25)), True),
            ("Net Margin", "net_margin", float(sector_data.get("median_net_margin", 0.05)), True),
            ("DSO (Days)", "dso_days", float(sector_data.get("median_dso_days", 60.0)), False) # Lower is better
        ]

        for display_name, key, sector_median, higher_is_better in benchmark_map:
            val = ratios.get(key)
            if val is None:
                continue

            # Evaluate status and relative percentile
            if higher_is_better:
                ratio_pct = (val / sector_median) if sector_median > 0 else 1.0
                if ratio_pct >= 1.15:
                    status = "healthy"
                    percentile = min(95.0, 50.0 + (ratio_pct - 1.0) * 35.0)
                elif ratio_pct >= 0.85:
                    status = "warning"
                    percentile = 50.0 + (ratio_pct - 1.0) * 25.0
                else:
                    status = "critical"
                    percentile = max(5.0, ratio_pct * 40.0)
            else:
                # Lower is better (e.g. Debt to equity, DSO)
                ratio_pct = (val / sector_median) if sector_median > 0 else 1.0
                if ratio_pct <= 0.85:
                    status = "healthy"
                    percentile = min(95.0, 50.0 + (1.0 - ratio_pct) * 35.0)
                elif ratio_pct <= 1.20:
                    status = "warning"
                    percentile = 50.0 - (ratio_pct - 1.0) * 25.0
                else:
                    status = "critical"
                    percentile = max(5.0, 50.0 - (ratio_pct - 1.0) * 35.0)

            benchmarks.append({
                "ratio_name": display_name,
                "key": key,
                "company_value": val,
                "sector_median": sector_median,
                "status": status,
                "percentile": round(percentile, 1),
                "higher_is_better": higher_is_better
            })

        return benchmarks

ratio_engine = FinancialRatioEngine()
