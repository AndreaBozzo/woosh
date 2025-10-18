from typing import Any, Optional

from woosh.search import search_companies


class MockDDGS:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_value: Optional[Exception],
        exc_tb: Optional[Any],
    ) -> None:
        pass

    def text(self, query: str, max_results: int = 10):
        company_slug = query.lower().replace(" ", "-")
        return [
            {"href": f"https://www.linkedin.com/company/{company_slug}"},
            {"href": f"https://agenziadelleentrate.gov.it/azienda/{company_slug}"},
            {"href": f"https://www.amazon.it/dp/{company_slug}"},
            {"href": f"https://www.medium.com/@{company_slug}"},
        ]


def test_search_companies(monkeypatch: Any) -> None:
    # Patch DDGS to use the mock class
    monkeypatch.setattr("company_finder.search.DDGS", MockDDGS)

    query = "Coca Cola"
    results = search_companies(query, max_results=10)

    expected_results = {
        "social": ["https://www.linkedin.com/company/coca-cola"],
        "istituzionali": ["https://agenziadelleentrate.gov.it/azienda/coca-cola"],
        "e-commerce": ["https://www.amazon.it/dp/coca-cola"],
        "altro": ["https://www.medium.com/@coca-cola"],
    }
    assert results == expected_results
