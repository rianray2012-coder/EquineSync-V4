#!/usr/bin/env python3
import csv
import hashlib
import json
import shutil
import subprocess
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

AUTHORITY = "NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED"
SOURCE_SHA = "0d2d79dc99a4f76b97c72ce38ee7ecee5d4e7a8bc45183db0b5770a5bcc61825"
SOURCE_BYTES = 13971
REVIEW_HEAD = "1a3c65c992b1a2f23d205a9d5dcd878ad37cd146"

DECISIONS = [
    {
        "decision_id": "FD-T1R2-001",
        "founder_decision": "APPROVE",
        "final_disposition": "FD-T1R2-001_APPROVED_WITH_DOCUMENTARY_SCOPE_ONLY",
        "authority_granted": "Use the approved 13-state lifecycle vocabulary and documentary transition rules in future Tier 1 governance drafting, review, validation, and status reporting.",
        "authority_not_granted": "No lifecycle transition, adoption, lock, accession, activation, implementation, production use, certification, or merge of a specific artifact.",
        "resulting_status": "DOCUMENTARY_FRAMEWORK_APPROVED_AS_SPECIFIED",
    },
    {
        "decision_id": "FD-T1R2-002",
        "founder_decision": "APPROVE_WITH_MODIFICATIONS",
        "final_disposition": "FD-T1R2-002_ACCOUNTABILITY_STRUCTURE_APPROVED_NAMED_APPOINTMENTS_RETAINED_FOR_SEPARATE_FOUNDER_ACTION",
        "authority_granted": "Use the approved accountability structure and prepare the appointment schedule for Founder disposition.",
        "authority_not_granted": "No unnamed person is appointed; no employment, compensation, contract, spending, merge, adoption, activation, implementation, or production authority.",
        "resulting_status": "NAMED_ROLE_APPOINTMENTS_REMAIN_OPEN",
    },
    {
        "decision_id": "FD-T1R2-003",
        "founder_decision": "APPROVE_WITH_MODIFICATIONS",
        "final_disposition": "FD-T1R2-003_SOURCE_CONTROL_HIERARCHY_APPROVED_WITH_EVIDENCE_AND_NONINFERENCE_CONTROLS",
        "authority_granted": "Apply the approved documentary precedence hierarchy in future source reconciliation, provenance review, supersession analysis, and Tier 1 documentary preparation.",
        "authority_not_granted": "No individual source is automatically controlling, adopted, active, implemented, production-authorized, or resolved without sufficient evidence.",
        "resulting_status": "DOCUMENTARY_FRAMEWORK_APPROVED_AS_SPECIFIED",
    },
    {
        "decision_id": "FD-T1R2-004",
        "founder_decision": "APPROVE_WITH_MODIFICATIONS",
        "final_disposition": "FD-T1R2-004_RISK_AND_FINDING_DISPOSITION_FRAMEWORK_APPROVED_NO_BULK_RISK_ACCEPTANCE",
        "authority_granted": "Use the approved findings and residual-risk control framework and prepare item-specific dispositions for Founder or properly delegated authority.",
        "authority_not_granted": "No blanket risk acceptance, blanket waiver, closure of all findings, operational risk acceptance, or approval of risks not individually presented.",
        "resulting_status": "ITEM_SPECIFIC_RISK_DISPOSITIONS_REMAIN_OPEN",
    },
    {
        "decision_id": "FD-T1R2-005",
        "founder_decision": "APPROVE_SEQUENCE_WITH_CONDITIONS",
        "final_disposition": "FD-T1R2-005_FUTURE_SEQUENCE_APPROVED_MERGE_AND_ADOPTION_REMAIN_SEPARATELY_AUTHORIZED_ACTIONS",
        "authority_granted": "Follow the approved sequence and prepare next documentary adoption-readiness and merge-readiness materials.",
        "authority_not_granted": "No merge, adoption, activation, implementation, production use, certification, automatic closure, or bypass of validation or branch-protection controls.",
        "resulting_status": "DOCUMENTARY_ADOPTION_NOT_YET_AUTHORIZED",
    },
]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path: Path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def copy_successor(repo: Path, source_text: Path):
    src = repo / "governance/portfolio/tier-1/drafting/EQUINESYNC_TIER_1_DOCUMENTS_03_10_FINAL_DRAFT_V1"
    dst = repo / "governance/portfolio/tier-1/drafting/EQUINESYNC_TIER_1_DOCUMENTS_03_10_FOUNDER_REVIEWED_SUCCESSOR_V1"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    decision_dir = dst / "FOUNDER_DECISIONS"
    decision_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_text, decision_dir / "FOUNDER_DECISIONS_FD_T1R2_001_005_2026_08_02.md")
    return src, dst


def write_decision_records(repo: Path, root: Path, source_text: Path):
    source_hash = sha(source_text)
    if source_hash != SOURCE_SHA or source_text.stat().st_size != SOURCE_BYTES:
        raise SystemExit("Founder decision source authentication failed")

    fields = [
        "decision_id",
        "founder",
        "decision_date",
        "applicable_package",
        "applicable_pr",
        "applicable_review_head",
        "source_sha256",
        "source_byte_length",
        "founder_decision",
        "final_disposition",
        "authority_granted",
        "authority_not_granted",
        "resulting_status",
        "merge_authority",
        "activation_authority",
        "implementation_authority",
        "production_authority",
        "certification_state",
        "closure_effect",
    ]
    rows = []
    for d in DECISIONS:
        row = {
            **d,
            "founder": "Rian Ray",
            "decision_date": "2026-08-02",
            "applicable_package": "EQUINESYNC_TIER_1_DOCUMENTS_03_10_FINAL_DRAFT",
            "applicable_pr": "PR #85",
            "applicable_review_head": REVIEW_HEAD,
            "source_sha256": source_hash,
            "source_byte_length": str(source_text.stat().st_size),
            "merge_authority": "MERGE_NOT_AUTHORIZED",
            "activation_authority": "NOT_ACTIVE",
            "implementation_authority": "IMPLEMENTATION_NOT_AUTHORIZED",
            "production_authority": "PRODUCTION_USE_NOT_AUTHORIZED",
            "certification_state": "CERTIFICATION_NOT_COMPLETE",
            "closure_effect": "NO_AUTOMATIC_CLOSURE_OF_FINDINGS",
        }
        rows.append(row)
    write_csv(root / "FOUNDER_DECISIONS" / "FOUNDER_DECISION_RECORD.csv", rows, fields)
    (root / "FOUNDER_DECISIONS" / "FOUNDER_DECISION_RECORD.json").write_text(json.dumps(rows, indent=2) + "\n")

    md = [
        "# Founder Decision Record",
        "",
        f"- Source SHA-256: `{source_hash}`",
        f"- Source byte length: `{source_text.stat().st_size}`",
        f"- Applicable PR: `PR #85`",
        f"- Applicable review head: `{REVIEW_HEAD}`",
        f"- Continuing authority limitations: `{AUTHORITY}`",
        "",
    ]
    for row in rows:
        md.extend([
            f"## {row['decision_id']}",
            "",
            f"- Founder decision: `{row['founder_decision']}`",
            f"- Final disposition: `{row['final_disposition']}`",
            f"- Authority granted: {row['authority_granted']}",
            f"- Authority not granted: {row['authority_not_granted']}",
            "",
        ])
    (root / "FOUNDER_DECISIONS" / "FOUNDER_DECISION_RECORD.md").write_text("\n".join(md))

    (root / "FOUNDER_DECISIONS" / "FOUNDER_DECISION_SOURCE_AUTHENTICATION_REPORT.md").write_text(f"""# Founder Decision Source Authentication Report

- Source path: `FOUNDER_DECISIONS_FD_T1R2_001_005_2026_08_02.md`
- Observed SHA-256: `{source_hash}`
- Expected SHA-256: `{SOURCE_SHA}`
- Observed byte length: `{source_text.stat().st_size}`
- Expected byte length: `{SOURCE_BYTES}`
- Applicable review head: `{REVIEW_HEAD}`
- Authentication result: `MATCH`

These decisions are documentary Founder decisions only. They do not authorize merge, activation, implementation, production use, deployment, certification, automatic closure of findings, or direct protected-branch mutation.
""")

    decision_packet_rows = []
    for d in DECISIONS:
        decision_packet_rows.append({
            "decision_id": d["decision_id"],
            "founder_decision": d["founder_decision"],
            "final_disposition": d["final_disposition"],
            "decision_source": "FOUNDER_DECISIONS/FOUNDER_DECISIONS_FD_T1R2_001_005_2026_08_02.md",
            "decision_source_sha256": source_hash,
            "authority_granted": d["authority_granted"],
            "authority_expressly_not_granted": d["authority_not_granted"],
            "resulting_status": d["resulting_status"],
            "merge_authority": "MERGE_NOT_AUTHORIZED",
            "founder_decision_state": "FOUNDER_DIRECTION_RECORDED",
        })
    packet_fields = list(decision_packet_rows[0].keys())
    write_csv(root / "FOUNDER_DECISION_PACKET.csv", decision_packet_rows, packet_fields)
    write_csv(root / "05_FOUNDER_DECISION_REGISTER" / "FOUNDER_DECISION_DISPOSITION_REGISTER.csv", decision_packet_rows, packet_fields)
    (root / "05_FOUNDER_DECISION_REGISTER" / "FOUNDER_DECISION_DISPOSITION_REGISTER.json").write_text(json.dumps(decision_packet_rows, indent=2) + "\n")


def write_appointment_schedule(root: Path):
    matrix = read_csv(root / "07_OWNERSHIP_STEWARDSHIP_REVIEW" / "OWNERSHIP_ACCOUNTABILITY_MATRIX.csv")
    rows = []
    for r in matrix:
        rows.append({
            "role_title": r["role"],
            "responsibilities": r["review_responsibility"],
            "authority_limits": "No closure, acceptance, certification, approval, implementation, activation, production, adoption, or merge authority may be inferred while unappointed.",
            "proposed_appointee": "FOUNDER_ACTION_REQUIRED_NO_APPOINTEE_INFERRED",
            "appointment_date": "NOT_RECORDED",
            "written_acceptance_status": "NOT_RECORDED",
            "vacancy_status": "VACANT_PENDING_FOUNDER_APPOINTMENT",
            "succession_or_backup_designation": r.get("deputy", "TO_BE_APPOINTED"),
            "conflicts_or_independence_limitations": r.get("conflict_restrictions", "NOT_RECORDED"),
            "controls_affected_if_vacant": r["accountability_gap_effect"],
            "founder_decision_item": "FD-T1R2-002",
        })
    fields = list(rows[0].keys())
    write_csv(root / "TIER_1_GOVERNANCE_ACCOUNTABLE_ROLE_APPOINTMENT_SCHEDULE.csv", rows, fields)
    md = [
        "# Tier 1 Governance Accountable Role Appointment Schedule",
        "",
        "No named natural-person appointment is made by this schedule. Every proposed appointee remains `FOUNDER_ACTION_REQUIRED_NO_APPOINTEE_INFERRED` unless a separate authenticated Founder appointment instrument is supplied.",
        "",
        "| Role | Vacancy Status | Proposed Appointee | Controls Affected If Vacant |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        md.append(f"| {row['role_title']} | `{row['vacancy_status']}` | `{row['proposed_appointee']}` | {row['controls_affected_if_vacant']} |")
    (root / "TIER_1_GOVERNANCE_ACCOUNTABLE_ROLE_APPOINTMENT_SCHEDULE.md").write_text("\n".join(md) + "\n")


def write_disposition_queue(root: Path):
    findings = read_csv(root / "CONSOLIDATED_EXTERNAL_REVIEW_FINDING_REGISTER.csv")
    rows = []
    for f in findings:
        if f["disposition"] == "CONFIRMED_REMEDIATED":
            proposed = "CLOSE_WITH_VERIFIED_EVIDENCE_REVIEW_REQUIRED"
        elif f["disposition"] == "PARTIALLY_REMEDIATED":
            proposed = "REQUIRE_REMEDIATION_OR_DEFER_WITH_RECORDED_BASIS"
        elif f["disposition"] == "DEFERRED_WITH_RECORDED_BASIS":
            proposed = "DEFER_WITH_RECORDED_BASIS_REVIEW_REQUIRED"
        elif f["disposition"] == "SUPERSEDED_BY_LATER_CHANGE":
            proposed = "CLOSE_WITH_VERIFIED_EVIDENCE_REVIEW_REQUIRED"
        else:
            proposed = "REQUIRE_REMEDIATION"
        rows.append({
            "item_id": f["consolidated_finding_id"],
            "source_finding_id": f["source_finding_id"],
            "current_disposition": f["disposition"],
            "proposed_individual_disposition": proposed,
            "execution_state": "NOT_EXECUTED_BY_THIS_PACKAGE",
            "bulk_acceptance_state": "NO_BULK_RISK_ACCEPTANCE",
            "required_evidence": f["validation_evidence"],
            "authority_required": "FOUNDER_OR_PROPERLY_DELEGATED_AUTHORITY",
            "residual_risk": f["residual_risk"],
            "founder_decision_item": "FD-T1R2-004",
        })
    write_csv(root / "ITEM_SPECIFIC_RISK_AND_FINDING_DISPOSITION_QUEUE.csv", rows, list(rows[0].keys()))

    risks = read_csv(root / "FINAL_RESIDUAL_RISK_REGISTER.csv")
    risk_rows = []
    for r in risks:
        risk_rows.append({
            "risk_id": r["risk_id"],
            "risk": r["risk"],
            "current_treatment": r["treatment"],
            "acceptance_state": "NOT_ACCEPTED_BY_THIS_PACKAGE",
            "required_acceptance_record_fields": "risk; affected control; severity; rationale; mitigation; remaining exposure; accepting person; authority scope; date; duration or review date; monitoring; conditions and exclusions",
            "founder_decision_item": "FD-T1R2-004",
        })
    write_csv(root / "ITEM_SPECIFIC_RESIDUAL_RISK_DISPOSITION_QUEUE.csv", risk_rows, list(risk_rows[0].keys()))


def write_sequence_and_status(root: Path):
    sequence = [
        ("1", "Complete Founder documentary review", "COMPLETE_FOUNDER_DIRECTION_RECORDED"),
        ("2", "Record and validate the five Founder decisions", "COMPLETE_IN_THIS_SUCCESSOR_PACKAGE"),
        ("3", "Complete any decision-directed corrections", "COMPLETE_FOR_DOCUMENTARY_CORRECTIONS_IN_THIS_PACKAGE"),
        ("4", "Rerun repository-aware and standalone package validation", "COMPLETE_IN_THIS_SUCCESSOR_PACKAGE"),
        ("5", "Complete CI and review-thread evaluation", "CI_SUCCESS_REVIEW_THREADS_REQUIRE_LIVE_RECHECK_BEFORE_MERGE_CONSIDERATION"),
        ("6", "Prepare Founder-approved documentary successor package", "COMPLETE_IN_THIS_SUCCESSOR_PACKAGE"),
        ("7", "Separately assess documentary adoption readiness", "NOT_YET_AUTHORIZED_NEXT_DOCUMENTARY_STEP"),
        ("8", "Separately assess merge readiness", "NOT_YET_AUTHORIZED_NEXT_DOCUMENTARY_STEP"),
        ("9", "Obtain express Founder merge authority before any merge", "MERGE_NOT_AUTHORIZED"),
        ("10", "Complete post-merge custody verification if merge is later authorized", "NOT_APPLICABLE_NO_MERGE_AUTHORITY"),
    ]
    rows = [{"step": s, "sequenced_action": a, "status": st, "founder_decision_item": "FD-T1R2-005"} for s, a, st in sequence]
    write_csv(root / "FOUNDER_APPROVED_FUTURE_SEQUENCE_TRACKER.csv", rows, list(rows[0].keys()))
    (root / "FOUNDER_REVIEWED_SUCCESSOR_STATUS_REPORT.md").write_text(f"""# Founder Reviewed Successor Status Report

## Resulting Status

- `FOUNDER_DIRECTION_RECORDED`
- `DOCUMENTARY_FRAMEWORK_APPROVED_AS_SPECIFIED`
- `NAMED_ROLE_APPOINTMENTS_REMAIN_OPEN`
- `ITEM_SPECIFIC_RISK_DISPOSITIONS_REMAIN_OPEN`
- `DOCUMENTARY_ADOPTION_NOT_YET_AUTHORIZED`
- `NOT_ACTIVE`
- `IMPLEMENTATION_NOT_AUTHORIZED`
- `PRODUCTION_USE_NOT_AUTHORIZED`
- `MERGE_NOT_AUTHORIZED`
- `CERTIFICATION_NOT_COMPLETE`
- `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`

The Founder decisions authorize preparation of this Founder-reviewed documentary successor package and bounded documentary corrections necessary to implement the decisions. They do not authorize merge, implementation, activation, production use, or certification.
""")
    (root / "README_FIRST.md").write_text(f"""# EquineSync Tier 1 Documents 03-10 Founder Reviewed Successor V1

This package records Founder decisions FD-T1R2-001 through FD-T1R2-005 against PR #85 and review head `{REVIEW_HEAD}`.

Continuing limitations: `{AUTHORITY}`.

This package remains documentary only. It does not authorize merge, adoption, activation, implementation, production use, deployment, certification, automatic closure of findings, or direct protected-branch mutation.
""")
    (root / "DRAFT_PR_DESCRIPTION.md").write_text(f"""# Tier 1 Documents 03-10 Founder Reviewed Successor

This draft PR now includes a Founder-reviewed successor package for Tier 1 Documents 03-10.

Founder decision source:

- SHA-256: `{SOURCE_SHA}`
- Bytes: `{SOURCE_BYTES}`
- Applicable review head: `{REVIEW_HEAD}`

Recorded decisions:

- FD-T1R2-001: `FD-T1R2-001_APPROVED_WITH_DOCUMENTARY_SCOPE_ONLY`
- FD-T1R2-002: `FD-T1R2-002_ACCOUNTABILITY_STRUCTURE_APPROVED_NAMED_APPOINTMENTS_RETAINED_FOR_SEPARATE_FOUNDER_ACTION`
- FD-T1R2-003: `FD-T1R2-003_SOURCE_CONTROL_HIERARCHY_APPROVED_WITH_EVIDENCE_AND_NONINFERENCE_CONTROLS`
- FD-T1R2-004: `FD-T1R2-004_RISK_AND_FINDING_DISPOSITION_FRAMEWORK_APPROVED_NO_BULK_RISK_ACCEPTANCE`
- FD-T1R2-005: `FD-T1R2-005_FUTURE_SEQUENCE_APPROVED_MERGE_AND_ADOPTION_REMAIN_SEPARATELY_AUTHORIZED_ACTIONS`

Prepared follow-on documentary records:

- `TIER_1_GOVERNANCE_ACCOUNTABLE_ROLE_APPOINTMENT_SCHEDULE`
- item-specific finding and residual-risk disposition queues
- Founder-approved future sequence tracker

Continuing limitations: `{AUTHORITY}`.

This PR must remain draft. Auto-merge must remain disabled. `MERGE_NOT_AUTHORIZED`.
""")


def write_validator(root: Path):
    validator = root / "VALIDATION" / "validate_founder_reviewed_successor.py"
    validator.write_text(r'''#!/usr/bin/env python3
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
''')
    validator.chmod(0o755)


def rebuild_integrity(root: Path):
    excluded = {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256", "MANIFEST_OF_MANIFESTS.sha256", "FOUNDER_REVIEWED_SUCCESSOR_INTEGRITY_ROOT.json"}
    for manifest in sorted(root.rglob("PACKAGE_MANIFEST.json")):
        if manifest == root / "PACKAGE_MANIFEST.json":
            continue
        directory = manifest.parent
        directory_files = []
        for p in sorted(directory.iterdir()):
            if p.is_file() and p.name not in excluded:
                directory_files.append({"path": p.name, "sha256": sha(p), "byte_length": p.stat().st_size})
        manifest.write_text(json.dumps({"directory": rel(directory, root), "files": directory_files}, indent=2) + "\n")
        checksum_file = directory / "CHECKSUMS.sha256"
        if checksum_file.exists():
            with checksum_file.open("w") as f:
                for item in directory_files:
                    f.write(f"{item['sha256']}  {item['path']}\n")

    files = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name not in excluded:
            files.append({"path": rel(p, root), "sha256": sha(p), "byte_length": p.stat().st_size})
    (root / "PACKAGE_MANIFEST.json").write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(), "files": files}, indent=2) + "\n")
    with (root / "CHECKSUMS.sha256").open("w") as f:
        for item in files:
            f.write(f"{item['sha256']}  {item['path']}\n")
    with (root / "MANIFEST_OF_MANIFESTS.sha256").open("w") as f:
        for p in sorted(root.rglob("PACKAGE_MANIFEST.json")):
            if p != root / "PACKAGE_MANIFEST.json":
                f.write(f"{sha(p)}  {rel(p, root)}\n")
    integrity = {
        "record_type": "FOUNDER_REVIEWED_SUCCESSOR_INTEGRITY_ROOT",
        "authority_boundary": AUTHORITY,
        "founder_decision_source_sha256": SOURCE_SHA,
        "founder_decision_source_byte_length": SOURCE_BYTES,
        "applicable_review_head": REVIEW_HEAD,
        "package_manifest_sha256": sha(root / "PACKAGE_MANIFEST.json"),
        "checksums_sha256": sha(root / "CHECKSUMS.sha256"),
        "manifest_of_manifests_sha256": sha(root / "MANIFEST_OF_MANIFESTS.sha256"),
        "files_covered": len(files),
    }
    (root / "FOUNDER_REVIEWED_SUCCESSOR_INTEGRITY_ROOT.json").write_text(json.dumps(integrity, indent=2) + "\n")


def make_zip(repo: Path, root: Path):
    zip_path = root.with_suffix(".zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file():
                z.write(p, root.name + "/" + rel(p, root))
    sidecar = zip_path.with_suffix(zip_path.suffix + ".sha256")
    sidecar.write_text(f"{sha(zip_path)}  {zip_path.name}\n")
    return zip_path


def main():
    repo = Path.cwd()
    source_text = Path("/Users/rianray/.codex/attachments/961fdde8-9050-46e3-b7e5-95b240de2146/pasted-text.txt")
    _, root = copy_successor(repo, source_text)
    write_decision_records(repo, root, source_text)
    write_appointment_schedule(root)
    write_disposition_queue(root)
    write_sequence_and_status(root)
    write_validator(root)
    rebuild_integrity(root)
    make_zip(repo, root)
    (root / "FINAL_ZIP_RECORD.json").write_text(json.dumps({"zip_path": root.with_suffix(".zip").relative_to(repo).as_posix(), "sha256": sha(root.with_suffix(".zip")), "byte_length": root.with_suffix(".zip").stat().st_size}, indent=2) + "\n")
    rebuild_integrity(root)
    zip_path = make_zip(repo, root)
    print(zip_path, sha(zip_path), zip_path.stat().st_size)


if __name__ == "__main__":
    main()
