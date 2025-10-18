from typing import Dict, List

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from search import search_companies
from vies import validate_vat, VATInfo

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


@app.get("/api/vat/{vat_number}", response_model=VATInfo)
def get_vat_info(
    vat_number: str,
    country: str = Query("IT", description="Default country code if not in VAT number"),
):
    """
    Validate a VAT number and get company information from VIES.

    The VAT number can include the country code (e.g., IT12345678901) or just the number.
    """
    try:
        result = validate_vat(vat_number, default_country=country)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating VAT: {str(e)}")
