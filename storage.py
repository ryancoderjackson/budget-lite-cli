from __future__ import annotations

import json
from pathlib import Path


DATA_FILE = Path("data.json")


def load_transactions() -> list[dict]:
    """Load transactions from data.json. Returns an empty list if file missing/empty/invalid."""
    if not DATA_FILE.exists():
        return []

    try:
        raw = DATA_FILE.read_text(encoding="utf-8").strip()
        if not raw:
            return []
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_transactions(transactions: list[dict]) -> None:
    """Save transactions to data.json (pretty-printed)."""
    DATA_FILE.write_text(json.dumps(transactions, indent=2), encoding="utf-8")
