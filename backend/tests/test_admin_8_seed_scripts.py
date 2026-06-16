"""tests/test_admin_8_seed_scripts.py — Phase Admin-8 verification.

Covers founder-locked Part D test requirements:
  1. Admin seed script is idempotent.
  2. Existing user promotion does not duplicate users.
  3. Admin seed writes audit entries.
  4. No password/token values appear in logs, audit metadata, or
     committed docs.
  5. Demo seed creates expected client-visible data.
  6. Demo account cannot access admin portal unless separately
     granted platform_role.
  7. Demo teardown removes only demo-tagged records.
  8. No landing page file changed.
  9. Old removed demo seed method is not restored.
"""
from __future__ import annotations

import io
import os
import pathlib
import re
import subprocess
import sys
import uuid

import pytest
from dotenv import load_dotenv
from pymongo import MongoClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")


def _run_admin_seed(*flags):
    return subprocess.run(
        [sys.executable, "-m", "scripts.seed_initial_admins", *flags],
        cwd=str(ROOT), capture_output=True, text=True, timeout=30,
        env={**os.environ},
    )


def _run_demo_seed(*flags, extra_env=None):
    env = {**os.environ}
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, "-m", "scripts.seed_demo_account", *flags],
        cwd=str(ROOT), capture_output=True, text=True, timeout=30,
        env=env,
    )


@pytest.fixture
def db():
    c = MongoClient(os.environ["MONGO_URL"])
    yield c[os.environ.get("DB_NAME") or "equinesync"]
    c.close()


# ----------------------------------------------------------------------
# 1 + 2 + 3 — admin seed idempotency + audit emission.
# ----------------------------------------------------------------------
def test_admin_seed_creates_4_admins_and_is_idempotent(db):
    """Two runs must yield exactly the same 4 admin user rows."""
    # First run.
    r1 = _run_admin_seed()
    assert r1.returncode == 0, r1.stderr
    emails = [
        "info@equine-sync.com",
        "prsindustries23@gmail.com",
        "rian.ray2012@gmail.com",
        "prspoon23@gmail.com",
    ]
    try:
        for e in emails:
            n = db.users.count_documents({"email": e})
            assert n == 1, f"first run: {e} count={n}"

        # Second run — must not duplicate or error.
        r2 = _run_admin_seed()
        assert r2.returncode == 0, r2.stderr
        for e in emails:
            n = db.users.count_documents({"email": e})
            assert n == 1, f"idempotent: {e} count={n}"

        # Audit entries — at least one row per admin tagged
        # admin.seed.* and never carrying a password.
        for e in emails:
            rows = list(db.audit_log.find({"metadata.target_email": e}))
            assert any(r["action"].startswith("admin.seed.") for r in rows), (
                f"no admin.seed.* audit row for {e}"
            )
            for r in rows:
                meta = r.get("metadata", {})
                # The metadata MUST NOT contain the literal password.
                # We don't know it, but we can assert no field looks
                # like a password by key name.
                for k in meta:
                    assert "password" not in k.lower() or k == "password_source", (
                        f"audit metadata key looks like a secret: {k!r}"
                    )
    finally:
        # Cleanup.
        db.users.delete_many({"email": {"$in": emails}})
        db.audit_log.delete_many({"metadata.target_email": {"$in": emails}})


def test_admin_seed_promotes_existing_user_without_duplicating(db):
    """If a user already exists with the target email, the script
    must PROMOTE (update platform_role) and never create a 2nd row."""
    email = "rian.ray2012@gmail.com"
    pre_id = str(uuid.uuid4())
    db.users.insert_one({
        "id": pre_id,
        "email": email,
        "full_name": "Rian (pre-existing)",
        "role": "horse_owner",
        "role_status": "active",
        "platform_role": None,
        "password_hash": "$2b$12$placeholder_only_for_test",
        "created_at": "2024-01-01T00:00:00+00:00",
        "_admin8_test": True,
    })
    try:
        r = _run_admin_seed()
        assert r.returncode == 0, r.stderr
        assert db.users.count_documents({"email": email}) == 1
        promoted = db.users.find_one({"email": email})
        assert promoted["id"] == pre_id, "must update in place"
        assert promoted["platform_role"] == "super_admin"
        # Promotion must NOT overwrite an existing password_hash.
        assert promoted["password_hash"] == "$2b$12$placeholder_only_for_test"
        # Audit row says "promoted" not "created".
        audits = list(db.audit_log.find({"metadata.target_email": email}))
        assert any(a["action"] == "admin.seed.promoted" for a in audits)
    finally:
        db.users.delete_one({"id": pre_id})
        db.audit_log.delete_many({"metadata.target_email": email})


# ----------------------------------------------------------------------
# 4 — no password in logs / audit / committed docs.
# ----------------------------------------------------------------------
def test_no_password_value_in_audit_log(db):
    """Run admin seed and demo seed; scan every audit row written for
    anything that looks like the minted bytes."""
    pwd_emails = [
        "info@equine-sync.com",
        "prsindustries23@gmail.com",
        "rian.ray2012@gmail.com",
        "prspoon23@gmail.com",
        "demo.client@equine-sync.com",
    ]
    try:
        r1 = _run_admin_seed()
        assert r1.returncode == 0
        r2 = _run_demo_seed()
        assert r2.returncode == 0

        # Extract minted passwords from stdout.
        passwords = []
        for line in (r1.stdout + r2.stdout).splitlines():
            m = re.match(r"\s+\S+@\S+\s+(\S{20,})\s*$", line)
            if m:
                passwords.append(m.group(1))
        assert passwords, "expected minted passwords to be printed"

        # Confirm none of those passwords appear in audit_log.
        all_audit = list(db.audit_log.find({
            "metadata.target_email": {"$in": pwd_emails},
        }))
        all_audit += list(db.audit_log.find({"actor_email": "(cli)"}))
        as_text = str(all_audit)
        for pw in passwords:
            assert pw not in as_text, (
                "password value leaked into audit_log"
            )
    finally:
        db.users.delete_many({"email": {"$in": pwd_emails}})
        db.audit_log.delete_many({
            "$or": [
                {"metadata.target_email": {"$in": pwd_emails}},
                {"metadata.demo_seed_key": "admin8_client_demo"},
            ]
        })
        db.barns.delete_many({"demo_seed_key": "admin8_client_demo"})
        db.horses.delete_many({"demo_seed_key": "admin8_client_demo"})
        if "tasks" in db.list_collection_names():
            db.tasks.delete_many({"demo_seed_key": "admin8_client_demo"})
        db.subscriptions.delete_many({"demo_seed_key": "admin8_client_demo"})


def test_no_password_in_committed_files():
    """Committed files (scripts + docs + tests) must not embed any
    obvious password literal."""
    files = [
        ROOT / "scripts" / "seed_initial_admins.py",
        ROOT / "scripts" / "seed_demo_account.py",
        ROOT / "tests" / "test_admin_8_seed_scripts.py",
        ROOT.parent / "docs" / "INITIAL_ADMIN_AND_DEMO_SETUP.md",
    ]
    # Lines that LITERALLY define a password constant assigned to a
    # plausible-looking string LITERAL (not a runtime concatenation).
    # `password = "..." + something` is allowed because the value is
    # constructed at runtime; `password = "abc12345"` is not.
    bad_re = re.compile(
        r'(?i)(password|secret|pwd)\s*=\s*'
        r'["\'][A-Za-z0-9!@#$%^&*_\-+=]{8,}["\']'
        r'\s*$'      # nothing else on the line — pure literal assignment
    )
    for f in files:
        if not f.exists():
            continue
        for i, line in enumerate(f.read_text().splitlines(), start=1):
            if "$2b$" in line or "placeholder" in line.lower():
                continue
            assert not bad_re.search(line), (
                f"hardcoded password literal in {f}:{i}  →  {line!r}"
            )


# ----------------------------------------------------------------------
# 5 + 6 — demo seed creates expected data + no platform_role.
# ----------------------------------------------------------------------
def test_demo_seed_creates_expected_records(db):
    try:
        r = _run_demo_seed()
        assert r.returncode == 0, r.stderr

        # Barn
        barn = db.barns.find_one({"demo_seed_key": "admin8_client_demo"})
        assert barn, "demo barn missing"
        assert barn["name"] == "Equine Sync Demo Barn"
        assert barn.get("subscription_id") is None, "demo barn must NOT carry subscription_id"

        # User
        user = db.users.find_one({"email": "demo.client@equine-sync.com"})
        assert user, "demo user missing"
        assert user["role"] == "horse_owner"
        # *** CRITICAL: no platform_role on the demo user.
        assert not user.get("platform_role"), (
            f"demo user must NOT have a platform_role; got {user.get('platform_role')!r}"
        )
        assert user["demo_seed_key"] == "admin8_client_demo"
        assert user["created_by_seed"] == "phase_admin_8"

        # Horses (3)
        horses = list(db.horses.find({"demo_seed_key": "admin8_client_demo"}))
        assert len(horses) == 3
        assert {h["name"] for h in horses} == {"Aurelia", "Beacon", "Cinder"}

        # Subscription — NO Stripe-shaped id
        sub = db.subscriptions.find_one({"demo_seed_key": "admin8_client_demo"})
        assert sub
        assert sub["status"] == "active"
        assert sub["tier"] == "demo"
        assert not re.match(r"^sub_[A-Za-z0-9]{14,}$", sub["id"]), (
            f"demo subscription must NOT use a Stripe-shaped id; got {sub['id']}"
        )
    finally:
        _run_demo_seed("--teardown")


def test_demo_user_cannot_reach_admin_portal_me(db):
    """Demo user has no platform_role → /api/admin/portal/me must 403."""
    import requests
    api_base = os.environ.get("REACT_APP_BACKEND_URL") or ""
    if not api_base:
        env = (pathlib.Path("/app/frontend/.env")).read_text()
        for line in env.splitlines():
            if line.startswith("REACT_APP_BACKEND_URL="):
                api_base = line.split("=", 1)[1].strip()
                break
    api = api_base.rstrip("/") + "/api"

    # Seed with a known password via env var so we can log in.
    password = "DemoOnly-" + uuid.uuid4().hex[:12] + "Aa1!"
    try:
        r = _run_demo_seed(extra_env={"SEED_DEMO_CLIENT_PASSWORD": password})
        assert r.returncode == 0, r.stderr

        login = requests.post(
            f"{api}/auth/login",
            json={"email": "demo.client@equine-sync.com", "password": password},
            timeout=10,
        )
        assert login.status_code == 200, login.text
        token = login.json()["token"]

        me = requests.get(f"{api}/admin/portal/me",
                          headers={"Authorization": f"Bearer {token}"},
                          timeout=10)
        assert me.status_code == 403, (
            f"demo user must be 403 on /admin/portal/me; got {me.status_code}"
        )
    finally:
        _run_demo_seed("--teardown")


# ----------------------------------------------------------------------
# 7 — teardown removes only demo-tagged records.
# ----------------------------------------------------------------------
def test_teardown_removes_only_demo_tagged_records(db):
    # Plant a non-demo barn with similar name → must SURVIVE teardown.
    survivor_id = f"barn_survivor_{uuid.uuid4().hex[:8]}"
    db.barns.insert_one({
        "id": survivor_id,
        "name": "Equine Sync Demo Barn (look-alike, NOT tagged)",
        "status": "active",
        "_admin8_test": True,
    })
    try:
        _run_demo_seed()
        # Confirm demo barn present.
        assert db.barns.count_documents({"demo_seed_key": "admin8_client_demo"}) == 1
        # Teardown.
        td = _run_demo_seed("--teardown")
        assert td.returncode == 0, td.stderr
        # Demo gone…
        assert db.barns.count_documents({"demo_seed_key": "admin8_client_demo"}) == 0
        assert db.users.count_documents({"email": "demo.client@equine-sync.com"}) == 0
        # …survivor still present.
        assert db.barns.count_documents({"id": survivor_id}) == 1
    finally:
        db.barns.delete_one({"id": survivor_id})


# ----------------------------------------------------------------------
# 8 — no landing page file changed.
# ----------------------------------------------------------------------
def test_no_landing_page_modified():
    """Admin-8 spec: 'No landing page changes.' Confirm no recent
    edits to known landing-page files."""
    candidates = [
        "/app/frontend/src/pages/Landing.jsx",
        "/app/frontend/src/pages/Home.jsx",
        "/app/frontend/src/pages/Index.jsx",
        "/app/frontend/src/App.js",
    ]
    out = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd="/app", capture_output=True, text=True, timeout=10,
    )
    changed = set(out.stdout.splitlines())
    for c in candidates:
        rel = c.replace("/app/", "")
        assert rel not in changed, (
            f"Admin-8 must not modify {rel}, but it appears in git diff."
        )


# ----------------------------------------------------------------------
# 9 — old removed demo seed method is not restored.
# ----------------------------------------------------------------------
def test_old_demo_seed_method_not_restored():
    """Anchor: scan backend for any restored landing-page demo-login
    shortcut. We look for symptomatic patterns rather than a specific
    function name."""
    bad_patterns = [
        r"/api/auth/demo[_\-]login",
        r"def\s+demo_login\b",
        r"def\s+seed_demo_user\b",     # old name candidate
        r"def\s+create_seeded_demo\b", # old name candidate
        r"DEMO_SHORTCUT",
    ]
    for py in pathlib.Path("/app/backend").rglob("*.py"):
        if py.name in (
            "seed_demo_account.py",
            "test_admin_8_seed_scripts.py",
        ):
            continue
        text = py.read_text()
        for pat in bad_patterns:
            assert not re.search(pat, text), (
                f"old demo-seed shortcut may be re-introduced: "
                f"pattern={pat} file={py}"
            )
