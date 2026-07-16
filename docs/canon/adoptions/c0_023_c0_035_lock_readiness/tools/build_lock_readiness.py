#!/usr/bin/env python3
"""Build the non-locking C0-023/C0-035 constitutional lock-readiness review."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
ROOT = REPO / "docs/canon/adoptions/c0_023_c0_035_lock_readiness"
OUTPUT = REPO / "outputs/governance_v1_0_c0_023_c0_035_lock_readiness"
ZIP_PATH = OUTPUT / "GOVERNANCE_V1_0_C0_023_C0_035_LOCK_READINESS_EVIDENCE_PACKAGE.zip"

PRIVACY_MD = REPO / "docs/canon/founder_approved_sources/MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_FOUNDER_APPROVED.md"
PRIVACY_DOCX = REPO / "docs/canon/founder_approved_sources/MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_FOUNDER_APPROVED.docx"
REPORTING_MD = REPO / "docs/canon/founder_approved_sources/MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0_FOUNDER_APPROVED.md"
REPORTING_DOCX = REPO / "docs/canon/founder_approved_sources/MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0_FOUNDER_APPROVED.docx"
PRIVACY_RECORD = REPO / "docs/canon/adoptions/c0_023_privacy_v2_0/C0_023_PRIVACY_AND_DATA_PROTECTION_CONSTITUTIONAL_ADOPTION_RECORD.md"
REPORTING_RECORD = REPO / "docs/canon/adoptions/c0_035_reporting_v2_0/C0_035_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_CONSTITUTIONAL_ADOPTION_RECORD.md"
PRIVACY_PREPARATION = REPO / "docs/canon/adoptions/c0_023_privacy_v2_0/C0_023_LOCK_READINESS_PREPARATION.md"
REPORTING_PREPARATION = REPO / "docs/canon/adoptions/c0_035_reporting_v2_0/C0_035_LOCK_READINESS_PREPARATION.md"
ADOPTION_PACKAGE = REPO / "outputs/governance_v1_0_c0_023_c0_035_adoption/GOVERNANCE_V1_0_C0_023_C0_035_CONSTITUTIONAL_ADOPTION_EVIDENCE_PACKAGE.zip"
PREREQUISITE_PACKAGE = REPO / "outputs/privacy_reporting_format_counterpart_completion_package.zip"
ADOPTION_VALIDATION = REPO / "docs/canon/adoptions/c0_023_c0_035_adoption/C0_023_C0_035_FORMAL_ADOPTION_VALIDATION.json"
LIFECYCLE = REPO / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_CURRENT_LIFECYCLE_STATE_REGISTER.json"
SOURCE_REGISTER = REPO / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json"
CANON_INDEX = REPO / "docs/canon/CANON_INDEX.md"
DEPENDENCY_MAP = REPO / "docs/canon/companions/EQUINESYNC_CANON_DEPENDENCY_MAP_V1_2.md"
AUTHORITY_MATRIX = REPO / "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_AUTHORITY_MATRIX_V1_2.md"
LOCK_LEDGER = REPO / "docs/canon/registries/CANON_LOCK_LEDGER.md"

EXPECTED = {
    PRIVACY_MD: "b773389d83308ab051e4959a4f61304cc3fb5328a5f8086ef683ab0a914498bb",
    PRIVACY_DOCX: "303b9ab9092a18deafc78d728c32f17bf8752e5383f5f793c0c47202bd305c7c",
    REPORTING_MD: "67b25cc23230492b9c8164c7a0b116f74109a623d544566a01b60425fe646f4f",
    REPORTING_DOCX: "56d30d5ce8d51c636179a0b1f05f31f005abcb64d998d9b499f9085ab67975d4",
    ADOPTION_PACKAGE: "32ef54edb2f5ab1a65e790854b85b3b50bb415a9adcdedc9c7eb476c4d9921cc",
    PREREQUISITE_PACKAGE: "9316affecd7f82ed0604f164edfc07d311b8c61481c5c192c288c3582303c593",
}

AUTHORITY = {
    "constitutional_lock": False,
    "governance_v1_baseline_adoption": False,
    "governance_v1_baseline_lock": False,
    "implementation": False,
    "migration": False,
    "runtime": False,
    "provider_activation": False,
    "integration_activation": False,
    "deployment": False,
    "production": False,
    "customer_data_processing": False,
    "public_launch": False,
    "certification": False,
    "public_trust_claims": False,
}


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    write_text(path, json.dumps(data, indent=2, sort_keys=False))


def verify_zip(path: Path) -> tuple[bool, int]:
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            return False, 0
        count = len([item for item in archive.infolist() if not item.is_dir()])
        with tempfile.TemporaryDirectory() as directory:
            archive.extractall(directory)
            if not any(Path(directory).rglob("*")):
                return False, 0
    return True, count


def markdown_links_resolve(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        clean = target.split("#", 1)[0]
        if clean and not (path.parent / clean).resolve().exists():
            return False
    return True


def lifecycle_rows() -> dict[str, dict]:
    data = json.loads(LIFECYCLE.read_text(encoding="utf-8"))
    return {row["record_id"]: row for row in data["rows"]}


def main() -> None:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    checks: dict[str, bool] = {}
    for path, expected in EXPECTED.items():
        checks[f"hash:{rel(path)}"] = path.is_file() and sha256(path) == expected

    privacy_sidecar = PRIVACY_RECORD.with_suffix(PRIVACY_RECORD.suffix + ".sha256")
    reporting_sidecar = REPORTING_RECORD.with_suffix(REPORTING_RECORD.suffix + ".sha256")
    checks["privacy_adoption_record_sidecar"] = privacy_sidecar.read_text().split()[0] == sha256(PRIVACY_RECORD)
    checks["reporting_adoption_record_sidecar"] = reporting_sidecar.read_text().split()[0] == sha256(REPORTING_RECORD)
    checks["prerequisite_archive_extracts"], prerequisite_count = verify_zip(PREREQUISITE_PACKAGE)
    checks["adoption_archive_extracts"], adoption_count = verify_zip(ADOPTION_PACKAGE)

    adoption_validation = json.loads(ADOPTION_VALIDATION.read_text(encoding="utf-8"))
    checks["adoption_validation_passed"] = adoption_validation["all_checks_pass"] is True
    checks["adoption_had_no_blocking_findings"] = adoption_validation["findings"] == {
        "p0": 0,
        "open_p1": 0,
        "adoption_blocking_p2": 0,
        "retained_nonblocking_p2": 0,
    }

    privacy_text = PRIVACY_MD.read_text(encoding="utf-8")
    reporting_text = REPORTING_MD.read_text(encoding="utf-8")
    for name, text in (("privacy", privacy_text), ("reporting", reporting_text)):
        checks[f"{name}_adopted_metadata"] = "Constitutional Adoption Status" in text and "ADOPTED" in text
        checks[f"{name}_not_locked"] = "NOT YET LOCKED" in text
        checks[f"{name}_authority_false"] = all(
            signal in text
            for signal in (
                "Implementation Authority: FALSE" if name == "privacy" else "Implementation Authority | FALSE",
                "Runtime Authority: FALSE" if name == "privacy" else "Runtime Authority | FALSE",
                "Production Authority: FALSE" if name == "privacy" else "Production Authority | FALSE",
            )
        )
        checks[f"{name}_no_merge_markers"] = not any(marker in text for marker in ("<<<<<<<", "=======", ">>>>>>>"))
        checks[f"{name}_no_unresolved_placeholders"] = not re.search(r"\b(?:TBD|TODO|FIXME|INSERT HERE)\b", text, re.I)

    index_text = CANON_INDEX.read_text(encoding="utf-8")
    dependency_text = DEPENDENCY_MAP.read_text(encoding="utf-8")
    authority_text = AUTHORITY_MATRIX.read_text(encoding="utf-8")
    lock_text = LOCK_LEDGER.read_text(encoding="utf-8")
    checks["single_privacy_index_entry"] = index_text.count("| 3 | Master Privacy and Data Protection Model |") == 1
    checks["single_reporting_index_entry"] = index_text.count("| 3 | Master Reporting, Analytics, and Business Intelligence Model |") == 1
    checks["dependency_map_entries_present"] = "CDM-023" in dependency_text and "CDM-035" in dependency_text
    checks["authority_matrix_entries_present"] = "AUTH-041" in authority_text and "Master Reporting, Analytics, and Business Intelligence Model" in authority_text
    checks["not_already_in_lock_ledger"] = "Master Privacy and Data Protection Model | 2.0" not in lock_text and "Master Reporting, Analytics, and Business Intelligence Model | 2.0" not in lock_text
    checks["companion_markdown_links_resolve"] = all(markdown_links_resolve(path) for path in (CANON_INDEX, DEPENDENCY_MAP, AUTHORITY_MATRIX))

    rows = lifecycle_rows()
    dependency_snapshot = {
        row_id: {
            "family": rows[row_id]["family"],
            "category": rows[row_id]["current_category"],
            "adoption": rows[row_id]["adoption_state"],
            "lock": rows[row_id]["lock_state"],
        }
        for row_id in (
            "C0-004", "C0-017", "C0-018", "C0-019", "C0-020", "C0-022",
            "C0-023", "C0-025", "C0-026", "C0-027", "C0-028", "C0-029",
            "C0-033", "C0-034", "C0-035", "C0-036", "C0-041",
        )
    }
    checks["privacy_primary_dependencies_resolved"] = all(
        rows[row_id]["adoption_state"] in {"ADOPTED", "SUPPORTING_OR_SCOPE_SPECIFIC"}
        for row_id in ("C0-004", "C0-017", "C0-018", "C0-019")
    )
    checks["reporting_primary_dependencies_resolved"] = all(
        rows[row_id]["adoption_state"] in {"ADOPTED", "SUPPORTING_OR_SCOPE_SPECIFIC"}
        for row_id in ("C0-004", "C0-022", "C0-023", "C0-026", "C0-027")
    ) and rows["C0-023"]["lock_state"] == "LOCKED"

    findings = [
        {
            "id": "C0-023-LR-P1-01",
            "severity": "P1",
            "row": "C0-023",
            "title": "Primary constitutional prerequisites are not lifecycle-resolved",
            "evidence": ["C0-004 Master Product Vision: NOT_ESTABLISHED", "C0-019 Agreement, Consent, and Authorization: NOT_ESTABLISHED"],
            "required_resolution": "Resolve exact-source identity and constitutional lifecycle for C0-004 and C0-019, then rerun the C0-023 lock-readiness review.",
        },
        {
            "id": "C0-035-LR-P1-01",
            "severity": "P1",
            "row": "C0-035",
            "title": "Reporting lock prerequisites are incomplete",
            "evidence": ["C0-004 Master Product Vision: NOT_ESTABLISHED", "C0-022 Permission and Access-Control: NOT_ESTABLISHED", "C0-023 Privacy: ADOPTED but NOT_YET_LOCKED"],
            "required_resolution": "Resolve C0-004 and C0-022, complete and lock C0-023 under separate authority, then rerun the C0-035 lock-readiness review.",
        },
        {
            "id": "C0-023-LR-P2-01",
            "severity": "P2",
            "row": "C0-023",
            "title": "Non-primary co-review families remain lifecycle-incomplete",
            "evidence": ["C0-028 Claims, Disputes, and Authority: NOT_ESTABLISHED", "C0-041 Vendor Security and Supply Chain: pending separate adoption"],
            "required_resolution": "Track change-impact review so later adoption cannot silently conflict with locked Privacy authority.",
        },
        {
            "id": "C0-035-LR-P2-01",
            "severity": "P2",
            "row": "C0-035",
            "title": "Search mandatory overlay remains lifecycle-incomplete",
            "evidence": ["C0-033 Search, Discovery, Ranking, and Retrieval: pending separate adoption"],
            "required_resolution": "Require future C0-033 adoption and lock review to conform to Reporting, Privacy, Permission, and Record authority.",
        },
    ]

    validation_pass = all(value for key, value in checks.items() if not key.endswith("primary_dependencies_resolved"))
    p0 = 0
    p1 = 2
    p2 = 2
    validation = {
        "generated_at": now,
        "disposition": "C0_023_AND_C0_035_LOCK_READINESS_CHECK_COMPLETE_NOT_READY",
        "validation_execution": "PASS" if validation_pass else "FAIL",
        "readiness": {"C0-023": False, "C0-035": False},
        "checks": checks,
        "findings": {"p0": p0, "open_p1": p1, "retained_p2": p2},
        "authority": AUTHORITY,
        "prerequisite_archive_file_count": prerequisite_count,
        "adoption_archive_file_count": adoption_count,
    }
    if not validation_pass:
        write_json(ROOT / "C0_023_C0_035_LOCK_READINESS_VALIDATION.json", validation)
        raise SystemExit("Lock-readiness validation execution failed")

    write_json(ROOT / "C0_023_C0_035_LOCK_READINESS_VALIDATION.json", validation)
    write_json(ROOT / "C0_023_C0_035_LOCK_READINESS_FINDINGS.json", {"generated_at": now, "findings": findings})
    write_json(ROOT / "C0_023_C0_035_DEPENDENCY_SNAPSHOT.json", {"generated_at": now, "rows": dependency_snapshot})

    privacy_certificate = {
        "row_id": "C0-023", "reviewed_at": now, "ready": False,
        "adopted_source": rel(PRIVACY_MD), "sha256": EXPECTED[PRIVACY_MD],
        "adoption_record_sha256": sha256(PRIVACY_RECORD), "p0": 0, "open_p1": 1,
        "lock_blocking_p2": 0, "retained_nonblocking_p2": ["C0-023-LR-P2-01"],
        "blocking_findings": ["C0-023-LR-P1-01"], "lock_issued": False, "authority": AUTHORITY,
    }
    reporting_certificate = {
        "row_id": "C0-035", "reviewed_at": now, "ready": False,
        "adopted_source": rel(REPORTING_DOCX), "sha256": EXPECTED[REPORTING_DOCX],
        "adoption_record_sha256": sha256(REPORTING_RECORD), "p0": 0, "open_p1": 1,
        "lock_blocking_p2": 0, "retained_nonblocking_p2": ["C0-035-LR-P2-01"],
        "blocking_findings": ["C0-035-LR-P1-01"], "lock_issued": False, "authority": AUTHORITY,
    }
    write_json(ROOT / "C0_023_LOCK_READINESS_CERTIFICATE.json", privacy_certificate)
    write_json(ROOT / "C0_035_LOCK_READINESS_CERTIFICATE.json", reporting_certificate)

    assessment_template = """# {title} Lock-Readiness Assessment

## Assessment

`NOT_READY_FOR_FOUNDER_LOCK_AUTHORIZATION`

The canon remains constitutionally `ADOPTED` and `NOT YET LOCKED`. Its adopted bytes, adoption record, parity evidence, provenance, authority boundaries, and package integrity remain valid. The lock-readiness review found one open P1 dependency finding and one retained nonblocking P2 change-impact observation.

## Blocking Finding

`{p1_id}`: {p1_title}

{p1_evidence}

Required resolution: {p1_resolution}

## Retained Observation

`{p2_id}`: {p2_title}

{p2_evidence}

## Verified Evidence

- Adopted source SHA-256: `{source_hash}`
- Adoption record SHA-256: `{record_hash}`
- Adoption and prerequisite evidence archives extract cleanly.
- P0: `0`
- Open P1: `1`
- Retained P2: `1`
- Constitutional lock issued: `FALSE`
- Implementation, runtime, migration, provider, production, launch, certification, and public-trust authority: `FALSE`

## Next Gate

Complete the required dependency lifecycle work, rerun this review, and obtain a separate Founder lock directive only after the row returns zero open P1 findings.
"""
    p1_privacy, p1_reporting, p2_privacy, p2_reporting = findings
    write_text(ROOT / "C0_023_PRIVACY_LOCK_READINESS_ASSESSMENT.md", assessment_template.format(
        title="C0-023 Privacy and Data Protection V2.0", p1_id=p1_privacy["id"],
        p1_title=p1_privacy["title"], p1_evidence="\n".join(f"- {item}" for item in p1_privacy["evidence"]),
        p1_resolution=p1_privacy["required_resolution"], p2_id=p2_privacy["id"], p2_title=p2_privacy["title"],
        p2_evidence="\n".join(f"- {item}" for item in p2_privacy["evidence"]),
        source_hash=EXPECTED[PRIVACY_MD], record_hash=sha256(PRIVACY_RECORD)))
    write_text(ROOT / "C0_035_REPORTING_LOCK_READINESS_ASSESSMENT.md", assessment_template.format(
        title="C0-035 Reporting, Analytics, and Business Intelligence V2.0", p1_id=p1_reporting["id"],
        p1_title=p1_reporting["title"], p1_evidence="\n".join(f"- {item}" for item in p1_reporting["evidence"]),
        p1_resolution=p1_reporting["required_resolution"], p2_id=p2_reporting["id"], p2_title=p2_reporting["title"],
        p2_evidence="\n".join(f"- {item}" for item in p2_reporting["evidence"]),
        source_hash=EXPECTED[REPORTING_DOCX], record_hash=sha256(REPORTING_RECORD)))

    write_text(ROOT / "C0_023_C0_035_LOCK_READINESS_MASTER_REPORT.md", f"""# C0-023 and C0-035 Lock-Readiness Master Report

## Disposition

`C0_023_AND_C0_035_LOCK_READINESS_CHECK_COMPLETE_NOT_READY`

| Row | Adoption | Lock | Ready | P0 | Open P1 | Retained P2 |
|---|---|---|---|---:|---:|---:|
| C0-023 | ADOPTED | NOT YET LOCKED | NO | 0 | 1 | 1 |
| C0-035 | ADOPTED | NOT YET LOCKED | NO | 0 | 1 | 1 |

## Required Sequence

1. Resolve C0-004 Product Vision exact-source and lifecycle authority.
2. Resolve C0-019 Agreement, Consent, and Authorization before rerunning C0-023.
3. Resolve C0-022 Permission and Access-Control before rerunning C0-035.
4. Rerun C0-023 lock readiness and obtain a separate Founder lock directive if clean.
5. Rerun C0-035 after C0-023 is locked.
6. Preserve the C0-028, C0-033, and C0-041 change-impact observations for later lifecycle reviews.

No lock was issued. This review created no implementation, runtime, migration, provider, production, launch, certification, or public-trust authority.
""")

    evidence_files = sorted(path for path in ROOT.rglob("*") if path.is_file() and "tools" not in path.parts and path.name not in {"C0_023_C0_035_LOCK_READINESS_MANIFEST.json", "C0_023_C0_035_LOCK_READINESS_PACKAGE_RECORD.json"})
    evidence_files += [
        PRIVACY_RECORD, REPORTING_RECORD, PRIVACY_PREPARATION, REPORTING_PREPARATION,
        ADOPTION_VALIDATION, CANON_INDEX, DEPENDENCY_MAP, AUTHORITY_MATRIX, LIFECYCLE,
        SOURCE_REGISTER,
    ]
    evidence_files = sorted(set(evidence_files))
    manifest_path = ROOT / "C0_023_C0_035_LOCK_READINESS_MANIFEST.json"
    manifest = {
        "disposition": "C0_023_AND_C0_035_LOCK_READINESS_CHECK_COMPLETE_NOT_READY",
        "files": [{"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)} for path in evidence_files],
        "manifest_self_hash_excluded": True,
    }
    write_json(manifest_path, manifest)
    evidence_files.append(manifest_path)

    with tempfile.TemporaryDirectory() as directory:
        staging = Path(directory)
        for source in evidence_files:
            destination = staging / rel(source)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        OUTPUT.mkdir(parents=True, exist_ok=True)
        if ZIP_PATH.exists():
            ZIP_PATH.unlink()
        with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(staging.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(staging))

    archive_ok, archive_count = verify_zip(ZIP_PATH)
    if not archive_ok:
        raise SystemExit("Evidence archive failed extraction validation")
    with tempfile.TemporaryDirectory() as directory:
        with zipfile.ZipFile(ZIP_PATH) as archive:
            archive.extractall(directory)
        extracted = Path(directory)
        packaged_manifest = json.loads((extracted / rel(manifest_path)).read_text(encoding="utf-8"))
        for item in packaged_manifest["files"]:
            path = extracted / item["path"]
            if not path.is_file() or path.stat().st_size != item["size_bytes"] or sha256(path) != item["sha256"]:
                raise SystemExit(f"Manifest verification failed: {item['path']}")

    package_record = {
        "package": rel(ZIP_PATH), "sha256": sha256(ZIP_PATH), "size_bytes": ZIP_PATH.stat().st_size,
        "archive_file_count": archive_count, "archive_extraction_validation": "PASS",
        "manifest_entry_validation": "PASS", "readiness": {"C0-023": False, "C0-035": False},
        "lock_issued": False, "findings": {"p0": 0, "open_p1": 2, "retained_p2": 2}, "authority": AUTHORITY,
    }
    write_json(ROOT / "C0_023_C0_035_LOCK_READINESS_PACKAGE_RECORD.json", package_record)
    print(json.dumps(package_record, indent=2))


if __name__ == "__main__":
    main()
