#!/usr/bin/env python3
import argparse, csv, json, shutil, subprocess, sys, tempfile
from pathlib import Path

def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)

def run_case(package, name, mutate, expected):
    with tempfile.TemporaryDirectory() as td:
        temp = Path(td) / package.name
        ignore = shutil.ignore_patterns("*.zip", "__pycache__")
        shutil.copytree(package, temp, ignore=ignore)
        mutate(temp)
        validator = temp / "VALIDATION/validate_tier1_documents_03_10_v4.py"
        result = subprocess.run([sys.executable, str(validator), "--package-root", str(temp)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        detected = result.returncode != 0 and expected in result.stdout
        return {"fixture": name, "expected_check": expected, "expected_failure_detected": detected}

def collapse_csv_field(root, rel, fields):
    path = root / rel
    rows = read_csv(path)
    for field in fields:
        for row in rows:
            row[field] = f"GENERIC_NEGATIVE_FIXTURE_{field}"
    write_csv(path, rows)

def identical_templates(root):
    template_dir = root / "10_CLOSING_AUDIT_PROTOCOL/templates"
    body = "# Generic Template\n\nTemplate name: `GENERIC`.\n\n## Purpose\n\nsame\n"
    for path in template_dir.glob("*.md"):
        path.write_text(body, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("positional_package_root", nargs="?")
    parser.add_argument("--package-root", dest="package_root")
    args = parser.parse_args()
    package = Path(args.package_root or args.positional_package_root or ".").resolve()
    cases = [
        ("founder_decision_consequence_collapse", lambda r: collapse_csv_field(r, "FOUNDER_DECISION_PACKET.csv", ["consequence_if_approved"]), "distinct_founder_decision_consequence_if_approved"),
        ("findings_analysis_collapse", lambda r: collapse_csv_field(r, "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv", ["severity_rationale", "impact", "mitigation"]), "distinct_findings_severity_rationale"),
        ("lifecycle_rule_collapse", lambda r: collapse_csv_field(r, "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv", ["reversal_rules"]), "distinct_lifecycle_reversal_rules"),
        ("audit_required_evidence_collapse", lambda r: collapse_csv_field(r, "10_CLOSING_AUDIT_PROTOCOL/AUDIT_REQUIREMENTS_MATRIX.csv", ["required_evidence"]), "distinct_audit_required_evidence_prefix_stripped"),
        ("doc10_template_body_collapse", identical_templates, "distinct_doc10_normalized_template_bodies"),
    ]
    checks = [run_case(package, name, mutate, expected) for name, mutate, expected in cases]
    report = {"status": "PASS" if all(c["expected_failure_detected"] for c in checks) else "FAIL", "fixture_count": len(checks), "checks": checks}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
