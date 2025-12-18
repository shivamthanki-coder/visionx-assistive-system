"""
visionx.utils
Shared helper utilities: structured logging, JSONL append, time helpers.
Human-style comments and simple, predictable behavior.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict

def now_ts() -> str:
    """Return an ISO-like timestamp (UTC)."""
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

def ensure_dir(path):
    """Ensure directory exists (Path or str)."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def append_jsonl(path, obj: Dict[str, Any]):
    """
    Append a dictionary as a single JSON line to path.
    Uses atomic write semantics (open in append mode).
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a") as f:
        f.write(json.dumps(obj, default=str) + "\\n")

def safe_get(obj: dict, keys, default=None):
    """Get first present key from keys (iterable) in obj, else default."""
    for k in keys:
        if k in obj and obj[k] is not None:
            return obj[k]
    return default
