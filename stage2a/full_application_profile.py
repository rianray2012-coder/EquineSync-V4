#!/usr/bin/env python3
"""Stage 2A wrapper for the complete EquineSync application.

The repository's development startup normally materializes local billing
catalog documents even when no provider credential is configured.  Stage 2A
requires zero startup document writes, so this wrapper disables only that
catalog materialization before importing the otherwise unchanged application.
Index metadata creation remains enabled and is inventoried by validation.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
BACKEND = REPO / "backend"
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(ROOT))

from lib.control import ALLOWED_NAMES, load_env, validate_env  # noqa: E402

# ``load_env`` performs the ambient-secret and backend-dotenv denials.  The
# second validation is deliberately against the process environment so a
# caller cannot import this wrapper without actually applying the profile.
load_env()
runtime_environment = {name: value for name, value in os.environ.items() if name in ALLOWED_NAMES}
validate_env(runtime_environment)

from core import billing_provisioning  # noqa: E402


async def _stage2a_catalog_noop(_db) -> None:
    """Prohibit development catalog document writes in this disposable run."""
    return None


billing_provisioning.ensure_stripe_catalog = _stage2a_catalog_noop

from server import app  # noqa: E402,F401
