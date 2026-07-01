"""Build-Next-13H barn manager intake shell contract checks."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.manager_intake import build_router


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13H_MANAGER_INTAKE_README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FakeManagerProfiles:
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
        self.manager_intake_profiles = FakeManagerProfiles()

    def __getitem__(self, name):
        if name != "manager_intake_profiles":
            raise KeyError(name)
        return self.manager_intake_profiles


def _client(user):
    db = FakeDb()

    async def get_current_user():
        return dict(user)

    app = FastAPI()
    app.include_router(build_router(db=db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), db


def test_bn13h_artifacts_exist():
    files = [
        README,
        ROOT / "backend" / "routes" / "manager_intake.py",
        FRONTEND / "pages" / "RoleHome.jsx",
        FRONTEND / "lib" / "roleLanding.js",
    ]
    for path in files:
        assert path.exists(), str(path)
        assert path.stat().st_size > 500, str(path)


def test_manager_get_returns_current_user_default_profile_only():
    client, db = _client({
        "id": "manager_1",
        "email": "manager@example.com",
        "full_name": "Manager One",
        "role": "barn_manager",
    })
    db.manager_intake_profiles.docs["other_manager"] = {
        "id": "manager_intake_other",
        "user_id": "other_manager",
        "preferred_name": "Other",
        "_id": "mongo",
    }

    r = client.get("/api/manager-intake/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "manager_1"
    assert body["email"] == "manager@example.com"
    assert body["preferred_name"] is None
    assert body["operations_focus"] == []
    assert body["completion"]["percent"] == 0
    assert "_id" not in body
    assert "password_hash" not in body


def test_manager_get_scrubs_same_user_internal_profile_fields():
    client, db = _client({
        "id": "manager_internal",
        "email": "manager-internal@example.com",
        "full_name": "Internal Manager",
        "role": "barn_manager",
    })
    db.manager_intake_profiles.docs["manager_internal"] = {
        "id": "manager_intake_internal",
        "user_id": "manager_internal",
        "preferred_name": "Ops Lead",
        "admin_note": "staff-only context",
        "review_status": "internal_review",
        "source_id": "src_secret",
        "barn_id": "barn_secret",
        "facility_id": "facility_secret",
        "task_ids": ["task_secret"],
        "staff_invites": [{"email": "staff@example.com"}],
        "staff_permissions": {"admin": True},
        "horseops_write_grants": {"feed": True},
        "stripe_customer_id": "cus_secret",
        "subscription_status": "active",
        "password_hash": "never",
        "_id": "mongo",
    }

    r = client.get("/api/manager-intake/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["preferred_name"] == "Ops Lead"
    for forbidden in [
        "admin_note",
        "review_status",
        "source_id",
        "barn_id",
        "facility_id",
        "task_ids",
        "staff_invites",
        "staff_permissions",
        "horseops_write_grants",
        "stripe_customer_id",
        "subscription_status",
        "password_hash",
        "_id",
    ]:
        assert forbidden not in body


def test_manager_patch_persists_whitelisted_fields_and_ignores_product_fields():
    client, db = _client({
        "id": "manager_2",
        "email": "manager2@example.com",
        "full_name": "Manager Two",
        "role": "barn_manager",
    })

    r = client.patch("/api/manager-intake/profile", json={
        "preferred_name": "  Morgan  ",
        "preferred_contact": "SMS",
        "operations_focus": ["DAILY_TASKS", "horse_care", "daily_tasks", ""],
        "shift_availability_notes": "Weekday mornings",
        "team_coordination_notes": "Needs handoff clarity",
        "horse_care_oversight_notes": "Watch feed and turnout logs",
        "task_board_goals": "Organize daily work without duplicate texts",
        "facility_connection_notes": "May cover North Star",
        "emergency_operations_notes": "Needs phone tree later",
        "notes": "No workflow changes yet",
        "user_id": "attacker",
        "barn_id": "barn_attacker",
        "facility_id": "facility_attacker",
        "platform_role": "super_admin",
        "task_ids": ["task_attacker"],
        "staff_invites": [{"email": "x@example.com"}],
        "staff_permissions": {"admin": True},
        "horseops_write_grants": {"feed": True},
        "stripe_customer_id": "cus_attacker",
        "subscription_status": "active",
    })

    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user_id"] == "manager_2"
    assert body["preferred_name"] == "Morgan"
    assert body["preferred_contact"] == "sms"
    assert body["operations_focus"] == ["daily_tasks", "horse_care"]
    assert body["completion"]["percent"] == 100
    for forbidden in [
        "barn_id",
        "facility_id",
        "platform_role",
        "task_ids",
        "staff_invites",
        "staff_permissions",
        "horseops_write_grants",
        "stripe_customer_id",
        "subscription_status",
    ]:
        assert forbidden not in body
    assert db.manager_intake_profiles.update_calls[-1]["query"] == {"user_id": "manager_2"}
    saved = db.manager_intake_profiles.docs["manager_2"]
    assert saved["user_id"] == "manager_2"
    assert "task_ids" not in saved
    assert "staff_invites" not in saved


def test_manager_patch_rejects_invalid_enums_and_non_string_values():
    client, _db = _client({"id": "manager_3", "role": "barn_manager"})

    assert client.patch("/api/manager-intake/profile", json={"preferred_contact": "fax"}).status_code == 422
    assert client.patch("/api/manager-intake/profile", json={"operations_focus": ["payroll"]}).status_code == 422
    assert client.patch("/api/manager-intake/profile", json={"preferred_name": 123}).status_code == 422


def test_non_manager_cannot_read_or_patch_manager_intake():
    for role in ["admin", "horse_owner", "parent", "trainer", "rider", "barn_owner", "groom"]:
        client, _db = _client({"id": f"user_{role}", "role": role})
        assert client.get("/api/manager-intake/profile").status_code == 403
        assert client.patch(
            "/api/manager-intake/profile",
            json={"preferred_name": "Nope"},
        ).status_code == 403


def test_server_registers_manager_router_without_product_facility_gate():
    server = _read(ROOT / "backend" / "server.py")

    assert "build_manager_intake_router" in server
    assert "Build-Next-13H" in server
    section = server.split("# Build-Next-13H", 1)[1].split("# Notifications", 1)[0]
    assert "PRODUCT_FACILITY_DEPS" not in section
    assert "PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH" not in section


def test_role_landing_routes_manager_to_intake_home_without_breaking_trainer():
    src = _read(FRONTEND / "lib" / "roleLanding.js")

    assert 'manager: "/role-home/manager"' in src
    assert 'trainer: "/role-home/trainer"' in src
    assert 'if (role === "trainer") return ROLE_HOME_PATHS.trainer;' in src
    assert 'if (role === "barn_manager") return ROLE_HOME_PATHS.manager;' in src


def test_role_home_manager_shell_uses_api_and_does_not_link_to_private_workflows():
    src = _read(FRONTEND / "pages" / "RoleHome.jsx")

    assert "function ManagerHome" in src
    assert '"/manager-intake/profile"' in src
    assert ".get(" in src
    assert ".patch(" in src
    assert 'data-testid="manager-intake-shell"' in src
    assert 'data-testid="manager-intake-save"' in src
    manager_section = src.split("function ManagerHome", 1)[1].split("function TrainerHome", 1)[0]
    for forbidden in [
        'to="/today"',
        'to="/staff"',
        'to="/horses"',
        '"/billing"',
        '"/admin',
        '"/invites"',
        '"/checkout"',
        '"/subscriptions"',
        '"/forms-signatures"',
        '"/horse-ledger"',
        '"/owner-updates"',
        '"/arena-schedule"',
    ]:
        assert forbidden not in manager_section
    for copy in [
        "This does not create tasks",
        "staff invites",
        "permissions",
        "HorseOps records",
        "facility setup",
    ]:
        assert copy in manager_section
