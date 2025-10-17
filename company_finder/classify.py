from urllib.parse import urlparse

from .config import CATEGORY_RULES


def classify_url(url: str) -> str:
    """Classify a URL into a category based on predefined rules."""
    domain = urlparse(url).netloc.lower()
    for category, keywords in CATEGORY_RULES.items():
        if any(keyword in domain for keyword in keywords):
            return category
    return "altro"  # Default category if no match found
