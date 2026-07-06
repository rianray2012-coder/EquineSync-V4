from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

os.environ.setdefault("MONGO_URL", "mongodb" + "://127.0.0.1:27017/?serverSelectionTimeoutMS=3000")
os.environ.setdefault("DB_NAME", "test_database")

from core.rf3_onboarding_import_setup_proof import build_rf3_proof, render_rf3_report
from routes.onboarding import build_router


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _section(source: str, start: str, end: str) -> str:
    start_at = source.index(start)
    end_at = source.index(end, start_at)
    return source[start_at:end_at]


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)

    async def to_list(self, length=100):
        return [dict(row) for row in self.rows[:length]]


class FakeCollection:
    def __init__(self, rows=None):
        self.rows = [dict(row) for row in (rows or [])]

    async def find_one(self, filt, projection=None):
        for row in self.rows:
            if _matches(row, filt):
                return _project(row, projection)
        return None

    def find(self, filt, projection=None):
        return FakeCursor([_project(row, projection) for row in self.rows if _matches(row, filt)])

    async def count_documents(self, filt):
        return sum(1 for row in self.rows if _matches(row, filt))

    async def insert_one(self, doc):
        self.rows.append(dict(doc))
        return None

    async def update_one(self, filt, update, upsert=False):
        for row in self.rows:
            if _matches(row, filt):
                _apply_update(row, update)
                return None
        if upsert:
            doc = dict(filt)
            _apply_update(doc, update)
            self.rows.append(doc)
        return None

    async def delete_one(self, filt):
        self.rows = [row for row in self.rows if not _matches(row, filt)]
        return None


class FakeDb:
    def __init__(self):
        for name in [
            "barn",
            "feed_templates",
            "horses",
            "inventory",
            "locations",
            "onboarding_progress",
            "owners",
            "riders",
            "staff_invites",
        ]:
            setattr(self, name, FakeCollection())

    def __getitem__(self, name):
        return getattr(self, name)


def _project(row, projection):
    if not projection:
        return dict(row)
    if projection.get("_id") == 0 and len(projection) == 1:
        return {k: v for k, v in row.items() if k != "_id"}
    selected = {k: row.get(k) for k, include in projection.items() if include and k in row}
    if projection.get("_id") == 0:
        selected.pop("_id", None)
    return selected


def _matches(row, filt):
    for key, expected in (filt or {}).items():
        actual = row.get(key)
        if isinstance(expected, dict):
            if "$in" in expected and actual not in expected["$in"]:
                return False
            if "$ne" in expected and actual == expected["$ne"]:
                return False
        elif actual != expected:
            return False
    return True


def _apply_update(row, update):
    for key, value in (update or {}).get("$set", {}).items():
        target = row
        parts = key.split(".")
        for part in parts[:-1]:
            target = target.setdefault(part, {})
        target[parts[-1]] = value


def _app(db: FakeDb) -> TestClient:
    async def get_current_user():
        return {"id": "u_admin", "role": "admin", "barn_id": "barn_a", "full_name": "Admin User"}

    def require_setup_role(user):
        if user.get("role") not in {"admin", "barn_manager", "barn_owner"}:
            raise AssertionError("setup role required")

    async def list_collection(name, filt):
        return await getattr(db, name).find(filt, {"_id": 0}).to_list(1000)

    app = FastAPI()
    app.include_router(build_router(
        db=db,
        get_current_user=get_current_user,
        require_setup_role=require_setup_role,
        roles=["admin", "barn_manager", "barn_owner", "trainer", "groom"],
        list_collection=list_collection,
        clean=lambda doc: dict(doc),
        new_id=lambda: f"id_{sum(len(getattr(db, name).rows) for name in ['horses', 'owners']) + 1}",
    ))
    return TestClient(app)


def test_rf3_csv_preview_is_review_first_and_non_mutating():
    db = FakeDb()
    db.horses.rows.append({"id": "h_existing", "barn_id": "barn_a", "name": "River"})
    client = _app(db)

    response = client.post(
        "/onboarding/csv-preview",
        json={"kind": "horses", "csv_text": "name,breed\nRiver,Welsh\nBlue,Hunter\n"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["review_required"] is True
    assert data["commit_allowed"] is True
    assert data["import_kind_status"] == "active"
    assert data["duplicates"] == ["River"]
    assert data["review_summary"]["warnings"] == 1
    assert data["review_summary"]["ready"] == 1
    assert len(db.horses.rows) == 1


def test_rf3_owner_preview_warns_on_duplicate_email_even_with_full_name():
    db = FakeDb()
    db.owners.rows.append({
        "id": "owner_existing",
        "barn_id": "barn_a",
        "full_name": "Existing Owner",
        "email": "owner@example.com",
    })
    client = _app(db)

    response = client.post(
        "/onboarding/csv-preview",
        json={"kind": "owners", "csv_text": "full_name,email\nOwner One,owner@example.com\nOwner Two,new@example.com\n"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["duplicates"] == ["owner@example.com"]
    assert data["review_summary"]["warnings"] == 1
    assert data["review_summary"]["ready"] == 1
    assert data["row_reviews"][0]["status"] == "warning"
    assert data["row_reviews"][1]["status"] == "ready"
    assert len(db.owners.rows) == 1


def test_rf3_csv_commit_requires_review_marker_before_mutation():
    db = FakeDb()
    client = _app(db)
    payload = {"kind": "owners", "rows": [{"full_name": "Owner One", "email": "owner@example.com"}]}

    blocked = client.post("/onboarding/csv-commit", json=payload)
    allowed = client.post("/onboarding/csv-commit", json={**payload, "reviewed": True})

    assert blocked.status_code == 409
    assert blocked.json()["detail"]["review_required"] is True
    assert allowed.status_code == 200, allowed.text
    assert allowed.json()["reviewed"] is True
    assert allowed.json()["created"] == 1
    assert db.owners.rows[0]["full_name"] == "Owner One"


def test_rf3_deferred_import_kinds_are_explicit_not_fake_live():
    db = FakeDb()
    client = _app(db)

    preview = client.post("/onboarding/csv-preview", json={"kind": "service_providers", "csv_text": "name,email\nVet,v@example.com\n"})
    commit = client.post("/onboarding/csv-commit", json={"kind": "service_providers", "rows": [], "reviewed": True})

    assert preview.status_code == 200
    assert preview.json()["import_kind_status"] == "deferred"
    assert preview.json()["commit_allowed"] is False
    assert "RF10" in preview.json()["deferred_reason"]
    assert commit.status_code == 409
    assert commit.json()["detail"]["kind"] == "service_providers"


def test_rf3_source_contracts_pin_review_first_import_and_setup_truth():
    onboarding = _read("backend/routes/onboarding.py")
    records_step = _read("frontend/src/components/onboarding/RecordsStep.jsx")
    onboarding_page = _read("frontend/src/pages/Onboarding.jsx")
    backlog = _read("backend/routes/backlog.py")

    preview = _section(
        onboarding,
        '@router.post("/onboarding/csv-preview")',
        '@router.post("/onboarding/csv-commit")',
    )
    commit = _section(
        onboarding,
        '@router.post("/onboarding/csv-commit")',
        '@router.get("/onboarding/csv-template")',
    )

    assert "RF3_ACTIVE_IMPORT_KINDS" in onboarding
    assert "RF3_DEFERRED_IMPORT_KINDS" in onboarding
    assert "row_reviews" in preview
    assert "review_summary" in preview
    assert "insert_one" not in preview
    assert "if not body.reviewed" in commit
    assert "CSV import must be previewed and reviewed before commit" in commit
    assert "reviewed: true" in records_step
    assert "preview.commit_allowed === false" in records_step
    assert 'api.get("/onboarding/readiness")' in onboarding_page
    assert "BN16B_REQUIRED_STEP_IDS" in onboarding
    assert "credentials_required" in backlog
    assert "Credentials and webhook configuration are required before live sync is enabled." in backlog


def test_rf3_proof_report_renders_ready_without_blockers():
    report = build_rf3_proof(ROOT)
    rendered = render_rf3_report(report)

    assert report["overall_status"] == "ready"
    assert report["status_counts"]["ready"] >= 7
    assert report["status_counts"]["deferred"] >= 1
    assert "RF3 Onboarding Import Setup Report" in rendered
    assert "## Founder Decision Rows" in rendered
    assert "horses and owners only" in rendered
