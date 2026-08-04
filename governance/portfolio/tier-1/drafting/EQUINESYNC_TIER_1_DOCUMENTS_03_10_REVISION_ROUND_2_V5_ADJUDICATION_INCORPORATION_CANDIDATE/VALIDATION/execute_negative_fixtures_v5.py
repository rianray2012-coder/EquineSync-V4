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

def collapse_lifecycle(root):
    p = root / "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv"
    rows = read_csv(p)
    for row in rows:
        prefix = f"{row['permitted_starting_state']}_TO_{row['permitted_next_state']}_"
        row["reversal_rules"] = prefix + "REVERSAL_REQUIRES_EXPLICIT_RESCISSION_OR_REMEDIATION_EVIDENCE"
        row["reactivation_rules"] = prefix + "REACTIVATION_REQUIRES_AUTHORITY_AND_EVIDENCE"
    write_csv(p, rows)

def break_doc03_metrics(root):
    p = root / "03_IMPLEMENTATION_TRACEABILITY/COVERAGE_METRICS_BY_DOMAIN.csv"
    rows = read_csv(p)
    for row in rows:
        if row["domain"] == "OVERALL":
            row["total_source_text_candidates"] = "96"
            row["open_candidate_rows"] = "96"
    write_csv(p, rows)

def run_case(package, name, mutate, expected):
    with tempfile.TemporaryDirectory() as td:
        temp = Path(td) / package.name
        shutil.copytree(package, temp, ignore=shutil.ignore_patterns("*.zip", "__pycache__"))
        mutate(temp)
        validator = temp / "VALIDATION/validate_tier1_documents_03_10_v5.py"
        result = subprocess.run([sys.executable, str(validator), "--package-root", str(temp)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {"fixture": name, "expected_check": expected, "expected_failure_detected": result.returncode != 0 and expected in result.stdout}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("positional_package_root", nargs="?")
    parser.add_argument("--package-root")
    args = parser.parse_args()
    package = Path(args.package_root or args.positional_package_root or ".").resolve()
    checks = [
        run_case(package, "mechanically_uniquified_lifecycle_rules", collapse_lifecycle, "lifecycle_prefix_stripped_reversal_rules"),
        run_case(package, "doc03_coverage_reverts_to_96", break_doc03_metrics, "doc03_coverage_matches_non_rejected"),
    ]
    report = {"status": "PASS" if all(c["expected_failure_detected"] for c in checks) else "FAIL", "fixture_count": len(checks), "checks": checks}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
