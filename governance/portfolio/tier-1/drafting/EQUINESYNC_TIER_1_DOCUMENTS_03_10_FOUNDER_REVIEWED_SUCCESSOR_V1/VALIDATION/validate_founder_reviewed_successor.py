#!/usr/bin/env python3
import argparse, csv, hashlib, json, shutil, tempfile
from pathlib import Path

SOURCE_SHA = "0d2d79dc99a4f76b97c72ce38ee7ecee5d4e7a8bc45183db0b5770a5bcc61825"
SOURCE_BYTES = 13971
REVIEW_HEAD = "1a3c65c992b1a2f23d205a9d5dcd878ad37cd146"
AUTHORITY_STATES = ["NOT_ACTIVE","IMPLEMENTATION_NOT_AUTHORIZED","PRODUCTION_USE_NOT_AUTHORIZED","MERGE_NOT_AUTHORIZED","CERTIFICATION_NOT_COMPLETE","UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED"]
EXPECTED = {
 "FD-T1R2-001": "FD-T1R2-001_APPROVED_WITH_DOCUMENTARY_SCOPE_ONLY",
 "FD-T1R2-002": "FD-T1R2-002_ACCOUNTABILITY_STRUCTURE_APPROVED_NAMED_APPOINTMENTS_RETAINED_FOR_SEPARATE_FOUNDER_ACTION",
 "FD-T1R2-003": "FD-T1R2-003_SOURCE_CONTROL_HIERARCHY_APPROVED_WITH_EVIDENCE_AND_NONINFERENCE_CONTROLS",
 "FD-T1R2-004": "FD-T1R2-004_RISK_AND_FINDING_DISPOSITION_FRAMEWORK_APPROVED_NO_BULK_RISK_ACCEPTANCE",
 "FD-T1R2-005": "FD-T1R2-005_FUTURE_SEQUENCE_APPROVED_MERGE_AND_ADOPTION_REMAIN_SEPARATELY_AUTHORIZED_ACTIONS",
}

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024), b""): h.update(c)
    return h.hexdigest()

def rows(p):
    with p.open(newline="") as f: return list(csv.DictReader(f))

def check(ok, name, details, out):
    out.append({"name":name,"failure_capable":True,"result":"CHECK_EXECUTED_NO_FAILURE_DETECTED" if ok else "FAIL","details":details})

def validate(root):
    root=Path(root); out=[]
    source=root/"FOUNDER_DECISIONS/FOUNDER_DECISIONS_FD_T1R2_001_005_2026_08_02.md"
    check(source.exists() and sha(source)==SOURCE_SHA and source.stat().st_size==SOURCE_BYTES, "founder_decision_source_authenticates", f"sha={sha(source) if source.exists() else 'missing'} bytes={source.stat().st_size if source.exists() else 0}", out)
    decisions=rows(root/"FOUNDER_DECISIONS/FOUNDER_DECISION_RECORD.csv")
    by={r["decision_id"]:r for r in decisions}
    check(set(by)==set(EXPECTED), "all_five_decisions_recorded", f"ids={sorted(by)}", out)
    for did, disp in EXPECTED.items():
        r=by.get(did,{})
        check(r.get("final_disposition")==disp and r.get("applicable_review_head")==REVIEW_HEAD, f"{did}_final_disposition_matches_source", r.get("final_disposition","missing"), out)
        check(r.get("merge_authority")=="MERGE_NOT_AUTHORIZED" and r.get("activation_authority")=="NOT_ACTIVE" and r.get("implementation_authority")=="IMPLEMENTATION_NOT_AUTHORIZED", f"{did}_non_authority_preserved", "merge/activation/implementation withheld", out)
    appts=rows(root/"TIER_1_GOVERNANCE_ACCOUNTABLE_ROLE_APPOINTMENT_SCHEDULE.csv")
    check(len(appts)==14, "appointment_schedule_covers_14_roles", f"rows={len(appts)}", out)
    check(all(r["proposed_appointee"]=="FOUNDER_ACTION_REQUIRED_NO_APPOINTEE_INFERRED" and r["vacancy_status"]=="VACANT_PENDING_FOUNDER_APPOINTMENT" for r in appts), "no_named_appointments_inferred", "all roles remain Founder action required", out)
    queue=rows(root/"ITEM_SPECIFIC_RISK_AND_FINDING_DISPOSITION_QUEUE.csv")
    check(len(queue)>=28 and all(r["execution_state"]=="NOT_EXECUTED_BY_THIS_PACKAGE" for r in queue), "item_specific_disposition_queue_prepared_not_executed", f"rows={len(queue)}", out)
    check(all(r["bulk_acceptance_state"]=="NO_BULK_RISK_ACCEPTANCE" for r in queue), "no_bulk_risk_acceptance", "bulk acceptance withheld", out)
    riskq=rows(root/"ITEM_SPECIFIC_RESIDUAL_RISK_DISPOSITION_QUEUE.csv")
    check(riskq and all(r["acceptance_state"]=="NOT_ACCEPTED_BY_THIS_PACKAGE" for r in riskq), "residual_risks_not_accepted_by_package", f"rows={len(riskq)}", out)
    seq=rows(root/"FOUNDER_APPROVED_FUTURE_SEQUENCE_TRACKER.csv")
    check(len(seq)==10 and any(r["status"]=="MERGE_NOT_AUTHORIZED" for r in seq), "future_sequence_records_merge_not_authorized", f"rows={len(seq)}", out)
    status=(root/"FOUNDER_REVIEWED_SUCCESSOR_STATUS_REPORT.md").read_text()
    check(all(s in status for s in AUTHORITY_STATES), "continuing_authority_limitations_visible", "authority states present", out)
    manifest=json.loads((root/"PACKAGE_MANIFEST.json").read_text())
    manifest_paths={r["path"] for r in manifest["files"]}
    actual={p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.name not in {"PACKAGE_MANIFEST.json","CHECKSUMS.sha256","MANIFEST_OF_MANIFESTS.sha256","FOUNDER_REVIEWED_SUCCESSOR_INTEGRITY_ROOT.json"}}
    check(not (actual-manifest_paths), "manifest_covers_successor_files", f"missing={sorted(actual-manifest_paths)[:10]}", out)
    return out

def self_test(root):
    failures=[]
    with tempfile.TemporaryDirectory() as td:
        dst=Path(td)/"pkg"; shutil.copytree(root,dst)
        p=dst/"TIER_1_GOVERNANCE_ACCOUNTABLE_ROLE_APPOINTMENT_SCHEDULE.csv"
        data=rows(p); data[0]["proposed_appointee"]="INFERRED_FROM_AUTHORSHIP"
        with p.open("w", newline="") as f:
            w=csv.DictWriter(f, fieldnames=data[0].keys(), lineterminator="\n"); w.writeheader(); w.writerows(data)
        if not any(r["name"]=="no_named_appointments_inferred" and r["result"]=="FAIL" for r in validate(dst)):
            failures.append("appointment inference negative control did not fail")
    with tempfile.TemporaryDirectory() as td:
        dst=Path(td)/"pkg"; shutil.copytree(root,dst)
        p=dst/"ITEM_SPECIFIC_RISK_AND_FINDING_DISPOSITION_QUEUE.csv"
        data=rows(p); data[0]["bulk_acceptance_state"]="BULK_ACCEPTED"
        with p.open("w", newline="") as f:
            w=csv.DictWriter(f, fieldnames=data[0].keys(), lineterminator="\n"); w.writeheader(); w.writerows(data)
        if not any(r["name"]=="no_bulk_risk_acceptance" and r["result"]=="FAIL" for r in validate(dst)):
            failures.append("bulk acceptance negative control did not fail")
    return failures

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--package-root", required=True)
    ap.add_argument("--mode", choices=["package-only","repository-aware"], default="package-only")
    ap.add_argument("--json-output")
    ap.add_argument("--self-test", action="store_true")
    args=ap.parse_args()
    results=validate(args.package_root)
    negatives=self_test(args.package_root) if args.self_test else []
    failed=[r for r in results if r["result"]=="FAIL"]
    out={"mode":args.mode,"checks_executed":len(results),"checks_capable_of_failure":len(results),"checks_passed":len(results)-len(failed),"checks_failed":len(failed),"negative_test_failures":negatives,"results":results,"overall":"CHECK_EXECUTED_NO_FAILURE_DETECTED" if not failed and not negatives else "FAIL"}
    if args.json_output:
        Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_output).write_text(json.dumps(out, indent=2)+"\n")
    print(json.dumps(out, indent=2))
    return 0 if out["overall"]!="FAIL" else 1
if __name__=="__main__":
    raise SystemExit(main())
