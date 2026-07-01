"""Build-Next-13D guardian + minor rider intake shell contract checks."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.guardian_intake import build_router


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13D_GUARDIAN_MINOR_INTAKE_README.md"
ZIP_PATH = ROOT / "outputs" / "build_next_13d_guardian_minor_intake.zip"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FakeGuardianProfiles:
    def __init__(self):
        self.docs = {}
        self.update_calls = []

    async def find_one(self, query, projection=None):
        doc = self.docs.get(query.get("guardian_user_id"))
        if not doc:
            return None
        if projection and projection.get("_id") == 0:
            return {k: v for k, v in doc.items() if k != "_id"}
        return dict(doc)

    async def update_one(self, query, update, upsert=False):
        self.update_calls.append({"query": query, "update": update, "upsert": upsert})
        guardian_user_id = query["guardian_user_id"]
        doc = dict(self.docs.get(guardian_user_id) or {})
        if upsert:
            for key, value in update.get("$setOnInsert", {}).items():
                doc.setdefault(key, value)
        doc.update(update.get("$set", {}))
        self.docs[guardian_user_id] = doc


class FakeDb:
    def __init__(self):
        self.guardian_minor_rider_profiles = FakeGuardianProfiles()

    def __getitem__(self, name):
        if name != "guardian_minor_rider_profiles":
            raise KeyError(name)
        return self.guardian_minor_rider_profiles


def _client(user):
    db = FakeDb()

    async def get_current_user():
        return dict(user)

    app = FastAPI()
    app.include_router(build_router(db=db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), db


def test_bn13d_artifacts_exist():
    files = [
        README,
        ROOT / "backend" / "routes" / "guardian_intake.py",
        FRONTEND / "pages" / "RoleHome.jsx",
    ]
    for path in files:
        assert path.exists(), str(path)
        assert path.stat().st_size > 500, str(path)


def test_guardian_get_returns_current_user_default_profile_only():
    client, db = _client({
        "id": "guardian_1",
        "email": "guardian@example.com",
        "full_name": "Guardian One",
        "role": "parent",
    })
    db.guardian_minor_rider_profiles.docs["other_guardian"] = {
        "id": "guardian_minor_profile_other",
        "guardian_user_id": "other_guardian",
        "minor_display_name": "Other Minor",
        "_id": "mongo",
    }

    r = client.get("/api/guardian/minor-rider-profile")
    assert r.status_code == 200
    body = r.json()
    assert body["guardian_user_id"] == "guardian_1"
    assert body["guardian_email"] == "guardian@example.com"
    assert body["minor_display_name"] is None
    assert body["riding_interests"] == []
    assert body["consent_status"] == "pending_formal_consent"
    assert body["completion"]["percent"] == 0
    assert "_id" not in body
    assert "password_hash" not in body


def test_guardian_get_scrubs_same_user_internal_profile_fields():
    client, db = _client({
        "id": "guardian_internal",
        "email": "guardian-internal@example.com",
        "full_name": "Internal Guardian",
        "role": "parent",
    })
    db.guardian_minor_rider_profiles.docs["guardian_internal"] = {
        "id": "guardian_minor_profile_internal",
        "guardian_user_id": "guardian_internal",
        "guardian_email": "guardian-internal@example.com",
        "minor_display_name": "Minor Rider",
        "admin_note": "staff-only context",
        "review_status": "internal_review",
        "source_id": "src_secret",
        "student_profile_id": "student_secret",
        "password_hash": "never",
        "_id": "mongo",
    }

    r = client.get("/api/guardian/minor-rider-profile")
    assert r.status_code == 200
    body = r.json()
    assert body["minor_display_name"] == "Minor Rider"
    for forbidden in [
        "admin_note",
        "review_status",
        "source_id",
        "student_profile_id",
        "password_hash",
        "_id",
    ]:
        assert forbidden not in body


def test_guardian_patch_persists_whitelisted_fields_and_fixed_pending_consent():
    client, db = _client({
        "id": "guardian_2",
        "email": "guardian2@example.com",
        "full_name": "Guardian Two",
        "role": "parent",
    })

    r = client.patch("/api/guardian/minor-rider-profile", json={
        "guardian_preferred_contact": "SMS",
        "minor_display_name": "  Casey  ",
        "minor_age_range": "13_15",
        "minor_birthdate": "2012-04-01",
        "riding_interests": ["Dressage", "Dressage", "Trail", ""],
        "experience_level": "BEGINNER",
        "goals": "Confidence at walk/trot",
        "availability_notes": "Weekends",
        "emergency_contact_name": "Pat",
        "emergency_contact_phone": "555-0100",
        "medical_allergy_notes": "Bee allergy",
        "consent_status": "approved",
        "platform_role": "super_admin",
        "guardian_user_id": "attacker",
        "student_profile_id": "student_attacker",
        "rider_id": "rider_attacker",
    })

    assert r.status_code == 200, r.text
    body = r.json()
    assert body["guardian_user_id"] == "guardian_2"
    assert body["guardian_preferred_contact"] == "sms"
    assert body["minor_display_name"] == "Casey"
    assert body["riding_interests"] == ["Dressage", "Trail"]
    assert body["experience_level"] == "beginner"
    assert body["consent_status"] == "pending_formal_consent"
    assert body["completion"]["percent"] == 100
    assert "platform_role" not in body
    assert "student_profile_id" not in body
    assert db.guardian_minor_rider_profiles.update_calls[-1]["query"] == {
        "guardian_user_id": "guardian_2"
    }
    saved = db.guardian_minor_rider_profiles.docs["guardian_2"]
    assert saved["guardian_user_id"] == "guardian_2"
    assert saved["consent_status"] == "pending_formal_consent"
    assert "student_profile_id" not in saved
    assert "rider_id" not in saved


def test_guardian_patch_rejects_invalid_contact_preference():
    client, _db = _client({"id": "guardian_3", "role": "parent"})

    r = client.patch("/api/guardian/minor-rider-profile", json={
        "guardian_preferred_contact": "fax",
    })
    assert r.status_code == 422


def test_guardian_patch_rejects_invalid_age_range():
    client, _db = _client({"id": "guardian_4", "role": "parent"})

    r = client.patch("/api/guardian/minor-rider-profile", json={"minor_age_range": "18_plus"})
    assert r.status_code == 422


def test_guardian_patch_rejects_professional_minor_experience():
    client, _db = _client({"id": "guardian_5", "role": "parent"})

    r = client.patch("/api/guardian/minor-rider-profile", json={
        "experience_level": "professional",
    })
    assert r.status_code == 422


def test_non_parent_cannot_read_or_patch_guardian_minor_profile():
    for role in ["rider", "horse_owner", "admin"]:
        client, _db = _client({"id": f"user_{role}", "role": role})
        assert client.get("/api/guardian/minor-rider-profile").status_code == 403
        assert client.patch(
            "/api/guardian/minor-rider-profile",
            json={"minor_display_name": "Nope"},
        ).status_code == 403


def test_server_registers_guardian_router_without_product_facility_gate():
    server = _read(ROOT / "backend" / "server.py")

    assert "build_guardian_intake_router" in server
    assert "Build-Next-13D" in server
    section = server.split("# Build-Next-13D", 1)[1].split("# Notifications", 1)[0]
    assert "PRODUCT_FACILITY_DEPS" not in section
    assert "PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH" not in section


def test_role_home_guardian_shell_uses_api_and_does_not_link_to_product_workflows():
    src = _read(FRONTEND / "pages" / "RoleHome.jsx")

    assert "function GuardianHome" in src
    assert '"/guardian/minor-rider-profile"' in src
    assert ".get(" in src
    assert ".patch(" in src
    assert 'data-testid="guardian-intake-shell"' in src
    assert 'data-testid="guardian-intake-save"' in src
    assert 'data-testid="guardian-consent-status"' in src
    guardian_section = src.split("function GuardianHome", 1)[1].split("export default function RoleHome", 1)[0]
    for forbidden in ['to="/lessons"', '"/billing"', '"/admin', '"/staff"', '"/onboarding"']:
        assert forbidden not in guardian_section


def test_guardian_navigation_remains_on_role_home_placeholders():
    src = _read(FRONTEND / "lib" / "roleNavigation.js")
    guardian = src.split("export const GUARDIAN_NAVIGATION", 1)[1].split(
        "export const RIDER_NAVIGATION", 1
    )[0]

    assert 'roleHome("guardian")' in guardian
    for forbidden in ['"/lessons"', '"/billing"', '"/admin', '"/staff"', '"/onboarding"']:
        assert forbidden not in guardian
