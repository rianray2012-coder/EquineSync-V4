"""routes/admin_portal — Admin Portal router package.

Admin-7A.1 layered split (Feb 2026):
  - Shared helpers/constants live in `_helpers.py`.
  - All endpoints live in `portal.py`, clearly sectioned by surface
    (`# --- Admin-1`, `# --- Admin-2`, …, `# --- Admin-6`).
  - The per-surface 12-file split lands in a future Admin-7A.2 once
    this helper boundary is locked.

External import path (unchanged from the previous flat module):

    from routes.admin_portal import build_router
"""
from .portal import build_router

__all__ = ["build_router"]
