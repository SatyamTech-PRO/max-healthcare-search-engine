from contextlib import asynccontextmanager
from typing import List, Optional, Any, Dict

from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from app import database
from app.search_engine import SearchResult, search_entities, load_fuzz_data
from app.db_mapper import map_json

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB and FTS tables
    database.init_db()
    # Load data for fuzzy search
    load_fuzz_data()
    yield
    # Cleanup if needed

app = FastAPI(title="Max Healthcare Search API", lifespan=lifespan)

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total: int


class MappedItem(BaseModel):
    input: str
    matched_id: Optional[int] = None
    matched_name: Optional[str] = None
    score: Optional[float] = None
    match_type: Optional[str] = None


class EPJsonRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    medication: Optional[List[Any]] = None
    investigationAdvised: Optional[List[Any]] = None
    procedureAdvised: Optional[List[Any]] = None


class EPJsonResponse(BaseModel):
    medication: Optional[List[MappedItem]] = None
    investigationAdvised: Optional[List[MappedItem]] = None
    procedureAdvised: Optional[List[MappedItem]] = None


@app.get("/api/search", response_model=SearchResponse)
def search(q: str = Query(..., min_length=1)):
    """Search across medicines, investigations, and procedures using FTS5 and RapidFuzz."""
    results = search_entities(q)
    
    # Log analytics
    database.log_search(q, "all", len(results), 0.0)

    return SearchResponse(query=q, results=results, total=len(results))


@app.post("/api/map-json", response_model=EPJsonResponse)
def api_map_json(payload: EPJsonRequest):
    """
    Maps free-text clinical entities from an EP JSON to structured database records.
    
    Example payload:
    {
      "medication": [{"drugDesc": "Ibuprofen"}],
      "investigationAdvised": [{"investigationAdvised": "CBC"}],
      "procedureAdvised": [{"procedureAdvised": "Appendectomy"}]
    }
    """
    # Use the decoupled db_mapper module
    mapped_dict = map_json(payload.model_dump())
    return EPJsonResponse(**mapped_dict)


@app.get("/api/stats")
def stats():
    return database.get_db_stats()