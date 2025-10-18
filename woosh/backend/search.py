import logging
from collections import defaultdict
from functools import lru_cache
from typing import Dict, List
from urllib.parse import urlparse

from classify import classify_url
from config import EXCLUDED, RULES
from ddgs import DDGS

logger = logging.getLogger(__name__)


def _get_base_domain(domain: str) -> str:
    """Extract base domain, removing subdomains like www, m, mobile."""
    parts = domain.split(".")
    if len(parts) > 2 and parts[0] in ("www", "m", "mobile", "en", "it"):
        return ".".join(parts[1:])
    return domain


def _get_priority(url: str, category: str) -> int:
    """Get priority score for a URL based on its category rules."""
    domain = urlparse(url).netloc.lower()
    if category in RULES:
        for rule in RULES[category]:
            if rule.matches(domain):
                return rule.priority
    return 0


@lru_cache(maxsize=128)
def search_companies(
    query: str, max_results: int = 100, timeout: int = 10, top_per_category: int = 5
) -> Dict[str, List[str]]:
    """Search for companies and categorize the results by domain type.

    Args:
        query: Search query string
        max_results: Maximum number of results to process
        timeout: Timeout in seconds for the search
        top_per_category: Maximum results to return per category (ranked by priority)

    Returns:
        Dictionary mapping categories to lists of URLs (sorted by priority)
    """
    if not query or not query.strip():
        logger.warning("Empty query provided")
        return {}

    results: Dict[str, List[tuple[str, int]]] = defaultdict(list)
    seen_domains: set[str] = set()

    try:
        with DDGS(timeout=timeout) as search:
            search_results = search.text(query, max_results=max_results)

            for result in search_results:
                url = result.get("href", "")
                if not url:
                    continue

                try:
                    parsed_url = urlparse(url)
                    domain = parsed_url.netloc.lower()

                    # Skip excluded domains
                    if any(excluded.matches(domain) for excluded in EXCLUDED):
                        continue

                    # Deduplicate by base domain
                    base_domain = _get_base_domain(domain)
                    if base_domain in seen_domains:
                        continue
                    seen_domains.add(base_domain)

                    # Classify and score
                    category = classify_url(url)
                    priority = _get_priority(url, category)
                    results[category].append((url, priority))

                except Exception as e:
                    logger.debug(f"Error processing URL {url}: {e}")
                    continue

        # Sort by priority and limit per category
        ranked_results = {}
        for category, urls in results.items():
            sorted_urls = sorted(urls, key=lambda x: x[1], reverse=True)
            ranked_results[category] = [
                url for url, _ in sorted_urls[:top_per_category]
            ]

        total = sum(len(urls) for urls in ranked_results.values())
        logger.info(f"Found {total} results across {len(ranked_results)} categories")
        return ranked_results

    except Exception as e:
        logger.error(f"Search failed for query '{query}': {e}")
        return {}
