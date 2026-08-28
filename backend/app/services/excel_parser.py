import os
import re
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple

# Canonical Line Item Mappings with Synonyms
CANONICAL_KEYS = {
    # Balance Sheet - Assets
    "cash_and_equivalents": ["cash", "cash and equivalents", "bank balances", "cash & bank", "cash in hand", "liquid funds"],
    "marketable_securities": ["marketable securities", "short term investments", "current investments"],
    "accounts_receivable": ["accounts receivable", "trade receivables", "debtors", "sundry debtors", "bills receivable", "receivables"],
    "inventory": ["inventory", "inventories", "stock in trade", "raw materials", "finished goods", "work in progress", "stock"],
    "prepaid_expenses": ["prepaid expenses", "prepayments", "advances to suppliers", "other current assets"],
    "total_current_assets": ["total current assets", "current assets", "total ca"],
    "property_plant_equipment": ["property plant and equipment", "ppe", "fixed assets", "tangible assets", "gross block", "net block", "plant and machinery"],
    "intangible_assets": ["intangible assets", "goodwill", "patents", "trademarks"],
    "total_non_current_assets": ["total non current assets", "non current assets", "fixed assets total", "other non current assets"],
    "total_assets": ["total assets", "total assets & liabilities", "total application of funds", "balance sheet total"],

    # Balance Sheet - Liabilities & Equity
    "accounts_payable": ["accounts payable", "trade payables", "creditors", "sundry creditors", "bills payable", "payables"],
    "short_term_debt": ["short term debt", "short term borrowings", "bank overdraft", "cash credit", "working capital loan", "current portion of lt debt"],
    "accrued_expenses": ["accrued expenses", "other current liabilities", "provisions", "accrued liabilities"],
    "total_current_liabilities": ["total current liabilities", "current liabilities", "total cl"],
    "long_term_debt": ["long term debt", "long term borrowings", "term loans", "secured loans", "unsecured loans", "non current debt"],
    "total_non_current_liabilities": ["total non current liabilities", "non current liabilities", "long term liabilities"],
    "total_liabilities": ["total liabilities", "total debt and liabilities"],
    "share_capital": ["share capital", "equity share capital", "paid up capital", "common stock", "owner capital"],
    "retained_earnings": ["retained earnings", "reserves and surplus", "accumulated profits", "surplus"],
    "total_equity": ["total equity", "shareholders equity", "total net worth", "net worth", "owner equity", "stockholders equity"],
    "total_liabilities_and_equity": ["total liabilities and equity", "total equity and liabilities", "total sources of funds"],

    # Income Statement
    "revenue": ["revenue", "sales", "gross sales", "net sales", "turnover", "total revenue", "revenue from operations"],
    "cost_of_goods_sold": ["cost of goods sold", "cogs", "cost of sales", "material cost", "raw material consumed", "direct expenses", "cost of materials"],
    "gross_profit": ["gross profit", "gross margin amount", "gross income"],
    "operating_expenses": ["operating expenses", "opex", "selling general and admin", "sg&a", "administrative expenses", "overhead costs", "employee expenses"],
    "ebitda": ["ebitda", "operating profit before depreciation", "operating income before da"],
    "depreciation_amortization": ["depreciation", "depreciation and amortization", "d&a", "depreciation & amortisation"],
    "ebit": ["ebit", "operating profit", "operating income", "profit before interest and tax", "pbit"],
    "interest_expense": ["interest", "interest expense", "finance costs", "finance charges", "borrowing costs"],
    "tax_expense": ["tax", "income tax", "provision for tax", "taxes"],
    "net_income": ["net income", "net profit", "pat", "profit after tax", "net profit after tax", "bottom line"]
}

class ExcelFinancialParser:
    """
    Parses Excel (.xlsx/.xls) and CSV financial statements for MSMEs.
    Extracts line items, normalizes terminology, and standardizes multi-year financial statements.
    """

    def clean_text(self, text: Any) -> str:
        if not isinstance(text, str):
            text = str(text)
        return re.sub(r"[^a-zA-Z0-9\s]", " ", text).lower().strip()

    def parse_number(self, val: Any) -> Optional[float]:
        if pd.isna(val) or val is None:
            return None
        if isinstance(val, (int, float)):
            return float(val)
        val_str = str(val).replace("$", "").replace("₹", "").replace(",", "").strip()
        # Handle parenthesized negative numbers e.g. (500) -> -500
        if val_str.startswith("(") and val_str.endswith(")"):
            val_str = "-" + val_str[1:-1]
        try:
            return float(val_str)
        except ValueError:
            return None

    def match_canonical_key(self, line_text: str) -> Optional[str]:
        cleaned = self.clean_text(line_text)
        if not cleaned:
            return None
            
        for canon_key, synonyms in CANONICAL_KEYS.items():
            for syn in synonyms:
                if syn in cleaned:
                    return canon_key
        return None

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parses financial statement from spreadsheet and returns normalized dictionary of line items.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")

        # Read sheet or CSV
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path, header=None)
        else:
            # Excel file - read all sheets and combine or read active sheet
            excel = pd.ExcelFile(file_path)
            sheets_data = {}
            for sheet_name in excel.sheet_names:
                sheets_data[sheet_name] = pd.read_excel(excel, sheet_name=sheet_name, header=None)
            # Combine or take first sheet
            df = sheets_data[excel.sheet_names[0]]

        extracted_items: Dict[str, float] = {}
        fiscal_year = 2024

        # Iterate rows to find line items and numeric columns
        for _, row in df.iterrows():
            row_items = [str(x).strip() for x in row if pd.notna(x) and str(x).strip() != ""]
            if not row_items:
                continue

            # Look for fiscal year in header row
            for item in row_items:
                match_yr = re.search(r"\b(20[1-2][0-9]|FY\s?[1-2][0-9])\b", str(item), re.IGNORECASE)
                if match_yr:
                    try:
                        yr_str = match_yr.group(0).upper().replace("FY", "").strip()
                        if len(yr_str) == 2:
                            fiscal_year = 2000 + int(yr_str)
                        elif len(yr_str) == 4:
                            fiscal_year = int(yr_str)
                    except Exception:
                        pass

            # Detect line item text in the first 1-2 text columns
            line_label = row_items[0]
            matched_key = self.match_canonical_key(line_label)
            if not matched_key and len(row_items) > 1 and not any(char.isdigit() for char in row_items[1]):
                line_label += " " + row_items[1]
                matched_key = self.match_canonical_key(line_label)

            if matched_key:
                # Find the corresponding numerical value (search from right to left or next column)
                for cell in reversed(row):
                    num = self.parse_number(cell)
                    if num is not None:
                        extracted_items[matched_key] = num
                        break

        # Calculate implied / missing fields if necessary
        self._impute_missing_totals(extracted_items)

        return {
            "fiscal_year": fiscal_year,
            "line_items": extracted_items,
            "raw_items_count": len(extracted_items),
            "file_source": os.path.basename(file_path)
        }

    def _impute_missing_totals(self, items: Dict[str, float]):
        # Impute Total Current Assets
        if "total_current_assets" not in items:
            ca_components = ["cash_and_equivalents", "marketable_securities", "accounts_receivable", "inventory", "prepaid_expenses"]
            ca_sum = sum(items[k] for k in ca_components if k in items)
            if ca_sum > 0:
                items["total_current_assets"] = ca_sum

        # Impute Total Assets
        if "total_assets" not in items:
            ca = items.get("total_current_assets", 0.0)
            nca = items.get("total_non_current_assets", items.get("property_plant_equipment", 0.0) + items.get("intangible_assets", 0.0))
            if ca + nca > 0:
                items["total_assets"] = ca + nca

        # Impute Total Current Liabilities
        if "total_current_liabilities" not in items:
            cl_components = ["accounts_payable", "short_term_debt", "accrued_expenses"]
            cl_sum = sum(items[k] for k in cl_components if k in items)
            if cl_sum > 0:
                items["total_current_liabilities"] = cl_sum

        # Impute Total Equity
        if "total_equity" not in items:
            eq_components = ["share_capital", "retained_earnings"]
            eq_sum = sum(items[k] for k in eq_components if k in items)
            if eq_sum > 0:
                items["total_equity"] = eq_sum

        # Impute Gross Profit
        if "gross_profit" not in items and "revenue" in items and "cost_of_goods_sold" in items:
            items["gross_profit"] = items["revenue"] - items["cost_of_goods_sold"]

        # Impute EBIT / Operating Income
        if "ebit" not in items:
            if "gross_profit" in items and "operating_expenses" in items:
                items["ebit"] = items["gross_profit"] - items["operating_expenses"]
            elif "revenue" in items and "cost_of_goods_sold" in items and "operating_expenses" in items:
                items["ebit"] = items["revenue"] - items["cost_of_goods_sold"] - items["operating_expenses"]

        # Impute Net Income
        if "net_income" not in items and "ebit" in items:
            interest = items.get("interest_expense", 0.0)
            tax = items.get("tax_expense", 0.0)
            items["net_income"] = items["ebit"] - interest - tax

excel_parser = ExcelFinancialParser()
