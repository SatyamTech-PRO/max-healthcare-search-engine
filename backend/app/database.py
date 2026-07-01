"""
SQLite database setup with FTS5 virtual tables for full-text search.
Handles schema creation, FTS5 indexing, and CSV data ingestion.
Production catalogs: medicines, investigations, procedures (from max_actualdata/).
"""

import csv
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = os.environ.get("DB_PATH", str(Path(__file__).parent.parent / "data" / "healthcare.db"))
ACTUAL_DATA_DIR = Path(__file__).parent.parent.parent / "max_actualdata"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=10000")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initialize database schema, FTS5 tables, and load CSV data if needed."""
    conn = get_connection()
    cur = conn.cursor()

    # ── Medicines table ────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id         INTEGER PRIMARY KEY,
            name       TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── Investigations table ───────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id         INTEGER PRIMARY KEY,
            name       TEXT NOT NULL,
            service_id TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── Procedures table ───────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS procedures (
            id         INTEGER PRIMARY KEY,
            name       TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── Search Analytics table ─────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS search_analytics (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            query         TEXT NOT NULL,
            category      TEXT,
            result_count  INTEGER DEFAULT 0,
            response_time REAL DEFAULT 0,
            searched_at   TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── FTS5 virtual tables ────────────────────────────────────────────────────
    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS medicines_fts USING fts5(
            name,
            content='medicines',
            content_rowid='id',
            tokenize='unicode61 remove_diacritics 1'
        )
    """)

    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS investigations_fts USING fts5(
            name,
            service_id,
            content='investigations',
            content_rowid='id',
            tokenize='unicode61 remove_diacritics 1'
        )
    """)

    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS procedures_fts USING fts5(
            name,
            content='procedures',
            content_rowid='id',
            tokenize='unicode61 remove_diacritics 1'
        )
    """)

    conn.commit()

    _load_csvs_if_needed(conn)
    _rebuild_fts_if_needed(conn)

    conn.close()
    print("✅ Database initialized successfully.")


def _load_csvs_if_needed(conn: sqlite3.Connection):
    """Load CSV files from max_actualdata/ into SQLite tables if tables are empty."""
    cur = conn.cursor()

    tables = [
        ("medicines",      ACTUAL_DATA_DIR / "medicine.csv",      ["ID", "NAME"],              "id, name"),
        ("investigations", ACTUAL_DATA_DIR / "investigation.csv",  ["Id", "name", "ServiceId"], "id, name, service_id"),
        ("procedures",     ACTUAL_DATA_DIR / "procedure.csv",      ["Id", "Name"],              "id, name"),
    ]

    for table, csv_path, cols, db_cols in tables:
        count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        if count > 0:
            continue
        if not csv_path.exists():
            print(f"⚠️  CSV not found: {csv_path}")
            continue
        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        if rows:
            placeholders = ", ".join(["?"] * len(cols))
            cur.executemany(
                f"INSERT OR REPLACE INTO {table} ({db_cols}) VALUES ({placeholders})",
                [[r.get(c, "") for c in cols] for r in rows]
            )
            conn.commit()
            print(f"✅ Loaded {len(rows)} rows into '{table}'")


def _rebuild_fts_if_needed(conn: sqlite3.Connection):
    """Populate FTS5 tables if empty."""
    cur = conn.cursor()
    for fts_table in ["medicines_fts", "investigations_fts", "procedures_fts"]:
        try:
            count = cur.execute(f"SELECT COUNT(*) FROM {fts_table}_data").fetchone()[0]
            if count <= 10:
                cur.execute(f"INSERT INTO {fts_table}({fts_table}) VALUES('rebuild')")
                conn.commit()
                print(f"✅ Built FTS5 index for '{fts_table}'")
        except Exception as e:
            print(f"⚠️  FTS rebuild issue for {fts_table}: {e}")


def log_search(query: str, category: str, result_count: int, response_time: float):
    """Log search query to analytics table."""
    try:
        with get_db() as conn:
            conn.execute(
                """INSERT INTO search_analytics (query, category, result_count, response_time)
                   VALUES (?, ?, ?, ?)""",
                (query, category, result_count, response_time)
            )
    except Exception as e:
        print(f"Analytics log error: {e}")


def get_db_stats() -> dict:
    """Return record counts for all production catalogs."""
    with get_db() as conn:
        med  = conn.execute("SELECT COUNT(*) FROM medicines").fetchone()[0]
        inv  = conn.execute("SELECT COUNT(*) FROM investigations").fetchone()[0]
        proc = conn.execute("SELECT COUNT(*) FROM procedures").fetchone()[0]
        searches = conn.execute("SELECT COUNT(*) FROM search_analytics").fetchone()[0]
    return {
        "medicines":      med,
        "investigations": inv,
        "procedures":     proc,
        "total_searches": searches,
    }
