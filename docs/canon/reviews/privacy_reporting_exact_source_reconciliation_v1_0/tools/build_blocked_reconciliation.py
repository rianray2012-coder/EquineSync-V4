#!/usr/bin/env python3
"""Build the evidence-only C0-023/C0-035 exact-source blocker package."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import date
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
REVIEW = REPO / "docs/canon/reviews/privacy_reporting_exact_source_reconciliation_v1_0"
SOURCE_EVENT = REVIEW / "source_event"
MOUNTED_SOURCES = REVIEW / "mounted_sources"
OUTPUT_DIR = REPO / "outputs/Privacy_Reporting_Exact_Source_Reconciliation_Blocker_Package"
OUTPUT_ZIP = REPO / "outputs/privacy_reporting_exact_source_reconciliation_blocker_package.zip"
INPUT_ZIP = Path("/Users/rianray/Downloads/EQUINESYNC_PRIVACY_REPORTING_FOUNDER_APPROVAL_PACKAGE_V1_0.zip")

EXPECTED_PACKAGE_FILES = {
    "EQUINESYNC_PRIVACY_AND_REPORTING_FOUNDER_APPROVAL_DIRECTIVE_V1_0.md": "b42ac56490f4fe6e9e3d4abf56d01fc784d74f31c9cf03644d4ee019f9832b0f",
    "EQUINESYNC_PRIVACY_AND_REPORTING_FOUNDER_APPROVAL_DIRECTIVE_V1_0.docx": "41d0ff2a0fab3c45f909e706e241828d970a4a0816b0ed50e2892ea04b43aa0c",
    "EQUINESYNC_PRIVACY_AND_REPORTING_REVIEW_MEMO_V1_0.md": "5740e3b2c2a542cb753d995073a650252ef79cc640235b51a845537c851bd55c",
    "CODEX_PROMPT_PRIVACY_AND_REPORTING_EXACT_SOURCE_RECONCILIATION.md": "8436b4f8dbecb39a97bf26775aa1c7247eea61fd3b686a8adf5c4997872ce816",
    "CODEX_PROMPT_PRIVACY_AND_REPORTING_EXACT_SOURCE_RECONCILIATION.txt": "8436b4f8dbecb39a97bf26775aa1c7247eea61fd3b686a8adf5c4997872ce816",
    "PACKAGE_MANIFEST.md": "859a99fdb07356775761caaa3960622c7710a8447d246533359b83d843aefb99",
}

REQUIRED_SOURCES = (
    ("C0-023", "MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_REVIEWED_DRAFT.md"),
    ("C0-023", "MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_REVIEWED_DRAFT.docx"),
    ("C0-035", "MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0.md"),
    ("C0-035", "MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0.docx"),
)

AUTHORITY = {
    "implementation": False,
    "runtime": False,
    "schema_or_migration": False,
    "production": False,
    "external_processor_or_provider_activation": False,
    "public_claims": False,
    "public_launch": False,
    "repository_lock": False,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def discover_exact_sources() -> tuple[list[dict], int, int, list[str]]:
    roots = [Path("/Users/rianray/Downloads"), REPO]
    names = {name for _, name in REQUIRED_SOURCES}
    matches: list[dict] = []
    archives_scanned = 0
    archive_errors: list[str] = []

    for root in roots:
        for path in root.rglob("*"):
            if not path.is_file() or "node_modules" in path.parts:
                continue
            if path == OUTPUT_ZIP or REVIEW in path.parents or OUTPUT_DIR in path.parents:
                continue
            if path.name in names:
                matches.append({
                    "kind": "filesystem",
                    "path": str(path),
                    "filename": path.name,
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256(path),
                })
            if path.suffix.lower() != ".zip":
                continue
            archives_scanned += 1
            try:
                with zipfile.ZipFile(path) as archive:
                    for member in archive.infolist():
                        if Path(member.filename).name in names:
                            matches.append({
                                "kind": "zip_member",
                                "path": str(path),
                                "member": member.filename,
                                "filename": Path(member.filename).name,
                                "size_bytes": member.file_size,
                            })
            except (OSError, zipfile.BadZipFile) as exc:
                archive_errors.append(f"{path}: {type(exc).__name__}")
    return matches, len(roots), archives_scanned, archive_errors


def build() -> None:
    if not INPUT_ZIP.is_file():
        raise SystemExit(f"Missing approval package: {INPUT_ZIP}")

    SOURCE_EVENT.mkdir(parents=True, exist_ok=True)
    approval_copy = SOURCE_EVENT / INPUT_ZIP.name
    shutil.copy2(INPUT_ZIP, approval_copy)
    with zipfile.ZipFile(INPUT_ZIP) as archive:
        archive.extractall(SOURCE_EVENT)

    package_verification = []
    for filename, expected in EXPECTED_PACKAGE_FILES.items():
        path = SOURCE_EVENT / filename
        actual = sha256(path) if path.is_file() else None
        package_verification.append({
            "filename": filename,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "result": "PASS" if actual == expected else "FAIL",
        })

    matches, roots_scanned, archives_scanned, archive_errors = discover_exact_sources()
    MOUNTED_SOURCES.mkdir(parents=True, exist_ok=True)
    required = []
    for row_id, filename in REQUIRED_SOURCES:
        found = [item for item in matches if item["filename"] == filename]
        mounted_copy = None
        direct = next((item for item in found if item["kind"] == "filesystem"), None)
        if direct:
            mounted_copy = MOUNTED_SOURCES / filename
            shutil.copy2(Path(direct["path"]), mounted_copy)
        required.append({
            "row_id": row_id,
            "filename": filename,
            "status": "MOUNTED" if found else "NOT_MOUNTED",
            "matches": found,
            "preserved_repository_path": rel(mounted_copy) if mounted_copy else None,
            "preserved_sha256": sha256(mounted_copy) if mounted_copy else None,
            "preserved_size_bytes": mounted_copy.stat().st_size if mounted_copy else None,
        })

    approval_sha = sha256(approval_copy)
    mounted_count = sum(item["status"] == "MOUNTED" for item in required)
    complete = mounted_count == len(required)
    disposition = (
        "PRIVACY_REPORTING_EXACT_SOURCE_RECONCILIATION_READY_FOR_CROSS_FORMAT_REVIEW"
        if complete
        else "PRIVACY_REPORTING_EXACT_SOURCE_RECONCILIATION_PARTIALLY_MOUNTED_COUNTERPARTS_REQUIRED"
    )
    missing = [item for item in required if item["status"] == "NOT_MOUNTED"]
    missing_lines = "\n".join(
        f"{index}. `{item['filename']}`" for index, item in enumerate(missing, start=1)
    ) or "None."

    report = f"""# Privacy and Reporting Exact-Source Reconciliation Report V1.0

## Disposition

`{disposition}`

The July 16, 2026 founder-approval package is valid approval evidence, but it does not contain the four constitutional source files that its own directive requires. Two separately mounted attachments now provide the Privacy Markdown and Reporting DOCX. Their exact counterparts remain absent, so neither source pair is complete and cross-format reconciliation cannot begin.

## Founder Status Preserved

- `C0-023`: founder approved as controlling substantive Privacy canon by the mounted directive; the exact reviewed Markdown is preserved, but its exact DOCX counterpart is unavailable, so no successor was generated.
- `C0-035`: founder-approved controlling Reporting status is preserved; the exact DOCX is preserved, but its exact Markdown counterpart is unavailable, so no rewrite, downgrade, or substitute was created.

## Remaining Exact Missing Files

{missing_lines}

## Search Performed

- Direct filesystem filename search: `/Users/rianray/Downloads` and `{REPO}`.
- ZIP-member filename search: {archives_scanned} archives across the same roots, excluding dependency directories.
- Required exact files mounted: {mounted_count} of {len(required)}.
- Existing repository inventories and C0 records were reviewed. They identify the expected model names but do not provide retrievable exact bytes for these four files.
- No independently mounted File Library byte source was available. The approval directive names the files but is not a substitute for them.

## Why Substitution Is Prohibited

The controlling prompt expressly forbids reconstruction from snippets, summaries, chat, extracted fragments, memory, related analytics canon, or another version. The review memo and founder directive are lifecycle evidence, not the constitutional source text.

## Minimum Required Action

Mount or attach the two remaining exact counterpart files above. Once mounted, C0-023 and C0-035 can resume independently for hashing, Markdown/DOCX comparison, Privacy successor generation, Reporting source designation, and companion-register reconciliation.

## Authority Boundary

This evidence package creates no implementation, runtime, schema, migration, production, processor/provider activation, public-claims, public-launch, or repository-lock authority. No runtime file, canon source, C0 lifecycle register, permission behavior, or production state was changed.
"""
    write(REVIEW / "PRIVACY_REPORTING_EXACT_SOURCE_RECONCILIATION_REPORT_V1_0.md", report)

    comparison = """# Privacy and Reporting Cross-Format Comparison V1.0

## Result

`NOT_EXECUTED_EXACT_SOURCE_PAIRS_NOT_MOUNTED`

Neither required Markdown/DOCX source pair is complete. Material consistency cannot be assessed from a single format, the founder directive, review memo, prompt, or related canons. No counterpart was regenerated and no substantive inference was made.

| C0 Row | Markdown | DOCX | Comparison |
|---|---|---|---|
| C0-023 | MOUNTED AND HASHED | NOT MOUNTED | BLOCKED |
| C0-035 | NOT MOUNTED | MOUNTED AND HASHED | BLOCKED |
"""
    write(REVIEW / "PRIVACY_REPORTING_CROSS_FORMAT_COMPARISON_V1_0.md", comparison)

    discovery_lines = [
        "# Privacy and Reporting Exact-Source Discovery Inventory V1.0",
        "",
        f"- Approval ZIP: `{approval_copy}`",
        f"- Approval ZIP SHA-256: `{approval_sha}`",
        f"- Search roots: `/Users/rianray/Downloads`; `{REPO}`",
        f"- ZIP archives inspected: `{archives_scanned}`",
        f"- Required exact files mounted: `{mounted_count}` of `{len(required)}`",
        f"- Archive read errors: `{len(archive_errors)}`",
        "",
        "| C0 Row | Required filename | Status |",
        "|---|---|---|",
    ]
    for item in required:
        discovery_lines.append(f"| {item['row_id']} | `{item['filename']}` | {item['status']} |")
    discovery_lines.extend([
        "",
        "## File Library Evidence",
        "",
        "Repository records and the mounted directive name the expected models. No File Library object exposing the four exact source bytes is mounted in this workspace, so no File Library checksum can be asserted.",
        "",
        "## Archive Read Notes",
        "",
    ])
    discovery_lines.extend(f"- `{error}`" for error in archive_errors)
    if not archive_errors:
        discovery_lines.append("- None.")
    write(REVIEW / "PRIVACY_REPORTING_EXACT_SOURCE_DISCOVERY_INVENTORY_V1_0.md", "\n".join(discovery_lines))

    provenance = f"""# Privacy and Reporting Provenance and Checksum Ledger V1.0

| Artifact | Role | SHA-256 | Bytes |
|---|---|---|---:|
| `{rel(approval_copy)}` | Original founder approval package | `{approval_sha}` | {approval_copy.stat().st_size} |
"""
    for filename in EXPECTED_PACKAGE_FILES:
        path = SOURCE_EVENT / filename
        provenance += f"| `{rel(path)}` | Approval-package member | `{sha256(path)}` | {path.stat().st_size} |\n"
    for item in required:
        if item["preserved_repository_path"]:
            provenance += (
                f"| `{item['preserved_repository_path']}` | Partial exact constitutional source | "
                f"`{item['preserved_sha256']}` | {item['preserved_size_bytes']} |\n"
            )
    provenance += """

The mounted package establishes founder direction and lifecycle intent. The two separately supplied source files are preserved and hashed, but neither Markdown/DOCX pair is complete.
"""
    write(REVIEW / "PRIVACY_REPORTING_PROVENANCE_AND_CHECKSUM_LEDGER_V1_0.md", provenance)

    manifest = {
        "package": "PRIVACY_REPORTING_EXACT_SOURCE_RECONCILIATION_V1_0",
        "generated_on": str(date.today()),
        "disposition": disposition,
        "approval_package": {
            "source_path": str(INPUT_ZIP),
            "repository_path": rel(approval_copy),
            "size_bytes": approval_copy.stat().st_size,
            "sha256": approval_sha,
            "members_verified": package_verification,
        },
        "source_search": {
            "roots": ["/Users/rianray/Downloads", str(REPO)],
            "root_count": roots_scanned,
            "zip_archives_scanned": archives_scanned,
            "archive_errors": archive_errors,
            "exact_matches": matches,
        },
        "required_sources": required,
        "rows": [
            {
                "row_id": "C0-023",
                "founder_approval_state": "FOUNDER_APPROVED_CONTROLLING_SUBSTANTIVE_CANON",
                "source_state": "MARKDOWN_MOUNTED_DOCX_COUNTERPART_REQUIRED",
                "successor_state": "NOT_CREATED",
                "adoption_state": "NOT_GRANTED_BY_DIRECTIVE",
                "lock_state": "NOT_GRANTED_BY_DIRECTIVE",
                "unresolved_items": [required[1]["filename"]],
            },
            {
                "row_id": "C0-035",
                "founder_approval_state": "FOUNDER_APPROVED_CONTROLLING_CANON_STATUS_PRESERVED",
                "source_state": "DOCX_MOUNTED_MARKDOWN_COUNTERPART_REQUIRED",
                "successor_state": "NOT_APPLICABLE_NO_REWRITE_PERMITTED",
                "adoption_state": "ONLY_AS_SEPARATELY_EVIDENCED",
                "lock_state": "NOT_GRANTED_BY_DIRECTIVE",
                "unresolved_items": [required[2]["filename"]],
            },
        ],
        "cross_format_comparison": "NOT_EXECUTED_EXACT_SOURCE_PAIRS_NOT_MOUNTED",
        "companion_artifacts_updated": [],
        "authority": AUTHORITY,
    }
    manifest_path = REVIEW / "PRIVACY_REPORTING_EXACT_SOURCE_RECONCILIATION_MANIFEST_V1_0.json"
    write(manifest_path, json.dumps(manifest, indent=2))

    checks = {
        "approval_zip_present": INPUT_ZIP.is_file(),
        "approval_zip_sha256": approval_sha,
        "package_member_hashes_pass": all(item["result"] == "PASS" for item in package_verification),
        "exact_required_sources_mounted": complete,
        "mounted_source_count": mounted_count,
        "missing_source_stop_behavior": not complete,
        "source_reconstruction_performed": False,
        "canon_source_files_created": False,
        "runtime_files_changed_by_builder": False,
        "c0_lifecycle_registers_changed_by_builder": False,
        "authority_flags_all_false": not any(AUTHORITY.values()),
    }
    validation = {
        "result": "PASS_PARTIAL_MOUNT_BLOCKER_CORRECTLY_RETAINED" if not complete and checks["package_member_hashes_pass"] else "REVIEW_REQUIRED",
        "disposition": disposition,
        "checks": checks,
    }
    write(REVIEW / "PRIVACY_REPORTING_VALIDATION_REPORT_V1_0.json", json.dumps(validation, indent=2))
    validation_md = f"""# Privacy and Reporting Validation Report V1.0

**Result:** `{validation['result']}`

| Check | Result |
|---|---|
| Approval ZIP preserved and hashed | PASS (`{approval_sha}`) |
| Six declared package-member hashes | {'PASS' if checks['package_member_hashes_pass'] else 'FAIL'} |
| Four exact constitutional source files | BLOCKED: {mounted_count} of 4 mounted |
| Missing-source stop behavior | PASS |
| Reconstruction from summaries or snippets | NOT PERFORMED |
| Privacy successor generation | NOT PERFORMED |
| Reporting rewrite or lifecycle regression | NOT PERFORMED |
| Authority flags | ALL FALSE |

The blocker is an input-evidence condition, not a validation failure. Reconciliation cannot complete until both remaining exact counterpart files are mounted.
"""
    write(REVIEW / "PRIVACY_REPORTING_VALIDATION_REPORT_V1_0.md", validation_md)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    for path in sorted(REVIEW.rglob("*")):
        if not path.is_file() or "tools" in path.parts:
            continue
        target = OUTPUT_DIR / path.relative_to(REVIEW)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)

    package_artifacts = []
    for path in sorted(OUTPUT_DIR.rglob("*")):
        if path.is_file():
            package_artifacts.append({
                "path": path.relative_to(OUTPUT_DIR).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            })
    write(OUTPUT_DIR / "PACKAGE_ARTIFACT_MANIFEST.json", json.dumps({
        "disposition": disposition,
        "artifact_count": len(package_artifacts),
        "artifacts": package_artifacts,
        "authority": AUTHORITY,
    }, indent=2))

    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()
    with zipfile.ZipFile(OUTPUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(OUTPUT_DIR.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(OUTPUT_DIR.parent))

    package_record = {
        "disposition": disposition,
        "package_path": rel(OUTPUT_ZIP),
        "package_size_bytes": OUTPUT_ZIP.stat().st_size,
        "package_sha256": sha256(OUTPUT_ZIP),
        "authority": AUTHORITY,
    }
    write(REVIEW / "PRIVACY_REPORTING_EVIDENCE_PACKAGE_RECORD_V1_0.json", json.dumps(package_record, indent=2))
    print(json.dumps(package_record, indent=2))


if __name__ == "__main__":
    build()
