from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DB_PATH = DATA / "trt4.db"
SCHEMA = DATA / "schema.sql"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    # Conexões curtas por chamada; timeout/WAL evitam lock sob reruns do Streamlit.
    conn = sqlite3.connect(str(path), timeout=30.0)
    try:
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 30000")
        conn.execute("PRAGMA journal_mode = WAL")
    except Exception:
        conn.close()
        raise
    return conn


def init_db(db_path: Path | None = None) -> Path:
    path = db_path or DB_PATH
    schema = SCHEMA.read_text(encoding="utf-8")
    with connect(path) as conn:
        conn.executescript(schema)
        conn.commit()
    return path


def count_questoes(db_path: Path | None = None) -> int:
    with connect(db_path) as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM sqlite_master WHERE type='table' AND name='questoes'"
        ).fetchone()
        if not row or row["n"] == 0:
            return 0
        return int(conn.execute("SELECT COUNT(*) AS c FROM questoes").fetchone()["c"])
