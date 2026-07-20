# CMT-04 Independent Fourteen-ADR Traceability Review

`NON_AGENT_CONTROLLED_THREAD_REVIEW`

`NOT_ES_RA_AGENT_EVIDENCE`

## 1. Run identity and provenance

| Field | Value |
|---|---|
| Review cycle | `ES-REV-2026-002` |
| Controlled lane | `CMT-04` |
| Runtime identity | Generic Codex controlled non-agent thread; no `ES-RA-*` identity claimed or loaded |
| Thread provenance | Delegated from Codex source thread `019f8104-9235-7f03-8a3e-c68d4b199e09`; lane prompt `CMT-04_PROMPT.md` |
| Operating labels | `NON_AGENT_CONTROLLED_THREAD_REVIEW`; `NOT_ES_RA_AGENT_EVIDENCE` |
| Prompt version | `CMT-04 Controlled Thread Prompt`, 13-line frozen prompt read in full |
| Contract versions | Codex Orchestration Directive `1.0.0`; Common Agent Operating Contract `1.0.0` |
| Runtime | Codex desktop; Darwin `25.5.0` arm64; zsh `5.9` |
| Runtime permission posture | Filesystem capability was broader than lane authority. The lane was logically constrained to read-only frozen inputs and writes only in this CMT-04 output directory. |
| Generated at | `2026-07-20T19:50:39Z` (`2026-07-20T14:50:39-05:00`) |
| Network/application execution | Not used; no application was run |
| Git/frozen-input mutation | None performed |

## 2. Authorization and scope

The controlling lane authorized an independent documentary comparison of all fourteen formal ADRs against Founder decisions and approved recommendations, plus source-authority and cross-domain-contract review. It prohibited consultation of `CMT-02` and `CMT-03`, network use, application execution, Git or frozen-input modification, and any output outside the CMT-04 lane directory. Those boundaries were followed.

No Founder decision, ratification, implementation, execution, PR, merge, tag, release, deployment, or `F-0001` closure is authorized or performed by this report.

## 3. Package identity and integrity

The recorded scope is the 140-file frozen composite at `/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials`:

1. `ES-PIA-IDENTITY-ONBOARDING-V1.1.0-CONTROLLED-REVISION`
2. `ES-ADR-REL-RECOMMENDATIONS-V1.0.0`
3. `ES-REL-CONTROLLED-SEQUENCE-V1.0.0`
4. `ES-PIA-RELATIONSHIPS-DELEGATED-AUTHORITY-V1.1.0-REVISED-CANDIDATE`
5. `ES-REL-PRE-RATIFICATION-COMPLETION-V1.0.0`

All entries in all five package `SHA256SUMS.txt` files verified successfully. The reproducibility digest over the lexically sorted 140 `shasum -a 256` output lines is `20beefc7adf8b8a2ecbed805ebdd634cc47e00b5c537e1f443e7a5fdf4216e40`. This is an inventory digest, not a substitute for the package checksum files.

The Relationships formal ADR bytes in the Controlled Sequence and Pre-Ratification packages are identical by their recorded SHA-256 values. The Pre-Ratification copies were used as the primary formal-text links because that package is the later documentary review assembly; no textual divergence was found.

## 4. Methodology and procedures

1. Read the complete lane prompt and controlling operating documents.
2. Inventoried all frozen materials without consulting `CMT-02` or `CMT-03`.
3. Re-performed all five package checksum validations.
4. Read all seven Identity formal ADRs and all seven Relationships formal ADRs in full.
5. Read all 12 Identity Founder decisions and all 16 Relationships Founder decisions.
6. Read all seven Relationships recommendation documents and the Founder approval-ingestion records.
7. Compared each Relationships formal `Decision` and `Normative Technical Rules` section to the approved recommendation's `Recommended Decision` and `Recommended Technical Parameters`. All fourteen extracted section pairs (seven decisions plus seven rule sets) matched byte-for-byte after heading exclusion.
8. Independently evaluated whether the ADR set actually expresses the Founder-approved directions named in its metadata; titles and traceability rows were not treated as semantic proof.
9. Compared Identity/Relationships/Authorization/Protected Participant contract artifacts and source-reconciliation registers.
10. Searched the entire relevant formal ADR set for allegedly traced controls to distinguish present normative content from a metadata-only reference or a validation-only mention.
11. Classified sources, claims, evidence strength, completeness, reliability, and severities only with the directive taxonomies.

A first read-only extraction command used `$n_FORMAL`, which the shell parsed as the unset variable `n_FORMAL`; it produced invalid empty-input mismatch results. The command did not write any file. It was corrected to `${n}_FORMAL`, rerun, and returned `MATCH` for every Relationships decision and rules pair. Only the corrected result supports this report.

## 5. Scope-denominator accounting

| Denominator | Accounted | Result |
|---|---:|---|
| Formal ADRs | `14/14` | Each has an individual row in `FOURTEEN_ADR_INDEPENDENT_MATRIX.csv` |
| Identity Founder decisions | `12/12` | Collectively checked against the seven Identity ADRs |
| Relationships Founder decisions | `16/16` | Collectively checked against the seven Relationships ADRs |
| Approved Relationships recommendations | `7/7` | Decision and technical-parameter sections independently compared |
| Standalone approved Identity recommendation sources | `0/7 available` | Package asserts approval, but no separately identifiable recommendation text or approval-ingestion mapping is present; recorded as a limitation and finding |
| Cross-domain contract areas | `16/16` | Recorded in `CROSS_DOMAIN_TRACEABILITY.csv` |
| Package checksum sets | `5/5` | All listed files verified |

Detailed procedure status is in `WORK_COMPLETENESS_LEDGER.csv`.

## 6. Overall result

**Disposition:** `NOT_READY_FOR_FINAL_FOUNDER_DISPOSITION`

**Completeness:** `C3_COMPLETE_WITH_LIMITATIONS`

**Reliability:** `R2_INTERNALLY_CHECKED`

**Confidence:** `HIGH` for byte-preservation, inventory, and identified text absences; `MODERATE` for constitutional source-authority conclusions because the frozen packages themselves record missing active paths, hashes, lifecycle proof, and downstream PIAs.

No `P0_CRITICAL` finding was identified. Three `P1_BLOCKING` findings and one `P2_NONBLOCKING` finding are open. The formal ADR sets should not be presented as completely traceable or exactly semantically conformant until the P1 items are remediated and independently re-reviewed.

## 7. Findings

### ES-REV-2026-002-F-0401 — Identity recommendation provenance and decision coverage are incomplete

- **Severity:** `P1_BLOCKING`
- **Lifecycle:** `OPEN`
- **Claim classification:** `SUPPORTED_BY_MULTIPLE_SOURCES`
- **Evidence sufficiency:** `E3`
- **Required disposition:** `FOUNDER_DECISION_REQUIRED`

The Identity package repeatedly states that seven formal ADRs were derived from Founder-approved recommendations, but the frozen materials contain no standalone Identity recommendation documents or approval-ingestion matrix comparable to the Relationships package. The formal ADRs are `DRAFT_CANDIDATE` exact-text proposals pending ratification. Consequently, the lane could not independently verify that new technical mandates—such as a single RP-domain strategy, specific TOTP parameters and step-up windows, opaque server-side sessions, a ten-code recovery set, and other detailed choices—were present in a separately approved recommendation rather than first introduced in the formal draft.

Founder-decision coverage is also incomplete at the formal-ADR layer:

- `IDENTITY-FD-005` invitation security has no formal ADR mapping or substantive formal-ADR text.
- `IDENTITY-FD-001` is only partially represented; invite-only, concierge-assisted pilot and first-external-facility-cohort terms are not encoded.
- `IDENTITY-FD-002` lacks verified-email authentication coverage and the register omits ADR-IDENTITY-003's TOTP relationship.
- `IDENTITY-FD-004` lacks the separate minor identity/account/credentials/attribution rule.
- `IDENTITY-FD-007` lacks reversible mappings and downstream relationship-effect preservation.
- `IDENTITY-FD-009` lacks case linkage, represented principal, purpose, approval, safe notice, and immediate-termination detail.
- `IDENTITY-FD-011` lacks the enumerated closure-history preservation obligations.
- `IDENTITY-FD-012` lacks the complete onboarding completion/evidence rule.

Several Identity register mappings are metadata-only or materially overbroad; for example, ADR-IDENTITY-005 contains no identity-merge, support-access, or account-closure decision even though it maps to `IDENTITY-FD-007`, `IDENTITY-FD-009`, and `IDENTITY-FD-011`.

**Required next action:** provide an immutable, Founder-approved recommendation source for each Identity ADR or relabel unsupported technical details as proposed; then redline the formal ADR set and traceability register so every mapped Founder direction is normatively present or explicitly and accurately delegated to another controlled artifact. Fresh independent review is required before exact-text ratification.

### ES-REV-2026-002-F-0402 — Relationships formal ADRs copy the approved recommendations exactly, but the recommendation/ADR set does not fully encode the Founder decisions

- **Severity:** `P1_BLOCKING`
- **Lifecycle:** `OPEN`
- **Claim classification:** `DETERMINISTICALLY_VERIFIED`
- **Evidence sufficiency:** `E4`
- **Required disposition:** `FOUNDER_DECISION_REQUIRED`

All seven formal Relationships `Decision` sections exactly preserve their recommendation counterparts, and all seven `Normative Technical Rules` sections exactly preserve the approved technical-parameter counterparts. That positive result does not prove that the approved recommendation texts completely encode the higher-authority Founder decisions.

The independent semantic pass found material decision content absent from the complete seven-ADR set:

- `REL-FD-002`: no prohibition on an unqualified generic “barn relationship.”
- `REL-FD-004`: no normative rule separating organization, tenant, facility, location, and program relationships or allowing one organization to operate multiple facilities/programs.
- `REL-FD-006`: no explicit mandatory delegate acceptance before initial activation for duty/access/safety/financial/protected-participant exposure.
- `REL-FD-008`: Care Circle appears only in a validation obligation, not a normative no-authority rule.
- `REL-FD-009`: emergency contact appears only in validation/migration guards, not the notification-priority-only and no-authority rule.
- `REL-FD-012`: public-signup provisional relationship claims and activation checks are absent.
- `REL-FD-015`: emergency/break-glass separation is absent.
- `REL-FD-016`: automatic expiry by default and current-authority revalidation for renewal are absent; only high-risk no-silent-renewal and fresh acceptance on material change are present.

`REL-FD-003`, `REL-FD-007`, and `REL-FD-011` are only partially explicit: the exact ownership/custody state set, independent concurrent scopes, and prospective-termination preservation terms are distributed or under-specified.

The frozen `ADR_RECOMMENDATION_TO_FORMAL_ADR_CONFORMANCE_MATRIX.csv` therefore supports exact recommendation-to-formal copying but overstates end-to-end Founder-decision conformance with `EXACTLY_ALIGNED` and zero missing parameters.

**Required next action:** preserve the exact approved recommendation history, issue a controlled redline or supplemental formal authority that explicitly carries the omitted Founder directions, correct the conformance and decision-traceability matrices, and obtain fresh review before Founder ratification.

### ES-REV-2026-002-F-0403 — Source authority and cross-domain contract closure remain incomplete

- **Severity:** `P1_BLOCKING`
- **Lifecycle:** `OPEN`
- **Claim classification:** `SUPPORTED_BY_MULTIPLE_SOURCES`
- **Evidence sufficiency:** `E3`

The Identity package verifies exact path/hash/lifecycle for 2 of 12 reconciliation sources; the Relationships package reports 4 of 16 fully verified. Authorization, Agreement/Consent, Safeguarding/Protected Participant, Horse/Transfer, Facility/Business, Audit/Evidence, Communication/Notice, Privacy, PIA-standard bytes, and repository PIA bytes remain partially reconciled, absent, or blocked. The Relationships cross-domain register has proposed, partially aligned, or blocked status for every one of its 12 rows; none is approved and closed.

The two Identity-to-Relationships contract copies are textually identical except for status metadata, and the ADR ownership boundaries are substantively consistent. This establishes documentary compatibility, not approved contract closure. The missing authorities prevent complete source-authority verification and block any claim that the fourteen ADRs are fully cross-domain closed.

**Required next action:** close the exact source identities and lifecycle evidence, approve the affected PIAs/contracts, map each material ADR clause to the controlling source, and rerun this lane against the new frozen package.

### ES-REV-2026-002-F-0404 — Frozen status metadata contains unresolved drift

- **Severity:** `P2_NONBLOCKING`
- **Lifecycle:** `OPEN`
- **Claim classification:** `DIRECTLY_OBSERVED`
- **Evidence sufficiency:** `E4`

The Relationships Pre-Ratification package contains `FOUNDER_DECISION_REGISTER.csv` rows marked `PENDING`, while the same package's formal ADR headers and decision-traceability file state Founder approval, and the Controlled Sequence contains an explicit Founder approval-ingestion record. The pending register is resolvable as `HISTORICAL_OR_SUPERSEDED`, but the package does not label it that way.

The Identity PIA likewise retains stale phrases such as “Twelve proposed Founder decisions,” an incomplete V1.1.0 change-control history, and older findings language alongside the approved package status. These do not overturn the more specific approval records, but they weaken source-authority clarity.

**Required next action:** mark retained pending registers as historical/superseded or replace them in a new version, reconcile status prose and change history, regenerate checksums/manifests, and rerun structural validation.

## 8. Positive conclusions and claim-to-evidence links

1. **All 140 frozen files were present and all five checksum sets passed.** Classification: `DETERMINISTICALLY_VERIFIED`; strength: `E4`; confidence: `HIGH`. Evidence: [Identity checksums](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/SHA256SUMS.txt), [Relationships recommendation checksums](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_ADR_Recommendations_V1_0_0/SHA256SUMS.txt), [Controlled Sequence checksums](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Controlled_Sequence_V1_0_0/SHA256SUMS.txt), [Relationships candidate checksums](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Delegated_Authority_PIA_V1_1_0_Revised_Candidate/SHA256SUMS.txt), [Pre-Ratification checksums](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0/SHA256SUMS.txt).
2. **All seven Relationships formal decisions and all seven normative-rule sets match the corresponding approved recommendation text.** Classification: `DETERMINISTICALLY_VERIFIED`; strength: `E4`; confidence: `HIGH`. Evidence: [Recommendations package](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_ADR_Recommendations_V1_0_0), [formal ADR package](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0), [approval ingestion](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Controlled_Sequence_V1_0_0/ADR_RECOMMENDATION_APPROVAL_INGESTION.csv).
3. **No formal ADR claims implementation authorization, final ratification, production readiness, or external assurance.** Classification: `DIRECTLY_OBSERVED`; strength: `E4`; confidence: `HIGH`. Evidence: [Identity formal register](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/FORMAL_ADR_REGISTER.csv), [Relationships formal register](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Controlled_Sequence_V1_0_0/FORMAL_ADR_REGISTER.csv).
4. **Identity and Relationships agree on the central ownership boundary:** Identity owns canonical identity/account/principal/assurance/session facts; Relationships owns relationship/delegation facts; Authorization owns final decisions; Agreement owns execution/consent; Claims owns adjudication; protective domains may narrow effects; Audit owns reconstruction. Classification: `SUPPORTED_BY_MULTIPLE_SOURCES`; strength: `E3`; confidence: `HIGH` for documentary consistency. Evidence: [Identity-to-Relationships contract](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/IDENTITY_RELATIONSHIPS_CONTRACT.md), [Relationships-to-Authorization contract](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0/RELATIONSHIPS_AUTHORIZATION_CONTRACT.md).

## 9. Source-authority classification

| Source family | Directive classification | Use in this lane |
|---|---|---|
| Identity Founder decision register | `FOUNDER_DECISION` | Exact approved Identity directions |
| Relationships approval-ingestion record and CSV | `FOUNDER_DECISION` | Exact approved Relationships directions and recommendation approval |
| Relationships recommendation documents before approval | `DRAFT_CANDIDATE` | Recommendation text; authority supplied by approval-ingestion record |
| Fourteen formal ADRs | `DRAFT_CANDIDATE` | Proposed exact wording pending final ratification |
| Founder-approved PIA design statements | `FOUNDER_DECISION` | Design authority only; no implementation authority |
| Pre-agent review reports and conformance matrices | `NONAUTHORITATIVE_COMMENTARY` | Corroborative inputs only; conclusions were independently re-performed |
| Stale `PENDING` register rows after approval | `HISTORICAL_OR_SUPERSEDED` | Must not override later explicit approval records |
| Unresolved active canon paths/hashes/lifecycles and absent PIAs | `MISSING_REQUIRED_SOURCE` | Material limitation and P1 gate |

No lower-authority draft or commentary was used to override a Founder decision.

## 10. Assumptions, contradictions, blocked and untested areas

- The frozen directory is treated as the complete authorized evidence universe for this lane. No repository or conversation evidence outside it was used for substantive conclusions.
- The Founder approval-ingestion record is treated as the controlling decision record for Relationships. The referenced “controlling conversation” itself was not present in the frozen materials, so authenticity beyond the package checksum is not independently re-performed.
- No separately identifiable Identity recommendation text was available; recommendation conformance is therefore `UNKNOWN`, not presumed.
- Source-reconciliation gaps recorded by the packages were not closed by external repository inspection because the lane prohibited evidence outside the frozen materials.
- No application, executable test, schema, repository implementation, environment, migration, rollback, or operational workflow was tested. Those matters are `NOT_TESTED`.
- No legal, security, privacy, safeguarding, or professional assurance is provided.

## 11. Required next actions

1. Remediate `ES-REV-2026-002-F-0401` and `ES-REV-2026-002-F-0402` through controlled redlines/new package version; do not edit this frozen evidence set.
2. Reconcile and approve the missing cross-domain sources/contracts identified in `ES-REV-2026-002-F-0403` to the gate required by the intended Founder disposition.
3. Correct status metadata drift from `ES-REV-2026-002-F-0404` in the successor package.
4. Freeze the successor package with new manifests/checksums and provide affected-reviewer notice.
5. Run fresh independent semantic, source-authority, and cross-domain review. Only the Founder may decide ratification or any later authorization.

## 12. Mandatory self-audit

| Question | Answer |
|---|---|
| Did I remain within role? | Yes. Generic CMT-04 non-agent review only; no `ES-RA-*` claim. |
| Did I review the correct package? | Yes. The 140-file frozen composite and its five package identities were recorded and checksum-verified. |
| Is every assigned item accounted for? | Yes, with the missing Identity recommendation provenance recorded as `COMPLETED_WITH_LIMITATION`. |
| Did I confuse a claim with evidence? | No. Pre-agent conclusions were treated as `NONAUTHORITATIVE_COMMENTARY`; material conclusions link to primary frozen text. |
| Did I overstate verification? | No. Byte preservation, documentary semantics, and source limitations are separated. |
| Did I disclose assumptions and conflicts? | Yes. |
| Did I disclose exclusions, sampling, and untested areas? | Yes. No sampling was used for the fourteen ADRs; executable behavior was not tested. |
| Are closure or pass criteria objective? | Yes. P1 remediation requires explicit normative text, corrected mappings, closed source references, a new frozen package, and fresh review. |
| Did I accidentally approve, waive, or accept risk? | No. |
| Can another reviewer reproduce the method? | Yes, using the evidence links, matrices, extraction boundaries, checksum files, and ledger. |
| Do all evidence and output references resolve? | Validated at submission; see `OUTPUT_MANIFEST.json`. |
| What could invalidate this result? | Frozen-input drift, missing or false approval evidence, a different controlling source lifecycle, unrecorded Founder changes, or defects in the text-extraction/semantic review. |

## 13. Completion Attestation

> I completed the procedures identified in the Work Completeness Ledger for the recorded scope. This attestation does not constitute Founder approval, external assurance, legal certification, or proof that undiscovered defects do not exist.

## 14. What This Work Did Not Establish

This work did not establish final ADR ratification, constitutional adoption or lock, implementation authorization, as-built conformance, executable correctness, security effectiveness, operational readiness, enrollment readiness, release readiness, production readiness, deployment authority, or `F-0001` closure. “No P0 identified” means only that no P0 was found within the recorded documentary scope and procedures.

## 15. Output manifest

The authoritative SHA-256 hashes and byte sizes for this report and the three CSV outputs are recorded in `OUTPUT_MANIFEST.json`; that file also records a normalized self-hash. Required outputs:

- `LANE_REPORT.md`
- `FOURTEEN_ADR_INDEPENDENT_MATRIX.csv`
- `CROSS_DOMAIN_TRACEABILITY.csv`
- `WORK_COMPLETENESS_LEDGER.csv`
- `OUTPUT_MANIFEST.json`

