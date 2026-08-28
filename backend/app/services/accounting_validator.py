from typing import Dict, Any, List, Optional

class AccountingEquationValidator:
    """
    Validates data integrity and accounting equation balance on extracted financial statements:
    - Fundamental Balance Sheet Equation: Total Assets = Total Liabilities + Total Equity
    - Sub-component checks: Current Assets <= Total Assets, Current Liabilities <= Total Liabilities
    - Income Statement Equation: Net Income = Revenue - COGS - OpEx - Interest - Tax
    """

    def __init__(self, tolerance_pct: float = 0.02, tolerance_abs: float = 500.0):
        self.tolerance_pct = tolerance_pct
        self.tolerance_abs = tolerance_abs

    def validate(self, line_items: Dict[str, float]) -> Dict[str, Any]:
        """
        Validates the extracted financial statement data.
        Returns validation status, boolean is_balanced flag, confidence score (0-100), and issues list.
        """
        errors: List[str] = []
        warnings: List[str] = []
        checks_passed = 0
        total_checks = 0

        # --- 1. Balance Sheet Equation Check ---
        total_assets = line_items.get("total_assets")
        total_liabilities = line_items.get("total_liabilities")
        total_equity = line_items.get("total_equity")
        total_liab_equity = line_items.get("total_liabilities_and_equity")

        bs_discrepancy = 0.0
        bs_balanced = False

        if total_assets is not None:
            # Check against total liabilities + total equity
            if total_liabilities is not None and total_equity is not None:
                total_checks += 1
                liab_plus_eq = total_liabilities + total_equity
                discrepancy = abs(total_assets - liab_plus_eq)
                pct_diff = discrepancy / max(total_assets, 1.0)

                if discrepancy <= self.tolerance_abs or pct_diff <= self.tolerance_pct:
                    checks_passed += 1
                    bs_balanced = True
                else:
                    errors.append(
                        f"Accounting Equation Mismatch: Total Assets ({total_assets:,.2f}) != "
                        f"Liabilities ({total_liabilities:,.2f}) + Equity ({total_equity:,.2f}) "
                        f"[Discrepancy: {discrepancy:,.2f} ({pct_diff*100:.2f}%)]"
                    )
                bs_discrepancy = discrepancy
            elif total_liab_equity is not None:
                total_checks += 1
                discrepancy = abs(total_assets - total_liab_equity)
                pct_diff = discrepancy / max(total_assets, 1.0)
                if discrepancy <= self.tolerance_abs or pct_diff <= self.tolerance_pct:
                    checks_passed += 1
                    bs_balanced = True
                else:
                    errors.append(
                        f"Balance Sheet Discrepancy: Total Assets ({total_assets:,.2f}) != "
                        f"Total Liabilities & Equity ({total_liab_equity:,.2f}) "
                        f"[Diff: {discrepancy:,.2f}]"
                    )
                bs_discrepancy = discrepancy

        # --- 2. Current Assets <= Total Assets ---
        ca = line_items.get("total_current_assets")
        if ca is not None and total_assets is not None:
            total_checks += 1
            if ca <= total_assets * (1.0 + self.tolerance_pct):
                checks_passed += 1
            else:
                errors.append(f"Current Assets ({ca:,.2f}) exceeds Total Assets ({total_assets:,.2f}).")

        # --- 3. Current Liabilities <= Total Liabilities ---
        cl = line_items.get("total_current_liabilities")
        if cl is not None and total_liabilities is not None:
            total_checks += 1
            if cl <= total_liabilities * (1.0 + self.tolerance_pct):
                checks_passed += 1
            else:
                errors.append(f"Current Liabilities ({cl:,.2f}) exceeds Total Liabilities ({total_liabilities:,.2f}).")

        # --- 4. Income Statement Reconciliation ---
        rev = line_items.get("revenue")
        cogs = line_items.get("cost_of_goods_sold")
        gp = line_items.get("gross_profit")
        if rev is not None and cogs is not None and gp is not None:
            total_checks += 1
            calc_gp = rev - cogs
            if abs(calc_gp - gp) <= max(self.tolerance_abs, gp * self.tolerance_pct):
                checks_passed += 1
            else:
                warnings.append(f"Gross Profit ({gp:,.2f}) differs from Revenue - COGS ({calc_gp:,.2f}).")

        ebit = line_items.get("ebit")
        opex = line_items.get("operating_expenses")
        if gp is not None and opex is not None and ebit is not None:
            total_checks += 1
            calc_ebit = gp - opex
            if abs(calc_ebit - ebit) <= max(self.tolerance_abs, abs(ebit) * self.tolerance_pct):
                checks_passed += 1
            else:
                warnings.append(f"EBIT ({ebit:,.2f}) differs from Gross Profit - OpEx ({calc_ebit:,.2f}).")

        net_inc = line_items.get("net_income")
        interest = line_items.get("interest_expense", 0.0)
        tax = line_items.get("tax_expense", 0.0)
        if ebit is not None and net_inc is not None:
            total_checks += 1
            calc_ni = ebit - interest - tax
            if abs(calc_ni - net_inc) <= max(self.tolerance_abs, abs(net_inc) * self.tolerance_pct):
                checks_passed += 1
            else:
                warnings.append(f"Net Income ({net_inc:,.2f}) differs from EBIT - Interest - Tax ({calc_ni:,.2f}).")

        # Compute Confidence Score
        confidence_score = 100.0 if total_checks == 0 else round((checks_passed / total_checks) * 100, 1)
        if len(errors) > 0:
            confidence_score = max(20.0, confidence_score - (len(errors) * 20.0))

        return {
            "is_valid": len(errors) == 0,
            "accounting_equation_balanced": bs_balanced,
            "discrepancy_amount": round(bs_discrepancy, 2),
            "confidence_score": confidence_score,
            "checks_passed": checks_passed,
            "total_checks": total_checks,
            "errors": errors,
            "warnings": warnings,
            "summary": "Accounting integrity validated successfully." if len(errors) == 0 else f"Found {len(errors)} data reconciliation issues."
        }

accounting_validator = AccountingEquationValidator()
