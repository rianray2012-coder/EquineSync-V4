#!/usr/bin/env python3
"""Round 3 remediation — deterministic transforms for F-01, F-04, F-05, F-06.

Run from the package root AFTER generate_audit_templates.py (F-02) and after the
prose corrections to Document 04 and Document 10 have been applied.

  python3 VALIDATION/apply_round3_remediation.py --package-root .

Every transform is idempotent: running twice produces byte-identical output.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

MANIFEST_FILENAMES = {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256"}
INTEGRITY_ROOT = "00_PROGRAM_CONTROL/ROUND_3_INTEGRITY_ROOT.json"
MOM = "MANIFEST_OF_MANIFESTS.sha256"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- F-01 -------------------------------------------------------------------

def f01_retype_traceability_register(package):
    """Rows are keyword-scan artifacts, not validated requirements.

    - requirement_type            -> SOURCE_TEXT_CANDIDATE_NOT_VALIDATED for every row
    - original_requirement_type_claim  preserves the Round 2 value
    - iso29148_characteristic_check    NOT_PERFORMED
    - requirement_status               CANDIDATE_PENDING_29148_VALIDATION
    - verification_method         -> renamed discovery_method (value unchanged)
    - verification_method (new)        NOT_PERFORMED
    """
    path = package / "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames)
        rows = list(reader)
    if "original_requirement_type_claim" in fields:
        return 0  # already applied

    out_fields = []
    for name in fields:
        if name == "requirement_type":
            out_fields += ["requirement_type", "original_requirement_type_claim",
                           "iso29148_characteristic_check", "requirement_status"]
        elif name == "verification_method":
            out_fields += ["discovery_method", "verification_method"]
        else:
            out_fields.append(name)

    for row in rows:
        row["original_requirement_type_claim"] = row["requirement_type"]
        row["requirement_type"] = "SOURCE_TEXT_CANDIDATE_NOT_VALIDATED"
        row["iso29148_characteristic_check"] = "NOT_PERFORMED"
        row["requirement_status"] = "CANDIDATE_PENDING_29148_VALIDATION"
        row["discovery_method"] = row["verification_method"]
        row["verification_method"] = "NOT_PERFORMED"

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=out_fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


# --- F-04 -------------------------------------------------------------------

def f04_declare_rule_implementation_status(package, enforced_rule_ids):
    """Every invalid-state rule must declare whether it is actually enforced."""
    path = package / "04_AUTHORITY_LIFECYCLE_REGISTER/INVALID_STATE_RULES.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames)
        rows = list(reader)
    if "implementation_status" in fields:
        return 0
    fields = fields + ["implementation_status", "validator_function"]
    for row in rows:
        rid = row["rule_id"]
        if rid in enforced_rule_ids:
            row["implementation_status"] = "ENFORCED"
            row["validator_function"] = "check_lifecycle_rules/RULE_IMPLEMENTATIONS"
        else:
            row["implementation_status"] = "DOCUMENTED_NOT_ENFORCED"
            row["validator_function"] = "NONE"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


# --- F-06 -------------------------------------------------------------------

def is_integrity_control(package, path):
    """Integrity controls are authenticated by the layer above them, never by
    PACKAGE_MANIFEST.json, so they are excluded from the content manifest.

    Layering:  content files -> PACKAGE_MANIFEST.json / CHECKSUMS.sha256
               those manifests -> MANIFEST_OF_MANIFESTS.sha256
               that file -> ROUND_3_INTEGRITY_ROOT.json  (externally attested)
    """
    rel = str(path.relative_to(package))
    if "__pycache__" in path.parts or path.suffix == ".pyc":
        return True
    return path.name in MANIFEST_FILENAMES or rel in {MOM, INTEGRITY_ROOT}


def f06_rebuild_manifests(package):
    """Rebuild every per-directory and root manifest and checksum file so the
    recorded evidence matches the shipped bytes."""
    content_files = sorted(
        p for p in package.rglob("*")
        if p.is_file() and not is_integrity_control(package, p)
    )

    directories = sorted({p.parent for p in content_files if p.parent != package})
    for directory in directories:
        files = sorted(f for f in directory.iterdir() if f.is_file() and not is_integrity_control(package, f))
        entries = [{"byte_length": f.stat().st_size, "path": f.name, "sha256": sha(f)} for f in files]
        (directory / "PACKAGE_MANIFEST.json").write_text(
            json.dumps({"directory": directory.name, "files": entries}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        (directory / "CHECKSUMS.sha256").write_text(
            "".join(f"{e['sha256']}  {e['path']}\n" for e in entries), encoding="utf-8")

    entries = [{"byte_length": f.stat().st_size, "path": str(f.relative_to(package)), "sha256": sha(f)}
               for f in content_files]
    (package / "PACKAGE_MANIFEST.json").write_text(
        json.dumps({"files": entries, "package": package.name}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    (package / "CHECKSUMS.sha256").write_text(
        "".join(f"{e['sha256']}  {e['path']}\n" for e in entries), encoding="utf-8")
    return len(entries)


def f06_replace_circular_validation_reports(package, validator_path):
    """A validation report cannot be stored inside the package it authenticates.

    The Round 2 reports recorded files=130 against a package shipping 132 files,
    and recorded the base branch SHA as the validated commit. Both are artefacts
    of the circularity: the report is written, then the package changes, and the
    report is never refreshed. Round 3 removes the frozen reports and ships a
    reproduction record instead, so the reader regenerates the evidence.
    """
    results_dir = package / "VALIDATION_RESULTS"
    removed = []
    for name in ("REPOSITORY_MODE_VALIDATION_REPORT.json",
                 "STANDALONE_EXTRACTED_PACKAGE_VALIDATION_REPORT.json"):
        target = results_dir / name
        if target.exists():
            target.unlink()
            removed.append(name)

    import subprocess
    self_test = json.loads(subprocess.run(
        ["python3", str(validator_path), "--self-test"],
        capture_output=True, text=True, check=True).stdout)

    rel_validator = validator_path.relative_to(package)
    (results_dir / "VALIDATION_REPRODUCTION_RECORD.json").write_text(json.dumps({
        "record_type": "VALIDATION_REPRODUCTION_RECORD",
        "why_no_stored_report": (
            "A validation report stored inside the package it validates cannot be accurate, "
            "because writing the report changes the package the report describes. The Round 2 "
            "reports recorded files=130 for a package shipping 132 files and recorded the base "
            "branch commit rather than the reviewed commit. Both frozen reports are withdrawn."
        ),
        "validator_path": str(rel_validator),
        "validator_sha256": sha(validator_path),
        "reproduction_commands": [
            f"python3 {rel_validator} --self-test",
            f"python3 {rel_validator} --package-root . --expected-head <REVIEWED_COMMIT_SHA>",
        ],
        "self_test_status": self_test["self_test"],
        "self_test_cases": [c["case"] for c in self_test["cases"]],
        "self_test_note": (
            "The self-test exercises the validator against synthetic defective inputs and does "
            "not read this package, so it is safe to record here without circularity."
        ),
        "reviewed_commit_expected": "a1a1ff5cf056e7e78c99c4038fb8afcb95aebab7",
        "reviewed_commit_note": (
            "Supply this value to --expected-head. The validator FAILs if the working tree "
            "head does not match, so the reviewed commit can no longer drift from the record."
        ),
        "authority_boundary": (
            "NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; "
            "MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; "
            "UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED"
        ),
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return removed


# --- F-05 -------------------------------------------------------------------

def f05_build_manifest_of_manifests(package):
    """Authenticate the integrity controls themselves, then publish a single
    integrity root that is the only value requiring external attestation."""
    manifests = sorted(
        p for p in package.rglob("*") if p.is_file() and p.name in MANIFEST_FILENAMES
    )
    lines = [
        "# MANIFEST_OF_MANIFESTS.sha256",
        "# Round 3 remediation F-05: the integrity controls must themselves be authenticated.",
        "# Covers every PACKAGE_MANIFEST.json and CHECKSUMS.sha256 in this package.",
        "# This file cannot authenticate itself. Its own SHA-256 is published in",
        f"# {INTEGRITY_ROOT} and is the single value requiring external attestation.",
    ]
    lines += [f"{sha(p)}  {p.relative_to(package)}" for p in manifests]
    mom_path = package / MOM
    mom_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    root_path = package / INTEGRITY_ROOT
    root_path.write_text(json.dumps({
        "record_type": "ROUND_3_INTEGRITY_ROOT",
        "manifest_of_manifests_path": MOM,
        "manifest_of_manifests_sha256": sha(mom_path),
        "manifest_of_manifests_byte_length": mom_path.stat().st_size,
        "manifest_files_covered": len(manifests),
        "attestation_note": (
            "This value is the single root of trust for the package. It is not self-authenticating. "
            "External attestation of this value is required before the integrity chain is complete."
        ),
        "external_attestation_state": "NOT_ATTESTED",
        "authority_boundary": (
            "NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; "
            "MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; "
            "UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED"
        ),
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return len(manifests)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", default=".")
    args = parser.parse_args()
    package = Path(args.package_root).resolve()

    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "validator", package / "VALIDATION/validate_tier1_documents_03_10_rr2.py")
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    enforced = set(validator.RULE_IMPLEMENTATIONS)

    # Strict ordering: content -> manifests -> manifest of manifests -> integrity root.
    print(f"F-01 retyped rows                 : {f01_retype_traceability_register(package)}")
    print(f"F-04 rules given implementation   : {f04_declare_rule_implementation_status(package, enforced)}")
    print(f"F-06 circular reports withdrawn   : {f06_replace_circular_validation_reports(package, package / 'VALIDATION/validate_tier1_documents_03_10_rr2.py')}")
    print(f"F-06 content files re-manifested  : {f06_rebuild_manifests(package)}")
    print(f"F-05 manifest files authenticated : {f05_build_manifest_of_manifests(package)}")
    print(f"F-05 integrity root               : {json.loads((package / INTEGRITY_ROOT).read_text())['manifest_of_manifests_sha256']}")


if __name__ == "__main__":
    raise SystemExit(main())
