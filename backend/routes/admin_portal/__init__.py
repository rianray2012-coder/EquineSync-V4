"""routes/admin_portal — Admin Portal router package.

Admin-7A.2b (Feb 2026):
  - Shared helpers/constants live in `_helpers.py`.
  - `portal.py` is a thin orchestrator.
  - Admin Portal endpoints live in per-surface modules such as
    `dashboard.py`, `facilities.py`, `horses.py`, and `reports.py`.

External import path (unchanged from the previous flat module):

    from routes.admin_portal import build_router
"""
from .portal import build_router

__all__ = ["build_router"]
