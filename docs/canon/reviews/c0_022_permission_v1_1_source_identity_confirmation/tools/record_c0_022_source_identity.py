#!/usr/bin/env python3
"""Record the founder confirmation of Permission Model V1.1 as controlling source."""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
ROOT = REPO / "docs/canon/reviews/c0_022_permission_v1_1_source_identity_confirmation"
RECOVERED = REPO / "docs/canon/reviews/governance_v1_0_c0_phase_c_hash_version_recovery/track_c/C0_022/recovered_sources/MASTER_PERMISSION_MODEL_V1_1.md"
V10 = REPO / "docs/canon/MASTER_PERMISSION_MODEL.md"
SOURCE = ROOT / "source_event/MASTER_PERMISSION_MODEL_V1_1_FOUNDER_CONFIRMED_CONTROLLING_SOURCE.md"
EXPECTED = "6e3f4160e4166831cfe4f154032ff7648a5a44b70762289252c615e98b899fa3"
V10_HASH = "2034979a0fe77fd89ba065ecf9d309f5897641b6c38c9bde7c69dc8ac06adeab"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=True))


def replace_row(path: Path, row: str) -> None:
    lines = path.read_text().splitlines()
    for index, line in enumerate(lines):
        if line.startswith("| C0-022 |"):
            lines[index] = row
            write_text(path, "\n".join(lines))
            return
    raise RuntimeError(f"C0-022 row missing from {path}")


def update_json_register(path: Path, collection: str, evidence: str) -> None:
    data = json.loads(path.read_text())
    row = next(item for item in data[collection] if item.get("record_id") == "C0-022")
    row.update({
        "current_category": "adoption_and_lock_required",
        "current_exact_source_status": "EXACT_V1_1_CONTROLLING_SOURCE_FOUNDER_CONFIRMED",
        "current_repository_path": rel(SOURCE),
        "current_sha256": EXPECTED,
        "founder_status": "FOUNDER_SOURCE_IDENTITY_CONFIRMED",
        "adoption_state": "PENDING_SEPARATE_FOUNDER_AUTHORIZATION",
        "lock_state": "PENDING_SEPARATE_FOUNDER_AUTHORIZATION",
        "supersession_state": "V1_1_CONTROLLING_SOURCE_V1_0_NONCONTROLLING_PREDECESSOR",
        "current_controlling_artifact": rel(SOURCE),
        "lifecycle_evidence": evidence,
        "unresolved_blocker": True,
        "remedy": "Conduct separately authorized constitutional adoption and lock review for V1.1.",
    })
    if "category_counts" in data:
        data["category_counts"]["unresolved_source_evidence"] -= 1
        data["category_counts"]["adoption_and_lock_required"] += 1
    data["status"] = "UPDATED_AFTER_C0_022_V1_1_SOURCE_IDENTITY_CONFIRMATION"
    data["generated_at"] = now()
    write_json(path, data)


def main() -> None:
    if sha(RECOVERED) != EXPECTED or sha(V10) != V10_HASH:
        raise RuntimeError("Permission source hash mismatch")
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(RECOVERED, SOURCE)
    if sha(SOURCE) != EXPECTED:
        raise RuntimeError("Preserved source mismatch")

    record = ROOT / "C0_022_PERMISSION_V1_1_FOUNDER_SOURCE_IDENTITY_CONFIRMATION.md"
    write_text(record, f"""# C0-022 Permission V1.1 Founder Source-Identity Confirmation

Disposition: `CONFIRM_V1_1_AS_CONTROLLING_C0_022_SOURCE`

- Recorded: `{now()}`
- C0 identifier: `C0-022`
- Controlling source: `{rel(SOURCE)}`
- Controlling source SHA-256: `{EXPECTED}`
- Superseded predecessor/derivative: `docs/canon/MASTER_PERMISSION_MODEL.md`
- V1.0 SHA-256: `{V10_HASH}`
- Source classification: `EXACT_V1_1_CONTROLLING_SOURCE_FOUNDER_CONFIRMED`
- Adoption: `PENDING_SEPARATE_FOUNDER_AUTHORIZATION`
- Lock: `PENDING_SEPARATE_FOUNDER_AUTHORIZATION`

The founder confirms Version 1.1 as the controlling C0-022 source identity. Version 1.0 remains preserved as a noncontrolling predecessor/derivative. This source decision does not constitute constitutional adoption, lock, implementation, migration, runtime activation, provider activation, production authority, or public-launch authority.
""")
    evidence = rel(record)
    batch = REPO / "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1"
    lifecycle = REPO / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle"
    update_json_register(batch / "C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json", "rows", evidence)
    update_json_register(lifecycle / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json", "rows", evidence)

    source_md = batch / "C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.md"
    state_md = lifecycle / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md"
    replace_row(source_md, f"| C0-022 | Master Permission and Access-Control Model | adoption_and_lock_required | EXACT_V1_1_CONTROLLING_SOURCE_FOUNDER_CONFIRMED | FOUNDER_SOURCE_IDENTITY_CONFIRMED | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | `{rel(SOURCE)}` |")
    replace_row(state_md, f"| C0-022 | Master Permission and Access-Control Model | EXACT_V1_1_CONTROLLING_SOURCE_FOUNDER_CONFIRMED | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | `{evidence}` | True |")
    write_text(source_md, source_md.read_text().replace("Status: `UPDATED_AFTER_FOUNDATIONAL_CANON_SOURCE_CERTIFICATION`", "Status: `UPDATED_AFTER_C0_022_V1_1_SOURCE_IDENTITY_CONFIRMATION`"))

    ledger_json = lifecycle / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json"
    ledger = json.loads(ledger_json.read_text())
    row = next(item for item in ledger["records"] if item["record_id"] == "C0-022")
    row.update({
        "resolution_track": "TRACK_F_ADOPTION_AND_LOCK",
        "current_category": "adoption_and_lock_required",
        "source": rel(SOURCE),
        "founder_status": "FOUNDER_SOURCE_IDENTITY_CONFIRMED",
        "adoption_state": "PENDING_SEPARATE_FOUNDER_AUTHORIZATION",
        "lock_state": "PENDING_SEPARATE_FOUNDER_AUTHORIZATION",
        "next_step": "Conduct separately authorized constitutional adoption and lock review for V1.1.",
        "source_identity_evidence": evidence,
        "phase_c_status": "FOUNDER_SOURCE_IDENTITY_DECISION_COMPLETE",
        "phase_c_classification": "EXACT_V1_1_CONTROLLING_SOURCE_FOUNDER_CONFIRMED",
        "phase_c_recommendation": "PROCEED_TO_SEPARATELY_AUTHORIZED_ADOPTION_REVIEW",
    })
    ledger["track_counts"]["TRACK_C_HASH_OR_VERSION_RECOVERY"] -= 1
    ledger["track_counts"]["TRACK_F_ADOPTION_AND_LOCK"] += 1
    ledger["status"] = "UPDATED_AFTER_C0_022_V1_1_SOURCE_IDENTITY_CONFIRMATION"
    ledger["generated_at"] = now()
    write_json(ledger_json, ledger)

    ledger_md = lifecycle / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md"
    blocker_md = lifecycle / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md"
    replace_row(ledger_md, "| C0-022 | TRACK_F_ADOPTION_AND_LOCK | adoption_and_lock_required | FOUNDER_SOURCE_IDENTITY_CONFIRMED | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | PENDING_SEPARATE_FOUNDER_AUTHORIZATION | Conduct separately authorized constitutional adoption and lock review for V1.1. |")
    replace_row(blocker_md, f"| C0-022 | Master Permission and Access-Control Model | adoption_and_lock_required | EXACT_V1_1_CONTROLLING_SOURCE_FOUNDER_CONFIRMED | Conduct separately authorized constitutional adoption and lock review using `{rel(SOURCE)}`. |")
    write_text(ledger_md, ledger_md.read_text().replace("Status: `UPDATED_AFTER_FOUNDATIONAL_CANON_SOURCE_CERTIFICATION`", "Status: `UPDATED_AFTER_C0_022_V1_1_SOURCE_IDENTITY_CONFIRMATION`"))

    index = REPO / "docs/canon/CANON_INDEX.md"
    text = index.read_text()
    text = text.replace(
        "| 4 | Master Permission Model | `docs/canon/MASTER_PERMISSION_MODEL.md` | available |",
        f"| 4 | Master Permission and Access-Control Model | `{rel(SOURCE)}` | founder-confirmed Version 1.1 controlling source; adoption and lock pending |",
    )
    text = text.replace(
        "C0-022 remains the sole Track C source-identity row.",
        "C0-022 Version 1.1 is founder-confirmed as the controlling source and now requires separately authorized adoption and lock review. No Track C source-identity rows remain.",
    )
    write_text(index, text)

    artifacts = [SOURCE, record, source_md, state_md, ledger_json, ledger_md, blocker_md, index,
                 batch / "C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json",
                 lifecycle / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json"]
    write_json(ROOT / "C0_022_PERMISSION_V1_1_SOURCE_IDENTITY_MANIFEST.json", {
        "disposition": "CONFIRM_V1_1_AS_CONTROLLING_C0_022_SOURCE",
        "files": {rel(path): sha(path) for path in artifacts},
        "authority": {key: False for key in ("adoption", "lock", "implementation", "migration", "runtime", "provider_activation", "production", "public_launch")},
    })
    print(json.dumps({"record": evidence, "record_sha256": sha(record), "source_sha256": sha(SOURCE)}, indent=2))


if __name__ == "__main__":
    main()
