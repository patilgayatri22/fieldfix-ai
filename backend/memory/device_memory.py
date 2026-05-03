"""SQLite-backed repair history store."""

import sqlite3
from pathlib import Path

from pydantic import BaseModel

from backend.schemas.repair_output import RepairOutput

_DB_PATH = Path(__file__).parent.parent / "data" / "device_memory.db"


# ── Pydantic models ────────────────────────────────────────────────────────────

class RepairHistoryEntry(BaseModel):
    id: int
    device_id: str
    symptom: str
    category: str | None
    risk_level: str | None
    detected_item: str | None
    created_at: str


class RepairHistoryResponse(BaseModel):
    device_id: str
    total: int
    entries: list[RepairHistoryEntry]


# ── DB bootstrap ───────────────────────────────────────────────────────────────

def _get_conn() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS repair_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id   TEXT NOT NULL,
            symptom     TEXT NOT NULL,
            category    TEXT,
            risk_level  TEXT,
            detected_item TEXT,
            created_at  TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    return conn


# ── Public API ─────────────────────────────────────────────────────────────────

def save_repair(device_id: str, output: RepairOutput) -> RepairHistoryEntry:
    """Persist one repair result for a device."""
    conn = _get_conn()
    cur = conn.execute(
        """
        INSERT INTO repair_history (device_id, symptom, category, risk_level, detected_item)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            device_id,
            output.problem_summary,
            output.category.value if output.category else None,
            output.risk_level.value if output.risk_level else None,
            output.detected_item,
        ),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM repair_history WHERE id = ?", (cur.lastrowid,)
    ).fetchone()
    conn.close()
    return RepairHistoryEntry(**dict(row))


def get_history(device_id: str) -> list[RepairHistoryEntry]:
    """Return all repair history for a device, newest first."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT * FROM repair_history WHERE device_id = ? ORDER BY id DESC",
        (device_id,),
    ).fetchall()
    conn.close()
    return [RepairHistoryEntry(**dict(r)) for r in rows]


def clear_history(device_id: str) -> int:
    """Delete all history for a device. Returns count deleted."""
    conn = _get_conn()
    cur = conn.execute(
        "DELETE FROM repair_history WHERE device_id = ?", (device_id,)
    )
    conn.commit()
    count = cur.rowcount
    conn.close()
    return count
