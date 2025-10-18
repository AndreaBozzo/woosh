"""Data models."""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class VATInfo(BaseModel):
    """VAT validation result."""

    country_code: str
    vat_number: str
    is_valid: bool
    company_name: Optional[str] = None
    company_address: Optional[str] = None


class CompanyData(BaseModel):
    """Company data: VAT + URLs."""

    vat: VATInfo
    urls: Dict[str, List[str]]  # category -> list of URLs
    timestamp: datetime = Field(default_factory=datetime.now)
