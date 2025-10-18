from urllib.parse import urlparse

from .config import RULES


def classify_url(url: str) -> str:
    """Classify a URL into a category based on predefined rules."""
    domain = urlparse(url).netloc.lower()
    for category, rules in RULES.items():
        if any(rule.matches(domain) for rule in rules):
            return category
    return "altro"  # Default category if no match found
