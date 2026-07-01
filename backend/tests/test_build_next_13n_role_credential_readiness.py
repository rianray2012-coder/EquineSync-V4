"""Build-Next-13N role credential-readiness checks."""
from __future__ import annotations

import importlib.util
import py_compile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_13N_ROLE_CREDENTIAL_READINESS_README.md"
REPORT = ROOT / "outputs" / "build_next_13n_role_credential_readiness_report.md"
SCRIPT = ROOT / "backend" / "scripts" / "seed_bn13_role_smoke_accounts.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_script_module():
    spec = importlib.util.spec_from_file_location("seed_bn13_role_smoke_accounts", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bn13n_artifacts_exist():
    for path in [README, REPORT, SCRIPT]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 1000, str(path)


def test_bn13n_script_compiles_and_has_expected_roster():
    py_compile.compile(str(SCRIPT), doraise=True)
    module = _load_script_module()
    roster = module.BN13_ROLE_SMOKE_ROSTER
    assert len(roster) == 11

    expected = {
        "UAT-R1": ("uat.platform@equine-sync.com", "admin", "platform_admin"),
        "UAT-R2a": ("uat.facility-admin@equine-sync.com", "admin", None),
        "UAT-R2b": ("uat.barn-owner@equine-sync.com", "barn_owner", None),
        "BN13M-T1": ("uat.trainer@equine-sync.com", "trainer", None),
        "UAT-R3": ("uat.manager@equine-sync.com", "barn_manager", None),
        "UAT-R4a": ("uat.staff@equine-sync.com", "groom", None),
        "BN13M-W1": ("uat.working-student@equine-sync.com", "working_student", None),
        "UAT-R5": ("uat.owner@equine-sync.com", "horse_owner", None),
        "UAT-R6": ("uat.guardian@equine-sync.com", "parent", None),
        "UAT-R7": ("uat.participant@equine-sync.com", "rider", None),
        "UAT-R8": ("uat.individual-owner@equine-sync.com", "horse_owner", None),
    }
    by_row = {item["row"]: item for item in roster}
    for row, (email, role, platform_role) in expected.items():
        assert by_row[row]["email"] == email
        assert by_row[row]["role"] == role
        assert by_row[row]["platform_role"] == platform_role


def test_bn13n_script_uses_safe_production_and_dry_run_guards():
    src = _read(SCRIPT)
    for phrase in [
        "--dry-run",
        "--allow-prod",
        "--reset-passwords",
        "DRY-RUN: no passwords minted, none printed.",
        "APP_ENV is production. Pass --allow-prod",
        "would_mint_on_apply",
        "bn13.role_smoke_account.seeded",
    ]:
        assert phrase in src


def test_bn13n_report_lists_every_env_var_without_values():
    text = _read(REPORT)
    for env_name in [
        "SEED_BN13_UAT_PLATFORM_EQUINE_SYNC_COM_PASSWORD",
        "SEED_BN13_UAT_FACILITY_ADMIN_EQUINE_SYNC_COM_PASSWORD",
        "SEED_BN13_UAT_BARN_OWNER_EQUINE_SYNC_COM_PASSWORD",
        "SEED_BN13_UAT_TRAINER_EQUINE_SYNC_COM_PASSWORD",
        "SEED_BN13_UAT_MANAGER_EQUINE_SYNC_COM_PASSWORD",
        "SEED_BN13_UAT_STAFF_EQUINE_SYNC_COM_PASSWORD",
        "SEED_BN13_UAT_WORKING_STUDENT_EQUINE_SYNC_COM_PASSWORD",
        "SEED_BN13_UAT_OWNER_EQUINE_SYNC_COM_PASSWORD",
        "SEED_BN13_UAT_GUARDIAN_EQUINE_SYNC_COM_PASSWORD",
        "SEED_BN13_UAT_PARTICIPANT_EQUINE_SYNC_COM_PASSWORD",
        "SEED_BN13_UAT_INDIVIDUAL_OWNER_EQUINE_SYNC_COM_PASSWORD",
    ]:
        assert env_name in text

    for unsafe in [
        "YOUR_PASSWORD",
        "PRIVATE_PASSWORD",
        "sk_live_",
        "rk_live_",
        "pk_live_",
        "BEGIN RSA PRIVATE KEY",
        "BEGIN PRIVATE KEY",
    ]:
        assert unsafe not in text


def test_bn13n_docs_do_not_claim_live_execution_or_screenshots():
    text = _read(README) + "\n" + _read(REPORT)
    assert "No live database writes are performed by this package" in text
    assert "No screenshots" in text
    assert "Rerun BN13M with credentialed browser sessions" in text
    assert "launch approved" not in text.lower()
