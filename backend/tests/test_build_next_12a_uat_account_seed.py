"""BN12A UAT account seed checks."""
from __future__ import annotations

import os
import re
import subprocess
import sys
import uuid
from pathlib import Path

import bcrypt
import certifi
from pymongo import MongoClient


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
README = ROOT / "BUILD_NEXT_12A_UAT_ACCOUNT_SEED_README.md"
ROLE_CHECKLIST = ROOT / "docs/BUILD_NEXT_12_ROLE_READINESS_CHECKLIST.md"
SCRIPT = BACKEND / "scripts/seed_bn12_uat_accounts.py"

ROSTER_EMAILS = [
    "uat.platform@equine-sync.com",
    "uat.facility-admin@equine-sync.com",
    "uat.manager@equine-sync.com",
    "uat.staff@equine-sync.com",
    "uat.owner@equine-sync.com",
    "uat.guardian@equine-sync.com",
    "uat.participant@equine-sync.com",
    "uat.individual-owner@equine-sync.com",
]


def _mongo_url() -> str:
    return os.environ.get("MONGO_URL") or "mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=3000"


def _run(*args: str, db_name: str, extra_env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env.update({
        "MONGO_URL": _mongo_url(),
        "DB_NAME": db_name,
        "APP_ENV": "development",
    })
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, "-m", "scripts.seed_bn12_uat_accounts", *args],
        cwd=str(BACKEND),
        env=env,
        text=True,
        capture_output=True,
        timeout=60,
    )


def _db(name: str):
    return MongoClient(_mongo_url())[name]


def test_bn12a_artifacts_exist_and_list_all_roles():
    assert README.exists()
    assert SCRIPT.exists()
    text = README.read_text(encoding="utf-8") + "\n" + ROLE_CHECKLIST.read_text(encoding="utf-8")
    for email in ROSTER_EMAILS:
        assert email in text
    for row in [f"UAT-R{i}" for i in range(1, 9)]:
        assert row in text


def test_bn12a_mongo_clients_use_certifi_for_atlas_tls():
    from core.mongo import mongo_client_kwargs

    kwargs = mongo_client_kwargs("mongodb+srv://user:pw@example.mongodb.net/ES_Members")
    assert kwargs["tlsCAFile"] == certifi.where()
    assert mongo_client_kwargs("mongodb://127.0.0.1:27017") == {}


def test_bn12a_dry_run_mints_no_passwords_and_writes_nothing():
    db_name = f"test_bn12a_dry_{uuid.uuid4().hex[:8]}"
    database = _db(db_name)
    try:
        proc = _run("--dry-run", db_name=db_name)
        assert proc.returncode == 0, proc.stderr
        out = proc.stdout
        assert "DRY-RUN: no passwords minted, none printed." in out
        assert "ONE-TIME PASSWORDS" not in out
        assert not re.search(r"\b[A-Za-z0-9_-]{24,}\b", "\n".join(
            line for line in out.splitlines() if "would mint" not in line
        ))
        assert database.users.count_documents({"uat_seed_key": "bn12_uat_accounts"}) == 0
        assert database.barns.count_documents({"uat_seed_key": "bn12_uat_accounts"}) == 0
    finally:
        database.client.drop_database(db_name)


def test_bn12a_seed_creates_8_accounts_memberships_and_passwords_once():
    db_name = f"test_bn12a_seed_{uuid.uuid4().hex[:8]}"
    database = _db(db_name)
    try:
        proc = _run(db_name=db_name)
        assert proc.returncode == 0, proc.stderr
        out = proc.stdout
        assert "BN12A ONE-TIME PASSWORDS" in out
        assert out.count("@equine-sync.com") >= 8

        users = list(database.users.find({"uat_seed_key": "bn12_uat_accounts"}, {"_id": 0}))
        assert len(users) == 8
        by_email = {u["email"]: u for u in users}
        assert set(by_email) == set(ROSTER_EMAILS)
        assert by_email["uat.platform@equine-sync.com"]["platform_role"] == "platform_admin"
        assert by_email["uat.platform@equine-sync.com"]["full_name"] == "Platform Admin"
        assert by_email["uat.facility-admin@equine-sync.com"]["full_name"] == "Facility Admin"
        assert by_email["uat.owner@equine-sync.com"]["full_name"] == "Horse Owner"
        assert by_email["uat.individual-owner@equine-sync.com"].get("barn_id") is None
        assert by_email["uat.individual-owner@equine-sync.com"]["role"] == "horse_owner"
        assert by_email["uat.individual-owner@equine-sync.com"]["full_name"] == "Individual Owner"
        assert all(u["email_verified"] is True for u in users)
        assert all(u["account_status"] == "active" for u in users)

        memberships = list(database.account_memberships.find(
            {"uat_seed_key": "bn12_uat_accounts"}, {"_id": 0},
        ))
        assert len(memberships) == 8
        individual = next(
            m for m in memberships
            if m["user_id"] == by_email["uat.individual-owner@equine-sync.com"]["id"]
        )
        assert individual["account_type"] == "individual_owner"
        assert individual["account_id"].startswith("acct_owner_")

        audit = list(database.audit_log.find(
            {"action": "bn12.uat_account.seeded"}, {"_id": 0},
        ))
        assert len(audit) == 8
        for entry in audit:
            metadata = entry["metadata"]
            assert set(metadata) == {
                "uat_id",
                "target_email",
                "role",
                "platform_role",
                "barn_id_present",
                "password_source",
                "password_action",
                "seed_phase",
            }
            assert metadata["password_source"] in {"mint", "env", "n/a (existing user)"}
            assert metadata["password_action"] in {"set", "reset", "not_changed"}
        audit_text = str(audit)
        for line in out.splitlines():
            if "@equine-sync.com" not in line:
                continue
            maybe_password = line.rsplit(maxsplit=1)[-1]
            if len(maybe_password) >= 20:
                assert maybe_password not in audit_text

        second = _run(db_name=db_name)
        assert second.returncode == 0, second.stderr
        assert "BN12A ONE-TIME PASSWORDS" not in second.stdout
        assert database.users.count_documents({"uat_seed_key": "bn12_uat_accounts"}) == 8

        database.barns.update_one(
            {"id": "bn12_uat_facility"},
            {"$set": {"name": "BN12 UAT Facility"}},
        )
        refreshed = _run(db_name=db_name)
        assert refreshed.returncode == 0, refreshed.stderr
        barn = database.barns.find_one({"id": "bn12_uat_facility"})
        assert barn["name"] == "EquineSync Pilot Stable"
    finally:
        database.client.drop_database(db_name)


def test_bn12a_env_password_and_reset_existing_password():
    db_name = f"test_bn12a_reset_{uuid.uuid4().hex[:8]}"
    database = _db(db_name)
    env = {"SEED_BN12_UAT_OWNER_EQUINE_SYNC_COM_PASSWORD": "BN12OwnerPassOne!234"}
    try:
        first = _run(db_name=db_name, extra_env=env)
        assert first.returncode == 0, first.stderr
        owner = database.users.find_one({"email": "uat.owner@equine-sync.com"})
        assert bcrypt.checkpw(env["SEED_BN12_UAT_OWNER_EQUINE_SYNC_COM_PASSWORD"].encode(), owner["password_hash"].encode())

        reset_env = {"SEED_BN12_UAT_OWNER_EQUINE_SYNC_COM_PASSWORD": "BN12OwnerPassTwo!234"}
        reset = _run("--reset-passwords", db_name=db_name, extra_env=reset_env)
        assert reset.returncode == 0, reset.stderr
        owner = database.users.find_one({"email": "uat.owner@equine-sync.com"})
        assert bcrypt.checkpw(reset_env["SEED_BN12_UAT_OWNER_EQUINE_SYNC_COM_PASSWORD"].encode(), owner["password_hash"].encode())
    finally:
        database.client.drop_database(db_name)


def test_bn12a_seed_clears_existing_login_attempt_lockouts():
    db_name = f"test_bn12a_lockout_{uuid.uuid4().hex[:8]}"
    database = _db(db_name)
    try:
        database.login_attempts.insert_one({
            "email": "uat.platform@equine-sync.com",
            "count": 5,
            "locked_until": "2999-01-01T00:00:00+00:00",
        })
        proc = _run(db_name=db_name)
        assert proc.returncode == 0, proc.stderr
        assert database.login_attempts.find_one({"email": "uat.platform@equine-sync.com"}) is None
    finally:
        database.client.drop_database(db_name)


def test_bn12a_production_writes_require_allow_prod_but_dry_run_allowed():
    db_name = f"test_bn12a_prod_{uuid.uuid4().hex[:8]}"
    database = _db(db_name)
    env = os.environ.copy()
    env.update({
        "MONGO_URL": _mongo_url(),
        "DB_NAME": db_name,
        "APP_ENV": "production",
    })
    try:
        blocked = subprocess.run(
            [sys.executable, "-m", "scripts.seed_bn12_uat_accounts"],
            cwd=str(BACKEND),
            env=env,
            text=True,
            capture_output=True,
            timeout=60,
        )
        assert blocked.returncode == 2
        assert "--allow-prod" in blocked.stderr

        allowed_preview = subprocess.run(
            [sys.executable, "-m", "scripts.seed_bn12_uat_accounts", "--dry-run"],
            cwd=str(BACKEND),
            env=env,
            text=True,
            capture_output=True,
            timeout=60,
        )
        assert allowed_preview.returncode == 0, allowed_preview.stderr
        assert "DRY-RUN" in allowed_preview.stdout
        assert database.users.count_documents({"uat_seed_key": "bn12_uat_accounts"}) == 0
    finally:
        database.client.drop_database(db_name)


def test_bn12a_docs_do_not_contain_secret_values_or_launch_approval():
    text = README.read_text(encoding="utf-8") + "\n" + ROLE_CHECKLIST.read_text(encoding="utf-8")
    forbidden = [
        "sk" + "_live_",
        "rk" + "_live_",
        "re" + "_",
        "wh" + "sec_",
        "-----" + "BEGIN",
        "Authorization" + ": Bearer",
        "mongodb" + "+srv://",
        "password" + ":",
        "launch approved",
        "pilot approved",
        "ready for unrestricted launch",
    ]
    for fragment in forbidden:
        assert fragment not in text
