from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rapidfuzz import process, fuzz

from app import database

# In-memory stores for RapidFuzz
fuzz_data = {
    "medicines": [],
    "diagnoses": [],
    "investigations": []
}

def load_fuzz_data():
    global fuzz_data
    with database.get_db() as conn:
        for table in ["medicines", "diagnoses", "investigations"]:
            rows = conn.execute(f"SELECT id, name FROM {table}").fetchall()
            fuzz_data[table] = [{"id": r["id"], "name": r["name"]} for r in rows]

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


class SearchResult(BaseModel):
    id: int
    name: str
    type: str
    details: str
    score: float


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total: int


@app.get("/api/search", response_model=SearchResponse)
def search(q: str = Query(..., min_length=1)):
    """Search across medicines, diagnoses, and investigations using FTS5 and RapidFuzz."""
    results = []
    
    with database.get_db() as conn:
        # FTS5 pass
        fts_query = f"{q}*"
        
        # Search Medicines
        med_rows = conn.execute(
            "SELECT m.id, m.name, m.generic_name, m.dosage_form, m.strength, rank FROM medicines_fts m_fts JOIN medicines m ON m_fts.rowid = m.id WHERE medicines_fts MATCH ? ORDER BY rank LIMIT 10",
            (fts_query,)
        ).fetchall()
        for r in med_rows:
            details = f"{r['generic_name']} | {r['strength']} {r['dosage_form']}"
            results.append(SearchResult(id=r['id'], name=r['name'], type='medicine', details=details, score=abs(r['rank'])))

        # Search Diagnoses
        diag_rows = conn.execute(
            "SELECT d.id, d.name, d.icd_code, d.specialty, rank FROM diagnoses_fts d_fts JOIN diagnoses d ON d_fts.rowid = d.id WHERE diagnoses_fts MATCH ? ORDER BY rank LIMIT 10",
            (fts_query,)
        ).fetchall()
        for r in diag_rows:
            details = f"ICD: {r['icd_code']} | {r['specialty']}"
            results.append(SearchResult(id=r['id'], name=r['name'], type='diagnosis', details=details, score=abs(r['rank'])))

        # Search Investigations
        inv_rows = conn.execute(
            "SELECT i.id, i.name, i.department, i.sample_type, rank FROM investigations_fts i_fts JOIN investigations i ON i_fts.rowid = i.id WHERE investigations_fts MATCH ? ORDER BY rank LIMIT 10",
            (fts_query,)
        ).fetchall()
        for r in inv_rows:
            details = f"{r['department']} | Sample: {r['sample_type']}"
            results.append(SearchResult(id=r['id'], name=r['name'], type='investigation', details=details, score=abs(r['rank'])))

    # If FTS5 yields few results, apply RapidFuzz to catch typos
    if len(results) < 5:
        existing_ids = {f"{r.type}_{r.id}" for r in results}
        
        # Fuzzy search medicines
        med_names = {x["name"]: x["id"] for x in fuzz_data["medicines"]}
        med_matches = process.extract(q, med_names.keys(), limit=5, scorer=fuzz.WRatio)
        
        with database.get_db() as conn:
            for match, score, _ in med_matches:
                if score < 70: continue
                med_id = med_names[match]
                if f"medicine_{med_id}" not in existing_ids:
                    r = conn.execute("SELECT name, generic_name, dosage_form, strength FROM medicines WHERE id = ?", (med_id,)).fetchone()
                    details = f"{r['generic_name']} | {r['strength']} {r['dosage_form']}"
                    results.append(SearchResult(id=med_id, name=r['name'], type='medicine', details=details, score=score))
                    existing_ids.add(f"medicine_{med_id}")
            
            # Fuzzy search diagnoses
            diag_names = {x["name"]: x["id"] for x in fuzz_data["diagnoses"]}
            diag_matches = process.extract(q, diag_names.keys(), limit=5, scorer=fuzz.WRatio)
            for match, score, _ in diag_matches:
                if score < 70: continue
                diag_id = diag_names[match]
                if f"diagnosis_{diag_id}" not in existing_ids:
                    r = conn.execute("SELECT name, icd_code, specialty FROM diagnoses WHERE id = ?", (diag_id,)).fetchone()
                    details = f"ICD: {r['icd_code']} | {r['specialty']}"
                    results.append(SearchResult(id=diag_id, name=r['name'], type='diagnosis', details=details, score=score))
                    existing_ids.add(f"diagnosis_{diag_id}")

            # Fuzzy search investigations
            inv_names = {x["name"]: x["id"] for x in fuzz_data["investigations"]}
            inv_matches = process.extract(q, inv_names.keys(), limit=5, scorer=fuzz.WRatio)
            for match, score, _ in inv_matches:
                if score < 70: continue
                inv_id = inv_names[match]
                if f"investigation_{inv_id}" not in existing_ids:
                    r = conn.execute("SELECT name, department, sample_type FROM investigations WHERE id = ?", (inv_id,)).fetchone()
                    details = f"{r['department']} | Sample: {r['sample_type']}"
                    results.append(SearchResult(id=inv_id, name=r['name'], type='investigation', details=details, score=score))
                    existing_ids.add(f"investigation_{inv_id}")

            # Deduplicate by name (case-insensitive)
    seen_names = set()
    unique_results = []
    for r in results:
        key = r.name.lower().strip()
        if key not in seen_names:
            seen_names.add(key)
            unique_results.append(r)
    results = unique_results

    # Exact match floats to top
    q_lower = q.lower().strip()
    q_words = set(q_lower.split())
    results.sort(key=lambda x: (
        0 if x.name.lower().strip() == q_lower else
        1 if all(w in x.name.lower() for w in q_words) else
        2,
        x.type,
        x.name
    ))

    # Log analytics
    database.log_search(q, "all", len(results), 0.0)

    return SearchResponse(
        query=q,
        results=results,
        total=len(results)
    )

@app.get("/api/stats")
def stats():
    return database.get_db_stats()