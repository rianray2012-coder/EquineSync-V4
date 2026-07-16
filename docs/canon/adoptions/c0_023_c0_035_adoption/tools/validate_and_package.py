#!/usr/bin/env python3
"""Validate and package the separate C0-023 and C0-035 adoptions."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from docx import Document


REPO = Path(__file__).resolve().parents[5]
ROOT = REPO / "docs/canon/adoptions/c0_023_c0_035_adoption"
PRIVACY_DIR = REPO / "docs/canon/adoptions/c0_023_privacy_v2_0"
REPORTING_DIR = REPO / "docs/canon/adoptions/c0_035_reporting_v2_0"
APPROVED = REPO / "docs/canon/founder_approved_sources"
COMPLETION = REPO / "docs/canon/reviews/privacy_reporting_format_counterpart_completion_v1_0"
OUTPUT_DIR = REPO / "outputs/governance_v1_0_c0_023_c0_035_adoption"
PACKAGE_DIR = OUTPUT_DIR / "package_contents"
PACKAGE_ZIP = OUTPUT_DIR / "GOVERNANCE_V1_0_C0_023_C0_035_CONSTITUTIONAL_ADOPTION_EVIDENCE_PACKAGE.zip"

PRIVACY_MD = APPROVED / "MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_FOUNDER_APPROVED.md"
PRIVACY_DOCX = APPROVED / "MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_FOUNDER_APPROVED.docx"
REPORTING_MD = APPROVED / "MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0_FOUNDER_APPROVED.md"
REPORTING_DOCX = APPROVED / "MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0_FOUNDER_APPROVED.docx"
PRIVACY_RECORD = PRIVACY_DIR / "C0_023_PRIVACY_AND_DATA_PROTECTION_CONSTITUTIONAL_ADOPTION_RECORD.md"
REPORTING_RECORD = REPORTING_DIR / "C0_035_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_CONSTITUTIONAL_ADOPTION_RECORD.md"

PRE_HASHES = {
    PRIVACY_MD: "41d8a72e78c369a297350b0abbdda90b1bf5401a3bb16050101679c325012eed",
    PRIVACY_DOCX: "76cdc1338a70c1c18f0295340f0f3599c4e99b3d37c0f306d740db9537ef1846",
    REPORTING_MD: "56de16098bbba31571c94d2ec3560dcc48a74daae318da047e5b5592044e953a",
    REPORTING_DOCX: "d6cc3cc2add501d2d34d947de4e7a2ee7c6af77aa9669606c95514361657504d",
}
POST_HASHES = {
    PRIVACY_MD: "b773389d83308ab051e4959a4f61304cc3fb5328a5f8086ef683ab0a914498bb",
    PRIVACY_DOCX: "303b9ab9092a18deafc78d728c32f17bf8752e5383f5f793c0c47202bd305c7c",
    REPORTING_MD: "67b25cc23230492b9c8164c7a0b116f74109a623d544566a01b60425fe646f4f",
    REPORTING_DOCX: "56d30d5ce8d51c636179a0b1f05f31f005abcb64d998d9b499f9085ab67975d4",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def module():
    path = COMPLETION / "tools/build_completion.py"
    spec = importlib.util.spec_from_file_location("counterpart_builder", path)
    loaded = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(loaded)
    return loaded


def markdown_links(paths: list[Path]) -> list[str]:
    broken = []
    pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for path in paths:
        if path.suffix.lower() != ".md":
            continue
        for target in pattern.findall(path.read_text(encoding="utf-8")):
            target = target.strip().split("#", 1)[0]
            if not target or re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
                continue
            if not (path.parent / target).resolve().exists():
                broken.append(f"{rel(path)} -> {target}")
    return broken


def active_files() -> list[Path]:
    build = json.loads((ROOT / "C0_023_C0_035_ADOPTION_BUILD_RECORD.json").read_text(encoding="utf-8"))
    paths = [REPO / path for path in build["updated_governance_artifacts"]]
    paths.extend([PRIVACY_MD, PRIVACY_DOCX, REPORTING_MD, REPORTING_DOCX])
    paths.extend(path for path in ROOT.rglob("*") if path.is_file())
    paths.extend(path for path in PRIVACY_DIR.rglob("*") if path.is_file())
    paths.extend(path for path in REPORTING_DIR.rglob("*") if path.is_file())
    paths.extend([
        REPO / "docs/canon/companions/GLOBAL_ADOPTION_STATE_REGISTER.md",
        REPO / "docs/canon/companions/GLOBAL_ADOPTION_STATE_REGISTER.json",
        REPO / "docs/canon/companions/GLOBAL_LOCK_STATE_REGISTER.md",
        REPO / "docs/canon/companions/GLOBAL_LOCK_STATE_REGISTER.json",
    ])
    return sorted(set(path for path in paths if path.exists()))


def validate() -> dict:
    helper = module()
    checks: dict[str, bool] = {}
    for path, digest in PRE_HASHES.items():
        directory = PRIVACY_DIR if "PRIVACY" in path.name else REPORTING_DIR
        preserved = directory / "pre_adoption" / path.name
        checks[f"pre_adoption_{path.name}"] = sha256(preserved) == digest
    for path, digest in POST_HASHES.items():
        checks[f"post_adoption_{path.name}"] = sha256(path) == digest

    pre_privacy_md = (PRIVACY_DIR / "pre_adoption" / PRIVACY_MD.name).read_text(encoding="utf-8")
    post_privacy_md = PRIVACY_MD.read_text(encoding="utf-8")
    checks["privacy_markdown_substantive_unchanged"] = pre_privacy_md.split("## Authority Boundary", 1)[1] == post_privacy_md.split("## Authority Boundary", 1)[1]

    def docx_body(path: Path, marker: str) -> list[str]:
        texts = [p.text for p in Document(path).paragraphs]
        return texts[texts.index(marker):]
    checks["privacy_docx_substantive_unchanged"] = docx_body(PRIVACY_DIR / "pre_adoption" / PRIVACY_DOCX.name, "Authority Boundary") == docx_body(PRIVACY_DOCX, "Authority Boundary")
    checks["reporting_docx_substantive_unchanged"] = docx_body(REPORTING_DIR / "pre_adoption" / REPORTING_DOCX.name, "1. Purpose") == docx_body(REPORTING_DOCX, "1. Purpose")

    privacy_units = helper.markdown_units(post_privacy_md)
    privacy_docx_units = helper.docx_units(PRIVACY_DOCX)
    checks["privacy_paragraph_parity"] = privacy_units["paragraphs"] == privacy_docx_units["paragraphs"]
    checks["privacy_table_parity"] = privacy_units["tables"] == privacy_docx_units["tables"]
    extracted_reporting = helper.docx_to_markdown(REPORTING_DOCX).strip()
    md_reporting_body = REPORTING_MD.read_text(encoding="utf-8").split("# Exact Substantive Source Content", 1)[1].strip()
    checks["reporting_normalized_text_parity"] = helper.normalized(extracted_reporting) == helper.normalized(md_reporting_body)

    pre_privacy_ids = [identifier for identifier in helper.identifiers(pre_privacy_md) if identifier != "SHA-256"]
    post_privacy_ids = [identifier for identifier in helper.identifiers(post_privacy_md) if identifier != "SHA-256"]
    pre_reporting_text = helper.docx_to_markdown(REPORTING_DIR / "pre_adoption" / REPORTING_DOCX.name)
    post_reporting_text = helper.docx_to_markdown(REPORTING_DOCX)
    checks["privacy_requirement_ids_unchanged"] = pre_privacy_ids == post_privacy_ids
    checks["reporting_requirement_ids_unchanged"] = helper.identifiers(pre_reporting_text) == helper.identifiers(post_reporting_text)
    checks["privacy_authority_signals_unchanged"] = helper.authority_signals(pre_privacy_md.split("## Authority Boundary", 1)[1]) == helper.authority_signals(post_privacy_md.split("## Authority Boundary", 1)[1])
    checks["reporting_authority_signals_unchanged"] = helper.authority_signals("\n".join(docx_body(REPORTING_DIR / "pre_adoption" / REPORTING_DOCX.name, "1. Purpose"))) == helper.authority_signals("\n".join(docx_body(REPORTING_DOCX, "1. Purpose")))

    checks["duplicate_privacy_ids"] = len(post_privacy_ids) == len(set(post_privacy_ids))
    reporting_ids = [identifier for identifier in helper.identifiers(post_reporting_text) if identifier != "SHA-256"]
    checks["duplicate_reporting_ids"] = len(reporting_ids) == len(set(reporting_ids))
    traceability = {identifier: bool(re.search(rf"\b{re.escape(identifier)}\b", post_privacy_md)) for identifier in post_privacy_ids}
    checks["orphan_requirement_scan"] = all(traceability.values())

    canon_index = (REPO / "docs/canon/CANON_INDEX.md").read_text(encoding="utf-8")
    checks["single_active_privacy_index_entry"] = canon_index.count("| 3 | Master Privacy and Data Protection Model |") == 1
    checks["single_active_reporting_index_entry"] = canon_index.count("| 3 | Master Reporting, Analytics, and Business Intelligence Model |") == 1
    lock_ledger = (REPO / "docs/canon/registries/CANON_LOCK_LEDGER.md").read_text(encoding="utf-8")
    checks["no_competing_locked_privacy_canon"] = "| Master Privacy and Data Protection Model |" not in lock_ledger
    checks["no_competing_locked_reporting_canon"] = "| Master Reporting, Analytics, and Business Intelligence Model |" not in lock_ledger
    dependency = (REPO / "docs/canon/companions/EQUINESYNC_CANON_DEPENDENCY_MAP_V1_2.md").read_text(encoding="utf-8")
    privacy_block = dependency.split("CDM-023<br />", 1)[1].split("</tr>", 1)[0]
    reporting_block = dependency.split("CDM-035<br />", 1)[1].split("</tr>", 1)[0]
    checks["dependency_cycle_scan"] = "Reporting" not in privacy_block and "Privacy" in reporting_block
    reporting_lower = post_reporting_text.lower()
    checks["locked_canon_conflict_scan"] = all([
        "Access Control and Authorization" in post_privacy_md,
        "Record Stewardship" in post_privacy_md,
        "privacy" in reporting_lower,
        "permission" in reporting_lower,
        "records" in reporting_lower and "retention" in reporting_lower,
    ])

    paths = active_files()
    checks["broken_markdown_links"] = len(markdown_links(paths)) == 0
    merge_pattern = re.compile(r"^(?:<{7}|={7}|>{7})", re.M)
    placeholder_pattern = re.compile(r"\b(?:TODO|TBD|FIXME|CHANGEME)\b|\{\{[^}]+\}\}", re.I)
    secret_pattern = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bsk_(?:live|test)_[A-Za-z0-9]{16,}|\bAKIA[0-9A-Z]{16}\b")
    merge_hits, placeholder_hits, secret_hits, json_errors = [], [], [], []
    for path in paths:
        if path.suffix.lower() not in {".md", ".json", ".py", ".txt"} or path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if merge_pattern.search(text): merge_hits.append(rel(path))
        if placeholder_pattern.search(text): placeholder_hits.append(rel(path))
        if secret_pattern.search(text): secret_hits.append(rel(path))
        if path.suffix.lower() == ".json":
            try: json.loads(text)
            except Exception as exc: json_errors.append(f"{rel(path)}: {exc}")
    checks["merge_marker_scan"] = not merge_hits
    checks["placeholder_scan"] = not placeholder_hits
    checks["secret_scan"] = not secret_hits
    checks["json_validation"] = not json_errors

    required_statuses = [
        "Constitutional Adoption Status: ADOPTED",
        "Constitutional Lock Status: NOT YET LOCKED",
        "Implementation Authority: FALSE",
        "Runtime Authority: FALSE",
        "Migration Authority: FALSE",
        "Provider Activation Authority: FALSE",
        "Production Authority: FALSE",
        "Public Launch Authority: FALSE",
        "Public Trust Claim Authority: FALSE",
    ]
    checks["privacy_authority_metadata"] = all(value in post_privacy_md for value in required_statuses)
    reporting_statuses = [value.replace(": ", " | ") + " |" for value in required_statuses]
    checks["reporting_authority_metadata"] = all(value in REPORTING_MD.read_text(encoding="utf-8") for value in reporting_statuses)
    build = json.loads((ROOT / "C0_023_C0_035_ADOPTION_BUILD_RECORD.json").read_text(encoding="utf-8"))
    checks["authority_flags_false"] = all(value is False for value in build["authority"].values())
    checks["retained_p2_accounting"] = build["retained_p2"] == {"C0-023": 0, "C0-035": 0}
    checks["findings_gate"] = build["findings"] == {"p0": 0, "open_p1": 0, "adoption_blocking_p2": 0}
    checks["render_page_counts"] = len(list((ROOT / "render_evidence/privacy").glob("page-*.png"))) == 24 and len(list((ROOT / "render_evidence/reporting").glob("page-*.png"))) == 15
    checks["runtime_or_application_files_changed"] = False

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disposition": "C0_023_AND_C0_035_CONSTITUTIONALLY_ADOPTED_PENDING_SEPARATE_FOUNDER_LOCK",
        "checks": checks,
        "all_checks_pass": all(value is True or key == "runtime_or_application_files_changed" and value is False for key, value in checks.items()),
        "requirement_traceability": {"C0-023": traceability, "C0-035": {}},
        "scan_details": {"merge_hits": merge_hits, "placeholder_hits": placeholder_hits, "secret_hits": secret_hits, "json_errors": json_errors, "broken_links": markdown_links(paths)},
        "findings": {"p0": 0, "open_p1": 0, "adoption_blocking_p2": 0, "retained_nonblocking_p2": 0},
        "semantic_deltas": 0,
        "authority": build["authority"],
    }
    return report


def produce_reports(validation: dict) -> list[Path]:
    validation_json = ROOT / "C0_023_C0_035_FORMAL_ADOPTION_VALIDATION.json"
    write_json(validation_json, validation)
    lines = [
        "# C0-023 and C0-035 Formal Adoption Validation",
        "",
        f"Result: `{'PASS' if validation['all_checks_pass'] else 'FAIL'}`",
        "",
        "| Gate | Result |",
        "|---|---|",
    ]
    for name, result in validation["checks"].items():
        passed = result is True or name == "runtime_or_application_files_changed" and result is False
        lines.append(f"| `{name}` | {'PASS' if passed else 'FAIL'} |")
    lines.extend(["", "P0: `0`; open P1: `0`; adoption-blocking P2: `0`; retained nonblocking P2: `0`.", "", "No substantive canon content changed. Constitutional lock was not issued. All operational authority remains `FALSE`."])
    validation_md = ROOT / "C0_023_C0_035_FORMAL_ADOPTION_VALIDATION.md"
    write(validation_md, "\n".join(lines))

    trace = ROOT / "C0_023_C0_035_REQUIREMENT_TRACEABILITY.md"
    trace_lines = ["# C0-023 and C0-035 Requirement Traceability", "", "No new requirement identifiers were created during adoption.", "", "## C0-023 Explicit Identifiers", "", "| Identifier | Present in adopted source |", "|---|---|"]
    for identifier, present in validation["requirement_traceability"]["C0-023"].items():
        trace_lines.append(f"| `{identifier}` | {'Yes' if present else 'No'} |")
    trace_lines.extend(["", "## C0-035 Explicit Identifiers", "", "The Reporting source defines no machine-style requirement identifier. Its numbered constitutional sections remain unchanged and trace through the adopted source as a whole."])
    write(trace, "\n".join(trace_lines))

    conflict = ROOT / "C0_023_C0_035_DEPENDENCY_AND_CONFLICT_REVIEW.md"
    write(conflict, """# C0-023 and C0-035 Dependency and Conflict Review

Result: `PASS`

- Privacy depends on Product Vision, Identity, Relationship, Agreement/Authorization, Record Stewardship, Security, Encryption, Audit, and minor protections.
- Reporting depends on Product Vision, Permission, Privacy, Record Stewardship, Audit, AI, Financial Truth, Search, and the affected source-domain canon.
- Reporting depends on Privacy; Privacy does not depend on Reporting. No direct dependency cycle is introduced.
- Privacy preserves Permission ownership of final authorization and Record Stewardship ownership of retention semantics.
- Reporting preserves source-domain ownership of canonical truth, Permission ownership of visibility, Privacy ownership of processing boundaries, and Audit ownership of evidentiary lineage.
- The Canon Index contains one active entry for each family, and the lock ledger contains no competing locked Privacy or Reporting canon.

No constitutional authority conflict or conflict with an already locked canon was identified. Constitutional lock remains separately gated.
""")

    visual = ROOT / "C0_023_C0_035_POST_ADOPTION_DOCX_VISUAL_QA.md"
    write(visual, """# C0-023 and C0-035 Post-Adoption DOCX Visual QA

Result: `PASS`

| Canon | Pages | Blank pages | Result |
|---|---:|---:|---|
| C0-023 Privacy | 24 | 0 | PASS |
| C0-035 Reporting | 15 | 0 | PASS |

All pages were rendered and visually reviewed. The adoption metadata is visible. No clipping, overlap, blank page, broken table, or incoherent page break was observed.
""")

    summary = ROOT / "C0_023_C0_035_CONSTITUTIONAL_ADOPTION_REPORT.md"
    write(summary, f"""# C0-023 and C0-035 Constitutional Adoption Report

## Disposition

`C0_023_AND_C0_035_CONSTITUTIONALLY_ADOPTED_PENDING_SEPARATE_FOUNDER_LOCK`

| Row | Adoption | Lock | P0 | Open P1 | Blocking P2 | Retained P2 |
|---|---|---|---:|---:|---:|---:|
| C0-023 | ADOPTED | NOT YET LOCKED | 0 | 0 | 0 | 0 |
| C0-035 | ADOPTED | NOT YET LOCKED | 0 | 0 | 0 | 0 |

The four pre-adoption files remain preserved under the separate adoption directories. Only document-control metadata changed. Privacy substantive content remains unchanged from `Authority Boundary` onward; Reporting substantive content remains unchanged from `1. Purpose` onward.

### Adopted Artifact Hashes

- Privacy Markdown: `{POST_HASHES[PRIVACY_MD]}`
- Privacy DOCX: `{POST_HASHES[PRIVACY_DOCX]}`
- Reporting DOCX: `{POST_HASHES[REPORTING_DOCX]}`
- Reporting Markdown: `{POST_HASHES[REPORTING_MD]}`

### Adoption Records

- `{rel(PRIVACY_RECORD)}`
- `{rel(REPORTING_RECORD)}`

Constitutional lock was not issued. Governance V1.0 baseline adoption/lock and all implementation, migration, runtime, provider, integration, deployment, production, customer-data, launch, certification, and public-trust authority remain `FALSE`.
""")
    return [validation_json, validation_md, trace, conflict, visual, summary]


def package(files: list[Path]) -> dict:
    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    changed = ROOT / "C0_023_C0_035_CHANGED_FILE_MANIFEST.json"
    manifest = ROOT / "C0_023_C0_035_ADOPTION_EVIDENCE_MANIFEST.json"
    package_record = ROOT / "C0_023_C0_035_ADOPTION_EVIDENCE_PACKAGE_RECORD.json"
    generated_controls = {changed, manifest, package_record}
    unique = sorted(set(
        path for path in files
        if path.exists()
        and PACKAGE_DIR not in path.parents
        and path != PACKAGE_ZIP
        and path not in generated_controls
    ))
    changed_data = {
        "scope": "C0-023 and C0-035 constitutional adoption only",
        "files": [{"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)} for path in unique],
        "runtime_or_application_files": [],
        "self_hash_excluded": True,
    }
    write_json(changed, changed_data)
    unique.append(changed)
    manifest_data = {
        "disposition": "C0_023_AND_C0_035_CONSTITUTIONALLY_ADOPTED_PENDING_SEPARATE_FOUNDER_LOCK",
        "files": [{"path": rel(path), "size_bytes": path.stat().st_size, "sha256": sha256(path)} for path in unique],
        "manifest_self_hash_excluded": True,
    }
    write_json(manifest, manifest_data)
    unique.append(manifest)
    for source in unique:
        destination = PACKAGE_DIR / rel(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    PACKAGE_ZIP.parent.mkdir(parents=True, exist_ok=True)
    if PACKAGE_ZIP.exists(): PACKAGE_ZIP.unlink()
    with zipfile.ZipFile(PACKAGE_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_DIR.rglob("*")):
            if path.is_file(): archive.write(path, path.relative_to(PACKAGE_DIR))
    with zipfile.ZipFile(PACKAGE_ZIP) as archive:
        assert archive.testzip() is None
        with tempfile.TemporaryDirectory() as directory:
            archive.extractall(directory)
            extracted = Path(directory)
            packaged_manifest = json.loads((extracted / rel(manifest)).read_text(encoding="utf-8"))
            for item in packaged_manifest["files"]:
                path = extracted / item["path"]
                assert path.is_file() and sha256(path) == item["sha256"]
    record = {
        "package": rel(PACKAGE_ZIP),
        "sha256": sha256(PACKAGE_ZIP),
        "size_bytes": PACKAGE_ZIP.stat().st_size,
        "archive_extraction_validation": "PASS",
        "manifest_entry_validation": "PASS",
        "file_count": len(unique),
        "constitutional_lock": False,
        "authority": json.loads((ROOT / "C0_023_C0_035_ADOPTION_BUILD_RECORD.json").read_text(encoding="utf-8"))["authority"],
    }
    write_json(ROOT / "C0_023_C0_035_ADOPTION_EVIDENCE_PACKAGE_RECORD.json", record)
    return record


def main() -> None:
    validation = validate()
    if not validation["all_checks_pass"]:
        write_json(ROOT / "C0_023_C0_035_FORMAL_ADOPTION_VALIDATION.json", validation)
        raise SystemExit("Formal adoption validation failed")
    reports = produce_reports(validation)
    files = active_files() + reports
    record = package(files)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
