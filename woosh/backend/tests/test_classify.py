import pytest

from classify import classify_url


@pytest.mark.parametrize(
    "url, expected_category",
    [
        ("https://www.linkedin.com/company/example", "social"),
        ("https://agenziadelleentrate.gov.it/azienda/example", "istituzionali"),
        ("https://www.amazon.it/dp/example", "e-commerce"),
        ("https://www.medium.com/@example", "altro"),
    ],
)
def test_classify_url(url, expected_category):
    assert classify_url(url) == expected_category


def test_classify_url_no_match():
    url = "https://www.unknownsite.com"
    expected_category = "altro"
    assert classify_url(url) == expected_category


def test_classify_is_case_insensitive():
    url = "HTTPS://WWW.LINKEDIN.COM/COMPANY/EXAMPLE"
    expected_category = "social"
    assert classify_url(url) == expected_category


def tst_classify_url_partial_match():
    url = "https://subdomain.linkedin.com/company/example"
    expected_category = "social"
    assert classify_url(url) == expected_category


def test_classify_url_empty():
    url = ""
    expected_category = "altro"
    assert classify_url(url) == expected_category


def test_classify_url_no_netloc():
    url = "not a valid url"
    expected_category = "altro"
    assert classify_url(url) == expected_category


def test_classify_handles_special_characters():
    url = "https://www.linkedin.com/company/example?ref=home"
    expected_category = "social"
    assert classify_url(url) == expected_category
