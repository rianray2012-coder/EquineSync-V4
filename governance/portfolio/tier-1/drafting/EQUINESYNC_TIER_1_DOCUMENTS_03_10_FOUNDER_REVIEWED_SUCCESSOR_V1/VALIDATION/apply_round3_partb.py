#!/usr/bin/env python3
"""
EquineSync Tier 1 - Round 3 Part B remediation transforms.

Scope: findings F-07 through F-28 of the external standards benchmark review,
and the Section 2 crosswalk observations C-03, C-04, C-05, C-07, C-08, C-09,
C-10, C-11, C-12, C-13, C-14, C-15, C-16, C-17, C-18, C-19, C-20, C-21, C-23,
C-24 (remainder) and C-27.

Every transform is idempotent: running the script twice produces byte-identical
output. No transform asserts adoption, activation, implementation authorisation,
production authorisation, merge authorisation, certification, or legal
compliance. Where a fact is not determinable from the package or from an
authenticated external observation, the transform writes an explicit
non-determination literal rather than a value.

Authority boundary preserved by every transform:
NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED;
MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED;
UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED
"""
from __future__ import annotations

import collections
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

D03 = ROOT / "03_IMPLEMENTATION_TRACEABILITY"
D04 = ROOT / "04_AUTHORITY_LIFECYCLE_REGISTER"
D05 = ROOT / "05_FOUNDER_DECISION_REGISTER"
D06 = ROOT / "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS"
D07 = ROOT / "07_OWNERSHIP_STEWARDSHIP_REVIEW"
D08 = ROOT / "08_SOURCE_RECONCILIATION"
D09 = ROOT / "09_WORKSTREAM_PR_BRANCH_DISPOSITION"
D10 = ROOT / "10_CLOSING_AUDIT_PROTOCOL"

NOT_DET = "NOT_DETERMINED_BY_THIS_PACKAGE"


# --------------------------------------------------------------------------
# CSV helpers
# --------------------------------------------------------------------------
def read_csv(path: pathlib.Path):
    with path.open(newline="", encoding="utf-8") as fh:
        rdr = csv.DictReader(fh)
        return list(rdr.fieldnames or []), list(rdr)


def write_csv(path: pathlib.Path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def insert_after(fields, anchor, new_cols):
    """Return a field list with new_cols inserted after anchor, no duplicates."""
    out = [f for f in fields if f not in new_cols]
    idx = out.index(anchor) + 1 if anchor in out else len(out)
    return out[:idx] + list(new_cols) + out[idx:]


def rename_field(fields, old, new):
    return [new if f == old else f for f in fields]


# ==========================================================================
# F-14 / F-17 / F-18 / F-26  -> C-03, C-04  Document 03 traceability register
# ==========================================================================
CONFIDENCE_RUBRIC = {
    # (path_verification_state) -> (confidence, confidence_basis)
    "IMPLEMENTATION_CANDIDATE_LOCATED": (
        "MEDIUM",
        "RUBRIC_L2_PATH_LOCATED_SYMBOL_UNRESOLVED_NO_EXECUTION",
    ),
    "NO_IMPLEMENTATION_CANDIDATE_LOCATED": (
        "LOW",
        "RUBRIC_L1_NO_IMPLEMENTATION_CANDIDATE_LOCATED",
    ),
}


def partb_document_03_register():
    """F-14, F-17, F-18, F-26 (C-03, C-04).

    - test_id renamed to candidate_test_file_id; adds test_case_identified so a
      file-level candidate can no longer be read as a specified test case.
    - symbol identifier column renamed and paired with an explicit
      symbol_resolution_state.
    - confidence values become derivable from a published rubric
      (confidence_basis), removing the unstated scale in F-17.
    - source_version_declaration_state distinguishes "no version string in the
      source" from "version unknown to the reviewer" (F-18).
    - backward_trace_state and design_tier_state make the absent bidirectional
      traceability and absent design tier explicit rather than silent (F-26,
      ISO/IEC/IEEE 29148:2018 Cl. 5.2.8 bidirectional traceability).
    """
    path = D03 / "REQUIREMENT_TRACEABILITY_REGISTER.csv"
    fields, rows = read_csv(path)

    fields = rename_field(fields, "test_id", "candidate_test_file_id")
    fields = rename_field(
        fields,
        "symbol_class_function_endpoint_component_migration_job_event_policy_identifier",
        "candidate_symbol_identifier",
    )
    fields = insert_after(fields, "source_version", ["source_version_declaration_state"])
    fields = insert_after(fields, "candidate_symbol_identifier", ["symbol_resolution_state"])
    fields = insert_after(fields, "candidate_test_file_id", ["test_case_identified"])
    fields = insert_after(fields, "confidence", ["confidence_basis"])
    fields = insert_after(
        fields, "requirement_status", ["backward_trace_state", "design_tier_state"]
    )

    for r in rows:
        if "test_id" in r:
            r["candidate_test_file_id"] = r.pop("test_id")
        old_sym = "symbol_class_function_endpoint_component_migration_job_event_policy_identifier"
        if old_sym in r:
            r["candidate_symbol_identifier"] = r.pop(old_sym)

        # F-18
        r["source_version_declaration_state"] = (
            "NO_VERSION_STRING_PRESENT_IN_CONTROLLING_SOURCE"
            if r.get("source_version") == "VERSION_NOT_DECLARED"
            else "VERSION_STRING_PRESENT"
        )

        # F-14 (a): symbol resolution
        sym = (r.get("candidate_symbol_identifier") or "").strip()
        if sym == "PATH_LEVEL_CANDIDATE_ONLY":
            r["symbol_resolution_state"] = "SYMBOL_NOT_RESOLVED_PATH_LEVEL_ONLY"
        elif sym == "":
            r["symbol_resolution_state"] = "NO_CANDIDATE_PATH_NO_SYMBOL_TO_RESOLVE"
        else:
            r["symbol_resolution_state"] = "SYMBOL_RESOLVED"

        # F-14 (b): test case vs test file
        loc = (r.get("exact_test_or_assertion_locator") or "").strip()
        tid = (r.get("candidate_test_file_id") or "").strip()
        if tid and loc == "FILE_LEVEL_CANDIDATE_ONLY":
            r["test_case_identified"] = "NO_FILE_LEVEL_CANDIDATE_ONLY"
        elif not tid:
            r["test_case_identified"] = "NO_NO_TEST_FILE_CANDIDATE"
        else:
            r["test_case_identified"] = "YES"

        # F-17
        conf, basis = CONFIDENCE_RUBRIC.get(
            r.get("path_verification_state", ""), ("LOW", "RUBRIC_L1_DEFAULT")
        )
        r["confidence"] = conf
        r["confidence_basis"] = basis

        # F-26 / C-04
        r["backward_trace_state"] = "NO_BACKWARD_TRACE_RECORDED_NO_IMPLEMENTATION_INDEX_EXISTS"
        r["design_tier_state"] = "NO_DESIGN_TIER_ARTIFACT_EXISTS_IN_THIS_PACKAGE"

    write_csv(path, fields, rows)
    return len(rows)


# ==========================================================================
# F-13 -> C-05  Document 03 coverage metrics
# ==========================================================================
def partb_document_03_coverage():
    """F-13 (C-05).

    Recomputes every metric from REQUIREMENT_TRACEABILITY_REGISTER.csv rather
    than restating drafted numbers, renames the misleading coverage percentage
    to candidate_match_rate_percentage, publishes verified_coverage_percentage
    (0.0) alongside it, and collapses the unfalsifiable tests_specified ==
    tests_located pair into a single measured column with an explicit
    test_cases_specified count.
    """
    _, reg = read_csv(D03 / "REQUIREMENT_TRACEABILITY_REGISTER.csv")

    fields = [
        "domain",
        "total_canonical_requirements",
        "mapped_requirements",
        "implementation_candidates_identified",
        "implementations_verified",
        "candidate_test_files_identified",
        "test_cases_specified",
        "tests_executed",
        "tests_passed",
        "negative_tests_present",
        "runtime_evidence_present",
        "requirements_with_open_evidence_gap",
        "requirements_with_candidates_not_executed",
        "requirements_with_no_owner",
        "candidate_match_rate_percentage",
        "verified_coverage_percentage",
        "executed_test_coverage_percentage",
        "metric_derivation",
        "unavailable_metric_treatment",
    ]

    def metrics(subset):
        n = len(subset)
        located = sum(
            1 for r in subset if r["path_verification_state"] == "IMPLEMENTATION_CANDIDATE_LOCATED"
        )
        testfiles = sum(1 for r in subset if (r.get("candidate_test_file_id") or "").strip())
        testcases = sum(1 for r in subset if r.get("test_case_identified") == "YES")
        open_gap = sum(1 for r in subset if r["gap_state"] == "OPEN_EVIDENCE_GAP")
        cand_ne = sum(
            1
            for r in subset
            if r["gap_state"] == "IMPLEMENTATION_AND_TEST_CANDIDATES_IDENTIFIED_NOT_EXECUTED"
        )
        no_owner = sum(
            1 for r in subset if r["owner"].strip() in ("", "FOUNDER_APPOINTMENT_REQUIRED")
        )
        return {
            "total_canonical_requirements": n,
            "mapped_requirements": located,
            "implementation_candidates_identified": located,
            "implementations_verified": 0,
            "candidate_test_files_identified": testfiles,
            "test_cases_specified": testcases,
            "tests_executed": 0,
            "tests_passed": 0,
            "negative_tests_present": 0,
            "runtime_evidence_present": 0,
            "requirements_with_open_evidence_gap": open_gap,
            "requirements_with_candidates_not_executed": cand_ne,
            "requirements_with_no_owner": no_owner,
            "candidate_match_rate_percentage": (
                f"{(located / n * 100):.1f}" if n else "NOT_APPLICABLE_ZERO_REQUIREMENTS"
            ),
            "verified_coverage_percentage": "0.0",
            "executed_test_coverage_percentage": "0.0",
        }

    derivation = (
        "Recomputed in Round 3 Part B directly from REQUIREMENT_TRACEABILITY_REGISTER.csv. "
        "mapped_requirements counts path_verification_state=IMPLEMENTATION_CANDIDATE_LOCATED. "
        "candidate_test_files_identified counts non-empty candidate_test_file_id. "
        "test_cases_specified counts test_case_identified=YES. "
        "candidate_match_rate_percentage = implementation_candidates_identified / "
        "total_canonical_requirements and is a location rate, not a satisfaction rate. "
        "verified_coverage_percentage is 0.0 because no implementation was reviewed at symbol "
        "level and no test was executed."
    )
    unavailable = (
        "Executed, runtime, and production metrics are zero because this documentary review "
        "executed no tests and observed no runtime behavior. Zero here means NOT_OBSERVED, not "
        "OBSERVED_AND_FAILED."
    )

    domains = sorted({r["product_domain"] for r in reg})
    rows = []
    for d in domains:
        row = {"domain": d}
        row.update(metrics([r for r in reg if r["product_domain"] == d]))
        row["metric_derivation"] = derivation
        row["unavailable_metric_treatment"] = unavailable
        rows.append(row)
    overall = {"domain": "OVERALL"}
    overall.update(metrics(reg))
    overall["metric_derivation"] = derivation
    overall["unavailable_metric_treatment"] = unavailable
    rows.append(overall)

    write_csv(D03 / "COVERAGE_METRICS_BY_DOMAIN.csv", fields, rows)
    return rows[-1]


# ==========================================================================
# F-15 -> C-07, C-08  Document 04 lifecycle transition matrix
# ==========================================================================
DECLARED_STATES = [
    "DRAFT_UNMERGED",
    "CANDIDATE",
    "BLOCKED_EVIDENCE_REQUIRED",
    "FOUNDER_REVIEW_READY",
    "ADOPTED",
    "LOCKED",
    "ACCESSIONED",
    "ACTIVE",
    "SUSPENDED",
    "SUPERSEDED",
    "HISTORICAL_RETAINED",
]
ADDED_STATES = ["REJECTED", "REMEDIATION_REQUIRED", "WITHDRAWN"]
ALL_STATES = DECLARED_STATES + ADDED_STATES

# (from, to) -> (required_authority, required_evidence)
PERMITTED = {
    ("DRAFT_UNMERGED", "CANDIDATE"): (
        "REVIEW_PREPARER",
        "Complete artifact set present and self-consistent; package manifest recomputed",
    ),
    ("DRAFT_UNMERGED", "WITHDRAWN"): (
        "REVIEW_PREPARER",
        "Written withdrawal note recorded in the program control record, naming the draft "
        "artifact and stating that no candidate was ever tendered for review",
    ),
    ("CANDIDATE", "BLOCKED_EVIDENCE_REQUIRED"): (
        "REVIEW_PREPARER",
        "Named missing evidence item recorded in the findings register",
    ),
    ("CANDIDATE", "FOUNDER_REVIEW_READY"): (
        "REVIEW_PREPARER",
        "Validator run with zero failures and manifest self-authentication satisfied",
    ),
    ("CANDIDATE", "WITHDRAWN"): (
        "REVIEW_PREPARER",
        "Written withdrawal note recorded in the program control record, naming the tendered "
        "candidate version and hash being withdrawn",
    ),
    ("BLOCKED_EVIDENCE_REQUIRED", "CANDIDATE"): (
        "REVIEW_PREPARER",
        "The named missing evidence item is attached and its finding is closed with evidence",
    ),
    ("BLOCKED_EVIDENCE_REQUIRED", "WITHDRAWN"): (
        "REVIEW_PREPARER",
        "Written withdrawal note recorded in the program control record, naming the unmet "
        "evidence item that will not be supplied and the finding it leaves open",
    ),
    ("FOUNDER_REVIEW_READY", "ADOPTED"): (
        "FOUNDER",
        "Signed Founder decision text naming this exact artifact version and hash",
    ),
    ("FOUNDER_REVIEW_READY", "REJECTED"): (
        "FOUNDER",
        "Signed Founder decision text recording rejection and its stated basis",
    ),
    ("FOUNDER_REVIEW_READY", "REMEDIATION_REQUIRED"): (
        "FOUNDER",
        "Signed Founder decision text naming each required remediation item",
    ),
    ("FOUNDER_REVIEW_READY", "WITHDRAWN"): (
        "FOUNDER",
        "Signed Founder withdrawal instruction naming the review-ready version and hash and "
        "stating that the pending review is discontinued without a decision",
    ),
    ("REMEDIATION_REQUIRED", "CANDIDATE"): (
        "REVIEW_PREPARER",
        "Every named remediation item closed with attached evidence and a recomputed manifest",
    ),
    ("REMEDIATION_REQUIRED", "WITHDRAWN"): (
        "FOUNDER",
        "Signed Founder withdrawal instruction naming each outstanding remediation item that "
        "will not be completed",
    ),
    ("REJECTED", "DRAFT_UNMERGED"): (
        "FOUNDER",
        "Signed Founder instruction authorising a new drafting cycle",
    ),
    ("ADOPTED", "LOCKED"): (
        "RECORDS_AND_EVIDENCE_CUSTODY",
        "Immutable stored copy with recorded hash and custody entry",
    ),
    ("ADOPTED", "REMEDIATION_REQUIRED"): (
        "FOUNDER",
        "Signed Founder rescission naming the defect and the required remediation",
    ),
    ("LOCKED", "ACCESSIONED"): (
        "RECORDS_AND_EVIDENCE_CUSTODY",
        "Accession number assigned and retention schedule recorded",
    ),
    ("ACCESSIONED", "ACTIVE"): (
        "RELEASE_AUTHORITY",
        "Activation instruction plus evidence the artifact is in operative use",
    ),
    ("ACTIVE", "SUSPENDED"): (
        "RELEASE_AUTHORITY",
        "Suspension instruction stating the basis and the reactivation condition",
    ),
    ("ACTIVE", "SUPERSEDED"): (
        "FOUNDER",
        "Named successor artifact with its own hash, or a documented basis for supersession "
        "without a successor",
    ),
    ("ACTIVE", "REMEDIATION_REQUIRED"): (
        "FOUNDER",
        "Signed Founder instruction naming the defect and the required remediation",
    ),
    ("SUSPENDED", "ACTIVE"): (
        "RELEASE_AUTHORITY",
        "Evidence that the recorded reactivation condition is satisfied",
    ),
    ("SUSPENDED", "SUPERSEDED"): (
        "FOUNDER",
        "Named successor artifact with its own hash, or a documented basis for supersession",
    ),
    ("SUPERSEDED", "HISTORICAL_RETAINED"): (
        "RECORDS_AND_EVIDENCE_CUSTODY",
        "Retention entry preserving prior truth without present-tense control claims",
    ),
    ("WITHDRAWN", "HISTORICAL_RETAINED"): (
        "RECORDS_AND_EVIDENCE_CUSTODY",
        "Retention entry preserving the withdrawn artifact and the withdrawal note",
    ),
    ("REJECTED", "HISTORICAL_RETAINED"): (
        "RECORDS_AND_EVIDENCE_CUSTODY",
        "Retention entry preserving the rejected artifact and the rejection basis",
    ),
}

TERMINAL_STATES = {"HISTORICAL_RETAINED"}


def partb_document_04_matrix():
    """F-15 (C-07, C-08).

    Rebuilds the transition matrix over the full declared state vocabulary
    (11 states) plus the three adverse states whose absence F-15 identified,
    giving 14 x 14 = 196 rows. Every row carries a distinct, transition-specific
    required_evidence string; prohibited rows carry a prohibition_reason rather
    than the single literal PROHIBITED_TRANSITION used in Round 2. The three
    added states are labelled so a reader can tell which states came from the
    Document 04 state list and which were added in Round 3 Part B.
    """
    fields = [
        "permitted_starting_state",
        "starting_state_declaration_source",
        "permitted_next_state",
        "next_state_declaration_source",
        "permitted",
        "required_authority",
        "required_evidence",
        "prohibition_reason",
        "reversal_rule",
        "suspension_rule",
        "supersession_rule",
        "reactivation_rule",
        "archival_rule",
    ]

    def source_of(state):
        return (
            "DECLARED_IN_DOCUMENT_04_STATE_LIST"
            if state in DECLARED_STATES
            else "ADDED_IN_ROUND_3_PART_B_TO_CLOSE_FINDING_F_15"
        )

    rows = []
    for a in ALL_STATES:
        for b in ALL_STATES:
            key = (a, b)
            row = {
                "permitted_starting_state": a,
                "starting_state_declaration_source": source_of(a),
                "permitted_next_state": b,
                "next_state_declaration_source": source_of(b),
                "reversal_rule": (
                    "No state may be reversed except by the explicit reverse transition listed "
                    "as permitted in this matrix"
                ),
                "suspension_rule": (
                    "Suspension removes operative effect but does not alter adoption state or "
                    "custody records"
                ),
                "supersession_rule": (
                    "Supersession requires a named successor artifact with its own hash, or a "
                    "recorded basis for supersession without a successor"
                ),
                "reactivation_rule": (
                    "Reactivation requires evidence that the recorded reactivation condition is "
                    "satisfied and requires RELEASE_AUTHORITY"
                ),
                "archival_rule": (
                    "Historical retention preserves prior truth and must not be written in the "
                    "present tense as an operative control"
                ),
            }
            if key in PERMITTED:
                auth, ev = PERMITTED[key]
                row.update(
                    permitted="YES",
                    required_authority=auth,
                    required_evidence=ev,
                    prohibition_reason="NOT_APPLICABLE_TRANSITION_IS_PERMITTED",
                )
            else:
                if a == b:
                    reason = "SELF_TRANSITION_IS_NOT_A_STATE_CHANGE"
                elif a in TERMINAL_STATES:
                    reason = (
                        f"{a} is terminal; exit requires a new artifact version rather than a "
                        f"transition of this artifact"
                    )
                else:
                    reason = (
                        f"No authority or evidence rule has been defined for {a} to {b}; the "
                        f"transition is prohibited until one is defined and Founder-approved"
                    )
                row.update(
                    permitted="NO",
                    required_authority="NOT_APPLICABLE_TRANSITION_IS_PROHIBITED",
                    required_evidence="NOT_APPLICABLE_TRANSITION_IS_PROHIBITED",
                    prohibition_reason=reason,
                )
            rows.append(row)

    write_csv(D04 / "LIFECYCLE_TRANSITION_MATRIX.csv", fields, rows)
    return len(rows), sum(1 for r in rows if r["permitted"] == "YES")


# ==========================================================================
# F-07, F-08, F-09, F-24 -> C-09, C-10, C-11  Document 05 + decision packet
# ==========================================================================
DISPOSITION_ENUM = ["approve", "approve with modification", "defer", "reject", "require remediation"]
NO_DISPOSITION = "NO_DISPOSITION_SELECTED"

# F-09 / C-11: one canonical question string per decision, used byte-identically
# in the disposition register, the packet CSV and the packet MD. The narrower
# Round 2 wording is retained as canonical because a documentary package must
# not widen the scope of a question it is presenting to the Founder.
CANONICAL_QUESTION = {
    "FD-T1R2-001": "Approve lifecycle authority vocabulary for future use",
    "FD-T1R2-002": "Appoint accountable governance roles",
    "FD-T1R2-003": "Approve source-control hierarchy",
    "FD-T1R2-004": "Accept or remediate unresolved residual risks",
    "FD-T1R2-005": "Authorize future merge sequencing",
}

# F-24 / C-10: decision-specific consequences and decision-specific evidence
# locators, replacing the five identical strings.
DECISION_DETAIL = {
    "FD-T1R2-001": {
        "consequences": (
            "approve: the state and transition vocabulary in "
            "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv becomes the "
            "vocabulary future packages must use; it does not move any artifact into any state. "
            "| approve with modification: the vocabulary is usable only as amended by the "
            "Founder text, and the matrix must be rebuilt before reuse. "
            "| defer: no vocabulary is settled and every future package must restate its own "
            "state definitions. "
            "| reject: the matrix is withdrawn and Document 04 must be redrafted from the "
            "state list upward. "
            "| require remediation: the named defects must be closed and the matrix "
            "re-validated before the question is re-presented."
        ),
        "evidence": (
            "04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv (196 rows, 14 "
            "states); 04_AUTHORITY_LIFECYCLE_REGISTER/"
            "EQUINESYNC_AUTHORITY_LIFECYCLE_STATE_AND_TRANSITION_REGISTER_REVISION_ROUND_2_V1.md"
        ),
    },
    "FD-T1R2-002": {
        "consequences": (
            "approve: named functions become accountable for the 14 roles in "
            "07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv and the 14 "
            "reviews in REVIEW_CALENDAR.csv stop being NOT_OPERATIVE. "
            "| approve with modification: only the roles the Founder names become accountable; "
            "the remainder stay vacant and their reviews stay non-operative. "
            "| defer: all 14 roles stay VACANT_PENDING_FOUNDER_APPOINTMENT, no review date is "
            "binding on anyone, and every escalation deadline is unenforceable. "
            "| reject: the role model itself is withdrawn and Document 07 must be redrafted. "
            "| require remediation: the appointment and acceptance evidence fields must be "
            "populated before the question is re-presented."
        ),
        "evidence": (
            "07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv (14 roles); "
            "07_OWNERSHIP_STEWARDSHIP_REVIEW/VACANCY_AND_SUCCESSION_REGISTER.csv (14 rows, all "
            "VACANT_PENDING_FOUNDER_APPOINTMENT); 07_OWNERSHIP_STEWARDSHIP_REVIEW/"
            "REVIEW_CALENDAR.csv (14 reviews, all NOT_COMPLETED)"
        ),
    },
    "FD-T1R2-003": {
        "consequences": (
            "approve: the preferred representation recorded for each of the 68 duplicate "
            "clusters in 08_SOURCE_RECONCILIATION/DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv "
            "becomes controlling, and canonical_representation can be resolved for the 145 "
            "rows currently marked CANONICAL_NOT_DETERMINED. "
            "| approve with modification: only the clusters the Founder names are resolved. "
            "| defer: canonical_representation stays CANONICAL_NOT_DETERMINED for all 145 "
            "cluster member rows and the version conflict in cluster T1R2-SRC-CLUSTER-001 "
            "stays open. "
            "| reject: no hierarchy exists and every duplicate must be treated as an "
            "independent source. "
            "| require remediation: a written canonicality rule must be drafted and applied "
            "before the question is re-presented."
        ),
        "evidence": (
            "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv (2961 rows, "
            "2884 unique SHA-256 values); 08_SOURCE_RECONCILIATION/"
            "DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv (68 clusters, 145 member rows, 77 "
            "redundant copies); 08_SOURCE_RECONCILIATION/SOURCE_DISPOSITION_DASHBOARD.csv"
        ),
    },
    "FD-T1R2-004": {
        "consequences": (
            "approve: not available as drafted, because this package records no observed "
            "finding to accept. "
            "| approve with modification: the Founder must name the specific risk being "
            "accepted, since none is recorded. "
            "| defer: accepted_risks stays NONE_ACCEPTED_BY_THIS_PACKAGE and no residual risk "
            "position exists. "
            "| reject: the question is withdrawn as unanswerable on the present evidence. "
            "| require remediation: a real findings population must be produced before any "
            "acceptance question can be presented, because "
            "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/"
            "FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv contains zero observed findings."
        ),
        "evidence": (
            "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv "
            "(0 observed rows); 06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/"
            "FINDINGS_RISKS_EXCEPTIONS_WAIVERS_SCHEMA_EXEMPLAR.csv (8 exemplar rows, not "
            "findings); UNRESOLVED_ISSUE_REGISTER.csv (UNRESOLVED_ISSUE_COUNT issues)"
        ),
    },
    "FD-T1R2-005": {
        "consequences": (
            "approve: not available as drafted, because merge authority is outside the scope "
            "of a documentary package and MERGE_NOT_AUTHORIZED is a boundary of this review. "
            "| approve with modification: the Founder may issue a separate merge directive "
            "naming exact pull requests and exact head SHAs. "
            "| defer: all nine pull requests in "
            "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv "
            "stay unmerged and six of the nine continue to drift further behind the base "
            "branch. "
            "| reject: the pull requests are retained as historical candidates only. "
            "| require remediation: the six pull requests behind the base branch must be "
            "rebased and the failing check on pull request 70 must be resolved before the "
            "question is re-presented."
        ),
        "evidence": (
            "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv "
            "(9 pull requests; 6 behind base; 1 failing check on pull request 70); "
            "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_DISPOSITION_REPORT.md"
        ),
    },
}


def partb_document_05_register():
    """F-07 (C-09), F-09 (C-11).

    selected_disposition is forced to the single null literal NO_DISPOSITION_SELECTED
    on all five rows, because exact_decision_text is
    NO_FOUNDER_DECISION_RECORDED_IN_THIS_PACKAGE and authority_granted is
    NONE_BY_THIS_PACKAGE on all five. The Round 2 strings are preserved rather
    than discarded. question_presented is set to the canonical string.
    """
    path = D05 / "FOUNDER_DECISION_DISPOSITION_REGISTER.csv"
    fields, rows = read_csv(path)
    fields = insert_after(
        fields,
        "selected_disposition",
        ["selected_disposition_enum_domain", "round_2_selected_disposition_text_retained"],
    )
    for r in rows:
        did = r["decision_id"]
        if r["selected_disposition"] != NO_DISPOSITION:
            r["round_2_selected_disposition_text_retained"] = r["selected_disposition"]
        r["selected_disposition"] = NO_DISPOSITION
        r["selected_disposition_enum_domain"] = (
            "; ".join(DISPOSITION_ENUM) + f"; {NO_DISPOSITION} (null literal, no decision recorded)"
        )
        r["question_presented"] = CANONICAL_QUESTION[did]
    write_csv(path, fields, rows)
    return len(rows)


def partb_decision_packet_csv():
    """F-08, F-09 (C-11), F-24 (C-10).

    recommended_option is set to NO_RECOMMENDATION_MADE_BY_THIS_PACKAGE on all
    five rows: a documentary package with authority_granted=NONE_BY_THIS_PACKAGE
    cannot pre-state an outcome, and three of the five Round 2 values were not
    members of the options enum they claimed to select from. The drafted text is
    retained as a non-recommendation note. issue is set byte-identical to
    question_presented in the disposition register. consequences and evidence
    become decision-specific.
    """
    path = ROOT / "FOUNDER_DECISION_PACKET.csv"
    fields, rows = read_csv(path)
    fields = insert_after(
        fields,
        "recommended_option",
        ["recommendation_authority_state", "round_2_drafting_note_not_a_recommendation"],
    )
    fields = insert_after(fields, "issue", ["round_2_issue_text_retained"])
    for r in rows:
        did = r["decision_id"]
        canonical = CANONICAL_QUESTION[did]
        if r["issue"] != canonical and not r.get("round_2_issue_text_retained"):
            r["round_2_issue_text_retained"] = r["issue"]
        elif not r.get("round_2_issue_text_retained"):
            r["round_2_issue_text_retained"] = "NO_VARIANT_ROUND_2_TEXT_MATCHED_CANONICAL"
        r["issue"] = canonical

        if r["recommended_option"] != "NO_RECOMMENDATION_MADE_BY_THIS_PACKAGE":
            r["round_2_drafting_note_not_a_recommendation"] = r["recommended_option"]
        r["recommended_option"] = "NO_RECOMMENDATION_MADE_BY_THIS_PACKAGE"
        r["recommendation_authority_state"] = (
            "THIS_PACKAGE_HOLDS_NO_AUTHORITY_TO_RECOMMEND_A_DISPOSITION"
        )
        r["options"] = "; ".join(DISPOSITION_ENUM)
        r["consequences_of_each_option"] = DECISION_DETAIL[did]["consequences"]
        r["relevant_evidence"] = DECISION_DETAIL[did]["evidence"]
    write_csv(path, fields, rows)
    return len(rows)


def partb_decision_packet_md():
    """F-09 (C-11), F-27. Rewrites the 7-line packet narrative."""
    lines = [
        "# Founder Decision Packet",
        "",
        "Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; "
        "PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; "
        "FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.",
        "",
        "## Purpose",
        "",
        "This packet presents the five questions that this documentary package cannot answer "
        "on its own authority. It records no decision, selects no disposition, and makes no "
        "recommendation.",
        "",
        "## Recommendation Status",
        "",
        "`recommended_option` is `NO_RECOMMENDATION_MADE_BY_THIS_PACKAGE` for all five "
        "decisions. In Revision Round 2 this field carried drafted outcome text, three "
        "instances of which were not members of the options enum they claimed to select from. "
        "That text is retained in `round_2_drafting_note_not_a_recommendation` in "
        "`FOUNDER_DECISION_PACKET.csv` as drafting history, not as advice.",
        "",
        "## Question Wording Control",
        "",
        "Each `issue` string below is byte-identical to the `question_presented` value for the "
        "same `decision_id` in "
        "`05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv`. Where "
        "Revision Round 2 wording differed between the two artifacts, the narrower wording is "
        "canonical and the wider variant is retained in `round_2_issue_text_retained`. A "
        "documentary package must not widen the scope of a question it presents to the Founder.",
        "",
        "## Decisions Presented",
        "",
    ]
    _, rows = read_csv(ROOT / "FOUNDER_DECISION_PACKET.csv")
    for r in rows:
        lines.append(f"### `{r['decision_id']}`")
        lines.append("")
        lines.append(f"- Question presented: {r['issue']}")
        lines.append(f"- Options: `{r['options']}`")
        lines.append(f"- Recommended option: `{r['recommended_option']}`")
        lines.append(
            f"- Round 2 drafting note (not a recommendation): "
            f"`{r['round_2_drafting_note_not_a_recommendation']}`"
        )
        lines.append(f"- Round 2 variant wording retained: `{r['round_2_issue_text_retained']}`")
        lines.append(f"- Evidence relied on: {r['relevant_evidence']}")
        lines.append("")
    lines += [
        "## Options Enum",
        "",
        "`" + "; ".join(DISPOSITION_ENUM) + "`",
        "",
        "Until a Founder decision is recorded, `selected_disposition` in the disposition "
        "register is the null literal `NO_DISPOSITION_SELECTED` for every decision.",
        "",
        "## Status",
        "",
        "`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; "
        "MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; "
        "UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`",
        "",
    ]
    (ROOT / "FOUNDER_DECISION_PACKET.md").write_text("\n".join(lines), encoding="utf-8")
    return len(lines)


def main():
    print("document_03_register rows =", partb_document_03_register())
    print("document_03_coverage overall =", json.dumps(partb_document_03_coverage()))
    print("document_04_matrix rows,permitted =", partb_document_04_matrix())
    print("document_05_register rows =", partb_document_05_register())
    print("decision_packet_csv rows =", partb_decision_packet_csv())
    print("decision_packet_md lines =", partb_decision_packet_md())


if __name__ == "__main__":
    sys.exit(main())
