"""
SQLite database setup with FTS5 virtual tables for full-text search.
Handles schema creation, FTS5 indexing, and CSV data ingestion.
"""

import csv
import os
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

DB_PATH = os.environ.get("DB_PATH", str(Path(__file__).parent.parent / "data" / "healthcare.db"))
DATA_DIR = Path(__file__).parent.parent / "data"


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
            id                  INTEGER PRIMARY KEY,
            name                TEXT NOT NULL,
            generic_name        TEXT,
            category            TEXT,
            manufacturer        TEXT,
            dosage_form         TEXT,
            strength            TEXT,
            description         TEXT,
            drug_class          TEXT,
            prescription_required TEXT,
            storage             TEXT,
            created_at          TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── Diagnoses table ────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS diagnoses (
            id                  INTEGER PRIMARY KEY,
            name                TEXT NOT NULL,
            icd_code            TEXT,
            specialty           TEXT,
            description         TEXT,
            severity            TEXT,
            chronic             TEXT,
            treatment_available TEXT,
            prevalence          TEXT,
            created_at          TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── Investigations table ───────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id                  INTEGER PRIMARY KEY,
            name                TEXT NOT NULL,
            department          TEXT,
            sample_type         TEXT,
            description         TEXT,
            turnaround_time     TEXT,
            fasting_required    TEXT,
            normal_range        TEXT,
            cost_category       TEXT,
            created_at          TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── Search Analytics table ─────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS search_analytics (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            query           TEXT NOT NULL,
            category        TEXT,
            result_count    INTEGER DEFAULT 0,
            response_time   REAL DEFAULT 0,
            searched_at     TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── FTS5 virtual tables ────────────────────────────────────────────────────
    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS medicines_fts USING fts5(
            name,
            generic_name,
            category,
            manufacturer,
            dosage_form,
            drug_class,
            description,
            content='medicines',
            content_rowid='id',
            tokenize='unicode61 remove_diacritics 1'
        )
    """)

    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS diagnoses_fts USING fts5(
            name,
            icd_code,
            specialty,
            description,
            content='diagnoses',
            content_rowid='id',
            tokenize='unicode61 remove_diacritics 1'
        )
    """)

    cur.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS investigations_fts USING fts5(
            name,
            department,
            sample_type,
            description,
            content='investigations',
            content_rowid='id',
            tokenize='unicode61 remove_diacritics 1'
        )
    """)

    conn.commit()

    # Load data if tables are empty
    _load_csvs_if_needed(conn)

    # Build FTS indices if needed
    _rebuild_fts_if_needed(conn)

    conn.close()
    print("✅ Database initialized successfully.")


def _load_csvs_if_needed(conn: sqlite3.Connection):
    """Load CSV files into SQLite tables if tables are empty."""
    cur = conn.cursor()

    tables = [
        ("medicines", DATA_DIR / "medicines.csv"),
        ("diagnoses", DATA_DIR / "diagnoses.csv"),
        ("investigations", DATA_DIR / "investigations.csv"),
    ]

    for table, csv_path in tables:
        count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        if count == 0:
            if not csv_path.exists():
                print(f"⚠️  CSV not found: {csv_path}. Run generate_datasets.py first.")
                continue
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            if rows:
                cols = [k for k in rows[0].keys() if k != ""]
                placeholders = ", ".join(["?" for _ in cols])
                col_names = ", ".join(cols)
                cur.executemany(
                    f"INSERT OR REPLACE INTO {table} ({col_names}) VALUES ({placeholders})",
                    [[r.get(c, "") for c in cols] for r in rows]
                )
                conn.commit()
                print(f"✅ Loaded {len(rows)} rows into '{table}'")


def _rebuild_fts_if_needed(conn: sqlite3.Connection):
    """Populate FTS5 tables if empty."""
    cur = conn.cursor()
    for fts_table, source_table in [
        ("medicines_fts", "medicines"),
        ("diagnoses_fts", "diagnoses"),
        ("investigations_fts", "investigations"),
    ]:
        try:
            count = cur.execute(f"SELECT COUNT(*) FROM {fts_table}_data").fetchone()[0]
            if count <= 10: # If data table is small, it means the index is basically empty
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
    """Return counts for all entities."""
    with get_db() as conn:
        med = conn.execute("SELECT COUNT(*) FROM medicines").fetchone()[0]
        diag = conn.execute("SELECT COUNT(*) FROM diagnoses").fetchone()[0]
        inv = conn.execute("SELECT COUNT(*) FROM investigations").fetchone()[0]
        searches = conn.execute("SELECT COUNT(*) FROM search_analytics").fetchone()[0]
    return {
        "medicines": med,
        "diagnoses": diag,
        "investigations": inv,
        "total_searches": searches,
    }
