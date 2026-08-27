"""Opt-in OpenAI live extraction proof for the draft-only AI lane.

Default behavior is non-networking: without RUN_AI_LIVE_EXTRACTION_PROOF=1 and
OPENAI_API_KEY, the script prints a redacted blocked snapshot and exits 0.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.testclient import TestClient

BACKEND_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from routes.ai_assistant import build_router  # noqa: E402
from services.ai_draft_extractor import (  # noqa: E402
    OpenAIDraftExtractor,
    ai_live_extraction_verification_snapshot,
)


class _Cursor:
    def __init__(self, rows: List[Dict[str, Any]]):
        self.rows = rows

    def sort(self, key, direction):
        self.rows = sorted(
            self.rows,
            key=lambda row: str(row.get(key) or ""),
            reverse=direction < 0,
        )
        return self

    def limit(self, limit):
        self.rows = self.rows[:limit]
        return self

    async def to_list(self, length):
        return self.rows[:length]


class _Collection:
    def __init__(self):
        self.rows: List[Dict[str, Any]] = []

    async def insert_one(self, doc):
        self.rows.append(dict(doc))

    async def find_one(self, query, projection=None):
        for row in self.rows:
            if all(row.get(k) == v for k, v in query.items()):
                return _project(row, projection)
        return None

    async def update_one(self, query, update):
        for row in self.rows:
            if all(row.get(k) == v for k, v in query.items()):
                row.update((update or {}).get("$set", {}))
                return

    def find(self, query, projection=None):
        return _Cursor([
            _project(row, projection)
            for row in self.rows
            if all(row.get(k) == v for k, v in (query or {}).items())
        ])


class _Db(dict):
    def __getitem__(self, name):
        if name not in self:
            self[name] = _Collection()
        return dict.__getitem__(self, name)


def _project(row, projection):
    out = dict(row)
    if projection:
        for key, include in projection.items():
            if include == 0:
                out.pop(key, None)
    return out


async def _audit_record(**kwargs):
    return None


async def _current_user():
    return {
        "id": "ai_live_proof_user",
        "role": "barn_manager",
        "barn_id": "ai_live_proof_barn",
        "email": "ai-live-proof@equinesync.invalid",
    }


def _app(db):
    app = FastAPI()
    app.include_router(
        build_router(
            db=db,
            get_current_user=_current_user,
            extractor=OpenAIDraftExtractor(),
            audit_record=_audit_record,
        ),
        prefix="/api",
    )
    return app


def main() -> int:
    snapshot = ai_live_extraction_verification_snapshot()
    if not snapshot["ready_to_run_live_proof"]:
        print(json.dumps({
            "status": "blocked",
            "reason": "Set RUN_AI_LIVE_EXTRACTION_PROOF=1 and OPENAI_API_KEY to run the live proof.",
            "snapshot": snapshot,
        }, indent=2, sort_keys=True))
        return 0

    db = _Db()
    with TestClient(_app(db)) as client:
        response = client.post("/api/ai/draft-jobs", json={
            "source_type": "service_invoice",
            "requested_output": "draft_service_history",
            "prompt": (
                "Extract draft service-history candidates only. Return JSON only. "
                "Do not save official records."
            ),
            "source_text": (
                "Seeded live proof source: On 2026-08-20, Cedar Creek Farrier "
                "trimmed horse River for 85.00 USD. Payment status is unknown."
            ),
        })
        if response.status_code != 201:
            print(json.dumps({
                "status": "failed",
                "stage": "create_draft_job",
                "http_status": response.status_code,
                "body": response.text[:500],
                "snapshot": snapshot,
            }, indent=2, sort_keys=True))
            return 1
        job = response.json()["job"]
        review = client.post(f"/api/ai/draft-jobs/{job['id']}/review", json={
            "action": "approved_no_save",
            "note": "Live extraction proof only. No official save authority.",
        })
        if review.status_code != 200:
            print(json.dumps({
                "status": "failed",
                "stage": "review_no_save",
                "http_status": review.status_code,
                "body": review.text[:500],
                "snapshot": snapshot,
            }, indent=2, sort_keys=True))
            return 1

    official_collections = [
        "inventory_items",
        "invoices",
        "horse_health_records",
        "service_history",
        "tasks",
        "payments",
    ]
    official_rows = {
        name: len(db[name].rows)
        for name in official_collections
        if name in db
    }
    passed = (
        job["draft_only"] is True
        and job["review_required"] is True
        and job["status"] in {"draft_ready", "draft_needs_manual_review"}
        and review.json()["review"]["official_records_written"] is False
        and not any(official_rows.values())
    )
    print(json.dumps({
        "status": "pass" if passed else "failed",
        "snapshot": snapshot,
        "job_status": job["status"],
        "review_action": review.json()["review"]["action"],
        "official_records_written": review.json()["review"]["official_records_written"],
        "official_collection_rows": official_rows,
    }, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

