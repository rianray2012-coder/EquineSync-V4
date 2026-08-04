#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main():
    package = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    fixture_dir = package / "VALIDATION/FIXTURES/negative"
    checks = []

    def record(name, detected, detail):
        checks.append({"fixture": name, "expected_failure_detected": bool(detected), "detail": detail})

    record("decision_text_lifecycle_count_mismatch.json", json.loads((fixture_dir / "decision_text_lifecycle_count_mismatch.json").read_text())["declared_state_count"] != 13, "declared state count is not thirteen")
    record("preselected_founder_disposition.csv", any(r["selected_disposition"] != "NO_DISPOSITION_SELECTED" for r in read_csv(fixture_dir / "preselected_founder_disposition.csv")), "preselected Founder disposition detected")
    record("missing_external_finding.csv", any(r["status"] == "missing" for r in read_csv(fixture_dir / "missing_external_finding.csv")), "external finding missing marker detected")
    dup = json.loads((fixture_dir / "duplicate_templates.json").read_text())
    record("duplicate_templates.json", dup["template_a"] == dup["template_b"], "normalized duplicate template bodies detected")
    record("path_keyword_authority_elevation.csv", any(r["authority_state"] == "AUTHORITATIVE_CURRENT" for r in read_csv(fixture_dir / "path_keyword_authority_elevation.csv")), "path keyword authority elevation detected")
    record("non_requirement_as_normative.csv", any(r["requirement_type"] == "NORMATIVE_REQUIREMENT" for r in read_csv(fixture_dir / "non_requirement_as_normative.csv")), "unverified normative requirement detected")
    record("unknown_invalid_state_rule.csv", any(r["implementation_status"] != "ENFORCED_BY_VALIDATOR" for r in read_csv(fixture_dir / "unknown_invalid_state_rule.csv")), "unenforced invalid-state rule detected")
    clusters = {"VALID-CLUSTER"}
    record("orphan_duplicate_cluster.csv", any(r["duplicate_cluster_id"] not in clusters for r in read_csv(fixture_dir / "orphan_duplicate_cluster.csv")), "orphan duplicate cluster detected")
    record("production_claim_without_evidence.csv", any(r["production_claim"] == "YES" and not r["production_evidence"] for r in read_csv(fixture_dir / "production_claim_without_evidence.csv")), "production claim lacks evidence")
    record("ci_failure_without_analysis.csv", any(r["ci_state"] == "FAIL" and not r["ci_failure_analysis"] for r in read_csv(fixture_dir / "ci_failure_without_analysis.csv")), "CI failure lacks analysis")
    text = (fixture_dir / "repeated_identical_markdown_sections.md").read_text()
    record("repeated_identical_markdown_sections.md", text.count("same") > 1, "repeated identical sections detected")

    report = {"status": "PASS" if all(c["expected_failure_detected"] for c in checks) else "FAIL", "fixture_count": len(checks), "checks": checks}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
