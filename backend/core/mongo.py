"""Mongo client options shared by the app and CLI scripts."""
from __future__ import annotations

from typing import Dict

import certifi


def mongo_client_kwargs(mongo_url: str) -> Dict[str, object]:
    """Return Atlas-safe Mongo client kwargs.

    Render's Python/OpenSSL stack can fail Atlas TLS negotiation when PyMongo
    falls back to a platform CA lookup. Pinning certifi keeps the connection
    path explicit without changing local Mongo behavior.
    """
    if mongo_url.startswith("mongodb+srv://"):
        return {"tlsCAFile": certifi.where()}
    return {}
