from __future__ import annotations

import hashlib
import re
from typing import Any, Dict

import orjson


SPACE_RE = re.compile(r"\s+")


def _normalize_text(value: str | None) -> str | None:
    if value is None:
        return None
    return SPACE_RE.sub(" ", value.strip())


def canonical_book_state(data: Dict[str, Any]) -> Dict[str, Any]:
    canonical = {
        "name": _normalize_text(data.get("name")),
        "description": _normalize_text(data.get("description")),
        "category": _normalize_text(data.get("category")),
        "price_excl_tax": round(float(data.get("price_excl_tax")) if data.get("price_excl_tax") is not None else 0.0, 2),
        "price_incl_tax": round(float(data.get("price_incl_tax")) if data.get("price_incl_tax") is not None else 0.0, 2),
        "availability": int(data.get("availability") or 0),
        "num_reviews": int(data.get("num_reviews") or 0),
        "image_url": data.get("image_url"),
        "rating": int(data.get("rating") or 0),
    }
    return canonical


def content_hash(data: Dict[str, Any]) -> str:
    canonical = canonical_book_state(data)
    blob = orjson.dumps(canonical, option=orjson.OPT_SORT_KEYS)
    digest = hashlib.sha256(blob).hexdigest()
    return f"sha256:{digest}"
