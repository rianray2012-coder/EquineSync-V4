#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/STAGE_24_PROFILE_ACTIVATION_CUSTODY_V1")
PHASE_A_PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_AND_STAGE_24_READINESS_REBASE_V1")
START_HEAD = "f5b2973c9a796d6864607dcae42aa6c89f894250"
ADOPTED_PROFILE = Path("governance/implementation/code-guides/profiles/ES-CODE-GUIDE-SOLO-FOUNDER-COMPENSATING-ASSURANCE-PROFILE-V1.0.0.md")
ADOPTED_SHA = "ef82faf0af5f33182014b75b35a59fbee25596f4ea1a5da52378de3ed54d2c2b"
ADOPTED_BYTES = 9681
EFFECTIVE_EVENT = "VERIFIED_PROTECTED_MERGE_OF_THE_POST_PR_59_STAGE_24_CUSTODY_PR"
DISPOSITION_ID = "ES-FD-CGP-006-STAGE-24-LIMITED-ACTIVATION-2026-07-30"
FINAL_TOKENS = {
    "SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_V1_0_0_ADOPTED_AND_ACTIVE",
    "ES_CG_00_ACTIVE_FOR_PLANNING_REFERENCE_IMPLEMENTATION_CONTROL_AND_PULL_REQUEST_REVIEW",
    "ES_CG_01_ACTIVE_FOR_PLANNING_REFERENCE_IMPLEMENTATION_CONTROL_AND_PULL_REQUEST_REVIEW",
    "ES_CG_10_ACTIVE_FOR_PLANNING_REFERENCE_IMPLEMENTATION_CONTROL_AND_PULL_REQUEST_REVIEW",
    "ES_CG_13_ACTIVE_FOR_PLANNING_REFERENCE_IMPLEMENTATION_CONTROL_AND_PULL_REQUEST_REVIEW",
    "MERGE_GATE_NOT_ACTIVE",
    "RELEASE_GATE_NOT_ACTIVE",
    "OPERATIONS_REFERENCE_NOT_ACTIVE",
    "TWELVE_RESIDUAL_RISKS_ACCEPTED_FOR_LIMITED_STAGE_24_ACTIVATION_ONLY",
    "GAP_0004_REMAINS_OPEN",
    "IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
}
ALLOWED_PATHS = {
    "governance/implementation/code-guides/PROGRAM_STATUS.md",
    "governance/implementation/code-guides/registers/GUIDE_ACTIVATION_REGISTER.csv",
    "governance/implementation/code-guides/registers/CODE_GUIDE_AUTHORITY_REGISTER.csv",
    "governance/implementation/code-guides/registers/IMPLEMENTATION_PROFILE_REGISTER.csv",
    "governance/implementation/code-guides/profiles/ES-CODE-GUIDE-SOLO-FOUNDER-COMPENSATING-ASSURANCE-PROFILE-V1.0.0.md",
    "governance/implementation/code-guides/receipts/CGP_006_STAGE_24_PROFILE_ACTIVATION_CUSTODY_RECEIPT.md",
    "governance/implementation/code-guides/validation/validate_activation_records.py",
    "governance/implementation/code-guides/validation/tests/test_validate_activation_records.py",
    "governance/implementation/code-guides/validation/cgp_validation.py",
    "governance/implementation/code-guides/validation/tests/test_wave1_current_status_custody_table.py",
}
ALLOWED_PR61_REMEDIATION_PATHS = {
    (PHASE_A_PACKAGE_REL / rel).as_posix()
    for rel in {
        "BUGBOT_PR59_FINDINGS_REPORT.md",
        "CHECKSUM_MANIFEST.sha256",
        "DIRECTIVE_EXECUTION_RECORD.md",
        "ES-CODE-GUIDE-SOLO-FOUNDER-COMPENSATING-ASSURANCE-PROFILE-V1.0.0.md",
        "FOUNDER_STAGE_24_LIMITED_ACTIVATION_DECISION_PACKET.md",
        "MULTI_PASS_REVIEW_RECONCILIATION_REPORT.md",
        "PACKAGE_MANIFEST.json",
        "README.md",
        "SOURCE_FREEZE_MANIFEST.json",
        "SOURCE_REGISTER.md",
        "SOURCE_SHA256SUMS.txt",
        "STAGE_24_FOUNDER_DISPOSITION_PRE_CUSTODY_RECORD.md",
        "tests/test_solo_founder_assurance_stage24_readiness.py",
        "validators/validate_solo_founder_assurance_stage24_readiness.py",
    }
}

class ValidationError(Exception):
    pass

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def changed_paths(root: Path) -> list[str]:
    out = subprocess.check_output(["git", "diff", "--name-only", START_HEAD, "HEAD"], cwd=root, text=True)
    return [line for line in out.splitlines() if line]

def check_authorized_paths(paths: list[str]) -> None:
    allowed_prefix = PACKAGE_REL.as_posix() + "/"
    outside = [p for p in paths if not (p.startswith(allowed_prefix) or p in ALLOWED_PATHS or p in ALLOWED_PR61_REMEDIATION_PATHS)]
    if outside:
        raise ValidationError(f"unauthorized path changed: {outside}")

def validate(root: Path | None = None, *, enforce_git_paths: bool = True) -> dict[str, object]:
    root = (root or Path.cwd()).resolve()
    pkg = root / PACKAGE_REL
    if not pkg.exists():
        raise ValidationError("custody package missing")
    if sha(root / ADOPTED_PROFILE) != ADOPTED_SHA or len((root / ADOPTED_PROFILE).read_bytes()) != ADOPTED_BYTES:
        raise ValidationError("canonical adopted profile identity mismatch")
    activation = rows(root / "governance/implementation/code-guides/registers/GUIDE_ACTIVATION_REGISTER.csv")
    active = [r for r in activation if r["guide_id"] in {"ES-CG-00", "ES-CG-01", "ES-CG-10", "ES-CG-13"}]
    if len(active) != 4:
        raise ValidationError("active guide rows missing")
    for row in active:
        if row["activation_state"] != "ACTIVE_LIMITED_STAGE_24":
            raise ValidationError("active guide state mismatch")
        for scope in ["PLANNING_REFERENCE", "IMPLEMENTATION_CONTROL", "PULL_REQUEST_REVIEW"]:
            if row[scope] != "TRUE":
                raise ValidationError("approved scope not active")
        for scope in ["MERGE_GATE", "RELEASE_GATE", "OPERATIONS_REFERENCE"]:
            if row[scope] != "FALSE":
                raise ValidationError("deferred scope active")
        if row["effective_date"] != EFFECTIVE_EVENT:
            raise ValidationError("effective event mismatch")
    if any(r["activation_state"] != "NOT_ACTIVE" for r in activation if r["guide_id"] not in {"ES-CG-00", "ES-CG-01", "ES-CG-10", "ES-CG-13"}):
        raise ValidationError("non-Wave-1 guide active")
    authority = rows(root / "governance/implementation/code-guides/registers/CODE_GUIDE_AUTHORITY_REGISTER.csv")
    if not any(r["authority_id"] == "CGP-V11-AUTH-0007" and r["status"] == "CUSTODY_COMPLETE_CONTROLLING" for r in authority):
        raise ValidationError("authority register missing Stage 24 custody authority")
    profiles = rows(root / "governance/implementation/code-guides/registers/IMPLEMENTATION_PROFILE_REGISTER.csv")
    if not any(r["profile_file"] == ADOPTED_PROFILE.name and r["repository_specific_mapping_allowed"] == "NO" for r in profiles):
        raise ValidationError("profile register missing no-mapping profile")
    status_text = (root / "governance/implementation/code-guides/PROGRAM_STATUS.md").read_text(encoding="utf-8")
    for token in FINAL_TOKENS:
        if token not in status_text:
            raise ValidationError(f"PROGRAM_STATUS missing final token: {token}")
    for token in ("REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AUTHORIZED", "IMPLEMENTATION_AUTHORIZED", "DEPLOYMENT_AUTHORIZED", "PILOT_AUTHORIZED", "PRODUCTION_AUTHORIZED"):
        if token in status_text:
            raise ValidationError(f"prohibited token present: {token}")
    manifest = json.loads((pkg / "SOURCE_FREEZE_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("pr59", {}).get("merge_commit") != START_HEAD:
        raise ValidationError("PR #59 merge metadata mismatch")
    if manifest.get("adopted_profile", {}).get("sha256") != ADOPTED_SHA:
        raise ValidationError("manifest adopted profile mismatch")
    package_manifest = json.loads((pkg / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    for entry in package_manifest["files"]:
        p = pkg / entry["path"]
        if sha(p) != entry["sha256"] or len(p.read_bytes()) != entry["byte_length"]:
            raise ValidationError(f"package manifest identity mismatch: {entry['path']}")
    for line in (pkg / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        if sha(pkg / rel) != digest:
            raise ValidationError(f"checksum mismatch: {rel}")
    if enforce_git_paths:
        check_authorized_paths(changed_paths(root))
    return {"status": "PASS", "active_guides": 4, "risk_decisions": 12, "package": str(pkg)}

def main() -> int:
    try:
        print(json.dumps(validate(Path.cwd()), indent=2, sort_keys=True))
    except ValidationError as exc:
        print(f"FAIL: {exc}")
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
