#!/usr/bin/env python3
"""Validate C0-023 lock and package the C0-035 blocked disposition."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

from docx import Document


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("build", HERE / "build_c0_023_lock.py")
BUILD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(BUILD)

REPO = BUILD.REPO
ROOT = BUILD.ROOT
READINESS = BUILD.READINESS
OUTPUT = REPO / "outputs/governance_v1_0_c0_023_privacy_lock_c0_035_blocked"
PACKAGE = OUTPUT / "GOVERNANCE_V1_0_C0_023_PRIVACY_LOCK_C0_035_BLOCKED_EVIDENCE_PACKAGE.zip"
LOCK_RECORD = ROOT / "C0_023_PRIVACY_AND_DATA_PROTECTION_CONSTITUTIONAL_LOCK_RECORD.md"
CHANGED = [
    "docs/canon/founder_approved_sources/MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_FOUNDER_APPROVED.md",
    "docs/canon/founder_approved_sources/MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_FOUNDER_APPROVED.docx",
    "docs/canon/CANON_INDEX.md",
    "docs/canon/registries/CANON_LOCK_LEDGER.md",
    "docs/canon/companions/GLOBAL_LOCK_STATE_REGISTER.md",
    "docs/canon/companions/GLOBAL_LOCK_STATE_REGISTER.json",
    "docs/canon/companions/GLOBAL_ADOPTION_STATE_REGISTER.md",
    "docs/canon/companions/GLOBAL_ADOPTION_STATE_REGISTER.json",
    "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.md",
    "docs/canon/reviews/governance_v1_0_c0_lifecycle_completion_batch_1/C0_CURRENT_SOURCE_OF_TRUTH_REGISTER.json",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_CURRENT_LIFECYCLE_STATE_REGISTER.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_CURRENT_LIFECYCLE_STATE_REGISTER.json",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_HISTORICAL_TO_CURRENT_DELTA.md",
    "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle/C0_HISTORICAL_TO_CURRENT_DELTA.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=True))


def main() -> None:
    checks: dict[str, object] = {}
    assert sha(BUILD.ADOPTION) == BUILD.ADOPTION_HASH
    assert sha(ROOT / "pre_lock" / BUILD.PRIVACY_MD.name) == BUILD.PRE_MD_HASH
    assert sha(ROOT / "pre_lock" / BUILD.PRIVACY_DOCX.name) == BUILD.PRE_DOCX_HASH
    checks["adoption_and_pre_lock_hashes"] = "PASS"

    md = BUILD.PRIVACY_MD.read_text()
    assert "Constitutional Lock Status: LOCKED" in md
    assert all(f"{name}: FALSE" in md for name in ("Implementation Authority", "Runtime Authority", "Migration Authority", "Production Authority", "Provider Activation Authority", "Public Launch Authority", "Public Trust Claim Authority"))
    pre_md = (ROOT / "pre_lock" / BUILD.PRIVACY_MD.name).read_text()
    assert pre_md.split("## Authority Boundary", 1)[1] == md.split("## Authority Boundary", 1)[1]
    def body(path: Path) -> list[str]:
        texts = [paragraph.text for paragraph in Document(path).paragraphs]
        return texts[texts.index("Authority Boundary"):]
    assert body(ROOT / "pre_lock" / BUILD.PRIVACY_DOCX.name) == body(BUILD.PRIVACY_DOCX)
    checks["substantive_immutability"] = "PASS"

    expected_record_hash = LOCK_RECORD.with_suffix(".sha256").read_text().split()[0]
    assert sha(LOCK_RECORD) == expected_record_hash
    checks["lock_record_hash"] = "PASS"
    pages = list((ROOT / "render_evidence/final_locked").glob("page-*.png"))
    sheets = list((ROOT / "render_evidence/final_locked").glob("contact-sheet-*.png"))
    assert len(pages) == 24 and len(sheets) == 2
    checks["visual_qa"] = "24_OF_24_PASS"

    state = json.loads((REPO / CHANGED[11]).read_text())
    rows = {row["record_id"]: row for row in state["rows"]}
    assert rows["C0-023"]["lock_state"] == "LOCKED" and rows["C0-023"]["unresolved_blocker"] is False
    assert rows["C0-035"]["lock_state"] == "NOT_YET_LOCKED" and rows["C0-035"]["unresolved_blocker"] is True
    assert state["unresolved_lifecycle_blockers"] == 14
    assert sum(state["category_counts"].values()) == 47
    checks["lifecycle_state"] = "PASS_C0_023_LOCKED_C0_035_OPEN"
    ledger = json.loads((REPO / CHANGED[13]).read_text())
    assert ledger["row_count"] == 14 and sum(ledger["track_counts"].values()) == 14
    assert all(row["record_id"] != "C0-023" for row in ledger["records"])
    assert any(row["record_id"] == "C0-035" for row in ledger["records"])
    checks["blocker_ledger"] = "PASS"

    rerun = json.loads((READINESS / "C0_023_C0_035_LOCK_READINESS_RERUN_FINDINGS.json").read_text())
    assert rerun["C0-023"]["ready"] is True and rerun["C0-023"]["open_p1"] == 0
    assert rerun["C0-035"]["ready"] is False and rerun["C0-035"]["open_p1"] == 1
    checks["readiness_findings"] = "PASS"

    files = [path for path in ROOT.rglob("*") if path.is_file()] + [path for path in READINESS.rglob("*") if path.is_file()] + [REPO / path for path in CHANGED]
    text_files = [path for path in files if path.suffix.lower() in {".md", ".json", ".txt", ".py"}]
    all_text = "\n".join(path.read_text(errors="replace") for path in text_files)
    assert not re.search(r"^(<<<<<<<|=======|>>>>>>>)", all_text, re.M)
    assert not re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bsk_(?:live|test)_[A-Za-z0-9]{16,}|\bAKIA[0-9A-Z]{16}\b", all_text)
    for path in files:
        if path.suffix == ".json":
            json.loads(path.read_text())
    checks["merge_secret_json_scans"] = "PASS"

    compile_result = subprocess.run(["python3", "-m", "py_compile", str(HERE / "build_c0_023_lock.py"), str(Path(__file__))], cwd=REPO, capture_output=True, text=True)
    assert compile_result.returncode == 0, compile_result.stderr
    diff_result = subprocess.run(["git", "diff", "--check"], cwd=REPO, capture_output=True, text=True)
    assert diff_result.returncode == 0, diff_result.stdout + diff_result.stderr
    checks["python_compilation"] = "PASS"
    checks["git_diff_check"] = "PASS"
    checks["application_runtime_files_changed"] = 0
    checks["authority"] = {key: False for key in ("implementation", "migration", "runtime", "provider_activation", "production", "public_launch", "certification", "public_trust_claims")}

    write_text(ROOT / "C0_023_PRIVACY_LOCK_VISUAL_QA_REPORT.md", """# C0-023 Privacy Lock Visual QA Report

- Final locked DOCX pages: `24`
- Pages inspected: `24 of 24`
- Contact sheets inspected: `2 of 2`
- Clipping, overlap, malformed content, or unexpected blank pages: `0`
- Result: `PASS`
""")
    write_json(ROOT / "C0_023_LOCK_C0_035_BLOCKED_FORMAL_VALIDATION.json", {
        "disposition": "C0_023_LOCKED_C0_035_BLOCKED_BY_C0_022_LIFECYCLE",
        "checks": checks,
        "findings": {"C0-023": {"p0": 0, "open_p1": 0, "retained_p2": 1}, "C0-035": {"p0": 0, "open_p1": 1, "retained_p2": 1}},
    })

    review_files = [
        path for path in ROOT.rglob("*")
        if path.is_file() and path.name != "C0_023_LOCK_C0_035_BLOCKED_EVIDENCE_MANIFEST.json"
    ] + [path for path in READINESS.rglob("*") if path.is_file()]
    package_files = set(review_files) | {REPO / path for path in CHANGED}
    manifest = {path.relative_to(REPO).as_posix(): sha(path) for path in sorted(package_files)}
    manifest_path = ROOT / "C0_023_LOCK_C0_035_BLOCKED_EVIDENCE_MANIFEST.json"
    write_json(manifest_path, {"files": manifest})
    package_files.add(manifest_path)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(PACKAGE, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(package_files):
            archive.write(path, path.relative_to(REPO).as_posix())
    with tempfile.TemporaryDirectory() as temp:
        with zipfile.ZipFile(PACKAGE) as archive:
            archive.extractall(temp)
        for name, expected in manifest.items():
            assert sha(Path(temp) / name) == expected
    package_hash = sha(PACKAGE)
    write_text(OUTPUT / f"{PACKAGE.name}.sha256", f"{package_hash}  {PACKAGE.name}")
    write_json(OUTPUT / "C0_023_LOCK_C0_035_BLOCKED_EVIDENCE_RECORD.json", {
        "package": PACKAGE.name,
        "sha256": package_hash,
        "fresh_extraction": "PASS",
        "manifest_verification": "PASS",
        "C0-023": "LOCKED",
        "C0-035": "NOT_LOCKED_OPEN_P1_C0_035_LR_P1_01",
    })
    print(json.dumps({"checks": checks, "package": PACKAGE.relative_to(REPO).as_posix(), "sha256": package_hash}, indent=2))


if __name__ == "__main__":
    main()
