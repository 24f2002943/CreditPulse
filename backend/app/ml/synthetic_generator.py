import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple
from backend.app.services.macro_adjustment import macro_engine

class SyntheticFinancialGenerator:
    """
    Generates realistic, mathematically coherent synthetic MSME financial statements and ratio profiles.
    Used to augment training datasets for credit risk models in the absence of large proprietary loan default registries.
    """

    def __init__(self, random_seed: int = 42):
        np.random.seed(random_seed)
        self.sectors = [
            "Retail & E-commerce",
            "Textiles & Apparel",
            "Light Manufacturing & Engineering",
            "IT & Software Services",
            "Food Processing & FMCG",
            "Construction & Subcontracting",
            "Pharmaceuticals & Healthcare",
            "Chemicals & Specialty Materials",
            "Automotive Components",
            "Logistics & Freight Services"
        ]

    def generate_company_statement(self, sector: str, health_tier: str = "healthy") -> Dict[str, Any]:
        """
        Generates a coherent single MSME financial statement.
        health_tier: 'healthy' (low risk), 'moderate' (medium risk), 'distressed' (high risk)
        """
        sector_info = macro_engine.get_sector_data(sector) or {}
        med_curr = float(sector_info.get("median_current_ratio", 1.5))
        med_de = float(sector_info.get("median_debt_to_equity", 1.2))
        med_gm = float(sector_info.get("median_gross_margin", 0.25))
        med_nm = float(sector_info.get("median_net_margin", 0.05))

        # Scale revenue: MSME turnover between $200k to $15M
        revenue = np.random.lognormal(mean=14.0, sigma=0.8)

        # Health tier multipliers
        if health_tier == "healthy":
            gm_mult = np.random.uniform(1.05, 1.35)
            nm_mult = np.random.uniform(1.1, 1.6)
            de_mult = np.random.uniform(0.4, 0.9)
            cr_mult = np.random.uniform(1.1, 1.5)
            default_prob = np.random.uniform(0.01, 0.12)
        elif health_tier == "moderate":
            gm_mult = np.random.uniform(0.85, 1.05)
            nm_mult = np.random.uniform(0.7, 1.1)
            de_mult = np.random.uniform(0.9, 1.5)
            cr_mult = np.random.uniform(0.85, 1.15)
            default_prob = np.random.uniform(0.15, 0.40)
        else: # distressed
            gm_mult = np.random.uniform(0.50, 0.85)
            nm_mult = np.random.uniform(-0.5, 0.6)
            de_mult = np.random.uniform(1.6, 3.5)
            cr_mult = np.random.uniform(0.50, 0.85)
            default_prob = np.random.uniform(0.55, 0.95)

        gross_margin = max(0.05, min(0.65, med_gm * gm_mult))
        net_margin = max(-0.20, min(0.30, med_nm * nm_mult))
        cogs = revenue * (1.0 - gross_margin)
        gross_profit = revenue - cogs

        opex_pct = gross_margin - (net_margin * 1.3)
        operating_expenses = revenue * max(0.05, opex_pct)
        ebit = gross_profit - operating_expenses

        # Asset base (Asset turnover around 1.2 to 2.2)
        total_assets = revenue / np.random.uniform(1.1, 2.3)
        current_assets_pct = np.random.uniform(0.50, 0.75)
        total_current_assets = total_assets * current_assets_pct
        fixed_assets = total_assets - total_current_assets

        # Working capital components
        inventory = total_current_assets * np.random.uniform(0.25, 0.45)
        accounts_receivable = total_current_assets * np.random.uniform(0.30, 0.50)
        cash = total_current_assets - inventory - accounts_receivable
        if cash < 0:
            cash = total_current_assets * 0.10
            inventory = (total_current_assets - cash) * 0.45
            accounts_receivable = total_current_assets - cash - inventory

        # Liabilities and Equity
        target_cr = max(0.6, med_curr * cr_mult)
        total_current_liabilities = total_current_assets / target_cr
        accounts_payable = total_current_liabilities * np.random.uniform(0.4, 0.7)
        short_term_debt = total_current_liabilities - accounts_payable

        # Debt to equity structuring
        target_de = max(0.3, med_de * de_mult)
        total_equity = max(10000.0, total_assets / (1.0 + target_de))
        total_liabilities = max(0.0, total_assets - total_equity)
        long_term_debt = max(0.0, total_liabilities - total_current_liabilities)
        if long_term_debt < 0:
            long_term_debt = 0.0
            total_current_liabilities = total_liabilities
            total_equity = total_assets - total_liabilities

        # Interest and Net Income
        interest_rate = np.random.uniform(0.07, 0.14)
        interest_expense = (short_term_debt + long_term_debt) * interest_rate
        ebt = ebit - interest_expense
        tax_expense = max(0.0, ebt * 0.25)
        net_income = ebt - tax_expense

        # Simulated default label
        defaulted = 1 if np.random.rand() < default_prob else 0

        return {
            "sector": sector,
            "health_tier": health_tier,
            "revenue": round(revenue, 2),
            "cost_of_goods_sold": round(cogs, 2),
            "gross_profit": round(gross_profit, 2),
            "operating_expenses": round(operating_expenses, 2),
            "ebit": round(ebit, 2),
            "interest_expense": round(interest_expense, 2),
            "tax_expense": round(tax_expense, 2),
            "net_income": round(net_income, 2),
            "total_assets": round(total_assets, 2),
            "total_current_assets": round(total_current_assets, 2),
            "property_plant_equipment": round(fixed_assets, 2),
            "cash_and_equivalents": round(cash, 2),
            "inventory": round(inventory, 2),
            "accounts_receivable": round(accounts_receivable, 2),
            "total_liabilities": round(total_liabilities, 2),
            "total_current_liabilities": round(total_current_liabilities, 2),
            "accounts_payable": round(accounts_payable, 2),
            "short_term_debt": round(short_term_debt, 2),
            "long_term_debt": round(long_term_debt, 2),
            "total_equity": round(total_equity, 2),
            "default_probability": round(default_prob, 3),
            "defaulted": defaulted
        }

    def generate_synthetic_dataset(self, n_samples: int = 1500) -> pd.DataFrame:
        """
        Generates a balanced synthetic dataset across sectors and health tiers.
        """
        records: List[Dict[str, Any]] = []
        tiers = ["healthy", "moderate", "distressed"]
        tier_weights = [0.55, 0.30, 0.15]

        for _ in range(n_samples):
            sector = np.random.choice(self.sectors)
            health = np.random.choice(tiers, p=tier_weights)
            stmt = self.generate_company_statement(sector, health)
            records.append(stmt)

        return pd.DataFrame(records)

synthetic_generator = SyntheticFinancialGenerator()
