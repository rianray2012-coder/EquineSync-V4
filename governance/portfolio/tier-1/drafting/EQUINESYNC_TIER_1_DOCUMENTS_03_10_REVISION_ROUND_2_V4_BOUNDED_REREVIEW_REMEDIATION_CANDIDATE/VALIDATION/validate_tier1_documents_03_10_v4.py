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

def distinct_count(records, field):
    return len({(r.get(field) or "").strip() for r in records})

def normalize_template(text):
    out = []
    for line in text.splitlines():
        if line.startswith("# ") or line.startswith("Template name:"):
            continue
        if line.strip():
            out.append(re.sub(r"\s+", " ", line.strip().lower()))
    return "\n".join(out)

def strip_generic_required_evidence(text):
    return re.sub(r"^Evidence specific to [^:]+:\s*", "", text).strip().lower()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("positional_package_root", nargs="?")
    parser.add_argument("--package-root", dest="package_root")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    package = Path(args.package_root or args.positional_package_root or ".").resolve()
    results, failures = [], 0

    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text())
    for item in manifest["files"]:
        path = package / item["path"]
        failures += add(results, f"root_manifest:{item['path']}", path.is_file() and sha(path) == item["sha256"] and path.stat().st_size == item["byte_length"], "root manifest hash and byte-length binding")
    for line in (package / "CHECKSUMS.sha256").read_text().splitlines():
        if not line.strip():
            continue
        digest, rel = line.split(maxsplit=1)
        rel = rel[2:] if rel.startswith("./") else rel
        path = package / rel
        failures += add(results, f"root_checksum:{rel}", path.is_file() and sha(path) == digest, "root checksum binding")

    mom = rows(package / "MANIFEST_OF_MANIFESTS.csv")
    failures += add(results, "manifest_of_manifests_scope", all(Path(r["path"]).name in {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256"} and r["path"] not in {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256", "MANIFEST_OF_MANIFESTS.csv"} for r in mom), "manifest of manifests contains only per-directory manifests/checksums")
    for item in mom:
        path = package / item["path"]
        failures += add(results, f"manifest_of_manifests:{item['path']}", path.is_file() and sha(path) == item["sha256"] and path.stat().st_size == int(item["byte_length"]), "per-directory manifest/checksum binding")

    t1c = rows(package / "OUTSIDE_REVIEW/T1C_CONSOLIDATED_FINDINGS_DISPOSITION_REGISTER.csv")
    open_rows = [r for r in t1c if "OPEN" in r.get("closure_state", "") or "PENDING" in r.get("closure_state", "")]
    failures += add(results, "substantive_closure_blocked_when_open", bool(open_rows), f"open_or_pending_rows={len(open_rows)}")
    failures += add(results, "authority_boundary_present", AUTHORITY_BOUNDARY in (package / "README_FIRST.md").read_text(), "full authority boundary in entrypoint")
    failures += add(results, "doc10_dispute_retained_open", any(r["t1c_id"] == "T1C-004" and "OPEN" in r["closure_state"] for r in t1c), "T1C-004 remains open pending independent adjudication")

    decisions = rows(package / "FOUNDER_DECISION_PACKET.csv")
    for field in ["consequence_if_approved", "consequence_if_deferred", "consequence_if_rejected", "consequence_if_remediation_required"]:
        failures += add(results, f"distinct_founder_decision_{field}", distinct_count(decisions, field) == len(decisions), f"distinct={distinct_count(decisions, field)} rows={len(decisions)}")
    failures += add(results, "founder_no_recommendation_selected", all(r["recommended_option"] == "NO_RECOMMENDATION_SELECTED" for r in decisions), "no preselected Founder option")

    findings = rows(package / "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv")
    for field in ["severity_rationale", "impact", "mitigation"]:
        failures += add(results, f"distinct_findings_{field}", distinct_count(findings, field) > 1, f"distinct={distinct_count(findings, field)}")

    lifecycle = rows(package / "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv")
    for field in ["required_evidence", "prohibited_transitions", "reversal_rules", "suspension_rules", "supersession_rules", "reactivation_rules", "archival_rules"]:
        failures += add(results, f"distinct_lifecycle_{field}", distinct_count(lifecycle, field) > 13, f"distinct={distinct_count(lifecycle, field)}")

    audit = rows(package / "10_CLOSING_AUDIT_PROTOCOL/AUDIT_REQUIREMENTS_MATRIX.csv")
    stripped = {strip_generic_required_evidence(r["required_evidence"]) for r in audit}
    failures += add(results, "distinct_audit_required_evidence_prefix_stripped", len(stripped) == len(audit), f"distinct={len(stripped)} rows={len(audit)}")

    template_files = sorted((package / "10_CLOSING_AUDIT_PROTOCOL/templates").glob("*.md"))
    normalized = {normalize_template(p.read_text(encoding="utf-8")) for p in template_files}
    failures += add(results, "distinct_doc10_normalized_template_bodies", len(normalized) == len(template_files) == 19, f"distinct={len(normalized)} files={len(template_files)}")
    failures += add(results, "legacy_validators_nonoperative", all("NON_OPERATIVE_HISTORICAL" in (package / "VALIDATION" / name).read_text() for name in ["validate_tier1_documents_03_10_v2.py", "validate_tier1_documents_03_10_v3.py"]), "V2/V3 validators labeled non-operative")
    failures += add(results, "rereview_prompt_names_authoritative_v4", "validate_tier1_documents_03_10_v4.py --package-root ." in (package / "INDEPENDENT_CLOSURE_REREVIEW_PACKAGE_AND_PROMPT.md").read_text(), "authoritative V4 invocation present")
    external = rows(package / "EXTERNAL_REVIEW/EXTERNAL_REVIEW_FINDING_DISPOSITION_REGISTER.csv")
    failures += add(results, "external_f02_not_claimed_remediated", any(r["finding_id"] == "F-02" and "REOPENED_V4" in r["round_2_disposition"] for r in external), "legacy F-02 disposition reopened/retained")
    source = rows(package / "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv")
    source_json = json.loads((package / "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.json").read_text())
    failures += add(results, "candidate_paths_not_authoritative_current", not any("/candidates/" in r["repository_path"] and r["source_disposition"] == "authoritative current source" for r in source + source_json), "candidate-tree paths not labeled authoritative current in CSV or JSON")
    inventory = rows(package / "TIER_1_DOCUMENT_INVENTORY.csv")
    failures += add(results, "inventory_not_ready_for_founder_final", not any("READY_FOR_FOUNDER_DIRECTIONAL_AND_FINAL" in r["readiness"] for r in inventory), "inventory readiness reflects open blockers")
    failures += add(results, "doc03_quarantine_present", (package / "03_IMPLEMENTATION_TRACEABILITY/NON_REQUIREMENT_SOURCE_FRAGMENT_QUARANTINE.csv").is_file(), "Doc03 non-requirement fragments quarantined")
    doc09 = rows(package / "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv")
    failures += add(results, "doc09_includes_remediation_prs", {"83", "84", "90"}.issubset({r["pr_number"] for r in doc09}), "Doc09 includes PR #83, #84, #90 or time-bound captures")

    status = "FAIL" if failures else ("STRUCTURAL_PASS_SUBSTANTIVE_CLOSURE_BLOCKED" if open_rows else "STRUCTURAL_PASS_SUBSTANTIVE_CLOSURE_READY_FOR_INDEPENDENT_CONFIRMATION")
    report = {
        "status": status,
        "failures": failures,
        "package_status": "PACKAGING_READY_FOR_BOUNDED_REREVIEW; CONTENT_REVISION_REQUIRED; NOT_ADOPTED; NOT_ACTIVE; MERGE_NOT_AUTHORIZED; FOUNDER_REVIEW_REQUIRED",
        "authority_boundary": AUTHORITY_BOUNDARY,
        "results": results,
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.json_output:
        Path(args.json_output).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
