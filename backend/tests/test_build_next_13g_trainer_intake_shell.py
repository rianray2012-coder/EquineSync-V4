"""Build-Next-13G trainer intake shell contract checks."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from routes.trainer_intake import build_router


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
README = ROOT / "BUILD_NEXT_13G_TRAINER_INTAKE_README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FakeTrainerProfiles:
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
        self.trainer_intake_profiles = FakeTrainerProfiles()

    def __getitem__(self, name):
        if name != "trainer_intake_profiles":
            raise KeyError(name)
        return self.trainer_intake_profiles


def _client(user):
    db = FakeDb()

    async def get_current_user():
        return dict(user)

    app = FastAPI()
    app.include_router(build_router(db=db, get_current_user=get_current_user), prefix="/api")
    return TestClient(app), db


def test_bn13g_artifacts_exist():
    files = [
        README,
        ROOT / "backend" / "routes" / "trainer_intake.py",
        FRONTEND / "pages" / "RoleHome.jsx",
        FRONTEND / "pages" / "RoleIntake.jsx",
        FRONTEND / "lib" / "roleLanding.js",
    ]
    for path in files:
        assert path.exists(), str(path)
        if path.name == "RoleHome.jsx":
            assert path.stat().st_size > 50, str(path)
        else:
            assert path.stat().st_size > 500, str(path)


def test_trainer_get_returns_current_user_default_profile_only():
    client, db = _client({
        "id": "trainer_1",
        "email": "trainer@example.com",
        "full_name": "Trainer One",
        "role": "trainer",
    })
    db.trainer_intake_profiles.docs["other_trainer"] = {
        "id": "trainer_intake_other",
        "user_id": "other_trainer",
        "preferred_name": "Other",
        "_id": "mongo",
    }

    r = client.get("/api/trainer-intake/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["user_id"] == "trainer_1"
    assert body["email"] == "trainer@example.com"
    assert body["preferred_name"] is None
    assert body["disciplines"] == []
    assert body["rider_levels_supported"] == []
    assert body["completion"]["percent"] == 0
    assert "_id" not in body
    assert "password_hash" not in body


def test_trainer_get_scrubs_same_user_internal_profile_fields():
    client, db = _client({
        "id": "trainer_internal",
        "email": "trainer-internal@example.com",
        "full_name": "Internal Trainer",
        "role": "trainer",
    })
    db.trainer_intake_profiles.docs["trainer_internal"] = {
        "id": "trainer_intake_internal",
        "user_id": "trainer_internal",
        "preferred_name": "Coach",
        "admin_note": "staff-only context",
        "review_status": "internal_review",
        "source_id": "src_secret",
        "barn_id": "barn_secret",
        "facility_id": "facility_secret",
        "assigned_horse_ids": ["horse_secret"],
        "student_ids": ["student_secret"],
        "lesson_ids": ["lesson_secret"],
        "staff_permissions": {"admin": True},
        "stripe_customer_id": "cus_secret",
        "subscription_status": "active",
        "password_hash": "never",
        "_id": "mongo",
    }

    r = client.get("/api/trainer-intake/profile")
    assert r.status_code == 200
    body = r.json()
    assert body["preferred_name"] == "Coach"
    for forbidden in [
        "admin_note",
        "review_status",
        "source_id",
        "barn_id",
        "facility_id",
        "assigned_horse_ids",
        "student_ids",
        "lesson_ids",
        "staff_permissions",
        "stripe_customer_id",
        "subscription_status",
        "password_hash",
        "_id",
    ]:
        assert forbidden not in body


def test_trainer_patch_persists_whitelisted_fields_and_ignores_assignment_fields():
    client, db = _client({
        "id": "trainer_2",
        "email": "trainer2@example.com",
        "full_name": "Trainer Two",
        "role": "trainer",
    })

    r = client.patch("/api/trainer-intake/profile", json={
        "preferred_name": "  Avery  ",
        "preferred_contact": "SMS",
        "disciplines": ["Dressage", "Dressage", "Eventing", ""],
        "program_focus": "LESSONS",
        "rider_levels_supported": ["BEGINNER", "intermediate", "beginner"],
        "availability_notes": "Weekday mornings",
        "certification_insurance_notes": "USDF member",
        "facility_connection_notes": "May teach at North Star",
        "goals": "Build lesson-program structure",
        "notes": "Needs student roster later",
        "user_id": "attacker",
        "barn_id": "barn_attacker",
        "facility_id": "facility_attacker",
        "platform_role": "super_admin",
        "assigned_horse_ids": ["horse_attacker"],
        "student_ids": ["student_attacker"],
        "lesson_ids": ["lesson_attacker"],
        "staff_permissions": {"admin": True},
        "stripe_customer_id": "cus_attacker",
        "subscription_status": "active",
    })

    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user_id"] == "trainer_2"
    assert body["preferred_name"] == "Avery"
    assert body["preferred_contact"] == "sms"
    assert body["disciplines"] == ["Dressage", "Eventing"]
    assert body["program_focus"] == "lessons"
    assert body["rider_levels_supported"] == ["beginner", "intermediate"]
    assert body["completion"]["percent"] == 100
    for forbidden in [
        "barn_id",
        "facility_id",
        "platform_role",
        "assigned_horse_ids",
        "student_ids",
        "lesson_ids",
        "staff_permissions",
        "stripe_customer_id",
        "subscription_status",
    ]:
        assert forbidden not in body
    assert db.trainer_intake_profiles.update_calls[-1]["query"] == {"user_id": "trainer_2"}
    saved = db.trainer_intake_profiles.docs["trainer_2"]
    assert saved["user_id"] == "trainer_2"
    assert "assigned_horse_ids" not in saved
    assert "student_ids" not in saved


def test_trainer_patch_rejects_invalid_enums_and_non_string_values():
    client, _db = _client({"id": "trainer_3", "role": "trainer"})

    assert client.patch("/api/trainer-intake/profile", json={"program_focus": "accounting"}).status_code == 422
    assert client.patch("/api/trainer-intake/profile", json={"preferred_contact": "fax"}).status_code == 422
    assert client.patch("/api/trainer-intake/profile", json={"rider_levels_supported": ["expert"]}).status_code == 422
    assert client.patch("/api/trainer-intake/profile", json={"preferred_name": 123}).status_code == 422


def test_non_trainer_cannot_read_or_patch_trainer_intake():
    for role in ["admin", "horse_owner", "parent", "barn_manager", "rider", "barn_owner"]:
        client, _db = _client({"id": f"user_{role}", "role": role})
        assert client.get("/api/trainer-intake/profile").status_code == 403
        assert client.patch(
            "/api/trainer-intake/profile",
            json={"preferred_name": "Nope"},
        ).status_code == 403


def test_server_registers_trainer_router_without_product_facility_gate():
    server = _read(ROOT / "backend" / "server.py")

    assert "build_trainer_intake_router" in server
    assert "build_trainer_operating_center_router" in server
    assert "Build-Next-13G" in server
    section = server.split("# Build-Next-13G", 1)[1].split("# RF9", 1)[0]
    assert "PRODUCT_FACILITY_DEPS" not in section
    assert "PRODUCT_FACILITY_DEPS_OPTIONAL_AUTH" not in section
    rf9_section = server.split("# RF9", 1)[1].split("# RF10", 1)[0]
    assert "PRODUCT_FACILITY_DEPS" in rf9_section


def test_role_landing_routes_trainer_to_intake_home_without_breaking_manager():
    src = _read(FRONTEND / "lib" / "roleLanding.js")

    assert 'trainer: "/role-home/trainer"' in src
    assert 'if (role === "trainer") return ROLE_INTAKE_PATHS.trainer;' in src
    assert 'if (role === "barn_manager") return ROLE_INTAKE_PATHS.manager;' in src


def test_role_home_trainer_shell_uses_api_and_does_not_link_to_private_workflows():
    src = _read(FRONTEND / "pages" / "RoleIntake.jsx")

    assert "function TrainerHome" in src
    assert '"/trainer-intake/profile"' in src
    assert ".get(" in src
    assert ".patch(" in src
    assert 'data-testid="trainer-intake-shell"' in src
    assert 'data-testid="trainer-intake-save"' in src
    trainer_section = src.split("function TrainerHome", 1)[1].split("function BarnOwnerHome", 1)[0]
    for forbidden in [
        'to="/lessons"',
        'to="/horses"',
        '"/billing"',
        '"/admin',
        '"/staff"',
        '"/invites"',
        '"/checkout"',
        '"/subscriptions"',
        '"/forms-signatures"',
        '"/students"',
        '"/arena-schedule"',
    ]:
        assert forbidden not in trainer_section


def test_tp1_tp2_trainer_review_posture_and_operating_summary_are_truthful():
    src = _read(FRONTEND / "pages" / "RoleIntake.jsx")
    signup = _read(FRONTEND / "pages" / "Signup.jsx")
    shell = _read(FRONTEND / "components" / "AppShell.jsx")
    plan = _read(ROOT / "docs" / "GATE_2_TRAINER_PROVIDER_PROMISE_PLAN.md")

    assert '"/trainer/operating-center"' in src
    assert 'data-testid="trainer-review-posture"' in src
    assert 'data-testid="trainer-operating-summary"' in src
    assert "Trainer Workspace" in src
    assert "approved assigned-work visibility" in signup
    assert "Complete your trainer intake while EquineSync reviews your profile" in shell
    assert "TP-1 and TP-2 Execution Notes" in plan
    assert "no production launch authority" in plan
    for forbidden in [
        "full directory experience",
        "client, horse, lesson, and program tools",
        "Verified equestrian network",
        "Equine Sync",
    ]:
        assert forbidden not in src
        assert forbidden not in signup
        assert forbidden not in shell


def test_trainer_navigation_keeps_admin_and_billing_out_of_trainer_menu():
    src = _read(FRONTEND / "lib" / "roleNavigation.js")
    trainer = src.split("export const TRAINER_NAVIGATION", 1)[1].split(
        "export const BARN_OWNER_NAVIGATION", 1
    )[0]

    for forbidden in ['"/admin', '"/billing"', '"/staff"']:
        assert forbidden not in trainer
