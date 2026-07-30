#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

DOCUMENT_ID = "ES-FD-SOLO-FOUNDER-COMPENSATING-ASSURANCE-2026-07-29"
VERSION = "1.0.0"
START_HEAD = "7e42d7e0338d55c75fc6be766fcf08b24b687246"
PACKAGE_REL = Path("governance/implementation/code-guides/founder-determinations/ES-FD-SOLO-FOUNDER-COMPENSATING-ASSURANCE-2026-07-29")
DOC_NAME = "FOUNDER_DETERMINATION_SOLO_FOUNDER_COMPENSATING_ASSURANCE_MODEL_2026-07-29.md"
APPROVAL_DISPOSITION = "APPROVED_AS_CONTROLLING_FOUNDER_DETERMINATION_FOR_SOLO_FOUNDER_COMPENSATING_ASSURANCE_AND_REVIEW_GATE_RECLASSIFICATION"
REQUIRED_FILES = [
    DOC_NAME,
    "FOUNDER_APPROVAL_RECORD.md",
    "SOURCE_PAYLOAD_ORIGINAL.md",
    "TEXTUAL_CORRECTION_AND_APPROVAL_FINALIZATION_LEDGER.csv",
    "SOURCE_TO_APPROVED_TEXT_DIFF_REPORT.md",
    "AUTHORITY_AND_EFFECT_RECORD.md",
    "ACCESSION_READINESS_REPORT.md",
    "AUTHORIZED_PATH_REPORT.md",
    "VALIDATION_REPORT.md",
    "UNAUTHORIZED_EDITORIAL_OBSERVATIONS.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validators/validate_founder_approved_solo_founder_determination.py",
    "tests/test_founder_approved_solo_founder_determination.py",
]
REQUIRED_CLOSING = [
    "PROGRAM_PLAN_V1_1_CONTROLLING",
    "FOUNDER_DETERMINATION_FOUNDER_APPROVED",
    "FOUNDER_APPROVAL_DATE_2026_07_29",
    "AUTHORIZED_TEXTUAL_CORRECTIONS_APPLIED",
    "MEDICAL_OR_SAFETY_TOKEN_CORRECTED",
    "SECURITY_AND_NEGATIVE_TOKEN_CORRECTED",
    "THREE_TOTAL_AUTHORIZED_TOKEN_CORRECTIONS_APPLIED",
    "AUTHORIZED_APPROVAL_METADATA_FINALIZATION_APPLIED",
    "NO_OTHER_SUBSTANTIVE_CHANGE_AUTHORIZED",
    "NO_OTHER_SUBSTANTIVE_CHANGE_PERFORMED",
    "APPROVED_SHA256_RECORDED_IN_COMPANION_APPROVAL_RECORD",
    "APPROVED_BYTE_LENGTH_RECORDED_IN_COMPANION_APPROVAL_RECORD",
    "PROTECTED_REPOSITORY_ACCESSION_COMPLETE",
    "POST_MERGE_CUSTODY_COMPLETE",
    "SOLO_FOUNDER_COMPENSATING_ASSURANCE_DETERMINATION_CONTROLLING",
    "FOUNDER_DOMAIN_OWNER_QUALIFICATION_ESTABLISHED",
    "INDEPENDENT_HUMAN_TECHNICAL_REVIEW_NOT_PERFORMED",
    "OUTSIDE_HUMAN_DOMAIN_EXPERT_REVIEW_NOT_PERFORMED",
    "NO_INDEPENDENT_ASSURANCE_CLAIM_AUTHORIZED",
    "RETAINED_CONDITIONS_REMAIN_OPEN_PENDING_READINESS_REBASE",
    "RETAINED_WARNINGS_REMAIN_OPEN_PENDING_READINESS_REBASE",
    "GAP_0004_REMAINS_OPEN",
    "STAGE_24_GUIDE_ACTIVATION_NOT_AUTHORIZED",
    "ES_CG_00_REMAINS_NOT_ACTIVE",
    "ES_CG_01_REMAINS_NOT_ACTIVE",
    "ES_CG_10_REMAINS_NOT_ACTIVE",
    "ES_CG_13_REMAINS_NOT_ACTIVE",
    "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED",
    "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "DEPLOYMENT_NOT_AUTHORIZED",
    "PILOT_NOT_AUTHORIZED",
    "PRODUCTION_NOT_AUTHORIZED",
    "WAVE_2_NOT_AUTHORIZED",
    "CGP_007_NOT_AUTHORIZED",
    "NEXT_WORKSTREAM_SOLO_FOUNDER_ASSURANCE_PROFILE_AND_STAGE_24_READINESS_REBASE",
]

REPLACEMENTS = [
    ("SFCA-TXT-001", "MEDICAL_OR SAFETY", "MEDICAL_OR_SAFETY", 2),
    ("SFCA-TXT-002", "SECURITY_AND NEGATIVE", "SECURITY_AND_NEGATIVE", 1),
    ("SFCA-APP-001", "**Founder Approval Date:** Pending exact-byte Founder approval", "**Founder Approval Date:** 2026-07-29", 1),
    ("SFCA-APP-002", "**Effective Date:** Upon exact-byte Founder approval for preparatory authority; controlling repository effect upon protected accession and custody", "**Effective Date:** 2026-07-29 for preparatory authority; controlling repository effect upon protected accession and custody", 1),
    ("SFCA-APP-003", "**Exact Approved SHA-256:** To be recorded after exact-byte approval", "**Exact Approved SHA-256:** Recorded in companion FOUNDER_APPROVAL_RECORD.md", 1),
    ("SFCA-APP-004", "**Approved Byte Length:** To be recorded after exact-byte approval", "**Approved Byte Length:** Recorded in companion FOUNDER_APPROVAL_RECORD.md", 1),
    ("SFCA-APP-005", "**Protected Accession Commit:** Pending", "**Protected Accession Commit:** Pending protected merge", 2),
    ("SFCA-APP-006", "**Repository Custody Receipt:** Pending", "**Repository Custody Receipt:** Pending post-merge custody", 1),
    ("SFCA-APP-007", "Upon exact-byte approval, the Founder disposition shall be:", "The Founder disposition is:", 1),
    ("SFCA-APP-008", "**Founder Decision:** Pending", f"**Founder Decision:** {APPROVAL_DISPOSITION}", 1),
    ("SFCA-APP-009", "**Approved Date:** Pending", "**Approved Date:** 2026-07-29", 1),
    ("SFCA-APP-010", "**Approved SHA-256:** Pending", "**Approved SHA-256:** Recorded in companion FOUNDER_APPROVAL_RECORD.md", 1),
    ("SFCA-APP-011", "**Approved Byte Length:** Pending", "**Approved Byte Length:** Recorded in companion FOUNDER_APPROVAL_RECORD.md", 1),
    ("SFCA-APP-012", "**Protected Accession PR:** Pending", "**Protected Accession PR:** Pending protected accession workflow", 1),
    ("SFCA-APP-013", "**Post-Merge Custody Receipt:** Pending", "**Post-Merge Custody Receipt:** Pending post-merge custody workflow", 1),
    ("SFCA-APP-014", "**Founder:** ______________________________", "**Founder:** EquineSync Founder", 1),
    ("SFCA-APP-015", "**Date:** _________________________________", "**Date:** 2026-07-29", 1),
    ("SFCA-APP-016", "**Approval Method:** ______________________", "**Approval Method:** Explicit written Founder instruction dated 2026-07-29", 1),
    ("SFCA-APP-017", "**Exact SHA-256:** ________________________", "**Exact SHA-256:** Recorded in companion FOUNDER_APPROVAL_RECORD.md", 1),
    ("SFCA-APP-018", "**Approved Byte Length:** _________________", "**Approved Byte Length:** Recorded in companion FOUNDER_APPROVAL_RECORD.md", 1),
]

class ValidationError(AssertionError):
    pass

def repo_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def canonical(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(line.rstrip(" \t") for line in lines) + "\n"

def apply_authorized_changes(source: str) -> str:
    text = canonical(source)
    for cid, old, new, expected in REPLACEMENTS:
        actual = text.count(old)
        if actual != expected:
            raise ValidationError(f"{cid} occurrence count mismatch: expected {expected}, got {actual}")
        text = text.replace(old, new)
    return canonical(text)

def assert_serialization(path: Path) -> None:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValidationError(f"BOM present: {path}")
    if b"\r" in data:
        raise ValidationError(f"Non-LF line ending present: {path}")
    if not data.endswith(b"\n") or data.endswith(b"\n\n"):
        raise ValidationError(f"Terminal newline must be exactly one: {path}")
    for number, line in enumerate(data.split(b"\n")[:-1], 1):
        if line.endswith((b" ", b"\t")):
            raise ValidationError(f"Trailing whitespace at {path}:{number}")
    data.decode("utf-8")

def extract_backtick_value(text: str, label: str) -> str:
    prefix = f"**{label}:** `"
    for line in text.splitlines():
        if line.startswith(prefix) and line.endswith("`"):
            return line[len(prefix):-1]
        plain_prefix = f"**{label}:** "
        if line.startswith(plain_prefix):
            return line[len(plain_prefix):].strip()
    raise ValidationError(f"Missing field: {label}")

def validate(root: Path | None = None, enforce_git_paths: bool = True) -> dict[str, object]:
    repo = root or repo_root()
    package = repo / PACKAGE_REL
    missing = [rel for rel in REQUIRED_FILES if not (package / rel).is_file()]
    if missing:
        raise ValidationError(f"Missing required files: {missing}")
    for rel in REQUIRED_FILES:
        if rel.endswith((".md", ".csv", ".json", ".py", ".sha256")):
            assert_serialization(package / rel)
    source = (package / "SOURCE_PAYLOAD_ORIGINAL.md").read_text(encoding="utf-8")
    doc = (package / DOC_NAME).read_text(encoding="utf-8")
    if not source.startswith("# EQUINESYNC FOUNDER DETERMINATION"):
        raise ValidationError("Source opening boundary missing")
    if not source.rstrip("\n").endswith("`STAGE_24_FOUNDER_ACTIVATION_DISPOSITION_PENDING`"):
        raise ValidationError("Source closing boundary missing")
    if source.count("MEDICAL_OR SAFETY") != 2 or source.count("SECURITY_AND NEGATIVE") != 1:
        raise ValidationError("Authorized correction count mismatch")
    expected = apply_authorized_changes(source)
    if doc != expected:
        raise ValidationError("Unauthorized textual difference in approved determination")
    if "FOUNDER_APPROVAL_CANDIDATE" in doc:
        raise ValidationError("Document remains marked Founder approval candidate")
    if extract_backtick_value(doc, "Founder Approval Status") != "FOUNDER_APPROVED":
        raise ValidationError("Founder approval status is not finalized")
    if extract_backtick_value(doc, "Founder Approval Date") != "2026-07-29":
        raise ValidationError("Founder approval date is missing or incorrect")
    if APPROVAL_DISPOSITION not in doc:
        raise ValidationError("Approval disposition missing")
    doc_sha = sha(package / DOC_NAME)
    doc_len = len((package / DOC_NAME).read_bytes())
    if doc_sha in doc or str(doc_len) in doc:
        raise ValidationError("Self-referential literal hash or byte length appears in determination")
    prohibited = [
        "STAGE_24_GUIDE_ACTIVATION_AUTHORIZED",
        "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AUTHORIZED",
        "IMPLEMENTATION_AUTHORIZED_BY_THIS_DETERMINATION",
        "DEPLOYMENT_AUTHORIZED",
        "PILOT_AUTHORIZED",
    ]
    for token in prohibited:
        if token in doc:
            raise ValidationError(f"Prohibited authority token present: {token}")
    approval = (package / "FOUNDER_APPROVAL_RECORD.md").read_text(encoding="utf-8")
    if doc_sha not in approval or str(doc_len) not in approval:
        raise ValidationError("Companion approval record lacks final hash or byte length")
    for token in REQUIRED_CLOSING:
        for rel in ["FOUNDER_APPROVAL_RECORD.md", "ACCESSION_READINESS_REPORT.md", "VALIDATION_REPORT.md"]:
            if token not in (package / rel).read_text(encoding="utf-8"):
                raise ValidationError(f"{rel} missing closing statement {token}")
    with (package / "TEXTUAL_CORRECTION_AND_APPROVAL_FINALIZATION_LEDGER.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    by_id = {row["change_id"]: row for row in rows}
    if by_id["SFCA-TXT-001"]["actual_occurrences"] != "2" or by_id["SFCA-TXT-002"]["actual_occurrences"] != "1":
        raise ValidationError("Ledger token correction counts are wrong")
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    def package_files_for_manifest() -> list[str]:
        return sorted(
            p.relative_to(package).as_posix()
            for p in package.rglob("*")
            if p.is_file()
            and p.name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"}
            and "__pycache__" not in p.parts
            and p.suffix != ".pyc"
        )

    manifest_paths = [entry["path"] for entry in manifest["files"]]
    expected_paths = package_files_for_manifest()
    if manifest_paths != expected_paths:
        raise ValidationError("Package manifest path mismatch")
    for entry in manifest["files"]:
        if sha(package / entry["path"]) != entry["sha256"]:
            raise ValidationError(f"Manifest checksum mismatch: {entry['path']}")
    checksum_entries = {}
    for line in (package / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            digest, rel = line.split("  ", 1)
        except ValueError as exc:
            raise ValidationError(f"Malformed checksum line: {line}") from exc
        checksum_entries[rel] = digest
    expected_checksum_paths = sorted(
        p.relative_to(package).as_posix()
        for p in package.rglob("*")
        if p.is_file()
        and p.name != "CHECKSUM_MANIFEST.sha256"
        and "__pycache__" not in p.parts
        and p.suffix != ".pyc"
    )
    if sorted(checksum_entries) != expected_checksum_paths:
        raise ValidationError("Checksum manifest path mismatch")
    for rel, digest in checksum_entries.items():
        if sha(package / rel) != digest:
            raise ValidationError(f"Checksum manifest digest mismatch: {rel}")
    if enforce_git_paths:
        proc = subprocess.run(["git", "diff", "--name-only", f"{START_HEAD}..HEAD"], cwd=repo, text=True, capture_output=True, check=False)
        changed = [line for line in proc.stdout.splitlines() if line]
        if not changed:
            proc = subprocess.run(["git", "diff", "--name-only", "--"], cwd=repo, text=True, capture_output=True, check=False)
            changed = [line for line in proc.stdout.splitlines() if line]
            untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", PACKAGE_REL.as_posix()], cwd=repo, text=True, capture_output=True, check=False).stdout.splitlines()
            changed += [line for line in untracked if line]
        outside = [path for path in changed if not path.startswith(PACKAGE_REL.as_posix() + "/")]
        if outside:
            raise ValidationError(f"Changed paths outside authorized accession package: {outside}")
    return {"status": "PASS", "document_sha256": doc_sha, "document_byte_length": doc_len, "source_sha256": sha(package / "SOURCE_PAYLOAD_ORIGINAL.md"), "source_byte_length": len((package / "SOURCE_PAYLOAD_ORIGINAL.md").read_bytes())}

def main() -> int:
    try:
        result = validate()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
