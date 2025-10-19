# woosh


             ______
          ,'"       "-._
        ,'              "-._ _._
        ;              __,-'/   |
       ;|           ,-' _,'"'._,.
       |:            _,'      |\ `.
       : \       _,-'         | \  `.
        \ \   ,-'             |  \   \
         \ '.         .-.     |       \
          \  \         "      |        :
           `. `.              |        |
             `. "-._          |        ;
             / |`._ `-._      L       /
            /  | \ `._   "-.___    _,'
           /   |  \_.-"-.___   """"
           \   :            /"""
            `._\_       __.'_
       __,--''_ ' "--'''' \_  `-._
 __,--'     .' /_  |   __. `-._   `-._
            `.  `-.-''  __,-'     _,-'
 `.            `.   _,-'"      _,-'
   `.                      _,-'
     `.                _,-'
       `.          _,-'
         `.   __,'"
           `'"

Python tool for EU VAT validation and company web search. Helps to get rid of Google bullsh*t and ads.
Main files MUST contain ASCII art, this is mandatory and entirely for memes purposes.

## Project Structure

```
woosh/
├── woosh/
│   ├── backend/          # FastAPI backend
│   │   ├── app.py       # API endpoints
│   │   ├── search.py    # Search logic
│   │   ├── classify.py  # URL classification
│   │   ├── config.py    # Category configuration
│   │   ├── tests/       # Backend tests
│   │   └── requirements.txt
│   └── frontend/        # Next.js frontend
│       ├── src/app/     # Next.js app directory
│       └── package.json
├── install.py          # Unified installation script
├── start.py            # Development server launcher
├── Makefile            # Common development tasks
├── pyproject.toml      # Python project configuration

```

## Requirements

- Python 3.8+
- Node.js 18+
- npm
- Make (optional, for using Makefile commands)

## Quick Start

```bash
# Install dependencies
make install
# or: python install.py

# Start development servers
make dev
# or: python start.py
```

Then open http://localhost:3000

## Installation

### Using Make (Recommended)

```bash
make install
```

### Using Python Script

```bash
python install.py
```

### Manual Installation

```bash
# Backend
cd woosh/backend
pip install -r requirements.txt

# Frontend
cd woosh/frontend
npm install
```

## Running the Application

### Using Make

```bash
make dev          # Start both frontend and backend
make backend      # Start only backend
make frontend     # Start only frontend
```

### Using Python Script

```bash
python start.py   # Start both frontend and backend
```

### Manual Start

```bash
# Backend (terminal 1)
cd woosh/backend
uvicorn app:app --reload --port 8000

# Frontend (terminal 2)
cd woosh/frontend
npm run dev
```

## Available Make Commands

```bash
make help              # Show all available commands
make install           # Install all dependencies
make dev              # Start development servers
make test             # Run tests
make clean            # Clean build artifacts
make lint             # Run linters
make format           # Format code
make build-frontend   # Build frontend for production
```

## Usage

1. Open browser at `http://localhost:3000`
2. Enter a company name in the search field
3. Press Enter to start the search
4. View results categorized by domain type

## API Endpoints

### GET /api/search

Cerca aziende e restituisce risultati categorizzati.

**Parametri:**
- `query` (required): Nome dell'azienda da cercare
- `max_results` (optional): Numero massimo di risultati (default: 100, max: 200)

**Esempio:**
```bash
curl "http://localhost:8000/api/search?query=Ferrari&max_results=50"
```

**Risposta:**
```json
{
  "results": {
    "istituzionali": ["https://..."],
    "finance": ["https://..."],
    "news": ["https://..."]
  },
  "total": 42
}
```

## Categories

The system automatically classifies results into the following categories:

- **istituzionali**: Government entities and official registries
- **open_data**: Open databases and public registries
- **finance**: Financial news and market analysis
- **fintech**: Digital financial services
- **blockchain**: Crypto and blockchain
- **social**: Social media
- **e-commerce**: Marketplaces and online stores
- **news**: News outlets
- **startup**: Startup ecosystem
- **ai**: Artificial intelligence
- **cybersecurity**: Information security
- **healthcare**: Healthcare
- **legal**: Legal information
- **real_estate**: Real estate
- **gaming**: Gaming and video games
- **marketing**: Marketing and advertising
- **altro**: Other uncategorized domains

## Configuration

Classification rules are defined in [woosh/backend/config.py](woosh/backend/config.py).

You can modify or add new categories and matching rules according to your needs.

## Technologies Used

### Backend

- **FastAPI**: Modern and fast web framework
- **DuckDuckGo Search**: Search engine for results
- **Pydantic**: Data validation

### Frontend

- **Next.js 15**: React framework with App Router
- **React 19**: UI library
- **Tailwind CSS 4**: Styling
- **TypeScript**: Type safety
