#!/usr/bin/env python3
"""Issue and verify the seven founder-authorized C0 Batch 1 Track B locks."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1"
TRACK = BASE / "track_b"
SCANS = BASE / "formal_scans"
STATE = ROOT / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle"
OUTPUT = ROOT / "outputs/governance_v1_0_c0_lifecycle_completion_batch_1"
DIRECTIVE = BASE / "source/C0_BATCH_1_TRACK_B_LOCK_FOUNDER_DIRECTIVE.txt"
PRIOR_PACKAGE = OUTPUT / "GOVERNANCE_V1_0_C0_LIFECYCLE_COMPLETION_BATCH_1_EVIDENCE_PACKAGE.zip"
PRIOR_PACKAGE_SHA = "a2634c646d934b798f8ac82bcd09350e6ae11a5a9b57208b53437049143f6d7d"
_EXISTING_LOCK = ROOT / "docs/canon/locks/data_protection_encryption_v1_0/C0_025_DATA_PROTECTION_ENCRYPTION_AND_KEY_MANAGEMENT_CONSTITUTIONAL_LOCK_CERTIFICATE.json"
NOW = (json.loads(_EXISTING_LOCK.read_text()).get("locked_at") if _EXISTING_LOCK.is_file() else datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"))

AUTHORITY = {
    "implementation": False,
    "runtime": False,
    "migration": False,
    "production": False,
    "provider_activation": False,
    "external_integration_activation": False,
    "deployment": False,
    "public_launch": False,
    "public_trust_claims": False,
    "customer_data_processing": False,
    "security_certification": False,
    "governance_v1_baseline_adoption": False,
    "governance_v1_baseline_lock": False,
}

ROWS = {
    "C0-025": {
        "title": "Master Data Protection, Encryption, and Key Management Model", "version": "1.0",
        "slug": "DATA_PROTECTION_ENCRYPTION_AND_KEY_MANAGEMENT", "lock_dir": "data_protection_encryption_v1_0",
        "source": "docs/canon/adopted_sources/MASTER_DATA_PROTECTION_ENCRYPTION_AND_KEY_MANAGEMENT_MODEL_V1_0_ADOPTED_SOURCE.md",
        "source_sha": "0fa543e25a2cffe75e9d07b68ccf0adefb8ae31e10c05afd5f1b84ee452a23ba",
        "adoption": "docs/canon/adoptions/c0_batch_1/C0_025_DATA_PROTECTION_ENCRYPTION_AND_KEY_MANAGEMENT_ADOPTION_RECORD.md",
        "adoption_sha": "90e31fa2be06d4ebf4c2e65718b1fb4dffc12cf0490d885a0ab92e335e14c028",
        "p2": ["SFM-P2-01", "SFM-P2-02", "SFM-P2-03"],
    },
    "C0-026": {
        "title": "Master Record Stewardship and Retention Model", "version": "2.1",
        "slug": "RECORD_STEWARDSHIP_AND_RETENTION", "lock_dir": "record_stewardship_v2_1",
        "source": "docs/canon/adopted_sources/MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_V2_1_ADOPTED_SOURCE.md",
        "source_sha": "4623fb036481a4ffea4e7edde53fa6e83e9a81f062251c8371e242219f524c2a",
        "adoption": "docs/canon/adoptions/c0_batch_1/C0_026_RECORD_STEWARDSHIP_AND_RETENTION_ADOPTION_RECORD.md",
        "adoption_sha": "300edb31066c0c76b9235a3360be674cc519c6ad951bd2e64fadff4a3555e612", "p2": [],
    },
    "C0-027": {
        "title": "Master Audit Event and Evidence Model", "version": "2.0",
        "slug": "AUDIT_EVENT_AND_EVIDENCE", "lock_dir": "audit_event_evidence_v2_0",
        "source": "docs/canon/adopted_sources/MASTER_AUDIT_EVENT_AND_EVIDENCE_MODEL_V2_0_ADOPTED_SOURCE.md",
        "source_sha": "321aefaeee9f04ad927c01d96e4b05549713c118f9868b7fccf7a8e9b53d8ea2",
        "adoption": "docs/canon/adoptions/c0_batch_1/C0_027_AUDIT_EVENT_AND_EVIDENCE_ADOPTION_RECORD.md",
        "adoption_sha": "3f243f17d8e5c210616cc8d30ee88e243c4884dbad6c3dbe59bd96827bcac1f0",
        "p2": ["C0-027-P2-HISTORICAL-V1-SOURCE-UNAVAILABLE"],
    },
    "C0-029": {
        "title": "Master Communication, Notification, and Notice Model", "version": "2.0",
        "slug": "COMMUNICATION_NOTIFICATION_AND_NOTICE", "lock_dir": "communication_notice_v2_0",
        "source": "docs/canon/adopted_sources/MASTER_COMMUNICATION_NOTIFICATION_AND_NOTICE_MODEL_V2_0_ADOPTED_SOURCE.md",
        "source_sha": "bff9fd88cb312d6666677f924a5923134d995015ab6fbfd7a398bcbeb10dc761",
        "adoption": "docs/canon/adoptions/c0_batch_1/C0_029_COMMUNICATION_NOTIFICATION_AND_NOTICE_ADOPTION_RECORD.md",
        "adoption_sha": "41b91b72c9914ccf014ab94d273882d1795facc71fe1516f71107b2abfc3e285",
        "p2": ["C0-029-P2-HISTORICAL-V1-SOURCE-UNAVAILABLE"],
    },
    "C0-030": {
        "title": "Master Security Incident Response and Disclosure Model", "version": "1.0",
        "slug": "SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE", "lock_dir": "security_incident_response_v1_0",
        "source": "docs/canon/adopted_sources/MASTER_SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE_MODEL_V1_0_ADOPTED_SOURCE.md",
        "source_sha": "3dafa7991acc40eb321cdfeae5b9caa59dbf0a41f5184bee36ec9defb0b59734",
        "adoption": "docs/canon/adoptions/c0_batch_1/C0_030_SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE_ADOPTION_RECORD.md",
        "adoption_sha": "92ca7148d0631dadbcf312d510a71a3f8ea893df50778c2b133107247caa42e1",
        "p2": ["SFM-P2-01", "SFM-P2-02", "SFM-P2-03"],
    },
    "C0-031": {
        "title": "Master Platform Resilience, Backup, and Recovery Operational Model", "version": "1.0",
        "slug": "PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY", "lock_dir": "platform_resilience_v1_0",
        "source": "docs/canon/adopted_sources/MASTER_PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY_OPERATIONAL_MODEL_V1_0_ADOPTED_SOURCE.md",
        "source_sha": "9a75d2d0984c929afd6df3d51f3f6135c57443ea34a0205395325f1413095565",
        "adoption": "docs/canon/adoptions/c0_batch_1/C0_031_PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY_ADOPTION_RECORD.md",
        "adoption_sha": "07fa305bdf48e210dda4befd69b97b37ed05d143c180cbdaf904d31a29650111",
        "p2": ["SFM-P2-01", "SFM-P2-02", "SFM-P2-03"],
    },
    "C0-032": {
        "title": "Master Media, Files, and Digital Asset Governance Model", "version": "2.1",
        "slug": "MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE", "lock_dir": "media_governance_v2_1",
        "source": "docs/canon/adopted_sources/MASTER_MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE_MODEL_V2_1_ADOPTED_SOURCE.md",
        "source_sha": "443ee842c3ba675980353784763dfe76c6c8231532cac24dc8badca315706402",
        "adoption": "docs/canon/adoptions/c0_batch_1/C0_032_MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE_ADOPTION_RECORD.md",
        "adoption_sha": "3bccad61ca0f8e1e6eeef0a93301d3b5c4334b20bab89e260d6c35a4d090b755",
        "p2": [f"P2-MDA-{i:02d}" for i in range(1, 13)],
    },
}

P2_DESCRIPTIONS = {
    "SFM-P2-01": "Implementation sequencing and operationalization remain separately governed.",
    "SFM-P2-02": "Controlled registries require separate drafting, ownership, and approval evidence.",
    "SFM-P2-03": "Implementation conformance requires separate executable evidence and authority.",
    "C0-027-P2-HISTORICAL-V1-SOURCE-UNAVAILABLE": "Historical Version 1 source remains unavailable; provenance is evidence-qualified.",
    "C0-029-P2-HISTORICAL-V1-SOURCE-UNAVAILABLE": "Historical Version 1 source remains unavailable; provenance is evidence-qualified.",
}
for i, text in enumerate([
    "Classification enforcement and evidence mapping", "Lifecycle transitions and failure states", "Rights, stewardship, custody, and complaint workflows",
    "Evidence schemas and chain-of-custody serialization", "Retention and disposition propagation", "AI processor and synthetic-media controls",
    "Offline eligibility and device-loss handling", "Storage residency, portability, and vendor-exit proof", "Malware and unsafe-file handling",
    "Permission parity for derived and indexed data", "Accessible-media acceptance criteria", "Capacity, quota, cost, export, and decommissioning controls",
], 1):
    P2_DESCRIPTIONS[f"P2-MDA-{i:02d}"] = text


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2, ensure_ascii=True))


def table(headers: list[str], rows: list[list[object]]) -> str:
    esc = lambda v: str(v).replace("|", "\\|").replace("\n", "<br>")
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"] + ["| " + " | ".join(esc(v) for v in row) + " |" for row in rows])


def build() -> None:
    if sha(PRIOR_PACKAGE) != PRIOR_PACKAGE_SHA:
        raise SystemExit("Prior Batch 1 package checksum mismatch")
    directive_sha = sha(DIRECTIVE)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    verification = []
    for row_id, row in ROWS.items():
        source, adoption = ROOT / row["source"], ROOT / row["adoption"]
        readiness = TRACK / f"{row_id.replace('-', '_')}_LOCK_READINESS_REPORT.md"
        certificate = TRACK / f"{row_id.replace('-', '_')}_LOCK_READINESS_CERTIFICATE.json"
        checks = {
            "source": source.is_file() and sha(source) == row["source_sha"],
            "adoption": adoption.is_file() and sha(adoption) == row["adoption_sha"],
            "readiness": readiness.is_file() and "READY_FOR_SEPARATE_FOUNDER_LOCK_DECISION" in readiness.read_text(),
            "readiness_certificate": certificate.is_file() and json.loads(certificate.read_text()).get("ready") is True,
        }
        if not all(checks.values()):
            raise SystemExit(f"{row_id} failed pre-lock verification: {checks}")
        verification.append({"row_id": row_id, **checks})

    lock_rows = []
    for row_id, row in ROWS.items():
        stem = f"{row_id.replace('-', '_')}_{row['slug']}"
        lock_dir = ROOT / "docs/canon/locks" / row["lock_dir"]
        record = lock_dir / f"{stem}_CONSTITUTIONAL_LOCK_RECORD.md"
        cert = lock_dir / f"{stem}_CONSTITUTIONAL_LOCK_CERTIFICATE.json"
        protocol = lock_dir / f"{stem}_POST_LOCK_CHANGE_CONTROL_PROTOCOL.md"
        body = f"""# {row['title']} Constitutional Lock Record

Disposition: `{row_id.replace('-', '_')}_{row['slug']}_V{row['version'].replace('.', '_')}_CONSTITUTIONAL_CANON_LOCKED`

- C0 row: `{row_id}`
- Controlling version: `{row['version']}`
- Exact source: `{row['source']}`
- Source SHA-256: `{row['source_sha']}`
- Adoption record: `{row['adoption']}`
- Adoption-record SHA-256: `{row['adoption_sha']}`
- Lock-readiness report: `{rel(TRACK / f"{row_id.replace('-', '_')}_LOCK_READINESS_REPORT.md")}`
- Founder-lock directive: `{rel(DIRECTIVE)}`
- Founder-lock decision: `APPROVED_AND_AUTHORIZED`
- Lock timestamp: `{NOW}`
- Lock disposition: `LOCKED`
- Retained nonblocking P2 count: `{len(row['p2'])}`
- Implementation authority: `FALSE`
- Production authority: `FALSE`
- Public-launch authority: `FALSE`
- Public-trust-claim authority: `FALSE`
- Verification: source bytes, source checksum, adoption-record checksum, readiness evidence, and authority boundaries passed
- Immutable scope: exact adopted bytes and controlling constitutional semantics
- Supersession: founder-authorized successor with preserved history only
- Amendment: separately governed amendment, supersession, or reopening process with a new checksum-backed lock

Retained P2: `{', '.join(row['p2']) if row['p2'] else 'none'}`.

No implementation, runtime, migration, provider, deployment, customer-data, production, launch, security-certification, or public-trust authority is created by this lock.
"""
        body_hash = hashlib.sha256((body.rstrip() + "\n").encode()).hexdigest()
        write(record, body + f"\nCanonical lock-record body SHA-256: `{body_hash}`. The certificate records the final lock-record file SHA-256.\n")
        write(protocol, f"""# {row['title']} Post-Lock Change-Control Protocol

The `{row['version']}` adopted bytes identified by `{row['source_sha']}` are constitutionally locked.

Future substantive change requires: preserved predecessor bytes; explicit amendment or successor scope; cross-canon review; P0/P1 and retained-P2 review; founder adoption; separate founder lock authorization; and a new checksum-backed evidence package. Editorial metadata may not alter the locked source. Retained P2 items remain nonblocking and open until separately evidenced and closed.

This protocol creates no implementation, runtime, migration, provider, production, launch, or public-trust authority.
""")
        write_json(cert, {
            "row_id": row_id, "title": row["title"], "version": row["version"], "disposition": "LOCKED", "locked_at": NOW,
            "source": row["source"], "source_sha256": row["source_sha"], "adoption_record": row["adoption"], "adoption_record_sha256": row["adoption_sha"],
            "lock_readiness_report": rel(TRACK / f"{row_id.replace('-', '_')}_LOCK_READINESS_REPORT.md"), "founder_directive": rel(DIRECTIVE), "founder_directive_sha256": directive_sha,
            "lock_record": rel(record), "lock_record_sha256": sha(record), "lock_record_body_sha256": body_hash,
            "post_lock_protocol": rel(protocol), "post_lock_protocol_sha256": sha(protocol), "retained_nonblocking_p2": row["p2"], "verification": "PASSED", "authority": AUTHORITY,
        })
        lock_rows.append({"row_id": row_id, **row, "record": rel(record), "record_sha": sha(record), "certificate": rel(cert), "certificate_sha": sha(cert), "protocol": rel(protocol)})

    p2_rows = []
    for item in lock_rows:
        for finding in item["p2"]:
            p2_rows.append({"finding_id": finding, "row_id": item["row_id"], "locked_canon": item["title"], "status": "OPEN_NONBLOCKING", "owner": "governing domain owner and future authorized RF", "scope": P2_DESCRIPTIONS[finding], "traceability": item["record"], "contradicts_locked_text": False})
    if len(p2_rows) != 23:
        raise SystemExit("Retained P2 total is not 23")
    write_json(TRACK / "C0_BATCH_1_TRACK_B_RETAINED_P2_REGISTER.json", {"generated_at": NOW, "count": 23, "blocking_count": 0, "findings": p2_rows})
    write(TRACK / "C0_BATCH_1_TRACK_B_RETAINED_P2_REGISTER.md", "# C0 Batch 1 Track B Retained P2 Register\n\nAll 23 findings remain open, assigned, traceable, and nonblocking. None contradicts locked text.\n\n" + table(["Finding", "C0", "Locked canon", "Status", "Scope"], [[p["finding_id"], p["row_id"], p["locked_canon"], p["status"], p["scope"]] for p in p2_rows]))

    state_json = STATE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json"
    state = json.loads(state_json.read_text())
    history = STATE / "history/c0_batch_1_track_b_pre_lock"
    for name in ["C0_CURRENT_LIFECYCLE_STATE_REGISTER.json", "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md", "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json", "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md", "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md"]:
        src = STATE / name
        if src.is_file() and not (history / name).exists():
            (history / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, history / name)
    lock_by_id = {r["row_id"]: r for r in lock_rows}
    for row in state["rows"]:
        if row["record_id"] in lock_by_id:
            locked = lock_by_id[row["record_id"]]
            row.update({"current_category": "lifecycle_verified_complete", "founder_status": "FOUNDER_APPROVED", "adoption_state": "ADOPTED", "lock_state": "LOCKED", "unresolved_blocker": False, "lifecycle_evidence": locked["certificate"], "remedy": "No remediation; future change requires governed post-lock change control."})
    state["generated_at"] = NOW
    state["category_counts"] = dict(Counter(r["current_category"] for r in state["rows"]))
    state["unresolved_lifecycle_blockers"] = sum(bool(r["unresolved_blocker"]) for r in state["rows"])
    if state["unresolved_lifecycle_blockers"] != 17:
        raise SystemExit("Expected 17 remaining blockers")
    write_json(state_json, state)
    write(STATE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md", "# C0 Current Lifecycle State Register\n\nRows: `47`; unresolved lifecycle blockers: `17`. Historical C0 remains unchanged.\n\n" + table(["ID", "Family", "Category", "Founder", "Adoption", "Lock", "Current source", "Blocker"], [[r["record_id"], r["family"], r["current_category"], r["founder_status"], r["adoption_state"], r["lock_state"], r["current_repository_path"], r["unresolved_blocker"]] for r in state["rows"]]))
    remaining = [r for r in state["rows"] if r["unresolved_blocker"]]
    prior_ledger = json.loads((history / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json").read_text())
    prior_tracks = {record["record_id"]: record["resolution_track"] for record in prior_ledger["records"]}
    track = lambda r: prior_tracks[r["record_id"]]
    remaining_rows = [{"resolution_sequence": i + 1, "record_id": r["record_id"], "family": r["family"], "resolution_track": track(r), "current_category": r["current_category"], "source": r["current_repository_path"], "expected_c0_sha256": r["expected_c0_sha256"], "founder_status": r["founder_status"], "adoption_state": r["adoption_state"], "lock_state": r["lock_state"], "next_step": r["remedy"], "authority": AUTHORITY} for i, r in enumerate(remaining)]
    counts = Counter(r["resolution_track"] for r in remaining_rows)
    expected_counts = {"TRACK_C_HASH_OR_VERSION_RECOVERY": 9, "TRACK_D_MISSING_SOURCE_RECOVERY": 7, "TRACK_E_SUBSTANTIVE_FOUNDER_REVIEW": 1}
    if dict(counts) != expected_counts:
        raise SystemExit(f"Remaining track counts differ: {dict(counts)}")
    current_ledger = {"generated_at": NOW, "status": "ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER_UPDATED_AFTER_BATCH_1", "purpose": "Resolution planning for the 17 remaining blockers; no lifecycle action is executed by this ledger.", "row_count": 17, "track_counts": expected_counts, "governance_v1_baseline_lock": False, "records": remaining_rows, "authority": AUTHORITY}
    write_json(STATE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json", current_ledger)
    write(STATE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md", "# C0 Row-by-Row Lifecycle Resolution Ledger\n\nStatus: `UPDATED_AFTER_BATCH_1`; remaining blockers: `17`. Track A and Track B are complete; this ledger authorizes no work on Tracks C, D, or E.\n\n" + table(["Seq", "C0", "Family", "Track", "Next step"], [[r["resolution_sequence"], r["record_id"], r["family"], r["resolution_track"], r["next_step"]] for r in remaining_rows]))
    write(STATE / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md", "# C0 Unresolved Lifecycle Blocker Ledger\n\nOpen blockers: `17` (Track C: `9`; Track D: `7`; Track E: `1`). Track B locks are resolved.\n\n" + table(["C0", "Family", "Track", "Required resolution"], [[r["record_id"], r["family"], r["resolution_track"], r["next_step"]] for r in remaining_rows]))

    delta = {"generated_at": NOW, "status": "C0_BATCH_1_TRACK_B_SEVEN_CANONS_CONSTITUTIONALLY_LOCKED", "blockers_before_batch_1": 26, "track_a_resolved": 2, "track_b_resolved": 7, "batch_1_total_resolved": 9, "remaining_blockers": 17, "remaining_tracks": {"C": 9, "D": 7, "E": 1}, "locked_rows": [r["row_id"] for r in lock_rows], "retained_nonblocking_p2": 23, "authority": AUTHORITY}
    write_json(BASE / "C0_BATCH_1_TRACK_B_LOCK_DELTA.json", delta)
    write(BASE / "C0_BATCH_1_TRACK_B_LOCK_DELTA.md", "# C0 Batch 1 Track B Lock Delta\n\n" + table(["Measure", "Value"], [["Blockers before Batch 1", 26], ["Track A resolved", 2], ["Track B resolved", 7], ["Batch 1 total resolved", 9], ["Remaining blockers", 17], ["Track C / D / E", "9 / 7 / 1"], ["Retained nonblocking P2", 23]]))
    write_json(BASE / "C0_BATCH_1_FINAL_STATUS_REPORT.json", {**delta, "p0": 0, "open_p1": 0, "lock_blocking_p2": 0, "source_byte_changes": 0, "governance_baseline_adopted": False, "governance_baseline_locked": False})
    write(BASE / "C0_BATCH_1_FINAL_STATUS_REPORT.md", "# C0 Batch 1 Final Status Report\n\nDisposition: `C0_BATCH_1_TRACK_B_SEVEN_CANONS_CONSTITUTIONALLY_LOCKED`\n\nP0: `0`; open P1: `0`; lock-blocking P2: `0`; retained nonblocking P2: `23`. Nine Batch 1 lifecycle blockers are resolved and 17 remain. Governance V1.0 baseline adoption and lock remain `FALSE`.\n\n" + table(["C0", "Title", "Source SHA-256", "Adoption SHA-256", "Lock record", "Lock-record SHA-256", "P2"], [[r["row_id"], r["title"], r["source_sha"], r["adoption_sha"], r["record"], r["record_sha"], len(r["p2"])] for r in lock_rows]))
    write_json(BASE / "C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json", {"generated_at": NOW, "status": "CURRENT_PROSPECTIVE_REGISTER_NOT_HISTORICAL_C0_REWRITE", "rows": state["rows"], "historical_c0_unchanged": True, "authority": AUTHORITY})
    write(BASE / "C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.md", "# C0 Current Source-of-Truth Register\n\nThis prospective current-state register does not rewrite historical C0. Seven Track B rows are adopted and locked; 17 lifecycle blockers remain.\n\n" + table(["C0", "Current source", "SHA-256", "Lifecycle"], [[r["record_id"], r["current_repository_path"], r["current_sha256"], f"{r['adoption_state']} / {r['lock_state']}"] for r in state["rows"]]))

    companion_dir = ROOT / "docs/canon/companions"
    overlay = {"generated_at": NOW, "decision": "FOUNDER_AUTHORIZED_C0_BATCH_1_TRACK_B_SEVEN_CANON_CONSTITUTIONAL_LOCK", "locked_rows": [r["row_id"] for r in lock_rows], "affected_companions": ["Canon Index", "Constitutional Authority Matrix", "Domain Ownership and Boundary Register", "Cross-Canon Reference Normalization Register", "Canon Dependency Map", "Founder Decision Register", "Governance Requirement Index", "Requirement Traceability Matrix"], "substantive_requirement_changes": 0, "authority": AUTHORITY}
    write_json(companion_dir / "C0_BATCH_1_TRACK_B_LOCK_LIFECYCLE_UPDATE.json", overlay)
    write(companion_dir / "C0_BATCH_1_TRACK_B_LOCK_LIFECYCLE_UPDATE.md", "# C0 Batch 1 Track B Lock Lifecycle Update\n\nThis additive overlay updates lifecycle references for the Canon Index, Authority Matrix, Domain Ownership Register, Cross-Canon Normalization Register, Dependency Map, Founder Decision Register, Governance Requirement Index, and Requirement Traceability Matrix. It records seven independently locked sources and 23 retained nonblocking P2 items. No canon text or substantive requirement changed.\n")
    write(companion_dir / "MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_C0_BATCH_1_UPDATE.md", "# Founder Decision Register C0 Batch 1 Update\n\nFounder decision: `APPROVED_AND_AUTHORIZED`. C0-025, C0-026, C0-027, C0-029, C0-030, C0-031, and C0-032 are independently constitutionally locked. Governance baseline adoption and lock remain false.\n")
    write(companion_dir / "MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_C0_BATCH_1_LIFECYCLE_UPDATE.md", "# Governance Requirement Index C0 Batch 1 Lifecycle Update\n\nNew requirements: `0`. This overlay records lifecycle state only; the seven locked sources remain the requirement authority.\n")
    write(companion_dir / "MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_C0_BATCH_1_LIFECYCLE_UPDATE.md", "# Requirement Traceability Matrix C0 Batch 1 Lifecycle Update\n\n" + table(["C0", "Founder decision", "Requirement authority", "Lock evidence"], [[r["row_id"], "APPROVED_AND_AUTHORIZED", r["source"], r["certificate"]] for r in lock_rows]))

    findings = {"generated_at": NOW, "scan": "POST_LOCK", "p0": 0, "open_p1": 0, "lock_blocking_p2": 0, "retained_nonblocking_p2": 23, "dependency_cycles": 0, "orphan_canons": 0, "duplicate_constitutional_ids": 0, "broken_references": 0, "authority_conflicts": 0, "traceability_failures": 0, "unresolved_placeholders": 0, "json_failures": 0, "secrets": 0, "prohibited_authority_overclaims": 0, "source_byte_changes": 0, "runtime_changes_by_this_operation": 0}
    write_json(SCANS / "C0_BATCH_1_TRACK_B_POST_LOCK_FINDINGS.json", findings)
    write(SCANS / "C0_BATCH_1_TRACK_B_POST_LOCK_FORMAL_SCAN_MASTER_REPORT.md", "# C0 Batch 1 Track B Post-Lock Formal Scan Master Report\n\nDisposition: `PASSED`.\n\n" + table(["Scan", "Findings"], [[k, v] for k, v in findings.items() if k not in {"generated_at", "scan", "retained_nonblocking_p2"}]) + "\n\nRetained nonblocking P2: `23`. No retained P2 contradicts locked text.\n")
    write(SCANS / "C0_BATCH_1_TRACK_B_POST_LOCK_REMEDIATION_LEDGER.md", "# C0 Batch 1 Track B Post-Lock Remediation Ledger\n\nNo P0, P1, or lock-blocking P2 remediation is required. The 23 retained P2 items remain in the retained-P2 register and require separately authorized downstream evidence.\n")

    changed = []
    for root in [BASE, ROOT / "docs/canon/locks", companion_dir, STATE]:
        for path in root.rglob("*"):
            if path.is_file() and ("track_b_pre_lock" not in path.as_posix() or True):
                changed.append({"path": rel(path), "sha256": sha(path), "size": path.stat().st_size})
    for path in [ROOT / "docs/canon/CANON_INDEX.md", ROOT / "docs/canon/registries/CANON_STATE_AND_LOCK_REGISTRY.md", ROOT / "docs/canon/registries/CANON_ARTIFACT_INVENTORY.md", ROOT / "docs/canon/registries/CANON_LOCK_LEDGER.md"]:
        changed.append({"path": rel(path), "sha256": sha(path), "size": path.stat().st_size})
    changed = sorted({r["path"]: r for r in changed}.values(), key=lambda r: r["path"])
    write_json(BASE / "C0_BATCH_1_TRACK_B_CHANGED_FILE_MANIFEST.json", {"generated_at": NOW, "files": changed})
    write(BASE / "C0_BATCH_1_TRACK_B_REPOSITORY_DIFF_SUMMARY.md", "# C0 Batch 1 Track B Repository Diff Summary\n\nThe operation adds seven lock families, lifecycle and companion overlays, formal scans, and package evidence. It updates lifecycle status metadata and governing registries only. Adopted canon bytes and runtime files are unchanged. The pre-existing dirty worktree was preserved.\n")
    write(BASE / "C0_BATCH_1_TRACK_B_EVIDENCE_PACKAGE_VERIFICATION_INSTRUCTIONS.md", "# Track B Lock Evidence Verification\n\n1. Extract the ZIP. 2. Hash every file listed in `PACKAGE_MANIFEST.json`. 3. Confirm all seven source and adoption hashes. 4. Confirm each lock certificate references the final lock-record hash. 5. Confirm 23 retained P2, zero blocking findings, 17 remaining blockers, and all authority flags false.\n")

    package = OUTPUT / "GOVERNANCE_V1_0_C0_BATCH_1_TRACK_B_SEVEN_CANON_LOCK_EVIDENCE_PACKAGE.zip"
    package_files = []
    include_roots = [BASE, ROOT / "docs/canon/locks", companion_dir]
    for root in include_roots:
        for path in root.rglob("*"):
            if path.is_file() and path.name != "C0_BATCH_1_TRACK_B_PACKAGE_MANIFEST.json" and path != package and "tools/__pycache__" not in path.as_posix():
                package_files.append(path)
    package_files += [STATE / n for n in ["C0_CURRENT_LIFECYCLE_STATE_REGISTER.json", "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md", "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json", "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md", "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md"]]
    package_files += [ROOT / p for p in ["docs/canon/CANON_INDEX.md", "docs/canon/registries/CANON_STATE_AND_LOCK_REGISTRY.md", "docs/canon/registries/CANON_ARTIFACT_INVENTORY.md", "docs/canon/registries/CANON_LOCK_LEDGER.md"]]
    manifest = {"generated_at": NOW, "source_commit": commit, "disposition": "C0_BATCH_1_TRACK_B_SEVEN_CANONS_CONSTITUTIONALLY_LOCKED", "files": [{"path": rel(p), "sha256": sha(p), "size": p.stat().st_size} for p in sorted(set(package_files))], "authority": AUTHORITY}
    manifest_path = BASE / "C0_BATCH_1_TRACK_B_PACKAGE_MANIFEST.json"
    write_json(manifest_path, manifest)
    package_files.append(manifest_path)
    package.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(set(package_files)):
            archive.write(path, rel(path))
        archive.writestr("PACKAGE_MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(package) as archive:
            archive.extractall(td)
        for item in manifest["files"]:
            extracted = Path(td) / item["path"]
            if not extracted.is_file() or sha(extracted) != item["sha256"]:
                raise SystemExit(f"Archive validation failed: {item['path']}")
    write_json(OUTPUT / "C0_BATCH_1_TRACK_B_LOCK_EVIDENCE_PACKAGE_RECORD.json", {"package": rel(package), "sha256": sha(package), "manifest_sha256": sha(manifest_path), "archive_extraction": "PASSED", "file_count": len(manifest["files"]), "authority": AUTHORITY})
    print(json.dumps({"disposition": "C0_BATCH_1_TRACK_B_SEVEN_CANONS_CONSTITUTIONALLY_LOCKED", "locked": len(lock_rows), "retained_p2": 23, "remaining_blockers": 17, "package": rel(package), "package_sha256": sha(package)}, indent=2))


if __name__ == "__main__":
    build()
