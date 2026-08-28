import os
import re
from typing import Dict, Any, List, Optional
from pypdf import PdfReader
from backend.app.services.excel_parser import CANONICAL_KEYS, excel_parser
from backend.app.services.accounting_validator import accounting_validator

class OCRStatementPipeline:
    """
    Ingests scanned or digital PDF / image financial statements.
    Extracts text line items, maps them to canonical schema, and executes accounting reconciliation.
    """

    def parse_pdf(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        reader = PdfReader(file_path)
        extracted_text = ""
        for page_idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            extracted_text += f"\n--- Page {page_idx + 1} ---\n" + page_text

        return self.parse_raw_text(extracted_text, file_source=os.path.basename(file_path))

    def parse_raw_text(self, text: str, file_source: str = "document") -> Dict[str, Any]:
        lines = text.split("\n")
        extracted_items: Dict[str, float] = {}
        fiscal_year = 2024

        for line in lines:
            line_str = line.strip()
            if not line_str or len(line_str) < 3:
                continue

            # Year extraction heuristic
            match_yr = re.search(r"\b(20[1-2][0-9]|FY\s?[1-2][0-9])\b", line_str, re.IGNORECASE)
            if match_yr:
                try:
                    yr_val = match_yr.group(0).upper().replace("FY", "").strip()
                    if len(yr_val) == 2:
                        fiscal_year = 2000 + int(yr_val)
                    elif len(yr_val) == 4:
                        fiscal_year = int(yr_val)
                except Exception:
                    pass

            # Check for canonical key
            matched_key = excel_parser.match_canonical_key(line_str)
            if matched_key:
                # Extract all numbers from line
                # Look for numbers with commas or decimals or parentheses e.g. 1,450.50 or (250.00)
                nums = re.findall(r"\(?\s*[\$₹]?\s*\d+(?:,\d{3})*(?:\.\d+)?\s*\)?", line_str)
                if nums:
                    # Choose the last number on the line as the financial figure
                    val = excel_parser.parse_number(nums[-1])
                    if val is not None:
                        extracted_items[matched_key] = val

        # Impute missing totals if possible
        excel_parser._impute_missing_totals(extracted_items)

        # Validate with accounting equation validator
        validation_report = accounting_validator.validate(extracted_items)

        return {
            "fiscal_year": fiscal_year,
            "line_items": extracted_items,
            "validation": validation_report,
            "raw_text_length": len(text),
            "file_source": file_source
        }

ocr_pipeline = OCRStatementPipeline()
