from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
REVIEW = ROOT / "docs/canon/reviews/financial_truth_v2_1"
CANON = ROOT / "docs/canon/MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1.md"
SOURCE = ROOT / "docs/canon/history/MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1_FOUNDER_APPROVED_SOURCE.md"
EXPECTED_SHA256 = "0a5302bba0240ba6acd9871b7453916ff212f91ce2f1622b9a4e236701f52604"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    text = CANON.read_text(encoding="utf-8")
    require(CANON.read_bytes() == SOURCE.read_bytes(), "adopted canon differs from approved source")
    require(sha256(CANON) == EXPECTED_SHA256, "unexpected adopted canon SHA-256")

    section_numbers = [int(value) for value in re.findall(r"^# (\d+)\. ", text, re.MULTILINE)]
    require(section_numbers == list(range(1, 76)), "numbered sections are not exactly 1 through 75")
    require("# 70. Explicit Prohibitions" in text, "explicit prohibitions section missing")

    for phrase in (
        "payment-provider activation",
        "schema implementation or migration",
        "QuickBooks write synchronization",
        "collections activity",
        "production mutation",
        "public launch",
    ):
        require(phrase in text, f"required prohibition missing: {phrase}")

    index = (ROOT / "docs/canon/CANON_INDEX.md").read_text(encoding="utf-8")
    require(index.count("docs/canon/MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1.md") >= 2, "active index entry or history missing")
    require("docs/canon/candidates/MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_0.md` | 2.0 | constitutional direction accepted" not in index, "V2.0 remains active candidate")

    for relative in (
        "docs/RF32/RF32_FINANCIAL_TRUTH_V2_1_DEPENDENCY.md",
        "docs/implementation/financial/FUTURE_PAYMENTS_AND_FINANCIAL_RAILS_V2_1_DEPENDENCY.md",
        "docs/implementation/financial/ACCOUNTING_INTEGRATION_V2_1_DEPENDENCY.md",
    ):
        dependency = ROOT / relative
        require(dependency.is_file(), f"dependency file missing: {relative}")
        require("V2_1" in dependency.name or "V2.1" in dependency.read_text(encoding="utf-8"), f"V2.1 dependency not explicit: {relative}")

    approval = json.loads((REVIEW / "master_financial_truth_v2_1_founder_approval.json").read_text(encoding="utf-8"))
    require(approval["canon_status"] == "ADOPTED", "adoption state mismatch")
    require(approval["lock_state"] == "LOCKED", "lock state mismatch")
    require(not any(approval["authority"].values()), "a prohibited authority flag is true")
    require(approval["findings"] == {"p0": 0, "open_p1": 0, "retained_p2": 0}, "finding counts mismatch")

    print("financial_truth_v2_1_lock_validation: PASS")
    print(f"sha256: {EXPECTED_SHA256}")
    print("sections: 75")
    print("authority_flags_true: 0")


if __name__ == "__main__":
    main()
