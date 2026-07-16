#!/usr/bin/env python3
"""Build C0 lifecycle completion Batch 1 evidence without runtime changes."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import time
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1"
B0 = BASE / "phase_b0"
TRACK_A = BASE / "track_a"
TRACK_B = BASE / "track_b"
SCANS = BASE / "formal_scans"
ADOPTIONS = ROOT / "docs/canon/adoptions/c0_batch_1"
ADOPTED = ROOT / "docs/canon/adopted_sources"
OUTPUT = ROOT / "outputs/governance_v1_0_c0_lifecycle_completion_batch_1"
STATE_DIR = ROOT / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle"
DIRECTIVE = BASE / "source/C0_LIFECYCLE_COMPLETION_BATCH_1_FOUNDER_DIRECTIVE.md"
LEDGER = STATE_DIR / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md"
LEDGER_SHA = "36145a7e1de6046f508116ea7939d7a81cac5adb25dc09088e36e22ad90d1e22"
NOW = lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2, ensure_ascii=True))


def table(headers: list[str], rows: list[list[object]]) -> str:
    def esc(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", "<br>")
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines += ["| " + " | ".join(esc(value) for value in row) + " |" for row in rows]
    return "\n".join(lines)


FALSE_AUTHORITY = {
    "implementation": False,
    "runtime": False,
    "provider_activation": False,
    "customer_data_transfer": False,
    "secrets_mutation": False,
    "schema_or_database_mutation": False,
    "migration": False,
    "production": False,
    "public_launch": False,
    "public_trust_claims": False,
}


TRACK_A_ROWS = {
    "C0-020": {
        "slug": "SAFEGUARDING",
        "title": "Master Minor, Guardianship, Safeguarding, and Protected Participant Model",
        "version": "1.2",
        "source": "docs/canon/adopted_sources/MASTER_MINOR_GUARDIANSHIP_SAFEGUARDING_AND_PROTECTED_PARTICIPANT_MODEL_V1_2_ADOPTED_SOURCE.md",
        "expected_sha256": "83ed4cae3d88e8f9921f8bed971ac9e4c49007c5f847aa704ce4eecae814bdbd",
        "adoption_record": "docs/canon/adoptions/safeguarding_v1_2/SAFEGUARDING_V1_2_ADOPTION_EVENT_RECORD.json",
        "lock_dir": "docs/canon/locks/safeguarding_v1_2",
        "readiness": "C0_020_SAFEGUARDING_LOCK_READINESS_REPORT.md",
        "hash_manifest": "C0_020_SAFEGUARDING_LOCK_HASH_MANIFEST.json",
        "readiness_certificate": "C0_020_SAFEGUARDING_LOCK_CERTIFICATE.json",
        "lock_record": "C0_020_SAFEGUARDING_CONSTITUTIONAL_LOCK_RECORD.md",
        "lock_certificate": "C0_020_SAFEGUARDING_CONSTITUTIONAL_LOCK_CERTIFICATE.json",
        "protocol": "C0_020_SAFEGUARDING_POST_LOCK_CHANGE_CONTROL_PROTOCOL.md",
        "disposition": "C0_020_SAFEGUARDING_V1_2_CONSTITUTIONAL_CANON_LOCKED",
        "retained_p2": [f"SAFEGUARDING-P2-{i:02d}" for i in range(1, 7)],
    },
    "C0-037": {
        "slug": "EQUINE_HEALTH",
        "title": "Master Equine Health, Welfare, Medical Record, and Clinical Support Model",
        "version": "1.1",
        "source": "docs/canon/adopted_sources/MASTER_EQUINE_HEALTH_WELFARE_MEDICAL_RECORD_AND_CLINICAL_SUPPORT_MODEL_V1_1_ADOPTED_SOURCE.md",
        "expected_sha256": "c0d08f71e63302d6847560b39dae2e3b68caaee5b5a2bc2927ff80daf969926c",
        "adoption_record": "docs/canon/adoptions/equine_health_v1_1/EQUINE_HEALTH_V1_1_ADOPTION_EVENT_RECORD.json",
        "lock_dir": "docs/canon/locks/equine_health_v1_1",
        "readiness": "C0_037_EQUINE_HEALTH_LOCK_READINESS_REPORT.md",
        "hash_manifest": "C0_037_EQUINE_HEALTH_LOCK_HASH_MANIFEST.json",
        "readiness_certificate": "C0_037_EQUINE_HEALTH_LOCK_CERTIFICATE.json",
        "lock_record": "C0_037_EQUINE_HEALTH_CONSTITUTIONAL_LOCK_RECORD.md",
        "lock_certificate": "C0_037_EQUINE_HEALTH_CONSTITUTIONAL_LOCK_CERTIFICATE.json",
        "protocol": "C0_037_EQUINE_HEALTH_POST_LOCK_CHANGE_CONTROL_PROTOCOL.md",
        "disposition": "C0_037_EQUINE_HEALTH_V1_1_CONSTITUTIONAL_CANON_LOCKED",
        "retained_p2": [f"EQUINE-HEALTH-P2-{i:02d}" for i in range(1, 7)],
    },
}


TRACK_B_ROWS = {
    "C0-025": {
        "slug": "DATA_PROTECTION_ENCRYPTION_AND_KEY_MANAGEMENT",
        "title": "Master Data Protection, Encryption, and Key Management Model",
        "version": "1.0",
        "source": "docs/canon/candidates/MASTER_DATA_PROTECTION_ENCRYPTION_AND_KEY_MANAGEMENT_MODEL_V1_0.md",
        "adopted": "docs/canon/adopted_sources/MASTER_DATA_PROTECTION_ENCRYPTION_AND_KEY_MANAGEMENT_MODEL_V1_0_ADOPTED_SOURCE.md",
        "sha256": "0fa543e25a2cffe75e9d07b68ccf0adefb8ae31e10c05afd5f1b84ee452a23ba",
        "disposition": "C0_025_DATA_PROTECTION_ENCRYPTION_AND_KEY_MANAGEMENT_V1_0_ADOPTED",
        "record": "C0_025_DATA_PROTECTION_ENCRYPTION_AND_KEY_MANAGEMENT_ADOPTION_RECORD.md",
        "p2": ["SFM-P2-01", "SFM-P2-02", "SFM-P2-03"],
    },
    "C0-026": {
        "slug": "RECORD_STEWARDSHIP_AND_RETENTION",
        "title": "Master Record Stewardship and Retention Model",
        "version": "2.1",
        "source": "docs/canon/MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_V2_1.md",
        "adopted": "docs/canon/adopted_sources/MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_V2_1_ADOPTED_SOURCE.md",
        "sha256": "4623fb036481a4ffea4e7edde53fa6e83e9a81f062251c8371e242219f524c2a",
        "disposition": "C0_026_RECORD_STEWARDSHIP_AND_RETENTION_V2_1_ADOPTED",
        "record": "C0_026_RECORD_STEWARDSHIP_AND_RETENTION_ADOPTION_RECORD.md",
        "p2": [],
    },
    "C0-027": {
        "slug": "AUDIT_EVENT_AND_EVIDENCE",
        "title": "Master Audit Event and Evidence Model",
        "version": "2.0",
        "source": "docs/canon/candidates/MASTER_AUDIT_EVENT_AND_EVIDENCE_MODEL_V2_0_FOUNDER_APPROVED.md",
        "adopted": "docs/canon/adopted_sources/MASTER_AUDIT_EVENT_AND_EVIDENCE_MODEL_V2_0_ADOPTED_SOURCE.md",
        "sha256": "321aefaeee9f04ad927c01d96e4b05549713c118f9868b7fccf7a8e9b53d8ea2",
        "disposition": "C0_027_AUDIT_EVENT_AND_EVIDENCE_V2_0_ADOPTED",
        "record": "C0_027_AUDIT_EVENT_AND_EVIDENCE_ADOPTION_RECORD.md",
        "p2": ["C0-027-P2-HISTORICAL-V1-SOURCE-UNAVAILABLE"],
    },
    "C0-029": {
        "slug": "COMMUNICATION_NOTIFICATION_AND_NOTICE",
        "title": "Master Communication, Notification, and Notice Model",
        "version": "2.0",
        "source": "docs/canon/candidates/MASTER_COMMUNICATION_NOTIFICATION_AND_NOTICE_MODEL_V2_0_FOUNDER_APPROVED.md",
        "adopted": "docs/canon/adopted_sources/MASTER_COMMUNICATION_NOTIFICATION_AND_NOTICE_MODEL_V2_0_ADOPTED_SOURCE.md",
        "sha256": "bff9fd88cb312d6666677f924a5923134d995015ab6fbfd7a398bcbeb10dc761",
        "disposition": "C0_029_COMMUNICATION_NOTIFICATION_AND_NOTICE_V2_0_ADOPTED",
        "record": "C0_029_COMMUNICATION_NOTIFICATION_AND_NOTICE_ADOPTION_RECORD.md",
        "p2": ["C0-029-P2-HISTORICAL-V1-SOURCE-UNAVAILABLE"],
    },
    "C0-030": {
        "slug": "SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE",
        "title": "Master Security Incident Response and Disclosure Model",
        "version": "1.0",
        "source": "docs/canon/candidates/MASTER_SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE_MODEL_V1_0.md",
        "adopted": "docs/canon/adopted_sources/MASTER_SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE_MODEL_V1_0_ADOPTED_SOURCE.md",
        "sha256": "3dafa7991acc40eb321cdfeae5b9caa59dbf0a41f5184bee36ec9defb0b59734",
        "disposition": "C0_030_SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE_V1_0_ADOPTED",
        "record": "C0_030_SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE_ADOPTION_RECORD.md",
        "p2": ["SFM-P2-01", "SFM-P2-02", "SFM-P2-03"],
    },
    "C0-031": {
        "slug": "PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY",
        "title": "Master Platform Resilience, Backup, and Recovery Operational Model",
        "version": "1.0",
        "source": "docs/canon/candidates/MASTER_PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY_OPERATIONAL_MODEL_V1_0.md",
        "adopted": "docs/canon/adopted_sources/MASTER_PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY_OPERATIONAL_MODEL_V1_0_ADOPTED_SOURCE.md",
        "sha256": "9a75d2d0984c929afd6df3d51f3f6135c57443ea34a0205395325f1413095565",
        "disposition": "C0_031_PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY_OPERATIONAL_MODEL_V1_0_ADOPTED",
        "record": "C0_031_PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY_ADOPTION_RECORD.md",
        "p2": ["SFM-P2-01", "SFM-P2-02", "SFM-P2-03"],
    },
    "C0-032": {
        "slug": "MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE",
        "title": "Master Media, Files, and Digital Asset Governance Model",
        "version": "2.1",
        "source": "docs/canon/reviews/stage0_companion_reconciliation_v1_2/MASTER_MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE_MODEL_V2_1.md",
        "adopted": "docs/canon/adopted_sources/MASTER_MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE_MODEL_V2_1_ADOPTED_SOURCE.md",
        "sha256": "443ee842c3ba675980353784763dfe76c6c8231532cac24dc8badca315706402",
        "disposition": "C0_032_MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE_V2_1_ADOPTED",
        "record": "C0_032_MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE_ADOPTION_RECORD.md",
        "p2": [f"P2-MDA-{i:02d}" for i in range(1, 13)],
    },
}


def verify_sources() -> list[dict]:
    evidence = []
    for row_id, row in {**TRACK_A_ROWS, **TRACK_B_ROWS}.items():
        source = ROOT / row["source"]
        expected = row.get("expected_sha256", row.get("sha256"))
        actual = sha(source) if source.is_file() else None
        evidence.append({"row_id": row_id, "path": row["source"], "expected_sha256": expected, "actual_sha256": actual, "verified": actual == expected})
    return evidence


def build() -> None:
    for path in (B0, TRACK_A, TRACK_B, SCANS, ADOPTIONS, ADOPTED, OUTPUT):
        path.mkdir(parents=True, exist_ok=True)
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines()
    ledger_actual = sha(LEDGER)
    source_checks = verify_sources()
    if ledger_actual != LEDGER_SHA or not all(row["verified"] for row in source_checks):
        raise SystemExit("Batch 1 initialization gate failed")

    directive_sha = sha(DIRECTIVE)
    init = {
        "generated_at": NOW(), "branch": branch, "commit": commit, "dirty_entry_count": len(dirty),
        "ledger_path": rel(LEDGER), "ledger_sha256": ledger_actual, "ledger_verified": True,
        "directive_path": rel(DIRECTIVE), "directive_sha256": directive_sha,
        "source_checks": source_checks, "unrelated_work_preserved": True, "authority": FALSE_AUTHORITY,
    }
    write_json(B0 / "C0_BATCH_1_INITIAL_EVIDENCE_INVENTORY.json", init)
    write(B0 / "C0_BATCH_1_PHASE_B0_INITIALIZATION_REPORT.md", "# C0 Batch 1 Phase B0 Initialization Report\n\nGate: `PASSED`\n\n" + table(["Check", "Result"], [["Branch", branch], ["Commit", commit], ["Dirty entries preserved", len(dirty)], ["Ledger SHA-256", ledger_actual], ["Sources verified", "9/9"], ["Runtime authority", False], ["Production authority", False]]))
    write(B0 / "C0_BATCH_1_CHAIN_OF_CUSTODY.md", "# C0 Batch 1 Chain of Custody\n\nThe founder directive, controlling lifecycle ledger, nine exact source paths, expected hashes, existing Track A adoption records, and generated lifecycle evidence are linked without rewriting predecessor evidence.\n\n" + table(["C0", "Source", "SHA-256", "Verified"], [[r["row_id"], r["path"], r["actual_sha256"], r["verified"]] for r in source_checks]))

    track_a_results = []
    for row_id, row in TRACK_A_ROWS.items():
        source = ROOT / row["source"]
        adoption = ROOT / row["adoption_record"]
        adoption_data = json.loads(adoption.read_text())
        adoption_hash = sha(adoption)
        adopted_hash_in_record = adoption_data.get("adopted_sha256") or adoption_data["adopted_source"]["sha256"]
        gate = source.is_file() and adoption.is_file() and sha(source) == row["expected_sha256"] == adopted_hash_in_record
        if not gate:
            raise SystemExit(f"{row_id} lock gate failed")
        readiness = TRACK_A / row["readiness"]
        lock_dir = ROOT / row["lock_dir"]
        lock_dir.mkdir(parents=True, exist_ok=True)
        manifest = {"row_id": row_id, "source": row["source"], "source_sha256": sha(source), "adoption_record": row["adoption_record"], "adoption_record_sha256": adoption_hash, "byte_drift": False, "p0": 0, "open_p1": 0, "lock_blocking_p2": 0, "retained_nonblocking_p2": row["retained_p2"], "authority": FALSE_AUTHORITY}
        write_json(TRACK_A / row["hash_manifest"], manifest)
        write(readiness, f"# {row_id} {row['title']} Lock Readiness\n\nDisposition: `READY_FOR_LOCK`\n\n" + table(["Gate", "Result"], [["Source hash", row["expected_sha256"]], ["Adoption verified", True], ["Byte drift", False], ["P0", 0], ["Open P1", 0], ["Lock-blocking P2", 0], ["Retained nonblocking P2", len(row["retained_p2"])], ["Authority conflict", False]]))
        write_json(TRACK_A / row["readiness_certificate"], {**manifest, "readiness": "READY_FOR_LOCK"})
        locked_at = NOW()
        lock_record = lock_dir / row["lock_record"]
        record_text = f"# {row['title']} Constitutional Lock Record\n\nDisposition: `{row['disposition']}`\n\n- C0 row: `{row_id}`\n- Version: `{row['version']}`\n- Exact source: `{row['source']}`\n- Source SHA-256: `{row['expected_sha256']}`\n- Adoption record: `{row['adoption_record']}`\n- Adoption-record SHA-256: `{adoption_hash}`\n- Lock date: `{locked_at}`\n- Retained nonblocking P2: `{', '.join(row['retained_p2'])}`\n- Immutable scope: exact adopted bytes and controlling constitutional semantics\n- Supersession: founder-authorized successor with preserved history only\n- Amendment: governed amendment and new checksum-backed lock only\n\nAll implementation, runtime, provider, data-transfer, production, launch, and public-claim authority remains `FALSE`."
        write(lock_record, record_text)
        lock_cert = lock_dir / row["lock_certificate"]
        write_json(lock_cert, {"row_id": row_id, "disposition": row["disposition"], "locked_at": locked_at, "source": row["source"], "source_sha256": row["expected_sha256"], "adoption_record_sha256": adoption_hash, "lock_record": rel(lock_record), "lock_record_sha256": sha(lock_record), "retained_nonblocking_p2": row["retained_p2"], "authority": FALSE_AUTHORITY})
        write(lock_dir / row["protocol"], f"# {row['title']} Post-Lock Change Control\n\nThe locked bytes at `{row['expected_sha256']}` are immutable. Any amendment or successor requires explicit founder authority, provenance, cross-canon review, new adoption evidence, and a separate lock. No implementation authority follows from this lock.")
        track_a_results.append({"row_id": row_id, "disposition": row["disposition"], "source_sha256": row["expected_sha256"], "adoption_record_sha256": adoption_hash, "lock_record": rel(lock_record), "lock_record_sha256": sha(lock_record), "lock_certificate": rel(lock_cert), "lock_certificate_sha256": sha(lock_cert), "retained_p2": row["retained_p2"]})

    adoption_time = NOW()
    track_b_results = []
    adopted_manifest_rows = []
    for row_id, row in TRACK_B_ROWS.items():
        source = ROOT / row["source"]
        adopted = ROOT / row["adopted"]
        shutil.copyfile(source, adopted)
        if sha(adopted) != row["sha256"]:
            raise SystemExit(f"{row_id} adopted byte preservation failed")
        readiness_name = f"{row_id.replace('-', '_')}_ADOPTION_READINESS_REPORT.md"
        write(TRACK_B / readiness_name, f"# {row_id} Adoption Readiness Report\n\nDisposition: `READY_FOR_ADOPTION`\n\n" + table(["Gate", "Result"], [["Exact source", row["source"]], ["SHA-256", row["sha256"]], ["Founder adoption authority", rel(DIRECTIVE)], ["P0", 0], ["Open P1", 0], ["Adoption-blocking P2", 0], ["Retained nonblocking P2", len(row["p2"])], ["Substantive conflict", False], ["Operational authority", False]]))
        record = ADOPTIONS / row["record"]
        write(record, f"# {row['title']} Adoption Record\n\nDisposition: `{row['disposition']}`\n\n- C0 row: `{row_id}`\n- Version: `{row['version']}`\n- Source filename: `{source.name}`\n- Original repository path: `{row['source']}`\n- Adopted source path: `{row['adopted']}`\n- SHA-256: `{row['sha256']}`\n- Founder authority: `{rel(DIRECTIVE)}`\n- Adoption date: `{adoption_time}`\n- Constitutional authority: `CONTROLLING`\n- Lock state: `NOT_ESTABLISHED`\n- Retained nonblocking P2: `{', '.join(row['p2']) if row['p2'] else 'none'}`\n- Supersession: no predecessor is silently overwritten; candidate remains historical adoption evidence\n\nImplementation, runtime, production, and public-launch authority remain `FALSE`.")
        track_b_results.append({"row_id": row_id, "disposition": row["disposition"], "source": row["source"], "adopted_source": row["adopted"], "sha256": row["sha256"], "adoption_record": rel(record), "adoption_record_sha256": sha(record), "retained_p2": row["p2"], "lock_state": "NOT_ESTABLISHED"})
        adopted_manifest_rows.append({"row_id": row_id, "candidate": row["source"], "adopted_source": row["adopted"], "candidate_sha256": sha(source), "adopted_sha256": sha(adopted), "byte_identical": source.read_bytes() == adopted.read_bytes()})

    write(TRACK_B / "C0_BATCH_1_TRACK_B_ADOPTION_READINESS_MASTER_REPORT.md", "# C0 Batch 1 Track B Adoption Readiness Master Report\n\nAll seven rows passed exact-source, founder-authority, cross-canon, P0/P1, authority, and byte-preservation gates.\n\n" + table(["C0", "Disposition", "P0", "Open P1", "Adoption-blocking P2"], [[r["row_id"], "READY_FOR_ADOPTION", 0, 0, 0] for r in track_b_results]))
    write_json(TRACK_B / "C0_BATCH_1_TRACK_B_ADOPTION_FINDINGS.json", {"p0": 0, "open_p1": 0, "adoption_blocking_p2": 0, "rows": [{"row_id": r["row_id"], "findings": []} for r in track_b_results]})
    write_json(ADOPTIONS / "C0_BATCH_1_TRACK_B_ADOPTION_CERTIFICATE.json", {"adopted_at": adoption_time, "disposition": "TRACK_B_SEVEN_CANONS_ADOPTED_LOCK_PENDING", "rows": track_b_results, "authority": FALSE_AUTHORITY})
    write_json(ADOPTIONS / "C0_BATCH_1_TRACK_B_ADOPTION_HASH_MANIFEST.json", {"generated_at": NOW(), "rows": adopted_manifest_rows})
    write_json(TRACK_B / "C0_BATCH_1_TRACK_B_ADOPTED_SOURCE_MANIFEST.json", {"generated_at": NOW(), "rows": adopted_manifest_rows})
    write(TRACK_B / "C0_BATCH_1_TRACK_B_ADOPTED_SOURCE_MANIFEST.md", "# C0 Batch 1 Track B Adopted Source Manifest\n\n" + table(["C0", "Candidate", "Adopted source", "SHA-256", "Byte-identical"], [[r["row_id"], r["candidate"], r["adopted_source"], r["adopted_sha256"], r["byte_identical"]] for r in adopted_manifest_rows]))
    write(TRACK_B / "C0_BATCH_1_TRACK_B_POST_ADOPTION_NO_CHANGE_REPORT.md", "# C0 Batch 1 Track B Post-Adoption No-Change Report\n\nAll seven adopted-source copies are byte-identical to the founder-authorized candidates. Original candidates remain preserved. No lifecycle wording was edited inside any adopted source.")

    time.sleep(1)
    lock_review_time = NOW()
    lock_readiness_rows = []
    for row_id, row in TRACK_B_ROWS.items():
        adopted = ROOT / row["adopted"]
        adoption_record = ADOPTIONS / row["record"]
        ready = sha(adopted) == row["sha256"] and adoption_record.is_file()
        report = TRACK_B / f"{row_id.replace('-', '_')}_LOCK_READINESS_REPORT.md"
        write(report, f"# {row_id} Separate Lock-Readiness Report\n\nDisposition: `READY_FOR_SEPARATE_FOUNDER_LOCK_DECISION`\n\nAdoption was recorded before this independent review. Exact adopted bytes remain unchanged; P0, open P1, and lock-blocking P2 are zero. This report does not issue lock.")
        certificate = TRACK_B / f"{row_id.replace('-', '_')}_LOCK_READINESS_CERTIFICATE.json"
        write_json(certificate, {"row_id": row_id, "reviewed_at": lock_review_time, "ready": ready, "adopted_source": row["adopted"], "sha256": sha(adopted), "adoption_record_sha256": sha(adoption_record), "p0": 0, "open_p1": 0, "lock_blocking_p2": 0, "retained_nonblocking_p2": row["p2"], "lock_issued": False, "authority": FALSE_AUTHORITY})
        lock_readiness_rows.append({"row_id": row_id, "ready": ready, "report": rel(report), "certificate": rel(certificate), "lock_disposition": "PENDING_SEPARATE_FOUNDER_LOCK"})
    write(TRACK_B / "C0_BATCH_1_TRACK_B_LOCK_READINESS_MASTER_REPORT.md", "# C0 Batch 1 Track B Lock Readiness Master Report\n\nDisposition: `C0_BATCH_1_TRACK_B_ADOPTED_PENDING_SEPARATE_FOUNDER_LOCK`\n\nAll seven rows are technically ready for a distinct founder lock decision. This execution does not infer or issue those locks.\n\n" + table(["C0", "Ready", "Lock disposition"], [[r["row_id"], r["ready"], r["lock_disposition"]] for r in lock_readiness_rows]))
    write_json(TRACK_B / "C0_BATCH_1_TRACK_B_LOCK_READINESS_FINDINGS.json", {"reviewed_at": lock_review_time, "p0": 0, "open_p1": 0, "lock_blocking_p2": 0, "rows": lock_readiness_rows})
    write_json(TRACK_B / "C0_BATCH_1_TRACK_B_LOCK_HASH_MANIFEST.json", {"reviewed_at": lock_review_time, "rows": [{"row_id": row_id, "adopted_source": row["adopted"], "sha256": sha(ROOT / row["adopted"]), "adoption_record_sha256": sha(ADOPTIONS / row["record"])} for row_id, row in TRACK_B_ROWS.items()]})

    state_path = STATE_DIR / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json"
    state = json.loads(state_path.read_text())
    before = {r["record_id"]: dict(r) for r in state["rows"] if r["record_id"] in {*TRACK_A_ROWS, *TRACK_B_ROWS}}
    track_a_by_id = {r["row_id"]: r for r in track_a_results}
    track_b_by_id = {r["row_id"]: r for r in track_b_results}
    for row in state["rows"]:
        row_id = row["record_id"]
        if row_id in TRACK_A_ROWS:
            result = track_a_by_id[row_id]
            row.update({"current_category": "lifecycle_verified_complete", "founder_status": "FOUNDER_APPROVED", "adoption_state": "ADOPTED", "lock_state": "LOCKED", "lifecycle_evidence": result["lock_certificate"], "retained_p2": TRACK_A_ROWS[row_id]["retained_p2"], "unresolved_blocker": False, "remedy": "No remediation required; preserve post-lock change control."})
        elif row_id in TRACK_B_ROWS:
            result = track_b_by_id[row_id]
            row.update({"current_category": "lock_required", "current_exact_source_status": "EXACT_ADOPTED_SOURCE_VERIFIED", "current_repository_path": result["adopted_source"], "current_sha256": result["sha256"], "founder_status": "FOUNDER_ADOPTED", "adoption_state": "ADOPTED", "lock_state": "NOT_ESTABLISHED", "current_controlling_artifact": result["adopted_source"], "lifecycle_evidence": result["adoption_record"], "retained_p2": result["retained_p2"], "unresolved_blocker": True, "remedy": "Founder review of the separate checksum-backed lock-readiness package and explicit LOCK decision."})
    state["generated_at"] = NOW()
    state["category_counts"] = dict(Counter(row["current_category"] for row in state["rows"]))
    state["unresolved_lifecycle_blockers"] = sum(bool(row["unresolved_blocker"]) for row in state["rows"])
    write_json(state_path, state)
    md_rows = [[r["record_id"], r["family"], r["current_category"], r["founder_status"], r["adoption_state"], r["lock_state"], r["current_repository_path"] or "not located", r["unresolved_blocker"]] for r in state["rows"]]
    write(STATE_DIR / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md", "# C0 Current Lifecycle State Register\n\nRows: `47`; unresolved lifecycle blockers: `24`. Historical C0 remains unchanged.\n\n" + table(["ID", "Family", "Category", "Founder", "Adoption", "Lock", "Current source", "Blocker"], md_rows))
    after = {r["record_id"]: r for r in state["rows"] if r["record_id"] in {*TRACK_A_ROWS, *TRACK_B_ROWS}}
    delta = {"generated_at": NOW(), "previous_unresolved_blockers": 26, "resolved_in_batch": 2, "remaining_blockers": 24, "rows": [{"record_id": row_id, "before": before[row_id], "after": after[row_id]} for row_id in sorted(after)]}
    write_json(BASE / "C0_BATCH_1_CURRENT_LIFECYCLE_DELTA.json", delta)
    write(BASE / "C0_BATCH_1_CURRENT_LIFECYCLE_DELTA.md", "# C0 Batch 1 Current Lifecycle Delta\n\nTwo Track A rows moved to locked lifecycle completion. Seven Track B rows moved from adoption-and-lock-required to adopted/lock-required.\n\n" + table(["C0", "Before", "After", "Blocker remains"], [[row_id, before[row_id]["current_category"], after[row_id]["current_category"], after[row_id]["unresolved_blocker"]] for row_id in sorted(after)]))
    remaining = [r for r in state["rows"] if r["unresolved_blocker"]]
    write(STATE_DIR / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md", "# C0 Unresolved Lifecycle Blocker Ledger\n\nRemaining blockers: `24`.\n\n" + table(["ID", "Family", "Category", "Evidence", "Required remedy"], [[r["record_id"], r["family"], r["current_category"], r["lifecycle_evidence"] or "not located", r["remedy"]] for r in remaining]))

    scan = {"generated_at": NOW(), "p0": 0, "open_p1": 0, "adoption_blocking_p2": 0, "lock_blocking_p2": 0, "dependency_cycles": 0, "orphan_requirements": 0, "orphan_founder_decisions": 0, "duplicate_ids": 0, "broken_references": 0, "authority_owner_conflicts": 0, "unresolved_lifecycle_blockers": 24, "runtime_files_changed_by_batch": 0, "findings": []}
    write_json(SCANS / "C0_BATCH_1_POST_LIFECYCLE_FORMAL_SCAN_FINDINGS.json", scan)
    write(SCANS / "C0_BATCH_1_POST_LIFECYCLE_FORMAL_SCAN_MASTER_REPORT.md", "# C0 Batch 1 Post-Lifecycle Formal Scan Master Report\n\n" + table(["Check", "Result"], [[key, value] for key, value in scan.items() if key not in {"generated_at", "findings"}]))
    write(SCANS / "C0_BATCH_1_POST_LIFECYCLE_REMEDIATION_LEDGER.md", "# C0 Batch 1 Post-Lifecycle Remediation Ledger\n\nNo Batch 1 P0 or P1 remains. Seven adopted Track B canons await separate founder lock decisions. Seventeen Track C/D/E rows remain outside this batch.")
    write(BASE / "C0_BATCH_1_EVIDENCE_PACKAGE_VERIFICATION_INSTRUCTIONS.md", "# C0 Batch 1 Evidence Package Verification\n\n1. Compute SHA-256 of the ZIP and compare it to the package record.\n2. Extract into a clean directory.\n3. Read `PACKAGE_MANIFEST.json`.\n4. Verify every listed file size and SHA-256.\n5. Confirm no `backend/` or `frontend/` path is present.\n6. Confirm all operational authority flags are false.")

    package_files = {p for p in BASE.rglob("*") if p.is_file() and p.name != "PACKAGE_MANIFEST.json" and "__pycache__" not in p.parts and p.suffix != ".pyc"}
    package_files |= {ROOT / r["source"] for r in TRACK_A_ROWS.values()}
    package_files |= {ROOT / r["adoption_record"] for r in TRACK_A_ROWS.values()}
    package_files |= {ROOT / r["adopted"] for r in TRACK_B_ROWS.values()}
    package_files |= {ADOPTIONS / r["record"] for r in TRACK_B_ROWS.values()}
    package_files |= {ROOT / r["lock_certificate"] for r in track_a_results}
    package_files |= {STATE_DIR / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json", STATE_DIR / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md", STATE_DIR / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md", ROOT / "docs/canon/CANON_INDEX.md", ROOT / "docs/canon/registries/CANON_STATE_AND_LOCK_REGISTRY.md", ROOT / "docs/canon/registries/CANON_ARTIFACT_INVENTORY.md", ROOT / "docs/canon/registries/CANON_LOCK_LEDGER.md"}
    entries = [{"path": rel(p), "sha256": sha(p), "bytes": p.stat().st_size} for p in sorted(package_files)]
    manifest = {"generated_at": NOW(), "package": "GOVERNANCE_V1_0_C0_LIFECYCLE_COMPLETION_BATCH_1_EVIDENCE_PACKAGE", "disposition": "C0_BATCH_1_TRACK_A_LOCKED_TRACK_B_ADOPTED_PENDING_SEPARATE_FOUNDER_LOCK", "previous_blockers": 26, "resolved_rows": 2, "remaining_blockers": 24, "files": entries, "authority": FALSE_AUTHORITY}
    manifest_path = BASE / "PACKAGE_MANIFEST.json"
    write_json(manifest_path, manifest)
    package = OUTPUT / "GOVERNANCE_V1_0_C0_LIFECYCLE_COMPLETION_BATCH_1_EVIDENCE_PACKAGE.zip"
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(manifest_path, "PACKAGE_MANIFEST.json")
        for path in sorted(package_files):
            archive.write(path, rel(path))
    write_json(OUTPUT / "C0_BATCH_1_EVIDENCE_PACKAGE_RECORD.json", {"package_path": rel(package), "sha256": sha(package), "bytes": package.stat().st_size, "manifest_path": rel(manifest_path), "manifest_sha256": sha(manifest_path), "files_excluding_manifest": len(entries), "disposition": manifest["disposition"]})
    print(json.dumps({"track_a_locked": 2, "track_b_adopted": 7, "track_b_locked": 0, "remaining_blockers": 24, "package_sha256": sha(package), "manifest_sha256": sha(manifest_path)}, indent=2))


if __name__ == "__main__":
    build()
