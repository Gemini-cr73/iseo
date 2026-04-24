import os
import sqlite3
from pathlib import Path

from app.core.config import settings


def get_db_path() -> str:
    db_path = getattr(settings, "db_path", None) or os.getenv(
        "ISEO_DB_PATH", "./data/iseo.sqlite"
    )

    if db_path.startswith("sqlite:///"):
        db_path = db_path.replace("sqlite:///", "", 1)

    return db_path


def get_conn() -> sqlite3.Connection:
    db_path = get_db_path()
    db_dir = os.path.dirname(db_path) or "."

    Path(db_dir).mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                trace_id TEXT,
                actor TEXT,
                event_type TEXT NOT NULL,
                input_json TEXT,
                output_json TEXT,
                notes TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                meta_json TEXT,
                created_ts TEXT NOT NULL
            )
            """
        )

        conn.commit()
        conn.close()

    except Exception as exc:
        print(f"Database initialization skipped or failed: {exc}")
