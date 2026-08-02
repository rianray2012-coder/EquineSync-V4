#!/usr/bin/env python3
import argparse, csv, difflib, hashlib, json, shutil, tempfile
from pathlib import Path

AUTHORITY = "NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED"
STATES = ["DRAFT_UNMERGED","FOUNDER_REVIEW_READY","ADOPTED","ACCESSIONED","LOCKED","ACTIVE","SUSPENDED","SUPERSEDED","HISTORICAL_RETAINED","WITHDRAWN","BLOCKED_EVIDENCE_REQUIRED","REMEDIATION_REQUIRED","REJECTED"]
REQUIRED_TEMPLATE_SECTIONS = ["## Purpose","## Triggering Event","## Required Inputs","## Required Evidence","## Exclusions","## Responsible Preparer","## Required Reviewer","## Approval Or Acknowledgement Field","## Authority Effect","## Prohibited Conclusions","## Completion Criteria","## Reopening Or Supersession Effect"]

def read_csv(p):
    with p.open(newline="") as f:
        return list(csv.DictReader(f))

def norm_template(text):
    lines=[]
    for line in text.splitlines():
        low=line.lower()
        if low.startswith("# ") or low.startswith("- template id:") or low.startswith("- template name:"):
            continue
        lines.append(" ".join(line.split()).lower())
    return "\n".join(lines)

def check(ok, name, details, results):
    results.append({"name": name, "failure_capable": True, "result": "CHECK_EXECUTED_NO_FAILURE_DETECTED" if ok else "FAIL", "details": details})

def validate(root):
    root=Path(root)
    results=[]
    tpl_dir=root/"10_CLOSING_AUDIT_PROTOCOL"/"templates"
    templates=sorted(tpl_dir.glob("*.md"))
    check(len(templates)==19, "document_10_all_19_templates_exist", f"count={len(templates)}", results)
    norms={}
    for p in templates:
        text=p.read_text()
        missing=[s for s in REQUIRED_TEMPLATE_SECTIONS if s not in text]
        check(not missing, f"document_10_required_sections_{p.name}", f"missing={missing}", results)
        check(AUTHORITY in text and "does not authorize adoption" in text.lower(), f"document_10_authority_boundary_{p.name}", "authority boundary present", results)
        norms[p.name]=norm_template(text)
    pairs=[]
    for a in templates:
        for b in templates:
            if a.name>=b.name: continue
            sim=difflib.SequenceMatcher(None, norms[a.name], norms[b.name]).ratio()
            pairs.append((sim,a.name,b.name))
    max_pair=max(pairs) if pairs else (0,"","")
    check(max_pair[0] < 0.92 and len(set(hashlib.sha256(v.encode()).hexdigest() for v in norms.values()))==19, "document_10_templates_not_functionally_identical", f"closest={max_pair}", results)

    vocab=[r["state"] for r in read_csv(root/"04_AUTHORITY_LIFECYCLE_REGISTER"/"LIFECYCLE_STATE_VOCABULARY.csv")]
    check(vocab==STATES, "document_04_exact_13_state_membership", f"states={vocab}", results)
    matrix=read_csv(root/"04_AUTHORITY_LIFECYCLE_REGISTER"/"LIFECYCLE_TRANSITION_MATRIX.csv")
    seen={(r["permitted_starting_state"], r["permitted_next_state"]) for r in matrix}
    check(len(matrix)==169 and seen=={(a,b) for a in STATES for b in STATES}, "document_04_complete_transition_coverage", f"rows={len(matrix)}", results)
    check(any(r["permitted_starting_state"]=="FOUNDER_REVIEW_READY" and r["permitted_next_state"]=="REMEDIATION_REQUIRED" and r["permitted"]=="YES" for r in matrix), "document_04_remediation_path", "FOUNDER_REVIEW_READY -> REMEDIATION_REQUIRED", results)
    check(any(r["permitted_starting_state"]=="FOUNDER_REVIEW_READY" and r["permitted_next_state"]=="REJECTED" and r["permitted"]=="YES" for r in matrix), "document_04_rejection_path", "FOUNDER_REVIEW_READY -> REJECTED", results)

    decision_rows=read_csv(root/"FOUNDER_DECISION_PACKET.csv")
    reg_rows=read_csv(root/"05_FOUNDER_DECISION_REGISTER"/"FOUNDER_DECISION_DISPOSITION_REGISTER.csv")
    check(len(decision_rows)==5 and len(reg_rows)==5, "document_05_all_five_decisions_present", f"packet={len(decision_rows)} register={len(reg_rows)}", results)
    reg_by={r["decision_id"]:r for r in reg_rows}
    for r in decision_rows:
        rr=reg_by.get(r["decision_id"], {})
        check(r["exact_decision_text"]==rr.get("exact_decision_text"), f"document_05_exact_question_identity_{r['decision_id']}", "packet/register exact text match", results)
        check(r["selected_disposition"]=="NO_DISPOSITION_SELECTED" and r["founder_decision_state"]=="NO_FOUNDER_DECISION_RECORDED" and r["authority_granted"]=="NONE_BY_THIS_PACKAGE", f"document_05_no_implied_approval_{r['decision_id']}", "no decision recorded", results)
        check(AUTHORITY in r["authority_expressly_not_granted"], f"document_05_authority_boundary_{r['decision_id']}", "non-authorities present", results)

    trace=read_csv(root/"03_IMPLEMENTATION_TRACEABILITY"/"REQUIREMENT_TRACEABILITY_REGISTER.csv")
    if trace:
        fields=trace[0].keys()
        check("requirement_type" in fields or "source_text_candidate_state" in fields, "document_03_candidate_verified_separation", f"fields={list(fields)[:10]}", results)
        bad=[r for r in trace if r.get("requirement_type")=="NORMATIVE_REQUIREMENT" and r.get("verification_method","").upper() in {"", "NOT_PERFORMED"}]
        check(not bad, "document_03_no_unverified_normative_requirement", f"bad_count={len(bad)}", results)

    findings=read_csv(root/"CONSOLIDATED_EXTERNAL_REVIEW_FINDING_REGISTER.csv")
    check(len(findings)>=20, "document_06_real_finding_rows_present", f"rows={len(findings)}", results)
    check(all(r["disposition"] in {"CONFIRMED_OPEN","CONFIRMED_REMEDIATED","PARTIALLY_REMEDIATED","NOT_REPRODUCED","SUPERSEDED_BY_LATER_CHANGE","DEFERRED_WITH_RECORDED_BASIS","FOUNDER_DECISION_REQUIRED"} for r in findings), "document_06_valid_disposition_enums", "allowed disposition enum", results)

    ownership=read_csv(root/"07_OWNERSHIP_STEWARDSHIP_REVIEW"/"VACANCY_AND_SUCCESSION_REGISTER.csv")
    invented=[r for r in ownership if "VACANT" not in " ".join(r.values()).upper() and "FOUNDER" not in " ".join(r.values()).upper()]
    check(not invented, "document_07_no_invented_appointments", f"invented_count={len(invented)}", results)

    clusters=read_csv(root/"08_SOURCE_RECONCILIATION"/"DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv")
    source=read_csv(root/"08_SOURCE_RECONCILIATION"/"SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv")
    cluster_ids={r.get("cluster_id") for r in clusters}
    blank=[r for r in source if r.get("duplicate_cluster_id","")==""]
    singleton_literals={"NO_DUPLICATE_CLUSTER","NOT_IN_DUPLICATE_CLUSTER","NOT_APPLICABLE"}
    invalid=[r for r in source if r.get("duplicate_cluster_id") and r.get("duplicate_cluster_id") not in singleton_literals and r.get("duplicate_cluster_id") not in cluster_ids]
    check(not blank and not invalid, "document_08_duplicate_cluster_fk_integrity", f"blank={len(blank)} invalid={len(invalid)}", results)

    pr=read_csv(root/"09_WORKSTREAM_PR_BRANCH_DISPOSITION"/"WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv")
    check(bool(pr) and any("review" in k.lower() for k in pr[0].keys()), "document_09_pr_review_thread_state_available", f"rows={len(pr)}", results)
    check(AUTHORITY in (root/"FINAL_DRAFT_EXECUTIVE_SUMMARY.md").read_text(), "package_authority_boundary_visible", "executive summary boundary", results)
    manifest=json.loads((root/"PACKAGE_MANIFEST.json").read_text())
    manifest_paths={r["path"] for r in manifest["files"]}
    actual={p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.name not in {"PACKAGE_MANIFEST.json","CHECKSUMS.sha256","MANIFEST_OF_MANIFESTS.sha256","FINAL_DRAFT_INTEGRITY_ROOT.json"}}
    missing=actual-manifest_paths
    check(not missing, "manifest_covers_package_files", f"missing={sorted(missing)[:10]}", results)
    return results

def self_test(root):
    root=Path(root)
    failures=[]
    with tempfile.TemporaryDirectory() as td:
        dst=Path(td)/"pkg"
        shutil.copytree(root,dst)
        first=sorted((dst/"10_CLOSING_AUDIT_PROTOCOL"/"templates").glob("*.md"))[0]
        second=sorted((dst/"10_CLOSING_AUDIT_PROTOCOL"/"templates").glob("*.md"))[1]
        second.write_text(first.read_text())
        if not any(r["name"]=="document_10_templates_not_functionally_identical" and r["result"]=="FAIL" for r in validate(dst)):
            failures.append("template clone negative control did not fail")
    with tempfile.TemporaryDirectory() as td:
        dst=Path(td)/"pkg"
        shutil.copytree(root,dst)
        rows=read_csv(dst/"FOUNDER_DECISION_PACKET.csv")
        rows[0]["selected_disposition"]="APPROVE_FOR_DOCUMENTARY_NEXT_STEP"
        with (dst/"FOUNDER_DECISION_PACKET.csv").open("w", newline="") as f:
            w=csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
        if not any(r["name"].startswith("document_05_no_implied_approval") and r["result"]=="FAIL" for r in validate(dst)):
            failures.append("decision preselection negative control did not fail")
    return failures

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--package-root", required=True)
    ap.add_argument("--mode", choices=["package-only","repository-aware"], default="package-only")
    ap.add_argument("--expected-head")
    ap.add_argument("--json-output")
    ap.add_argument("--self-test", action="store_true")
    args=ap.parse_args()
    results=validate(args.package_root)
    negatives=self_test(args.package_root) if args.self_test else []
    passed=sum(1 for r in results if r["result"]!="FAIL")
    failed=[r for r in results if r["result"]=="FAIL"]
    out={"mode":args.mode,"expected_head":args.expected_head,"checks_executed":len(results),"checks_capable_of_failure":len(results),"checks_passed":passed,"checks_failed":len(failed),"negative_test_failures":negatives,"results":results,"overall":"CHECK_EXECUTED_NO_FAILURE_DETECTED" if not failed and not negatives else "FAIL"}
    if args.json_output:
        Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_output).write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))
    return 0 if out["overall"]!="FAIL" else 1
if __name__=="__main__":
    raise SystemExit(main())
