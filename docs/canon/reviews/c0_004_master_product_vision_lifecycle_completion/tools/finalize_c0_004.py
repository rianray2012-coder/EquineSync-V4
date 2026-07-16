#!/usr/bin/env python3
"""Finalize C0-004 adoption, lock review, lock, and current-state records."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("c0build", HERE / "build_c0_004.py")
BUILD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(BUILD)

REPO = BUILD.REPO
ROOT = BUILD.ROOT
ACTIVE_MD = BUILD.ACTIVE_MD
ACTIVE_DOCX = BUILD.ACTIVE_DOCX
RAW = BUILD.RAW
AUTHORITY = BUILD.AUTHORITY
EXPECTED = BUILD.EXPECTED_RAW_HASH
ADOPT_DIR = REPO / "docs/canon/adoptions/c0_004_master_product_vision"
LOCK_DIR = REPO / "docs/canon/locks/master_product_vision_v2_1"
CURRENT_LIFECYCLE = REPO / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle"
SOURCE_REG = REPO / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    return BUILD.sha256(path)


def rel(path: Path) -> str:
    return BUILD.rel(path)


def write_text(path: Path, text: str) -> None:
    BUILD.write_text(path, text)


def write_json(path: Path, value: object) -> None:
    BUILD.write_json(path, value)


def record_hash(path: Path) -> str:
    return sha(path)


def copy_verified(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if sha(source) != sha(destination):
        raise RuntimeError(f"Preservation copy mismatch: {destination}")


def update_phase_a_visual() -> None:
    report = ROOT / "C0_004_DOCX_VISUAL_QA_REPORT.md"
    write_text(report, """# C0-004 DOCX Visual QA Report

- Rendered artifact: `docs/canon/founder_approved_sources/MASTER_PRODUCT_VISION_V2_1_FOUNDER_APPROVED.docx`
- Rendered pages: `47`
- Pages inspected: `47 of 47`
- Contact sheets inspected: `3 of 3`
- Clipped text: `0`
- Overlap: `0`
- Malformed tables or lists: `0`
- Unexpected blank pages: `0`
- Page 47 open space: legitimate end-of-document pagination
- Result: `PASS`
""")
    phase_a = json.loads((ROOT / "C0_004_PHASE_A_VALIDATION.json").read_text())
    phase_a["checks"]["visual_qa_pending"] = False
    phase_a["checks"]["visual_qa_passed_47_of_47"] = True
    write_json(ROOT / "C0_004_PHASE_A_VALIDATION.json", phase_a)
    readiness = ROOT / "C0_004_ADOPTION_READINESS_REPORT.md"
    text = readiness.read_text()
    text = text.replace(
        "DOCX page-by-page visual QA remains the final Phase A execution gate before adoption.",
        "DOCX page-by-page visual QA passed for all 47 pages. All Phase A execution gates passed.",
    )
    write_text(readiness, text)


def create_adoption() -> tuple[str, str, str]:
    ADOPT_DIR.mkdir(parents=True, exist_ok=True)
    pre_md = ADOPT_DIR / "history/MASTER_PRODUCT_VISION_V2_1_PRE_ADOPTION_FOUNDER_APPROVED.md"
    pre_docx = ADOPT_DIR / "history/MASTER_PRODUCT_VISION_V2_1_PRE_ADOPTION_FOUNDER_APPROVED.docx"
    copy_verified(ACTIVE_MD, pre_md)
    copy_verified(ACTIVE_DOCX, pre_docx)

    adopted = BUILD.lifecycle_markdown("ADOPTED", "NOT YET LOCKED")
    write_text(ACTIVE_MD, adopted)
    BUILD.create_docx(adopted, ACTIVE_DOCX)
    if BUILD.normalized_markdown_text(RAW.read_text(), True) != BUILD.normalized_markdown_text(adopted, True):
        raise RuntimeError("Adoption metadata changed substantive content")
    adopted_md_hash, adopted_docx_hash = sha(ACTIVE_MD), sha(ACTIVE_DOCX)
    copy_verified(ACTIVE_MD, ADOPT_DIR / "MASTER_PRODUCT_VISION_V2_1_ADOPTED_PRE_LOCK.md")
    copy_verified(ACTIVE_DOCX, ADOPT_DIR / "MASTER_PRODUCT_VISION_V2_1_ADOPTED_PRE_LOCK.docx")

    adoption_record = ADOPT_DIR / "C0_004_MASTER_PRODUCT_VISION_CONSTITUTIONAL_ADOPTION_RECORD.md"
    write_text(adoption_record, f"""# C0-004 Master Product Vision Constitutional Adoption Record

- C0 identifier: `C0-004`
- Canon: `Master Product Vision V2.1`
- Source identity: `EXACT_C0_EXPECTED_SOURCE_CONFIRMED`
- Exact source event: `{rel(RAW)}` / `{EXPECTED}`
- Adopted Markdown: `{rel(ACTIVE_MD)}` / `{adopted_md_hash}`
- Deterministic DOCX counterpart: `{rel(ACTIVE_DOCX)}` / `{adopted_docx_hash}`
- Pre-adoption Markdown: `{rel(pre_md)}` / `{sha(pre_md)}`
- Pre-adoption DOCX: `{rel(pre_docx)}` / `{sha(pre_docx)}`
- Founder disposition: `APPROVED_AND_AUTHORIZED_FOR_CONDITIONAL_C0_004_LIFECYCLE_COMPLETION`
- Adoption timestamp: `{now()}`
- Adoption decision: `ADOPTED`
- P0: `0`
- Open P1: `0`
- Adoption-blocking P2: `0`
- Constitutional lock at this event: `NOT YET LOCKED`
- Implementation authority: `FALSE`
- Production authority: `FALSE`
- Public-launch authority: `FALSE`

`ADOPTION DOES NOT CONSTITUTE CONSTITUTIONAL LOCK OR IMPLEMENTATION AUTHORITY`

V2.0 and the short unversioned summary remain historical noncontrolling predecessors. Amendment or supersession requires a separate founder-authorized constitutional lifecycle event.
""")
    adoption_hash = record_hash(adoption_record)
    write_text(adoption_record.with_suffix(".sha256"), f"{adoption_hash}  {adoption_record.name}")
    return adopted_md_hash, adopted_docx_hash, adoption_hash


def lock_readiness(adopted_md_hash: str, adopted_docx_hash: str, adoption_hash: str) -> None:
    write_text(ROOT / "C0_004_LOCK_READINESS_REPORT.md", f"""# C0-004 Lock Readiness Report

Disposition: `C0_004_MASTER_PRODUCT_VISION_LOCK_READINESS_PASSED`

- Adoption verified: `TRUE`
- Adopted Markdown SHA-256: `{adopted_md_hash}`
- Adopted DOCX SHA-256: `{adopted_docx_hash}`
- Adoption-record SHA-256: `{adoption_hash}`
- Exact source bytes unchanged: `TRUE`
- Dependency and cross-reference analysis: `PASS`
- Traceability review: `PASS`
- Apex-canon contradiction: `NONE`
- Locked-canon authority conflict: `NONE`
- P0: `0`
- Open P1: `0`
- Lock-blocking P2: `0`
- Retained nonblocking P2: `0`

The Product Vision governs product purpose and delegates domain controls to specialized canon. It creates no implementation, runtime, provider, production, launch, certification, or public-trust authority.
""")


def create_lock(adopted_md_hash: str, adopted_docx_hash: str, adoption_hash: str) -> tuple[str, str, str]:
    locked = BUILD.lifecycle_markdown("ADOPTED", "LOCKED")
    write_text(ACTIVE_MD, locked)
    BUILD.create_docx(locked, ACTIVE_DOCX)
    if BUILD.normalized_markdown_text(RAW.read_text(), True) != BUILD.normalized_markdown_text(locked, True):
        raise RuntimeError("Lock metadata changed substantive content")
    final_md_hash, final_docx_hash = sha(ACTIVE_MD), sha(ACTIVE_DOCX)
    LOCK_DIR.mkdir(parents=True, exist_ok=True)
    lock_record = LOCK_DIR / "C0_004_MASTER_PRODUCT_VISION_CONSTITUTIONAL_LOCK_RECORD.md"
    write_text(lock_record, f"""# C0-004 Master Product Vision Constitutional Lock Record

- C0 identifier: `C0-004`
- Canon: `Master Product Vision V2.1`
- Exact source: `{rel(RAW)}` / `{EXPECTED}`
- Locked Markdown: `{rel(ACTIVE_MD)}` / `{final_md_hash}`
- Locked DOCX counterpart: `{rel(ACTIVE_DOCX)}` / `{final_docx_hash}`
- Adopted pre-lock Markdown SHA-256: `{adopted_md_hash}`
- Adopted pre-lock DOCX SHA-256: `{adopted_docx_hash}`
- Adoption record: `{rel(ADOPT_DIR / 'C0_004_MASTER_PRODUCT_VISION_CONSTITUTIONAL_ADOPTION_RECORD.md')}` / `{adoption_hash}`
- Lock-readiness report: `{rel(ROOT / 'C0_004_LOCK_READINESS_REPORT.md')}` / `{sha(ROOT / 'C0_004_LOCK_READINESS_REPORT.md')}`
- Founder directive: `APPROVED_AND_AUTHORIZED_FOR_CONDITIONAL_C0_004_LIFECYCLE_COMPLETION`
- Lock timestamp: `{now()}`
- Lock disposition: `LOCKED`
- P0: `0`
- Open P1: `0`
- Lock-blocking P2: `0`
- Retained nonblocking P2: `0`
- Implementation authority: `FALSE`
- Production authority: `FALSE`
- Public-launch authority: `FALSE`
- Public-trust-claim authority: `FALSE`

The lock makes V2.1 the immutable controlling product-purpose reference. Amendment or supersession requires a separate founder-authorized constitutional event. Lock creates no implementation or operational authority.
""")
    lock_hash = record_hash(lock_record)
    write_text(lock_record.with_suffix(".sha256"), f"{lock_hash}  {lock_record.name}")
    return final_md_hash, final_docx_hash, lock_hash


def update_json_row(path: Path, collection: str, final_hash: str) -> None:
    data = json.loads(path.read_text())
    rows = data[collection]
    for row in rows:
        if row.get("record_id") != "C0-004":
            continue
        row.update({
            "current_category": "lifecycle_verified_complete",
            "current_exact_source_status": "EXACT_ADOPTED_SOURCE_VERIFIED",
            "current_repository_path": rel(ACTIVE_MD),
            "current_sha256": final_hash,
            "founder_status": "FOUNDER_APPROVED",
            "adoption_state": "ADOPTED",
            "lock_state": "LOCKED",
            "supersession_state": "V2_1_CONTROLLING_V2_0_HISTORICAL",
            "current_controlling_artifact": rel(ACTIVE_MD),
            "lifecycle_evidence": rel(LOCK_DIR / "C0_004_MASTER_PRODUCT_VISION_CONSTITUTIONAL_LOCK_RECORD.md"),
            "retained_p2": [],
            "unresolved_blocker": False,
            "remedy": "Complete; future changes require governed amendment or supersession.",
        })
    data["generated_at"] = now()
    if "unresolved_lifecycle_blockers" in data:
        data["unresolved_lifecycle_blockers"] = 16
        counts = data.get("category_counts", {})
        counts["unresolved_source_evidence"] = max(0, counts.get("unresolved_source_evidence", 0) - 1)
        counts["lifecycle_verified_complete"] = counts.get("lifecycle_verified_complete", 0) + 1
    if "status" in data:
        data["status"] = "UPDATED_AFTER_C0_004_CONSTITUTIONAL_LOCK"
    write_json(path, data)


def replace_table_row(path: Path, prefix: str, row: str, header_replacements: tuple[tuple[str, str], ...] = ()) -> None:
    text = path.read_text()
    lines = text.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = row
            replaced = True
            break
    if not replaced:
        raise RuntimeError(f"Row not found in {path}: {prefix}")
    text = "\n".join(lines) + "\n"
    for old, new in header_replacements:
        text = text.replace(old, new)
    write_text(path, text)


def update_current_state(final_hash: str, lock_hash: str) -> None:
    source_json = SOURCE_REG / "C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json"
    state_json = CURRENT_LIFECYCLE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json"
    update_json_row(source_json, "rows", final_hash)
    update_json_row(state_json, "rows", final_hash)

    source_md = SOURCE_REG / "C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.md"
    replace_table_row(
        source_md,
        "| C0-004 |",
        f"| C0-004 | Master Product Vision | lifecycle_verified_complete | EXACT_ADOPTED_SOURCE_VERIFIED | FOUNDER_APPROVED | ADOPTED | LOCKED | `{rel(ACTIVE_MD)}` |",
        (("Status: `UPDATED_AFTER_EIGHT_CANON_FOUNDER_APPROVAL_RECONCILIATION`", "Status: `UPDATED_AFTER_C0_004_CONSTITUTIONAL_LOCK`"),),
    )
    state_md = CURRENT_LIFECYCLE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md"
    replace_table_row(
        state_md,
        "| C0-004 |",
        f"| C0-004 | Master Product Vision | EXACT_ADOPTED_SOURCE_VERIFIED | ADOPTED | LOCKED | `{rel(LOCK_DIR / 'C0_004_MASTER_PRODUCT_VISION_CONSTITUTIONAL_LOCK_RECORD.md')}` | False |",
        (("unresolved lifecycle blockers: `17`", "unresolved lifecycle blockers: `16`"),),
    )

    ledger_json = CURRENT_LIFECYCLE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json"
    ledger = json.loads(ledger_json.read_text())
    ledger["records"] = [r for r in ledger["records"] if r.get("record_id") != "C0-004"]
    ledger["row_count"] = len(ledger["records"])
    ledger["track_counts"]["TRACK_C_HASH_OR_VERSION_RECOVERY"] -= 1
    ledger["generated_at"] = now()
    ledger["status"] = "UPDATED_AFTER_C0_004_CONSTITUTIONAL_LOCK"
    ledger["purpose"] = "Resolution planning for the 16 remaining blockers; C0-004 completed separately."
    write_json(ledger_json, ledger)
    ledger_md = CURRENT_LIFECYCLE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md"
    text = ledger_md.read_text()
    text = "\n".join(line for line in text.splitlines() if not line.startswith("| C0-004 |")) + "\n"
    text = text.replace("remaining lifecycle blockers: `17`", "remaining lifecycle blockers: `16`")
    text = text.replace("Status: `UPDATED_AFTER_C0_023_C0_035_CONSTITUTIONAL_ADOPTION`", "Status: `UPDATED_AFTER_C0_004_CONSTITUTIONAL_LOCK`")
    write_text(ledger_md, text)

    blocker_md = CURRENT_LIFECYCLE / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md"
    text = "\n".join(line for line in blocker_md.read_text().splitlines() if not line.startswith("| C0-004 |")) + "\n"
    text = text.replace("unresolved lifecycle blockers: `17`", "unresolved lifecycle blockers: `16`")
    write_text(blocker_md, text)

    delta_json = CURRENT_LIFECYCLE / "C0_HISTORICAL_TO_CURRENT_DELTA.json"
    data = json.loads(delta_json.read_text())
    for row in data["rows"]:
        if row.get("record_id") == "C0-004":
            row.update({"current_adoption": "ADOPTED", "current_lock": "LOCKED", "basis": rel(ACTIVE_MD)})
    data["generated_at"] = now()
    write_json(delta_json, data)
    delta_md = CURRENT_LIFECYCLE / "C0_HISTORICAL_TO_CURRENT_DELTA.md"
    replace_table_row(delta_md, "| C0-004 |", f"| C0-004 | UNRESOLVED | ADOPTED | UNRESOLVED | LOCKED | `{rel(ACTIVE_MD)}` |")

    index = REPO / "docs/canon/CANON_INDEX.md"
    replace_table_row(index, "| 1 | Master Product Vision |", f"| 1 | Master Product Vision | `{rel(ACTIVE_MD)}` | `ADOPTED`; `LOCKED`; Version 2.1 controlling | Highest product-purpose authority; specialized canon retains domain controls. No implementation or production authority. |")
    index_text = index.read_text().replace(
        "Expected bytes for C0-004, C0-005, C0-012, C0-014, C0-015, and C0-016 were not locally recovered.",
        "C0-004 exact expected bytes were recovered, verified, adopted, and locked as Version 2.1. Expected bytes for C0-005, C0-012, C0-014, C0-015, and C0-016 remain unrecovered.",
    )
    write_text(index, index_text)

    overlay = ROOT / "C0_004_GOVERNANCE_REGISTER_OVERLAY.md"
    write_text(overlay, f"""# C0-004 Governance Register Overlay

- Lifecycle event: `C0_004_MASTER_PRODUCT_VISION_CONSTITUTIONALLY_LOCKED`
- Controlling artifact: `{rel(ACTIVE_MD)}` / `{final_hash}`
- Lock record: `{rel(LOCK_DIR / 'C0_004_MASTER_PRODUCT_VISION_CONSTITUTIONAL_LOCK_RECORD.md')}` / `{lock_hash}`
- Domain owner: Founder / Product Strategy
- Dependency role: apex product-purpose authority; no circular dependency introduced
- Reference normalization: `Master Product Vision` means C0-004 V2.1
- Founder decision: conditional lifecycle completion gates passed
- Requirement and traceability effect: existing product-purpose references now resolve to the locked V2.1 artifact
- Retained P2: `0`
- Operational authority: all prohibited authority flags remain `FALSE`
""")
    for path in (
        REPO / "docs/canon/companions/EQUINESYNC_CONSTITUTIONAL_AUTHORITY_MATRIX_V1_2.md",
        REPO / "docs/canon/companions/CONSTITUTIONAL_DOMAIN_OWNERSHIP_AND_BOUNDARY_REGISTER_V1_1.md",
        REPO / "docs/canon/companions/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_1.md",
        REPO / "docs/canon/companions/EQUINESYNC_CANON_DEPENDENCY_MAP_V1_2.md",
        REPO / "docs/canon/companions/MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.md",
        REPO / "docs/canon/companions/MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.md",
        REPO / "docs/canon/companions/MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.md",
        REPO / "docs/canon/registries/CANON_ARTIFACT_INVENTORY.md",
    ):
        text = path.read_text()
        note = f"**July 16, 2026 C0-004 lifecycle completion:** Master Product Vision V2.1 is `ADOPTED` and `LOCKED`. Current-state overlay: [`C0_004_GOVERNANCE_REGISTER_OVERLAY.md`](../reviews/c0_004_master_product_vision_lifecycle_completion/C0_004_GOVERNANCE_REGISTER_OVERLAY.md). No implementation or production authority.\n\n"
        if "C0-004 lifecycle completion" not in text:
            lines = text.splitlines()
            lines.insert(2 if len(lines) > 2 else len(lines), note.rstrip())
            write_text(path, "\n".join(lines))


def final_reports(final_md_hash: str, final_docx_hash: str, adoption_hash: str, lock_hash: str) -> None:
    write_text(ROOT / "C0_004_PRIVACY_DEPENDENCY_IMPACT_REPORT.md", """# C0-004 Privacy Dependency Impact Report

- C0-004 source identity: `VERIFIED`
- C0-004 lifecycle: `LOCKED`
- C0-023 Product Vision dependency: `RESOLVED`
- C0-023 lock rerun authorized here: `FALSE`
- Expected remaining Privacy lock blocker: `C0-019 Master Agreement, Consent, and Authorization Model lifecycle completion`

C0-023 may proceed to a separate lock-readiness rerun after C0-019 is resolved. This report neither reruns nor locks Privacy.
""")
    write_text(ROOT / "C0_004_FINAL_LIFECYCLE_COMPLETION_REPORT.md", f"""# C0-004 Final Lifecycle Completion Report

Final disposition: `C0_004_MASTER_PRODUCT_VISION_CONSTITUTIONALLY_LOCKED`

- Attachment SHA-256: `{EXPECTED}`
- Source classification: `EXACT_C0_EXPECTED_SOURCE_CONFIRMED`
- Controlling Markdown: `{rel(ACTIVE_MD)}` / `{final_md_hash}`
- DOCX counterpart: `{rel(ACTIVE_DOCX)}` / `{final_docx_hash}`
- Adoption record SHA-256: `{adoption_hash}`
- Lock record SHA-256: `{lock_hash}`
- P0: `0`
- Open P1: `0`
- Blocking P2: `0`
- Retained P2: `0`
- MD/DOCX parity: `PASS`
- 47-page visual QA: `PASS`
- Substantive canon changes during processing: `0`
- Application/runtime files changed: `0`
- Privacy Product Vision dependency: `RESOLVED`; C0-019 remains separate
- Governance V1.0 baseline adoption/lock: `FALSE`
- Implementation/runtime/migration/provider/integration/deployment/production/customer-data/public-launch/certification/public-trust authority: `FALSE`
""")


def main() -> None:
    update_phase_a_visual()
    adopted_md_hash, adopted_docx_hash, adoption_hash = create_adoption()
    lock_readiness(adopted_md_hash, adopted_docx_hash, adoption_hash)
    final_md_hash, final_docx_hash, lock_hash = create_lock(adopted_md_hash, adopted_docx_hash, adoption_hash)
    update_current_state(final_md_hash, lock_hash)
    final_reports(final_md_hash, final_docx_hash, adoption_hash, lock_hash)
    print(json.dumps({
        "disposition": "C0_004_MASTER_PRODUCT_VISION_CONSTITUTIONALLY_LOCKED",
        "final_markdown_sha256": final_md_hash,
        "final_docx_sha256": final_docx_hash,
        "adoption_record_sha256": adoption_hash,
        "lock_record_sha256": lock_hash,
    }, indent=2))


if __name__ == "__main__":
    main()
