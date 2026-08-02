# EQUINESYNC FOUNDER DIRECTIVE

## GOVERNANCE DOCUMENT LIFECYCLE SIMPLIFICATION, STATE CONTROL, AND TRANSITION STANDARD

**Directive ID:** ES-FD-GOV-LIFECYCLE-001
**Version:** 1.1.0
**Authority:** Founder
**Status:** FOUNDER APPROVED
**Effective Date:** Effective upon repository accession in accordance with Section 15
**Controlling Lifecycle:** Draft → Approved → Authoritative → Verified

---

# 1. Purpose

This Founder Directive establishes a single, controlling four-state lifecycle for EquineSync governance documents.

The purpose of this Directive is to:

1. eliminate redundant or overlapping lifecycle terminology;
2. distinguish documentary approval from repository authority and implementation verification;
3. prevent repository operations, deployment activities, and technical work from being mistaken for governance approval;
4. establish clear transition requirements and evidence for each lifecycle state;
5. preserve historical records without requiring unnecessary reapproval; and
6. create a lifecycle model suitable for repository enforcement, workflow automation, traceability, and audit.

This Directive supersedes prior governance lifecycle terminology only to the extent that prior terminology conflicts with the definitions, transition rules, or authority requirements stated here.

---

# 2. Founder Determination

The Founder determines that the prior lifecycle terminology:

* adoption;
* merge;
* activation;
* implementation;
* production use;
* certification; and
* automatic closure of findings

combined distinct concepts that should be governed separately.

Those concepts include:

* documentary development;
* Founder approval;
* establishment of governing authority;
* implementation activity;
* operational deployment;
* verification of conformity; and
* finding disposition.

Effective under this Directive, EquineSync governance documents shall use only the following lifecycle states:

1. Draft;
2. Approved;
3. Authoritative; and
4. Verified.

Implementation progress, deployment status, production use, certification activity, and finding status shall be tracked as separate attributes, events, registers, or evidence records. They shall not create additional document lifecycle states.

---

# 3. Scope

This Directive applies to all EquineSync governance artifacts, including:

* governance standards;
* governance policies;
* governance frameworks;
* Founder directives;
* product implementation atlases;
* code guides where assigned governance authority;
* privacy, safeguarding, security, artificial intelligence, health, identity, relationship, billing, operational, and compliance governance artifacts;
* governance registers and controlled appendices; and
* future documentary artifacts expressly classified as governance documents.

This Directive does not automatically apply to:

* ordinary engineering notes;
* issue comments;
* pull request descriptions;
* working spreadsheets;
* test output;
* implementation plans;
* deployment records; or
* informal communications,

unless such material is formally classified or incorporated as a controlled governance artifact.

---

# 4. Controlling Principles

The following principles govern interpretation of the four-state lifecycle.

## 4.1 State Is Documentary

A lifecycle state describes the legal, governance, or documentary status of the controlled artifact.

A lifecycle state does not, by itself, establish that:

* code has been written;
* implementation is complete;
* deployment has occurred;
* production use is authorized;
* testing has passed;
* certification has been issued; or
* findings have been closed.

## 4.2 State Changes Require Evidence

No document may change lifecycle state solely because:

* a file was renamed;
* a branch was created;
* a pull request was opened or merged;
* metadata was edited;
* a status label was changed;
* a document was copied into a different directory; or
* an automated tool inferred completion.

Each state transition requires the authority and evidence stated in this Directive.

## 4.3 No Implied Authority

Approval of content does not create production authority, deployment authority, operational authority, or unrestricted implementation authority unless such authority is expressly granted.

## 4.4 Highest Truthful State

A document shall be assigned only the highest lifecycle state fully supported by available evidence.

A document shall not be advanced based on anticipated, partial, assumed, or planned evidence.

## 4.5 No Automatic Forward Transition

No lifecycle transition is automatic unless a Founder-approved automation rule expressly identifies:

* the triggering evidence;
* the applicable document class;
* the authorized actor or system;
* the validation requirements; and
* the rollback or correction mechanism.

---

# 5. State 1: Draft

## 5.1 Definition

A Draft is a governance document under development, review, correction, or reconsideration that has not received final Founder approval for the version at issue.

## 5.2 Characteristics

A Draft:

* may contain unresolved questions, placeholders, findings, alternatives, or proposed decisions;
* may be revised without formal amendment procedures;
* may undergo internal, technical, legal, operational, or outside review;
* does not control conflicting governance;
* does not supersede an existing Authoritative version;
* does not establish mandatory implementation requirements; and
* shall not be represented as approved, adopted, controlling, active, effective, certified, or verified.

## 5.3 Permitted Activities

Permitted Draft activities include:

* drafting;
* redlining;
* review;
* comparison;
* testing of proposed approaches;
* evidence gathering;
* Founder review;
* outside review;
* revision; and
* preparation of a decision packet.

## 5.4 Implementation Restriction

A Draft does not authorize implementation.

Prototype, research, sandbox, or reversible exploratory work may occur only where separately authorized and clearly labeled as non-authoritative and non-production.

---

# 6. State 2: Approved

## 6.1 Definition

An Approved document is a specific, identified version whose substantive content has received express Founder approval.

## 6.2 Approval Requirements

A document may enter Approved state only where the approval record identifies, at minimum:

* the document title;
* the version or revision identifier;
* the approved file or canonical artifact;
* the approval date;
* the approving authority;
* any approved exceptions, modifications, retained findings, conditions, or limitations; and
* sufficient file identity information to distinguish the approved version from prior or later drafts.

Where practicable, file identity shall include a cryptographic hash, repository path, immutable record, or equivalent evidence.

## 6.3 Effect of Approval

Approved state means:

* the substantive governance decisions in the identified version are accepted by the Founder;
* the approved content shall not be materially changed without controlled revision or renewed approval;
* repository accession and authority-establishment work may proceed; and
* implementation planning may proceed.

Approved state does not, by itself:

* make the document the controlling repository authority;
* supersede the existing Authoritative version;
* authorize production use;
* authorize unrestricted implementation;
* establish implementation completion;
* close findings; or
* establish verification.

## 6.4 Implementation Authority

Implementation may begin from an Approved document only where one of the following exists:

1. the document expressly grants implementation authority;
2. a separate Founder directive grants implementation authority;
3. an applicable Authoritative governance instrument already grants such authority; or
4. the work is limited to non-production, reversible preparation that does not create operational reliance.

Absent one of these conditions, Approved state authorizes planning and accession work only.

---

# 7. State 3: Authoritative

## 7.1 Definition

An Authoritative document is the controlling governance source for its defined subject matter, scope, version, and effective period.

## 7.2 Authoritative Transition Requirements

An Approved document may enter Authoritative state only when all applicable requirements below are satisfied:

1. the approved version has been authenticated;
2. the canonical repository path or controlled source location has been established;
3. the document’s scope and supersession effect are identified;
4. conflicting or prior versions are appropriately retained, superseded, archived, or cross-referenced;
5. required metadata and registers are updated;
6. the accession or authority record identifies the effective version;
7. required validation checks pass; and
8. no unresolved authority blocker prevents the transition.

## 7.3 Authority Record

The Authoritative transition shall be supported by an accession, custody, adoption-equivalent, authority, or repository record that identifies:

* the authoritative artifact;
* its version;
* its canonical location;
* the effective date;
* the prior version, if any;
* the supersession rule;
* the approving authority;
* the repository or custody evidence; and
* any limitations on scope or implementation authority.

## 7.4 Effect of Authoritative State

An Authoritative document:

* governs future work within its stated scope;
* supersedes prior controlling versions only as expressly stated;
* shall be used by implementation atlases, code guides, specifications, validation work, and compliance review;
* may support implementation authority where such authority is expressly stated or separately granted; and
* remains authoritative unless amended, superseded, withdrawn, suspended, or invalidated through controlled governance action.

## 7.5 Merge Is Not Sufficient

A repository merge may be part of the evidence supporting Authoritative state, but merge alone does not establish authority.

A merged document remains Approved, or Draft if approval is absent, until all applicable Authoritative transition requirements are satisfied.

## 7.6 Activation Is Not a Separate State

The term “activation” may continue to describe a technical, operational, staged, feature, policy-enforcement, or deployment event.

Activation shall be recorded separately and shall not replace or alter the document’s governance lifecycle state.

## 7.7 Implementation Is Not a Separate State

Implementation shall be tracked independently using implementation status fields such as:

* not started;
* planned;
* in progress;
* partially implemented;
* implemented pending verification;
* verified conforming;
* implemented with exception;
* deferred; or
* not applicable.

These implementation statuses shall not be treated as governance lifecycle states.

---

# 8. State 4: Verified

## 8.1 Definition

A Verified document is an Authoritative document for which sufficient objective evidence demonstrates that the identified implementation, control environment, process, or governed subject conforms to the applicable requirements within a defined verification scope.

## 8.2 Verified Does Not Mean Universal Conformity

Verified state shall always be interpreted according to its stated scope.

Verification may be:

* document-wide;
* requirement-specific;
* module-specific;
* release-specific;
* environment-specific;
* implementation-wave-specific;
* facility-specific;
* jurisdiction-specific; or
* otherwise bounded.

A document shall not be represented as universally verified where verification covers only part of its requirements or implementation scope.

## 8.3 Verification Requirements

Verified state requires:

1. an Authoritative document;
2. a defined verification scope;
3. identified acceptance criteria;
4. objective evidence;
5. review by an authorized verifier or verification process;
6. a determination of conformity, exceptions, and residual risks;
7. traceability between requirements and evidence; and
8. a verification record retained in the controlled repository or evidence system.

## 8.4 Acceptable Verification Evidence

Verification evidence may include:

* repository review;
* code review;
* automated tests;
* manual tests;
* implementation atlas review;
* traceability matrices;
* configuration evidence;
* deployment evidence;
* process records;
* audit results;
* control testing;
* certification reports;
* security or privacy assessments;
* safeguarding review;
* legal compliance analysis;
* production observations;
* user acceptance evidence; or
* other evidence approved for the applicable domain.

No single evidence type is automatically sufficient for every document.

## 8.5 Verification Determinations

A verification record shall state one of the following, or an equivalent controlled determination:

* VERIFIED_CONFORMING;
* VERIFIED_CONFORMING_WITH_LIMITATIONS;
* PARTIALLY_VERIFIED;
* VERIFICATION_FAILED;
* VERIFICATION_BLOCKED;
* NOT_YET_VERIFIED; or
* NOT_APPLICABLE.

Only VERIFIED_CONFORMING or VERIFIED_CONFORMING_WITH_LIMITATIONS may support transition of the applicable scope to Verified state.

## 8.6 Production Use

Production use is not a lifecycle state.

Production use may:

* occur before verification only where separately authorized;
* be prohibited until verification where required by an applicable governance instrument;
* provide evidence supporting verification; or
* continue subject to limitations, remediation, monitoring, or accepted risk.

Verified state does not independently authorize production use unless production authority is expressly included in the governing approval, authoritative record, or separate Founder directive.

## 8.7 Certification

Certification is not a lifecycle state.

Certification may serve as verification evidence, but a certificate alone is sufficient only where:

* the certification scope matches the governance scope;
* the certifying body or process is authorized;
* the underlying evidence is adequate; and
* known exceptions are disclosed.

---

# 9. Findings Lifecycle

Findings shall be governed separately from document lifecycle.

The standard finding states are:

1. Open;
2. Accepted;
3. Resolved;
4. Verified Closed.

Additional controlled sub-statuses may be used where needed, including:

* disputed;
* deferred;
* accepted risk;
* duplicate;
* not reproducible;
* superseded;
* withdrawn; or
* not applicable.

## 9.1 Open

The finding has been identified and remains unresolved or undisposed.

## 9.2 Accepted

The finding has been acknowledged and assigned an approved disposition, owner, remediation path, risk treatment, or exception.

Accepted does not mean corrected or closed.

## 9.3 Resolved

Corrective action or an approved disposition has been completed, but closure evidence has not yet been independently verified.

## 9.4 Verified Closed

Objective evidence demonstrates that the finding’s closure criteria are satisfied.

A finding may be marked Verified Closed only where the closure record identifies:

* the finding;
* the applicable closure criteria;
* the supporting evidence;
* the verifying actor or process;
* the verification date; and
* any residual limitation or accepted risk.

## 9.5 No Uncontrolled Automatic Closure

A document becoming Verified does not automatically close every linked finding.

A linked finding may close automatically only where:

1. the finding has explicit machine-readable closure criteria;
2. the verification evidence satisfies those criteria;
3. the evidence is traceably linked to the finding;
4. no exception, residual risk, or contrary evidence remains;
5. the automated closure rule is Founder-approved; and
6. the closure event is logged and reversible if later shown to be erroneous.

Otherwise, the finding requires an explicit Verified Closed determination.

---

# 10. Relationship Between Document State and Operational Status

The following concepts shall be tracked independently from document lifecycle:

* implementation status;
* deployment status;
* production-use status;
* activation status;
* enforcement status;
* certification status;
* finding status;
* exception status;
* residual-risk status; and
* retirement or supersession status.

A document may therefore be:

* Authoritative but not yet implemented;
* Authoritative and partially implemented;
* Authoritative and implemented but not verified;
* Verified for one release but not another;
* Verified with limitations;
* Approved but not yet Authoritative; or
* Authoritative while production use remains prohibited.

These combinations are valid and shall not be collapsed into a single ambiguous status.

---

# 11. Transition Authority

## 11.1 Draft to Approved

Requires express Founder approval or approval by a properly delegated authority whose delegation is documented and applicable.

## 11.2 Approved to Authoritative

Requires completion of the Authoritative transition requirements and an accession or authority record.

The transition may be performed by an authorized governance custodian, repository custodian, or automated workflow only within granted authority.

## 11.3 Authoritative to Verified

Requires an authorized verification determination supported by objective evidence.

Verification authority may differ by domain. Legal, privacy, security, safeguarding, technical, financial, and operational verification shall be performed or approved by appropriately authorized reviewers.

## 11.4 No Skipping States

A document shall not move directly:

* from Draft to Authoritative;
* from Draft to Verified; or
* from Approved to Verified

without satisfying and recording the requirements of each intervening state.

A single transaction may record multiple transitions only where all required evidence and approvals for each transition independently exist.

---

# 12. Revision, Amendment, and Supersession

## 12.1 Material Changes

A material change to an Approved, Authoritative, or Verified document creates a new Draft version unless the change is expressly classified as non-substantive.

Material changes include changes to:

* requirements;
* permissions;
* prohibitions;
* authority;
* scope;
* definitions affecting interpretation;
* decision rights;
* control obligations;
* implementation requirements;
* verification criteria;
* risk treatment; or
* finding disposition.

## 12.2 Non-Substantive Changes

Formatting, spelling, broken links, metadata corrections, and equivalent editorial changes may be made through a controlled non-substantive correction process.

The correction record shall demonstrate that substantive meaning was not changed.

## 12.3 Supersession

A later document supersedes an earlier Authoritative document only where the supersession is explicit.

Approval of a new version does not, by itself, supersede the current Authoritative version.

The prior Authoritative version remains controlling until the new version enters Authoritative state, unless a Founder directive expressly provides otherwise.

## 12.4 Effect on Verified Status

A material change creates a new verification requirement for the changed scope.

Prior verification remains valid only for:

* the prior version;
* unchanged requirements;
* unchanged implementation; and
* the scope supported by retained evidence.

Verification shall not be carried forward automatically where the change could affect conformity.

---

# 13. Legacy Terminology Mapping

Legacy terminology shall be interpreted as follows, subject to the actual underlying evidence.

| Legacy Term               | New Treatment                                                                    |
| ------------------------- | -------------------------------------------------------------------------------- |
| Draft                     | Draft                                                                            |
| Proposed                  | Draft                                                                            |
| Candidate                 | Draft                                                                            |
| Founder Approved          | Approved                                                                         |
| Adopted                   | Usually Approved or Authoritative, depending on accession and authority evidence |
| Merged                    | Repository event only; may support Authoritative state                           |
| Accessioned               | May support Authoritative state if authority requirements are met                |
| Activated                 | Operational or technical event only                                              |
| Implementation Authorized | Separate authority attribute                                                     |
| Implemented               | Separate implementation-status attribute                                         |
| Production Use            | Separate operational-status attribute                                            |
| Certified                 | Verification evidence or separate certification attribute                        |
| Closed                    | Finding status, not document state                                               |
| Automatically Closed      | Permitted only under Section 9.5                                                 |
| Verified                  | Verified only where Section 8 requirements are met                               |

No legacy term shall be mechanically converted based only on its label.

Each existing artifact shall be mapped according to its actual approval, authority, implementation, and verification evidence.

---

# 14. Existing Documents and Migration

## 14.1 No Automatic Reapproval

Existing documents do not require reapproval solely because this Directive changes lifecycle terminology.

## 14.2 Evidence-Based Remapping

Each existing governance artifact shall be assigned the highest truthful state supported by evidence.

Examples:

* Founder-approved content not yet accessioned as controlling governance shall be Approved.
* Founder-approved content accessioned as the controlling source shall be Authoritative.
* An Authoritative document with complete scoped verification evidence may be Verified for that scope.
* A merged document lacking Founder approval shall remain Draft.
* A production-used document lacking verification evidence shall not be treated as Verified.

## 14.3 Migration Register

The governance program shall maintain a migration register identifying:

* document;
* legacy state;
* new state;
* supporting evidence;
* implementation status;
* verification scope;
* linked findings;
* unresolved ambiguity; and
* required follow-up action.

## 14.4 No Loss of Historical Evidence

Historical labels, approvals, merges, certifications, findings, and closure records shall be preserved as historical evidence.

Migration shall not erase or rewrite prior records.

---

# 15. Effective Date and Accession

This Directive is Founder Approved upon execution.

It becomes Authoritative when:

1. the Founder-approved version is authenticated;
2. it is placed in the designated canonical governance repository location;
3. the authority and lifecycle registers are updated;
4. its supersession effect is recorded; and
5. an accession record confirms the effective date and controlling version.

Until those steps are complete, this Directive shall be treated as Approved but not yet Authoritative.

No person or system shall describe this Directive as Authoritative solely because the text states that it is Founder Approved.

---

# 16. Required Implementation Actions

The governance program shall:

1. update lifecycle fields to permit only Draft, Approved, Authoritative, and Verified;
2. create separate fields for implementation, activation, deployment, production use, certification, findings, exceptions, and residual risk;
3. update governance templates and registers;
4. update repository validators and automation;
5. create the migration register required by Section 14;
6. identify legacy terms that require evidence-based interpretation;
7. prevent uncontrolled automatic finding closure;
8. update reviewer and Codex directives to use the new lifecycle;
9. preserve historical terminology in archival records; and
10. produce a validation report confirming that the lifecycle change did not silently advance any document, implementation, or finding status.

These actions are documentary and workflow changes only unless separate implementation or production authority is granted.

---

# 17. Prohibited Interpretations

This Directive shall not be interpreted to mean that:

* Founder approval automatically creates repository authority;
* repository merge automatically creates governance authority;
* Authoritative status means implementation is complete;
* Authoritative status independently authorizes production deployment;
* production use proves conformity;
* certification automatically proves full compliance;
* Verified status applies beyond its stated scope;
* all linked findings close when a document becomes Verified;
* historical records may be deleted after migration;
* a document may silently skip a required lifecycle state; or
* an automated system may create governance authority without documented authorization.

---

# 18. Controlling Founder Decision

The Founder hereby establishes the following as the exclusive governance document lifecycle for EquineSync:

**Draft → Approved → Authoritative → Verified**

The four states shall be interpreted as follows:

* **Draft:** under development and not approved;
* **Approved:** substantive content approved for the identified version;
* **Authoritative:** established as the controlling governance source for its defined scope;
* **Verified:** objective evidence demonstrates conformity for a defined verification scope.

All other terms, including merge, activation, implementation, production use, certification, and finding closure, shall be maintained as separate events, statuses, evidence types, or operational attributes.

This Directive supersedes inconsistent lifecycle terminology but does not invalidate prior approvals, repository records, implementation work, production decisions, certifications, or finding dispositions that remain otherwise valid.

---

# 19. Founder Approval Record

**Founder Determination:** APPROVED
**Lifecycle Model:** Draft → Approved → Authoritative → Verified
**Directive Version:** 1.1.0
**Implementation Required:** Yes
**Production Authority Granted:** No
**Automatic Finding Closure Authorized:** No, except under Founder-approved rules satisfying Section 9.5
**Historical Reapproval Required:** No
**Evidence-Based Migration Required:** Yes
**Separate Repository Accession Required for Authoritative Status:** Yes
**Separate Verification Evidence Required for Verified Status:** Yes

---

## Founder Execution

**Founder:** Rian Ray
**Approval Status:** FOUNDER APPROVED
**Execution Date:** 2026-01-23
**Signature or Controlled Approval Record:** Rian Ray

---

## Final Status Upon Signature but Before Accession

**APPROVED**

## Final Status After Successful Accession Under Section 15

**AUTHORITATIVE**
