# woosh

Python tool for EU VAT validation and company web search.
Helps to get rid of Google bullsh*t and ads.

## Overview

Search for companies by name or validate EU VAT numbers via VIES. Automatically categorizes URLs found into social media, institutional sites, e-commerce, news, etc.

## Features

- **EU VAT validation** via VIES (VAT Information Exchange System)
- **Smart input detection**: automatically detects if input is VAT number or company name
- Web search via DuckDuckGo
- URL classification into categories (social, institutional, e-commerce, news, open data, etc.)
- JSON export

## Requirements

- Python 3.10 or higher

## Installation

```bash
pip install -e .
```

## Usage

```bash
python main.py
```

Enter either:

- **VAT number** (e.g., `IT12345678901`) - validates via VIES and searches for company URLs
- **Company name** (e.g., `Microsoft`) - searches for URLs

Results are displayed in formatted tables and can be saved to JSON.

## Project Structure

```
company_finder/
├── enrich.py       # VAT validation + search
├── vies.py         # VIES SOAP client
├── models.py       # Data models
├── search.py       # DuckDuckGo search
├── classify.py     # URL categorization
└── config.py       # Categories config
main.py             # CLI (smart VAT/name detection)
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Code quality tools:
- **black** - Code formatting (88 char line length)
- **isort** - Import sorting
- **mypy** - Type checking
- **flake8** - Linting

## License

This project is under active development.
