"""VIES (VAT Information Exchange System) integration for EU VAT validation."""

from typing import Any, Optional

from pydantic import BaseModel
from zeep import Client
from zeep.exceptions import Fault


class VATInfo(BaseModel):
    """VAT validation result."""

    country_code: str
    vat_number: str
    is_valid: bool
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    request_date: Optional[str] = None
    error_message: Optional[str] = None


class _VIESClient:
    """Internal SOAP client for VIES service (not meant for direct use)."""

    VIES_WSDL_URL = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"

    def __init__(self):
        """Initialize the VIES SOAP client."""
        self.client = Client(self.VIES_WSDL_URL)

    def _call_service(self, country_code: str, vat_number: str) -> VATInfo:
        """
        Internal method: Call VIES service with pre-cleaned inputs.

        Args:
            country_code: Two-letter country code (uppercase)
            vat_number: VAT number without country code (uppercase, no spaces)

        Returns:
            VATInfo object with validation results
        """
        try:
            # Call VIES service directly with cleaned inputs
            response: Any = self.client.service.checkVat(
                countryCode=country_code, vatNumber=vat_number
            )

            # Extract data from SOAP response (zeep returns dynamic objects)
            # Response attributes: requestDate (datetime), valid (bool), name (str), address (str)
            request_date: str = response.requestDate.isoformat()  # type: ignore[attr-defined]
            is_valid: bool = response.valid  # type: ignore[attr-defined]
            company_name: Optional[str] = response.name or None  # type: ignore[attr-defined]
            company_address: Optional[str] = response.address or None  # type: ignore[attr-defined]

            return VATInfo(
                country_code=country_code,
                vat_number=vat_number,
                is_valid=is_valid,
                company_name=company_name,
                company_address=company_address,
                request_date=request_date,
                error_message=None,
            )
        except Fault as e:
            return VATInfo(
                country_code=country_code,
                vat_number=vat_number,
                is_valid=False,
                error_message=f"VIES Error: {str(e)}",
            )
        except (OSError, ConnectionError, TimeoutError) as e:
            return VATInfo(
                country_code=country_code,
                vat_number=vat_number,
                is_valid=False,
                error_message=f"Connection Error: {str(e)}",
            )


def parse_vat_input(vat_input: str, default_country: str = "IT") -> tuple[str, str]:
    """
    Parse VAT input and extract country code and number.

    Args:
        vat_input: VAT number with or without country code (e.g., 'IT12345678901' or '12345678901')
        default_country: Default country code if not specified (default: 'IT')

    Returns:
        Tuple of (country_code, vat_number)

    Examples:
        >>> parse_vat_input('IT12345678901')
        ('IT', '12345678901')
        >>> parse_vat_input('12345678901')
        ('IT', '12345678901')
        >>> parse_vat_input('12345678901', 'DE')
        ('DE', '12345678901')
    """
    vat_clean = vat_input.strip().upper().replace(" ", "")

    # Check if starts with 2-letter country code
    if len(vat_clean) >= 2 and vat_clean[:2].isalpha():
        country_code = vat_clean[:2]
        vat_number = vat_clean[2:]
    else:
        country_code = default_country.upper()
        vat_number = vat_clean

    return country_code, vat_number


# Global client instance for efficiency (reuse SOAP connection)
_vies_client: Optional[_VIESClient] = None


def _get_client() -> _VIESClient:
    """Get or create singleton VIES client instance."""
    global _vies_client
    if _vies_client is None:
        _vies_client = _VIESClient()
    return _vies_client


def validate_vat(vat_input: str, default_country: str = "IT") -> VATInfo:
    """
    Validate a VAT number using the VIES service.

    Args:
        vat_input: VAT number with or without country code (e.g., 'IT12345678901' or '12345678901')
        default_country: Default country code if not specified in input (default: 'IT')

    Returns:
        VATInfo object with validation results

    Example:
        >>> result = validate_vat("IT12345678901")
        >>> if result.is_valid:
        ...     print(f"Company: {result.company_name}")
        ... else:
        ...     print(f"Error: {result.error_message}")
    """
    country_code, vat_number = parse_vat_input(vat_input, default_country)
    client = _get_client()
    return client._call_service(country_code, vat_number)
