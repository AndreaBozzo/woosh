from typing import Dict, List

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from search import search_companies

app = FastAPI(title="Woosh API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchResponse(BaseModel):
    results: Dict[str, List[str]]
    total: int


@app.get("/")
def root():
    return {"message": "Woosh API is running", "version": "1.0.0"}


@app.get("/api/search", response_model=SearchResponse)
def search(
    query: str = Query(..., description="Company name to search for"),
    max_results: int = Query(
        100, ge=1, le=200, description="Maximum number of results"
    ),
):
    """Search for companies and categorize results by domain type."""
    results = search_companies(query, max_results)
    total = sum(len(urls) for urls in results.values())

    return SearchResponse(results=results, total=total)
