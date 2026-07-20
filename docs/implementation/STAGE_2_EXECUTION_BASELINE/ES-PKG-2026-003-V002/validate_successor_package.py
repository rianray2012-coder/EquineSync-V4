#!/usr/bin/env python3
"""Static package-control validator. Does not execute EquineSync."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKAGE_ID = "ES-PKG-2026-003-V002"
PREDECESSOR_ID = "ES-PKG-2026-002-V001"
PREDECESSOR_SHA = "268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f"
COMMIT = "acb518ea5a160820e64681ff95a16b010fe1156c"

DRAFT_REQUIRED = {
    "PRE_CHANGE_BASELINE.md", "PRE_CHANGE_BASELINE.json",
    "MIAP_TERMINOLOGY_AND_AUTHORITY_CONFIRMATION.md", "MIAP_TERMINOLOGY_INTEGRITY_REGISTER.csv",
    "EXECUTION_BASELINE_GAP_ANALYSIS.md", "EXECUTION_BASELINE_GAP_ANALYSIS.json",
    "F0002_INDEPENDENT_DISPOSITION.md", "F0002_INDEPENDENT_DISPOSITION.json",
    "F0002_EVIDENCE_REGISTER.md", "F0002_EVIDENCE_REGISTER.json",
    "IDENTITY_EXECUTION_MAPPING.md", "IDENTITY_EXECUTION_MAPPING.json", "IDENTITY_TRACEABILITY_MATRIX.csv", "IDENTITY_UNRESOLVED_EVIDENCE_REGISTER.md",
    "RELATIONSHIPS_EXECUTION_MAPPING.md", "RELATIONSHIPS_EXECUTION_MAPPING.json", "RELATIONSHIPS_TRACEABILITY_MATRIX.csv", "RELATIONSHIPS_UNRESOLVED_EVIDENCE_REGISTER.md",
    "AUTHORIZATION_EXECUTION_MAPPING.md", "AUTHORIZATION_EXECUTION_MAPPING.json", "AUTHORIZATION_TRACEABILITY_MATRIX.csv", "AUTHORIZATION_UNRESOLVED_EVIDENCE_REGISTER.md",
    "GP05_IMPLEMENTATION_STATUS_REPORT.md", "GP05_IMPLEMENTATION_STATUS_REPORT.json", "GP05_IMPLEMENTATION_PLAN.md", "GP05_IMPLEMENTATION_PLAN.json", "GP05_TRACEABILITY_MATRIX.csv",
    "EXECUTION_ENVIRONMENT_CONTRACT.md", "EXECUTION_ENVIRONMENT_CONTRACT.json", "ENVIRONMENT_VARIABLE_REGISTER.md", "ENVIRONMENT_VARIABLE_REGISTER.json",
    "DEPENDENCY_INSTALL_SPECIFICATION.md", "BUILD_SPECIFICATION.md", "RUNTIME_SPECIFICATION.md", "VALIDATION_COMMAND_REGISTER.md", "VALIDATION_COMMAND_REGISTER.json",
    "EXECUTION_FIXTURE_REGISTER.md", "EXECUTION_FIXTURE_REGISTER.json", "EXECUTION_EXPECTED_RESULTS.md", "EXECUTION_EXPECTED_RESULTS.json", "EXECUTION_ORACLE_REGISTER.md", "EXECUTION_ORACLE_REGISTER.json", "NEGATIVE_TEST_REGISTER.md", "NEGATIVE_TEST_REGISTER.json",
    "CP3_EXECUTION_MAPPING.md", "CP3_EXECUTION_MAPPING.json", "CP3_GAP_REGISTER.md", "CP3_GAP_REGISTER.json",
    "EXECUTION_ROLLBACK_PLAN.md", "EXECUTION_ROLLBACK_PLAN.json", "EXECUTION_CLEANUP_PLAN.md", "EXECUTION_CLEANUP_PLAN.json", "EXECUTION_EVIDENCE_CAPTURE_PLAN.md", "EXECUTION_EVIDENCE_CAPTURE_PLAN.json",
    "ATLAS_COMPLETION_REPORT.md", "ATLAS_COMPLETION_REPORT.json", "ATLAS_READINESS_MATRIX.csv",
    "SOURCE_EVIDENCE_REGISTER.csv", "SOURCE_EVIDENCE_REGISTER.json", "FOUNDER_AUTHORIZATION_BOUNDARY.md", "ASSURANCE_STATEMENT.md", "PREDECESSOR_REFERENCE_RECORD.md", "IMMUTABLE_BASELINE_RECORD.md", "PACKAGE_STATUS_RECORD.md", "README.md", "validate_successor_package.py",
    "SOURCE_EVIDENCE_VERIFICATION.md", "SOURCE_EVIDENCE_VERIFICATION.json",
    "F0002_RAW_MACHINE_EVIDENCE.md", "F0002_RAW_MACHINE_EVIDENCE.json",
    "DRAFT_REVIEW_SNAPSHOT_SHA256SUMS.txt", "DRAFT_REVIEW_SNAPSHOT_RECORD.md", "DRAFT_REVIEW_SNAPSHOT_RECORD.json",
}

FINAL_REQUIRED = DRAFT_REQUIRED | {
    "SUCCESSOR_PACKAGE_INDEX.md", "SUCCESSOR_PACKAGE_INDEX.json", "SUCCESSOR_PACKAGE_MANIFEST.md", "SUCCESSOR_PACKAGE_MANIFEST.json", "SUCCESSOR_PACKAGE_SHA256SUMS.txt",
    "SUCCESSOR_PACKAGE_CHANGE_MANIFEST.md", "SUCCESSOR_PACKAGE_CHANGE_MANIFEST.json", "SUCCESSOR_PACKAGE_EXCLUDED_FILES_REGISTER.md",
    "SUCCESSOR_PACKAGE_FINDINGS_REGISTER.md", "SUCCESSOR_PACKAGE_FINDINGS_REGISTER.json", "SOURCE_TO_OUTPUT_TRACEABILITY.md", "SOURCE_TO_OUTPUT_TRACEABILITY.json", "REVIEW_EVIDENCE_REGISTER.md", "EXACT_FILE_INVENTORY.json",
    "SUCCESSOR_PACKAGE_MACHINE_VALIDATION.md", "SUCCESSOR_PACKAGE_MACHINE_VALIDATION.json", "SUCCESSOR_PACKAGE_CLEAN_EXTRACTION_VERIFICATION.md", "SUCCESSOR_PACKAGE_CLEAN_EXTRACTION_VERIFICATION.json",
    "SUCCESSOR_PACKAGE_SEGREGATED_REVIEW.md", "SUCCESSOR_PACKAGE_SEGREGATED_FINDINGS.json", "SUCCESSOR_PACKAGE_ADVERSARIAL_REVIEW.md", "SUCCESSOR_PACKAGE_ADVERSARIAL_FINDINGS.json", "SUCCESSOR_PACKAGE_FINDING_RECONCILIATION.md", "SUCCESSOR_PACKAGE_FINDING_RECONCILIATION.json",
    "F0001_READINESS_DETERMINATION.md", "F0001_READINESS_DETERMINATION.json",
}


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["draft", "final"], default="final")
    ap.add_argument("--require-source-recompute", action="store_true")
    ap.add_argument("--source-repository", type=Path)
    ap.add_argument("--predecessor-zip", type=Path)
    args = ap.parse_args()
    checks: list[dict[str, object]] = []
    errors: list[str] = []

    def check(name: str, ok: bool, detail: object) -> None:
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
        if not ok:
            errors.append(f"{name}: {detail}")

    files = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file())
    file_set = set(files)
    required = FINAL_REQUIRED if args.phase == "final" else DRAFT_REQUIRED
    check("required_outputs", required <= file_set, {"present": len(required & file_set), "required": len(required), "missing": sorted(required-file_set)})
    check("no_symlinks", not any(p.is_symlink() for p in ROOT.rglob("*")), "package tree")
    check("path_traversal", all(not p.startswith("/") and ".." not in Path(p).parts for p in files), "relative normalized paths")
    check("case_collisions", len({p.casefold() for p in files}) == len(files), "case-folded paths unique")
    check("duplicate_paths", len(files) == len(file_set), len(files))

    json_ok = True
    for p in ROOT.rglob("*.json"):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:
            json_ok = False
            errors.append(f"json:{p.name}:{exc}")
    check("json_parsing", json_ok, sum(1 for _ in ROOT.rglob("*.json")))

    csv_ok = True
    for p in ROOT.rglob("*.csv"):
        rows = list(csv.reader(p.open(newline="", encoding="utf-8-sig")))
        if not rows or any(len(r) != len(rows[0]) for r in rows):
            csv_ok = False
            errors.append(f"csv_width:{p.name}")
    check("csv_structure", csv_ok, sum(1 for _ in ROOT.rglob("*.csv")))

    snapshot_record=json.loads((ROOT/"DRAFT_REVIEW_SNAPSHOT_RECORD.json").read_text())
    snapshot_lines=(ROOT/"DRAFT_REVIEW_SNAPSHOT_SHA256SUMS.txt").read_text().splitlines()
    snapshot_bad=[]; snapshot_paths=[]
    for line in snapshot_lines:
        try: digest,rel=line.split("  ",1)
        except ValueError: snapshot_bad.append(line); continue
        snapshot_paths.append(rel); path=ROOT/rel
        if not path.is_file() or sha(path)!=digest: snapshot_bad.append(rel)
    snapshot_manifest_sha=sha(ROOT/"DRAFT_REVIEW_SNAPSHOT_SHA256SUMS.txt")
    check("draft_snapshot_recomputation",not snapshot_bad and len(snapshot_paths)==len(set(snapshot_paths))==snapshot_record["snapshot_file_count"] and snapshot_manifest_sha==snapshot_record["snapshot_manifest_sha256"],{"listed":len(snapshot_paths),"bad":snapshot_bad[:10],"manifest_sha256":snapshot_manifest_sha})

    gaps = json.loads((ROOT/"EXECUTION_BASELINE_GAP_ANALYSIS.json").read_text())["gaps"]
    gap_ids = [g["identifier"] for g in gaps]
    gap_fields = {"identifier","related_finding","affected_domain_or_workflow","present_status","source_evidence","missing_evidence","missing_implementation","required_remediation","validation_method","closure_criteria","responsible_review_function","blocks_f0001","documentation_alone_may_resolve","code_implementation_required","future_founder_authorization_required"}
    check("gap_schema", len(gaps)==31 and all(gap_fields <= set(g) for g in gaps), len(gaps))
    check("gap_identifiers", len(gap_ids)==len(set(gap_ids)) and gap_ids==[f"S2-GAP-{i:03d}" for i in range(1,32)], gap_ids[:2]+gap_ids[-2:])

    id_sets = []
    for filename, key, field in [
        ("IDENTITY_EXECUTION_MAPPING.json","coverage","item_id"),("RELATIONSHIPS_EXECUTION_MAPPING.json","coverage","item_id"),("AUTHORIZATION_EXECUTION_MAPPING.json","coverage","item_id"),
        ("VALIDATION_COMMAND_REGISTER.json","commands","command_id"),("EXECUTION_FIXTURE_REGISTER.json","fixtures","fixture_id"),("EXECUTION_ORACLE_REGISTER.json","oracles","oracle_id"),("NEGATIVE_TEST_REGISTER.json","tests","test_id"),("CP3_EXECUTION_MAPPING.json","suites","suite_id"),
    ]:
        rows=json.loads((ROOT/filename).read_text())[key]; ids=[r[field] for r in rows]
        id_sets.extend(ids); check(f"unique_{field}_{filename}",len(ids)==len(set(ids)),len(ids))
    check("all_control_ids_unique",len(id_sets)==len(set(id_sets)),len(id_sets))

    parity_bad=[]; parity_pairs=0
    def controlled_ids(value: object, key: str="") -> set[str]:
        found:set[str]=set()
        if isinstance(value,dict):
            for k,v in value.items(): found |= controlled_ids(v,k)
        elif isinstance(value,list):
            for v in value: found |= controlled_ids(v,key)
        elif isinstance(value,str) and (key=="identifier" or key.endswith("_id")):
            if re.fullmatch(r"[A-Z0-9][A-Z0-9._-]+",value): found.add(value)
        return found
    for jp in ROOT.glob("*.json"):
        mp=jp.with_suffix(".md")
        if not mp.is_file(): continue
        if jp.name=="SOURCE_EVIDENCE_VERIFICATION.json": continue
        ids=controlled_ids(json.loads(jp.read_text()))
        if not ids: continue
        parity_pairs+=1; md=mp.read_text(errors="ignore")
        missing=sorted(v for v in ids if v not in md)
        if missing: parity_bad.append({"pair":jp.stem,"missing_ids":missing[:20]})
    check("paired_format_identifier_parity",not parity_bad,{"pairs":parity_pairs,"bad":parity_bad})

    cp3=json.loads((ROOT/"CP3_EXECUTION_MAPPING.json").read_text())["suites"]
    allowed={"AVAILABLE_EXECUTABLE","AVAILABLE_INCOMPLETE","DOCUMENTED_NOT_IMPLEMENTED","NOT_FOUND","BLOCKED_BY_ENVIRONMENT","BLOCKED_BY_DEPENDENCY"}
    check("cp3_status_values",all(r["status"] in allowed for r in cp3),sorted({r["status"] for r in cp3}))
    check("cp3_denominator",len(cp3)==13,"13 suites / 52 documentary scenarios")

    active_files=[ROOT/p for p in files if Path(p).suffix.lower() in {".md",".json",".csv",".txt",".py"}]
    content_files=[p for p in active_files if p.name != "validate_successor_package.py"]
    active="\n".join(p.read_text(errors="ignore") for p in active_files)
    content="\n".join(p.read_text(errors="ignore") for p in content_files)
    check("package_identity",PACKAGE_ID in active and PREDECESSOR_ID in active,"successor/predecessor")
    check("baseline_identity",COMMIT in active and PREDECESSOR_SHA in active,"immutable anchors")
    check("no_absolute_local_paths",not re.search(r"/(?:Users|private|var/folders|home)/",active),"local paths prohibited")
    check("no_unresolved_placeholders",not re.search(r"\b(?:TODO|TBD|FIXME|CHANGEME|INSERT HERE|PLACEHOLDER)\b",content,re.I),"UNKNOWN is the controlled missing-evidence value")
    check("no_secret_values",not re.search(r"\b(?:sk|rk|pk)_(?:live|test)_[A-Za-z0-9]+|demo1234",content),"names only")
    err_term = "MA" + "IP"
    term_violations=[]
    for p in active_files:
        rel=p.relative_to(ROOT).as_posix()
        if err_term in p.read_text(errors="ignore") and rel not in {"MIAP_TERMINOLOGY_INTEGRITY_REGISTER.csv","validate_successor_package.py"}:
            term_violations.append(rel)
    check("terminology_integrity",not term_violations,term_violations)
    confirm=(ROOT/"MIAP_TERMINOLOGY_AND_AUTHORITY_CONFIRMATION.md").read_text()
    check("miap_authority","Product Implementation Atlases operate beneath and within MIAP" in confirm,"PIA beneath MIAP")

    f2=json.loads((ROOT/"F0002_INDEPENDENT_DISPOSITION.json").read_text())
    check("f0002_bounded",f2["recommended_disposition"]=="F0002_READY_FOR_AUTHORIZED_CLOSURE" and f2["closure_effect"]=="CLOSURE_RECOMMENDED_NOT_SELF_CLOSED","recommendation only")
    f2_raw=json.loads((ROOT/"F0002_RAW_MACHINE_EVIDENCE.json").read_text())
    check("f0002_raw_machine_evidence",f2_raw["validation"]=="PASS" and f2_raw["baseline_object_count"]==5228 and f2_raw["missing_objects"]==0 and f2_raw["index_entries"]==3340,"raw output, object integrity, and index capture")
    gp=json.loads((ROOT/"GP05_IMPLEMENTATION_STATUS_REPORT.json").read_text())
    check("gp05_bounded",gp["status"]=="GP05_DOCUMENTED_NOT_IMPLEMENTED" and gp["implementation_authorized"] is False,"no implementation claim")
    prohibited_authority=[
        "Founder-approved ES-IP",
        "Founder-approved GP-05",
        "FOUNDER_CERTIFIED_ESIP",
    ]
    check("gp05_candidate_authority",gp.get("documentary_authority")=="SEALED_INTERNAL_ASSURANCE_CANDIDATE_NOT_FOUNDER_APPROVED" and not any(v.lower() in content.lower() for v in prohibited_authority),"candidate is documentary, not adopted authority")

    source=json.loads((ROOT/"SOURCE_EVIDENCE_REGISTER.json").read_text())
    evidence=source["evidence"]
    evidence_paths={r["path"] for r in evidence}
    source_verify=json.loads((ROOT/"SOURCE_EVIDENCE_VERIFICATION.json").read_text())
    check("source_evidence_verification",source_verify["validation"]=="PASS" and source_verify["row_count"]==source["reviewed_file_count"]==len(evidence) and all(r["status"]=="PASS" for r in source_verify["rows"]),{"rows":len(evidence),"validation":source_verify["validation"]})
    source_verify_md=(ROOT/"SOURCE_EVIDENCE_VERIFICATION.md").read_text()
    source_md_values=[source_verify["validation"],str(source_verify["row_count"]),str(source_verify["repository_rows"]),str(source_verify["nested_candidate_rows"]),source_verify["predecessor_sha256"],source_verify["stage1_sha256"],source_verify["candidate_sha256"],source_verify["miap_sha256"]]
    check("source_verification_md_json_aggregate_parity",all(v in source_verify_md for v in source_md_values),source_md_values)
    source_by_id={r["evidence_id"]:r for r in evidence}
    verification_by_id={r["evidence_id"]:r for r in source_verify["rows"]}
    verification_mismatch=[]
    for eid,row in source_by_id.items():
        captured=verification_by_id.get(eid,{})
        if captured.get("source")!=row["source"] or captured.get("path")!=row["path"] or captured.get("expected_sha256")!=row["sha256"] or captured.get("expected_blob")!=row["git_blob_sha1"]:
            verification_mismatch.append(eid)
    check("register_to_verification_row_equality",set(source_by_id)==set(verification_by_id) and not verification_mismatch,verification_mismatch[:20])
    expected_chain={
        "predecessor_sha256": PREDECESSOR_SHA,
        "stage1_sha256": "78f433ac5619861fd99b73a725507292c69433f7215c22d076ea72df888b1d33",
        "candidate_sha256": "e46fc2cc70ae994061937e5e90cb502d9453d197bb0f3322f433db1c3bfffd92",
        "miap_sha256": "5e494c785feb6b8a2dad9d8289fc1ac5af254223bd88cf439611773a4082314f",
    }
    check("nested_archive_custody",all(source_verify.get(k)==v for k,v in expected_chain.items()) and source_verify.get("candidate_member_count")==343,expected_chain)
    commands=json.loads((ROOT/"VALIDATION_COMMAND_REGISTER.json").read_text())["commands"]
    command_paths=sorted({p for row in commands for p in row.get("source_evidence_paths",[])})
    check("command_source_reconciliation",all(p in evidence_paths for p in command_paths),{"command_paths":len(command_paths),"missing":sorted(set(command_paths)-evidence_paths)})
    required_command_paths={
        "backend/core/rf1_data_fences_capability_gates_proof.py",
        "backend/core/rf2_identity_access_migration_proof.py",
        "backend/routes/backlog.py",
        "backend/routes/owner_updates.py",
        "backend/scripts/build_rf1_data_fences_capability_gates_proof.py",
        "backend/scripts/build_rf2_identity_access_migration_proof.py",
        "backend/tests/test_rf1_data_fences_capability_gates.py",
        "docs/ROLE_PERMISSION_MATRIX.md",
        "outputs/build_next_rf2_identity_access_migration.zip",
        "outputs/rf1_data_fences_capability_gates_report.md",
        "outputs/rf2_identity_access_migration_report.md",
    }
    check("required_mapping_sources",required_command_paths<=evidence_paths,sorted(required_command_paths-evidence_paths))
    atlas=json.loads((ROOT/"ATLAS_COMPLETION_REPORT.json").read_text())
    atlas_sections=atlas["sections"]
    atlas_counts={name:sum(r["atlas"]==name for r in atlas_sections) for name in ("Identity","Relationships","Authorization")}
    check("atlas_section_assessment",atlas["section_count_per_atlas"]==33 and atlas["total_section_rows"]==99 and len(atlas_sections)==99 and atlas_counts=={"Identity":33,"Relationships":33,"Authorization":33} and all(r["status"]!="COMPLETE_FOR_INDEPENDENT_REVIEW" for r in atlas_sections),atlas_counts)

    repo=args.source_repository
    if repo is None:
        for parent in ROOT.parents:
            if (parent/".git").exists(): repo=parent; break
    pred_zip=args.predecessor_zip
    if pred_zip is None and repo is not None:
        candidate=repo.parent.parent/"outputs/EquineSync_ES_IP_V1_2_2_Execution_Baseline_Resolution_Package.zip"
        if candidate.is_file(): pred_zip=candidate
    direct_errors=[]; direct_rows=0
    if repo is not None and pred_zip is not None and repo.is_dir() and pred_zip.is_file():
        outer_bytes=pred_zip.read_bytes()
        if hashlib.sha256(outer_bytes).hexdigest()!=PREDECESSOR_SHA: direct_errors.append("predecessor_sha256")
        with zipfile.ZipFile(io.BytesIO(outer_bytes)) as outer:
            outer_names=outer.namelist(); outer_prefix="EquineSync_ES_IP_V1_2_2_Execution_Baseline_Resolution_Package/"
            stage1_member=outer_prefix+"supporting_evidence/source_materials/EquineSync_ES_IP_V1_2_2_Stage_1_Pilot_Exit_Package.zip"
            stage1=outer.read(stage1_member)
            with zipfile.ZipFile(io.BytesIO(stage1)) as s1:
                s1_root="EquineSync_ES_IP_V1_2_2_Stage_1_Pilot_Exit_Package/"
                cand=s1.read(s1_root+"01_frozen_package/source_materials/EquineSync_Implementation_Playbook_V1.2.2_Internal_Assurance_Candidate.zip")
            with zipfile.ZipFile(io.BytesIO(cand)) as cz:
                cand_root="EquineSync_Implementation_Playbook_V1.2.2_Internal_Assurance_Candidate/"
                miap=cz.read(cand_root+"SOURCE_EVIDENCE/EquineSync_MIAP_Controlled_Baseline_Release_V1.0.0.zip")
                for row in evidence:
                    direct_rows+=1; src=row["source"]; expected=row["sha256"]
                    try:
                        if src=="OFFICIAL_REPOSITORY_IMMUTABLE_COMMIT":
                            data=subprocess.run(["git","show",f"{COMMIT}:{row['path']}"],cwd=repo,capture_output=True,check=True).stdout
                            blob=subprocess.run(["git","rev-parse",f"{COMMIT}:{row['path']}"],cwd=repo,text=True,capture_output=True,check=True).stdout.strip()
                            ok=hashlib.sha256(data).hexdigest()==expected and blob==row["git_blob_sha1"]
                        elif src=="SEALED_NESTED_INTERNAL_ASSURANCE_CANDIDATE":
                            rel=row["path"].split("!/",2)[-1]; member=cand_root+rel.removeprefix(cand_root)
                            ok=hashlib.sha256(cz.read(member)).hexdigest()==expected
                        elif src=="SEALED_PREDECESSOR_ES_PKG_2026_002_V001":
                            ok=hashlib.sha256(outer.read(outer_prefix+row["path"])).hexdigest()==expected
                        elif src=="SEALED_PREDECESSOR_CONTAINER": ok=hashlib.sha256(outer_bytes).hexdigest()==expected
                        elif src=="SEALED_NESTED_STAGE1_CONTAINER": ok=hashlib.sha256(stage1).hexdigest()==expected
                        elif src=="SEALED_NESTED_CANDIDATE_CONTAINER": ok=hashlib.sha256(cand).hexdigest()==expected
                        elif src=="SEALED_NESTED_EVIDENCE_CHAIN": ok=hashlib.sha256(miap).hexdigest()==expected
                        else: ok=False
                        if not ok: direct_errors.append(row["evidence_id"])
                    except Exception: direct_errors.append(row["evidence_id"])
    elif args.require_source_recompute:
        direct_errors.append("required_source_material_unavailable")
    check("direct_source_recomputation",not direct_errors,{"mode":"LIVE_RECOMPUTED" if direct_rows else "OFFLINE_CAPTURED_EVIDENCE_ONLY","rows":direct_rows,"errors":direct_errors[:20]})

    if args.phase=="final":
        manifest=json.loads((ROOT/"SUCCESSOR_PACKAGE_MANIFEST.json").read_text())
        listed=[r["path"] for r in manifest["files"]]
        check("manifest_paths_unique",len(listed)==len(set(listed)),len(listed))
        excluded={"SUCCESSOR_PACKAGE_MANIFEST.md","SUCCESSOR_PACKAGE_MANIFEST.json","SUCCESSOR_PACKAGE_SHA256SUMS.txt","SUCCESSOR_PACKAGE_MACHINE_VALIDATION.md","SUCCESSOR_PACKAGE_MACHINE_VALIDATION.json","SUCCESSOR_PACKAGE_CLEAN_EXTRACTION_VERIFICATION.md","SUCCESSOR_PACKAGE_CLEAN_EXTRACTION_VERIFICATION.json"}
        expected=sorted(file_set-excluded)
        check("stable_manifest_coverage",listed==expected,{"listed":len(listed),"expected":len(expected)})
        bad=[r["path"] for r in manifest["files"] if not (ROOT/r["path"]).is_file() or sha(ROOT/r["path"])!=r["sha256"] or (ROOT/r["path"]).stat().st_size!=r["bytes"]]
        check("stable_manifest_hashes",not bad,bad[:10])
        sums=(ROOT/"SUCCESSOR_PACKAGE_SHA256SUMS.txt").read_text().splitlines(); seen=[]; bad=[]
        for line in sums:
            digest,rel=line.split("  ",1); seen.append(rel)
            if not (ROOT/rel).is_file() or sha(ROOT/rel)!=digest: bad.append(rel)
        check("checksum_reconciliation",seen==sorted(file_set-{"SUCCESSOR_PACKAGE_SHA256SUMS.txt"}) and not bad,{"entries":len(seen),"bad":bad[:10]})
        idx=json.loads((ROOT/"EXACT_FILE_INVENTORY.json").read_text())
        check("exact_inventory",[r["path"] for r in idx["files"]]==files,len(files))
        findings=json.loads((ROOT/"SUCCESSOR_PACKAGE_FINDINGS_REGISTER.json").read_text())["findings"]
        required_f={"finding_id","severity","status","title","evidence","required_remediation","closure_authority","blocks_f0001"}
        check("finding_schema",all(required_f<=set(r) for r in findings),len(findings))
        check("finding_ids_unique",len(findings)==len({r["finding_id"] for r in findings}),len(findings))
        ready=json.loads((ROOT/"F0001_READINESS_DETERMINATION.json").read_text())
        check("f0001_disposition",ready["disposition"]=="F0001_REMAINS_OPEN_BLOCKING","not self-closed")
        check("final_disposition",ready["principal_final_disposition"]=="EXECUTION_BASELINE_STILL_NOT_READY" and ready["execution"]=="EXECUTION_NOT_AUTHORIZED","bounded")

    result={"validation":"FAIL" if errors else "PASS","phase":args.phase,"score":f"{sum(c['status']=='PASS' for c in checks)}/{len(checks)}","check_count":len(checks),"errors":errors,"files":len(files),"required_outputs":len(required),"checks":checks}
    print(json.dumps(result,indent=2))
    return 1 if errors else 0


if __name__=="__main__":
    sys.exit(main())
