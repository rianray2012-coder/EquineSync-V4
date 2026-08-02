#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

# Importing a sibling module would otherwise drop a __pycache__ directory into
# the package being validated, which the coverage-universe check would then,
# correctly, report as an uncovered file. The validator must not modify the
# thing it is measuring.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import validator_partb_checks as partb

# Per-document required files. Restored from the V1 per-document validators that
# Revision Round 2 deleted without disclosure (F-16).
PER_DOCUMENT_REQUIRED_FILES = {
    "03_IMPLEMENTATION_TRACEABILITY": [
        "REQUIREMENT_TRACEABILITY_REGISTER.csv", "COVERAGE_METRICS_BY_DOMAIN.csv"],
    "04_AUTHORITY_LIFECYCLE_REGISTER": [
        "AUTHORITY_LIFECYCLE_STATE_REGISTER.csv", "LIFECYCLE_TRANSITION_MATRIX.csv",
        "INVALID_STATE_RULES.csv"],
    "05_FOUNDER_DECISION_REGISTER": ["FOUNDER_DECISION_DISPOSITION_REGISTER.csv"],
    "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS": [
        "FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv",
        "FINDINGS_RISKS_EXCEPTIONS_WAIVERS_SCHEMA_EXEMPLAR.csv",
        "DUPLICATE_AND_STALENESS_ANALYSIS.csv"],
    "07_OWNERSHIP_STEWARDSHIP_REVIEW": [
        "OWNERSHIP_ACCOUNTABILITY_MATRIX.csv", "REVIEW_CALENDAR.csv"],
    "08_SOURCE_RECONCILIATION": [
        "SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv", "SOURCE_DISPOSITION_DASHBOARD.csv",
        "DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv"],
    "09_WORKSTREAM_PR_BRANCH_DISPOSITION": [
        "WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv"],
    "10_CLOSING_AUDIT_PROTOCOL": ["TEMPLATE_INDEX.csv", "AUDIT_REQUIREMENTS_MATRIX.csv"],
}

PARTB_REGISTERS = [
    "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv",
    "03_IMPLEMENTATION_TRACEABILITY/COVERAGE_METRICS_BY_DOMAIN.csv",
    "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv",
    "05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv",
    "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv",
    "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_SCHEMA_EXEMPLAR.csv",
    "07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv",
    "07_OWNERSHIP_STEWARDSHIP_REVIEW/REVIEW_CALENDAR.csv",
    "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv",
    "08_SOURCE_RECONCILIATION/SOURCE_DISPOSITION_DASHBOARD.csv",
    "08_SOURCE_RECONCILIATION/DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv",
    "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv",
    "10_CLOSING_AUDIT_PROTOCOL/AUDIT_REQUIREMENTS_MATRIX.csv",
    "FOUNDER_DECISION_PACKET.csv",
    "UNRESOLVED_ISSUE_REGISTER.csv",
]

# The principal per-document narrative in each document directory.
NARRATIVE_GLOB = "EQUINESYNC_*_REVISION_ROUND_2_V1.md"

PACKAGE_NAME = "EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V1"
REQUIRED_FILES = [
    "README_FIRST.md",
    "SHARED_TIER_1_DOCUMENTARY_STANDARD_REVISION_ROUND_2_V1.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUMS.sha256",
    "MANIFEST_OF_MANIFESTS.sha256",
    "00_PROGRAM_CONTROL/ROUND_3_INTEGRITY_ROOT.json",
    "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv",
    "04_AUTHORITY_LIFECYCLE_REGISTER/AUTHORITY_LIFECYCLE_STATE_REGISTER.csv",
    "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv",
    "04_AUTHORITY_LIFECYCLE_REGISTER/INVALID_STATE_RULES.csv",
    "05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv",
    "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv",
    "07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv",
    "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv",
    "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv",
    "10_CLOSING_AUDIT_PROTOCOL/TEMPLATE_INDEX.csv",
]

# Columns in Document 03 that must remain unexecuted in a documentary package.
DOC03_NON_EXECUTION_COLUMNS = {
    "result": {"NOT_EXECUTED"},
    "runtime_evidence": {"NOT_OBSERVED"},
    "execution_command": {"", "NOT_EXECUTED", "NOT_EXECUTED_BY_DOCUMENTARY_REVIEW"},
    "execution_environment": {"", "NOT_EXECUTED", "NOT_EXECUTED_BY_DOCUMENTARY_REVIEW"},
    "execution_date": {""},
    "execution_commit": {""},
    "verification_method": {"NOT_PERFORMED"},
    "iso29148_characteristic_check": {"NOT_PERFORMED"},
    "requirement_type": {"SOURCE_TEXT_CANDIDATE_NOT_VALIDATED"},
}

# Rule implementations for 04_AUTHORITY_LIFECYCLE_REGISTER/INVALID_STATE_RULES.csv.
# Each predicate returns True when the row VIOLATES the rule.
RULE_IMPLEMENTATIONS = {
    "T1R2-LIFE-RULE-01": lambda r: r["activation_state"] == "ACTIVE" and r["adoption_state"] != "ADOPTED",
    "T1R2-LIFE-RULE-02": lambda r: r["adoption_state"] == "ADOPTED" and not r["approval_evidence"].strip(),
    "T1R2-LIFE-RULE-03": lambda r: r["accession_state"] == "ACCESSIONED" and not r["accession_evidence"].strip(),
    "T1R2-LIFE-RULE-04": lambda r: r["custody_state"] == "CUSTODY_COMPLETE" and r["accession_state"] != "ACCESSIONED",
    "T1R2-LIFE-RULE-05": lambda r: r["supersession_state"].startswith("SUPERSEDED") and not r["successor_or_basis"].strip(),
    "T1R2-LIFE-RULE-06": lambda r: r["document_lifecycle_state"] == "LOCKED" and not r["lock_evidence"].strip(),
    "T1R2-LIFE-RULE-07": lambda r: r["authority_state"] == "EFFECTIVE" and not r["effective_date"].strip(),
    "T1R2-LIFE-RULE-08": lambda r: r["implementation_authority"] == "AUTHORIZED" and r["authority_state"] != "IMPLEMENTATION_AUTHORIZING",
    "T1R2-LIFE-RULE-09": lambda r: r["production_authority"] == "AUTHORIZED" and r["activation_state"] != "ACTIVE",
    "T1R2-LIFE-RULE-10": lambda r: r["suspension_state"] == "SUSPENDED" and r["activation_state"] == "ACTIVE",
    "T1R2-LIFE-RULE-11": lambda r: r["document_lifecycle_state"] == "HISTORICAL_RETAINED" and r["authority_state"] == "CONTROLLING",
    "T1R2-LIFE-RULE-12": lambda r: r["authority_state"] == "DOCUMENTARY_CANDIDATE_ONLY" and r["adoption_state"] == "ADOPTED",
}

MANIFEST_FILENAMES = {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256"}
MOM = "MANIFEST_OF_MANIFESTS.sha256"
INTEGRITY_ROOT = "00_PROGRAM_CONTROL/ROUND_3_INTEGRITY_ROOT.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def add(results, check, status, detail, failure_capable=True):
    results.append({
        "check": check,
        "status": status,
        "detail": detail,
        "failure_capable": failure_capable,
    })


# ---------------------------------------------------------------------------
# Individual checks. Each returns (status, detail, failure_count).
# Each is a pure function of its inputs so that --self-test can drive it with
# synthetic violating data and prove it is capable of returning FAIL.
# ---------------------------------------------------------------------------

def check_evidence_state_separation(doc03):
    offenders = []
    for row in doc03:
        for column, allowed in DOC03_NON_EXECUTION_COLUMNS.items():
            if column in row and row[column].strip() not in allowed:
                offenders.append((row.get("requirement_id", "?"), column, row[column]))
    if offenders:
        sample = "; ".join(f"{rid}:{col}={val}" for rid, col, val in offenders[:5])
        return "FAIL", f"executed_or_runtime_evidence_claimed={len(offenders)} ({sample})", len(offenders)
    return "PASS", "execution/runtime/production evidence remains separated", 0


def check_lifecycle_rules(life, rule_rows):
    detail = {}
    failures = 0
    for rule in rule_rows:
        rule_id = rule["rule_id"]
        declared = rule.get("implementation_status", "").strip()
        predicate = RULE_IMPLEMENTATIONS.get(rule_id)
        if predicate is None:
            detail[rule_id] = "NOT_IMPLEMENTED"
            if declared == "ENFORCED":
                failures += 1
                detail[rule_id] = "DECLARED_ENFORCED_BUT_NOT_IMPLEMENTED"
            continue
        violations = [r for r in life if predicate(r)]
        if declared != "ENFORCED":
            failures += 1
            detail[rule_id] = f"IMPLEMENTED_BUT_DECLARED_{declared or 'BLANK'}"
            continue
        detail[rule_id] = f"ENFORCED violations={len(violations)}"
        failures += len(violations)
    status = "PASS" if failures == 0 else "FAIL"
    return status, json.dumps(detail, sort_keys=True), failures


def check_source_disposition_rules(sources):
    missing = [r for r in sources if not r["source_disposition"].strip()]
    if missing:
        return "FAIL", f"sources={len(sources)} missing_disposition={len(missing)}", len(missing)
    return "PASS", f"sources={len(sources)} missing_disposition=0", 0


def check_workstream_completeness(prs):
    if not prs:
        return "FAIL", "prs=0 register empty", 1
    missing = [r for r in prs if not r["recommended_disposition"].strip()]
    if missing:
        return "FAIL", f"prs={len(prs)} missing_disposition={len(missing)}", len(missing)
    return "PASS", f"prs={len(prs)} missing_disposition=0", 0


def check_audit_template_distinctness(package, templates):
    """Templates must be genuinely distinct, not one file renamed 19 times."""
    if len(templates) != 19:
        return "FAIL", f"templates={len(templates)} expected=19", 1
    # TEMPLATE_INDEX.csv paths are relative to the Document 10 directory.
    package = package / "10_CLOSING_AUDIT_PROTOCOL"
    digests = {}
    missing = []
    for row in templates:
        rel = row.get("template_path") or row.get("path") or ""
        path = package / rel
        if not path.is_file():
            missing.append(rel)
            continue
        body = [
            line for line in path.read_text(encoding="utf-8").splitlines()
            if not line.startswith("# ") and not line.startswith("Template ID:")
        ]
        digests.setdefault(sha_bytes("\n".join(body).encode("utf-8")), []).append(rel)
    if missing:
        return "FAIL", f"missing_template_files={len(missing)} ({missing[:3]})", len(missing)
    collisions = {d: p for d, p in digests.items() if len(p) > 1}
    if collisions:
        worst = max(collisions.values(), key=len)
        return (
            "FAIL",
            f"distinct_bodies={len(digests)} expected=19 duplicate_groups={len(collisions)} largest_group={len(worst)}",
            sum(len(p) - 1 for p in collisions.values()),
        )
    return "PASS", f"templates=19 distinct_bodies={len(digests)}", 0


def check_manifest_of_manifests(package):
    """The integrity controls must themselves be authenticated (F-05)."""
    mom = package / MOM
    if not mom.is_file():
        return "FAIL", f"{MOM} absent", 1
    declared = {}
    for line in mom.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, _, rel = line.partition("  ")
        declared[rel.strip()] = digest.strip()
    on_disk = sorted(
        str(p.relative_to(package))
        for p in package.rglob("*")
        if p.is_file() and p.name in MANIFEST_FILENAMES
    )
    uncovered = [p for p in on_disk if p not in declared]
    stale = [p for p in declared if p not in on_disk]
    mismatched = [
        rel for rel, digest in declared.items()
        if rel in on_disk and sha(package / rel) != digest
    ]
    # The manifest of manifests cannot authenticate itself; the integrity root does.
    root_path = package / INTEGRITY_ROOT
    root_mismatch = 0
    root_detail = "integrity_root_absent"
    if root_path.is_file():
        root = json.loads(root_path.read_text())
        if root.get("manifest_of_manifests_sha256") == sha(mom):
            root_detail = f"integrity_root_ok external_attestation={root.get('external_attestation_state')}"
        else:
            root_detail = "integrity_root_hash_mismatch"
            root_mismatch = 1
    else:
        root_mismatch = 1
    total = len(uncovered) + len(stale) + len(mismatched) + root_mismatch
    if total:
        return (
            "FAIL",
            f"manifest_files={len(on_disk)} uncovered={len(uncovered)} stale={len(stale)} "
            f"mismatched={len(mismatched)} {root_detail}",
            total,
        )
    return "PASS", f"manifest_files={len(on_disk)} all_authenticated {root_detail}", 0


def check_coverage_universe(package):
    """Every file on disk must be covered by either PACKAGE_MANIFEST.json or MANIFEST_OF_MANIFESTS.sha256."""
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text())
    covered = {f["path"] for f in manifest["files"]}
    mom = package / MOM
    if mom.is_file():
        covered.add(MOM)
        covered.add(INTEGRITY_ROOT)
        for line in mom.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                covered.add(line.partition("  ")[2].strip())
    # Interpreter bytecode caches are a by-product of running the validator, not
    # package content. Manifesting them would make the manifest depend on which
    # interpreter last read the package, which is the opposite of what a manifest
    # is for. They are excluded here and are never shipped.
    on_disk = {
        str(p.relative_to(package))
        for p in package.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    uncovered = sorted(on_disk - covered)
    if uncovered:
        return "FAIL", f"files_on_disk={len(on_disk)} uncovered={len(uncovered)} ({uncovered[:3]})", len(uncovered)
    return "PASS", f"files_on_disk={len(on_disk)} uncovered=0", 0


# ---------------------------------------------------------------------------


def run_self_test():
    """Prove every failure-capable check can actually return FAIL (F-03)."""
    outcomes = []

    status, _, count = check_evidence_state_separation([
        {"requirement_id": "X", "result": "PASSED", "runtime_evidence": "NOT_OBSERVED",
         "execution_command": "", "execution_environment": "", "execution_date": "", "execution_commit": ""}
    ])
    outcomes.append(("evidence_state_separation", status == "FAIL" and count == 1))

    # Three synthetic rows chosen so that between them every one of the twelve
    # rules is triggered at least once. Some rules are mutually exclusive on a
    # single row, so one row cannot cover all twelve.
    base = {
        "document_lifecycle_state": "", "authority_state": "", "adoption_state": "",
        "accession_state": "", "activation_state": "", "implementation_authority": "",
        "production_authority": "", "suspension_state": "", "supersession_state": "",
        "custody_state": "", "effective_date": "", "approval_evidence": "",
        "accession_evidence": "", "lock_evidence": "", "successor_or_basis": "",
    }
    row_a = dict(base, document_lifecycle_state="LOCKED", authority_state="DOCUMENTARY_CANDIDATE_ONLY",
                 adoption_state="ADOPTED", accession_state="ACCESSIONED", activation_state="ACTIVE",
                 implementation_authority="AUTHORIZED", suspension_state="SUSPENDED",
                 supersession_state="SUPERSEDED", custody_state="CUSTODY_COMPLETE")
    row_b = dict(base, authority_state="EFFECTIVE", adoption_state="NOT_ADOPTED",
                 activation_state="ACTIVE", accession_state="NOT_ACCESSIONED",
                 custody_state="CUSTODY_COMPLETE")
    row_c = dict(base, document_lifecycle_state="HISTORICAL_RETAINED", authority_state="CONTROLLING",
                 activation_state="NOT_ACTIVE", production_authority="AUTHORIZED")
    enforced = [{"rule_id": rid, "implementation_status": "ENFORCED"} for rid in RULE_IMPLEMENTATIONS]
    status, detail, count = check_lifecycle_rules([row_a, row_b, row_c], enforced)
    parsed = json.loads(detail)
    uncovered = [rid for rid in RULE_IMPLEMENTATIONS if parsed.get(rid, "").endswith("violations=0")]
    outcomes.append(("lifecycle_invalid_combination_rules", status == "FAIL" and count > 0))
    outcomes.append(("lifecycle_all_twelve_rules_trigger", not uncovered))

    status, _, _ = check_lifecycle_rules([], [{"rule_id": "T1R2-LIFE-RULE-01", "implementation_status": "DOCUMENTED_NOT_ENFORCED"}])
    outcomes.append(("lifecycle_declaration_truthfulness", status == "FAIL"))

    status, _, _ = check_lifecycle_rules([], [{"rule_id": "T1R2-LIFE-RULE-99", "implementation_status": "ENFORCED"}])
    outcomes.append(("lifecycle_phantom_rule_detection", status == "FAIL"))

    status, _, _ = check_source_disposition_rules([{"source_disposition": ""}])
    outcomes.append(("source_disposition_rules", status == "FAIL"))

    status, _, _ = check_workstream_completeness([])
    outcomes.append(("workstream_completeness_empty", status == "FAIL"))
    status, _, _ = check_workstream_completeness([{"recommended_disposition": ""}])
    outcomes.append(("workstream_completeness_blank", status == "FAIL"))

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        outcomes.extend(partb.self_test_cases(lambda: tmp))

    ok = all(passed for _, passed in outcomes)
    report = {
        "self_test": "PASS" if ok else "FAIL",
        "cases": [{"case": name, "failure_capable_confirmed": passed} for name, passed in outcomes],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root")
    parser.add_argument("--package-root")
    parser.add_argument("--mode", choices=["package-only", "repository-aware"], default="package-only")
    parser.add_argument("--expected-head", help="Commit SHA the package is being validated at; recorded and compared.")
    parser.add_argument("--json-output")
    parser.add_argument(
        "--exclude-check", action="append", default=[],
        help=("Skip a named check and record the exclusion in the report. Intended for the "
              "single bootstrap case where a check cannot be satisfied at the moment it is "
              "run: an attestation cannot attest to its own presence in the register it is "
              "about to be written to."))
    parser.add_argument("--self-test", action="store_true", help="Prove each check is capable of failing, then exit.")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()
    package = Path(args.package_root) if args.package_root else Path.cwd()
    if package.name != PACKAGE_NAME and (package / PACKAGE_NAME).exists():
        package = package / PACKAGE_NAME
    results = []
    failures = 0
    for rel in REQUIRED_FILES:
        exists = (package / rel).is_file()
        add(results, f"required_file:{rel}", "PASS" if exists else "FAIL", "present" if exists else "missing")
        failures += 0 if exists else 1
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text())
    manifest_paths = {f["path"]: f for f in manifest["files"]}
    manifest_failures = 0
    for rel, item in manifest_paths.items():
        path = package / rel
        if not path.is_file():
            add(results, f"manifest_file:{rel}", "FAIL", "missing")
            manifest_failures += 1
            continue
        if sha(path) != item["sha256"] or path.stat().st_size != item["byte_length"]:
            add(results, f"manifest_integrity:{rel}", "FAIL", "hash or byte length mismatch")
            manifest_failures += 1
    add(results, "manifest_accuracy", "PASS" if manifest_failures == 0 else "FAIL",
        f"files={len(manifest_paths)} integrity_failures={manifest_failures}")
    failures += manifest_failures

    status, detail, count = check_manifest_of_manifests(package)
    add(results, "manifest_self_authentication", status, detail)
    failures += count

    status, detail, count = check_coverage_universe(package)
    add(results, "manifest_coverage_universe", status, detail)
    failures += count

    doc03 = rows(package / "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv")
    status, detail, count = check_evidence_state_separation(doc03)
    add(results, "evidence_state_separation", status, detail)
    failures += count

    life = rows(package / "04_AUTHORITY_LIFECYCLE_REGISTER/AUTHORITY_LIFECYCLE_STATE_REGISTER.csv")
    rule_rows = rows(package / "04_AUTHORITY_LIFECYCLE_REGISTER/INVALID_STATE_RULES.csv")
    status, detail, count = check_lifecycle_rules(life, rule_rows)
    add(results, "lifecycle_invalid_combination_rules", status, detail)
    failures += count

    decisions = rows(package / "05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv")
    bad_decisions = [r for r in decisions if r["authority_granted"] != "NONE_BY_THIS_PACKAGE"]
    add(results, "decision_authority_boundary", "PASS" if not bad_decisions else "FAIL", f"bad_decisions={len(bad_decisions)}")
    failures += len(bad_decisions)

    frwe = rows(package / "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv")
    bad_waivers = [r for r in frwe if r["record_classification"] in {"waiver", "exception", "temporary deviation"} and (not r["expiration_date"] or r["silent_permanent_continuation_prohibited"] != "YES")]
    add(results, "waiver_expiration_controls", "PASS" if not bad_waivers else "FAIL", f"bad_waivers={len(bad_waivers)}")
    failures += len(bad_waivers)

    owners = rows(package / "07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv")
    invented = [r for r in owners if r["appointment_evidence"] != "NOT_RECORDED" and not r["effective_date"]]
    add(results, "ownership_vacancy_handling", "PASS" if not invented else "FAIL", f"invented_assignments={len(invented)}")
    failures += len(invented)

    sources = rows(package / "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv")
    status, detail, count = check_source_disposition_rules(sources)
    add(results, "source_disposition_rules", status, detail)
    failures += count

    prs = rows(package / "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv")
    status, detail, count = check_workstream_completeness(prs)
    add(results, "workstream_completeness", status, detail)
    failures += count

    templates = rows(package / "10_CLOSING_AUDIT_PROTOCOL/TEMPLATE_INDEX.csv")
    add(results, "audit_template_completeness", "PASS" if len(templates) == 19 else "FAIL", f"templates={len(templates)}")
    failures += 0 if len(templates) == 19 else 1
    status, detail, count = check_audit_template_distinctness(package, templates)
    add(results, "audit_template_distinctness", status, detail)
    failures += count

    # ---------------------------------------------------------------------
    # Round 3 Part B checks. Each is defined in validator_partb_checks.py and
    # is driven with violating data by --self-test, so none of them is a
    # decorative assertion.
    # ---------------------------------------------------------------------
    loaded = {}
    for rel in PARTB_REGISTERS:
        path = package / rel
        loaded[rel] = rows(path) if path.is_file() else []

    narratives = {}
    for directory in sorted(PER_DOCUMENT_REQUIRED_FILES):
        for path in sorted((package / directory).glob(NARRATIVE_GLOB)):
            if "CRITICAL_REVIEW_REPORT" in path.name:
                continue
            narratives[f"{directory}/{path.name}"] = path.read_text(encoding="utf-8")

    attestations_path = package / "VALIDATION/INDEPENDENT_REPRODUCTION_ATTESTATIONS.csv"
    attestations = rows(attestations_path) if attestations_path.is_file() else []
    delta_path = package / "VALIDATION/SCOPE_DELTA_FROM_V1.md"
    delta_text = delta_path.read_text(encoding="utf-8") if delta_path.is_file() else ""
    removed_path = package / "VALIDATION/V1_REMOVED_FILE_DIGESTS.json"
    removed_expected = json.loads(removed_path.read_text()) if removed_path.is_file() else {}

    partb_checks = [
        ("per_document_required_files",
         partb.check_per_document_required_files(package, PER_DOCUMENT_REQUIRED_FILES)),
        ("parse_integrity", partb.check_parse_integrity(package)),
        ("placeholder_marker_scan", partb.check_placeholder_markers(package)),
        ("enum_conformance", partb.check_enum_conformance(loaded)),
        ("referential_integrity", partb.check_referential_integrity(loaded)),
        ("cross_register_arithmetic", partb.check_cross_register_arithmetic(loaded)),
        ("decision_disposition_null_literal",
         partb.check_decision_disposition_null_literal(
             loaded["05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv"])),
        ("question_wording_identity",
         partb.check_question_wording_identity(
             loaded["05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv"],
             loaded["FOUNDER_DECISION_PACKET.csv"])),
        ("packet_recommendation_neutrality",
         partb.check_packet_recommendation_neutrality(loaded["FOUNDER_DECISION_PACKET.csv"])),
        ("packet_citation_counts",
         partb.check_packet_citation_counts(
             loaded["FOUNDER_DECISION_PACKET.csv"], loaded["UNRESOLVED_ISSUE_REGISTER.csv"])),
        ("lifecycle_matrix_completeness",
         partb.check_lifecycle_matrix_completeness(
             loaded["04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv"])),
        ("findings_exemplar_separation",
         partb.check_findings_exemplar_separation(
             loaded["06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv"],
             loaded["06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_SCHEMA_EXEMPLAR.csv"],
             loaded["UNRESOLVED_ISSUE_REGISTER.csv"])),
        ("review_calendar_operability",
         partb.check_review_calendar_operability(
             loaded["07_OWNERSHIP_STEWARDSHIP_REVIEW/REVIEW_CALENDAR.csv"],
             loaded["07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv"])),
        ("authority_state_tense",
         partb.check_authority_state_tense(
             loaded["08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv"])),
        ("workstream_external_observation",
         partb.check_workstream_external_observation(
             loaded["09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv"])),
        ("audit_evidence_distinctness",
         partb.check_audit_evidence_distinctness(
             loaded["10_CLOSING_AUDIT_PROTOCOL/AUDIT_REQUIREMENTS_MATRIX.csv"])),
        ("narrative_completeness", partb.check_narrative_completeness(narratives)),
        ("reproduction_attestations", partb.check_reproduction_attestations(attestations)),
        ("scope_delta_disclosure",
         partb.check_scope_delta_disclosure(delta_text, removed_expected)),
    ]
    for name, (status, detail, count) in partb_checks:
        if name in args.exclude_check:
            add(results, name, "EXCLUDED_BY_REQUEST", detail, failure_capable=False)
            continue
        add(results, name, status, detail)
        failures += count

    head = None
    if args.mode == "repository-aware":
        if not args.repo_root or not (Path(args.repo_root) / ".git").exists():
            add(results, "git_metadata", "NOT_APPLICABLE_OUTSIDE_GIT", "repository root unavailable", failure_capable=False)
        else:
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=args.repo_root, text=True).strip()
            if args.expected_head and head != args.expected_head:
                add(results, "git_metadata", "FAIL", f"head={head} expected={args.expected_head}")
                failures += 1
            else:
                add(results, "git_metadata", "PASS", head)
    else:
        add(results, "git_metadata", "NOT_APPLICABLE_OUTSIDE_GIT", "package-only validation", failure_capable=False)

    report = {
        "status": "PASS" if failures == 0 else "FAIL",
        "failures": failures,
        "python_version": sys.version,
        "platform": platform.platform(),
        "dependency_versions": {"stdlib_only": True},
        "package_root": str(package),
        "mode": args.mode,
        "excluded_checks": sorted(args.exclude_check),
        "validated_at_commit": head or args.expected_head or "NOT_RECORDED",
        "expected_head": args.expected_head or "NOT_SUPPLIED",
        "failure_capable_checks": sum(1 for r in results if r["failure_capable"]),
        "non_failure_capable_checks": sum(1 for r in results if not r["failure_capable"]),
        "results": results,
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.json_output:
        output_path = Path(args.json_output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
