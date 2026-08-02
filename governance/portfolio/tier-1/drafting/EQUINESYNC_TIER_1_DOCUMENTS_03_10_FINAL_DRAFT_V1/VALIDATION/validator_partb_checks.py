#!/usr/bin/env python3
"""Round 3 Part B validator checks.

Every function in this module is a pure function of its arguments and returns
``(status, detail, failure_count)`` in the same shape as the checks already in
``validate_tier1_documents_03_10_rr2.py``. Purity is deliberate: it is what lets
``--self-test`` drive each check with synthetic violating data and prove the
check is capable of returning FAIL. A check that cannot fail is not a control.

These checks exist because Revision Round 2 asserted properties that nothing
verified. Each one below is tied to the finding that showed the assertion was
unguarded. They test the package as it stands; they do not certify it, and none
of them makes any statement about adoption, activation, implementation
authority, production authority, merge authority, certification, or legal
compliance.
"""

import csv
import hashlib
import json
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Enumerated domains. A value outside its domain is a failure, not a warning:
# an unrecognised state is exactly the condition under which a downstream reader
# would substitute their own meaning.
# ---------------------------------------------------------------------------

ENUM_DOMAINS = {
    ("05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv",
     "selected_disposition"): {"NO_DISPOSITION_SELECTED"},
    ("05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv",
     "selected_disposition_enum_domain"): {
        'approve; approve with modification; defer; reject; require remediation; NO_DISPOSITION_SELECTED (null literal, no decision recorded)'},
    ("08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv",
     "authority_state"): {
        "HISTORICAL_ADOPTION_EVIDENCE_OBSERVED",
        "HISTORICAL_FOUNDER_APPROVAL_EVIDENCE_OBSERVED",
        "HISTORICAL_CONTEXT_ONLY",
        "DOCUMENTARY_CONTEXT_ONLY",
        "PROTECTED_REPOSITORY_BYTES_PRESENT",
        "EXACT_BYTES_RECORDED_ONLY",
    },
    ("08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv",
     "present_adoption_state"): {"NOT_ADOPTED_BY_THIS_PACKAGE"},
    ("08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv",
     "canonical_representation"): {
        "CANONICAL_NOT_DETERMINED", "SOLE_KNOWN_REPRESENTATION"},
    ("09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv",
     "review_thread_state"): {
        "NO_REVIEW_REQUESTED_NO_REVIEW_SUBMITTED_ZERO_REVIEW_THREADS"},
    ("09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv",
     "review_decision_state"): {"NO_REVIEW_DECISION_RECORDED"},
    ("09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv",
     "base_drift"): {"YES", "NO"},
    ("03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv",
     "test_case_identified"): {
        "NO_FILE_LEVEL_CANDIDATE_ONLY", "NO_NO_TEST_FILE_CANDIDATE"},
    ("03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv",
     "requirement_type"): {"SOURCE_TEXT_CANDIDATE_NOT_VALIDATED"},
    ("03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv",
     "original_requirement_type_claim"): {
        "NORMATIVE_REQUIREMENT", "EVIDENCE_REQUIREMENT", "PROHIBITION",
        "VALIDATION_REQUIREMENT"},
    ("07_OWNERSHIP_STEWARDSHIP_REVIEW/REVIEW_CALENDAR.csv",
     "operative_state"): {"NOT_OPERATIVE_PENDING_FOUNDER_APPOINTMENT"},
    ("07_OWNERSHIP_STEWARDSHIP_REVIEW/REVIEW_CALENDAR.csv",
     "date_binding_state"): {"PROPOSED_NOT_BINDING_NO_APPOINTED_OWNER_EXISTS"},
    ("04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv",
     "permitted"): {"YES", "NO"},
}

# Reserved literals meaning "this key deliberately points at nothing". They are
# not dangling references and must not be reported as such.
NULL_REFERENCE_LITERALS = {
    "", "NONE", "NOT_APPLICABLE", "NOT_IN_DUPLICATE_CLUSTER",
    "NOT_IDENTIFIED", "NOT_DETERMINED",
}

PLACEHOLDER_MARKERS = ("TODO", "TBD", "FIXME", "XXX", "LOREM IPSUM", "<PLACEHOLDER>")

# Words that assert a present, live authority. Document 08 records historical
# observation only, so these must not appear in its authority_state column.
PRESENT_TENSE_AUTHORITY_TOKENS = ("IS_ADOPTED", "ADOPTED_BY", "CURRENTLY_", "_ACTIVE")


def _fail(count, detail):
    return ("FAIL" if count else "PASS", detail, count)


def _rows(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


# ---------------------------------------------------------------------------
# F-16. Restore the per-document coverage that V1 had and Round 2 dropped.
# ---------------------------------------------------------------------------

def check_per_document_required_files(package_root, expected):
    """V1 shipped a per-document validator that listed each document's required
    files. Round 2 removed those sixteen files and replaced them with one
    package-level validator that does not carry the per-document list, so a
    document could lose a register and nothing would notice. This restores the
    list. ``expected`` maps a document directory to its required file names.
    """
    missing = []
    for directory, names in sorted(expected.items()):
        for name in names:
            if not (Path(package_root) / directory / name).is_file():
                missing.append(f"{directory}/{name}")
    return _fail(len(missing), json.dumps({"missing": missing}, sort_keys=True))


def check_parse_integrity(package_root):
    """Every CSV parses as CSV with a stable column count, and every JSON parses
    as JSON. V1 checked this per document. A register that has become ragged is
    a register whose downstream counts are meaningless.
    """
    problems = []
    root = Path(package_root)
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix == ".csv":
            try:
                with path.open(encoding="utf-8", newline="") as handle:
                    reader = csv.reader(handle)
                    header = next(reader, None)
                    if not header:
                        problems.append(f"{rel}: empty")
                        continue
                    for number, row in enumerate(reader, start=2):
                        if len(row) != len(header):
                            problems.append(
                                f"{rel}: line {number} has {len(row)} fields, header has {len(header)}")
                            break
            except Exception as exc:                       # pragma: no cover
                problems.append(f"{rel}: {type(exc).__name__}")
        elif path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                problems.append(f"{rel}: {type(exc).__name__}")
    return _fail(len(problems), json.dumps({"parse_problems": problems}, sort_keys=True))


def check_placeholder_markers(package_root):
    """V1 rejected any document containing TODO or TBD. Restored, widened, and
    scoped to exclude this module, which necessarily names the markers it looks
    for.
    """
    hits = []
    root = Path(package_root)
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.name in {"validator_partb_checks.py", "SCOPE_DELTA_FROM_V1.md"}:
            continue
        if path.suffix not in {".md", ".csv", ".json", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:                          # pragma: no cover
            continue
        upper = text.upper()
        for marker in PLACEHOLDER_MARKERS:
            if marker in upper:
                hits.append(f"{path.relative_to(root).as_posix()}:{marker}")
    return _fail(len(hits), json.dumps({"placeholder_hits": hits}, sort_keys=True))


# ---------------------------------------------------------------------------
# Enumerations and referential integrity.
# ---------------------------------------------------------------------------

def check_enum_conformance(loaded):
    """``loaded`` maps a relative path to its parsed rows. Any value outside its
    declared domain fails. Round 2 declared states in prose and enforced none of
    them.
    """
    violations = []
    for (rel, column), domain in sorted(ENUM_DOMAINS.items()):
        if rel not in loaded:
            violations.append(f"{rel}: not loaded")
            continue
        for index, row in enumerate(loaded[rel], start=2):
            if column not in row:
                violations.append(f"{rel}:{column}: column absent")
                break
            value = (row[column] or "").strip()
            if value not in domain:
                violations.append(f"{rel}:{column}: line {index} value {value!r}")
    return _fail(len(violations), json.dumps({"enum_violations": violations[:40],
                                              "total": len(violations)}, sort_keys=True))


def check_referential_integrity(loaded):
    """Cross-register joins must actually join. Round 2 asserted a duplicate
    cluster count, a domain coverage table, a review calendar and a decision
    packet that each referenced another register, and nothing checked that the
    referenced keys existed.
    """
    broken = []

    sources = loaded.get(
        "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv", [])
    clusters = loaded.get(
        "08_SOURCE_RECONCILIATION/DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv", [])
    cluster_ids = {(r.get("cluster_id") or "").strip() for r in clusters} - {""}
    for r in sources:
        cid = (r.get("duplicate_cluster_id") or "").strip()
        if cid in NULL_REFERENCE_LITERALS:
            continue
        if cid not in cluster_ids:
            broken.append(f"doc08 source {r.get('source_id')} -> unknown cluster {cid}")
    # And the join must hold in the other direction: a cluster with no members
    # in the source register is a cluster that describes nothing.
    member_ids = {(r.get("duplicate_cluster_id") or "").strip() for r in sources}
    member_ids -= NULL_REFERENCE_LITERALS
    for cid in sorted(cluster_ids - member_ids):
        broken.append(f"doc08 cluster {cid} has no member rows in the source register")

    reqs = loaded.get(
        "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv", [])
    coverage = loaded.get("03_IMPLEMENTATION_TRACEABILITY/COVERAGE_METRICS_BY_DOMAIN.csv", [])
    req_domains = {(r.get("product_domain") or "").strip() for r in reqs} - {""}
    cov_domains = {(r.get("domain") or "").strip() for r in coverage} - {"", "OVERALL"}
    for d in sorted(req_domains - cov_domains):
        broken.append(f"doc03 domain {d!r} present in register, absent from coverage table")
    for d in sorted(cov_domains - req_domains):
        broken.append(f"doc03 domain {d!r} present in coverage table, absent from register")

    matrix = loaded.get("07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv", [])
    calendar = loaded.get("07_OWNERSHIP_STEWARDSHIP_REVIEW/REVIEW_CALENDAR.csv", [])
    roles = {(r.get("role") or "").strip() for r in matrix} - {""}
    for r in calendar:
        owner = (r.get("responsible_owner") or "").strip()
        if owner and owner not in roles:
            broken.append(f"doc07 review {r.get('review_id')} owner {owner!r} is not a declared role")

    decisions = loaded.get(
        "05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv", [])
    packet = loaded.get("FOUNDER_DECISION_PACKET.csv", [])
    dec_ids = [(r.get("decision_id") or "").strip() for r in decisions]
    pkt_ids = [(r.get("decision_id") or "").strip() for r in packet]
    if sorted(dec_ids) != sorted(pkt_ids):
        broken.append(f"doc05 register ids {sorted(dec_ids)} != packet ids {sorted(pkt_ids)}")

    return _fail(len(broken), json.dumps({"broken_references": broken[:40],
                                          "total": len(broken)}, sort_keys=True))


# ---------------------------------------------------------------------------
# Arithmetic. Round 2 published totals that no one recomputed.
# ---------------------------------------------------------------------------

def check_cross_register_arithmetic(loaded):
    """Recompute the published Document 03 coverage row and the Document 08
    dashboard from the underlying registers. Any published figure that does not
    reproduce fails. This is the check that would have caught the Round 2
    duplicate-cluster and coverage numbers.
    """
    mismatches = []

    reqs = loaded.get(
        "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv", [])
    coverage = loaded.get("03_IMPLEMENTATION_TRACEABILITY/COVERAGE_METRICS_BY_DOMAIN.csv", [])
    overall = next((r for r in coverage if (r.get("domain") or "").strip() == "OVERALL"), None)
    if reqs and overall:
        computed = {
            "total_canonical_requirements": len(reqs),
            "candidate_test_files_identified": sum(
                1 for r in reqs if (r.get("candidate_test_file_id") or "").strip()
                not in {"", "NONE", "NOT_IDENTIFIED"}),
            "test_cases_specified": sum(
                1 for r in reqs if (r.get("test_case_identified") or "").strip() == "YES"),
            "tests_executed": sum(
                1 for r in reqs if (r.get("result") or "").strip() != "NOT_EXECUTED"),
            "runtime_evidence_present": sum(
                1 for r in reqs if (r.get("runtime_evidence") or "").strip() != "NOT_OBSERVED"),
        }
        for key, value in sorted(computed.items()):
            published = (overall.get(key) or "").strip()
            if published != str(value):
                mismatches.append(f"doc03 OVERALL.{key}: published {published!r}, recomputed {value}")

    sources = loaded.get(
        "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv", [])
    dashboard = loaded.get("08_SOURCE_RECONCILIATION/SOURCE_DISPOSITION_DASHBOARD.csv", [])
    if sources and dashboard:
        d = dashboard[0]
        by_cluster = {}
        for r in sources:
            cid = (r.get("duplicate_cluster_id") or "").strip()
            if cid not in NULL_REFERENCE_LITERALS:
                by_cluster.setdefault(cid, []).append(r)
        in_clusters = sum(len(v) for v in by_cluster.values())
        computed = {
            "total_source_rows": len(sources),
            "unique_source_identities": len({(r.get("sha256") or "").strip() for r in sources}),
            "duplicate_clusters": len(by_cluster),
            "rows_in_duplicate_clusters": in_clusters,
            "redundant_copies": in_clusters - len(by_cluster),
            "duplicate_cluster_id_populated_rows": in_clusters,
            "canonical_representation_undetermined_rows": sum(
                1 for r in sources
                if (r.get("canonical_representation") or "").strip() == "CANONICAL_NOT_DETERMINED"),
            "controlling_version_not_declared_rows": sum(
                1 for r in sources
                if (r.get("controlling_version_declaration_state") or "").strip()
                == "NO_VERSION_STRING_PRESENT_IN_SOURCE"),
            "controlling_version_conflict_rows": sum(
                1 for r in sources
                if (r.get("controlling_version_declaration_state") or "").strip()
                == "CONFLICTING_DECLARATIONS"),
            "founder_decisions_required": sum(
                1 for r in sources
                if (r.get("founder_disposition_required") or "").strip() == "YES"),
        }
        for key, value in sorted(computed.items()):
            published = (d.get(key) or "").strip()
            if published != str(value):
                mismatches.append(f"doc08 dashboard.{key}: published {published!r}, recomputed {value}")

    return _fail(len(mismatches), json.dumps({"arithmetic_mismatches": mismatches[:40],
                                              "total": len(mismatches)}, sort_keys=True))


# ---------------------------------------------------------------------------
# F-07, F-09, F-24. Decision register and packet.
# ---------------------------------------------------------------------------

def check_decision_disposition_null_literal(decisions):
    """F-07. Round 2 left ``selected_disposition`` holding prose that read as an
    outcome. A decision that has not been made must say so in one reserved
    literal, and must not also carry a recommendation.
    """
    bad = []
    for r in decisions:
        did = r.get("decision_id")
        if (r.get("selected_disposition") or "").strip() != "NO_DISPOSITION_SELECTED":
            bad.append(f"{did}: selected_disposition is not the reserved null literal")
        if not (r.get("round_2_selected_disposition_text_retained") or "").strip():
            bad.append(f"{did}: superseded Round 2 text was discarded rather than retained")
        if (r.get("authority_granted") or "").strip() not in {
                "", "NONE", "NONE_BY_THIS_PACKAGE",
                "NO_AUTHORITY_GRANTED_BY_THIS_PACKAGE"}:
            bad.append(f"{did}: authority_granted asserts a grant")
    return _fail(len(bad), json.dumps({"decision_defects": bad}, sort_keys=True))


def check_question_wording_identity(decisions, packet):
    """F-09. The register and the packet stated the same question in different
    words, so a founder signing the packet would not be signing the register's
    question. The two must be byte-identical.
    """
    reg = {(r.get("decision_id") or "").strip(): (r.get("question_presented") or "")
           for r in decisions}
    pkt = {(r.get("decision_id") or "").strip(): (r.get("issue") or "") for r in packet}
    divergent = [k for k in sorted(set(reg) | set(pkt)) if reg.get(k) != pkt.get(k)]
    return _fail(len(divergent), json.dumps({"divergent_question_wording": divergent},
                                            sort_keys=True))


def check_packet_recommendation_neutrality(packet):
    """F-24. The packet must not recommend. A packet that recommends is a packet
    that has pre-decided the question it presents.
    """
    bad = []
    for r in packet:
        did = r.get("decision_id")
        if (r.get("recommended_option") or "").strip() \
                != "NO_RECOMMENDATION_MADE_BY_THIS_PACKAGE":
            bad.append(f"{did}: recommended_option is not the reserved neutral literal")
        if not (r.get("consequences_of_each_option") or "").strip():
            bad.append(f"{did}: consequences_of_each_option is empty")
        if not (r.get("relevant_evidence") or "").strip():
            bad.append(f"{did}: relevant_evidence is empty")
    return _fail(len(bad), json.dumps({"packet_defects": bad}, sort_keys=True))


# ---------------------------------------------------------------------------
# F-15. Lifecycle matrix.
# ---------------------------------------------------------------------------

def check_lifecycle_matrix_completeness(matrix, state_count=14):
    """F-15. Round 2 published a partial matrix, so a transition that was simply
    absent was indistinguishable from one that was prohibited. The matrix must
    be total: every ordered pair of states present, every prohibited pair
    carrying a reason, every permitted pair carrying evidence that is not shared
    with another row.
    """
    problems = []
    expected = state_count * state_count
    if len(matrix) != expected:
        problems.append(f"row count {len(matrix)}, expected {expected} for {state_count} states")

    starts = {(r.get("permitted_starting_state") or "").strip() for r in matrix}
    nexts = {(r.get("permitted_next_state") or "").strip() for r in matrix}
    if starts != nexts:
        problems.append(f"starting states and next states differ: {sorted(starts ^ nexts)}")
    if len(starts) != state_count:
        problems.append(f"distinct states {len(starts)}, expected {state_count}")

    pairs = [((r.get("permitted_starting_state") or "").strip(),
              (r.get("permitted_next_state") or "").strip()) for r in matrix]
    if len(set(pairs)) != len(pairs):
        problems.append("duplicate state pairs present")
    for s in sorted(starts):
        for n in sorted(nexts):
            if (s, n) not in set(pairs):
                problems.append(f"missing pair {s} -> {n}")

    evidence = []
    for r in matrix:
        pair = f"{r.get('permitted_starting_state')} -> {r.get('permitted_next_state')}"
        permitted = (r.get("permitted") or "").strip()
        if permitted == "YES":
            text = (r.get("required_evidence") or "").strip()
            if not text:
                problems.append(f"{pair}: permitted with no required_evidence")
            else:
                evidence.append(text)
            reason = (r.get("prohibition_reason") or "").strip()
            if reason != "NOT_APPLICABLE_TRANSITION_IS_PERMITTED":
                problems.append(
                    f"{pair}: permitted, so prohibition_reason must be the reserved "
                    f"not-applicable literal, found {reason!r}")
        elif permitted == "NO":
            reason = (r.get("prohibition_reason") or "").strip()
            if not reason or reason == "NOT_APPLICABLE_TRANSITION_IS_PERMITTED":
                problems.append(f"{pair}: prohibited with no stated prohibition_reason")
        for column in ("starting_state_declaration_source", "next_state_declaration_source"):
            if not (r.get(column) or "").strip():
                problems.append(f"{pair}: {column} is empty")
    if len(set(evidence)) != len(evidence):
        problems.append(f"required_evidence not distinct across permitted rows: "
                        f"{len(evidence)} rows, {len(set(evidence))} distinct")

    return _fail(len(problems), json.dumps({"lifecycle_matrix_problems": problems[:40],
                                            "total": len(problems)}, sort_keys=True))


# ---------------------------------------------------------------------------
# F-12, F-22. Findings register.
# ---------------------------------------------------------------------------

def check_findings_exemplar_separation(register, exemplar, unresolved):
    """F-12. Round 2 put eight illustrative rows in the live findings register,
    where they read as real findings. Illustrations belong in an exemplar file.
    The live register's population is zero, and every row anywhere must declare
    its provenance and its operative effect.
    """
    problems = []
    if register:
        problems.append(f"live findings register is not empty: {len(register)} rows")
    if not exemplar:
        problems.append("exemplar file has no rows, so the illustrations were lost, not moved")
    for r in exemplar:
        rid = r.get("record_id")
        if (r.get("record_provenance") or "").strip() != "SCHEMA_EXEMPLAR_NOT_AN_OBSERVED_FINDING":
            problems.append(f"exemplar {rid}: provenance does not disclaim finding status")
        for column in ("classification_operative_effect", "root_cause", "root_cause_method"):
            if not (r.get(column) or "").strip():
                problems.append(f"exemplar {rid}: {column} is empty")
    if register and exemplar:
        if set(register[0].keys()) != set(exemplar[0].keys()):
            problems.append("register and exemplar schemas diverge")

    # F-22: an unresolved issue that quantifies a population must locate it.
    for r in unresolved:
        iid = r.get("issue_id") or r.get("unresolved_issue_id")
        count = (r.get("underlying_item_count") or "").strip()
        locator = (r.get("underlying_population_locator") or "").strip()
        if not count:
            problems.append(f"unresolved {iid}: underlying_item_count is empty")
        if not locator:
            problems.append(f"unresolved {iid}: underlying_population_locator is empty")
    return _fail(len(problems), json.dumps({"findings_problems": problems[:40],
                                            "total": len(problems)}, sort_keys=True))


# ---------------------------------------------------------------------------
# F-21. Review calendar.
# ---------------------------------------------------------------------------

def check_review_calendar_operability(calendar, matrix):
    """F-21. Round 2 published review dates and escalation deadlines against
    roles that have no appointed holder. A deadline no one holds is not a
    control. Dates must be labelled proposed, the calendar must be labelled not
    operative, and each row must name who an escalation would go to.
    """
    problems = []
    appointed = {
        (r.get("role") or "").strip()
        for r in matrix
        if (r.get("appointment_evidence") or "").strip()
        not in {"", "NONE", "NOT_RECORDED", "NOT_APPOINTED", "NO_APPOINTMENT_EVIDENCE"}
    }
    for r in calendar:
        rid = r.get("review_id")
        if "proposed_next_review_date" not in r:
            problems.append(f"{rid}: date column is not labelled proposed")
        if (r.get("operative_state") or "").strip() \
                != "NOT_OPERATIVE_PENDING_FOUNDER_APPOINTMENT":
            problems.append(f"{rid}: operative_state asserts an operative calendar")
        if not (r.get("escalation_addressee") or "").strip():
            problems.append(f"{rid}: escalation_addressee is empty")
        owner = (r.get("responsible_owner") or "").strip()
        if owner in appointed and (r.get("date_binding_state") or "").strip().startswith("PROPOSED"):
            problems.append(f"{rid}: owner {owner} is appointed but the date is still non-binding")
    return _fail(len(problems), json.dumps({"calendar_problems": problems[:40],
                                            "total": len(problems)}, sort_keys=True))


# ---------------------------------------------------------------------------
# F-20. Source authority tense.
# ---------------------------------------------------------------------------

def check_authority_state_tense(sources):
    """F-20. Round 2 labelled historical evidence with present-tense state names
    such as ADOPTION_OR_LOCK_EVIDENCE_PRESENT, which reads as a live adoption.
    Document 08 observes history; it does not adopt. Every row must also carry
    the retained Round 2 label so the relabelling is auditable rather than
    silent.
    """
    bad = []
    for r in sources:
        sid = r.get("source_id")
        state = (r.get("authority_state") or "").strip()
        for token in PRESENT_TENSE_AUTHORITY_TOKENS:
            if token in state:
                bad.append(f"{sid}: authority_state {state!r} asserts present tense")
                break
        if (r.get("present_adoption_state") or "").strip() != "NOT_ADOPTED_BY_THIS_PACKAGE":
            bad.append(f"{sid}: present_adoption_state does not disclaim adoption")
        if not (r.get("authority_state_round_2_label_retained") or "").strip():
            bad.append(f"{sid}: the superseded Round 2 label was discarded, not retained")
    return _fail(len(bad), json.dumps({"tense_defects": bad[:40], "total": len(bad)},
                                      sort_keys=True))


# ---------------------------------------------------------------------------
# F-25. Workstream register against external observation.
# ---------------------------------------------------------------------------

def check_workstream_external_observation(prs):
    """F-25. Round 2 recorded review and drift states that had not been observed
    against the forge. Each row must name the method and time of the external
    observation, cite the commit the CI result was read at, and state drift as a
    pair of integers with a stated definition rather than as a bare flag.
    """
    problems = []
    for r in prs:
        pr = r.get("pr_number")
        for column in ("external_observation_method", "external_observed_at_utc",
                       "ci_observation_commit", "base_drift_definition",
                       "review_participation_evidence"):
            if not (r.get(column) or "").strip():
                problems.append(f"PR {pr}: {column} is empty")
        behind = (r.get("commits_behind_base_branch_head") or "").strip()
        ahead = (r.get("commits_ahead_of_base_branch_head") or "").strip()
        if not behind.isdigit() or not ahead.isdigit():
            problems.append(f"PR {pr}: drift counts are not integers ({behind!r}, {ahead!r})")
            continue
        drift = (r.get("base_drift") or "").strip()
        expected = "YES" if int(behind) > 0 else "NO"
        if drift != expected:
            problems.append(
                f"PR {pr}: base_drift {drift!r} contradicts commits_behind={behind}")
        head = (r.get("head_sha") or "").strip()
        commit = (r.get("ci_observation_commit") or "").strip()
        if head and commit and not commit.startswith(head[:7]) and not head.startswith(commit[:7]):
            problems.append(f"PR {pr}: CI was read at {commit} but head is {head}")
    return _fail(len(problems), json.dumps({"workstream_problems": problems[:40],
                                            "total": len(problems)}, sort_keys=True))


# ---------------------------------------------------------------------------
# F-23. Audit evidence.
# ---------------------------------------------------------------------------

def check_audit_evidence_distinctness(templates):
    """F-23. Round 2 gave all nineteen audit templates the same required-evidence
    string, which means the column carried no information. Each template must
    state what evidence that template specifically requires, and the superseded
    shared string must be retained rather than deleted.
    """
    problems = []
    seen = {}
    for r in templates:
        rid = (r.get("requirement_id") or "").strip()
        name = (r.get("template_name") or "").strip()
        text = (r.get("required_evidence") or "").strip()
        if not text:
            problems.append(f"{rid}: required_evidence is empty")
        elif text in seen:
            problems.append(f"{rid} ({name}) shares required_evidence with {seen[text]}")
        else:
            seen[text] = f"{rid} ({name})"
        if not (r.get("required_evidence_round_2_shared_text") or "").strip():
            problems.append(f"{rid}: the superseded shared string was discarded, not retained")
    return _fail(len(problems), json.dumps({"audit_evidence_problems": problems,
                                            "distinct_strings": len(seen)}, sort_keys=True))


# ---------------------------------------------------------------------------
# F-27, F-28. Narratives and reproducibility.
# ---------------------------------------------------------------------------

NARRATIVE_REQUIRED_HEADINGS = (
    "## Identification",
    "## Purpose",
    "## Scope",
    "## Exclusions",
    "## Method",
    "## Contents Inventory",
    "## Known Limitations",
    "## Status",
)


def check_packet_citation_counts(packet, unresolved):
    """A packet that cites the size of another register must cite it correctly.
    Part B initially shipped a packet citing five unresolved issues against a
    register holding six, because the citation was typed by hand at a point in
    the run before the register had finished growing. Nothing caught it; this
    does.
    """
    import re as _re
    expected = len(unresolved)
    bad = []
    for r in packet:
        for value in r.values():
            for cited in _re.findall(
                    r"UNRESOLVED_ISSUE_REGISTER\.csv \((\d+) issues\)", value or ""):
                if int(cited) != expected:
                    bad.append(f"{r.get('decision_id')}: cites {cited} unresolved issues, "
                               f"register holds {expected}")
    return _fail(len(bad), json.dumps({"citation_mismatches": bad}, sort_keys=True))


def check_narrative_completeness(narratives):
    """F-27. Round 2's per-document narratives were short cover notes that did
    not say how their figures were derived or what the document does not
    establish, so a reader could not tell an observation from an assertion. Each
    narrative must carry the five required sections and end with the verbatim
    status line.
    """
    problems = []
    for rel, text in sorted(narratives.items()):
        for heading in NARRATIVE_REQUIRED_HEADINGS:
            if heading not in text:
                problems.append(f"{rel}: missing section {heading!r}")
        if "NOT_ADOPTED" not in text or "FOUNDER_REVIEW_REQUIRED" not in text:
            problems.append(f"{rel}: status line absent or incomplete")
        if len(text.splitlines()) < 40:
            problems.append(f"{rel}: {len(text.splitlines())} lines, below the 40-line floor")
    return _fail(len(problems), json.dumps({"narrative_problems": problems[:40],
                                            "total": len(problems)}, sort_keys=True))


def check_reproduction_attestations(attestations):
    """F-28 (C-27). A reproducibility claim needs at least two runs on materially
    different hosts, each recording what it observed, and each stating plainly
    that the runner is the preparer rather than an independent party.
    """
    problems = []
    if len(attestations) < 2:
        problems.append(f"{len(attestations)} attestations, at least 2 required")
    platforms = set()
    for r in attestations:
        aid = r.get("attestation_id")
        platforms.add((r.get("host_platform") or "").strip())
        for column in ("observed_at_utc", "host_platform", "interpreter",
                       "validator_status", "attestor", "independence_state"):
            if not (r.get(column) or "").strip():
                problems.append(f"{aid}: {column} is empty")
        if (r.get("validator_status") or "").strip() not in {"PASS", "SET_AT_RUN_TIME"}:
            problems.append(f"{aid}: recorded validator_status is "
                            f"{r.get('validator_status')!r}, not PASS")
        if "NOT_INDEPENDENT" not in (r.get("independence_state") or ""):
            problems.append(f"{aid}: independence_state does not disclaim independence")
        if (r.get("signature_state") or "").strip() != "NOT_SIGNED_NO_SIGNING_KEY_PROVISIONED":
            problems.append(f"{aid}: signature_state overstates the signing position")
    if len(platforms) < 2:
        problems.append(f"all attestations share {len(platforms)} platform(s); "
                        "a second host was not exercised")
    return _fail(len(problems), json.dumps({"attestation_problems": problems},
                                           sort_keys=True))


def check_scope_delta_disclosure(text, removed_expected):
    """F-16. Round 2 removed sixteen V1 validator and test files and did not say
    so anywhere. The scope delta record must name every removed file and carry
    its V1 SHA-256, so the removal is a disclosed decision rather than a silent
    loss.
    """
    problems = []
    for name, digest in sorted(removed_expected.items()):
        if name not in text:
            problems.append(f"{name}: not disclosed")
        elif digest not in text:
            problems.append(f"{name}: disclosed without its V1 SHA-256")
    for heading in ("## Why This Record Exists", "## Files Removed",
                    "## What The Removed Files Checked", "## Where That Coverage Now Lives",
                    "## Reductions Not Restored"):
        if heading not in text:
            problems.append(f"the record is missing the section {heading!r}")
    return _fail(len(problems), json.dumps({"scope_delta_problems": problems,
                                            "expected_files": len(removed_expected)},
                                           sort_keys=True))


# ---------------------------------------------------------------------------
# Self-test. Every check above is driven with data that must make it FAIL.
# ---------------------------------------------------------------------------

def self_test_cases(tmp_factory=None):
    """Return ``[(case_name, failure_capable_confirmed), ...]``.

    Each case feeds a check synthetic data that violates it and asserts the
    check returns FAIL, then, where the passing shape is small enough to build
    by hand, feeds it conforming data and asserts PASS. A check that returns
    FAIL on everything is as useless as one that never fails.
    """
    out = []

    def case(name, status, expect="FAIL"):
        out.append((name, status == expect))

    # enum conformance
    s, _, _ = check_enum_conformance({
        "05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv":
            [{"selected_disposition": "APPROVED", "selected_disposition_enum_domain": "x"}],
    })
    case("enum_conformance_detects_out_of_domain_value", s)
    s, _, _ = check_enum_conformance({})
    case("enum_conformance_detects_missing_register", s)

    # referential integrity
    s, _, _ = check_referential_integrity({
        "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv":
            [{"source_id": "S1", "duplicate_cluster_id": "C-999", "sha256": "a"}],
        "08_SOURCE_RECONCILIATION/DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv": [],
    })
    case("referential_integrity_detects_dangling_cluster_id", s)
    s, _, _ = check_referential_integrity({
        "05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv":
            [{"decision_id": "D1"}],
        "FOUNDER_DECISION_PACKET.csv": [{"decision_id": "D2"}],
    })
    case("referential_integrity_detects_packet_register_id_drift", s)

    # arithmetic
    s, _, _ = check_cross_register_arithmetic({
        "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv":
            [{"candidate_test_file_id": "", "test_case_identified": "NO",
              "result": "NOT_EXECUTED", "runtime_evidence": "NOT_OBSERVED"}],
        "03_IMPLEMENTATION_TRACEABILITY/COVERAGE_METRICS_BY_DOMAIN.csv":
            [{"domain": "OVERALL", "total_canonical_requirements": "96",
              "candidate_test_files_identified": "0", "test_cases_specified": "0",
              "tests_executed": "0", "runtime_evidence_present": "0"}],
    })
    case("cross_register_arithmetic_detects_inflated_total", s)

    # decision register
    s, _, _ = check_decision_disposition_null_literal(
        [{"decision_id": "D1", "selected_disposition": "APPROVED",
          "round_2_selected_disposition_text_retained": "x", "authority_granted": ""}])
    case("decision_disposition_detects_outcome_prose", s)
    s, _, _ = check_decision_disposition_null_literal(
        [{"decision_id": "D1", "selected_disposition": "NO_DISPOSITION_SELECTED",
          "round_2_selected_disposition_text_retained": "x", "authority_granted": "NONE"}])
    case("decision_disposition_accepts_conforming_row", s, expect="PASS")

    s, _, _ = check_question_wording_identity(
        [{"decision_id": "D1", "question_presented": "A"}],
        [{"decision_id": "D1", "issue": "A but worded differently"}])
    case("question_wording_identity_detects_divergence", s)
    s, _, _ = check_question_wording_identity(
        [{"decision_id": "D1", "question_presented": "A"}],
        [{"decision_id": "D1", "issue": "A"}])
    case("question_wording_identity_accepts_identical_text", s, expect="PASS")

    s, _, _ = check_packet_recommendation_neutrality(
        [{"decision_id": "D1", "recommended_option": "Option 2",
          "consequences_of_each_option": "x", "relevant_evidence": "y"}])
    case("packet_recommendation_neutrality_detects_recommendation", s)

    # lifecycle matrix
    s, _, _ = check_lifecycle_matrix_completeness(
        [{"permitted_starting_state": "A", "permitted_next_state": "A", "permitted": "YES",
          "required_evidence": "",
          "prohibition_reason": "NOT_APPLICABLE_TRANSITION_IS_PERMITTED",
          "starting_state_declaration_source": "d", "next_state_declaration_source": "d"}],
        state_count=14)
    case("lifecycle_matrix_detects_partial_matrix", s)
    s, _, _ = check_lifecycle_matrix_completeness(
        [{"permitted_starting_state": a, "permitted_next_state": b, "permitted": "NO",
          "required_evidence": "", "prohibition_reason": "r",
          "starting_state_declaration_source": "d", "next_state_declaration_source": "d"}
         for a in "AB" for b in "AB"], state_count=2)
    case("lifecycle_matrix_accepts_total_matrix", s, expect="PASS")
    s, _, _ = check_lifecycle_matrix_completeness(
        [{"permitted_starting_state": a, "permitted_next_state": b, "permitted": "YES",
          "required_evidence": "same",
          "prohibition_reason": "NOT_APPLICABLE_TRANSITION_IS_PERMITTED",
          "starting_state_declaration_source": "d", "next_state_declaration_source": "d"}
         for a in "AB" for b in "AB"], state_count=2)
    case("lifecycle_matrix_detects_shared_evidence_text", s)

    # findings
    s, _, _ = check_findings_exemplar_separation(
        [{"record_id": "F1"}], [], [])
    case("findings_exemplar_separation_detects_illustrations_in_live_register", s)
    s, _, _ = check_findings_exemplar_separation(
        [], [{"record_id": "E1", "record_provenance": "REAL_FINDING",
              "classification_operative_effect": "x", "root_cause": "y",
              "root_cause_method": "z"}], [])
    case("findings_exemplar_separation_detects_undisclaimed_exemplar", s)
    s, _, _ = check_findings_exemplar_separation(
        [], [{"record_id": "E1",
              "record_provenance": "SCHEMA_EXEMPLAR_NOT_AN_OBSERVED_FINDING",
              "classification_operative_effect": "x", "root_cause": "y",
              "root_cause_method": "z"}],
        [{"issue_id": "U1", "underlying_item_count": "578",
          "underlying_population_locator": "doc08 register"}])
    case("findings_exemplar_separation_accepts_conforming_split", s, expect="PASS")
    s, _, _ = check_findings_exemplar_separation(
        [], [{"record_id": "E1",
              "record_provenance": "SCHEMA_EXEMPLAR_NOT_AN_OBSERVED_FINDING",
              "classification_operative_effect": "x", "root_cause": "y",
              "root_cause_method": "z"}],
        [{"issue_id": "U1", "underlying_item_count": "", "underlying_population_locator": ""}])
    case("findings_exemplar_separation_detects_unlocated_population", s)

    # review calendar
    s, _, _ = check_review_calendar_operability(
        [{"review_id": "R1", "next_review_date": "2026-01-01", "operative_state": "OPERATIVE",
          "escalation_addressee": "", "responsible_owner": "governance stewardship",
          "date_binding_state": "BINDING"}],
        [{"role": "governance stewardship", "appointment_evidence": "NONE"}])
    case("review_calendar_detects_operative_claim_without_appointment", s)
    s, _, _ = check_review_calendar_operability(
        [{"review_id": "R1", "proposed_next_review_date": "2026-01-01",
          "operative_state": "NOT_OPERATIVE_PENDING_FOUNDER_APPOINTMENT",
          "escalation_addressee": "founder", "responsible_owner": "governance stewardship",
          "date_binding_state": "PROPOSED_NOT_BINDING_NO_APPOINTED_OWNER_EXISTS"}],
        [{"role": "governance stewardship", "appointment_evidence": "NONE"}])
    case("review_calendar_accepts_proposed_non_operative_calendar", s, expect="PASS")

    # authority tense
    s, _, _ = check_authority_state_tense(
        [{"source_id": "S1", "authority_state": "DOCUMENT_IS_ADOPTED",
          "present_adoption_state": "NOT_ADOPTED_BY_THIS_PACKAGE",
          "authority_state_round_2_label_retained": "x"}])
    case("authority_state_tense_detects_present_tense_label", s)
    s, _, _ = check_authority_state_tense(
        [{"source_id": "S1", "authority_state": "HISTORICAL_ADOPTION_EVIDENCE_OBSERVED",
          "present_adoption_state": "NOT_ADOPTED_BY_THIS_PACKAGE",
          "authority_state_round_2_label_retained": "x"}])
    case("authority_state_tense_accepts_historical_label", s, expect="PASS")
    s, _, _ = check_authority_state_tense(
        [{"source_id": "S1", "authority_state": "HISTORICAL_ADOPTION_EVIDENCE_OBSERVED",
          "present_adoption_state": "NOT_ADOPTED_BY_THIS_PACKAGE",
          "authority_state_round_2_label_retained": ""}])
    case("authority_state_tense_detects_discarded_round_2_label", s)

    # workstream
    good_pr = {"pr_number": "82", "external_observation_method": "gh api",
               "external_observed_at_utc": "2026-08-01T00:00:00Z",
               "ci_observation_commit": "7748c47", "base_drift_definition": "d",
               "review_participation_evidence": "e",
               "commits_behind_base_branch_head": "0",
               "commits_ahead_of_base_branch_head": "18",
               "base_drift": "NO", "head_sha": "7748c477"}
    s, _, _ = check_workstream_external_observation([good_pr])
    case("workstream_external_observation_accepts_observed_row", s, expect="PASS")
    s, _, _ = check_workstream_external_observation([dict(good_pr, base_drift="YES")])
    case("workstream_external_observation_detects_drift_flag_contradiction", s)
    s, _, _ = check_workstream_external_observation(
        [dict(good_pr, external_observation_method="")])
    case("workstream_external_observation_detects_unsourced_row", s)
    s, _, _ = check_workstream_external_observation(
        [dict(good_pr, ci_observation_commit="deadbee")])
    case("workstream_external_observation_detects_ci_read_at_wrong_commit", s)

    # audit evidence
    s, _, _ = check_audit_evidence_distinctness(
        [{"requirement_id": "R1", "template_name": "A", "required_evidence": "same",
          "required_evidence_round_2_shared_text": "same"},
         {"requirement_id": "R2", "template_name": "B", "required_evidence": "same",
          "required_evidence_round_2_shared_text": "same"}])
    case("audit_evidence_distinctness_detects_shared_string", s)
    s, _, _ = check_audit_evidence_distinctness(
        [{"requirement_id": "R1", "template_name": "A", "required_evidence": "one",
          "required_evidence_round_2_shared_text": "same"},
         {"requirement_id": "R2", "template_name": "B", "required_evidence": "two",
          "required_evidence_round_2_shared_text": "same"}])
    case("audit_evidence_distinctness_accepts_distinct_strings", s, expect="PASS")

    s, _, _ = check_packet_citation_counts(
        [{"decision_id": "D1", "relevant_evidence":
          "UNRESOLVED_ISSUE_REGISTER.csv (5 issues)"}], [{}] * 6)
    case("packet_citation_counts_detects_stale_count", s)
    s, _, _ = check_packet_citation_counts(
        [{"decision_id": "D1", "relevant_evidence":
          "UNRESOLVED_ISSUE_REGISTER.csv (6 issues)"}], [{}] * 6)
    case("packet_citation_counts_accepts_current_count", s, expect="PASS")

    # narratives
    s, _, _ = check_narrative_completeness({"x.md": "# Title\n\nA short cover note.\n"})
    case("narrative_completeness_detects_cover_note", s)
    full = "\n".join(NARRATIVE_REQUIRED_HEADINGS) + "\nNOT_ADOPTED FOUNDER_REVIEW_REQUIRED\n" \
        + "\n".join(f"line {i}" for i in range(40))
    s, _, _ = check_narrative_completeness({"x.md": full})
    case("narrative_completeness_accepts_full_narrative", s, expect="PASS")

    # attestations
    good_att = {"attestation_id": "A1", "observed_at_utc": "t", "host_platform": "linux",
                "interpreter": "cpython", "validator_status": "PASS", "attestor": "preparer",
                "independence_state": "NOT_INDEPENDENT_RUN_BY_THE_PREPARER",
                "signature_state": "NOT_SIGNED_NO_SIGNING_KEY_PROVISIONED"}
    s, _, _ = check_reproduction_attestations([good_att])
    case("reproduction_attestations_detects_single_host", s)
    s, _, _ = check_reproduction_attestations(
        [good_att, dict(good_att, attestation_id="A2", host_platform="macos",
                        independence_state="INDEPENDENTLY_VERIFIED")])
    case("reproduction_attestations_detects_independence_overclaim", s)
    s, _, _ = check_reproduction_attestations(
        [good_att, dict(good_att, attestation_id="A2", host_platform="macos")])
    case("reproduction_attestations_accepts_two_hosts", s, expect="PASS")

    # scope delta
    s, _, _ = check_scope_delta_disclosure("nothing here", {"validate_document_03.py": "abc"})
    case("scope_delta_disclosure_detects_undisclosed_removal", s)
    s, _, _ = check_scope_delta_disclosure(
        "## Why This Record Exists\n## Files Removed\nvalidate_document_03.py abc\n"
        "## What The Removed Files Checked\n## Where That Coverage Now Lives\n"
        "## Reductions Not Restored\n", {"validate_document_03.py": "abc"})
    case("scope_delta_disclosure_accepts_full_disclosure", s, expect="PASS")

    # placeholder + parse, driven against a temporary tree when one is offered
    if tmp_factory is not None:
        tmp = Path(tmp_factory())
        (tmp / "bad.csv").write_text("a,b\n1,2,3\n", encoding="utf-8")
        s, _, _ = check_parse_integrity(tmp)
        case("parse_integrity_detects_ragged_csv", s)
        (tmp / "bad.csv").write_text("a,b\n1,2\n", encoding="utf-8")
        s, _, _ = check_parse_integrity(tmp)
        case("parse_integrity_accepts_well_formed_csv", s, expect="PASS")
        (tmp / "note.md").write_text("TODO: finish this\n", encoding="utf-8")
        s, _, _ = check_placeholder_markers(tmp)
        case("placeholder_markers_detects_unfinished_work_marker", s)
        (tmp / "note.md").write_text("This section is complete.\n", encoding="utf-8")
        s, _, _ = check_placeholder_markers(tmp)
        case("placeholder_markers_accepts_clean_tree", s, expect="PASS")
        s, _, _ = check_per_document_required_files(tmp, {"03_X": ["MISSING.csv"]})
        case("per_document_required_files_detects_missing_register", s)
        (tmp / "03_X").mkdir(exist_ok=True)
        (tmp / "03_X" / "MISSING.csv").write_text("a\n1\n", encoding="utf-8")
        s, _, _ = check_per_document_required_files(tmp, {"03_X": ["MISSING.csv"]})
        case("per_document_required_files_accepts_complete_document", s, expect="PASS")

    return out
