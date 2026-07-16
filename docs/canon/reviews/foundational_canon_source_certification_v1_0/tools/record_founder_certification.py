#!/usr/bin/env python3
"""Preserve and record the July 2026 foundational-canon source certification."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
ROOT = REPO / "docs/canon/reviews/foundational_canon_source_certification_v1_0"
SOURCE = ROOT / "source_event"
ARCHIVE = Path("/Users/rianray/Downloads/EquineSync_Six_Foundational_Canon_Reviewed_Candidates.zip")
BUSINESS = Path("/Users/rianray/Downloads/MASTER_BUSINESS_LIFECYCLE (2).md")
CLAIMS = Path("/Users/rianray/Downloads/MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0 (1).md")
ARCHIVE_HASH = "eb6a73c71fbc666b25790ab13067eba858575a0ab98b22c0e7cd561c218c949b"
BUSINESS_HASH = "063339ec8b8aab20908742675013692de2dbb56f018939bac71371b8366d2466"
CLAIMS_HASH = "a4787fb641dca1d28d98f10240957d0b09ea8ee1cee8358f64e80dd658b8b626"

ROWS = {
    "C0-005": ("Master Ecosystem Model", "MASTER_ECOSYSTEM_MODEL_V2_1_REVIEWED_CANDIDATE.md", "67175779abfe8ff2dee0ff7b1b8c06eee42943052071bbad1f65439c73696d07"),
    "C0-012": ("Master Horse Lifecycle and Passport Model", "MASTER_HORSE_LIFECYCLE_V3_1_REVIEWED_CANDIDATE.md", "41313d11aae592d041decaf34e5a131863423e843057d47864e666bdea21e6bf"),
    "C0-014": ("Master Facility Domain Model", "MASTER_FACILITY_DOMAIN_MODEL_V2_1_REVIEWED_CANDIDATE.md", "8323b8402c3d445fe2b8d363caf16bb2a8eb4e08b0b37bd36b90ee69092a698d"),
    "C0-015": ("Master Barn Lifecycle and Operations Canon", "MASTER_BARN_LIFECYCLE_V3_1_REVIEWED_CANDIDATE.md", "c2a698ca1bbb8dc723ea7ac0270a9f66e8b06d0cbcb01535efefc517b6076d4a"),
    "C0-016": ("Master Business Lifecycle Model", "MASTER_BUSINESS_LIFECYCLE_V2_1_REVIEWED_CANDIDATE.md", "a07b0ba2fc6c3c0ce5b9db3f56c5f26fcda8d87e5f4f115a02e19b6b5fb4b37d"),
    "C0-028": ("Master Claims, Disputes, and Authority Model", "MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0_FOUNDER_CERTIFIED_SOURCE.md", CLAIMS_HASH),
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=True))


def replace_row(path: Path, row_id: str, value: str) -> None:
    lines = path.read_text().splitlines()
    for index, line in enumerate(lines):
        if line.startswith(f"| {row_id} |"):
            lines[index] = value
            write_text(path, "\n".join(lines))
            return
    raise RuntimeError(f"Missing {row_id} in {path}")


def preserve() -> dict[str, str]:
    if sha(ARCHIVE) != ARCHIVE_HASH or sha(BUSINESS) != BUSINESS_HASH or sha(CLAIMS) != CLAIMS_HASH:
        raise RuntimeError("Founder attachment hash changed")
    SOURCE.mkdir(parents=True, exist_ok=True)
    archive_copy = SOURCE / ARCHIVE.name
    business_copy = SOURCE / "MASTER_BUSINESS_LIFECYCLE_V2_0_FOUNDER_CERTIFIED_CURRENT_SOURCE.md"
    claims_copy = SOURCE / "MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0_FOUNDER_CERTIFIED_SOURCE.md"
    for src, dst in ((ARCHIVE, archive_copy), (BUSINESS, business_copy), (CLAIMS, claims_copy)):
        shutil.copy2(src, dst)
        if sha(src) != sha(dst):
            raise RuntimeError(f"Copy mismatch: {dst}")
    extracted = SOURCE / "six_reviewed_candidates"
    extracted.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive_copy) as package:
        if package.testzip() is not None:
            raise RuntimeError("Archive integrity failure")
        package.extractall(extracted)
    for _, filename, expected in ROWS.values():
        path = claims_copy if filename.endswith("FOUNDER_CERTIFIED_SOURCE.md") else extracted / filename
        if sha(path) != expected:
            raise RuntimeError(f"Entry hash mismatch: {path}")
    if sha(REPO / "docs/canon/MASTER_BUSINESS_LIFECYCLE.md") != BUSINESS_HASH:
        raise RuntimeError("Business repository parity failure")
    recovered_claims = REPO / "docs/canon/reviews/governance_v1_0_c0_phase_c_hash_version_recovery/track_c/C0_028/recovered_sources/MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0_FOUNDER_SOURCE.md"
    if sha(recovered_claims) != CLAIMS_HASH:
        raise RuntimeError("Claims recovered-source parity failure")
    return {"archive": rel(archive_copy), "business": rel(business_copy), "claims": rel(claims_copy), "extracted": rel(extracted)}


def update_json_register(path: Path, collection: str, evidence: str) -> None:
    data = json.loads(path.read_text())
    for row in data[collection]:
        if row.get("record_id") not in ROWS:
            continue
        _, filename, expected = ROWS[row["record_id"]]
        candidate = SOURCE / filename if row["record_id"] == "C0-028" else SOURCE / "six_reviewed_candidates" / filename
        row.update({
            "current_category": "adoption_and_lock_required",
            "current_exact_source_status": "FOUNDER_CERTIFIED_CORRECT_VERSION_SOURCE_VERIFIED",
            "current_repository_path": rel(candidate),
            "current_sha256": expected,
            "founder_status": "FOUNDER_SOURCE_VERSION_CERTIFIED",
            "adoption_state": "PENDING_SEPARATE_FOUNDER_AUTHORIZATION",
            "lock_state": "PENDING_SEPARATE_FOUNDER_AUTHORIZATION",
            "supersession_state": "FOUNDER_CERTIFIED_SOURCE_PENDING_LIFECYCLE_DECISION",
            "lifecycle_evidence": evidence,
            "unresolved_blocker": True,
            "remedy": "Conduct separately authorized adoption review and constitutional lock review.",
        })
    if "category_counts" in data:
        counts = data["category_counts"]
        counts["unresolved_source_evidence"] -= len(ROWS)
        counts["adoption_and_lock_required"] = counts.get("adoption_and_lock_required", 0) + len(ROWS)
    data["status"] = "UPDATED_AFTER_FOUNDATIONAL_CANON_SOURCE_CERTIFICATION"
    data["generated_at"] = now()
    write_json(path, data)


def update_registers(evidence: str) -> None:
    batch = REPO / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1"
    lifecycle = REPO / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle"
    source_json = batch / "C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json"
    state_json = lifecycle / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json"
    update_json_register(source_json, "rows", evidence)
    update_json_register(state_json, "rows", evidence)

    source_md = batch / "C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.md"
    state_md = lifecycle / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md"
    for row_id, (family, filename, _) in ROWS.items():
        candidate = SOURCE / filename if row_id == "C0-028" else SOURCE / "six_reviewed_candidates" / filename
        replace_row(source_md, row_id, f"| {row_id} | {family} | adoption_and_lock_required | FOUNDER_CERTIFIED_CORRECT_VERSION_SOURCE_VERIFIED | FOUNDER_SOURCE_VERSION_CERTIFIED | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | `{rel(candidate)}` |")
        replace_row(state_md, row_id, f"| {row_id} | {family} | FOUNDER_CERTIFIED_CORRECT_VERSION_SOURCE_VERIFIED | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | `{evidence}` | True |")
    write_text(source_md, source_md.read_text().replace("Status: `UPDATED_AFTER_C0_019_CONSTITUTIONAL_LOCK`", "Status: `UPDATED_AFTER_FOUNDATIONAL_CANON_SOURCE_CERTIFICATION`"))

    ledger_json = lifecycle / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json"
    ledger = json.loads(ledger_json.read_text())
    for row in ledger["records"]:
        if row.get("record_id") in ROWS:
            row.update({
                "resolution_track": "TRACK_F_ADOPTION_AND_LOCK",
                "current_category": "adoption_and_lock_required",
                "founder_status": "FOUNDER_SOURCE_VERSION_CERTIFIED",
                "adoption_state": "PENDING_SEPARATE_FOUNDER_AUTHORIZATION",
                "lock_state": "PENDING_SEPARATE_FOUNDER_AUTHORIZATION",
                "next_step": "Conduct separately authorized adoption and lock lifecycle review.",
                "source_certification_evidence": evidence,
                "phase_c_status": "SUPERSEDED_BY_FOUNDER_SOURCE_CERTIFICATION",
                "phase_c_classification": "HISTORICAL_SOURCE_RECOVERY QUESTION_RESOLVED_BY_AUTHENTICATED_FOUNDER_SUCCESSOR_CERTIFICATION",
                "phase_c_recommendation": "PROCEED_TO_SEPARATELY_AUTHORIZED_ADOPTION_REVIEW",
            })
    ledger["track_counts"]["TRACK_C_HASH_OR_VERSION_RECOVERY"] -= len(ROWS)
    ledger["track_counts"]["TRACK_F_ADOPTION_AND_LOCK"] += len(ROWS)
    ledger["status"] = "UPDATED_AFTER_FOUNDATIONAL_CANON_SOURCE_CERTIFICATION"
    ledger["generated_at"] = now()
    write_json(ledger_json, ledger)

    ledger_md = lifecycle / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md"
    blocker_md = lifecycle / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md"
    for row_id, (family, filename, _) in ROWS.items():
        candidate = SOURCE / filename if row_id == "C0-028" else SOURCE / "six_reviewed_candidates" / filename
        replace_row(ledger_md, row_id, f"| {row_id} | TRACK_F_ADOPTION_AND_LOCK | adoption_and_lock_required | FOUNDER_SOURCE_VERSION_CERTIFIED | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | Conduct separately authorized adoption and lock lifecycle review. |")
        replace_row(blocker_md, row_id, f"| {row_id} | {family} | adoption_and_lock_required | FOUNDER_CERTIFIED_CORRECT_VERSION_SOURCE_VERIFIED | Conduct separately authorized adoption and lock lifecycle review using `{rel(candidate)}`. |")
    write_text(ledger_md, ledger_md.read_text().replace("Status: `UPDATED_AFTER_C0_019_CONSTITUTIONAL_LOCK`", "Status: `UPDATED_AFTER_FOUNDATIONAL_CANON_SOURCE_CERTIFICATION`"))


def main() -> None:
    paths = preserve()
    report = ROOT / "FOUNDATIONAL_CANON_FOUNDER_SOURCE_CERTIFICATION_RECORD.md"
    write_text(report, f"""# Foundational Canon Founder Source Certification Record

Disposition: `FOUNDER_CERTIFIED_PREVIOUSLY_ATTACHED_FILES_AS_CORRECT_VERSIONS`

Recorded: `{now()}`

## Certified source event

- Six-candidate package: `{paths['archive']}` / `{ARCHIVE_HASH}`
- Business V2.0 current source: `{paths['business']}` / `{BUSINESS_HASH}`
- Claims V2.0 founder source: `{paths['claims']}` / `{CLAIMS_HASH}`
- Extracted reviewed candidates: `{paths['extracted']}`

The six package documents are certified as the correct reviewed successor-candidate versions. The standalone Business V2.0 document is certified as the correct current predecessor source and remains byte-identical to `docs/canon/MASTER_BUSINESS_LIFECYCLE.md`. The standalone Claims V2.0 document is certified as the correct founder source and remains byte-identical to the recovered C0-028 source.

This certification resolves source-version identity for C0-005, C0-012, C0-014, C0-015, C0-016, and C0-028. It does not adopt or lock any document. The Analytics Framework is certified as a reviewed candidate without assigning a new C0 identifier.

All implementation, runtime, migration, provider, production, launch, certification-claim, and Governance V1 baseline authority remains `FALSE`.
""")
    update_registers(rel(report))
    artifacts = sorted(path for path in ROOT.rglob("*") if path.is_file())
    manifest = {rel(path): sha(path) for path in artifacts if path.name != "FOUNDATIONAL_CANON_SOURCE_CERTIFICATION_MANIFEST.json"}
    write_json(ROOT / "FOUNDATIONAL_CANON_SOURCE_CERTIFICATION_MANIFEST.json", {
        "disposition": "FOUNDER_CERTIFIED_PREVIOUSLY_ATTACHED_FILES_AS_CORRECT_VERSIONS",
        "files": manifest,
        "authority": {key: False for key in ("adoption", "lock", "implementation", "runtime", "migration", "provider_activation", "production", "public_launch", "governance_v1_baseline_adoption", "governance_v1_baseline_lock")},
    })
    print(json.dumps({"record": rel(report), "record_sha256": sha(report), "manifest_entries": len(manifest)}, indent=2))


if __name__ == "__main__":
    main()
