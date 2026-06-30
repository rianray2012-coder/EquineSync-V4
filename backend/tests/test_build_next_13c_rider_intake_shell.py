"""Build-Next-13C rider intake shell contract checks."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.rider_profile import build_router


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13C_RIDER_INTAKE_README.md"
ZIP_PATH = ROOT / "outputs" / "build_next_13c_rider_intake_shell.zip"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FakeRiderProfiles:
    def __init__(self):
        self.docs = {}
        self.update_calls = []

    async def find_one(self, query, projection=None):
        doc = self.docs.get(query.get("user_id"))
        if not doc:
            return None
        if projection and projection.get("_id") == 0:
            return {k: v for k, v in doc.items() if k != "_id"}
        return dict(doc)

    async def update_one(self, query, update, upsert=False):
        self.update_calls.append({"query": query, "update": update, "upsert": upsert})
        user_id = query["user_id"]
        doc = dict(self.docs.get(user_id) or {})
        if upsert:
            for key, value in update.get("$setOnInsert", {}).items():
                doc.setdefault(key, value)
        doc.update(update.get("$set", {}))
        self.docs[user_id] = doc


class FakeDb:
    def __init__(self):
        self.rider_profiles = FakeRiderProfiles()

    def __getitem__(self, name):
        if name != "rider_profiles":
            raise KeyError(name)
        return self.rider_profiles


def _client(user):
    db = FakeDb()

    async def get_current_user():
        return dict(user)

    app = FastAPI()
    app.include_router(build_router(db=db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), db


def test_bn13c_artifacts_exist():
    files = [
        README,
        ROOT / "backend" / "routes" / "rider_profile.py",
        FRONTEND / "pages" / "RoleHome.jsx",
    ]
    for path in files:
        assert path.exists(), str(path)
        assert path.stat().st_size > 500, str(path)


def test_rider_get_returns_current_user_default_profile_only():
    client, db = _client({
        "id": "rider_1",
        "email": "rider@example.com",
        "full_name": "Rider One",
        "role": "rider",
    })
    db.rider_profiles.docs["other_user"] = {
        "id": "rider_profile_other",
        "user_id": "other_user",
        "preferred_name": "Other",
        "_id": "mongo",
    }

    r = client.get("/api/rider/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "rider_1"
    assert body["email"] == "rider@example.com"
    assert body["preferred_name"] is None
    assert body["disciplines"] == []
    assert body["consent_acknowledged"] is False
    assert body["completion"]["percent"] == 0
    assert "_id" not in body
    assert "password_hash" not in body


def test_rider_get_scrubs_same_user_internal_profile_fields():
    client, db = _client({
        "id": "rider_internal",
        "email": "rider-internal@example.com",
        "full_name": "Internal Rider",
        "role": "rider",
    })
    db.rider_profiles.docs["rider_internal"] = {
        "id": "rider_profile_internal",
        "user_id": "rider_internal",
        "email": "rider-internal@example.com",
        "full_name": "Internal Rider",
        "preferred_name": "IR",
        "disciplines": ["Dressage"],
        "experience_level": "beginner",
        "admin_note": "staff-only context",
        "review_status": "internal_review",
        "source_id": "src_secret",
        "password_hash": "never",
        "_id": "mongo",
    }

    r = client.get("/api/rider/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["preferred_name"] == "IR"
    for forbidden in ["admin_note", "review_status", "source_id", "password_hash", "_id"]:
        assert forbidden not in body


def test_rider_patch_persists_whitelisted_profile_fields_and_completion():
    client, db = _client({
        "id": "rider_2",
        "email": "rider2@example.com",
        "full_name": "Rider Two",
        "role": "rider",
    })

    r = client.patch("/api/rider/profile", json={
        "preferred_name": "  RJ  ",
        "disciplines": ["Dressage", "Dressage", "Trail", ""],
        "experience_level": "INTERMEDIATE",
        "goals": "Canter with confidence",
        "availability_notes": "Weekends",
        "emergency_contact_name": "Pat",
        "emergency_contact_phone": "555-0100",
        "consent_acknowledged": True,
        "platform_role": "super_admin",
        "user_id": "attacker",
    })

    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user_id"] == "rider_2"
    assert body["preferred_name"] == "RJ"
    assert body["disciplines"] == ["Dressage", "Trail"]
    assert body["experience_level"] == "intermediate"
    assert body["consent_acknowledged"] is True
    assert body["completion"]["percent"] == 100
    assert "platform_role" not in body
    assert db.rider_profiles.update_calls[-1]["query"] == {"user_id": "rider_2"}
    assert db.rider_profiles.docs["rider_2"]["user_id"] == "rider_2"


def test_rider_patch_rejects_invalid_experience_level():
    client, _db = _client({"id": "rider_3", "role": "rider"})

    r = client.patch("/api/rider/profile", json={"experience_level": "wizard"})
    assert r.status_code == 422


def test_non_rider_cannot_read_or_patch_rider_profile():
    client, _db = _client({"id": "owner_1", "role": "horse_owner"})

    assert client.get("/api/rider/profile").status_code == 403
    assert client.patch("/api/rider/profile", json={"preferred_name": "Nope"}).status_code == 403


def test_server_registers_rider_profile_router_without_product_facility_gate():
    server = _read(ROOT / "backend" / "server.py")

    assert "build_rider_profile_router" in server
    assert "Build-Next-13C" in server
    section = server.split("# Build-Next-13C", 1)[1].split("# Notifications", 1)[0]
    assert "PRODUCT_FACILITY_DEPS" not in section
    assert "PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH" not in section


def test_role_home_rider_shell_uses_api_and_does_not_link_to_lessons():
    src = _read(FRONTEND / "pages" / "RoleHome.jsx")

    assert "function RiderHome" in src
    assert '"/rider/profile"' in src
    assert ".get(" in src
    assert ".patch(" in src
    assert 'data-testid="rider-intake-shell"' in src
    assert 'data-testid="rider-profile-save"' in src
    rider_section = src.split("function RiderHome", 1)[1].split("export default function RoleHome", 1)[0]
    assert 'to="/lessons"' not in rider_section
    assert '"/admin' not in rider_section
    assert "DocuSign" not in rider_section


def test_rider_navigation_remains_on_role_home_placeholders():
    src = _read(FRONTEND / "lib" / "roleNavigation.js")
    rider = src.split("export const RIDER_NAVIGATION", 1)[1].split("export const DEFAULT_NAVIGATION", 1)[0]

    assert 'roleHome("rider")' in rider
    assert '"/lessons"' not in rider
    assert '"/admin' not in rider
    assert '"/billing"' not in rider
