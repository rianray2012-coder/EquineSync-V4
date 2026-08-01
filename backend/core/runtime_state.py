"""Phase 10B — tiny in-process runtime state for readiness reporting.

Pure process state: no DB, no external calls, no secrets. Written by the
application lifecycle (`core/lifespan.py`) and read by the readiness probe
(`routes/system.py`). Safe to import from both — no circular dependency.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Optional

_started_at_iso: Optional[str] = None
_started_monotonic: Optional[float] = None
_indexes_ensured: bool = False
_stripe_catalog_ready: Optional[bool] = None
_stripe_catalog_environment: Optional[str] = None
_stripe_catalog_verified_at: Optional[str] = None
_stripe_catalog_blockers: list[str] = []


def mark_started() -> None:
    global _started_at_iso, _started_monotonic
    _started_at_iso = datetime.now(timezone.utc).isoformat()
    _started_monotonic = time.monotonic()


def mark_indexes_ensured() -> None:
    global _indexes_ensured
    _indexes_ensured = True


def mark_stripe_catalog(
    *,
    ready: bool,
    environment: str,
    verified_at: Optional[str] = None,
    blockers: Optional[list[str]] = None,
) -> None:
    global _stripe_catalog_ready
    global _stripe_catalog_environment
    global _stripe_catalog_verified_at
    global _stripe_catalog_blockers
    _stripe_catalog_ready = bool(ready)
    _stripe_catalog_environment = environment
    _stripe_catalog_verified_at = verified_at
    _stripe_catalog_blockers = list(blockers or [])


def snapshot() -> dict:
    """Additive, no-secret readiness fields."""
    uptime = None
    if _started_monotonic is not None:
        uptime = round(time.monotonic() - _started_monotonic, 1)
    return {
        "started_at": _started_at_iso,
        "uptime_seconds": uptime,
        "indexes_ensured": _indexes_ensured,
        "stripe_catalog_ready": _stripe_catalog_ready,
        "stripe_catalog_environment": _stripe_catalog_environment,
        "stripe_catalog_verified_at": _stripe_catalog_verified_at,
        "stripe_catalog_blockers": list(_stripe_catalog_blockers),
    }
