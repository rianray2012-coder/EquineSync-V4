#!/usr/bin/env python3
"""Fail-closed validation for the Founder-directed ten-item PIA portfolio."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
POSITIONS = [f"{n:02d}" for n in range(1, 11)]
CLASSES = {
    "PRIMARY_PIA_PACKAGE", "PIA_COMPONENT_PACKAGE", "SUBORDINATE_ADR_OR_CONTRACT",
    "CROSS_PIA_REVIEW_PACKAGE", "CROSS_PIA_REMEDIATION_PACKAGE", "PIA_HANDOFF_PACKAGE",
    "CONTROLLING_PIA_STANDARD", "CONSTITUTIONAL_OR_CANONICAL_SOURCE", "MIAP_CROSS_CUTTING_PROFILE",
    "ASSURANCE_TOOLING", "ENGINEERING_WORK_PACKAGE", "HISTORICAL_SUPERSEDED", "NON_PIA_UNRELATED",
}
DISPOSITION = "TEN_ITEM_PIA_PORTFOLIO_REALIGNED_AND_DRIFT_CONTROLS_ACTIVE"


def main() -> int:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    with (ROOT / "PIA_PORTFOLIO_REALIGNMENT_REGISTER.csv").open(newline="", encoding="utf-8") as handle:
        portfolio = list(csv.DictReader(handle))
    with (ROOT / "PIA_PACKAGE_INVENTORY.csv").open(newline="", encoding="utf-8") as handle:
        inventory = list(csv.DictReader(handle))
    machine = json.loads((ROOT / "PIA_PORTFOLIO_MACHINE_READABLE.json").read_text(encoding="utf-8"))

    check("EXACTLY_TEN_POSITIONS", [r["position"] for r in portfolio] == POSITIONS, f"positions={len(portfolio)}")
    check("NO_POSITION_OUTSIDE_01_10", all(r["position"] in POSITIONS for r in portfolio), "allowed=01..10")
    item03 = [r for r in portfolio if r["position"] == "03"]
    check("ITEM_03_COMBINED", len(item03) == 1 and item03[0]["controlling_title"] == "Relationship, Authorization, and Permission", "Relationships, Authorization, and Permission remain combined")
    check("NO_ELEVENTH_PIA", len(portfolio) == 10 and not any(r["position"] == "11" for r in portfolio), "no position 11")
    check("ALL_ARTIFACTS_CLASSIFIED", all(r["artifact_class"] in CLASSES for r in inventory), f"unclassified={sum(r['artifact_class'] not in CLASSES for r in inventory)}")
    check("INVENTORY_DENOMINATOR_MATCH", machine["inventory_denominator"] == len(inventory), f"inventory={len(inventory)}")
    check("UNCLASSIFIED_COUNT_ZERO", machine["unclassified_count"] == 0, f"unclassified={machine['unclassified_count']}")
    check("ARTIFACT_IDS_UNIQUE", len({r["artifact_id"] for r in inventory}) == len(inventory), "artifact identifiers unique")
    check("IMPLEMENTATION_AUTHORITY_FALSE", all(r["implementation_authority"] == "FALSE" for r in inventory), "no implementation authority")
    check("ENROLLMENT_IN_ITEM_01", all(r["primary_portfolio_position"] == "01" for r in inventory if r["document_id"] == "ENROLLMENT-CAPABILITY"), "Enrollment is Item 01 component")
    check("REVIEWS_NOT_PIAS", all(r["artifact_class"] in {"CROSS_PIA_REVIEW_PACKAGE", "PIA_HANDOFF_PACKAGE", "ASSURANCE_TOOLING"} for r in inventory if "REVIEW" in r["artifact_name"].upper()), "review artifacts are not primary PIAs")
    check("STAGE2A_NOT_PIA", all(r["artifact_class"] == "MIAP_CROSS_CUTTING_PROFILE" for r in inventory if "STAGE 2A" in r["artifact_name"].upper()), "Stage 2A is MIAP cross-cutting")
    check("RECOMMENDATIONS_NOT_APPROVED", all(not r["founder_approval_status"].startswith("FOUNDER_APPROVED") for r in inventory if "RECOMMENDATION" in r["artifact_name"].upper()), "recommendations carry no approval")
    active_files = [p for p in ROOT.iterdir() if p.suffix.lower() in {".md", ".csv", ".json"}]
    transposed = []
    for path in active_files:
        if re.search(r"\bMAIP\b", path.read_text(encoding="utf-8"), flags=re.IGNORECASE):
            transposed.append(path.name)
    check("ACTIVE_TERMINOLOGY_USES_MIAP", not transposed, f"transposed_term_files={transposed}")
    check("MACHINE_STATUS_MATCH", machine["status"] == DISPOSITION, machine["status"])

    passed = all(item["passed"] for item in checks)
    report = {
        "package_id": "ES-PIA-PORTFOLIO-REALIGNMENT-V1.0.0",
        "result": "PASS" if passed else "FAIL",
        "disposition": DISPOSITION if passed else "PORTFOLIO_REALIGNMENT_VALIDATION_FAILED",
        "portfolio_positions": len(portfolio),
        "inventory_denominator": len(inventory),
        "unclassified_count": sum(r["artifact_class"] not in CLASSES for r in inventory),
        "source_gap_count": sum(r["source_gap"] == "TRUE" for r in inventory),
        "checks": checks,
        "implementation_activity": "NONE",
    }
    (ROOT / "VALIDATION_REPORT.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# PIA Portfolio Realignment Validation Report", "",
        f"**Result:** `{'PASS' if passed else 'FAIL'}`  ",
        f"**Disposition:** `{report['disposition']}`  ",
        f"**Inventory denominator:** `{len(inventory)}`  ",
        f"**Unclassified count:** `{report['unclassified_count']}`  ",
        f"**Exact-source gaps:** `{report['source_gap_count']}`  ",
        "**Implementation activity:** `NONE`", "", "## Checks", "",
    ]
    lines.extend(f"- `{'PASS' if c['passed'] else 'FAIL'}` `{c['check']}` - {c['detail']}" for c in checks)
    (ROOT / "VALIDATION_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
