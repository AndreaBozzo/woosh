"""VAT validation + web search."""

from .models import CompanyData, VATInfo
from .search import search_companies
from .vies import validate_vat_number


def lookup_vat(vat_input: str) -> CompanyData:
    """Validate VAT and search URLs.

    Args:
        vat_input: VAT number (e.g., 'IT12345678901')

    Returns:
        CompanyData with VAT info + URLs found
    """
    # Validate VAT
    vat_data = validate_vat_number(vat_input)

    vat_info = VATInfo(
        country_code=vat_data.country_code,
        vat_number=vat_data.vat_number,
        is_valid=vat_data.valid,
        company_name=vat_data.name,
        company_address=vat_data.address,
    )

    # Search URLs using company name
    query = vat_data.name if vat_data.valid and vat_data.name else vat_input
    if "Error:" in (query or ""):
        query = vat_input

    urls = search_companies(query)

    return CompanyData(vat=vat_info, urls=urls)
