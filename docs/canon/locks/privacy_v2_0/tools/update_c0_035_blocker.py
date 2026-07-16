#!/usr/bin/env python3
"""Narrow the C0-035 lock blocker after the C0-023 lock."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
LIFECYCLE = REPO / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle"
BATCH = REPO / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1"
REPORT = REPO / "docs/canon/adoptions/c0_023_c0_035_lock_readiness_rerun/C0_035_REPORTING_LOCK_READINESS_RERUN.md"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n")


def update_json(path: Path, collection: str) -> None:
    data = json.loads(path.read_text())
    row = next(item for item in data[collection] if item["record_id"] == "C0-035")
    row.update({
        "lock_readiness_state": "NOT_READY_C0_022_ADOPTION_AND_LOCK_REQUIRED",
        "retained_p2": ["C0-035-LR-P2-01"],
        "remedy": "Adopt and lock C0-022, then rerun C0-035 lock readiness under separate founder authority.",
        "lock_readiness_evidence": REPORT.relative_to(REPO).as_posix(),
    })
    data["generated_at"] = now()
    path.write_text(json.dumps(data, indent=2) + "\n")


def replace_row(path: Path, replacement: str) -> None:
    lines = path.read_text().splitlines()
    for index, line in enumerate(lines):
        if line.startswith("| C0-035 |"):
            lines[index] = replacement
            write(path, "\n".join(lines))
            return
    raise RuntimeError(f"C0-035 row missing in {path}")


def main() -> None:
    update_json(BATCH / "C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json", "rows")
    update_json(LIFECYCLE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json", "rows")

    ledger_path = LIFECYCLE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json"
    ledger = json.loads(ledger_path.read_text())
    row = next(item for item in ledger["records"] if item["record_id"] == "C0-035")
    row.update({
        "next_step": "Adopt and lock C0-022, then rerun C0-035 lock readiness under separate founder authority.",
        "lock_readiness_state": "NOT_READY_C0_022_ADOPTION_AND_LOCK_REQUIRED",
        "retained_p2": ["C0-035-LR-P2-01"],
        "lock_readiness_evidence": REPORT.relative_to(REPO).as_posix(),
    })
    ledger["generated_at"] = now()
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")

    replace_row(LIFECYCLE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md", "| C0-035 | TRACK_D_MISSING_SOURCE_RECOVERY | lock_required | FOUNDER_ADOPTED | ADOPTED | NOT_YET_LOCKED | Adopt and lock C0-022, then rerun C0-035 lock readiness under separate founder authority. |")
    replace_row(LIFECYCLE / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md", "| C0-035 | Master Reporting, Analytics, and Business Intelligence Model | lock_required | NOT_READY_C0_022_ADOPTION_AND_LOCK_REQUIRED | Adopt and lock C0-022, then rerun C0-035 lock readiness under separate founder authority. |")

    index = REPO / "docs/canon/CANON_INDEX.md"
    text = index.read_text()
    old = next(line for line in text.splitlines() if line.startswith("| 3 | Master Reporting, Analytics, and Business Intelligence Model |"))
    new = "| 3 | Master Reporting, Analytics, and Business Intelligence Model | `docs/canon/founder_approved_sources/MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0_FOUNDER_APPROVED.docx` | `ADOPTED`; controlling; `NOT_READY_C0_022_ADOPTION_AND_LOCK_REQUIRED`; not locked | Reporting and analytics constitutional authority. Open `C0-035-LR-P1-01`; C0-022 must be adopted and locked before rerun. No operational authority. |"
    write(index, text.replace(old, new))


if __name__ == "__main__":
    main()
