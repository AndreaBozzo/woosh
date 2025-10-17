from typing import Dict, List
from urllib.parse import urlparse

from ddgs import DDGS

from .classify import classify_url
from .config import EXCLUDED_DOMAINS


def search_companies(query: str, max_results: int = 50) -> Dict[str, List[str]]:
    """Search for companies and categorize the results by domain type."""
    results: dict[str, List[str]] = {}

    try:
        # Initialize the search
        search = DDGS()
        search_results = search.text(query, max_results=max_results)

        # Process each search result
        for result in search_results:
            url = result.get("href", "")

            # Skip excluded domains
            domain: str = urlparse(url).netloc.lower()
            if any(excluded in domain for excluded in EXCLUDED_DOMAINS):
                continue

            # Classify the URL and add to results
            category = classify_url(url)
            if category not in results:
                results[category] = []
            results[category].append(url)

        return results

    except Exception as e:
        print(f"An error occurred during search: {e}")
        # Return empty dict on error to satisfy return type
        return {}
