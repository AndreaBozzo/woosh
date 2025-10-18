"""VIES (VAT Information Exchange System) integration for EU VAT validation."""

from dataclasses import dataclass
from typing import Optional

from zeep import Client
from zeep.exceptions import Fault


@dataclass
class VATInfo:
    """VAT information returned from VIES service."""

    country_code: str
    vat_number: str
    valid: bool
    name: Optional[str] = None
    address: Optional[str] = None
    request_date: Optional[str] = None


class VIESClient:
    """Client for interacting with the VIES SOAP service."""

    VIES_WSDL_URL = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"

    def __init__(self):
        """Initialize the VIES SOAP client."""
        self.client = Client(self.VIES_WSDL_URL)

    def validate_vat(self, country_code: str, vat_number: str) -> VATInfo:
        """
        Validate a VAT number using the VIES service.

        Args:
            country_code: Two-letter country code (e.g., 'IT', 'DE', 'FR')
            vat_number: VAT number without country code prefix

        Returns:
            VATInfo object with validation results

        Raises:
            Fault: If the VIES service returns an error
            Exception: For other network or parsing errors
        """
        try:
            # Clean VAT number (remove spaces, country code if present)
            clean_vat = vat_number.strip().upper()
            clean_country = country_code.strip().upper()

            # Remove country code from VAT number if present
            if clean_vat.startswith(clean_country):
                clean_vat = clean_vat[len(clean_country) :]

            # Call VIES service
            result = self.client.service.checkVat(clean_country, clean_vat)

            return VATInfo(
                country_code=result.countryCode,
                vat_number=result.vatNumber,
                valid=result.valid,
                name=result.name if hasattr(result, "name") else None,
                address=result.address if hasattr(result, "address") else None,
                request_date=(
                    str(result.requestDate) if hasattr(result, "requestDate") else None
                ),
            )

        except Fault as e:
            # VIES service error (invalid format, service unavailable, etc.)
            return VATInfo(
                country_code=country_code,
                vat_number=vat_number,
                valid=False,
                name=f"VIES Error: {str(e)}",
            )
        except Exception as e:
            # Network or other errors
            return VATInfo(
                country_code=country_code,
                vat_number=vat_number,
                valid=False,
                name=f"Error: {str(e)}",
            )


def parse_vat_input(vat_input: str) -> tuple[str, str]:
    """
    Parse VAT input and extract country code and number.

    Args:
        vat_input: VAT number with or without country code (e.g., 'IT12345678901' or '12345678901')

    Returns:
        Tuple of (country_code, vat_number)

    Examples:
        >>> parse_vat_input('IT12345678901')
        ('IT', '12345678901')
        >>> parse_vat_input('12345678901')
        ('IT', '12345678901')  # Defaults to IT if no country code
    """
    vat_clean = vat_input.strip().upper().replace(" ", "")

    # Check if starts with 2-letter country code
    if len(vat_clean) >= 2 and vat_clean[:2].isalpha():
        country_code = vat_clean[:2]
        vat_number = vat_clean[2:].strip()
    else:
        # Default to IT (Italy) if no country code provided
        country_code = "IT"
        vat_number = vat_clean.strip()

    return country_code, vat_number


def validate_vat_number(vat_input: str) -> VATInfo:
    """
    Convenience function to validate a VAT number.

    Args:
        vat_input: VAT number with or without country code

    Returns:
        VATInfo object with validation results
    """
    country_code, vat_number = parse_vat_input(vat_input)
    client = VIESClient()
    return client.validate_vat(country_code, vat_number)
