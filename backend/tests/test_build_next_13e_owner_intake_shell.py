"""Build-Next-13E owner intake shell contract checks."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.owner_intake import build_router


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13E_OWNER_INTAKE_README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FakeOwnerProfiles:
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
        self.owner_intake_profiles = FakeOwnerProfiles()

    def __getitem__(self, name):
        if name != "owner_intake_profiles":
            raise KeyError(name)
        return self.owner_intake_profiles


def _client(user):
    db = FakeDb()

    async def get_current_user():
        return dict(user)

    app = FastAPI()
    app.include_router(build_router(db=db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), db


def test_bn13e_artifacts_exist():
    files = [
        README,
        ROOT / "backend" / "routes" / "owner_intake.py",
        FRONTEND / "pages" / "RoleHome.jsx",
    ]
    for path in files:
        assert path.exists(), str(path)
        assert path.stat().st_size > 500, str(path)


def test_owner_get_returns_current_user_default_profile_for_unattached_owner():
    client, db = _client({
        "id": "owner_1",
        "email": "owner@example.com",
        "full_name": "Owner One",
        "role": "horse_owner",
    })
    db.owner_intake_profiles.docs["other_owner"] = {
        "id": "owner_intake_other",
        "user_id": "other_owner",
        "preferred_name": "Other",
        "_id": "mongo",
    }

    r = client.get("/api/owner-intake/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "owner_1"
    assert body["email"] == "owner@example.com"
    assert body["preferred_name"] is None
    assert body["owner_type"] is None
    assert body["completion"]["percent"] == 0
    assert "_id" not in body
    assert "password_hash" not in body


def test_owner_get_scrubs_same_user_internal_profile_fields():
    client, db = _client({
        "id": "owner_internal",
        "email": "owner-internal@example.com",
        "full_name": "Internal Owner",
        "role": "horse_owner",
    })
    db.owner_intake_profiles.docs["owner_internal"] = {
        "id": "owner_intake_internal",
        "user_id": "owner_internal",
        "preferred_name": "IO",
        "owner_type": "facility_linked",
        "admin_note": "staff-only context",
        "review_status": "internal_review",
        "source_id": "src_secret",
        "stripe_customer_id": "cus_secret",
        "subscription_status": "active",
        "password_hash": "never",
        "_id": "mongo",
    }

    r = client.get("/api/owner-intake/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["preferred_name"] == "IO"
    for forbidden in [
        "admin_note",
        "review_status",
        "source_id",
        "stripe_customer_id",
        "subscription_status",
        "password_hash",
        "_id",
    ]:
        assert forbidden not in body


def test_owner_patch_persists_whitelisted_fields_and_ignores_identity_billing_fields():
    client, db = _client({
        "id": "owner_2",
        "email": "owner2@example.com",
        "full_name": "Owner Two",
        "role": "horse_owner",
    })

    r = client.patch("/api/owner-intake/profile", json={
        "preferred_name": "  Alex  ",
        "preferred_contact": "SMS",
        "owner_type": "INDIVIDUAL_OWNER",
        "primary_horse_name": "Maple",
        "horse_count_intent": "ONE",
        "riding_or_care_goals": "Simple care visibility",
        "facility_search_name": "North Star Farm",
        "facility_city_state": "Lexington, KY",
        "notes": "Interested in one-horse setup",
        "user_id": "attacker",
        "barn_id": "barn_attacker",
        "platform_role": "super_admin",
        "stripe_customer_id": "cus_attacker",
        "subscription_status": "active",
    })

    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user_id"] == "owner_2"
    assert body["preferred_name"] == "Alex"
    assert body["preferred_contact"] == "sms"
    assert body["owner_type"] == "individual_owner"
    assert body["primary_horse_name"] == "Maple"
    assert body["horse_count_intent"] == "one"
    assert body["completion"]["percent"] == 100
    for forbidden in ["barn_id", "platform_role", "stripe_customer_id", "subscription_status"]:
        assert forbidden not in body
    assert db.owner_intake_profiles.update_calls[-1]["query"] == {"user_id": "owner_2"}
    saved = db.owner_intake_profiles.docs["owner_2"]
    assert saved["user_id"] == "owner_2"
    assert "barn_id" not in saved
    assert "stripe_customer_id" not in saved


def test_owner_patch_rejects_invalid_enums_and_non_string_values():
    client, _db = _client({"id": "owner_3", "role": "horse_owner"})

    assert client.patch("/api/owner-intake/profile", json={"owner_type": "barn_admin"}).status_code == 422
    assert client.patch("/api/owner-intake/profile", json={"preferred_contact": "fax"}).status_code == 422
    assert client.patch("/api/owner-intake/profile", json={"horse_count_intent": "100"}).status_code == 422
    assert client.patch("/api/owner-intake/profile", json={"preferred_name": 123}).status_code == 422


def test_non_owner_cannot_read_or_patch_owner_intake():
    for role in ["rider", "parent", "admin", "barn_manager"]:
        client, _db = _client({"id": f"user_{role}", "role": role})
        assert client.get("/api/owner-intake/profile").status_code == 403
        assert client.patch(
            "/api/owner-intake/profile",
            json={"preferred_name": "Nope"},
        ).status_code == 403


def test_server_registers_owner_router_without_product_facility_gate():
    server = _read(ROOT / "backend" / "server.py")

    assert "build_owner_intake_router" in server
    assert "Build-Next-13E" in server
    section = server.split("# Build-Next-13E", 1)[1].split("# Notifications", 1)[0]
    assert "PRODUCT_FACILITY_DEPS" not in section
    assert "PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH" not in section


def test_role_home_owner_shell_uses_api_and_does_not_link_to_private_workflows():
    src = _read(FRONTEND / "pages" / "RoleHome.jsx")

    assert "function OwnerHome" in src
    assert '"/owner-intake/profile"' in src
    assert ".get(" in src
    assert ".patch(" in src
    assert 'data-testid="owner-intake-shell"' in src
    assert 'data-testid="owner-intake-save"' in src
    owner_section = src.split("function OwnerHome", 1)[1].split("function RiderHome", 1)[0]
    assert 'to="/owner-portal"' in owner_section
    for forbidden in ['to="/billing"', '"/admin', '"/staff"', '"/onboarding"', '"/horse-ledger"']:
        assert forbidden not in owner_section


def test_owner_navigation_keeps_unfinished_tools_on_owner_placeholders():
    src = _read(FRONTEND / "lib" / "roleNavigation.js")
    individual = src.split("export const INDIVIDUAL_OWNER_NAVIGATION", 1)[1].split(
        "export const GUARDIAN_NAVIGATION", 1
    )[0]

    assert 'roleHome("owner")' in individual
    for forbidden in ['"/billing"', '"/admin', '"/staff"', '"/onboarding"', '"/arena-schedule"']:
        assert forbidden not in individual
