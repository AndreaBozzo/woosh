from typing import Dict, List
from urllib.parse import ParseResult, urlparse

from classify import classify_url
from config import EXCLUDED
from ddgs import DDGS


def search_companies(query: str, max_results: int = 100) -> Dict[str, List[str]]:
    """Search for companies and categorize the results by domain type."""
    results: Dict[str, List[str]] = {}

    try:
        # Initialize the search
        with DDGS() as search:
            search_results = search.text(query, max_results=max_results)

            # Process each search result
            for result in search_results:
                url = result.get("href", "")

                if not url:
                    continue

                # Skip excluded domains
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.lower()

                if any(excluded.matches(domain) for excluded in EXCLUDED):
                    continue

                # Classify the URL and add to results
                category = classify_url(url)
                if category not in results:
                    results[category] = []
                results[category].append(url)

        return results

    except Exception:
        return {}
