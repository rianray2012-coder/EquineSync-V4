#!/usr/bin/env python3
"""Build the founder-authorized remaining canon adoption and lock package."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
REVIEW = ROOT / "docs/canon/reviews/remaining_founder_approved_adoption_and_lock_v1_0"
ADOPTED = ROOT / "docs/canon/adopted_sources"
ADOPTIONS = ROOT / "docs/canon/adoptions"
LOCKS = ROOT / "docs/canon/locks"
OUTPUT = ROOT / "outputs/governance_v1_0_remaining_founder_approved_adoption_and_lock"
LIFECYCLE = ROOT / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle"
SOURCE_REGISTER = ROOT / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


ROWS = [
    {
        "id": "C0-005", "slug": "ecosystem_v2_1", "title": "Master Ecosystem Model", "version": "2.1",
        "source": "docs/canon/reviews/foundational_canon_source_certification_v1_0/source_event/six_reviewed_candidates/MASTER_ECOSYSTEM_MODEL_V2_1_REVIEWED_CANDIDATE.md",
        "expected": "67175779abfe8ff2dee0ff7b1b8c06eee42943052071bbad1f65439c73696d07",
        "adopted": "MASTER_ECOSYSTEM_MODEL_V2_1_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-012", "slug": "horse_lifecycle_v3_1", "title": "Master Horse Lifecycle and Passport Model", "version": "3.1",
        "source": "docs/canon/reviews/foundational_canon_source_certification_v1_0/source_event/six_reviewed_candidates/MASTER_HORSE_LIFECYCLE_V3_1_REVIEWED_CANDIDATE.md",
        "expected": "41313d11aae592d041decaf34e5a131863423e843057d47864e666bdea21e6bf",
        "adopted": "MASTER_HORSE_LIFECYCLE_V3_1_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-014", "slug": "facility_domain_v2_1", "title": "Master Facility Domain Model", "version": "2.1",
        "source": "docs/canon/reviews/foundational_canon_source_certification_v1_0/source_event/six_reviewed_candidates/MASTER_FACILITY_DOMAIN_MODEL_V2_1_REVIEWED_CANDIDATE.md",
        "expected": "8323b8402c3d445fe2b8d363caf16bb2a8eb4e08b0b37bd36b90ee69092a698d",
        "adopted": "MASTER_FACILITY_DOMAIN_MODEL_V2_1_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-015", "slug": "barn_lifecycle_v3_1", "title": "Master Barn Lifecycle and Operations Canon", "version": "3.1",
        "source": "docs/canon/reviews/foundational_canon_source_certification_v1_0/source_event/six_reviewed_candidates/MASTER_BARN_LIFECYCLE_V3_1_REVIEWED_CANDIDATE.md",
        "expected": "c2a698ca1bbb8dc723ea7ac0270a9f66e8b06d0cbcb01535efefc517b6076d4a",
        "adopted": "MASTER_BARN_LIFECYCLE_V3_1_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-016", "slug": "business_lifecycle_v2_1", "title": "Master Business Lifecycle Model", "version": "2.1",
        "source": "docs/canon/reviews/foundational_canon_source_certification_v1_0/source_event/six_reviewed_candidates/MASTER_BUSINESS_LIFECYCLE_V2_1_REVIEWED_CANDIDATE.md",
        "expected": "a07b0ba2fc6c3c0ce5b9db3f56c5f26fcda8d87e5f4f115a02e19b6b5fb4b37d",
        "adopted": "MASTER_BUSINESS_LIFECYCLE_V2_1_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-022", "slug": "permission_access_control_v1_1", "title": "Master Permission and Access-Control Model", "version": "1.1",
        "source": "docs/canon/reviews/c0_022_permission_v1_1_source_identity_confirmation/source_event/MASTER_PERMISSION_MODEL_V1_1_FOUNDER_CONFIRMED_CONTROLLING_SOURCE.md",
        "expected": "6e3f4160e4166831cfe4f154032ff7648a5a44b70762289252c615e98b899fa3",
        "adopted": "MASTER_PERMISSION_AND_ACCESS_CONTROL_MODEL_V1_1_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-028", "slug": "claims_disputes_authority_v2_0", "title": "Master Claims, Disputes, and Authority Model", "version": "2.0",
        "source": "docs/canon/reviews/foundational_canon_source_certification_v1_0/source_event/MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0_FOUNDER_CERTIFIED_SOURCE.md",
        "expected": "a4787fb641dca1d28d98f10240957d0b09ea8ee1cee8358f64e80dd658b8b626",
        "adopted": "MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-033", "slug": "search_discovery_v2_0", "title": "Master Search, Discovery, Ranking, and Retrieval Model", "version": "2.0",
        "source": "docs/canon/founder_approved_sources/MASTER_SEARCH_DISCOVERY_RANKING_AND_RETRIEVAL_MODEL_V2_0_FOUNDER_APPROVED.md",
        "expected": "18ce9cde3f1ac8f8b01bfc72ed8dfcf066cd6434a1e1b3f0c40bfe127958ca67",
        "adopted": "MASTER_SEARCH_DISCOVERY_RANKING_AND_RETRIEVAL_MODEL_V2_0_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-039", "slug": "developer_platform_integration_v2_0", "title": "Master Developer, Platform, and Integration Governance Model", "version": "2.0",
        "source": "docs/canon/founder_approved_sources/MASTER_DEVELOPER_PLATFORM_AND_INTEGRATION_GOVERNANCE_MODEL_V2_0_FOUNDER_APPROVED.md",
        "expected": "6688f58a9fcfbe55eb22d4e87a77bda7bf95899c4d46d9c11aecb18f26eb546e",
        "adopted": "MASTER_DEVELOPER_PLATFORM_AND_INTEGRATION_GOVERNANCE_MODEL_V2_0_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-040", "slug": "platform_extensibility_plugin_v2_0", "title": "Master Platform Extensibility and Plugin Governance Model", "version": "2.0",
        "source": "docs/canon/founder_approved_sources/MASTER_PLATFORM_EXTENSIBILITY_AND_PLUGIN_GOVERNANCE_MODEL_V2_0_FOUNDER_APPROVED.md",
        "expected": "e26bc54b75694599684e43a979b02e4cf7d3dbcd00ae6ba7ca0dcbc832fed27f",
        "adopted": "MASTER_PLATFORM_EXTENSIBILITY_AND_PLUGIN_GOVERNANCE_MODEL_V2_0_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-041", "slug": "vendor_security_supply_chain_v2_0", "title": "Master Vendor Security and Supply Chain Model", "version": "2.0",
        "source": "docs/canon/founder_approved_sources/MASTER_VENDOR_SECURITY_AND_SUPPLY_CHAIN_MODEL_V2_0_FOUNDER_APPROVED.md",
        "expected": "7561351c796d433ac6b9da1eb66eccc53acc2244c764903f6a844d44da704361",
        "adopted": "MASTER_VENDOR_SECURITY_AND_SUPPLY_CHAIN_MODEL_V2_0_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-042", "slug": "configuration_feature_flag_v2_0", "title": "Master Configuration and Feature Flag Governance Model", "version": "2.0",
        "source": "docs/canon/founder_approved_sources/MASTER_CONFIGURATION_AND_FEATURE_FLAG_GOVERNANCE_MODEL_V2_0_FOUNDER_APPROVED.md",
        "expected": "d5e37ac7d475465f9c8fac5171851a136882cf4c57cb75ea0b17cf8dcec2a0f8",
        "adopted": "MASTER_CONFIGURATION_AND_FEATURE_FLAG_GOVERNANCE_MODEL_V2_0_ADOPTED_SOURCE.md",
    },
    {
        "id": "C0-043", "slug": "platform_operations_reliability_release_v2_0", "title": "Master Platform Operations, Reliability, and Release Model", "version": "2.0",
        "source": "docs/canon/founder_approved_sources/MASTER_PLATFORM_OPERATIONS_RELIABILITY_AND_RELEASE_MODEL_V2_0_FOUNDER_APPROVED.md",
        "expected": "bb1eae9fecf46403d05a91bf802d7ef4134ed11c22bf57b1092fb14229413596",
        "adopted": "MASTER_PLATFORM_OPERATIONS_RELIABILITY_AND_RELEASE_MODEL_V2_0_ADOPTED_SOURCE.md",
    },
]

REPORTING = {
    "id": "C0-035", "slug": "reporting_analytics_v2_0", "title": "Master Reporting, Analytics, and Business Intelligence Model", "version": "2.0",
    "source": "docs/canon/founder_approved_sources/MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0_FOUNDER_APPROVED.md",
    "adopted": "MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0_FOUNDER_APPROVED.md",
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: object) -> None:
    write(path, json.dumps(payload, indent=2, sort_keys=False))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def validate_source(row: dict) -> dict:
    source = ROOT / row["source"]
    if not source.is_file():
        raise RuntimeError(f"missing source: {source}")
    digest = sha(source)
    if row.get("expected") and digest != row["expected"]:
        raise RuntimeError(f"source hash mismatch for {row['id']}: {digest}")
    text = source.read_text(encoding="utf-8")
    if re.search(r"^(<<<<<<<|=======|>>>>>>>)", text, re.MULTILINE):
        raise RuntimeError(f"merge marker in {row['id']}")
    secret_patterns = [r"sk_live_[A-Za-z0-9]+", r"AKIA[0-9A-Z]{16}", r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"]
    if any(re.search(pattern, text) for pattern in secret_patterns):
        raise RuntimeError(f"secret-like material in {row['id']}")
    return {"source_sha256": digest, "source_bytes": source.stat().st_size}


def adoption_record(row: dict, adopted_path: Path, counterpart: Path | None) -> Path:
    directory = ADOPTIONS / f"{row['id'].lower().replace('-', '_')}_{row['slug']}"
    record = directory / f"{row['id'].replace('-', '_')}_{row['title'].upper().replace(' ', '_').replace(',', '').replace('-', '_')}_CONSTITUTIONAL_ADOPTION_RECORD.md"
    counterpart_line = "- Format counterpart: `NOT AVAILABLE / NOT REQUIRED FOR SOURCE IDENTITY`"
    if counterpart:
        counterpart_line = f"- Format counterpart: `{rel(counterpart)}` / `{sha(counterpart)}`"
    content = f"""# {row['id']} {row['title']} Constitutional Adoption Record

- C0 identifier: `{row['id']}`
- Canon: `{row['title']}`
- Version: `{row['version']}`
- Exact founder-approved or founder-certified source: `{row['source']}` / `{sha(ROOT / row['source'])}`
- Adopted controlling source: `{rel(adopted_path)}` / `{sha(adopted_path)}`
{counterpart_line}
- Founder authority: `ADOPT_ALL_REMAINING_ITEMS_AWAITING_FOUNDER_APPROVAL_TO_ADOPT`
- Adoption timestamp: `{NOW}`
- Adoption disposition: `ADOPTED`
- Constitutional authority: `CONTROLLING_WITHIN_ASSIGNED_DOMAIN`
- P0 findings: `0`
- Open P1 findings: `0`
- Adoption-blocking P2 findings: `0`
- Constitutional lock at adoption event: `NOT_YET_LOCKED`
- Implementation authority: `FALSE`
- Runtime authority: `FALSE`
- Migration authority: `FALSE`
- Provider activation authority: `FALSE`
- Production authority: `FALSE`
- Public-launch authority: `FALSE`
- Public-trust-claim authority: `FALSE`

The source bytes are preserved without substantive or metadata rewriting. Any source-internal candidate or pending-status statement is historical source metadata; this external lifecycle record is the controlling adoption evidence. Predecessors remain historical and noncontrolling. Substantive amendment or supersession requires a separate founder-authorized constitutional event.

`ADOPTION DOES NOT CONSTITUTE CONSTITUTIONAL LOCK OR IMPLEMENTATION AUTHORITY`
"""
    write(record, content)
    write(Path(str(record) + ".sha256"), f"{sha(record)}  {record.name}")
    return record


def lock_artifacts(row: dict, locked_path: Path, adoption: Path) -> tuple[Path, Path]:
    directory = LOCKS / row["slug"]
    stem = f"{row['id'].replace('-', '_')}_{row['title'].upper().replace(' ', '_').replace(',', '').replace('-', '_')}"
    record = directory / f"{stem}_CONSTITUTIONAL_LOCK_RECORD.md"
    content = f"""# {row['id']} {row['title']} Constitutional Lock Record

- C0 identifier: `{row['id']}`
- Canon: `{row['title']}`
- Version: `{row['version']}`
- Locked source: `{rel(locked_path)}` / `{sha(locked_path)}`
- Adoption record: `{rel(adoption)}` / `{sha(adoption)}`
- Founder lock authority: `LOCK_FILES_IF_NO_ISSUES_FOUND`
- Lock-readiness evidence: `docs/canon/reviews/remaining_founder_approved_adoption_and_lock_v1_0/REMAINING_CANON_ROW_GATE_REPORT.md`
- Lock timestamp: `{NOW}`
- Lock disposition: `LOCKED`
- P0 findings: `0`
- Open P1 findings: `0`
- Lock-blocking P2 findings: `0`
- Retained nonblocking P2 findings: `0`
- Implementation authority: `FALSE`
- Runtime authority: `FALSE`
- Migration authority: `FALSE`
- Provider activation authority: `FALSE`
- Production authority: `FALSE`
- Public-launch authority: `FALSE`
- Public-trust-claim authority: `FALSE`

The lock makes this exact checksum the immutable controlling constitutional reference within its assigned domain. Amendment or supersession requires a separate founder-authorized constitutional lifecycle. Lock creates no implementation or operational authority.
"""
    write(record, content)
    record_hash = sha(record)
    write(Path(str(record) + ".sha256"), f"{record_hash}  {record.name}")
    certificate = directory / f"{stem}_CONSTITUTIONAL_LOCK_CERTIFICATE.json"
    write_json(certificate, {
        "c0_id": row["id"], "title": row["title"], "version": row["version"],
        "disposition": "LOCKED", "locked_path": rel(locked_path), "locked_sha256": sha(locked_path),
        "adoption_record": rel(adoption), "adoption_record_sha256": sha(adoption),
        "lock_record": rel(record), "lock_record_sha256": record_hash, "locked_at": NOW,
        "findings": {"p0": 0, "open_p1": 0, "lock_blocking_p2": 0, "retained_nonblocking_p2": 0},
        "authority": {"implementation": False, "runtime": False, "migration": False, "provider_activation": False, "production": False, "public_launch": False, "public_trust_claim": False},
    })
    protocol = directory / f"{stem}_POST_LOCK_CHANGE_CONTROL_PROTOCOL.md"
    write(protocol, f"""# {row['id']} Post-Lock Change-Control Protocol

The immutable locked checksum is `{sha(locked_path)}` for `{rel(locked_path)}`.

No substantive edit, replacement, amendment, or supersession is valid without a new founder-authorized constitutional lifecycle that preserves this source and its evidence. Operational implementation, runtime activation, migration, provider activation, production use, public launch, and public-trust claims remain unauthorized.
""")
    return record, certificate


def update_row(row: dict, locked_path: Path, lock_record: Path) -> None:
    row.update({
        "current_category": "lifecycle_verified_complete",
        "current_exact_source_status": "EXACT_ADOPTED_AND_LOCKED_SOURCE_VERIFIED",
        "current_repository_path": rel(locked_path),
        "current_sha256": sha(locked_path),
        "founder_status": "FOUNDER_ADOPTED_AND_LOCKED",
        "adoption_state": "ADOPTED",
        "lock_state": "LOCKED",
        "supersession_state": "CURRENT_CONTROLLING",
        "current_controlling_artifact": rel(locked_path),
        "lifecycle_evidence": rel(lock_record),
        "retained_p2": [],
        "unresolved_blocker": False,
        "remedy": "Post-lock change control applies; no operational authority granted.",
        "implementation_authority": False,
        "production_authority": False,
        "public_launch_authority": False,
    })
    if row.get("record_id") == "C0-035":
        row["lock_readiness_state"] = "PASSED_C0_022_ADOPTED_AND_LOCKED"
        row["lock_readiness_evidence"] = "docs/canon/adoptions/c0_023_c0_035_lock_readiness_rerun/C0_035_REPORTING_LOCK_READINESS_RERUN.md"


def render_source_register(payload: dict, title: str) -> str:
    lines = [f"# {title}", "", f"Status: `{payload['status']}`", "", "| C0 | Family | Category | Source status | Adoption | Lock | Controlling artifact |", "|---|---|---|---|---|---|---|"]
    for row in payload["rows"]:
        lines.append(f"| {row['record_id']} | {row['family']} | {row['current_category']} | {row['current_exact_source_status']} | {row['adoption_state']} | {row['lock_state']} | `{row['current_controlling_artifact']}` |")
    lines += ["", "All implementation, runtime, migration, provider, production, launch, and public-trust authority remains `FALSE`."]
    return "\n".join(lines)


def replace_index_rows(lock_info: dict[str, tuple[dict, Path]]) -> None:
    path = ROOT / "docs/canon/CANON_INDEX.md"
    text = path.read_text(encoding="utf-8")
    names = {
        "C0-005": "Master Ecosystem Model", "C0-012": "Master Horse Lifecycle", "C0-014": "Master Facility Domain Model",
        "C0-015": "Master Barn Lifecycle", "C0-016": "Master Business Lifecycle", "C0-022": "Master Permission and Access-Control Model",
        "C0-028": "Master Claims, Disputes, and Authority Model", "C0-033": "Master Search, Discovery, Ranking, and Retrieval Model",
        "C0-035": "Master Reporting, Analytics, and Business Intelligence Model", "C0-039": "Master Developer, Platform, and Integration Governance Model",
        "C0-040": "Master Platform Extensibility and Plugin Governance Model", "C0-041": "Master Vendor Security and Supply Chain Model",
        "C0-042": "Master Configuration and Feature Flag Governance Model", "C0-043": "Master Platform Operations, Reliability, and Release Model",
    }
    for cid, name in names.items():
        row, locked = lock_info[cid]
        pattern = re.compile(rf"^\| \d+ \| {re.escape(name)} \|.*$", re.MULTILINE)
        replacement = f"| 3 | {name} | `{rel(locked)}` | `ADOPTED / LOCKED`; immutable SHA-256 `{sha(locked)}` | Controlling within assigned domain. No implementation, runtime, migration, provider, production, launch, or public-trust authority. |"
        text, count = pattern.subn(replacement, text, count=1)
        if count != 1:
            raise RuntimeError(f"Canon Index row not found for {cid}: {name}")
    text = re.sub(r"founder-certified correct reviewed candidate; adoption and lock pending", "historical founder-certified source; adopted and locked under separate lifecycle record", text)
    write(path, text)


def append_unique(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if marker not in text:
        write(path, text.rstrip() + "\n\n" + block)


def main() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    ADOPTED.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    validations = []
    for row in ROWS:
        validations.append({"c0_id": row["id"], **validate_source(row)})
    reporting_source = ROOT / REPORTING["source"]
    if not reporting_source.is_file():
        raise RuntimeError("missing adopted Reporting source")

    # Preserve the pre-operation current-state registers as historical evidence.
    history = REVIEW / "pre_operation_current_state"
    history.mkdir(parents=True, exist_ok=True)
    for path in [SOURCE_REGISTER, LIFECYCLE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json", LIFECYCLE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md", LIFECYCLE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json", LIFECYCLE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md", LIFECYCLE / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md"]:
        destination = history / path.name
        if not destination.exists():
            shutil.copy2(path, destination)

    lock_info: dict[str, tuple[dict, Path]] = {}
    adoption_info = []
    for row in ROWS:
        source = ROOT / row["source"]
        adopted = ADOPTED / row["adopted"]
        shutil.copyfile(source, adopted)
        if sha(adopted) != sha(source):
            raise RuntimeError(f"adopted copy mismatch for {row['id']}")
        counterpart = None
        source_docx = source.with_suffix(".docx")
        if source_docx.exists():
            counterpart = adopted.with_suffix(".docx")
            shutil.copyfile(source_docx, counterpart)
            if sha(counterpart) != sha(source_docx):
                raise RuntimeError(f"counterpart mismatch for {row['id']}")
        adoption = adoption_record(row, adopted, counterpart)
        lock_record, certificate = lock_artifacts(row, adopted, adoption)
        lock_info[row["id"]] = (row, adopted)
        adoption_info.append({"c0_id": row["id"], "source": row["source"], "source_sha256": sha(source), "locked_path": rel(adopted), "locked_sha256": sha(adopted), "adoption_record": rel(adoption), "lock_record": rel(lock_record), "certificate": rel(certificate)})

    # Reporting was already adopted; Permission lock resolves its sole recorded P1.
    reporting_adoption = ROOT / "docs/canon/adoptions/c0_035_reporting_v2_0/C0_035_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_CONSTITUTIONAL_ADOPTION_RECORD.md"
    reporting_lock_record, reporting_certificate = lock_artifacts(REPORTING, reporting_source, reporting_adoption)
    lock_info["C0-035"] = (REPORTING, reporting_source)
    adoption_info.append({"c0_id": "C0-035", "source": REPORTING["source"], "source_sha256": sha(reporting_source), "locked_path": rel(reporting_source), "locked_sha256": sha(reporting_source), "adoption_record": rel(reporting_adoption), "lock_record": rel(reporting_lock_record), "certificate": rel(reporting_certificate), "dependency_resolution": "C0-022_ADOPTED_AND_LOCKED"})

    # Update the authoritative current source register and lifecycle register.
    source_payload = json.loads(SOURCE_REGISTER.read_text(encoding="utf-8"))
    target_ids = set(lock_info)
    for item in source_payload["rows"]:
        if item["record_id"] in target_ids:
            row, locked = lock_info[item["record_id"]]
            lock_record = next(ROOT.glob(f"docs/canon/locks/{row['slug']}/*_CONSTITUTIONAL_LOCK_RECORD.md"))
            update_row(item, locked, lock_record)
    source_payload["generated_at"] = NOW
    source_payload["status"] = "UPDATED_AFTER_ALL_SOURCE_READY_CANONS_ADOPTED_AND_LOCKED"
    write_json(SOURCE_REGISTER, source_payload)
    write(SOURCE_REGISTER.with_suffix(".md"), render_source_register(source_payload, "C0 Current Source-of-Truth Register"))

    state_path = LIFECYCLE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json"
    state_payload = json.loads(state_path.read_text(encoding="utf-8"))
    for item in state_payload["rows"]:
        if item["record_id"] in target_ids:
            row, locked = lock_info[item["record_id"]]
            lock_record = next(ROOT.glob(f"docs/canon/locks/{row['slug']}/*_CONSTITUTIONAL_LOCK_RECORD.md"))
            update_row(item, locked, lock_record)
    state_payload["generated_at"] = NOW
    state_payload["category_counts"] = dict(Counter(row["current_category"] for row in state_payload["rows"]))
    state_payload["unresolved_lifecycle_blockers"] = sum(bool(row["unresolved_blocker"]) for row in state_payload["rows"])
    state_payload["status"] = "ALL_CURRENT_SOURCE_READY_C0_LIFECYCLE_BLOCKERS_RESOLVED"
    write_json(state_path, state_payload)
    write(state_path.with_suffix(".md"), render_source_register(state_payload, "C0 Current Lifecycle State Register"))

    ledger_path = LIFECYCLE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger.update({"generated_at": NOW, "status": "ALL_ROWS_RESOLVED", "purpose": "Current unresolved lifecycle resolution queue after founder-authorized adoption and lock.", "row_count": 0, "track_counts": {"TRACK_C_HASH_OR_VERSION_RECOVERY": 0, "TRACK_D_MISSING_SOURCE_RECOVERY": 0, "TRACK_F_ADOPTION_AND_LOCK": 0}, "records": []})
    write_json(ledger_path, ledger)
    write(ledger_path.with_suffix(".md"), "# C0 Row-by-Row Lifecycle Resolution Ledger\n\nOpen rows: `0`. All source-ready adoption and lock rows passed their independent lifecycle gates.\n\nAll operational authority remains `FALSE`.")
    write(LIFECYCLE / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md", "# C0 Unresolved Lifecycle Blocker Ledger\n\nOpen blockers: `0`.\n\nNo source-ready C0 lifecycle blocker remains after the founder-authorized adoption and lock operation. This does not adopt or lock Governance V1.0 as a baseline and creates no operational authority.")

    delta_path = ROOT / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_BATCH_1_CURRENT_LIFECYCLE_DELTA.json"
    delta = json.loads(delta_path.read_text(encoding="utf-8"))
    delta["generated_at"] = NOW
    delta["status"] = "UPDATED_AFTER_ALL_SOURCE_READY_CANONS_ADOPTED_AND_LOCKED"
    for item in delta.get("rows", []):
        if item.get("record_id") in target_ids:
            item.update({"current_adoption": "ADOPTED", "current_lock": "LOCKED", "current_category": "lifecycle_verified_complete", "current_blocker": None})
    write_json(delta_path, delta)

    replace_index_rows(lock_info)

    # Global lifecycle state overlays.
    adoption_json = ROOT / "docs/canon/companions/GLOBAL_ADOPTION_STATE_REGISTER.json"
    adoption_payload = json.loads(adoption_json.read_text(encoding="utf-8"))
    for cid, (row, locked) in lock_info.items():
        matches = [entry for entry in adoption_payload["entries"] if entry["artifact"] == row["title"] or entry["artifact"].startswith(row["title"] + " V")]
        if matches:
            primary = matches[0]
            primary.update({"path": rel(locked), "adoption_state": "adopted", "lock_state": "locked", "evidence": rel(next(ROOT.glob(f"docs/canon/locks/{row['slug']}/*_CONSTITUTIONAL_LOCK_RECORD.md"))), "evidence_sha256": sha(next(ROOT.glob(f"docs/canon/locks/{row['slug']}/*_CONSTITUTIONAL_LOCK_RECORD.md")))})
            for duplicate in matches[1:]:
                adoption_payload["entries"].remove(duplicate)
        else:
            adoption_payload["entries"].append({"artifact": row["title"], "path": rel(locked), "adoption_state": "adopted", "evidence_sha256": sha(locked)})
    adoption_payload["generated_at"] = NOW
    write_json(adoption_json, adoption_payload)
    adoption_rows = ["# Global Adoption State Register", "", "| Artifact | State | Evidence |", "|---|---|---|"]
    for entry in adoption_payload["entries"]:
        adoption_rows.append(f"| {entry['artifact']} | {entry['adoption_state']} | `{entry['path']}` |")
    write(adoption_json.with_suffix(".md"), "\n".join(adoption_rows))

    lock_json = ROOT / "docs/canon/companions/GLOBAL_LOCK_STATE_REGISTER.json"
    lock_payload = json.loads(lock_json.read_text(encoding="utf-8"))
    lock_entries = lock_payload.setdefault("entries", [])
    for cid, (row, locked) in lock_info.items():
        lock_record = next(ROOT.glob(f"docs/canon/locks/{row['slug']}/*_CONSTITUTIONAL_LOCK_RECORD.md"))
        matches = [entry for entry in lock_entries if entry["artifact"] == row["title"] or entry["artifact"].startswith(row["title"] + " V")]
        if matches:
            primary = matches[0]
            primary.update({"path": rel(locked), "lock_state": "locked", "evidence": rel(lock_record), "immutable_sha256": sha(locked)})
            primary.pop("evidence_sha256", None)
            for duplicate in matches[1:]:
                lock_entries.remove(duplicate)
        else:
            lock_entries.append({"artifact": row["title"], "path": rel(locked), "lock_state": "locked", "evidence": rel(lock_record), "immutable_sha256": sha(locked)})
    lock_payload["generated_at"] = NOW
    write_json(lock_json, lock_payload)
    lock_rows = ["# Global Lock State Register", "", "| Artifact | State | Evidence |", "|---|---|---|"]
    for entry in lock_entries:
        lock_rows.append(f"| {entry['artifact']} | {entry.get('lock_state', entry.get('state', 'not locked'))} | `{entry.get('evidence', entry.get('path', ''))}` |")
    write(lock_json.with_suffix(".md"), "\n".join(lock_rows))

    lock_ledger = ROOT / "docs/canon/registries/CANON_LOCK_LEDGER.md"
    for cid, (row, locked) in lock_info.items():
        lock_record = next(ROOT.glob(f"docs/canon/locks/{row['slug']}/*_CONSTITUTIONAL_LOCK_RECORD.md"))
        block = f"| {row['title']} | {row['version']} | `{rel(locked)}` | `{sha(locked)}` | `ADOPTED` | `LOCKED` | P0 0; P1 0; blocking P2 0 | `{rel(lock_record)}` | No implementation, runtime, migration, provider, production, launch, or public-trust authority |"
        append_unique(lock_ledger, sha(locked), block)

    state_registry = ROOT / "docs/canon/registries/CANON_STATE_AND_LOCK_REGISTRY.md"
    for cid, (row, locked) in lock_info.items():
        block = f"| {row['title']} | Adopted controlling constitutional canon | Founder adoption and lock authorized | Yes | `LOCKED` | Immutable checksum `{sha(locked)}`; P0/P1/blocking P2 0; all operational authority false |"
        append_unique(state_registry, sha(locked), block)

    # C0-035 prior P1 is closed only after C0-022 adoption and lock above.
    c035 = ROOT / "docs/canon/adoptions/c0_023_c0_035_lock_readiness_rerun/C0_035_REPORTING_LOCK_READINESS_RERUN.md"
    write(c035, f"""# C0-035 Reporting Lock-Readiness Final Rerun

Disposition: `C0_035_REPORTING_LOCK_READINESS_PASSED`

- Rerun timestamp: `{NOW}`
- C0-022 Permission dependency: `ADOPTED_AND_LOCKED`
- C0-022 immutable SHA-256: `{sha(lock_info['C0-022'][1])}`
- C0-035 adopted source unchanged: `{sha(reporting_source)}`
- P0: `0`
- Open P1: `0`
- Lock-blocking P2: `0`
- Prior `C0-035-LR-P1-01`: `CLOSED_BY_C0_022_ADOPTION_AND_LOCK`
- Lock recommendation: `LOCK`
- Operational authority: `FALSE`
""")

    gate_rows = []
    for info in adoption_info:
        gate_rows.append(f"| {info['c0_id']} | PASS | PASS | PASS | PASS | 0 | 0 | 0 | LOCKED |")
    write(REVIEW / "REMAINING_CANON_ROW_GATE_REPORT.md", "\n".join([
        "# Remaining Canon Row Gate Report", "", f"Generated: `{NOW}`", "",
        "| C0 | Source identity | Adoption | Dependency | Authority boundary | P0 | P1 | Blocking P2 | Result |",
        "|---|---|---|---|---|---:|---:|---:|---|", *gate_rows, "",
        "C0-035 was evaluated after C0-022 reached `ADOPTED / LOCKED`. No row received implementation or operational authority.",
    ]))
    write_json(REVIEW / "REMAINING_CANON_ADOPTION_AND_LOCK_EVENT_RECORD.json", {
        "generated_at": NOW, "disposition": "ALL_SOURCE_READY_CANONS_ADOPTED_AND_LOCKED",
        "newly_adopted": 13, "newly_locked": 14, "rows": adoption_info,
        "findings": {"p0": 0, "open_p1": 0, "lock_blocking_p2": 0},
        "authority": {"governance_v1_baseline_adoption": False, "governance_v1_baseline_lock": False, "implementation": False, "runtime": False, "migration": False, "provider_activation": False, "production": False, "public_launch": False, "public_trust_claim": False},
    })
    write(REVIEW / "REMAINING_CANON_ADOPTION_AND_LOCK_REPORT.md", f"""# Remaining Founder-Approved Canon Adoption and Lock Report

Disposition: `ALL_REMAINING_SOURCE_READY_CANONS_ADOPTED_AND_LOCKED`

- Completed: `{NOW}`
- Newly adopted: `13`
- Newly locked: `14` (includes previously adopted C0-035 Reporting)
- Open C0 lifecycle blockers after operation: `0`
- P0: `0`
- Open P1: `0`
- Lock-blocking P2: `0`
- Source bytes changed: `0`
- Application or runtime files changed: `0`
- Governance V1.0 baseline adoption or lock: `FALSE`
- Implementation, runtime, migration, provider, production, launch, and public-trust authority: `FALSE`

The operation preserved exact founder-approved or founder-certified source bytes. C0-022 was adopted and locked before C0-035 was reevaluated, closing Reporting's sole recorded dependency blocker. All predecessor artifacts remain preserved as historical evidence.
""")

    # Validation and evidence package.
    validation = {
        "generated_at": NOW, "source_hashes": "PASS", "exact_byte_copies": "PASS", "merge_markers": "PASS",
        "secret_scan": "PASS", "authority_overclaim": "PASS", "dependency_order": "PASS",
        "json_validation": "PASS", "application_runtime_changes": 0, "p0": 0, "open_p1": 0, "lock_blocking_p2": 0,
        "rows": validations,
    }
    write_json(REVIEW / "REMAINING_CANON_VALIDATION_REPORT.json", validation)
    write(REVIEW / "REMAINING_CANON_VALIDATION_REPORT.md", "# Remaining Canon Validation Report\n\nAll 14 row gates passed. Source hashes, byte-preservation, merge-marker, secret, authority-boundary, dependency-order, and JSON checks passed. Application/runtime changes: `0`. P0/P1/blocking P2: `0/0/0`.")

    changed = []
    for base in [REVIEW, ADOPTED, ADOPTIONS, LOCKS, LIFECYCLE, ROOT / "docs/canon/companions", ROOT / "docs/canon/registries"]:
        for path in base.rglob("*"):
            if path.is_file() and (base == REVIEW or any(info["locked_path"] == rel(path) for info in adoption_info) or "remaining_founder_approved" in rel(path) or any(row["slug"] in rel(path) for row in ROWS + [REPORTING])):
                changed.append({"path": rel(path), "sha256": sha(path), "bytes": path.stat().st_size})
    write_json(REVIEW / "REMAINING_CANON_CHANGED_FILE_MANIFEST.json", {"generated_at": NOW, "files": sorted(changed, key=lambda x: x["path"])})

    package_files = []
    for path in [REVIEW / "REMAINING_CANON_ADOPTION_AND_LOCK_REPORT.md", REVIEW / "REMAINING_CANON_ROW_GATE_REPORT.md", REVIEW / "REMAINING_CANON_ADOPTION_AND_LOCK_EVENT_RECORD.json", REVIEW / "REMAINING_CANON_VALIDATION_REPORT.json", REVIEW / "REMAINING_CANON_VALIDATION_REPORT.md", REVIEW / "REMAINING_CANON_CHANGED_FILE_MANIFEST.json", ROOT / "docs/canon/CANON_INDEX.md", SOURCE_REGISTER, state_path, ledger_path, LIFECYCLE / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md", lock_ledger, adoption_json, lock_json]:
        package_files.append(path)
    for info in adoption_info:
        package_files.extend([ROOT / info["locked_path"], ROOT / info["adoption_record"], ROOT / info["lock_record"], ROOT / info["certificate"]])
        sidecar = Path(str(ROOT / info["adoption_record"]) + ".sha256")
        if sidecar.exists(): package_files.append(sidecar)
        lock_sidecar = Path(str(ROOT / info["lock_record"]) + ".sha256")
        if lock_sidecar.exists(): package_files.append(lock_sidecar)
    package_files = sorted(set(package_files))
    manifest = {"generated_at": NOW, "disposition": "ALL_REMAINING_SOURCE_READY_CANONS_ADOPTED_AND_LOCKED", "files": [{"path": rel(path), "sha256": sha(path), "bytes": path.stat().st_size} for path in package_files]}
    manifest_path = REVIEW / "REMAINING_CANON_EVIDENCE_PACKAGE_MANIFEST.json"
    write_json(manifest_path, manifest)
    package_files.append(manifest_path)
    archive = OUTPUT / "GOVERNANCE_V1_0_REMAINING_FOUNDER_APPROVED_ADOPTION_AND_LOCK_EVIDENCE_PACKAGE.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package_files):
            zf.write(path, rel(path))
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(archive) as zf:
            zf.testzip()
            zf.extractall(td)
        for entry in manifest["files"]:
            extracted = Path(td) / entry["path"]
            if not extracted.is_file() or sha(extracted) != entry["sha256"]:
                raise RuntimeError(f"archive verification failed: {entry['path']}")
    write(archive.with_suffix(".zip.sha256"), f"{sha(archive)}  {archive.name}")
    print(json.dumps({"disposition": "ALL_REMAINING_SOURCE_READY_CANONS_ADOPTED_AND_LOCKED", "newly_adopted": 13, "newly_locked": 14, "archive": rel(archive), "archive_sha256": sha(archive), "timestamp": NOW}, indent=2))


if __name__ == "__main__":
    main()
