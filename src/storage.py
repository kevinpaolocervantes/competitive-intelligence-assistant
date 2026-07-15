from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SNAPSHOT_DIR = Path("data/snapshots")


def _safe_name(name: str) -> str:
    return "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")


def snapshot_path(competitor: str) -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    return SNAPSHOT_DIR / f"{_safe_name(competitor)}.json"


def load_history(competitor: str) -> list[dict[str, Any]]:
    path = snapshot_path(competitor)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_run(competitor: str, run: dict[str, Any]) -> None:
    history = load_history(competitor)
    history.append(run)
    snapshot_path(competitor).write_text(
        json.dumps(history, indent=2), encoding="utf-8"
    )
