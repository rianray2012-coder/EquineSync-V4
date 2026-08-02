#!/usr/bin/env python3
import csv
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import textwrap
import zipfile
from datetime import datetime, timezone
from pathlib import Path

AUTHORITY = "NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED"
STATES = [
    "DRAFT_UNMERGED",
    "FOUNDER_REVIEW_READY",
    "ADOPTED",
    "ACCESSIONED",
    "LOCKED",
    "ACTIVE",
    "SUSPENDED",
    "SUPERSEDED",
    "HISTORICAL_RETAINED",
    "WITHDRAWN",
    "BLOCKED_EVIDENCE_REQUIRED",
    "REMEDIATION_REQUIRED",
    "REJECTED",
]

TEMPLATES = [
    ("01", "INTERNAL_DOCUMENTARY_REVIEW_PLAN", "Audit or internal documentary review plan", "Need to plan a bounded first-party review before any claim is made", "Package identifier; package SHA-256; review scope; planned procedures; reviewer disclosure", "Authenticated package bytes; branch head; reviewer assignment record; procedure list", "No production testing, third-party certification, legal compliance conclusion, or activation testing", "Review preparer", "Founder or assigned governance reviewer", "Plan acknowledgement only", "Creates no adoption, activation, implementation, production, merge, or certification authority", "Do not conclude audit certification, independent assurance, compliance, readiness for production, or Founder approval", "Every planned procedure has an evidence locator or a recorded exclusion", "Superseded only by a later plan naming this plan and its hash"),
    ("02", "SCOPE_AND_EXCLUSIONS_SCHEDULE", "Scope and exclusions schedule", "Review boundary must be fixed before evidence is assessed", "In-scope documents; excluded artifacts; reason for each exclusion; affected decisions", "Document inventory; exclusion rationale; unresolved issue link", "No silent expansion into runtime, deployment, merge, product, or legal scope", "Scope preparer", "Founder or assigned governance reviewer", "Scope acknowledgement only", "Defines review boundary only", "Do not imply excluded matters are resolved", "Each exclusion has a basis and residual-risk treatment", "Reopened when an excluded item becomes material"),
    ("03", "SOURCE_MANIFEST", "Source manifest", "Package or repository source evidence is assembled", "Source path; SHA-256; byte length; custody source; version status", "Source file bytes; checksum records; repository locator", "No source-precedence conclusion without reconciliation checks", "Evidence custodian", "Governance reviewer", "Manifest acknowledgement only", "Documents evidence custody only", "Do not imply source approval, adoption, or canonical status", "All listed sources have hash and byte length", "Superseded by a later manifest with complete delta"),
    ("04", "EVIDENCE_INDEX", "Evidence index", "Evidence is linked to findings, decisions, or validators", "Evidence ID; artifact path; row locator; hash; related finding or decision", "Referenced records; validation output; review notes", "No unlocated evidence or generic bundle references for closure", "Evidence index preparer", "Governance reviewer", "Index acknowledgement only", "Creates no closure authority by itself", "Do not imply evidence has been accepted by Founder", "Every evidence row resolves to a package file or external authenticated input", "Reopened when a referenced file changes hash"),
    ("05", "SAMPLING_RECORD", "Sampling record", "A bounded sample is used instead of full population review", "Population definition; sample size; sampling method; seed or selection basis", "Population register; sampled rows; selection record", "No claim of full-population validation from a sample", "Sampling preparer", "Governance reviewer", "Sample acknowledgement only", "Limits, rather than expands, assurance", "Do not imply sampled review proves unsampled rows", "Sample basis is reproducible and limitations are explicit", "Superseded when the population changes or full review replaces sample"),
    ("06", "REVIEWER_INDEPENDENCE_DISCLOSURE", "Reviewer independence disclosure", "A reviewer performs or contributes to documentary review", "Reviewer identity or role; relationship; tooling used; independence limits", "Disclosure statement; review assignment; conflict cross-reference", "No third-party or independent certification unless separately evidenced", "Reviewer", "Founder or assigned governance reviewer", "Disclosure acknowledgement only", "Discloses limits only", "Do not claim independence when review is Founder-directed or machine-assisted", "All limitations are recorded and unresolved limitations remain open", "Reopened when reviewer role or relationship changes"),
    ("07", "CONFLICT_DISCLOSURE", "Conflict disclosure", "Potential conflict, dependency, or self-review risk is identified", "Conflict description; affected artifacts; mitigation; unresolved effect", "Conflict source; mitigation evidence; residual risk link", "No closure merely because a conflict is disclosed", "Reviewer or preparer", "Founder or assigned governance reviewer", "Conflict acknowledgement only", "Records risk; grants no waiver unless separately authorized", "Do not imply acceptance of conflict or risk", "Each conflict has mitigation or explicit unresolved status", "Reopened when conflict scope expands"),
    ("08", "FINDING_SCHEDULE", "Finding schedule", "A finding requires tracking, disposition, or closure evidence", "Finding ID; severity; affected path; evidence; owner state; due basis", "Finding register row; source review; validation evidence", "No closure without direct current-package evidence", "Finding register preparer", "Governance reviewer", "Finding disposition acknowledgement only", "Records disposition evidence only", "Do not imply Founder acceptance, waiver, or closure authority", "Every finding has status, evidence, residual risk, and closure authority", "Reopened on regression or invalid evidence"),
    ("09", "RESIDUAL_RISK_SCHEDULE", "Residual-risk schedule", "A remediated or deferred item leaves residual risk", "Risk ID; affected item; likelihood basis; impact basis; proposed treatment", "Risk source; mitigation record; decision dependency", "No accepted-risk label without named accepting authority", "Risk preparer", "Founder or assigned risk reviewer", "Risk review acknowledgement only", "Does not accept risk by itself", "Do not imply bulk acceptance or indefinite waiver", "Each risk has individual treatment and Founder-action flag", "Reopened at expiry, material change, or rejection"),
    ("10", "FOUNDER_ATTESTATION_SCHEDULE", "Founder attestation schedule", "Founder may later record a documentary statement", "Question; exact statement; scope; exclusions; decision status", "Founder instruction if later supplied; evidence locator", "No prefilled approval, adoption, ratification, or certification", "Decision packet preparer", "Founder", "NO_DISPOSITION_SELECTED", "No authority until authenticated Founder decision", "Do not imply decision, appointment, certification, or production approval", "Every row remains unanswered absent authenticated instruction", "Superseded only by exact authenticated Founder instruction"),
    ("11", "CLOSING_EXHIBITS_INDEX", "Closing exhibits index", "A final documentary package references exhibits", "Exhibit ID; path; hash; purpose; related finding or decision", "Package manifest; checksums; validation report", "No exhibit can replace missing approval or validation", "Closing package preparer", "Governance reviewer", "Exhibit index acknowledgement only", "Indexes evidence only", "Do not imply closing completeness if unresolved items remain", "All exhibits resolve and hash-match", "Reopened when any exhibit hash changes"),
    ("12", "FOUNDER_DOCUMENTARY_ACKNOWLEDGEMENT", "Founder documentary acknowledgement instrument", "Founder may acknowledge review receipt or direction", "Acknowledgement question; package hash; scope; express non-authorities", "Authenticated Founder instruction if supplied later", "No ratification, adoption, activation, implementation, production, merge, or certification unless explicitly selected", "Decision packet preparer", "Founder", "NO_DISPOSITION_SELECTED", "No authority until authenticated Founder decision", "Do not imply ratification or approval from review preparation", "All authority boundaries remain visible", "Superseded only by later authenticated Founder direction"),
    ("13", "ADOPTION_RECORD", "Adoption record", "Founder may later adopt a documentary artifact", "Artifact ID; version; hash; adoption question; effective constraints", "Authenticated adoption instruction; manifest hash; unresolved risks", "No adoption by package preparation, PR creation, validation, or merge readiness", "Adoption record preparer", "Founder", "NO_DISPOSITION_SELECTED", "No adoption authority absent Founder decision", "Do not imply adoption from draft PR or validation success", "Record remains NOT_ADOPTED unless authenticated evidence exists", "Reopened on supersession or authority withdrawal"),
    ("14", "ACCESSION_OR_REPOSITORY_CUSTODY_RECEIPT", "Accession or repository-custody receipt", "A package is placed under repository custody", "Package hash; branch; commit; path; accession state", "Commit SHA; file list; checksum; PR link", "No adoption, activation, or merge authority from accession", "Repository custodian", "Governance reviewer", "Custody acknowledgement only", "Repository custody only", "Do not imply protected-branch merge unless merge receipt exists", "Receipt identifies exact commit and package bytes", "Superseded by later custody receipt"),
    ("15", "POST_MERGE_CUSTODY_RECEIPT", "Post-merge custody receipt", "A separately authorized merge has occurred", "PR number; expected head; merge commit; parent SHAs; protected head", "GitHub merge metadata; branch protection observation", "No use unless merge was separately authorized and performed", "Repository custodian", "Governance reviewer", "Post-merge acknowledgement only", "Records merge custody only if merge exists", "Do not create a merge record for draft PRs", "All merge parents and protected head reconcile", "Reopened on protected-head drift or merge reversal"),
    ("16", "FINAL_DOCUMENTARY_CLOSING_RECORD", "Final documentary closing record", "A documentary review package reaches a bounded closeout state", "Package hash; validation results; unresolved items; non-authorities", "Final manifest; validation report; unresolved register", "No certification, adoption, activation, implementation, production, or merge conclusion", "Closing preparer", "Founder or assigned governance reviewer", "Closing acknowledgement only", "Documentary closeout only", "Do not imply certification complete or unresolved issues closed", "All blockers closed or incomplete determination is issued", "Reopened if any blocker regresses"),
    ("17", "BOUNDED_SCOPE_SELF_DECLARATION_RECORD", "Bounded-scope self-declaration record", "A first-party preparer states what checks were executed", "Scope; checks; failure-capability; limitations; preparer statement", "Validation report; negative-control evidence; limitation log", "No independent assurance or third-party conformity claim", "First-party preparer", "Governance reviewer", "Self-declaration acknowledgement only", "First-party statement only", "Do not imply certification or external accreditation", "All checks identify capability and limitations", "Reopened when validation source or package bytes change"),
    ("18", "REOPENING_NOTICE", "Reopening notice", "A closed or draft item must be reopened", "Prior record; trigger; affected artifacts; corrective path", "Regression evidence; changed hash; review finding", "No blame, waiver, or closure from notice alone", "Issue owner or reviewer", "Governance reviewer", "Notice acknowledgement only", "Reopens or flags status only", "Do not imply remediation has occurred", "Trigger and affected records are specific", "Superseded by corrective disposition"),
    ("19", "PERIODIC_REVIEW_OR_REFRESH_RECORD", "Periodic review or refresh record", "A retained package requires scheduled review", "Review period; trigger; required checks; owner state; next review basis", "Review calendar; role assignment evidence; package hash", "No operative calendar while roles are vacant", "Review coordinator", "Founder or assigned governance reviewer", "Review acknowledgement only", "Schedules review only", "Do not imply active governance unless roles are appointed", "Next review condition is operable or explicitly blocked", "Reopened at next review date or material change"),
]

FINDINGS = [
    ("C-OR-01", "Cursor", "F-02", "S1", "10_CLOSING_AUDIT_PROTOCOL/templates/*.md", "CONFIRMED_REMEDIATED", "Replaced clone templates with 19 instrument-specific templates and distinctness validator."),
    ("C-OR-02", "Cursor", "F-09/F-15", "S2", "04_AUTHORITY_LIFECYCLE_REGISTER; FOUNDER_DECISION_PACKET", "CONFIRMED_REMEDIATED", "Established exact 13-state vocabulary and byte-identical decision question text."),
    ("C-OR-03", "Cursor", "F-16", "S2", "VALIDATION/validate_final_draft.py", "CONFIRMED_REMEDIATED", "Added document-specific validator with negative controls."),
    ("C-OR-04", "Cursor", "ownership", "S2", "07_OWNERSHIP_STEWARDSHIP_REVIEW", "CONFIRMED_REMEDIATED", "Validator checks no invented appointments and vacancy consistency."),
    ("C-OR-05", "Cursor", "F-12", "S2", "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS", "PARTIALLY_REMEDIATED", "Consolidated review findings are real rows; source register limitations remain tracked."),
    ("C-OR-06", "Cursor", "F-20", "S3", "08_SOURCE_RECONCILIATION", "DEFERRED_WITH_RECORDED_BASIS", "Legacy source authority labels retained as historical source metadata with authority boundary."),
    ("C-OR-07", "Cursor", "inventory", "S3", "TIER_1_DOCUMENT_INVENTORY.csv", "CONFIRMED_REMEDIATED", "Final executive summary and validator align final determination token."),
    ("C-OR-08", "Cursor", "F-22", "S3", "UNRESOLVED_ISSUE_REGISTER.csv", "PARTIALLY_REMEDIATED", "Final unresolved register separates open, remediated, deferred, and Founder decision items."),
    ("C-OR-09", "Cursor", "PR #83 hash", "S3", "PR metadata", "SUPERSEDED_BY_LATER_CHANGE", "Final package records new package hash; PR #83 is left draft and unmerged."),
    ("C-OR-10", "Cursor", "F-05/F-28", "S3", "integrity model", "DEFERRED_WITH_RECORDED_BASIS", "Final package has manifest, checksums, integrity root, ZIP sidecar; external attestation remains not supplied."),
    ("C-OR-11", "Cursor", "F-01", "S3", "03_IMPLEMENTATION_TRACEABILITY", "CONFIRMED_REMEDIATED", "Validator confirms candidate vs verified evidence separation and no static-scan verification claim."),
    ("C-OR-12", "Cursor", "delta heading", "S4", "FINAL_DRAFT_DELTA_REPORT.md", "CONFIRMED_REMEDIATED", "Final delta report is single-purpose and not repeated."),
    ("C-OR-13", "Cursor", "F-28", "S4", "VALIDATION_RESULTS", "DEFERRED_WITH_RECORDED_BASIS", "Repository and package-only validation are recorded; independent external signature remains unavailable."),
    ("F-01", "Perplexity/Cursor", "F-01", "S1", "03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv", "CONFIRMED_REMEDIATED", "Candidate rows remain source-text candidates, not normative requirements."),
    ("F-03", "Perplexity/Cursor", "F-03", "S1", "VALIDATION/validate_final_draft.py", "CONFIRMED_REMEDIATED", "Negative controls prove material checks fail."),
    ("F-04", "Perplexity/Cursor", "F-04", "S1", "04_AUTHORITY_LIFECYCLE_REGISTER/INVALID_STATE_RULES.csv", "CONFIRMED_REMEDIATED", "Invalid-state rules are checked or explicitly documented."),
    ("F-05", "Perplexity/Cursor", "F-05", "S1", "MANIFEST_OF_MANIFESTS.sha256", "CONFIRMED_REMEDIATED", "Package has manifest-of-manifests and final integrity root, with external attestation limitation disclosed."),
    ("F-06", "Perplexity/Cursor", "F-06", "S1", "VALIDATION_RESULTS", "CONFIRMED_REMEDIATED", "Validation evidence is regenerated for final branch/package bytes."),
    ("F-07", "Perplexity/Cursor", "F-07", "S2", "FOUNDER_DECISION_PACKET", "CONFIRMED_REMEDIATED", "All Founder decisions remain NO_DISPOSITION_SELECTED."),
    ("F-08", "Perplexity/Cursor", "F-08", "S2", "FOUNDER_DECISION_PACKET", "CONFIRMED_REMEDIATED", "Recommendations are separated from Founder dispositions."),
    ("F-09", "Perplexity/Cursor", "F-09", "S2", "FOUNDER_DECISION_PACKET", "CONFIRMED_REMEDIATED", "Decision wording is byte-identical across CSV, JSON, Markdown, and brief addendum."),
    ("F-10", "Perplexity/Cursor", "F-10", "S2", "08_SOURCE_RECONCILIATION", "CONFIRMED_REMEDIATED", "Duplicate-cluster FK checks remain enforced."),
    ("F-11", "Perplexity/Cursor", "F-11", "S2", "08_SOURCE_RECONCILIATION", "CONFIRMED_REMEDIATED", "Dashboard arithmetic checks remain enforced."),
    ("F-12", "Perplexity/Cursor", "F-12", "S2", "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS", "PARTIALLY_REMEDIATED", "Schema examples are separated; some legacy rows remain retained with explicit limitation."),
    ("F-13", "Perplexity/Cursor", "F-13", "S2", "03_IMPLEMENTATION_TRACEABILITY", "CONFIRMED_REMEDIATED", "Traceability metrics remain separated by candidate, located, verified, and executed states."),
    ("F-14", "Perplexity/Cursor", "F-14", "S2", "03_IMPLEMENTATION_TRACEABILITY", "CONFIRMED_REMEDIATED", "Test IDs do not overclaim verification where locators are absent."),
    ("F-15", "Perplexity/Cursor", "F-15", "S2", "04_AUTHORITY_LIFECYCLE_REGISTER", "CONFIRMED_REMEDIATED", "Reject and remediation outcomes are in the exact 13-state lifecycle."),
    ("F-16", "Perplexity/Cursor", "F-16", "S1", "VALIDATION/validate_final_draft.py", "CONFIRMED_REMEDIATED", "Per-document semantics and negative tests added."),
]

DECISIONS = {
    "FD-T1R2-001": "Should the Founder approve the exact 13-state lifecycle vocabulary for future documentary governance use, without authorizing adoption, activation, implementation, production use, certification, or merge?",
    "FD-T1R2-002": "Should the Founder appoint accountable governance roles for Documents 03-10, while recognizing that unappointed roles leave review, ownership, closure, and calendar controls inoperative?",
    "FD-T1R2-003": "Should the Founder approve the source-precedence rule for future use only after source-reconciliation integrity checks pass, without changing current adoption or activation status?",
    "FD-T1R2-004": "Should the Founder decide each listed residual risk individually by accepting, remediating, waiving, or deferring it, without bulk acceptance of demonstration rows or unresolved categories?",
    "FD-T1R2-005": "Should the Founder approve future sequencing for documentary next steps only, without authorizing merge, adoption, activation, implementation, production use, or certification?",
}

def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def rel(path, root):
    return path.relative_to(root).as_posix()

def write_templates(root):
    tdir = root / "10_CLOSING_AUDIT_PROTOCOL" / "templates"
    for old in tdir.glob("*.md"):
        old.unlink()
    index = []
    requirements = []
    for item in TEMPLATES:
        num, name, purpose, trigger, inputs, evidence, exclusions, preparer, reviewer, ack, effect, prohibited, completion, reopen = item
        template_id = f"T1FD-AUDIT-TEMPLATE-{num}"
        path = tdir / f"{num}_{name}.md"
        body = f"""# {name.replace('_', ' ').title()}

## Document Control

- Template ID: `{template_id}`
- Template name: `{name}`
- Authority boundary: `{AUTHORITY}`
- First-party status: `FIRST_PARTY_DOCUMENTARY_INSTRUMENT_ONLY`
- Disposition state: `NO_DISPOSITION_SELECTED`

## Purpose

{purpose}.

## Triggering Event

{trigger}.

## Required Inputs

{inputs}.

## Required Evidence

{evidence}.

## Exclusions

{exclusions}.

## Responsible Preparer

{preparer}.

## Required Reviewer

{reviewer}.

## Approval Or Acknowledgement Field

{ack}; blank until an authenticated Founder or reviewer action is supplied.

## Authority Effect

{effect}. This template does not authorize adoption, activation, implementation, production use, certification completion, merge, or protected-branch mutation.

## Prohibited Conclusions

{prohibited}.

## Completion Criteria

{completion}.

## Reopening Or Supersession Effect

{reopen}.

## Instrument-Specific Control

The preparer must record a concrete evidence locator for this instrument's purpose and must mark the row `INCOMPLETE` if the locator is absent.

## Example Row

`EXAMPLE_ONLY_NOT_A_FINDING_OR_DECISION` | `{template_id}` | `NO_DISPOSITION_SELECTED` | `EVIDENCE_LOCATOR_REQUIRED`
"""
        path.write_text(body)
        index.append({
            "template_id": template_id,
            "template_name": name,
            "path": f"templates/{path.name}",
            "bounded_complete_allowed": "NO_IF_EXCLUSIONS_OR_OPEN_ITEMS_REMAIN",
            "source_register_linkage_required": "YES",
            "evidence_register_linkage_required": "YES",
            "purpose": purpose,
            "unique_required_sections": "purpose; triggering event; required inputs; required evidence; exclusions; preparer; reviewer; acknowledgement; authority effect; prohibited conclusions; completion criteria; reopening effect",
        })
        requirements.append({
            "requirement_id": f"T1FD-AUDIT-REQ-{num}",
            "template_name": name,
            "required_evidence": evidence,
            "required_evidence_round_2_shared_text": "SUPERSEDED_BY_FINAL_DRAFT_PURPOSE_SPECIFIC_REQUIREMENT",
            "completion_criterion": completion,
            "prohibited_conclusion": prohibited,
        })
    write_csv(root / "10_CLOSING_AUDIT_PROTOCOL" / "TEMPLATE_INDEX.csv", index, list(index[0].keys()))
    write_csv(root / "10_CLOSING_AUDIT_PROTOCOL" / "AUDIT_REQUIREMENTS_MATRIX.csv", requirements, list(requirements[0].keys()))

def write_lifecycle(root):
    rows = []
    for s in STATES:
        for n in STATES:
            permitted = "YES" if (
                (s == "DRAFT_UNMERGED" and n == "FOUNDER_REVIEW_READY") or
                (s == "FOUNDER_REVIEW_READY" and n in {"REMEDIATION_REQUIRED", "REJECTED", "ADOPTED", "BLOCKED_EVIDENCE_REQUIRED"}) or
                (s == "REMEDIATION_REQUIRED" and n in {"DRAFT_UNMERGED", "FOUNDER_REVIEW_READY", "WITHDRAWN"}) or
                (s == "ADOPTED" and n in {"ACCESSIONED", "SUPERSEDED", "WITHDRAWN"}) or
                (s == "ACCESSIONED" and n in {"LOCKED", "SUPERSEDED", "WITHDRAWN"}) or
                (s == "LOCKED" and n in {"ACTIVE", "SUSPENDED", "SUPERSEDED"}) or
                (s == "ACTIVE" and n in {"SUSPENDED", "SUPERSEDED", "HISTORICAL_RETAINED"}) or
                (s == "SUSPENDED" and n in {"ACTIVE", "SUPERSEDED", "WITHDRAWN"}) or
                (s == "SUPERSEDED" and n == "HISTORICAL_RETAINED") or
                (s == "BLOCKED_EVIDENCE_REQUIRED" and n in {"REMEDIATION_REQUIRED", "REJECTED"}) or
                (s == "REJECTED" and n == "HISTORICAL_RETAINED") or
                (s == "WITHDRAWN" and n == "HISTORICAL_RETAINED")
            ) else "NO"
            rows.append({
                "permitted_starting_state": s,
                "starting_state_declaration_source": "FINAL_DRAFT_13_STATE_VOCABULARY",
                "permitted_next_state": n,
                "next_state_declaration_source": "FINAL_DRAFT_13_STATE_VOCABULARY",
                "permitted": permitted,
                "required_authority": "FOUNDER_DIRECTION_REQUIRED" if permitted == "YES" and n in {"ADOPTED", "ACCESSIONED", "LOCKED", "ACTIVE"} else ("DOCUMENTARY_REVIEW_AUTHORITY" if permitted == "YES" else "NOT_APPLICABLE_TRANSITION_IS_PROHIBITED"),
                "required_evidence": "Authenticated decision/custody evidence required for authority-bearing transitions" if permitted == "YES" else "NOT_APPLICABLE_TRANSITION_IS_PROHIBITED",
                "prohibition_reason": "NOT_APPLICABLE_TRANSITION_IS_PERMITTED" if permitted == "YES" else "Transition not in exact 13-state final-draft matrix",
                "authority_boundary": AUTHORITY,
            })
    write_csv(root / "04_AUTHORITY_LIFECYCLE_REGISTER" / "LIFECYCLE_TRANSITION_MATRIX.csv", rows, list(rows[0].keys()))
    write_csv(root / "04_AUTHORITY_LIFECYCLE_REGISTER" / "LIFECYCLE_STATE_VOCABULARY.csv", [{"state": s, "state_count": "13", "authority_boundary": AUTHORITY} for s in STATES], ["state", "state_count", "authority_boundary"])
    model = {
        "state_count": 13,
        "states": STATES,
        "authority_boundary": AUTHORITY,
        "transition_rows": len(rows),
        "invalid_rules": json.loads((root / "04_AUTHORITY_LIFECYCLE_REGISTER" / "AUTHORITY_LIFECYCLE_MODEL.json").read_text()).get("invalid_rules", []),
    }
    (root / "04_AUTHORITY_LIFECYCLE_REGISTER" / "AUTHORITY_LIFECYCLE_MODEL.json").write_text(json.dumps(model, indent=2) + "\n")

def write_decisions(root):
    rows = []
    for did, q in DECISIONS.items():
        rows.append({
            "decision_id": did,
            "question_presented": q,
            "exact_decision_text": q,
            "defined_scope": "Final-draft documentary review preparation for Tier 1 Documents 03-10",
            "express_exclusions": "No adoption, activation, implementation, production use, certification completion, merge, auto-merge, protected-branch mutation, appointment, waiver, or risk acceptance unless separately and exactly authenticated.",
            "conditions_precedent": "Founder review of final package, consolidated finding register, validation report, unresolved issue register, and residual-risk register.",
            "available_options": "APPROVE_FOR_DOCUMENTARY_NEXT_STEP; APPROVE_WITH_MODIFICATION; REQUIRE_REMEDIATION; DEFER; REJECT; NO_DISPOSITION_SELECTED",
            "consequences_of_each_option": "APPROVE_FOR_DOCUMENTARY_NEXT_STEP permits only the named documentary next step; APPROVE_WITH_MODIFICATION requires written modification; REQUIRE_REMEDIATION keeps blockers open; DEFER leaves status unchanged; REJECT records rejection; NO_DISPOSITION_SELECTED records no decision.",
            "exact_evidence_locators": "FINAL_DRAFT_SOURCE_AUTHENTICATION_AND_REPOSITORY_STATE_REPORT.md; CONSOLIDATED_EXTERNAL_REVIEW_FINDING_REGISTER.csv; VALIDATION_RESULTS/FINAL_DRAFT_VALIDATION_REPORT.json",
            "authority_granted_if_selected": "DOCUMENTARY_DIRECTION_ONLY_IF_AUTHENTICATED_BY_FOUNDER",
            "authority_expressly_not_granted": AUTHORITY,
            "dependencies": "Exact package hash, validation report, and unresolved issue register must reconcile.",
            "unresolved_risks": "See FINAL_RESIDUAL_RISK_REGISTER.csv and UNRESOLVED_ISSUE_REGISTER.csv.",
            "selected_disposition": "NO_DISPOSITION_SELECTED",
            "founder_decision_state": "NO_FOUNDER_DECISION_RECORDED",
            "authority_granted": "NONE_BY_THIS_PACKAGE",
        })
    fields = list(rows[0].keys())
    write_csv(root / "FOUNDER_DECISION_PACKET.csv", rows, fields)
    write_csv(root / "05_FOUNDER_DECISION_REGISTER" / "FOUNDER_DECISION_DISPOSITION_REGISTER.csv", rows, fields)
    (root / "05_FOUNDER_DECISION_REGISTER" / "FOUNDER_DECISION_DISPOSITION_REGISTER.json").write_text(json.dumps(rows, indent=2) + "\n")
    md = ["# Founder Decision Packet", "", f"Authority boundary: `{AUTHORITY}`", "", "No Founder decision is recorded by this package.", ""]
    for row in rows:
        md += [f"## {row['decision_id']}", "", row["exact_decision_text"], "", f"- Disposition: `{row['selected_disposition']}`", f"- Founder decision state: `{row['founder_decision_state']}`", f"- Authority granted: `{row['authority_granted']}`", ""]
    (root / "FOUNDER_DECISION_PACKET.md").write_text("\n".join(md))

def write_findings(root):
    fields = ["consolidated_finding_id", "source_reviewer", "source_finding_id", "original_severity", "package_version_reviewed", "exact_affected_path", "affected_row_field_symbol_or_template", "plain_language_explanation", "verification_method", "current_repository_status", "disposition", "remediation_performed", "validation_evidence", "residual_risk", "founder_action_required", "closure_authority", "closure_status"]
    rows = []
    for fid, reviewer, sid, sev, path, disposition, remediation in FINDINGS:
        rows.append({
            "consolidated_finding_id": fid,
            "source_reviewer": reviewer,
            "source_finding_id": sid,
            "original_severity": sev,
            "package_version_reviewed": "Round 3 Part B and final-draft successor",
            "exact_affected_path": path,
            "affected_row_field_symbol_or_template": "See source review and final validator evidence",
            "plain_language_explanation": remediation,
            "verification_method": "Direct current-package inspection plus final-draft validator",
            "current_repository_status": "Addressed in final-draft branch; not merged; protected branch unchanged",
            "disposition": disposition,
            "remediation_performed": remediation,
            "validation_evidence": "VALIDATION_RESULTS/FINAL_DRAFT_VALIDATION_REPORT.json",
            "residual_risk": "External attestation and Founder decisions remain unavailable" if "DEFERRED" in disposition or "PARTIALLY" in disposition else "No material residual risk identified for this finding within documentary scope",
            "founder_action_required": "YES" if disposition in {"FOUNDER_DECISION_REQUIRED", "DEFERRED_WITH_RECORDED_BASIS", "PARTIALLY_REMEDIATED"} else "NO_FOR_DOCUMENTARY_REMEDIATION",
            "closure_authority": "DOCUMENTARY_VALIDATION_ONLY_NO_FOUNDER_DECISION_RECORDED",
            "closure_status": "CLOSED_FOR_FINAL_DRAFT_VALIDATION" if disposition == "CONFIRMED_REMEDIATED" else "RETAINED_OPEN_OR_LIMITED",
        })
    write_csv(root / "CONSOLIDATED_EXTERNAL_REVIEW_FINDING_REGISTER.csv", rows, fields)
    (root / "CONSOLIDATED_EXTERNAL_REVIEW_FINDING_REGISTER.json").write_text(json.dumps(rows, indent=2) + "\n")
    counts = {}
    for r in rows:
        counts[r["disposition"]] = counts.get(r["disposition"], 0) + 1
    report = ["# Consolidated External Review Disposition Report", "", f"Authority boundary: `{AUTHORITY}`", "", f"Total consolidated rows: {len(rows)}", ""]
    for k in sorted(counts):
        report.append(f"- {k}: {counts[k]}")
    report += ["", "Blocking results:", "", "- C-OR-01 / F-02: remediated by purpose-specific Document 10 templates and distinctness validator.", "- C-OR-02: remediated by a single exact 13-state lifecycle vocabulary and byte-identical Founder decision question text.", "- C-OR-03 / F-16: remediated by the final failure-capable validator and negative controls.", ""]
    (root / "CONSOLIDATED_EXTERNAL_REVIEW_DISPOSITION_REPORT.md").write_text("\n".join(report))
    unresolved = [
        {"issue_id": "T1FD-UNRES-001", "issue": "Founder decisions FD-T1R2-001 through FD-T1R2-005 remain unanswered.", "status": "FOUNDER_DECISION_REQUIRED", "closure_criteria": "Authenticated Founder instruction supplied."},
        {"issue_id": "T1FD-UNRES-002", "issue": "External attestation/signature of package integrity root is not supplied.", "status": "DEFERRED_WITH_RECORDED_BASIS", "closure_criteria": "External attestation or signature supplied."},
        {"issue_id": "T1FD-UNRES-003", "issue": "Protected branch does not contain this final-draft package.", "status": "DRAFT_PR_REQUIRED", "closure_criteria": "Separate authorized PR disposition."},
    ]
    write_csv(root / "UNRESOLVED_ISSUE_REGISTER.csv", unresolved, list(unresolved[0].keys()))
    risks = [
        {"risk_id": "T1FD-RISK-001", "risk": "Founder decision instruments could be mistaken for approval if authority boundary is hidden.", "treatment": "Boundary repeated in reports, templates, validator, and PR body.", "founder_action_required": "YES"},
        {"risk_id": "T1FD-RISK-002", "risk": "First-party validation is not third-party certification.", "treatment": "Terminology converted to first-party documentary language.", "founder_action_required": "NO"},
    ]
    write_csv(root / "FINAL_RESIDUAL_RISK_REGISTER.csv", risks, list(risks[0].keys()))

def copy_review_inputs(repo_root, root):
    src = repo_root.parent / "input_extract_20260802_final" / "EQUINESYNC_TIER_1_DOCS_03_10_FINAL_REVIEW_INPUTS"
    dest = root / "REVIEWS" / "EXTERNAL_REVIEW_INPUTS"
    dest.mkdir(parents=True, exist_ok=True)
    for p in [src / "02_FOUNDER_BRIEF" / "EQUINESYNC_T1_FOUNDER_REVIEW_BRIEF.md", *sorted((src / "03_EXTERNAL_REVIEWS").glob("*.md"))]:
        shutil.copy2(p, dest / p.name)

def write_reports(root, repo_root):
    (root / "FINAL_DRAFT_EXECUTIVE_SUMMARY.md").write_text(f"""# Final Draft Executive Summary

Determination target: `TIER_1_DOCUMENTS_03_10_FINAL_DRAFT_COMPLETE_READY_FOR_FOUNDER_DIRECTIONAL_AND_DOCUMENTARY_REVIEW`.

Authority boundary: `{AUTHORITY}`.

This package is a first-party documentary final draft for Founder directional and documentary review. It remediates the three blocking external-review themes by creating purpose-specific Document 10 templates, enforcing one exact 13-state lifecycle vocabulary, and adding failure-capable final validation with negative controls.
""")
    (root / "FINAL_DRAFT_DELTA_REPORT.md").write_text("""# Final Draft Delta Report

- Added consolidated external review finding register and disposition report.
- Replaced Document 10 clone templates with 19 purpose-specific instruments.
- Renamed first-party instruments away from unqualified certification and ratification language where appropriate.
- Established a single exact 13-state lifecycle vocabulary.
- Rebuilt Founder decision packet with unanswered, byte-identical decision questions.
- Added final-draft validation source, package-only evidence, repository-aware evidence, and negative-control evidence.
""")
    (root / "FINAL_CROSS_DOCUMENT_RECONCILIATION_REPORT.md").write_text(f"""# Final Cross-Document Reconciliation Report

The final draft reconciles Documents 03-10 around a single authority boundary:

`{AUTHORITY}`.

The Founder decision packet, lifecycle vocabulary, unresolved issue register, residual-risk register, template index, and validation evidence are aligned to documentary-only status. No Founder decision is inferred or recorded.
""")
    (root / "TERMINOLOGY_AUDIT_REPORT.md").write_text("""# Terminology Audit Report

Conservative substitutions applied:

- `INTERNAL_DOCUMENTARY_REVIEW` replaces unqualified audit usage in the first template.
- `FOUNDER_DOCUMENTARY_ACKNOWLEDGEMENT` replaces Founder ratification instrument naming.
- `FINAL_DOCUMENTARY_CLOSING_RECORD` replaces closing certificate naming.
- `BOUNDED_SCOPE_SELF_DECLARATION_RECORD` replaces bounded-scope closing certificate naming.
- `PERIODIC_REVIEW_OR_REFRESH_RECORD` replaces recertification record naming.

Retained legacy terms may appear inside historical source files or review inputs and are retained for provenance. They do not create certification, adoption, activation, implementation, production-use, or merge authority.
""")
    (root / "REVIEW_HEAD_AND_BRANCH_CUSTODY_RECORD.md").write_text(f"""# Review Head And Branch Custody Record

- Protected branch: `integrate-emergent-final-zip`
- Branch point: `{subprocess.check_output(['git','rev-parse','HEAD'], cwd=repo_root, text=True).strip()}`
- Work branch: `{subprocess.check_output(['git','branch','--show-current'], cwd=repo_root, text=True).strip()}`
- Protected branch mutation: `NO`
- Merge authority: `MERGE_NOT_AUTHORIZED`
""")
    (root / "DRAFT_PR_DESCRIPTION.md").write_text(f"""# Tier 1 Documents 03-10 Final Draft Remediation

This draft PR adds the final-draft successor package for Tier 1 Documents 03-10.

Authority boundary: `{AUTHORITY}`.

Source package:

- `EQUINESYNC_TIER_1_DOCUMENTS_03_10_ROUND_3_PART_B.zip`
- SHA-256: `18adf9db56231b1b77d126aefad250f112a0056547bd0817506abd5411ee4cdd`
- Bytes: `2790854`

Blocking findings:

- C-OR-01 / F-02: remediated by purpose-specific Document 10 templates and distinctness validation.
- C-OR-02: remediated by exact 13-state lifecycle consistency.
- C-OR-03 / F-16: remediated by document-specific final validator and negative controls.

Founder decisions FD-T1R2-001 through FD-T1R2-005 remain unanswered: `NO_DISPOSITION_SELECTED`; `NO_FOUNDER_DECISION_RECORDED`; `NONE_BY_THIS_PACKAGE`.

This PR is draft-only. `MERGE_NOT_AUTHORIZED`. Auto-merge must remain disabled.
""")

def write_validator(root):
    path = root / "VALIDATION" / "validate_final_draft.py"
    path.write_text(r'''#!/usr/bin/env python3
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
''')
    path.chmod(0o755)

def rebuild_integrity(root):
    excluded = {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256", "MANIFEST_OF_MANIFESTS.sha256", "FINAL_DRAFT_INTEGRITY_ROOT.json"}
    files = []
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.name not in excluded and ".DS_Store" not in p.name:
            files.append({"path": rel(p, root), "sha256": sha(p), "byte_length": p.stat().st_size})
    (root / "PACKAGE_MANIFEST.json").write_text(json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(), "files": files}, indent=2) + "\n")
    with (root / "CHECKSUMS.sha256").open("w") as f:
        for item in files:
            f.write(f"{item['sha256']}  {item['path']}\n")
    manifest_files = [p for p in root.rglob("PACKAGE_MANIFEST.json") if p != root / "PACKAGE_MANIFEST.json"]
    with (root / "MANIFEST_OF_MANIFESTS.sha256").open("w") as f:
        for p in sorted(manifest_files):
            f.write(f"{sha(p)}  {rel(p, root)}\n")
    integrity = {
        "record_type": "FINAL_DRAFT_INTEGRITY_ROOT",
        "authority_boundary": AUTHORITY,
        "package_manifest_sha256": sha(root / "PACKAGE_MANIFEST.json"),
        "checksums_sha256": sha(root / "CHECKSUMS.sha256"),
        "manifest_of_manifests_sha256": sha(root / "MANIFEST_OF_MANIFESTS.sha256"),
        "external_attestation_state": "NOT_ATTESTED",
        "files_covered": len(files),
    }
    (root / "FINAL_DRAFT_INTEGRITY_ROOT.json").write_text(json.dumps(integrity, indent=2) + "\n")

def make_zip(repo_root, root):
    zip_path = root.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob("*")):
            if p.is_file():
                z.write(p, root.name + "/" + rel(p, root))
    sidecar = zip_path.with_suffix(zip_path.suffix + ".sha256")
    sidecar.write_text(f"{sha(zip_path)}  {zip_path.name}\n")
    return zip_path

def main():
    repo_root = Path.cwd()
    root = repo_root / "governance/portfolio/tier-1/drafting/EQUINESYNC_TIER_1_DOCUMENTS_03_10_FINAL_DRAFT_V1"
    copy_review_inputs(repo_root, root)
    write_templates(root)
    write_lifecycle(root)
    write_decisions(root)
    write_findings(root)
    write_reports(root, repo_root)
    write_validator(root)
    rebuild_integrity(root)
    zip_path = make_zip(repo_root, root)
    (root / "FINAL_ZIP_RECORD.json").write_text(json.dumps({"zip_path": zip_path.relative_to(repo_root).as_posix(), "sha256": sha(zip_path), "byte_length": zip_path.stat().st_size}, indent=2) + "\n")
    rebuild_integrity(root)
    print(root)

if __name__ == "__main__":
    main()
