"""Build-Next-13F barn owner intake shell contract checks."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.barn_owner_intake import build_router


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13F_BARN_OWNER_INTAKE_README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FakeBarnOwnerProfiles:
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
        self.barn_owner_intake_profiles = FakeBarnOwnerProfiles()

    def __getitem__(self, name):
        if name != "barn_owner_intake_profiles":
            raise KeyError(name)
        return self.barn_owner_intake_profiles


def _client(user):
    db = FakeDb()

    async def get_current_user():
        return dict(user)

    app = FastAPI()
    app.include_router(build_router(db=db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), db


def test_bn13f_artifacts_exist():
    files = [
        README,
        ROOT / "backend" / "routes" / "barn_owner_intake.py",
        FRONTEND / "pages" / "RoleHome.jsx",
        FRONTEND / "lib" / "roleLanding.js",
    ]
    for path in files:
        assert path.exists(), str(path)
        assert path.stat().st_size > 500, str(path)


def test_barn_owner_get_returns_current_user_default_profile_only():
    client, db = _client({
        "id": "barn_owner_1",
        "email": "founder@example.com",
        "full_name": "Founder One",
        "role": "barn_owner",
    })
    db.barn_owner_intake_profiles.docs["other_founder"] = {
        "id": "barn_owner_intake_other",
        "user_id": "other_founder",
        "facility_name": "Other Barn",
        "_id": "mongo",
    }

    r = client.get("/api/barn-owner-intake/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "barn_owner_1"
    assert body["email"] == "founder@example.com"
    assert body["facility_name"] is None
    assert body["services_offered"] == []
    assert body["completion"]["percent"] == 0
    assert "_id" not in body
    assert "password_hash" not in body


def test_barn_owner_get_scrubs_same_user_internal_profile_fields():
    client, db = _client({
        "id": "barn_owner_internal",
        "email": "founder-internal@example.com",
        "full_name": "Internal Founder",
        "role": "barn_owner",
    })
    db.barn_owner_intake_profiles.docs["barn_owner_internal"] = {
        "id": "barn_owner_intake_internal",
        "user_id": "barn_owner_internal",
        "facility_name": "Hidden Creek",
        "admin_note": "staff-only context",
        "review_status": "internal_review",
        "source_id": "src_secret",
        "stripe_customer_id": "cus_secret",
        "subscription_status": "active",
        "barn_id": "barn_secret",
        "facility_id": "facility_secret",
        "onboarding_step": "invite_staff",
        "staff_invites": [{"email": "staff@example.com"}],
        "entitlements": {"horses": 50},
        "password_hash": "never",
        "_id": "mongo",
    }

    r = client.get("/api/barn-owner-intake/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["facility_name"] == "Hidden Creek"
    for forbidden in [
        "admin_note",
        "review_status",
        "source_id",
        "stripe_customer_id",
        "subscription_status",
        "barn_id",
        "facility_id",
        "onboarding_step",
        "staff_invites",
        "entitlements",
        "password_hash",
        "_id",
    ]:
        assert forbidden not in body


def test_barn_owner_patch_persists_whitelisted_fields_and_ignores_product_fields():
    client, db = _client({
        "id": "barn_owner_2",
        "email": "founder2@example.com",
        "full_name": "Founder Two",
        "role": "barn_owner",
    })

    r = client.patch("/api/barn-owner-intake/profile", json={
        "preferred_name": "  Jordan  ",
        "preferred_contact": "SMS",
        "facility_name": "  North Star Farm  ",
        "facility_city_state": "Lexington, KY",
        "facility_type": "LESSON_PROGRAM",
        "horse_count_range": "11_30",
        "staff_count_range": "1_3",
        "services_offered": ["Lessons", "Lessons", "Boarding", ""],
        "setup_goals": "Move owner communication and care coordination into one place.",
        "timeline": "30_DAYS",
        "notes": "Need careful rollout.",
        "user_id": "attacker",
        "barn_id": "barn_attacker",
        "facility_id": "facility_attacker",
        "platform_role": "super_admin",
        "stripe_customer_id": "cus_attacker",
        "subscription_status": "active",
        "onboarding_step": "done",
        "staff_invites": [{"email": "x@example.com"}],
        "entitlements": {"horses": 999},
    })

    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user_id"] == "barn_owner_2"
    assert body["preferred_name"] == "Jordan"
    assert body["preferred_contact"] == "sms"
    assert body["facility_name"] == "North Star Farm"
    assert body["facility_type"] == "lesson_program"
    assert body["horse_count_range"] == "11_30"
    assert body["staff_count_range"] == "1_3"
    assert body["services_offered"] == ["Lessons", "Boarding"]
    assert body["timeline"] == "30_days"
    assert body["completion"]["percent"] == 100
    for forbidden in [
        "barn_id",
        "facility_id",
        "platform_role",
        "stripe_customer_id",
        "subscription_status",
        "onboarding_step",
        "staff_invites",
        "entitlements",
    ]:
        assert forbidden not in body
    assert db.barn_owner_intake_profiles.update_calls[-1]["query"] == {"user_id": "barn_owner_2"}
    saved = db.barn_owner_intake_profiles.docs["barn_owner_2"]
    assert saved["user_id"] == "barn_owner_2"
    assert "barn_id" not in saved
    assert "staff_invites" not in saved


def test_barn_owner_patch_rejects_invalid_enums_and_non_string_values():
    client, _db = _client({"id": "barn_owner_3", "role": "barn_owner"})

    assert client.patch("/api/barn-owner-intake/profile", json={"facility_type": "enterprise"}).status_code == 422
    assert client.patch("/api/barn-owner-intake/profile", json={"preferred_contact": "fax"}).status_code == 422
    assert client.patch("/api/barn-owner-intake/profile", json={"horse_count_range": "500"}).status_code == 422
    assert client.patch("/api/barn-owner-intake/profile", json={"staff_count_range": "100"}).status_code == 422
    assert client.patch("/api/barn-owner-intake/profile", json={"timeline": "yesterday"}).status_code == 422
    assert client.patch("/api/barn-owner-intake/profile", json={"preferred_name": 123}).status_code == 422


def test_non_barn_owner_cannot_read_or_patch_barn_owner_intake():
    for role in ["admin", "horse_owner", "parent", "barn_manager", "rider"]:
        client, _db = _client({"id": f"user_{role}", "role": role})
        assert client.get("/api/barn-owner-intake/profile").status_code == 403
        assert client.patch(
            "/api/barn-owner-intake/profile",
            json={"facility_name": "Nope"},
        ).status_code == 403


def test_server_registers_barn_owner_router_without_product_facility_gate():
    server = _read(ROOT / "backend" / "server.py")

    assert "build_barn_owner_intake_router" in server
    assert "Build-Next-13F" in server
    section = server.split("# Build-Next-13F", 1)[1].split("# Notifications", 1)[0]
    assert "PRODUCT_FACILITY_DEPS" not in section
    assert "PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH" not in section


def test_role_landing_routes_barn_owner_to_intake_home_without_breaking_admin_setup():
    src = _read(FRONTEND / "lib" / "roleLanding.js")

    assert 'barnOwner: "/role-home/barn-owner"' in src
    assert 'if (role === "barn_owner") return ROLE_HOME_PATHS.barnOwner;' in src
    assert 'export const SETUP_ELIGIBLE_ROLES = ["admin", "barn_owner"];' in src
    assert 'if (role === "admin")' in src
    assert 'return "/onboarding";' in src


def test_role_home_barn_owner_shell_uses_api_and_does_not_link_to_product_workflows():
    src = _read(FRONTEND / "pages" / "RoleHome.jsx")

    assert "function BarnOwnerHome" in src
    assert '"/barn-owner-intake/profile"' in src
    assert ".get(" in src
    assert ".patch(" in src
    assert 'data-testid="barn-owner-intake-shell"' in src
    assert 'data-testid="barn-owner-intake-save"' in src
    barn_owner_section = src.split("function BarnOwnerHome", 1)[1].split("function OwnerHome", 1)[0]
    for forbidden in [
        'to="/onboarding"',
        '"/billing"',
        '"/admin',
        '"/staff"',
        '"/invites"',
        '"/checkout"',
        '"/subscriptions"',
        '"/forms-signatures"',
        '"/horses"',
    ]:
        assert forbidden not in barn_owner_section


def test_barn_owner_navigation_keeps_high_risk_workflows_out_of_role_home_nav():
    src = _read(FRONTEND / "lib" / "roleNavigation.js")
    barn_owner = src.split("export const BARN_OWNER_NAVIGATION", 1)[1].split(
        "export const STAFF_NAVIGATION", 1
    )[0]

    assert 'item("/onboarding", "Setup", "sparkles")' in barn_owner
    for forbidden in ['"/admin', '"/billing"', '"/staff"']:
        assert forbidden not in barn_owner
