#!/usr/bin/env python3
import argparse, csv, hashlib, json, re, sys
from pathlib import Path

AUTHORITY_BOUNDARY = "NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

def add(results, name, ok, detail):
    results.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
    return 0 if ok else 1

def strip_key_prefix(value, row):
    prefix = f"{row.get('permitted_starting_state','')}_TO_{row.get('permitted_next_state','')}_"
    return value.replace(prefix, "", 1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("positional_package_root", nargs="?")
    parser.add_argument("--package-root")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    package = Path(args.package_root or args.positional_package_root or ".").resolve()
    results, failures = [], 0
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text())
    for item in manifest["files"]:
        path = package / item["path"]
        failures += add(results, f"root_manifest:{item['path']}", path.is_file() and sha(path) == item["sha256"] and path.stat().st_size == item["byte_length"], "root manifest binding")
    for line in (package / "CHECKSUMS.sha256").read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(maxsplit=1)
        path = package / (rel[2:] if rel.startswith("./") else rel)
        failures += add(results, f"root_checksum:{path.relative_to(package).as_posix()}", path.is_file() and sha(path) == digest, "root checksum binding")

    reg = rows(package / "OUTSIDE_REVIEW/T1C_CONSOLIDATED_FINDINGS_DISPOSITION_REGISTER.csv")
    failures += add(results, "package_status_v5", "REVISION_REQUIRED" in (package / "README_FIRST.md").read_text() and "PACKAGING_READY_FOR_BOUNDED_REREVIEW_ACCEPTED" in (package / "README_FIRST.md").read_text() and "CONTENT_REVISION_REQUIRED" in (package / "README_FIRST.md").read_text(), "V5 package status present")
    failures += add(results, "t1c004_not_blocking", any(r["t1c_id"] == "T1C-004" and r["severity"] != "BLOCKING" and "ACCEPTED" in r["current_target_disposition"] for r in reg), "T1C-004 moved out of blocking with accepted core remediation")
    open_required = {"T1C-003","T1C-006","T1C-010","T1C-013","T1C-014","T1C-016","T1C-019","T1C-020"}
    failures += add(results, "required_t1c_items_retained_open", open_required.issubset({r["t1c_id"] for r in reg if "OPEN" in r["closure_state"] or "RETAINED" in r["closure_state"]}), "required open items retained")
    failures += add(results, "t1c009_t1c011_mappings_corrected", all("PPLX-P-02" not in r["source_review_ids"] and "PPLX-P-05" not in r["source_review_ids"] for r in reg if r["t1c_id"] in {"T1C-009","T1C-011"}), "stale source-review IDs removed")

    reqs = rows(package / "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv")
    quarantine = rows(package / "03_IMPLEMENTATION_TRACEABILITY/NON_REQUIREMENT_SOURCE_FRAGMENT_QUARANTINE.csv")
    survivors = [r for r in reqs if r["requirement_type"] != "REJECTED_SOURCE_FRAGMENT_NOT_REQUIREMENT"]
    metrics = rows(package / "03_IMPLEMENTATION_TRACEABILITY/COVERAGE_METRICS_BY_DOMAIN.csv")
    overall = next(r for r in metrics if r["domain"] == "OVERALL")
    failures += add(results, "doc03_survivor_count_45", len(survivors) == 45, f"survivors={len(survivors)}")
    failures += add(results, "doc03_quarantine_count_51", len(quarantine) == 51, f"quarantine={len(quarantine)}")
    failures += add(results, "doc03_coverage_matches_non_rejected", int(overall["total_source_text_candidates"]) == len(survivors) and int(overall["open_candidate_rows"]) == len(survivors), f"overall={overall['total_source_text_candidates']} survivors={len(survivors)}")
    iso_fields = ["iso_29148_characteristic_check","necessary_check","appropriate_check","unambiguous_check","complete_check","singular_check","feasible_check","verifiable_check","correct_check","conforming_check"]
    failures += add(results, "doc03_iso_checks_not_performed_on_survivors", all(all(r[f] == "NOT_PERFORMED" for f in iso_fields) for r in survivors), "survivor ISO checks retained NOT_PERFORMED")

    lifecycle = rows(package / "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv")
    classes = rows(package / "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_RULE_CLASS_TABLE.csv")
    class_ids = {r["rule_class_id"] for r in classes}
    failures += add(results, "lifecycle_rule_class_table_present", len(classes) >= 5 and all(r.get("lifecycle_rule_class_id") in class_ids for r in lifecycle), f"classes={len(classes)}")
    for field in ["reversal_rules","suspension_rules","supersession_rules","reactivation_rules","archival_rules"]:
        stripped = {strip_key_prefix(r[field], r) for r in lifecycle}
        failures += add(results, f"lifecycle_prefix_stripped_{field}", 1 < len(stripped) < len(lifecycle), f"stripped_distinct={len(stripped)} rows={len(lifecycle)}")
    failures += add(results, "prohibited_transitions_no_reversal_reactivation_semantics", all(r["reversal_rules"] == "NOT_APPLICABLE_FOR_PROHIBITED_TRANSITION" and r["reactivation_rules"] == "NOT_APPLICABLE_FOR_PROHIBITED_TRANSITION" for r in lifecycle if r["permitted"] == "NO"), "prohibited transitions do not carry reversal/reactivation rules")

    residual = rows(package / "OUTSIDE_REVIEW/RESIDUAL_NONBLOCKING_AND_NEW_FINDING_REGISTER_V5.csv")
    failures += add(results, "doc10_residual_nonblocking_recorded", any(r["item_id"] == "DOC10-RES-001" for r in residual), "Doc10 control-layer residual present")
    failures += add(results, "v4_01_recorded", any(r["item_id"] == "V4-01" for r in residual), "V4-01 lifecycle finding present")
    failures += add(results, "legacy_stubs_nonzero_documented", all("sys.exit(2)" in (package / "VALIDATION" / name).read_text() for name in ["validate_tier1_documents_03_10_rr2.py","validate_tier1_documents_03_10_v2.py","validate_tier1_documents_03_10_v3.py","validate_tier1_documents_03_10_v4.py"]), "legacy stubs exit nonzero")

    status = "FAIL" if failures else "STRUCTURAL_PASS_SUBSTANTIVE_CLOSURE_BLOCKED"
    report = {"status": status, "failures": failures, "package_status": "REVISION_REQUIRED; PACKAGING_READY_FOR_BOUNDED_REREVIEW_ACCEPTED; CONTENT_REVISION_REQUIRED", "authority_boundary": AUTHORITY_BOUNDARY, "results": results}
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.json_output:
        Path(args.json_output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
