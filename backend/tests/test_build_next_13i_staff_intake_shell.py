"""Build-Next-13I staff intake shell contract checks."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.staff_intake import build_router


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13I_STAFF_INTAKE_README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FakeStaffProfiles:
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
        self.staff_intake_profiles = FakeStaffProfiles()

    def __getitem__(self, name):
        if name != "staff_intake_profiles":
            raise KeyError(name)
        return self.staff_intake_profiles


def _client(user):
    db = FakeDb()

    async def get_current_user():
        return dict(user)

    app = FastAPI()
    app.include_router(build_router(db=db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), db


def test_bn13i_artifacts_exist():
    files = [
        README,
        ROOT / "backend" / "routes" / "staff_intake.py",
        FRONTEND / "pages" / "RoleHome.jsx",
        FRONTEND / "lib" / "roleLanding.js",
    ]
    for path in files:
        assert path.exists(), str(path)
        assert path.stat().st_size > 500, str(path)


def test_groom_get_returns_current_user_default_profile_only():
    client, db = _client({
        "id": "groom_1",
        "email": "groom@example.com",
        "full_name": "Groom One",
        "role": "groom",
    })
    db.staff_intake_profiles.docs["other_staff"] = {
        "id": "staff_intake_other",
        "user_id": "other_staff",
        "preferred_name": "Other",
        "_id": "mongo",
    }

    r = client.get("/api/staff-intake/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "groom_1"
    assert body["email"] == "groom@example.com"
    assert body["preferred_name"] is None
    assert body["care_area_comfort"] == []
    assert body["completion"]["percent"] == 0
    assert "_id" not in body
    assert "password_hash" not in body


def test_working_student_can_patch_own_staff_intake():
    client, db = _client({
        "id": "student_1",
        "email": "student@example.com",
        "full_name": "Student One",
        "role": "working_student",
    })

    r = client.patch("/api/staff-intake/profile", json={
        "preferred_name": "  Riley  ",
        "preferred_contact": "SMS",
        "availability_notes": "Afternoons after school",
        "experience_level": "INTERMEDIATE",
        "care_area_comfort": ["FEEDING", "water", "feeding", ""],
        "training_support_needs": "Needs hay-net walkthrough",
        "emergency_contact_preference": "Call parent first",
        "notes": "No workflow changes yet",
        "user_id": "attacker",
        "barn_id": "barn_attacker",
        "facility_id": "facility_attacker",
        "platform_role": "super_admin",
        "task_ids": ["task_attacker"],
        "task_completion_ids": ["done_attacker"],
        "horseops_write_grants": {"feed": True},
        "staff_permissions": {"admin": True},
        "schedule_ids": ["schedule_attacker"],
        "payroll_profile_id": "payroll_attacker",
        "stripe_customer_id": "cus_attacker",
        "subscription_status": "active",
    })

    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user_id"] == "student_1"
    assert body["preferred_name"] == "Riley"
    assert body["preferred_contact"] == "sms"
    assert body["experience_level"] == "intermediate"
    assert body["care_area_comfort"] == ["feeding", "water"]
    assert body["completion"]["percent"] == 100
    for forbidden in [
        "barn_id",
        "facility_id",
        "platform_role",
        "task_ids",
        "task_completion_ids",
        "horseops_write_grants",
        "staff_permissions",
        "schedule_ids",
        "payroll_profile_id",
        "stripe_customer_id",
        "subscription_status",
    ]:
        assert forbidden not in body
    assert db.staff_intake_profiles.update_calls[-1]["query"] == {"user_id": "student_1"}
    saved = db.staff_intake_profiles.docs["student_1"]
    assert saved["user_id"] == "student_1"
    assert "task_ids" not in saved
    assert "horseops_write_grants" not in saved


def test_staff_get_scrubs_same_user_internal_profile_fields():
    client, db = _client({
        "id": "staff_internal",
        "email": "staff-internal@example.com",
        "full_name": "Internal Staff",
        "role": "groom",
    })
    db.staff_intake_profiles.docs["staff_internal"] = {
        "id": "staff_intake_internal",
        "user_id": "staff_internal",
        "preferred_name": "Care Lead",
        "admin_note": "staff-only context",
        "review_status": "internal_review",
        "source_id": "src_secret",
        "barn_id": "barn_secret",
        "facility_id": "facility_secret",
        "task_ids": ["task_secret"],
        "task_completion_ids": ["done_secret"],
        "horseops_write_grants": {"feed": True},
        "staff_permissions": {"admin": True},
        "schedule_ids": ["schedule_secret"],
        "payroll_profile_id": "payroll_secret",
        "stripe_customer_id": "cus_secret",
        "subscription_status": "active",
        "password_hash": "never",
        "_id": "mongo",
    }

    r = client.get("/api/staff-intake/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["preferred_name"] == "Care Lead"
    for forbidden in [
        "admin_note",
        "review_status",
        "source_id",
        "barn_id",
        "facility_id",
        "task_ids",
        "task_completion_ids",
        "horseops_write_grants",
        "staff_permissions",
        "schedule_ids",
        "payroll_profile_id",
        "stripe_customer_id",
        "subscription_status",
        "password_hash",
        "_id",
    ]:
        assert forbidden not in body


def test_staff_patch_rejects_invalid_enums_and_non_string_values():
    client, _db = _client({"id": "groom_2", "role": "groom"})

    assert client.patch("/api/staff-intake/profile", json={"preferred_contact": "fax"}).status_code == 422
    assert client.patch("/api/staff-intake/profile", json={"experience_level": "wizard"}).status_code == 422
    assert client.patch("/api/staff-intake/profile", json={"care_area_comfort": ["payroll"]}).status_code == 422
    assert client.patch("/api/staff-intake/profile", json={"preferred_name": 123}).status_code == 422


def test_non_staff_roles_cannot_read_or_patch_staff_intake():
    for role in ["admin", "horse_owner", "parent", "trainer", "rider", "barn_owner", "barn_manager"]:
        client, _db = _client({"id": f"user_{role}", "role": role})
        assert client.get("/api/staff-intake/profile").status_code == 403
        assert client.patch(
            "/api/staff-intake/profile",
            json={"preferred_name": "Nope"},
        ).status_code == 403


def test_server_registers_staff_router_without_product_facility_gate():
    server = _read(ROOT / "backend" / "server.py")

    assert "build_staff_intake_router" in server
    assert "Build-Next-13I" in server
    section = server.split("# Build-Next-13I", 1)[1].split("# Notifications", 1)[0]
    assert "PRODUCT_FACILITY_DEPS" not in section
    assert "PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH" not in section


def test_role_landing_routes_staff_to_intake_home_without_breaking_manager():
    src = _read(FRONTEND / "lib" / "roleLanding.js")

    assert 'staff: "/role-home/staff"' in src
    assert 'manager: "/role-home/manager"' in src
    assert 'if (role === "barn_manager") return ROLE_HOME_PATHS.manager;' in src
    assert 'if (role === "groom" || role === "working_student") return ROLE_HOME_PATHS.staff;' in src


def test_role_home_staff_shell_uses_api_and_does_not_link_to_private_workflows():
    src = _read(FRONTEND / "pages" / "RoleHome.jsx")

    assert "function StaffHome" in src
    assert '"/staff-intake/profile"' in src
    assert ".get(" in src
    assert ".patch(" in src
    assert 'data-testid="staff-intake-shell"' in src
    assert 'data-testid="staff-intake-save"' in src
    staff_section = src.split("function StaffHome", 1)[1].split("function ManagerHome", 1)[0]
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
        '"/tasks"',
        '"/schedule"',
        '"/payroll"',
    ]:
        assert forbidden not in staff_section
    for copy in [
        "This does not create tasks",
        "task completions",
        "schedules",
        "staff permissions",
        "HorseOps records",
    ]:
        assert copy in staff_section
