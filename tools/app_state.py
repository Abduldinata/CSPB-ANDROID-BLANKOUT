from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / ".cache"


def _ensure_cache_dir() -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def cache_file(name: str) -> Path:
    _ensure_cache_dir()
    return CACHE_DIR / name


def load_json(name: str, default: Any) -> Any:
    path = cache_file(name)
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(name: str, data: Any) -> None:
    path = cache_file(name)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def append_history(name: str, entry: dict[str, Any], limit: int = 50) -> list[dict[str, Any]]:
    items = load_json(name, [])
    if not isinstance(items, list):
        items = []
    items.insert(0, entry)
    items = items[:limit]
    save_json(name, items)
    return items


def clear_cache() -> None:
    if not CACHE_DIR.exists():
        return
    for item in CACHE_DIR.glob("*"):
        if item.is_file():
            item.unlink(missing_ok=True)
