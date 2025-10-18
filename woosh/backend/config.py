"""
Configuration for company finder - simple, powerful, no BS.
"""

import re
from dataclasses import dataclass
from typing import Pattern

# =============================================================================
# PATTERN MATCHING
# =============================================================================


@dataclass
class Rule:
    """Simple pattern rule with regex support."""

    pattern: str
    is_regex: bool = False
    priority: int = 0
    _compiled: Pattern[str] | None = None

    def __post_init__(self):
        if self.is_regex:
            self._compiled = re.compile(self.pattern, re.IGNORECASE)

    def matches(self, domain: str) -> bool:
        if self._compiled:
            return bool(self._compiled.search(domain.lower()))
        return self.pattern.lower() in domain.lower()


# =============================================================================
# CATEGORIES - organized by priority
# =============================================================================

RULES = {
    # Priority 10 - Institutional
    "istituzionali": [
        Rule(r"\.gov\.(it|uk|fr|de)$", is_regex=True, priority=10),
        Rule("europa.eu", priority=10),
        Rule("camera.it", priority=10),
        Rule("inps.it", priority=9),
        Rule("gazzettaufficiale.it", priority=9),
        Rule("consob.it", priority=9),
        Rule("bancaditalia.it", priority=9),
        Rule("istat.it", priority=9),
        Rule("agid.gov.it", priority=9),
        Rule("agenziadelleentrate.gov.it", priority=10),
        Rule("registroimprese.it", priority=10),
        Rule("camcom.gov.it", priority=10),
        Rule("chamberofcommerce.com", priority=9),
        Rule("unioncamere.gov.it", priority=9),
    ],
    # Priority 9 - Open Data & Registries
    "open_data": [
        Rule("opencorporates.com", priority=10),
        Rule("registroimprese.it", priority=10),
        Rule("dati.gov.it", priority=10),
        Rule("data.gov", priority=9),
        Rule("data.gov.uk", priority=9),
        Rule("data.gov.it", priority=9),
        Rule("companieshouse.gov.uk", priority=10),
        Rule("data.gov.au", priority=9),
        Rule("data.gov.nz", priority=9),
    ],
    # Priority 8 - Finance
    "finance": [
        Rule("bloomberg.com", priority=10),
        Rule("reuters.com", priority=10),
        Rule("ft.com", priority=10),
        Rule("wsj.com", priority=10),
        Rule("morningstar.com", priority=9),
        Rule("yahoo.com/finance", priority=9),
        Rule("marketwatch.com", priority=9),
        Rule("cnbc.com", priority=9),
        Rule("investing.com", priority=9),
        Rule("sec.gov", priority=10),
    ],
    # Priority 7 - Fintech & Blockchain
    "fintech": [
        Rule("finextra.com", priority=10),
        Rule("stripe.com", priority=9),
        Rule("squareup.com", priority=9),
        Rule("paypal.com", priority=9),
        Rule("adyen.com", priority=8),
        Rule("klarna.com", priority=8),
        Rule("revolut.com", priority=8),
        Rule("wise.com", priority=8),
    ],
    "blockchain": [
        Rule("coindesk.com", priority=10),
        Rule("theblock.co", priority=10),
        Rule("decrypt.co", priority=10),
        Rule("cointelegraph.com", priority=9),
        Rule("etherscan.io", priority=9),
        Rule("bscscan.com", priority=9),
        Rule("blockchair.com", priority=8),
        Rule("blockcypher.com", priority=8),
    ],
    # Priority 6 - Social & E-commerce
    "social": [
        Rule("linkedin.com", priority=10),
        Rule("facebook.com", priority=10),
        Rule("instagram.com", priority=10),
        Rule(r"^x\.com$", is_regex=True, priority=10),
        Rule("twitter.com", priority=10),
        Rule("youtube.com", priority=9),
        Rule("pinterest.com", priority=8),
        Rule("tiktok.com", priority=8),
        Rule("reddit.com", priority=7),
    ],
    "e-commerce": [
        Rule(r"amazon\.(it|com|de|fr|es|co\.uk)", is_regex=True, priority=10),
        Rule(r"ebay\.(it|com)", is_regex=True, priority=10),
        Rule("etsy.com", priority=9),
        Rule("shopify.com", priority=8),
        Rule("alibaba.com", priority=9),
        Rule("zalando.it", priority=8),
        Rule("mercadolibre.com", priority=8),
        Rule("wish.com", priority=7),
    ],
    # Priority 5 - News & Tech
    "news": [
        Rule("ansa.it", priority=10),
        Rule("repubblica.it", priority=10),
        Rule("corriere.it", priority=10),
        Rule("ilsole24ore.com", priority=10),
        Rule("bbc.com", priority=9),
        Rule("cnn.com", priority=9),
        Rule("theguardian.com", priority=9),
        Rule("nytimes.com", priority=9),
        Rule("theverge.com", priority=8),
        Rule("techcrunch.com", priority=8),
        Rule("wired.com", priority=8),
        Rule("Wired.it", priority=8),
    ],
    "startup": [
        Rule("startupitalia.eu", priority=10),
        Rule("techcrunch.com", priority=8),
        Rule("venturebeat.com", priority=8),
        Rule("thenextweb.com", priority=8),
        Rule("angel.co", priority=7),
        Rule("seedrs.com", priority=7),
    ],
    "ai": [
        Rule("openai.com", priority=10),
        Rule("huggingface.co", priority=9),
        Rule("anthropic.com", priority=9),
        Rule("deepmind.com", priority=9),
        Rule("google.com", priority=8),
        Rule("microsoft.com", priority=8),
        Rule("ibm.com", priority=8),
    ],
    "cybersecurity": [
        Rule("krebsonsecurity.com", priority=10),
        Rule("bleepingcomputer.com", priority=9),
        Rule("thehackernews.com", priority=9),
        Rule("cyberscoop.com", priority=8),
        Rule("darkreading.com", priority=8),
    ],
    # Priority 4 - Specialized
    "healthcare": [
        Rule("healthcareitnews.com", priority=10),
        Rule("medtechdive.com", priority=9),
        Rule("fiercehealthcare.com", priority=8),
        Rule("modernhealthcare.com", priority=8),
        Rule("beckerhospitalreview.com", priority=7),
    ],
    "legal": [
        Rule("law360.com", priority=10),
        Rule("legalweek.com", priority=9),
        Rule("thelawyer.com", priority=8),
        Rule("abovethelaw.com", priority=8),
        Rule("corporate counsel.com", priority=7),
        Rule("law.com", priority=7),
    ],
    "real_estate": [
        Rule("immobiliare.it", priority=10),
        Rule("idealista.it", priority=9),
        Rule("rightmove.co.uk", priority=8),
        Rule("zillow.com", priority=8),
        Rule("realtor.com", priority=7),
        Rule("loopnet.com", priority=7),
    ],
    "gaming": [
        Rule("gamesindustry.biz", priority=10),
        Rule("gamasutra.com", priority=9),
        Rule("ign.com", priority=8),
        Rule("pcgamer.com", priority=8),
        Rule("kotaku.com", priority=7),
        Rule("rockpapershotgun.com", priority=7),
        Rule("pcgamer.com", priority=8),
    ],
    "marketing": [
        Rule("adweek.com", priority=10),
        Rule("marketingland.com", priority=9),
        Rule("searchenginejournal.com", priority=8),
        Rule("contentmarketinginstitute.com", priority=8),
        Rule("socialmediatoday.com", priority=7),
    ],
}


# Exclusions
EXCLUDED = [
    Rule("example.com", priority=10),
    Rule("localhost", priority=10),
    Rule(r"^(127|192\.168|10)\.", is_regex=True, priority=10),
    Rule(".test", priority=10),
    Rule(".local", priority=10),
]
