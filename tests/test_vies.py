"""Tests for VIES VAT validation module."""

import pytest

from woosh.backend.vies import parse_vat_input


class TestParseVatInput:
    """Tests for VAT input parsing."""

    def test_parse_vat_with_country_code(self):
        """Test parsing VAT with country code."""
        country, vat = parse_vat_input("IT12345678901")
        assert country == "IT"
        assert vat == "12345678901"

    def test_parse_vat_without_country_code(self):
        """Test parsing VAT without country code (defaults to IT)."""
        country, vat = parse_vat_input("12345678901")
        assert country == "IT"
        assert vat == "12345678901"

    def test_parse_vat_lowercase(self):
        """Test parsing converts to uppercase."""
        country, vat = parse_vat_input("it12345678901")
        assert country == "IT"
        assert vat == "12345678901"

    def test_parse_vat_with_spaces(self):
        """Test parsing handles spaces."""
        country, vat = parse_vat_input("  IT 12345678901  ")
        assert country == "IT"
        assert vat == "12345678901"

    def test_parse_vat_different_countries(self):
        """Test parsing different EU country codes."""
        test_cases = [
            ("DE123456789", "DE", "123456789"),
            ("FR12345678901", "FR", "12345678901"),
            ("ES12345678", "ES", "12345678"),
        ]

        for vat_input, expected_country, expected_vat in test_cases:
            country, vat = parse_vat_input(vat_input)
            assert country == expected_country
            assert vat == expected_vat
