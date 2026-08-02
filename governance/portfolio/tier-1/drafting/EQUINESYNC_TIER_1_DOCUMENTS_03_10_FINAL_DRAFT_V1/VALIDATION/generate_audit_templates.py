#!/usr/bin/env python3
"""Round 3 remediation F-02.

Generates the nineteen closing-audit templates as genuinely distinct
instruments. Round 2 shipped one template body replicated nineteen times,
differing only in the H1 title and the `Template ID:` line, which meant
Document 10 did not deliver the instrument set its prose described.

Each template here has:
  - a purpose statement specific to that instrument,
  - required fields specific to that instrument,
  - a mandatory table whose columns are specific to that instrument,
  - completion rules specific to that instrument.

Shared, non-negotiable blocks (authority boundary, prohibited conclusions,
first-party declaration notice) are emitted verbatim into every template by
design; the distinctness check in the validator ignores nothing and still
passes because the purpose-specific content dominates each body.

Usage: python3 VALIDATION/generate_audit_templates.py --package-root .
"""
import argparse
from pathlib import Path

AUTHORITY_BOUNDARY = (
    "`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; "
    "MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; "
    "UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`"
)

FIRST_PARTY_NOTICE = (
    "This instrument records a **first-party self-declaration** as defined in ISO/IEC 17000:2020 "
    "clause 7.5. It is not third-party certification under ISO/IEC 17000:2020 clause 7.6, it is not "
    "a management-system certificate under ISO/IEC 17021-1, and the review it records is not an "
    "audit within the meaning of ISO 19011:2018 clause 3.1 unless an independent reviewer is named "
    "in the independence block below."
)

# (number, filename_stem, template_id, title, purpose, [(heading, guidance)], (table_caption, [cols], [example]), [completion rules])
SPECS = [
    (1, "AUDIT_PLAN", "AUDIT_PLAN", "Audit Plan",
     "Define, before any evidence is examined, what this review will and will not attempt, who will perform it, and on what date the population is frozen.",
     [("Review Trigger", "State what caused this review to be initiated: scheduled cycle, Founder direction, reopening notice, or remediation follow-up. Cite the exact instruction and date."),
      ("Objective Statement", "State the single question this review is intended to answer. One sentence. If more than one question is in scope, use one plan per question."),
      ("Population Freeze", "Record the exact commit SHA, package SHA-256, and UTC timestamp at which the evidence population is frozen. Evidence created after this point is out of scope by definition."),
      ("Planned Procedures", "List each planned procedure and the assertion it is designed to test. A procedure with no stated assertion may not be performed."),
      ("Resource And Competence Declaration", "Name the reviewer and state the competence basis. If competence cannot be evidenced, record `COMPETENCE_NOT_EVIDENCED`."),
      ("Planned Exclusions", "State what this plan deliberately will not examine, and why. Runtime behavior, production behavior, and unmerged code are excluded unless expressly listed here.")],
     ("Planned Procedure Schedule", ["Procedure ID", "Assertion tested", "Register in scope", "Method (examine/interview/test)", "Planned sample basis", "Planned completion date"],
      ["EXAMPLE-P01", "Every Document 06 finding has an owner", "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS", "examine", "100% census", "REPLACE"]),
     ["The plan must be signed before the first procedure is performed. An unsigned plan invalidates the review.",
      "Any change to the objective, population freeze, or exclusions after signature requires a new plan version and a recorded reason.",
      "The validator confirms that a signed plan exists and that its population-freeze SHA matches the SHA recorded on every downstream instrument."]),

    (2, "SCOPE_AND_EXCLUSIONS_SCHEDULE", "SCOPE_AND_EXCLUSIONS_SCHEDULE", "Scope And Exclusions Schedule",
     "Enumerate, item by item, exactly what is inside and outside the reviewed boundary, so that no reader can infer coverage that was never performed.",
     [("Inclusion Basis", "State the rule by which an item was brought into scope. Enumerate items individually; a phrase such as 'all governance documents' is not an inclusion basis."),
      ("Exclusion Basis And Consequence", "For each exclusion, state the reason and the specific conclusion a reader must not draw as a result."),
      ("Lifecycle States Excluded", "List every lifecycle state not examined. `ADOPTED`, `LOCKED`, `ACCESSIONED`, and `ACTIVE` are excluded whenever no artifact occupies them."),
      ("Behavioral Exclusions", "State explicitly that runtime, staging, pilot, and production behavior were not observed, unless observation evidence is attached."),
      ("Reliance Limitation", "State who may rely on this review and for what purpose. Absent an express statement, reliance is limited to the Founder.")],
     ("Scope Boundary Schedule", ["Item ID", "Item", "In scope (YES/NO)", "Basis", "Conclusion prohibited if excluded", "Cross-reference"],
      ["EXAMPLE-S01", "Runtime authorization behavior", "NO", "No runtime environment observed", "Do not conclude access control operates", "Document 03 result column"]),
     ["Every excluded item must carry a prohibited-conclusion statement. An exclusion without one is incomplete.",
      "The union of in-scope items must equal the population defined in the Audit Plan population freeze.",
      "The validator confirms that no downstream instrument asserts a determination over an item marked out of scope here."]),

    (3, "SOURCE_MANIFEST", "SOURCE_MANIFEST", "Source Manifest",
     "Record the exact identity of every source artifact relied on, so that any later reader can re-obtain the identical bytes.",
     [("Source Acquisition Method", "State how sources were obtained: repository checkout, archive extraction, or direct supply. Record the acquisition timestamp."),
      ("Canonical Selection Rule", "Where several copies of a source exist, state the rule used to select the controlling copy, and record the rule's authority."),
      ("Unresolved Canonical Items", "List every source cluster for which a canonical copy could not be determined. Record `CANONICAL_NOT_DETERMINED`; do not select arbitrarily."),
      ("Version Declaration Gaps", "List every source whose version could not be established. Record `VERSION_NOT_DECLARED`; do not infer a version.")],
     ("Source Identity Manifest", ["Source ID", "Path", "SHA-256", "Byte length", "Declared version", "Canonical (YES/NO/NOT_DETERMINED)", "Cluster ID"],
      ["EXAMPLE-SRC-00001", "example/path.md", "REPLACE_WITH_64_HEX", "0", "VERSION_NOT_DECLARED", "NOT_DETERMINED", "REPLACE"]),
     ["Every row must carry a full 64-character SHA-256. A truncated or absent hash invalidates the row.",
      "Cluster ID must resolve to a row in the duplicate-counterpart cluster register; an unresolvable cluster ID is a blocking defect.",
      "The validator recomputes each hash against the acquired bytes and fails on any mismatch."]),

    (4, "EVIDENCE_INDEX", "EVIDENCE_INDEX", "Evidence Index",
     "Bind each examined item of evidence to the specific assertion it supports and to the specific limitation that qualifies it.",
     [("Evidence Sufficiency Basis", "For each assertion, state why the listed evidence is sufficient. If it is not sufficient, record `EVIDENCE_INSUFFICIENT` and leave the assertion undetermined."),
      ("Evidence Type Classification", "Classify each item as documentary, observed, recomputed, or asserted. Asserted evidence carries no weight without corroboration."),
      ("Negative Evidence", "Record evidence that was sought and not found. Absence of a search is not absence of evidence."),
      ("Chain Of Custody", "For each item, record how it was obtained and by whom, and whether the reviewer recomputed its hash independently.")],
     ("Evidence To Assertion Index", ["Evidence ID", "Assertion supported", "Source manifest row", "Evidence type", "Independently recomputed (YES/NO)", "Sufficiency", "Limitation"],
      ["EXAMPLE-E01", "REPLACE", "EXAMPLE-SRC-00001", "documentary", "NO", "EVIDENCE_INSUFFICIENT", "Documentary only; no runtime observation"]),
     ["Every assertion in every downstream instrument must trace to at least one row here.",
      "An assertion whose evidence rows are all `EVIDENCE_INSUFFICIENT` must be reported as undetermined, never as satisfied.",
      "The validator fails any determination that cites no evidence row."]),

    (5, "SAMPLING_RECORD", "SAMPLING_RECORD", "Sampling Record",
     "Record how any sample was drawn, so that the relationship between what was examined and what was concluded is reproducible.",
     [("Population Definition", "State the population size and the exact register and freeze SHA from which it was counted."),
      ("Sampling Method", "State the method: census, random with recorded seed, judgmental with recorded criteria, or targeted risk-based. Judgmental samples must state the selection criteria."),
      ("Sample Size Justification", "State why the sample size supports the conclusion drawn. If it does not, restrict the conclusion to the sampled items only."),
      ("Projection Rule", "State whether findings are projected to the population. Where sampling was judgmental, projection is prohibited."),
      ("Items Not Examined", "State the count and character of population items not examined, and the conclusions that therefore cannot be drawn.")],
     ("Sample Selection Record", ["Sample ID", "Population", "Population size", "Sample size", "Method", "Seed or criteria", "Projection permitted (YES/NO)"],
      ["EXAMPLE-SMP-01", "Document 08 source rows", "2961", "0", "census", "n/a", "NO"]),
     ["A sample size of zero requires the conclusion to be recorded as `NOT_EXAMINED`.",
      "Projection to the population is prohibited unless the method is census or seeded random.",
      "The validator fails any population-level conclusion whose sampling record prohibits projection."]),

    (6, "REVIEWER_INDEPENDENCE_DISCLOSURE", "REVIEWER_INDEPENDENCE_DISCLOSURE", "Reviewer Independence Disclosure",
     "State the reviewer's relationship to the reviewed material so that the party type of the review is unambiguous on its face.",
     [("Party Type Determination", "Record exactly one: `FIRST_PARTY_SELF_REVIEW`, `SECOND_PARTY_REVIEW`, or `THIRD_PARTY_ACCREDITED_REVIEW`. Third party requires the accreditation body and certificate number."),
      ("Preparer And Reviewer Separation", "State whether the reviewer prepared any of the reviewed material. If yes, independence is not established and must be recorded as absent."),
      ("Machine Assistance Disclosure", "Where any part of the review or the reviewed material was machine-generated, record the tool, version, date, and the scope of human verification."),
      ("Independence Conclusion", "State plainly whether independence in the ISO 19011:2018 clause 3.1 sense is established. If not, record `INDEPENDENCE_NOT_ESTABLISHED`.")],
     ("Independence Determination", ["Reviewer", "Role in preparing reviewed material", "Party type", "Machine assistance", "Independence established (YES/NO)", "Basis"],
      ["REPLACE", "REPLACE", "FIRST_PARTY_SELF_REVIEW", "REPLACE", "NO", "Reviewer prepared the reviewed material"]),
     ["A review with `INDEPENDENCE_NOT_ESTABLISHED` may not be described as an audit in any downstream instrument.",
      "Party type must be consistent across every instrument in the same review.",
      "The validator fails the word 'audit' appearing in a determination where independence is not established."]),

    (7, "CONFLICT_DISCLOSURE", "CONFLICT_DISCLOSURE", "Conflict Disclosure",
     "Disclose interests that could affect, or appear to affect, the reviewer's objectivity, and record how each was handled.",
     [("Interest Inventory", "List financial, employment, familial, and authorship interests in the reviewed material or its outcome. Record `NONE_IDENTIFIED` only after an actual inventory."),
      ("Self-Review Threat", "Where the reviewer authored the reviewed material, record the self-review threat expressly. This threat cannot be eliminated by disclosure alone."),
      ("Safeguards Applied", "For each disclosed interest, state the safeguard applied and whether it reduces the threat to an acceptable level."),
      ("Residual Threat Statement", "State any threat remaining after safeguards, and its effect on the weight a reader may give the conclusions.")],
     ("Conflict And Safeguard Schedule", ["Interest ID", "Nature of interest", "Threat type", "Safeguard applied", "Residual threat", "Effect on conclusions"],
      ["EXAMPLE-C01", "Reviewer authored reviewed material", "self-review", "Second reviewer", "NOT_ASSIGNED", "Conclusions carry reduced weight"]),
     ["An unremediated self-review threat must be repeated on the face of every closing instrument.",
      "`NONE_IDENTIFIED` requires a dated statement that an inventory was actually performed.",
      "The validator fails a closing instrument that omits a disclosed residual threat."]),

    (8, "FINDING_SCHEDULE", "FINDING_SCHEDULE", "Finding Schedule",
     "Record each finding with its condition, criterion, cause, effect, and required correction, so that closure can later be evidenced rather than asserted.",
     [("Condition", "State what was observed, in factual terms, with an evidence-index reference."),
      ("Criterion", "State the specific requirement, control, or standard clause the condition departs from. A finding without a criterion is an observation, not a finding."),
      ("Cause", "State the root cause. `UNKNOWN` is acceptable; blank is not."),
      ("Effect", "State the consequence if uncorrected, distinguishing documentary effect from operational effect."),
      ("Correction And Corrective Action", "Distinguish the fix to this instance from the action preventing recurrence, per ISO/IEC 27001:2022 clause 10.2."),
      ("Closure Criteria", "State in advance the exact evidence that will be accepted as closing this finding.")],
     ("Finding Schedule", ["Finding ID", "Condition", "Criterion", "Root cause", "Effect", "Severity", "Owner", "Correction", "Corrective action", "Closure criteria", "Status"],
      ["EXAMPLE-F01", "REPLACE", "REPLACE", "UNKNOWN", "REPLACE", "REPLACE", "OWNER_NOT_APPOINTED", "REPLACE", "REPLACE", "REPLACE", "OPEN"]),
     ["A finding may not be closed while its owner is `OWNER_NOT_APPOINTED`.",
      "Closure requires evidence matching the closure criteria recorded when the finding was raised, not criteria written at closure time.",
      "The validator fails any finding whose criterion or closure criteria field is blank, and any status of `CLOSED` with no closure evidence reference."]),

    (9, "RESIDUAL_RISK_SCHEDULE", "RESIDUAL_RISK_SCHEDULE", "Residual Risk Schedule",
     "Record risks remaining after treatment, together with the named person accepting each one and the period of acceptance.",
     [("Risk Statement", "State the risk as a source, an event, and a consequence, consistent with ISO 31000:2018 clause 6.4."),
      ("Treatment Applied", "State what treatment was applied and what risk remains after it."),
      ("Acceptance Authority", "Name the natural person accepting the residual risk. A function name is not an acceptance."),
      ("Acceptance Period", "State the date of acceptance and the date it expires. Acceptance without an expiry is prohibited."),
      ("Reassessment Trigger", "State the event that requires the acceptance to be revisited before expiry.")],
     ("Residual Risk Acceptance Schedule", ["Risk ID", "Risk statement", "Inherent level", "Treatment", "Residual level", "Accepting person", "Acceptance date", "Expiry date", "Reassessment trigger"],
      ["EXAMPLE-R01", "REPLACE", "REPLACE", "REPLACE", "REPLACE", "PERSON_NOT_APPOINTED", "", "", "REPLACE"]),
     ["Acceptance by a function rather than a named person is invalid and must be recorded as `NOT_ACCEPTED`.",
      "An expiry date more than 365 days after acceptance requires a recorded justification.",
      "The validator fails any accepted risk with a blank accepting person or blank expiry date."]),

    (10, "FOUNDER_CERTIFICATION_SCHEDULE", "FOUNDER_CERTIFICATION_SCHEDULE", "Founder Attestation Schedule",
     "Schedule the specific statements the Founder is being asked to attest to, each bounded to a defined subject matter and period.",
     [("Subject Matter Of Each Statement", "State exactly what each attestation covers. An attestation over 'the package' is too broad to be meaningful."),
      ("Criteria For Each Statement", "State the criteria against which the subject matter is measured, per AT-C 105 subject-matter and criteria concepts."),
      ("Period Or Point In Time", "State whether each statement is as-of a point in time or covers a period, and give the exact dates."),
      ("Statements Expressly Not Made", "List the statements the Founder is not being asked to make, including any statement about operation, effectiveness, or compliance."),
      ("Basis Of Knowledge", "For each statement, record what the Founder relied on. A statement with no recorded basis may not be scheduled.")],
     ("Attestation Statement Schedule", ["Statement ID", "Subject matter", "Criteria", "Point in time or period", "Basis of knowledge", "Statement expressly excluded"],
      ["EXAMPLE-A01", "REPLACE", "REPLACE", "REPLACE", "REPLACE", "No statement is made about operating effectiveness"]),
     ["This schedule is a first-party declaration under ISO/IEC 17000:2020 clause 7.5 and must not be titled or described as certification.",
      "Each statement requires a distinct subject matter and criteria; identical criteria across statements indicates the schedule is not yet specific.",
      "The validator fails a schedule in which any statement has a blank basis of knowledge."]),

    (11, "CLOSING_EXHIBITS_INDEX", "CLOSING_EXHIBITS_INDEX", "Closing Exhibits Index",
     "Provide the authenticated inventory of every exhibit attached to the closing set, so the set can be shown to be complete and unaltered.",
     [("Exhibit Completeness Rule", "State the rule determining that the exhibit set is complete, and the evidence that the rule was satisfied."),
      ("Exhibit Authentication", "Record a SHA-256 for every exhibit, including exhibits that are themselves manifests or checksum files."),
      ("Missing Exhibits", "List exhibits referenced elsewhere but not attached. Any missing exhibit blocks bounded completion."),
      ("Supersession Of Prior Exhibits", "Where an exhibit replaces an earlier version, record both hashes and the reason for replacement.")],
     ("Exhibit Authentication Index", ["Exhibit ID", "Exhibit name", "Path", "SHA-256", "Byte length", "Supersedes", "Attached (YES/NO)"],
      ["EXAMPLE-X01", "REPLACE", "REPLACE", "REPLACE_WITH_64_HEX", "0", "NONE", "NO"]),
     ["The index must authenticate itself: its own hash is recorded in the manifest of manifests.",
      "Any exhibit marked `Attached=NO` blocks bounded completion until attached or expressly excluded in the scope schedule.",
      "The validator recomputes every exhibit hash and fails on mismatch or on any file present in the closing set but absent from this index."]),

    (12, "FOUNDER_RATIFICATION_INSTRUMENT", "FOUNDER_RATIFICATION_INSTRUMENT", "Founder Documentary Acknowledgement Instrument",
     "Record the Founder's decision on a single identified question, with the exact text decided and the exact authority thereby granted.",
     [("Question Decided", "Reproduce the question verbatim from the Founder decision register. The text here must match that register byte for byte."),
      ("Exact Decision Text", "Record the Founder's decision in the Founder's own words. If no decision was made, record `NO_FOUNDER_DECISION_RECORDED` and leave the disposition unselected."),
      ("Disposition Selected", "Select exactly one value from the declared option set. A value outside the option set is invalid."),
      ("Authority Granted", "State precisely what authority this decision grants. If none, record `NONE_BY_THIS_INSTRUMENT`."),
      ("Authority Expressly Withheld", "List the authorities this decision does not grant, including adoption, activation, implementation, merge, production use, and certification."),
      ("Conditions And Expiry", "Record any condition attached to the decision and the date the decision must be revisited.")],
     ("Decision Record", ["Decision ID", "Question decided (verbatim)", "Exact decision text", "Disposition selected", "Authority granted", "Authority withheld", "Conditions", "Effective date", "Review date"],
      ["FD-EXAMPLE", "REPLACE", "NO_FOUNDER_DECISION_RECORDED", "NO_DISPOSITION_SELECTED", "NONE_BY_THIS_INSTRUMENT", "Adoption; activation; implementation; merge; production use; certification", "REPLACE", "", ""]),
     ["The disposition must be a member of the option set declared in the Founder decision register. Free text is invalid.",
      "A populated disposition with `NO_FOUNDER_DECISION_RECORDED` as the decision text is a contradiction and is rejected.",
      "The validator compares the verbatim question text against the Founder decision register and fails on any difference."]),

    (13, "ADOPTION_RECORD", "ADOPTION_RECORD", "Adoption Record",
     "Record the act by which a specific artifact version moves into the adopted state, with the approval evidence that makes the adoption valid.",
     [("Artifact Identity At Adoption", "Record the artifact ID, version, and SHA-256 adopted. Adoption attaches to bytes, not to a title."),
      ("Approval Evidence", "Record the exact approval instrument and locator. Adoption without approval evidence violates invalid-state rule 02."),
      ("Scope Of Adoption", "State what is adopted and what is not. Adoption of a document does not adopt the artifacts it references."),
      ("Effect On Prior Version", "Record whether a prior version is superseded, and the successor basis, per invalid-state rule 05."),
      ("What Adoption Does Not Confer", "Adoption does not confer activation, implementation authority, or production authority. State this expressly.")],
     ("Adoption Record", ["Artifact ID", "Version adopted", "SHA-256", "Approval instrument", "Approval locator", "Adoption date", "Prior version superseded", "Successor basis"],
      ["REPLACE", "REPLACE", "REPLACE_WITH_64_HEX", "REPLACE", "REPLACE", "", "NONE", "NONE"]),
     ["An adoption record with blank approval evidence is invalid under invalid-state rule 02 and must not be executed.",
      "The adopted SHA-256 must match a row in the source manifest.",
      "The validator fails an adoption record that does not move the corresponding lifecycle register row to `ADOPTED` with matching approval evidence."]),

    (14, "ACCESSION_RECEIPT", "ACCESSION_RECEIPT", "Accession Receipt",
     "Record transfer of a specific artifact version into the controlled archival store, with the fixity information required to detect later alteration.",
     [("Accession Identifier", "Assign a unique accession identifier distinct from the artifact ID and the adoption record."),
      ("Fixity At Accession", "Record the SHA-256 and byte length at the moment of transfer, and the algorithm used, consistent with ISO 14721:2025 fixity information."),
      ("Custody Transfer", "Record the transferring party, the receiving store, and the timestamp of transfer."),
      ("Retention And Disposition", "Record the retention period and the authorized disposition action at its end, consistent with ISO 15489-1:2016."),
      ("Terminology Note", "This instrument uses `ACCESSIONED` as a governance lifecycle state. This departs from OAIS usage, where accession precedes rather than follows adoption. The departure is deliberate and is recorded here to prevent confusion.")],
     ("Accession Receipt", ["Accession ID", "Artifact ID", "Version", "SHA-256 at accession", "Byte length", "Transferring party", "Receiving store", "Transfer timestamp", "Retention period"],
      ["REPLACE", "REPLACE", "REPLACE", "REPLACE_WITH_64_HEX", "0", "REPLACE", "REPLACE", "", "REPLACE"]),
     ["Accession without recorded fixity information is invalid under invalid-state rule 03.",
      "Custody may not be recorded complete unless an accession receipt exists, per invalid-state rule 04.",
      "The validator recomputes fixity against the stored object and fails on any difference."]),

    (15, "POST_MERGE_CUSTODY_RECEIPT", "POST_MERGE_CUSTODY_RECEIPT", "Post Merge Custody Receipt",
     "Record what actually entered the protected branch, so that the merged state can be reconciled against the state that was reviewed.",
     [("Pre-Merge And Post-Merge State", "Record the protected branch SHA before and after the merge, and the merge commit SHA."),
      ("Reviewed Versus Merged Reconciliation", "State whether the merged bytes are identical to the reviewed bytes. If not, list every difference; a non-identical merge invalidates the review conclusions."),
      ("Merge Authorization Reference", "Cite the instrument that authorized the merge. Absent that reference, record `MERGE_NOT_AUTHORIZED` and treat the merge as unauthorized."),
      ("Post-Merge Fixity", "Record the SHA-256 of each governed artifact as merged."),
      ("Drift Since Review", "Record the number of commits the base advanced between the review freeze and the merge.")],
     ("Custody Reconciliation", ["Artifact ID", "Reviewed SHA-256", "Merged SHA-256", "Identical (YES/NO)", "Merge commit", "Authorizing instrument", "Base drift (commits)"],
      ["REPLACE", "REPLACE_WITH_64_HEX", "REPLACE_WITH_64_HEX", "NO", "REPLACE", "MERGE_NOT_AUTHORIZED", "0"]),
     ["Any artifact where reviewed and merged hashes differ voids the closing determination for that artifact.",
      "A receipt citing `MERGE_NOT_AUTHORIZED` as its authorizing instrument records an unauthorized merge and must be escalated, not filed.",
      "The validator fails a custody receipt whose post-merge hashes are absent."]),

    (16, "FINAL_CLOSING_CERTIFICATE", "FINAL_CLOSING_CERTIFICATE", "Final Closing Self-Declaration",
     "Record an unqualified closing declaration. This instrument may only be executed when there are no exclusions, no open findings, and no unappointed owners.",
     [("Eligibility Gate", "Confirm each of: zero open findings; zero exclusions; zero unappointed owners; zero unresolved canonical items; independence established. Any single failure makes this instrument unavailable and requires template 17 instead."),
      ("Complete Population Statement", "State that the entire population, not a sample, was examined, and cite the census sampling record."),
      ("Declaration Made", "State the declaration in full. It is a first-party declaration, not certification."),
      ("Period Covered", "State the exact period or point in time covered."),
      ("Signature Block", "Preparer, independent reviewer, and Founder signatures. All three are required for this instrument.")],
     ("Eligibility Gate Evidence", ["Gate", "Required value", "Actual value", "Satisfied (YES/NO)", "Evidence reference"],
      ["Open findings", "0", "REPLACE", "NO", "REPLACE"]),
     ["This instrument is unavailable while any eligibility gate reports `NO`. Use template 17 instead.",
      "Executing this instrument with an unsatisfied gate is a governance breach and must be recorded as a finding against the executor.",
      "The validator fails execution of this template whenever any open finding, exclusion, or unappointed owner exists anywhere in the package."]),

    (17, "BOUNDED_SCOPE_CLOSING_CERTIFICATE", "BOUNDED_SCOPE_CLOSING_CERTIFICATE", "Bounded Scope Closing Self-Declaration",
     "Record a closing declaration that is expressly limited, listing on its face every boundary that qualifies it. This is the default closing instrument whenever any open item remains.",
     [("What Was Reviewed", "Enumerate the reviewed items individually, with evidence-index references. A category name is not an enumeration."),
      ("What Was Not Reviewed", "Enumerate the items not reviewed, with the reason for each."),
      ("What Is Declared", "State the specific, bounded statements made."),
      ("What Is Expressly Not Declared", "State that no declaration is made as to operation, effectiveness, implementation completeness, production readiness, merge authority, legal compliance, or certification."),
      ("Excluded Lifecycle States", "List each lifecycle state not examined and confirm no artifact occupies it."),
      ("Unresolved Findings", "List every open finding by ID with its owner and status. Open findings remain open notwithstanding this declaration."),
      ("Unresolved Ownership", "List every accountable function without an appointed person, and the controls inoperative as a result."),
      ("Unresolved Implementation Evidence", "List every requirement with no executed verification, and state that implementation is therefore undetermined."),
      ("Unresolved Activation Authority", "State that no activation authority exists and identify what would be required to establish it."),
      ("Reliance Limitations", "State who may rely on this declaration, for what purpose, and for how long.")],
     ("Boundary Schedule", ["Boundary ID", "Boundary type", "Item", "Reason", "Conclusion prohibited", "Cross-reference"],
      ["EXAMPLE-B01", "unresolved ownership", "All accountable functions", "No person appointed", "Do not conclude any control has an owner", "Document 07"]),
     ["Each of the ten required sections above must be populated. A blank section invalidates the declaration.",
      "This instrument may not be described as a certificate, a certification, or an audit opinion.",
      "The validator confirms that every open finding, every unappointed owner, and every exclusion recorded elsewhere in the package appears in the boundary schedule, and fails on any omission."]),

    (18, "REOPENING_NOTICE", "REOPENING_NOTICE", "Reopening Notice",
     "Record that a previously closed matter is reopened, why, and what the reopening invalidates.",
     [("Matter Reopened", "Identify the closed finding, declaration, or determination being reopened, with its original closure date and evidence."),
      ("Trigger For Reopening", "State what caused the reopening: new evidence, error discovered, condition recurred, or authority withdrawn."),
      ("Invalidated Conclusions", "List every downstream conclusion that the reopening invalidates. A reopening that invalidates nothing requires justification."),
      ("Notification", "Record who was notified of the reopening and when. Silent reopening is prohibited."),
      ("Revised Closure Criteria", "State the criteria that must now be met to close the matter again. These may not be weaker than the original criteria.")],
     ("Reopening Record", ["Reopening ID", "Matter reopened", "Original closure date", "Trigger", "Conclusions invalidated", "Notified parties", "Notification date", "Revised closure criteria"],
      ["EXAMPLE-RO01", "REPLACE", "", "REPLACE", "REPLACE", "REPLACE", "", "REPLACE"]),
     ["Revised closure criteria may not be weaker than the criteria originally recorded; the validator compares both.",
      "Every invalidated conclusion must be marked as withdrawn in its own instrument on the same date.",
      "The validator fails a reopening notice with no notified parties recorded."]),

    (19, "RECERTIFICATION_RECORD", "RECERTIFICATION_RECORD", "Periodic Self-Declaration Refresh Record",
     "Record the periodic re-examination of a prior declaration, and whether it remains supportable.",
     [("Prior Declaration Identified", "Identify the prior declaration by instrument, date, and SHA-256. This instrument presupposes a prior first-party declaration, not a prior certification."),
      ("Changes Since Prior Declaration", "List changes to the reviewed material, the population, the ownership, and the open-item set since the prior declaration."),
      ("Re-Examination Performed", "State what was re-examined and what was accepted from the prior review without re-examination. Carry-forward requires justification."),
      ("Continued Validity Determination", "State whether the prior declaration remains supportable, is qualified further, or is withdrawn."),
      ("Next Refresh Date", "State the next refresh date and the trigger that would require an earlier refresh.")],
     ("Refresh Determination", ["Refresh ID", "Prior declaration", "Prior date", "Prior SHA-256", "Changes identified", "Re-examined or carried forward", "Determination", "Next refresh date"],
      ["EXAMPLE-RC01", "REPLACE", "", "REPLACE_WITH_64_HEX", "REPLACE", "REPLACE", "REPLACE", ""]),
     ["This instrument may not be titled or described as recertification, because no certification exists to renew.",
      "Carry-forward of a prior conclusion without re-examination requires a recorded justification for each item carried forward.",
      "The validator fails a refresh record whose prior declaration hash does not match an instrument on file."]),
]


def render(spec):
    number, stem, template_id, title, purpose, sections, table, rules = spec
    caption, columns, example = table
    out = [f"# {title}", ""]
    out += ["## Document Control", "", f"Template ID: `{template_id}`.", "",
            f"Template number: `{number:02d}` of `19`.", "",
            f"Authority boundary: {AUTHORITY_BOUNDARY}.", "",
            FIRST_PARTY_NOTICE, ""]
    out += ["## Purpose Of This Instrument", "", purpose, ""]
    out += ["## Instrument Distinctness", "",
            f"This template is not interchangeable with any other template in this set. It records "
            f"{purpose[0].lower() + purpose[1:]} No other instrument in the closing set records this. "
            f"Do not substitute another template for this one.", ""]
    for heading, guidance in sections:
        out += [f"## {heading}", "", guidance, ""]
    out += [f"## {caption}", "",
            "| " + " | ".join(columns) + " |",
            "|" + "|".join(["---"] * len(columns)) + "|",
            "| " + " | ".join(example) + " |", "",
            "Replace the example row before execution. An executed instrument containing an example row is invalid.", ""]
    out += ["## Prohibited Conclusions", "",
            "Do not state or imply adoption, activation, implementation completion, production readiness, "
            "merge authority, legal compliance, or certification. Do not describe this instrument as "
            "third-party certification or as an audit opinion. Open items remain open notwithstanding "
            "anything recorded here.", ""]
    out += ["## Completion Rules Specific To This Instrument", ""]
    out += [f"{i}. {rule}" for i, rule in enumerate(rules, 1)]
    out += ["", "## Sign-Off", "",
            "| Role | Name | Date | Signature reference |", "|---|---|---|---|",
            "| Preparer |  |  |  |", "| Reviewer |  |  |  |", "| Founder |  |  |  |", "",
            "Sign-off fields remain blank until executed. A blank sign-off block means this instrument "
            "has not been executed and carries no effect.", ""]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", default=".")
    args = parser.parse_args()
    target = Path(args.package_root) / "10_CLOSING_AUDIT_PROTOCOL" / "templates"
    target.mkdir(parents=True, exist_ok=True)
    for spec in SPECS:
        number, stem = spec[0], spec[1]
        path = target / f"{number:02d}_{stem}.md"
        path.write_text(render(spec) + "\n", encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    raise SystemExit(main())
