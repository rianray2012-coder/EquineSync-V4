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

CODEX ROUND-1 P0 NOTE
---------------------
This suite MUST NEVER create, promote, or delete the real founder
admin emails (the four locked roster addresses in
``backend/scripts/seed_initial_admins.py``). Every admin-seed
invocation passes ``--roster <tmp.json>`` so the script targets
throwaway ``*@admin8-test.local`` rows that we own end-to-end.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import uuid

import bcrypt
import pytest
from dotenv import load_dotenv
from pymongo import MongoClient

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")


# ----------------------------------------------------------------------
# Throwaway roster — NEVER overlaps with the real founder roster.
# Every email lives under @admin8-test.local so a bad cleanup can
# never touch a production-shaped address.
# ----------------------------------------------------------------------
TEST_ROSTER = [
    {
        "email":         "alpha@admin8-test.local",
        "full_name":     "Alpha Test Admin",
        "title":         "Test Initial Admin Operator",
        "platform_role": "platform_admin",
    },
    {
        "email":         "bravo@admin8-test.local",
        "full_name":     "Bravo Test Admin",
        "title":         "Test Billing Administrator",
        "platform_role": "billing_admin",
    },
    {
        "email":         "charlie@admin8-test.local",
        "full_name":     "Charlie Test Admin",
        "title":         "Test Super Admin 1",
        "platform_role": "super_admin",
    },
    {
        "email":         "delta@admin8-test.local",
        "full_name":     "Delta Test Admin",
        "title":         "Test Super Admin 2",
        "platform_role": "super_admin",
    },
]
TEST_EMAILS = [e["email"] for e in TEST_ROSTER]


@pytest.fixture
def roster_path(tmp_path):
    """Write the throwaway roster to a temp JSON file the script
    can load with `--roster`."""
    p = tmp_path / "admin8_test_roster.json"
    p.write_text(json.dumps(TEST_ROSTER))
    return str(p)


def _run_admin_seed(roster_path, *flags):
    """Always pass --roster <path> so we NEVER touch the real founders."""
    return subprocess.run(
        [
            sys.executable, "-m", "scripts.seed_initial_admins",
            "--roster", roster_path, *flags,
        ],
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


def _cleanup_admin_test_rows(db):
    """Hard-delete any rows that the test-only roster could have
    created. Restricted by the @admin8-test.local domain so we
    can never reach production-shaped emails."""
    db.users.delete_many({"email": {"$in": TEST_EMAILS}})
    db.audit_log.delete_many({"metadata.target_email": {"$in": TEST_EMAILS}})


# ----------------------------------------------------------------------
# 1 + 2 + 3 — admin seed idempotency + audit emission.
# ----------------------------------------------------------------------
def test_admin_seed_creates_4_admins_and_is_idempotent(db, roster_path):
    """Two runs must yield exactly the same 4 admin user rows
    against the throwaway roster (NEVER founder emails)."""
    _cleanup_admin_test_rows(db)
    try:
        r1 = _run_admin_seed(roster_path)
        assert r1.returncode == 0, r1.stderr
        for e in TEST_EMAILS:
            n = db.users.count_documents({"email": e})
            assert n == 1, f"first run: {e} count={n}"

        # Second run — must not duplicate or error.
        r2 = _run_admin_seed(roster_path)
        assert r2.returncode == 0, r2.stderr
        for e in TEST_EMAILS:
            n = db.users.count_documents({"email": e})
            assert n == 1, f"idempotent: {e} count={n}"

        # Audit entries — at least one row per admin tagged
        # admin.seed.* and never carrying a password.
        for e in TEST_EMAILS:
            rows = list(db.audit_log.find({"metadata.target_email": e}))
            assert any(row["action"].startswith("admin.seed.") for row in rows), (
                f"no admin.seed.* audit row for {e}"
            )
            for row in rows:
                meta = row.get("metadata", {})
                # The metadata MUST NOT contain the literal password.
                # We don't know it, but we can assert no field looks
                # like a password by key name.
                for k in meta:
                    assert "password" not in k.lower() or k == "password_source", (
                        f"audit metadata key looks like a secret: {k!r}"
                    )
    finally:
        _cleanup_admin_test_rows(db)


def test_admin_seed_promotes_existing_user_without_duplicating(db, roster_path):
    """If a user already exists with the target email, the script
    must PROMOTE (update platform_role) and never create a 2nd row.
    Uses a throwaway @admin8-test.local email, never a founder one."""
    _cleanup_admin_test_rows(db)
    # Pick the charlie@ entry (super_admin in the test roster).
    email = "charlie@admin8-test.local"
    pre_id = str(uuid.uuid4())
    db.users.insert_one({
        "id": pre_id,
        "email": email,
        "full_name": "Charlie (pre-existing)",
        "role": "horse_owner",
        "role_status": "active",
        "platform_role": None,           # no role yet → not a "diff", a promotion
        "password_hash": "$2b$12$placeholder_only_for_test",
        "created_at": "2024-01-01T00:00:00+00:00",
        "_admin8_test": True,
    })
    try:
        r = _run_admin_seed(roster_path)
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
        _cleanup_admin_test_rows(db)


def test_admin_seed_skips_role_change_without_force_flag(db, roster_path):
    """Codex round-1 P1: existing user with a DIFFERENT platform_role
    must be skipped unless --force-role-change is passed."""
    _cleanup_admin_test_rows(db)
    email = "delta@admin8-test.local"  # target role in roster = super_admin
    pre_id = str(uuid.uuid4())
    db.users.insert_one({
        "id": pre_id,
        "email": email,
        "full_name": "Delta (pre-existing)",
        "role": "horse_owner",
        "role_status": "active",
        "platform_role": "billing_admin",  # DIFFERS from target super_admin
        "password_hash": "$2b$12$placeholder_only_for_test",
        "created_at": "2024-01-01T00:00:00+00:00",
        "_admin8_test": True,
    })
    try:
        # First run WITHOUT --force-role-change → must skip.
        r = _run_admin_seed(roster_path)
        assert r.returncode == 0, r.stderr
        after = db.users.find_one({"email": email})
        assert after["platform_role"] == "billing_admin", (
            "platform_role must NOT be overwritten without --force-role-change"
        )
        skipped = list(db.audit_log.find({
            "metadata.target_email": email,
            "action": "admin.seed.skipped_role_diff",
        }))
        assert skipped, "expected an admin.seed.skipped_role_diff audit row"

        # Second run WITH --force-role-change → role flips.
        r2 = _run_admin_seed(roster_path, "--force-role-change")
        assert r2.returncode == 0, r2.stderr
        after2 = db.users.find_one({"email": email})
        assert after2["platform_role"] == "super_admin", (
            "--force-role-change must overwrite the existing platform_role"
        )
        promoted = list(db.audit_log.find({
            "metadata.target_email": email,
            "action": "admin.seed.promoted",
        }))
        assert promoted, "expected an admin.seed.promoted audit row after force"
    finally:
        _cleanup_admin_test_rows(db)


def test_admin_seed_dry_run_does_not_print_passwords(db, roster_path):
    """Codex round-2 P1: --dry-run must NOT mint or print any
    one-time password. The minted value would never persist, so any
    operator who copied it from the output would be holding a
    credential that doesn't work on the real system. The dry-run
    output is also forbidden from containing the literal banner
    text 'ONE-TIME PASSWORDS'."""
    _cleanup_admin_test_rows(db)
    try:
        r = _run_admin_seed(roster_path, "--dry-run")
        assert r.returncode == 0, r.stderr
        stdout = r.stdout

        # Banner must NOT appear in dry-run.
        assert "ONE-TIME PASSWORDS" not in stdout, (
            "dry-run must not print the live ONE-TIME PASSWORDS banner; "
            "got:\n" + stdout
        )

        # No URL-safe 24-char token may appear next to an email — that
        # is the shape of `secrets.token_urlsafe(24)` minted passwords.
        for line in stdout.splitlines():
            m = re.match(r"\s+\S+@\S+\s+(\S+)\s*$", line)
            if not m:
                continue
            candidate = m.group(1)
            # `(would mint password on apply)` ends with `)` — accept it.
            if candidate.startswith("(") and candidate.endswith(")"):
                continue
            # `(...)` parenthetical phrases the script may print.
            if "(" in candidate and ")" in candidate:
                continue
            # Otherwise, any long URL-safe token is a leaked credential.
            assert not re.fullmatch(r"[A-Za-z0-9_\-]{20,}", candidate), (
                f"dry-run output contains a credential-shaped token "
                f"({candidate!r}) — this is the P1 finding."
            )

        # Dry-run must NOT have created any user rows.
        for e in TEST_EMAILS:
            assert db.users.count_documents({"email": e}) == 0, (
                f"dry-run created a real user row for {e}"
            )
    finally:
        _cleanup_admin_test_rows(db)


def test_demo_seed_dry_run_does_not_print_passwords(db):
    """Same invariant as the admin test, applied to the demo seed."""
    # Make sure the demo barn isn't already present from a prior run.
    _run_demo_seed("--teardown")
    try:
        r = _run_demo_seed("--dry-run")
        assert r.returncode == 0, r.stderr
        stdout = r.stdout

        assert "ONE-TIME DEMO PASSWORD" not in stdout, (
            "dry-run must not print the live ONE-TIME DEMO PASSWORD banner"
        )

        for line in stdout.splitlines():
            m = re.match(r"\s+\S+@\S+\s+(\S+)\s*$", line)
            if not m:
                continue
            candidate = m.group(1)
            if candidate.startswith("(") and candidate.endswith(")"):
                continue
            if "(" in candidate and ")" in candidate:
                continue
            assert not re.fullmatch(r"[A-Za-z0-9_\-]{20,}", candidate), (
                f"demo dry-run output contains a credential-shaped "
                f"token ({candidate!r})"
            )

        # And nothing was actually persisted.
        assert db.users.count_documents({"email": "demo.client@equine-sync.com"}) == 0
        assert db.barns.count_documents({"demo_seed_key": "admin8_client_demo"}) == 0
    finally:
        _run_demo_seed("--teardown")


# ----------------------------------------------------------------------
# 4 — no password in logs / audit / committed docs.
# ----------------------------------------------------------------------
def test_no_password_value_in_audit_log(db, roster_path):
    """Run admin seed and demo seed; scan every audit row written for
    anything that looks like the minted bytes."""
    _cleanup_admin_test_rows(db)
    try:
        r1 = _run_admin_seed(roster_path)
        assert r1.returncode == 0, r1.stderr
        r2 = _run_demo_seed()
        assert r2.returncode == 0, r2.stderr

        # Extract minted passwords from stdout.
        passwords = []
        for line in (r1.stdout + r2.stdout).splitlines():
            m = re.match(r"\s+\S+@\S+\s+(\S{20,})\s*$", line)
            if m:
                passwords.append(m.group(1))
        assert passwords, "expected minted passwords to be printed"

        # Confirm none of those passwords appear in audit_log.
        all_audit = list(db.audit_log.find({
            "metadata.target_email": {"$in": TEST_EMAILS},
        }))
        all_audit += list(db.audit_log.find({"actor_email": "(cli)"}))
        as_text = str(all_audit)
        for pw in passwords:
            assert pw not in as_text, (
                "password value leaked into audit_log"
            )
    finally:
        _cleanup_admin_test_rows(db)
        _run_demo_seed("--teardown")


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
        assert barn.get("subscription_id") is None, (
            "demo barn must NOT carry subscription_id"
        )

        # User
        user = db.users.find_one({"email": "demo.client@equine-sync.com"})
        assert user, "demo user missing"
        assert user["role"] == "horse_owner"
        # *** CRITICAL: no platform_role on the demo user.
        assert not user.get("platform_role"), (
            f"demo user must NOT have a platform_role; got "
            f"{user.get('platform_role')!r}"
        )
        assert user["demo_seed_key"] == "admin8_client_demo"
        assert user["created_by_seed"] == "phase_admin_8"

        # Horses (3)
        horses = list(db.horses.find({"demo_seed_key": "admin8_client_demo"}))
        assert len(horses) == 3
        assert {h["name"] for h in horses} == {"Aurelia", "Beacon", "Cinder"}

        # Subscription — Codex round-1 P1: must NOT be Stripe-shaped.
        sub = db.subscriptions.find_one({"demo_seed_key": "admin8_client_demo"})
        assert sub
        assert sub["status"] == "active"
        assert sub["tier"] == "demo"
        # Stripe subscription IDs match ^sub_[A-Za-z0-9]+ and trigger
        # the _STRIPE_VALUE_RE scrubber. Our demo id must not.
        assert not sub["id"].startswith("sub_"), (
            f"demo subscription id must NOT use the Stripe `sub_` prefix; "
            f"got {sub['id']!r}"
        )
        assert sub["id"].startswith("demo_subscription_"), (
            f"demo subscription id must start with `demo_subscription_`; "
            f"got {sub['id']!r}"
        )
    finally:
        _run_demo_seed("--teardown")


def test_demo_seed_extra_owner_creates_second_owner_and_links_horse(db):
    """Extra demo owner is opt-in, demo-tagged, login-ready, and
    linked to one existing demo horse without changing the original
    demo client account."""
    password = "ExtraDemo-" + uuid.uuid4().hex[:12] + "Aa1!"
    try:
        r = _run_demo_seed(
            "--extra-owner",
            extra_env={"SEED_DEMO_EXTRA_OWNER_PASSWORD": password},
        )
        assert r.returncode == 0, r.stderr
        assert "demo.owner2@equine-sync.com" in r.stdout

        primary = db.users.find_one({"email": "demo.client@equine-sync.com"})
        extra = db.users.find_one({"email": "demo.owner2@equine-sync.com"})
        assert primary
        assert extra
        assert primary["id"] != extra["id"]
        assert extra["role"] == "horse_owner"
        assert extra["barn_id"] == primary["barn_id"]
        assert extra["demo_seed_key"] == "admin8_client_demo"
        assert not extra.get("platform_role"), (
            "extra demo owner must not receive admin access"
        )
        assert bcrypt.checkpw(
            password.encode("utf-8"),
            extra["password_hash"].encode("utf-8"),
        )

        beacon = db.horses.find_one({
            "name": "Beacon",
            "demo_seed_key": "admin8_client_demo",
        })
        assert beacon
        assert extra["id"] in (beacon.get("secondary_owner_ids") or [])

        membership = db.account_memberships.find_one({
            "user_id": extra["id"],
            "demo_seed_key": "admin8_client_demo",
        })
        assert membership
        assert membership["account_id"] == extra["barn_id"]
        assert membership["relationship_type"] == "owner"

        audits = list(db.audit_log.find({
            "action": "admin.seed.demo_extra_owner_created",
            "metadata.target_email": "demo.owner2@equine-sync.com",
        }))
        assert audits
        assert password not in str(audits)
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
        assert db.users.count_documents({"email": "demo.owner2@equine-sync.com"}) == 0
        assert db.account_memberships.count_documents({
            "demo_seed_key": "admin8_client_demo",
        }) == 0
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
        cwd=str(ROOT.parent), capture_output=True, text=True, timeout=10,
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
    for py in (ROOT.parent / "backend").rglob("*.py"):
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


# ----------------------------------------------------------------------
# 10 — founder roster guard. Asserts the test suite NEVER touches
# the real founder emails (Codex round-1 P0 invariant).
# ----------------------------------------------------------------------
def test_test_suite_never_targets_real_founder_emails():
    """Sanity check: scan this test file for any literal founder
    email so a future edit cannot regress us back to wiping real
    admin accounts. The check emails are split-built so this test
    itself does not contain the offending literal."""
    real_emails = [
        "info" + "@" + "equine-sync.com",
        "prsindustries23" + "@" + "gmail.com",
        "rian.ray2012" + "@" + "gmail.com",
        "prspoon23" + "@" + "gmail.com",
    ]
    this_file = pathlib.Path(__file__).read_text()
    for e in real_emails:
        # Use ``find`` over the literal we constructed at runtime
        # (the constant never appears whole in the file source).
        assert this_file.find(e) == -1, (
            f"test file must never reference real founder email {e!r}; "
            f"use a throwaway @admin8-test.local address instead."
        )
