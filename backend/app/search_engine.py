from typing import List
from pydantic import BaseModel
from rapidfuzz import process, fuzz

from app import database

# In-memory stores for RapidFuzz — one entry per production catalog
fuzz_data = {
    "medicines":      [],
    "investigations": [],
    "procedures":     []
}


def load_fuzz_data():
    """Load all catalog names into memory for fast fuzzy matching."""
    global fuzz_data
    with database.get_db() as conn:
        for table in ["medicines", "investigations", "procedures"]:
            rows = conn.execute(f"SELECT id, name FROM {table}").fetchall()
            fuzz_data[table] = [{"id": r["id"], "name": r["name"]} for r in rows]


class SearchResult(BaseModel):
    id: int
    name: str
    type: str
    details: str
    score: float


def search_entities(q: str, allowed_types: List[str] = None) -> List[SearchResult]:
    """
    Search production catalogs via FTS5 with RapidFuzz typo-tolerance fallback.
    allowed_types: subset of ["medicine", "investigation", "procedure"]
    """
    results = []
    if not q or not q.strip():
        return results

    if allowed_types is None:
        allowed_types = ["medicine", "investigation", "procedure"]

    with database.get_db() as conn:
        fts_query = f"{q}*"

        if "medicine" in allowed_types:
            rows = conn.execute(
                "SELECT m.id, m.name, rank "
                "FROM medicines_fts JOIN medicines m ON medicines_fts.rowid = m.id "
                "WHERE medicines_fts MATCH ? ORDER BY rank LIMIT 10",
                (fts_query,)
            ).fetchall()
            for r in rows:
                results.append(SearchResult(
                    id=r["id"], name=r["name"], type="medicine",
                    details=f"ID: {r['id']}", score=100.0
                ))

        if "investigation" in allowed_types:
            rows = conn.execute(
                "SELECT i.id, i.name, i.service_id, rank "
                "FROM investigations_fts JOIN investigations i ON investigations_fts.rowid = i.id "
                "WHERE investigations_fts MATCH ? ORDER BY rank LIMIT 10",
                (fts_query,)
            ).fetchall()
            for r in rows:
                details = f"Service ID: {r['service_id']}" if r["service_id"] else f"ID: {r['id']}"
                results.append(SearchResult(
                    id=r["id"], name=r["name"], type="investigation",
                    details=details, score=100.0
                ))

        if "procedure" in allowed_types:
            rows = conn.execute(
                "SELECT p.id, p.name, rank "
                "FROM procedures_fts JOIN procedures p ON procedures_fts.rowid = p.id "
                "WHERE procedures_fts MATCH ? ORDER BY rank LIMIT 10",
                (fts_query,)
            ).fetchall()
            for r in rows:
                results.append(SearchResult(
                    id=r["id"], name=r["name"], type="procedure",
                    details=f"ID: {r['id']}", score=100.0
                ))

    # RapidFuzz fallback when FTS5 yields sparse results
    if len(results) < 5:
        existing_ids = {f"{r.type}_{r.id}" for r in results}

        with database.get_db() as conn:
            if "medicine" in allowed_types:
                name_to_id = {x["name"]: x["id"] for x in fuzz_data["medicines"]}
                if name_to_id:
                    for match, score, _ in process.extract(q, name_to_id.keys(), limit=5, scorer=fuzz.WRatio):
                        if score < 70:
                            continue
                        mid = name_to_id[match]
                        key = f"medicine_{mid}"
                        if key not in existing_ids:
                            r = conn.execute("SELECT name FROM medicines WHERE id = ?", (mid,)).fetchone()
                            results.append(SearchResult(id=mid, name=r["name"], type="medicine", details=f"ID: {mid}", score=score))
                            existing_ids.add(key)

            if "investigation" in allowed_types:
                name_to_id = {x["name"]: x["id"] for x in fuzz_data["investigations"]}
                if name_to_id:
                    for match, score, _ in process.extract(q, name_to_id.keys(), limit=5, scorer=fuzz.WRatio):
                        if score < 70:
                            continue
                        iid = name_to_id[match]
                        key = f"investigation_{iid}"
                        if key not in existing_ids:
                            r = conn.execute("SELECT name, service_id FROM investigations WHERE id = ?", (iid,)).fetchone()
                            details = f"Service ID: {r['service_id']}" if r["service_id"] else f"ID: {iid}"
                            results.append(SearchResult(id=iid, name=r["name"], type="investigation", details=details, score=score))
                            existing_ids.add(key)

            if "procedure" in allowed_types:
                name_to_id = {x["name"]: x["id"] for x in fuzz_data["procedures"]}
                if name_to_id:
                    for match, score, _ in process.extract(q, name_to_id.keys(), limit=5, scorer=fuzz.WRatio):
                        if score < 70:
                            continue
                        pid = name_to_id[match]
                        key = f"procedure_{pid}"
                        if key not in existing_ids:
                            r = conn.execute("SELECT name FROM procedures WHERE id = ?", (pid,)).fetchone()
                            results.append(SearchResult(id=pid, name=r["name"], type="procedure", details=f"ID: {pid}", score=score))
                            existing_ids.add(key)

    # Deduplicate by name (case-insensitive)
    seen, unique = set(), []
    for r in results:
        k = r.name.lower().strip()
        if k not in seen:
            seen.add(k)
            unique.append(r)
    results = unique

    # Sort: exact match → partial match → fuzzy, then by score desc
    q_lower = q.lower().strip()
    q_words = set(q_lower.split())
    results.sort(key=lambda x: (
        0 if x.name.lower().strip() == q_lower else
        1 if all(w in x.name.lower() for w in q_words) else
        2,
        -x.score,
        x.type,
        x.name
    ))

    return results
