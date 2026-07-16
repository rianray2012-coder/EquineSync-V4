#!/usr/bin/env python3
"""Independently verify Phase C artifacts without issuing lifecycle authority."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/canon/reviews/governance_v1_0_c0_phase_c_hash_version_recovery"
TRACK = BASE / "track_c"
STATE = ROOT / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle"
SCANS = BASE / "formal_scans"

EXPECTED = {
    "C0-004": ("ba2bdedfbbd89889af02035656d2f738175dcbde3869084c5e0c92062644c469", "42f01b4094923d85ab6b7de9c56fc6c084adac4f9b06464554ba2f9e91787953", False),
    "C0-005": ("4344294c05b4b5483ff23497f198edb18e8bcb54d93410266791a57809107533", "5d600fec0bb674b5b9a961628e70453e3bd56083ad53edd19c974216ae18fa9c", False),
    "C0-012": ("cd47c8fe3e76eee067594f38efd45265929d279c4d1fd9dc2a70e16fea976391", "be225014b476d266d4effcd35fa8577da21d8646e53afbbf60ca3b6509ea0057", False),
    "C0-014": ("ee97b61290d7552a9907df14db25b2a3b4a8a32a57871adca6ce0e373b5c712b", "4b88f477677bb2147df44f766a36b07ca587421967ea510b00e20315a34d2590", False),
    "C0-015": ("3e7428771d3d8868e801e80551912a8f6284f5a4d53698d170d4b67b3be13553", "aebae6b952423435806837abf2fd9d5f1dd0dc96fca74810e78da50f0f80c47a", False),
    "C0-016": ("063339ec8b8aab20908742675013692de2dbb56f018939bac71371b8366d2466", "cd66ca4fcfdcc188ce5d6a44239ad52541c8a0be0c571d935405f64af6b72085", False),
    "C0-019": ("630b6128e37734be01a40d64b80d9fb4d74fce48198c60f9fcbd1a2ef83c232b", "af34895d8248f0fa26f7c976c345caa7ac9fba7b7bf4f597d32bfb68e0797d20", True),
    "C0-022": ("2034979a0fe77fd89ba065ecf9d309f5897641b6c38c9bde7c69dc8ac06adeab", "6e3f4160e4166831cfe4f154032ff7648a5a44b70762289252c615e98b899fa3", True),
    "C0-028": ("def33679b38b25ab5bbe0fc5c9c78a4fe8d505533d9c1d91a37035735f283ab4", "a4787fb641dca1d28d98f10240957d0b09ea8ee1cee8358f64e80dd658b8b626", True),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    register = json.loads((BASE / "C0_PHASE_C_SOURCE_RECOVERY_REGISTER.json").read_text())
    assert register["row_count"] == 9 and register["recovered"] == 3 and register["not_recovered"] == 6
    assert not any(register["authority"].values())
    rows = {row["row_id"]: row for row in register["rows"]}
    assert set(rows) == set(EXPECTED)
    required_suffixes = [
        "SOURCE_RECOVERY_REPORT.md", "SOURCE_PROVENANCE_RECORD.md", "RAW_BYTE_COMPARISON.json",
        "NORMALIZED_TEXT_COMPARISON.md", "SEMANTIC_AND_AUTHORITY_DELTA.md", "REQUIREMENT_ID_DELTA.json",
        "CROSS_CANON_IMPACT_REPORT.md", "SOURCE_RELATIONSHIP_CLASSIFICATION.md",
        "FOUNDER_SOURCE_IDENTITY_DECISION_PACKET.md", "EVIDENCE_MANIFEST.json",
    ]
    for row_id, (current_sha, expected_sha, recovered) in EXPECTED.items():
        row = rows[row_id]
        assert row["current_sha256"] == current_sha and row["expected_sha256"] == expected_sha
        assert row["recovered"] is recovered
        row_dir = TRACK / row_id.replace("-", "_")
        names = [p.name for p in row_dir.rglob("*") if p.is_file()]
        for suffix in required_suffixes:
            assert any(name.endswith(suffix) for name in names), (row_id, suffix)
        manifest = json.loads(next(row_dir.glob("*_EVIDENCE_MANIFEST.json")).read_text())
        assert not any(manifest["authority"].values())
        for item in manifest["files"]:
            path = ROOT / item["path"]
            assert path.is_file() and sha(path) == item["sha256"]
        recovered_files = list((row_dir / "recovered_sources").glob("*"))
        if recovered:
            assert len(recovered_files) == 1 and sha(recovered_files[0]) == expected_sha
        else:
            assert not recovered_files
    assert rows["C0-028"]["classification"] == "EXACT_EXPECTED_SOURCE_RECOVERED_CURRENT_FORMATTING_DERIVATIVE"
    assert rows["C0-028"]["normalized_similarity"] == 1.0
    assert rows["C0-019"]["classification"].endswith("CURRENT_NONCONTROLLING_DERIVATIVE")
    assert rows["C0-022"]["classification"].endswith("CURRENT_NONCONTROLLING_DERIVATIVE")

    state = json.loads((STATE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json").read_text())
    assert state["unresolved_lifecycle_blockers"] == 17
    for row in state["rows"]:
        if row["record_id"] in EXPECTED:
            assert row["unresolved_blocker"] is True and row["adoption_state"] == "NOT_ESTABLISHED" and row["lock_state"] == "NOT_ESTABLISHED"
    findings = json.loads((BASE / "C0_PHASE_C_RETAINED_FINDINGS_REGISTER.json").read_text())
    assert (findings["p0"], findings["open_p1"], findings["source_classification_blocking_p2"], findings["retained_p2"]) == (0, 0, 0, 6)

    for path in list(BASE.rglob("*.json")) + [STATE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json", STATE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json"]:
        json.loads(path.read_text())
    secret = re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{20,}")
    merge = re.compile(r"^(<<<<<<<|=======|>>>>>>>)", re.MULTILINE)
    for path in [p for p in BASE.rglob("*") if p.is_file() and p.suffix in {".md", ".json"}]:
        text = path.read_text(errors="ignore")
        assert not secret.search(text), path
        assert not merge.search(text), path
    changed = json.loads((BASE / "C0_PHASE_C_CHANGED_FILE_MANIFEST.json").read_text())
    assert changed["runtime_or_application_files"] == []
    subprocess.run(["git", "diff", "--check"], cwd=ROOT, check=True)

    result = {
        "verification": "PASSED_WITH_SIX_RETAINED_SOURCE_EVIDENCE_BLOCKERS",
        "rows_verified": 9, "exact_sources_verified": 3, "absent_sources_recorded": 6,
        "current_sources_unchanged": 9, "row_artifact_sets_complete": 9,
        "p0": 0, "open_p1": 0, "source_classification_blocking_p2": 0,
        "retained_source_evidence_p2": 6, "remaining_lifecycle_blockers": 17,
        "json": "PASSED", "secret_scan": "PASSED", "merge_marker_scan": "PASSED",
        "diff_hygiene": "PASSED", "runtime_or_application_changes": 0,
        "adoptions_issued": 0, "locks_issued": 0, "authority_flags_false": True,
    }
    (SCANS / "C0_PHASE_C_INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n")
    (SCANS / "C0_PHASE_C_INDEPENDENT_VERIFICATION.md").write_text("# C0 Phase C Independent Verification\n\n" + "\n".join(f"- {key}: `{value}`" for key, value in result.items()) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
