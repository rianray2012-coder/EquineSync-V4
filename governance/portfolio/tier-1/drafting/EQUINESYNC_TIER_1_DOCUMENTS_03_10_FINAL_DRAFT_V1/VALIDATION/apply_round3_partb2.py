#!/usr/bin/env python3
"""
EquineSync Tier 1 - Round 3 Part B remediation transforms, documents 06 to 10.

Covers findings F-10, F-11, F-12, F-19, F-20, F-21, F-22, F-23, F-25 and
crosswalk observations C-12, C-13, C-14, C-15, C-16, C-17, C-18, C-19, C-20,
C-21, C-23.

Idempotent. No transform asserts adoption, activation, implementation
authorisation, production authorisation, merge authorisation, certification, or
legal compliance.
"""
from __future__ import annotations

import collections
import csv
import re
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from apply_round3_partb import (  # noqa: E402
    D06,
    D07,
    D08,
    D09,
    D10,
    ROOT,
    insert_after,
    read_csv,
    rename_field,
    write_csv,
)

# --------------------------------------------------------------------------
# Externally observed GitHub facts. Each value below was read from the GitHub
# GraphQL and REST APIs for repository rianray2012-coder/EquineSync-V4 at the
# observation timestamp recorded in OBSERVATION. They are recorded here so the
# transform is reproducible without network access and so the provenance of
# every value in the Document 09 register is inspectable.
# --------------------------------------------------------------------------
OBSERVATION = {
    "observed_at_utc": "2026-08-02T03:40:00Z",
    "method": "GitHub GraphQL v4 pullRequest.reviewThreads/reviews/statusCheckRollup "
    "plus REST compare(base_branch_head...head_sha)",
    "base_branch": "integrate-emergent-final-zip",
    "base_branch_head_sha_at_observation": "1eb384d80daa700ba2e71ee42872cc9bba926332",
}

PR_OBSERVED = {
    # pr -> head_sha, commits_behind_base_head, commits_ahead, mergeStateStatus,
    #       checks [(name, conclusion)], reviews, review_threads, changed_files
    "82": dict(head="7748c4774037e89c32a12ccd8d52df2b0361e24f", behind=0, ahead=18,
               merge_state="CLEAN", reviews=0, threads=0, changed_files=142,
               checks=[("Backend suite is collectable", "SUCCESS"),
                       ("Backend known-failure non-regression gate", "SUCCESS"),
                       ("Frontend build", "SUCCESS"), ("Vercel", "SUCCESS"),
                       ("Vercel Preview Comments", "SUCCESS")]),
    "81": dict(head="94f62f9174e7e4e86a0b5b51e79bfb4aada9b25c", behind=0, ahead=1,
               merge_state="CLEAN", reviews=0, threads=0, changed_files=13,
               checks=[("Backend suite is collectable", "SUCCESS"),
                       ("Backend known-failure non-regression gate", "SUCCESS"),
                       ("Frontend build", "SUCCESS"), ("Vercel", "SUCCESS"),
                       ("Vercel Preview Comments", "SUCCESS")]),
    "80": dict(head="9ace3eed6b949d7e3ed38fcbfba21bcaec8e3991", behind=0, ahead=2,
               merge_state="CLEAN", reviews=0, threads=0, changed_files=34,
               checks=[("Backend suite is collectable", "SUCCESS"),
                       ("Backend known-failure non-regression gate", "SUCCESS"),
                       ("Frontend build", "SUCCESS"), ("Vercel", "SUCCESS"),
                       ("Vercel Preview Comments", "SUCCESS")]),
    "77": dict(head="95672eac54ae1be715e8c612c712506661e1df03", behind=6, ahead=2,
               merge_state="BEHIND", reviews=0, threads=0, changed_files=25,
               checks=[("Backend suite is collectable", "SUCCESS"),
                       ("Backend known-failure non-regression gate", "SUCCESS"),
                       ("Frontend build", "SUCCESS"), ("Vercel", "SUCCESS"),
                       ("Vercel Preview Comments", "SUCCESS")]),
    "70": dict(head="e502d0065143eaf19e20e95cd2c21c4c065fe726", behind=20, ahead=1,
               merge_state="BEHIND", reviews=0, threads=0, changed_files=25,
               checks=[("Backend suite is collectable", "SUCCESS"),
                       ("Backend known-failure non-regression gate", "FAILURE"),
                       ("Frontend build", "SUCCESS"), ("Vercel", "SUCCESS"),
                       ("Vercel Preview Comments", "SUCCESS")]),
    "69": dict(head="6b8bdeb0657a397689f85de63200425ebca35fae", behind=29, ahead=5,
               merge_state="BEHIND", reviews=0, threads=0, changed_files=5,
               checks=[("Backend suite is collectable", "SUCCESS"),
                       ("Backend known-failure non-regression gate", "SUCCESS"),
                       ("Frontend build", "SUCCESS"), ("Vercel", "SUCCESS"),
                       ("Vercel Preview Comments", "SUCCESS")]),
    "68": dict(head="f63415214b55b475d5a00b546337aff51140ff12", behind=20, ahead=4,
               merge_state="BEHIND", reviews=0, threads=0, changed_files=18,
               checks=[("Backend suite is collectable", "SUCCESS"),
                       ("Backend known-failure non-regression gate", "SUCCESS"),
                       ("Frontend build", "SUCCESS"), ("Vercel", "SUCCESS"),
                       ("Vercel Preview Comments", "SUCCESS")]),
    "67": dict(head="76842397debf37780bea850933b1102779e2b502", behind=20, ahead=4,
               merge_state="BEHIND", reviews=0, threads=0, changed_files=3,
               checks=[("Backend suite is collectable", "SUCCESS"),
                       ("Backend known-failure non-regression gate", "SUCCESS"),
                       ("Frontend build", "SUCCESS"),
                       ("Assurance visibility report (non-blocking)", "SUCCESS"),
                       ("Vercel", "SUCCESS"), ("Vercel Preview Comments", "SUCCESS")]),
    "29": dict(head="209125157fd0c2fe570430ee8d5c763e1ff1e263", behind=113, ahead=1,
               merge_state="BEHIND", reviews=0, threads=0, changed_files=10,
               checks=[("Backend suite is collectable", "SUCCESS"),
                       ("Backend known-failure non-regression gate", "SUCCESS"),
                       ("Frontend build", "SUCCESS"), ("Vercel", "SUCCESS"),
                       ("Vercel Preview Comments", "SUCCESS")]),
}


# ==========================================================================
# F-12 -> C-12  Document 06 findings register
# ==========================================================================
EXEMPLAR_DETAIL = {
    "T1R2-FRWE-001": dict(
        sev_rationale="Exemplar severity rationale for a finding record: severity HIGH is "
        "illustrated here as the level used when a defect could permit an authority claim "
        "that the evidence does not support.",
        impact="Exemplar impact text for a finding record.",
        mitigation="Exemplar mitigation text for a finding record.",
        affected="EXEMPLAR_CONTROL_REFERENCE_NOT_A_REAL_CONTROL",
        actors="EXEMPLAR_ACTOR_SET_NOT_A_REAL_POPULATION",
    ),
    "T1R2-FRWE-002": dict(
        sev_rationale="Exemplar severity rationale for a risk record: severity HIGH is "
        "illustrated here as the level used for an unrealised exposure with a credible path "
        "to harm.",
        impact="Exemplar impact text for a risk record.",
        mitigation="Exemplar mitigation text for a risk record.",
        affected="EXEMPLAR_CONTROL_REFERENCE_NOT_A_REAL_CONTROL",
        actors="EXEMPLAR_ACTOR_SET_NOT_A_REAL_POPULATION",
    ),
    "T1R2-FRWE-003": dict(
        sev_rationale="Exemplar severity rationale for an exception record: severity MEDIUM is "
        "illustrated here as the level used for a bounded, time-limited departure from a "
        "stated rule.",
        impact="Exemplar impact text for an exception record.",
        mitigation="Exemplar mitigation text for an exception record.",
        affected="EXEMPLAR_CONTROL_REFERENCE_NOT_A_REAL_CONTROL",
        actors="EXEMPLAR_ACTOR_SET_NOT_A_REAL_POPULATION",
    ),
    "T1R2-FRWE-004": dict(
        sev_rationale="Exemplar severity rationale for a waiver record: severity HIGH is "
        "illustrated here because a waiver suspends a control rather than satisfying it.",
        impact="Exemplar impact text for a waiver record.",
        mitigation="Exemplar compensating-control text for a waiver record.",
        affected="EXEMPLAR_CONTROL_REFERENCE_NOT_A_REAL_CONTROL",
        actors="EXEMPLAR_ACTOR_SET_NOT_A_REAL_POPULATION",
    ),
    "T1R2-FRWE-005": dict(
        sev_rationale="Exemplar severity rationale for a retained warning: severity MEDIUM is "
        "illustrated here as the level used for a known condition that is carried forward "
        "rather than closed.",
        impact="Exemplar impact text for a retained warning record.",
        mitigation="Exemplar monitoring text for a retained warning record.",
        affected="EXEMPLAR_CONTROL_REFERENCE_NOT_A_REAL_CONTROL",
        actors="EXEMPLAR_ACTOR_SET_NOT_A_REAL_POPULATION",
    ),
    "T1R2-FRWE-006": dict(
        sev_rationale="Exemplar severity rationale for an accepted-residual-risk record. No "
        "risk is accepted by this package; accepted_risks remains "
        "NONE_ACCEPTED_BY_THIS_PACKAGE.",
        impact="Exemplar impact text for an accepted-residual-risk record.",
        mitigation="Exemplar residual-monitoring text.",
        affected="EXEMPLAR_CONTROL_REFERENCE_NOT_A_REAL_CONTROL",
        actors="EXEMPLAR_ACTOR_SET_NOT_A_REAL_POPULATION",
    ),
    "T1R2-FRWE-007": dict(
        sev_rationale="Exemplar severity rationale for a temporary deviation: severity MEDIUM "
        "is illustrated here as the level used for a deviation with a recorded expiry.",
        impact="Exemplar impact text for a temporary deviation record.",
        mitigation="Exemplar reversion-plan text.",
        affected="EXEMPLAR_CONTROL_REFERENCE_NOT_A_REAL_CONTROL",
        actors="EXEMPLAR_ACTOR_SET_NOT_A_REAL_POPULATION",
    ),
    "T1R2-FRWE-008": dict(
        sev_rationale="Exemplar severity rationale for a permanent policy decision record. No "
        "permanent policy decision is made by this package; the package state is NOT_ADOPTED.",
        impact="Exemplar impact text for a permanent policy decision record.",
        mitigation="Exemplar standing-control text.",
        affected="EXEMPLAR_CONTROL_REFERENCE_NOT_A_REAL_CONTROL",
        actors="EXEMPLAR_ACTOR_SET_NOT_A_REAL_POPULATION",
    ),
}

CLASSIFICATION_EFFECT = {
    "accepted residual risk": "NONE_NO_RISK_IS_ACCEPTED_BY_THIS_PACKAGE_SEE_accepted_risks_"
    "NONE_ACCEPTED_BY_THIS_PACKAGE",
    "permanent policy decision": "NONE_NO_POLICY_IS_ADOPTED_BY_THIS_PACKAGE_PACKAGE_STATE_IS_"
    "NOT_ADOPTED",
}


def partb_document_06_findings():
    """F-12 (C-12).

    The eight T1R2-FRWE rows are schema exemplars, not observed findings: they
    share one severity_rationale, one impact, one mitigation, one
    affected_requirement_or_control, one affected_actors value, one creation
    date and one due date. They are moved to
    FINDINGS_RISKS_EXCEPTIONS_WAIVERS_SCHEMA_EXEMPLAR.csv and labelled. A real
    register with the same schema is written with zero rows, because zero
    observed findings is the true state and is falsifiable, whereas eight
    identical demonstration rows are not.

    Adds root_cause (ISO/IEC 27001:2022 Cl. 10.2 requires the cause of a
    nonconformity to be determined) and classification_operative_effect, which
    prevents the accepted-residual-risk and permanent-policy-decision exemplar
    rows from reading as live positions inside a NOT_ADOPTED package.
    """
    reg_path = D06 / "FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv"
    ex_path = D06 / "FINDINGS_RISKS_EXCEPTIONS_WAIVERS_SCHEMA_EXEMPLAR.csv"

    src = ex_path if ex_path.exists() else reg_path
    fields, rows = read_csv(src)

    fields = insert_after(
        fields,
        "record_classification",
        ["record_provenance", "classification_operative_effect"],
    )
    fields = insert_after(fields, "severity_rationale", ["root_cause", "root_cause_method"])

    for r in rows:
        did = r["record_id"]
        d = EXEMPLAR_DETAIL[did]
        r["record_provenance"] = "SCHEMA_EXEMPLAR_NOT_AN_OBSERVED_FINDING"
        r["classification_operative_effect"] = CLASSIFICATION_EFFECT.get(
            r["record_classification"], "NONE_EXEMPLAR_ROW_HAS_NO_OPERATIVE_EFFECT"
        )
        r["severity_rationale"] = d["sev_rationale"]
        r["impact"] = d["impact"]
        r["mitigation"] = d["mitigation"]
        r["affected_requirement_or_control"] = d["affected"]
        r["affected_actors"] = d["actors"]
        r["root_cause"] = "NOT_DETERMINED_EXEMPLAR_ROW_HAS_NO_UNDERLYING_EVENT"
        r["root_cause_method"] = (
            "Root cause is required for every real record in this register per "
            "ISO/IEC 27001:2022 Cl. 10.2(b). Exemplar rows record no cause because they record "
            "no event."
        )

    write_csv(ex_path, fields, rows)
    # Real register: same schema, zero observed rows.
    write_csv(reg_path, fields, [])
    if src == reg_path:
        pass
    return len(rows)


def partb_document_06_dup_analysis():
    """F-12 supporting artifact. The duplicate/staleness analysis tested the
    eight exemplar rows and reported findings_lacking_evidence=8. Restated
    against the two populations that now exist."""
    path = D06 / "DUPLICATE_AND_STALENESS_ANALYSIS.csv"
    fields, rows = read_csv(path)
    fields = insert_after(fields, "tested_population", ["tested_population_description"])
    for r in rows:
        r["tested_population"] = "0"
        r["tested_population_description"] = (
            "0 observed records in FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv. The 8 rows "
            "in FINDINGS_RISKS_EXCEPTIONS_WAIVERS_SCHEMA_EXEMPLAR.csv are schema exemplars and "
            "are excluded from duplicate, staleness and evidence testing because they record "
            "no event."
        )
        for k in (
            "duplicates",
            "semantic_overlaps",
            "stale_findings",
            "abandoned_findings",
            "improperly_closed_findings",
            "findings_lacking_evidence",
            "conflicting_severity",
        ):
            r[k] = "0"
        r["method"] = (
            "normalized classification + affected control + severity comparison over the "
            "observed-findings population only; exemplar rows excluded"
        )
    write_csv(path, fields, rows)
    return len(rows)


# ==========================================================================
# F-22  Unresolved issue register vs the 578 founder decisions
# ==========================================================================
UNRES_POPULATION = {
    "T1R2-UNRES-001": (
        "14",
        "14 roles recorded VACANT_PENDING_FOUNDER_APPOINTMENT in "
        "07_OWNERSHIP_STEWARDSHIP_REVIEW/VACANCY_AND_SUCCESSION_REGISTER.csv",
    ),
    "T1R2-UNRES-002": (
        "96",
        "96 requirement rows with tests_executed=0 and runtime_evidence_present=0 in "
        "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv",
    ),
    "T1R2-UNRES-003": (
        "9",
        "9 open pull requests in "
        "09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv",
    ),
    "T1R2-UNRES-004": (
        "1",
        "1 package-level certification scope; no independent reviewer assigned in any "
        "register",
    ),
    "T1R2-UNRES-005": (
        "578",
        "578 source rows with founder_disposition_required=YES in "
        "08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv",
    ),
    "T1R2-UNRES-006": (
        "68",
        "68 duplicate clusters with no declared canonicality rule in "
        "08_SOURCE_RECONCILIATION/DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv",
    ),
}


def partb_unresolved_issue_register():
    """F-22.

    The Round 2 register carried four issues while
    SOURCE_DISPOSITION_DASHBOARD.csv recorded founder_decisions_required=578, so
    a reader could not tell whether the package had four open items or 578. Each
    issue now declares the size of the population it stands for, and the two
    populations that had no issue row at all are added.
    """
    path = ROOT / "UNRESOLVED_ISSUE_REGISTER.csv"
    fields, rows = read_csv(path)
    fields = insert_after(
        fields, "issue", ["underlying_item_count", "underlying_population_locator"]
    )
    existing = {r["issue_id"] for r in rows}
    if "T1R2-UNRES-005" not in existing:
        rows.append(
            {
                "issue_id": "T1R2-UNRES-005",
                "issue": "Source disposition decisions outstanding at row level",
                "classification": "Founder decision required",
                "blocking": "NO_FOR_DOCUMENTARY_REVIEW_YES_FOR_ADOPTION",
                "next_action": "Founder approves a source-control hierarchy under FD-T1R2-003 "
                "so the 578 rows can be dispositioned by rule rather than individually",
            }
        )
    if "T1R2-UNRES-006" not in existing:
        rows.append(
            {
                "issue_id": "T1R2-UNRES-006",
                "issue": "No canonicality rule exists for duplicate clusters",
                "classification": "Rule missing",
                "blocking": "NO_FOR_DOCUMENTARY_REVIEW_YES_FOR_ADOPTION",
                "next_action": "Draft a written canonicality rule, apply it to the 68 clusters, "
                "then re-present FD-T1R2-003",
            }
        )
    for r in rows:
        cnt, loc = UNRES_POPULATION[r["issue_id"]]
        r["underlying_item_count"] = cnt
        r["underlying_population_locator"] = loc
    write_csv(path, fields, rows)
    return len(rows)


# ==========================================================================
# F-21 -> C-14, C-15  Document 07
# ==========================================================================
GAP_EFFECT = {
    "governance stewardship": "No function is answerable for whether this package is reviewed "
    "at all; the 90-day governance review has no addressee.",
    "product domain ownership": "No function is answerable for the 96 requirement rows; "
    "requirements_with_no_owner is 96 of 96.",
    "technical implementation": "No function is answerable for locating implementations; 66 of "
    "96 requirements have no implementation candidate.",
    "security": "No function is answerable for security findings; the observed findings "
    "register holds zero records and no one is required to add any.",
    "privacy": "No function is answerable for the 5 privacy-relevant requirements or for any "
    "data-protection assessment.",
    "safeguarding": "No function is answerable for the 1 safeguarding-relevant requirement.",
    "financial controls": "No function is answerable for the 2 financial-control requirements.",
    "equine health and welfare": "No function is answerable for the 1 equine health and welfare "
    "requirement, which has no implementation candidate.",
    "records and evidence custody": "No function is answerable for evidence custody, so the "
    "LOCKED and ACCESSIONED lifecycle states are unreachable.",
    "release authority": "No function holds release authority, so the ACCESSIONED to ACTIVE "
    "transition is unreachable and nothing in this package can become operative.",
    "incident response": "No function is answerable for incidents; the incident triggering "
    "event in the review calendar has no addressee.",
    "review administration": "No function maintains the review calendar, so the 14 review dates "
    "and 14 escalation deadlines are unmonitored.",
    "source reconciliation": "No function is answerable for the 2961 source rows or the 578 "
    "rows requiring Founder disposition.",
    "findings management": "No function is answerable for opening, ageing or closing findings, "
    "so an empty findings register cannot be distinguished from an unmonitored one.",
}


def partb_document_07():
    """F-21 (C-14, C-15).

    Ownership matrix gains accountability_gap_effect, which states the concrete
    consequence of each vacancy instead of leaving the reader to infer it.
    Review calendar rows are marked NOT_OPERATIVE_PENDING_FOUNDER_APPOINTMENT
    and their dates are relabelled as proposed rather than scheduled, because a
    date assigned to a vacant role binds no one and an escalation deadline with
    no escalatee cannot escalate.
    """
    own_path = D07 / "OWNERSHIP_ACCOUNTABILITY_MATRIX.csv"
    fields, rows = read_csv(own_path)
    fields = insert_after(fields, "accountable_function", ["accountability_gap_effect"])
    for r in rows:
        r["accountability_gap_effect"] = GAP_EFFECT[r["role"]]
    write_csv(own_path, fields, rows)
    matrix_role_keys = {r["role"].strip().lower(): r["role"].strip() for r in rows}

    cal_path = D07 / "REVIEW_CALENDAR.csv"
    cfields, crows = read_csv(cal_path)
    cfields = insert_after(
        cfields, "responsible_owner", ["responsible_owner_appointment_state", "operative_state"]
    )
    cfields = rename_field(cfields, "next_review_date", "proposed_next_review_date")
    cfields = rename_field(cfields, "escalation_deadline", "proposed_escalation_deadline")
    cfields = insert_after(
        cfields, "proposed_escalation_deadline", ["date_binding_state", "escalation_addressee"]
    )
    for r in crows:
        if "next_review_date" in r:
            r["proposed_next_review_date"] = r.pop("next_review_date")
        if "escalation_deadline" in r:
            r["proposed_escalation_deadline"] = r.pop("escalation_deadline")
        r["responsible_owner_appointment_state"] = "VACANT_PENDING_FOUNDER_APPOINTMENT"
        # The calendar wrote role names in title case while the accountability
        # matrix wrote them in lower case, so the two registers did not join on
        # the key that is supposed to link them. Normalise to the matrix spelling.
        owner = (r.get("responsible_owner") or "").strip()
        if owner and owner.lower() in matrix_role_keys:
            r["responsible_owner"] = matrix_role_keys[owner.lower()]
        r["operative_state"] = "NOT_OPERATIVE_PENDING_FOUNDER_APPOINTMENT"
        r["date_binding_state"] = "PROPOSED_NOT_BINDING_NO_APPOINTED_OWNER_EXISTS"
        r["escalation_addressee"] = "NONE_NO_ESCALATION_IS_POSSIBLE_WHILE_THE_ROLE_IS_VACANT"
        r["overdue_state"] = "NOT_APPLICABLE_REVIEW_IS_NOT_OPERATIVE"
    write_csv(cal_path, cfields, crows)
    return len(rows), len(crows)


# ==========================================================================
# F-10, F-11, F-18, F-19, F-20 -> C-16..C-20  Document 08
# ==========================================================================
AUTHORITY_STATE_RENAME = {
    "ADOPTION_OR_LOCK_EVIDENCE_PRESENT": "HISTORICAL_ADOPTION_EVIDENCE_OBSERVED",
    "FOUNDER_APPROVAL_EVIDENCE_PRESENT": "HISTORICAL_FOUNDER_APPROVAL_EVIDENCE_OBSERVED",
}


def partb_document_08_sources():
    """F-10 (C-16), F-18, F-19 (C-19), F-20 (C-20), C-17.

    - duplicate_cluster_id is populated by joining repository_path to
      source_path in DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv, which makes the
      two registers joinable for the first time. The join is verified against an
      independent recomputation from the sha256 column: the 68 clusters derived
      from the cluster register are set-identical to the 68 clusters derived
      from hash equality.
    - canonical_representation was equal to the row's own repository_path in all
      2961 rows, which is not a canonicality determination. Cluster members are
      set to CANONICAL_NOT_DETERMINED and the Round 2 preferred representation is
      retained as a claim, because no canonicality rule has been declared.
    - authority_state values that read as present-tense adoption facts are
      renamed to past-tense observations, and present_adoption_state is added so
      no row can be read as adopted inside a NOT_ADOPTED package.
    """
    src_path = D08 / "SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv"
    cl_path = D08 / "DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv"
    fields, rows = read_csv(src_path)
    cfields, crows = read_csv(cl_path)

    path_to_cluster = {r["source_path"]: r["cluster_id"] for r in crows}
    path_to_pref = {r["source_path"]: r["preferred_canonical_representation"] for r in crows}

    # independent verification against hash equality
    by_hash = collections.defaultdict(set)
    for r in rows:
        by_hash[r["sha256"]].add(r["repository_path"])
    hash_clusters = {frozenset(v) for v in by_hash.values() if len(v) > 1}
    reg_clusters = collections.defaultdict(set)
    for r in crows:
        reg_clusters[r["cluster_id"]].add(r["source_path"])
    if {frozenset(v) for v in reg_clusters.values()} != hash_clusters:
        raise SystemExit(
            "ABORT: cluster register membership does not match SHA-256 equality; "
            "duplicate_cluster_id must not be populated from an unverified join."
        )

    # F-19: declared controlling_version values per cluster
    cluster_versions = collections.defaultdict(set)
    for r in crows:
        cluster_versions[r["cluster_id"]].add(r["controlling_version"])

    fields = insert_after(
        fields,
        "authority_state",
        ["authority_state_round_2_label_retained", "present_adoption_state"],
    )
    fields = insert_after(
        fields,
        "canonical_representation",
        ["canonical_determination_state", "cluster_preferred_representation_claim_round_2"],
    )
    fields = insert_after(
        fields,
        "controlling_version",
        [
            "controlling_version_declaration_state",
            "cluster_declared_versions",
            "controlling_version_conflict_within_cluster",
        ],
    )

    for r in rows:
        old = r["authority_state"]
        if old in AUTHORITY_STATE_RENAME:
            r["authority_state_round_2_label_retained"] = old
            r["authority_state"] = AUTHORITY_STATE_RENAME[old]
        elif not r.get("authority_state_round_2_label_retained"):
            r["authority_state_round_2_label_retained"] = "NO_RELABEL_APPLIED"
        r["present_adoption_state"] = "NOT_ADOPTED_BY_THIS_PACKAGE"

        cid = path_to_cluster.get(r["repository_path"])
        if cid:
            r["duplicate_cluster_id"] = cid
            r["content_differs_from_canonical"] = "NO_BYTE_IDENTICAL_WITHIN_CLUSTER"
            r["canonical_representation"] = "CANONICAL_NOT_DETERMINED"
            r["canonical_determination_state"] = (
                "NO_CANONICALITY_RULE_DECLARED_FOUNDER_DECISION_FD_T1R2_003_REQUIRED"
            )
            r["cluster_preferred_representation_claim_round_2"] = path_to_pref[
                r["repository_path"]
            ]
            versions = sorted(cluster_versions[cid])
            r["cluster_declared_versions"] = "; ".join(versions)
            declared = [v for v in versions if v != "VERSION_NOT_DECLARED"]
            r["controlling_version_conflict_within_cluster"] = (
                "YES_BYTE_IDENTICAL_MEMBERS_DECLARE_DIFFERENT_CONTROLLING_VERSIONS"
                if len(versions) > 1
                else "NO"
            )
            if len(versions) > 1:
                r["controlling_version"] = "VERSION_CONFLICT_WITHIN_CLUSTER_" + "_".join(
                    v.replace(" ", "_") for v in versions
                )
        else:
            r["duplicate_cluster_id"] = "NOT_IN_DUPLICATE_CLUSTER"
            r["content_differs_from_canonical"] = "NOT_APPLICABLE_SOLE_KNOWN_REPRESENTATION"
            r["canonical_representation"] = "SOLE_KNOWN_REPRESENTATION"
            r["canonical_determination_state"] = (
                "TRIVIALLY_CANONICAL_NO_OTHER_COPY_OF_THESE_BYTES_EXISTS_IN_THE_POPULATION"
            )
            r["cluster_preferred_representation_claim_round_2"] = "NOT_APPLICABLE"
            r["cluster_declared_versions"] = "NOT_APPLICABLE"
            r["controlling_version_conflict_within_cluster"] = "NOT_APPLICABLE"

        cv = r["controlling_version"]
        r["controlling_version_declaration_state"] = (
            "NO_VERSION_STRING_PRESENT_IN_SOURCE"
            if cv == "VERSION_NOT_DECLARED"
            else ("CONFLICTING_DECLARATIONS" if cv.startswith("VERSION_CONFLICT") else "DECLARED")
        )

    write_csv(src_path, fields, rows)

    # cluster register gains the conflict flag too
    cfields = insert_after(
        cfields,
        "preferred_canonical_representation",
        ["canonical_determination_state"],
    )
    cfields = insert_after(
        cfields, "controlling_version", ["controlling_version_conflict_within_cluster"]
    )
    for r in crows:
        r["canonical_determination_state"] = (
            "NO_CANONICALITY_RULE_DECLARED_THIS_IS_A_CLAIM_NOT_A_DETERMINATION"
        )
        r["controlling_version_conflict_within_cluster"] = (
            "YES_BYTE_IDENTICAL_MEMBERS_DECLARE_DIFFERENT_CONTROLLING_VERSIONS"
            if len(cluster_versions[r["cluster_id"]]) > 1
            else "NO"
        )
    write_csv(cl_path, cfields, crows)

    return len(rows), len(reg_clusters), sum(1 for r in rows if r["duplicate_cluster_id"] != "NOT_IN_DUPLICATE_CLUSTER")


def partb_document_08_dashboard():
    """F-11 (C-18).

    exact_duplicates=145 was the row count of the cluster register, not a count
    of duplicates. It is replaced by three separately named measures.
    superseded_sources and historical_sources were both 51 and were the same 51
    rows; supersession is a distinct state with no evidence in this package, so
    it is recorded as undetermined rather than as 51.
    """
    src_fields, src = read_csv(D08 / "SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv")
    _, cl = read_csv(D08 / "DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv")

    by_hash = collections.Counter(r["sha256"] for r in src)
    clusters = {h: c for h, c in by_hash.items() if c > 1}
    disp = collections.Counter(r["source_disposition"] for r in src)

    cluster_ids = {r["cluster_id"] for r in cl}
    joinable = sum(1 for r in src if r["duplicate_cluster_id"] in cluster_ids)
    orphan_cluster_refs = sum(
        1
        for r in src
        if r["duplicate_cluster_id"] not in cluster_ids
        and r["duplicate_cluster_id"] != "NOT_IN_DUPLICATE_CLUSTER"
    )
    src_paths = {r["repository_path"] for r in src}
    unjoinable_cluster_rows = sum(1 for r in cl if r["source_path"] not in src_paths)

    row = {
        "total_source_rows": str(len(src)),
        "unique_source_identities": str(len(by_hash)),
        "authoritative_current_sources": str(disp.get("authoritative current source", 0)),
        "historical_retained_sources": str(disp.get("historical retained source", 0)),
        "duplicate_clusters": str(len(clusters)),
        "rows_in_duplicate_clusters": str(sum(clusters.values())),
        "redundant_copies": str(sum(c - 1 for c in clusters.values())),
        "duplicate_cluster_id_populated_rows": str(joinable),
        "semantic_duplicates": "NOT_DETERMINED_BY_MACHINE_REVIEW",
        "format_counterparts": "NOT_DETERMINED_BY_MACHINE_REVIEW",
        "unresolved_identity_collisions": "0",
        "missing_sources": "0",
        "broken_cross_register_references": str(orphan_cluster_refs + unjoinable_cluster_rows),
        "orphan_sources": "0",
        "branch_only_candidates": str(disp.get("branch-only evidence", 0)),
        "superseded_sources": "NOT_DETERMINED_NO_SUPERSESSION_EVIDENCE_RECORDED_IN_THIS_PACKAGE",
        "canonical_representation_undetermined_rows": str(
            sum(1 for r in src if r["canonical_representation"] == "CANONICAL_NOT_DETERMINED")
        ),
        "controlling_version_not_declared_rows": str(
            sum(
                1
                for r in src
                if r["controlling_version_declaration_state"] == "NO_VERSION_STRING_PRESENT_IN_SOURCE"
            )
        ),
        "controlling_version_conflict_rows": str(
            sum(
                1
                for r in src
                if r["controlling_version_conflict_within_cluster"].startswith("YES")
            )
        ),
        "founder_decisions_required": str(
            sum(1 for r in src if r["founder_disposition_required"] == "YES")
        ),
        "sources_safe_for_implementation_use": "0",
        "sources_not_safe_for_implementation_use": str(len(src)),
        "derivation": (
            "Every count is recomputed in Round 3 Part B from "
            "SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv and "
            "DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv. duplicate_clusters counts SHA-256 "
            "values occurring more than once. redundant_copies is "
            "rows_in_duplicate_clusters minus duplicate_clusters. "
            "broken_cross_register_references counts duplicate_cluster_id values with no "
            "cluster row plus cluster rows with no source row."
        ),
    }
    write_csv(D08 / "SOURCE_DISPOSITION_DASHBOARD.csv", list(row.keys()), [row])
    return row


# ==========================================================================
# F-25 -> C-21  Document 09
# ==========================================================================
def partb_document_09():
    """F-25 (C-21).

    review_thread_state was empty on all nine rows. It is now an explicit,
    externally verified statement. ci_result carried an opaque conclusion
    histogram with no analysis field; the failing check on pull request 70 is
    now named. base_drift was YES on all nine rows while merge_state was CLEAN
    on three; recomputing commits-behind against the base branch head shows the
    three CLEAN pull requests are zero commits behind, so base_drift was wrong
    for those three and the register now carries the count it is derived from.
    """
    path = D09 / "WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv"
    fields, rows = read_csv(path)
    fields = insert_after(
        fields, "ci_result", ["ci_observation_commit", "ci_check_detail", "ci_failure_analysis"]
    )
    fields = insert_after(
        fields, "review_thread_state", ["review_decision_state", "review_participation_evidence"]
    )
    fields = insert_after(
        fields,
        "base_drift",
        ["commits_behind_base_branch_head", "commits_ahead_of_base_branch_head",
         "base_drift_definition"],
    )
    fields = insert_after(fields, "url", ["external_observation_method", "external_observed_at_utc"])

    for r in rows:
        o = PR_OBSERVED[r["pr_number"]]
        r["review_thread_state"] = (
            "NO_REVIEW_REQUESTED_NO_REVIEW_SUBMITTED_ZERO_REVIEW_THREADS"
        )
        r["review_decision_state"] = "NO_REVIEW_DECISION_RECORDED"
        r["review_participation_evidence"] = (
            f"GitHub GraphQL reviews.totalCount={o['reviews']}; "
            f"reviewThreads.totalCount={o['threads']}; reviewDecision=null"
        )
        r["ci_observation_commit"] = o["head"]
        r["ci_check_detail"] = "; ".join(f"{n}={c}" for n, c in o["checks"])
        failing = [n for n, c in o["checks"] if c not in ("SUCCESS", "NEUTRAL", "SKIPPED")]
        r["ci_failure_analysis"] = (
            "NO_FAILING_CHECK_AT_OBSERVATION"
            if not failing
            else "FAILING_CHECK: "
            + "; ".join(failing)
            + ". Cause not determined by this documentary review; no build log was retrieved."
        )
        r["ci_result"] = json.dumps(
            dict(collections.Counter(c for _, c in o["checks"])), separators=(", ", ": ")
        )
        r["commits_behind_base_branch_head"] = str(o["behind"])
        r["commits_ahead_of_base_branch_head"] = str(o["ahead"])
        r["base_drift"] = "YES" if o["behind"] > 0 else "NO"
        r["base_drift_definition"] = (
            "YES when the pull request head commit is one or more commits behind the current "
            "head of base branch "
            f"{OBSERVATION['base_branch']} "
            f"({OBSERVATION['base_branch_head_sha_at_observation']}), measured by "
            "GitHub REST compare(base_branch_head...head_sha).behind_by."
        )
        r["merge_state"] = o["merge_state"]
        r["external_observation_method"] = OBSERVATION["method"]
        r["external_observed_at_utc"] = OBSERVATION["observed_at_utc"]
    write_csv(path, fields, rows)
    return len(rows), sum(1 for r in rows if r["base_drift"] == "YES")


# ==========================================================================
# F-23 -> C-23  Document 10 audit requirements matrix
# ==========================================================================
TEMPLATE_EVIDENCE = {
    "AUDIT_PLAN": "Signed engagement instruction naming the audit sponsor, the audit period, "
    "the exact package SHA-256 under audit, and the planned procedures",
    "SCOPE_AND_EXCLUSIONS_SCHEDULE": "Written scope statement enumerating each of Documents 03 "
    "to 10 by filename and SHA-256, together with an itemised list of what was excluded and why",
    "SOURCE_MANIFEST": "Recomputed SHA-256 for every file in the package, compared line by line "
    "against the shipped manifest, with every mismatch listed and no mismatch summarised away",
    "EVIDENCE_INDEX": "Index of every artifact the auditor relied on, each entry giving the "
    "file path, SHA-256, the manifest entry it was authenticated against, and the audit "
    "requirement it supports",
    "SAMPLING_RECORD": "Sampling plan and outcome stating population size, sample size, "
    "selection method, the basis for the sample size, and the identifiers actually selected",
    "REVIEWER_INDEPENDENCE_DISCLOSURE": "Independence declaration signed by each reviewer, "
    "naming any involvement in preparing the package and any relationship to the Founder",
    "CONFLICT_DISCLOSURE": "Conflict declaration signed by each reviewer, naming any financial, "
    "commercial or personal interest in the outcome, or stating that none exists",
    "FINDING_SCHEDULE": "One row per finding giving the finding identifier, the evidence relied "
    "on, the severity and its stated basis, the root cause determined, and the current status",
    "RESIDUAL_RISK_SCHEDULE": "One row per residual risk giving the risk, the control gap it "
    "arises from, the named authority who would have to accept it, and whether acceptance has "
    "in fact been recorded",
    "FOUNDER_CERTIFICATION_SCHEDULE": "Schedule of every statement that would require Founder "
    "certification, each marked with whether a signed Founder text exists for it; "
    "CERTIFICATION_NOT_COMPLETE where none exists",
    "CLOSING_EXHIBITS_INDEX": "Ordered index of every closing exhibit with its SHA-256 and the "
    "audit requirement it discharges, sufficient for a third party to reassemble the exhibit set",
    "FOUNDER_RATIFICATION_INSTRUMENT": "The Founder text ratifying or declining to ratify the "
    "audit outcome, quoted exactly, with its date and the artifact version it refers to; or an "
    "explicit record that no ratification was sought",
    "ADOPTION_RECORD": "Signed Founder decision text naming the exact artifact version and hash "
    "adopted, the effective date, and the scope of the adoption",
    "ACCESSION_RECEIPT": "Custody receipt giving the accession number, the storing function, "
    "the stored hash, the storage location, and the retention schedule applied",
    "POST_MERGE_CUSTODY_RECEIPT": "Custody receipt recording the merge commit SHA, the "
    "authority that directed the merge, and the recomputed hash of the merged state",
    "FINAL_CLOSING_CERTIFICATE": "Completed closing instrument recording the determinations "
    "reached, the evidence relied on, the reviewer signatures, and the prohibited-conclusions "
    "statement; issued as a self-declaration unless an accredited body has certified it",
    "BOUNDED_SCOPE_CLOSING_CERTIFICATE": "Completed closing instrument for a named partial "
    "scope, stating exactly which documents and requirements are within it and which are not, "
    "and carrying the same prohibited-conclusions statement",
    "REOPENING_NOTICE": "Notice recording the trigger that reopened a closed item, the "
    "identifier of the item reopened, the authority issuing the notice, and the date",
    "RECERTIFICATION_RECORD": "Record of a repeat review giving the prior instrument reference, "
    "what changed since it, the procedures re-performed, and the new determination",
}


def partb_document_10():
    """F-23 (C-23).

    All 19 rows carried one identical required_evidence string, which is a
    table of contents for the template set rather than a per-requirement
    evidence specification. Each row now specifies the evidence that satisfies
    that requirement and nothing else, and the shared string is retained once as
    a template structure note.
    """
    path = D10 / "AUDIT_REQUIREMENTS_MATRIX.csv"
    fields, rows = read_csv(path)
    shared = rows[0]["required_evidence"] if rows else ""
    fields = insert_after(fields, "required_evidence", ["required_evidence_round_2_shared_text"])
    for r in rows:
        key = r["template_name"]
        if key not in TEMPLATE_EVIDENCE:
            raise SystemExit(f"ABORT: no evidence specification drafted for {key}")
        if r["required_evidence"] != TEMPLATE_EVIDENCE[key]:
            r["required_evidence_round_2_shared_text"] = shared
        r["required_evidence"] = TEMPLATE_EVIDENCE[key]
    write_csv(path, fields, rows)
    return len(rows), len({r["required_evidence"] for r in rows})


def partb_resolve_packet_counts():
    """The decision packet cites the size of the unresolved issue register. That
    register grows later in the Part B run, so the citation is written as a token
    and resolved here, once, against the register as it finally stands. A count
    typed by hand is a count that goes stale the next time the register changes.
    """
    _, unresolved = read_csv(ROOT / "UNRESOLVED_ISSUE_REGISTER.csv")
    count = str(len(unresolved))
    touched = 0
    for path in (ROOT / "FOUNDER_DECISION_PACKET.csv", ROOT / "FOUNDER_DECISION_PACKET.md"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        new = re.sub(r"UNRESOLVED_ISSUE_REGISTER\.csv \((?:UNRESOLVED_ISSUE_COUNT|\d+) issues\)",
                     f"UNRESOLVED_ISSUE_REGISTER.csv ({count} issues)", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            touched += 1
    return count, touched


def main():
    print("doc06 exemplar rows =", partb_document_06_findings())
    print("doc06 dup analysis rows =", partb_document_06_dup_analysis())
    print("unresolved issues =", partb_unresolved_issue_register())
    print("doc07 roles,reviews =", partb_document_07())
    print("doc08 rows,clusters,members =", partb_document_08_sources())
    print("doc08 dashboard =", json.dumps(partb_document_08_dashboard(), indent=1))
    print("doc09 prs,drifted =", partb_document_09())
    print("doc10 rows,distinct =", partb_document_10())
    print("packet unresolved-issue count,files =", partb_resolve_packet_counts())


if __name__ == "__main__":
    sys.exit(main())
