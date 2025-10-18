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
        Rule(r"\.gov\.(it|uk|fr|de|es)$", is_regex=True, priority=10),
        # European institutions
        Rule("europa.eu", priority=10),
        Rule("ec.europa.eu", priority=10),
        Rule("eur-lex.europa.eu", priority=10),
        Rule("eib.org", priority=9),  # European Investment Bank
        Rule("ecb.europa.eu", priority=10),  # European Central Bank
        Rule("esm.europa.eu", priority=9),  # European Stability Mechanism
        # Italian institutions
        Rule("camera.it", priority=10),
        Rule("senato.it", priority=10),
        Rule("governo.it", priority=10),
        Rule("presidenza.governo.it", priority=10),
        Rule("inps.it", priority=9),
        Rule("gazzettaufficiale.it", priority=10),
        Rule("consob.it", priority=10),
        Rule("bancaditalia.it", priority=10),
        Rule("istat.it", priority=10),
        Rule("agid.gov.it", priority=9),
        Rule("agenziadelleentrate.gov.it", priority=10),
        Rule("registroimprese.it", priority=10),
        Rule("camcom.gov.it", priority=10),
        Rule("unioncamere.gov.it", priority=9),
        Rule("mise.gov.it", priority=9),  # Ministero Sviluppo Economico
        Rule("mef.gov.it", priority=9),  # Ministero Economia e Finanze
        Rule("giustizia.it", priority=9),
        Rule("infocamere.it", priority=9),
        Rule("agcom.it", priority=9),
        Rule("antitrust.it", priority=9),
        Rule("ivass.it", priority=9),  # Insurance regulator
        Rule("covip.it", priority=9),  # Pension funds regulator
        # Other EU countries
        Rule("chamberofcommerce.com", priority=9),
        Rule("gov.uk/companies-house", priority=10),
        Rule("service-public.fr", priority=9),
        Rule("handelsregister.de", priority=9),
    ],
    # Priority 9 - Open Data & Registries
    "open_data": [
        # International
        Rule("opencorporates.com", priority=10),
        Rule("companieshouse.gov.uk", priority=10),
        Rule("data.gov", priority=9),
        Rule("data.gov.uk", priority=9),
        Rule("data.gov.au", priority=9),
        Rule("data.gov.nz", priority=9),
        # Italian
        Rule("registroimprese.it", priority=10),
        Rule("dati.gov.it", priority=10),
        Rule("infocamere.it", priority=10),
        Rule("telemaco.infocamere.it", priority=10),
        Rule("impresa.italia.it", priority=10),
        # European
        Rule("data.europa.eu", priority=10),
        Rule("ted.europa.eu", priority=9),  # Tenders Electronic Daily
    ],
    # Priority 8 - Finance
    "finance": [
        # International
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
        # Italian
        Rule("ilsole24ore.com", priority=10),
        Rule("milanofinanza.it", priority=10),
        Rule("borsaitaliana.it", priority=10),
        Rule("borsaitaliana.reuters.it", priority=9),
        Rule("it.finance.yahoo.com", priority=8),
        Rule("finanza.repubblica.it", priority=8),
        Rule("economy.ilsole24ore.com", priority=9),
        Rule("plus24.ilsole24ore.com", priority=9),
        Rule("classcnbc.it", priority=9),
        Rule("bebeez.it", priority=9),  # Private equity & VC
        # European
        Rule("euronext.com", priority=9),
        Rule("deutsche-boerse.com", priority=9),
        Rule("londonstockexchange.com", priority=9),
    ],
    # Priority 7 - Fintech & Blockchain
    "fintech": [
        # International
        Rule("finextra.com", priority=10),
        Rule("stripe.com", priority=9),
        Rule("squareup.com", priority=9),
        Rule("paypal.com", priority=9),
        Rule("adyen.com", priority=8),
        Rule("klarna.com", priority=8),
        Rule("revolut.com", priority=8),
        Rule("wise.com", priority=8),
        # Italian & European
        Rule("nexi.it", priority=9),
        Rule("satispay.com", priority=9),
        Rule("tinaba.it", priority=8),
        Rule("hype.it", priority=8),
        Rule("n26.com", priority=8),
        Rule("qonto.com", priority=8),
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
        # Italian
        Rule("ansa.it", priority=10),
        Rule("repubblica.it", priority=10),
        Rule("corriere.it", priority=10),
        Rule("ilsole24ore.com", priority=10),
        Rule("ilpost.it", priority=10),
        Rule("lastampa.it", priority=9),
        Rule("ilmessaggero.it", priority=9),
        Rule("rainews.it", priority=9),
        Rule("tgcom24.mediaset.it", priority=9),
        Rule("adnkronos.com", priority=9),
        Rule("ilgiornale.it", priority=8),
        Rule("huffingtonpost.it", priority=8),
        Rule("fanpage.it", priority=8),
        Rule("today.it", priority=8),
        Rule("wired.it", priority=9),
        Rule("punto-informatico.it", priority=8),
        Rule("hwupgrade.it", priority=8),
        # International
        Rule("bbc.com", priority=9),
        Rule("cnn.com", priority=9),
        Rule("theguardian.com", priority=9),
        Rule("nytimes.com", priority=9),
        Rule("theverge.com", priority=8),
        Rule("techcrunch.com", priority=8),
        Rule("wired.com", priority=8),
        Rule("arstechnica.com", priority=8),
        # European
        Rule("euractiv.com", priority=9),
        Rule("politico.eu", priority=9),
        Rule("euobserver.com", priority=8),
    ],
    "startup": [
        # Italian
        Rule("startupitalia.eu", priority=10),
        Rule("economyup.it", priority=9),
        Rule("innovationpost.it", priority=9),
        Rule("startupbusiness.it", priority=9),
        Rule("italiastartup.it", priority=8),
        Rule("ninjamarketing.it", priority=8),
        Rule("digital4.biz", priority=8),
        Rule("cdp.it", priority=8),  # Cassa Depositi e Prestiti
        Rule("invitalia.it", priority=8),
        # International
        Rule("techcrunch.com", priority=8),
        Rule("venturebeat.com", priority=8),
        Rule("thenextweb.com", priority=8),
        Rule("angel.co", priority=7),
        Rule("seedrs.com", priority=7),
        Rule("crunchbase.com", priority=9),
        # European
        Rule("eu-startups.com", priority=8),
        Rule("sifted.eu", priority=9),
    ],
    "ai": [
        # International
        Rule("openai.com", priority=10),
        Rule("huggingface.co", priority=9),
        Rule("anthropic.com", priority=9),
        Rule("deepmind.com", priority=9),
        Rule("google.com/ai", priority=8),
        Rule("microsoft.com/ai", priority=8),
        Rule("ibm.com/watson", priority=8),
        # Italian & European
        Rule("ai4business.it", priority=9),
        Rule("agendadigitale.eu", priority=9),
        Rule("ict4executive.it", priority=8),
    ],
    "cybersecurity": [
        # International
        Rule("krebsonsecurity.com", priority=10),
        Rule("bleepingcomputer.com", priority=9),
        Rule("thehackernews.com", priority=9),
        Rule("cyberscoop.com", priority=8),
        Rule("darkreading.com", priority=8),
        # Italian & European
        Rule("cybersecurity360.it", priority=9),
        Rule("agendadigitale.eu", priority=9),
        Rule("sicurezzamagazine.it", priority=8),
        Rule("cert-agid.gov.it", priority=10),
        Rule("csirt.gov.it", priority=10),
    ],
    # Priority 4 - Specialized
    "healthcare": [
        # International
        Rule("healthcareitnews.com", priority=10),
        Rule("medtechdive.com", priority=9),
        Rule("fiercehealthcare.com", priority=8),
        Rule("modernhealthcare.com", priority=8),
        Rule("beckerhospitalreview.com", priority=7),
        # Italian
        Rule("quotidianosanita.it", priority=9),
        Rule("sanita24.ilsole24ore.com", priority=9),
        Rule("salute.gov.it", priority=10),
        Rule("aifa.gov.it", priority=9),
        Rule("iss.it", priority=9),  # Istituto Superiore di Sanità
    ],
    "legal": [
        # International
        Rule("law360.com", priority=10),
        Rule("legalweek.com", priority=9),
        Rule("thelawyer.com", priority=8),
        Rule("abovethelaw.com", priority=8),
        Rule("corporatecounsel.com", priority=7),
        Rule("law.com", priority=7),
        # Italian
        Rule("diritto24.ilsole24ore.com", priority=9),
        Rule("altalex.com", priority=9),
        Rule("dirittoegiustizia.it", priority=8),
        Rule("legalcommunity.it", priority=8),
        Rule("studiocataldi.it", priority=7),
        Rule("normattiva.it", priority=10),  # Italian legislation database
    ],
    "real_estate": [
        # Italian
        Rule("immobiliare.it", priority=10),
        Rule("idealista.it", priority=9),
        Rule("casa.it", priority=9),
        Rule("tecnocasa.it", priority=8),
        Rule("gabetti.it", priority=8),
        Rule("wikicasa.it", priority=8),
        Rule("nomisma.it", priority=9),  # Real estate market research
        # International
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
        # International
        Rule("adweek.com", priority=10),
        Rule("marketingland.com", priority=9),
        Rule("searchenginejournal.com", priority=8),
        Rule("contentmarketinginstitute.com", priority=8),
        Rule("socialmediatoday.com", priority=7),
        # Italian
        Rule("ninjamarketing.it", priority=9),
        Rule("marketingjournal.it", priority=8),
        Rule("insidemarketing.it", priority=8),
        Rule("brandnews.it", priority=8),
        Rule("engage.it", priority=8),
    ],
}


# Exclusions
EXCLUDED = [
    # Development/test
    Rule("example.com", priority=10),
    Rule("localhost", priority=10),
    Rule(r"^(127|192\.168|10)\.", is_regex=True, priority=10),
    Rule(".test", priority=10),
    Rule(".local", priority=10),
    # Aggregators & low-quality
    Rule("wikipedia.org", priority=10),
    Rule("wikimedia.org", priority=10),
    Rule("wikidata.org", priority=10),
    Rule("facebook.com/pages", priority=10),
    Rule("pinterest.com", priority=9),
    Rule("quora.com", priority=9),
    Rule("answers.yahoo.com", priority=9),
    Rule("ask.com", priority=9),
    # Directories & listings (generic)
    Rule("yellowpages", priority=9),
    Rule("paginegialle", priority=9),
    Rule("yelp.com", priority=8),
    Rule("tripadvisor", priority=8),
    Rule("manta.com", priority=8),
    Rule("thumbtack.com", priority=8),
]
