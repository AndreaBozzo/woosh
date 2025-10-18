# Woosh

Applicazione per la ricerca e categorizzazione di informazioni su aziende.

## Struttura del Progetto

```
woosh/
├── backend/          # FastAPI backend
│   ├── app.py       # API endpoints
│   ├── search.py    # Logica di ricerca
│   ├── classify.py  # Classificazione URL
│   ├── config.py    # Configurazione categorie
│   └── requirements.txt
├── frontend/        # Next.js frontend
│   └── src/
│       └── app/
│           └── page.tsx
└── start.py         # Script di avvio rapido
```

## Requisiti

- Python 3.8+
- Node.js 18+
- npm

## Installazione

### Backend

```bash
cd woosh/backend
pip install -r requirements.txt
```

### Frontend

```bash
cd woosh/frontend
npm install
```

## Avvio dell'Applicazione

### Metodo Rapido (Consigliato)

Avvia sia frontend che backend con un solo comando:

```bash
python start.py
```

Lo script:
- Avvia automaticamente backend (porta 8000) e frontend (porta 3000)
- Mostra lo stato di entrambi i servizi
- Termina entrambi con `Ctrl+C`

### Metodo Manuale

Se preferisci avviare i servizi separatamente:

#### 1. Avvia il Backend (FastAPI)

```bash
cd woosh/backend
uvicorn app:app --reload --port 8000
```

Il backend sara disponibile su `http://localhost:8000`

#### 2. Avvia il Frontend (Next.js)

In un altro terminale:

```bash
cd woosh/frontend
npm run dev
```

Il frontend sara disponibile su `http://localhost:3000`

## Utilizzo

1. Apri il browser su `http://localhost:3000`
2. Inserisci il nome di un'azienda nel campo di ricerca
3. Premi Invio per avviare la ricerca
4. Visualizza i risultati categorizzati per tipo di dominio

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

## Categorie

Il sistema classifica automaticamente i risultati nelle seguenti categorie:

- **istituzionali**: Enti governativi e registri ufficiali
- **open_data**: Database aperti e registri pubblici
- **finance**: Notizie finanziarie e analisi di mercato
- **fintech**: Servizi finanziari digitali
- **blockchain**: Crypto e blockchain
- **social**: Social media
- **e-commerce**: Marketplace e negozi online
- **news**: Testate giornalistiche
- **startup**: Ecosistema startup
- **ai**: Intelligenza artificiale
- **cybersecurity**: Sicurezza informatica
- **healthcare**: Sanita
- **legal**: Informazioni legali
- **real_estate**: Immobiliare
- **gaming**: Gaming e videogiochi
- **marketing**: Marketing e pubblicita
- **altro**: Altri domini non categorizzati

## Configurazione

Le regole di classificazione sono definite in [woosh/backend/config.py](woosh/backend/config.py).

Puoi modificare o aggiungere nuove categorie e regole di matching secondo le tue esigenze.

## Tecnologie Utilizzate

### Backend
- **FastAPI**: Framework web moderno e veloce
- **DuckDuckGo Search**: Motore di ricerca per risultati
- **Pydantic**: Validazione dati

### Frontend
- **Next.js 15**: Framework React con App Router
- **React 19**: Libreria UI
- **Tailwind CSS 4**: Styling
- **TypeScript**: Type safety
