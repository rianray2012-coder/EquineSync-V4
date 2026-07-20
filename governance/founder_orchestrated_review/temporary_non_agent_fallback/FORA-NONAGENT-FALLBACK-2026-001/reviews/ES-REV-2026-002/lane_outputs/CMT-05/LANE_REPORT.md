# CMT-05 Blind First-Pass Adversarial Challenge

`NON_AGENT_CONTROLLED_THREAD_REVIEW`

`NOT_ES_RA_AGENT_EVIDENCE`

## Review result

`P1_DOCUMENTARY_GAPS_PRESENT_EXACT_TEXT_RATIFICATION_SHOULD_REMAIN_PENDING`

No P0 was identified. Five P1 documentary gaps and three P2 documentary gaps were identified. This is a lane review result only. It is not a Founder decision, ratification, implementation authorization, execution authorization, baseline freeze, release decision, deployment decision, or F-0001 closure.

## Provenance and control boundary

| Field | Value |
|---|---|
| Lane | `CMT-05` |
| Directive classification | `NON_AGENT_CONTROLLED_THREAD_REVIEW` |
| Evidence classification | `NOT_ES_RA_AGENT_EVIDENCE` |
| Runtime | Generic controlled Codex desktop thread; no ES-RA custom-agent identity claimed or loaded |
| Source delegation thread ID | `019f8104-9235-7f03-8a3e-c68d4b199e09` |
| Review ID | `ES-REV-2026-002` |
| Input boundary | Frozen read-only materials at `/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials` only |
| Output boundary | This CMT-05 lane-output directory only |
| Started/completed | `2026-07-20T19:49:08Z` / `2026-07-20T19:51:35Z` |
| Local completion time | `2026-07-20T14:51:35-0500 CDT` |

Result scope classifications are limited to `DOCUMENTARY_GAP` and `IMPLEMENTATION_CONCERN_OUTSIDE_SCOPE`. Finding severity uses only `P0`, `P1`, and `P2`.

## Integrity and intake

- Inventoried 140 frozen files across five packages.
- Verified all 130 artifacts listed by the five package `SHA256SUMS.txt` files: 130/130 passed.
- Parsed every JSON input successfully.
- Parsed every CSV input successfully.
- Exact active-token scan found `MAIP` 0 times and `MIAP` 62 times.
- No network access, application execution, Git mutation, frozen-input mutation, other-lane-output inspection, or proposed-redline inspection occurred.

## Findings

### CMT05-F-001 — P1 — disputed source authority is not unambiguously fail-closed

Classification: `DOCUMENTARY_GAP`

The Founder-approved direction requires fail-closed invalidation when any required delegation source becomes inactive or disputed. Formal ADR-REL-003 instead permits a dependent grant to become ineligible **or** enter a protective restricted state. Elsewhere, a restriction is defined as a limitation that does not necessarily eliminate all effect. That alternative is therefore not demonstrably equivalent to fail-closed invalidation and can preserve residual authority unless the restricted state is explicitly non-authorizing.

Evidence:

- [Founder-approved REL-FD-014](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Controlled_Sequence_V1_0_0/FOUNDER_DECISION_APPROVAL_INGESTION.csv:15)
- [ADR-REL-003 disputed-source treatment](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0/ADR-REL-003_FORMAL.md:43)
- [Restriction definition](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Delegated_Authority_PIA_V1_1_0_Revised_Candidate/PIA_RELATIONSHIPS_DELEGATED_AUTHORITY_V1_1_0.md:204)
- [Conformance claim of exact alignment](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0/ADR_RECOMMENDATION_TO_FORMAL_ADR_CONFORMANCE_MATRIX.csv:4)

Required documentary disposition: define the disputed-source protective state as non-authorizing for every dependent grant effect unless a separately approved independent source is revalidated; then reassess the `EXACTLY_ALIGNED` claim.

### CMT05-F-002 — P1 — recovery completion authority and lifecycle are absent from the controlling matrices

Classification: `DOCUMENTARY_GAP`

Account recovery is required for first-user enrollment, and manual review may restore bounded access. The PIA calls `RecoveryCase` a material state model, but `STATE_TRANSITION_MATRIX.csv` contains no RecoveryCase transitions and `PERMISSION_MATRIX.csv` identifies neither the actor allowed to complete manual recovery nor the boundary of that completion authority. The same omission affects the transition from compromised/restricted access back to usable access. The documentary package therefore does not yet define who may restore access, under which preconditions, or which post-recovery capabilities remain blocked.

Evidence:

- [Recovery is a material state model](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/PIA_IDENTITY_ACCOUNT_ACTOR_ENROLLMENT_ONBOARDING_V1_1_0.md:442)
- [Identity state matrix ends without RecoveryCase transitions](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/STATE_TRANSITION_MATRIX.csv:1)
- [Identity permission matrix omits recovery completion authority](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/PERMISSION_MATRIX.csv:1)
- [ADR-IDENTITY-005 manual recovery capability](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/ADR-IDENTITY-005_FORMAL.md:15)
- [First-user recovery requirement](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/REQUIREMENT_REGISTER.csv:27)

Required documentary disposition: enumerate RecoveryCase states, authorized initiators/reviewers/completers, evidence and segregation requirements, expiry/failure/compromise paths, and the exact bounded post-recovery capability envelope.

### CMT05-F-003 — P1 — protected-participant account requirements contradict the workflow and contract

Classification: `DOCUMENTARY_GAP`

The approved direction and normative requirement say every minor uses a separate account and credentials. The first-user workflow makes the minor account optional, while the proposed protected-participant contract weakens the rule to “ordinarily” separate. These statements cannot all control the same first-user flow. The ambiguity creates a path to guardian/minor account collapse even though the tests expect separate accounts.

Evidence:

- [Founder-approved separate-account direction](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/FOUNDER_DECISION_REGISTER.csv:5)
- [Normative separate-account requirement](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/REQUIREMENT_REGISTER.csv:18)
- [First-user workflow makes the minor account optional](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/WORKFLOW_REGISTER.csv:5)
- [Proposed contract says ordinarily separate](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/IDENTITY_PROTECTED_PARTICIPANT_CONTRACT.md:5)
- [Test expects separate identities and accounts](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/TEST_MATRIX.csv:12)

Required documentary disposition: establish one controlling rule for minor accounts and credentials, and align the workflow, contract, acceptance criteria, tests, and transition behavior to it.

### CMT05-F-004 — P1 — canonical `VERIFIED` relationship state conflicts with claim-specific verification

Classification: `DOCUMENTARY_GAP`

ADR-REL-004 requires distinct VerificationAssessment records and rejects a universal authoritative `verified` flag. The relationship transition matrix nevertheless transitions the canonical Relationship aggregate to `VERIFIED`, and the requirements separately list verified as a relationship lifecycle state. Without an explicit purpose-qualified projection rule, that state can become the universal trust badge the ADR prohibits.

Evidence:

- [ADR-REL-004 separates verification assessments and rejects universal verified](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0/ADR-REL-004_FORMAL.md:25)
- [Canonical Relationship transition to VERIFIED](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Delegated_Authority_PIA_V1_1_0_Revised_Candidate/STATE_TRANSITION_MATRIX.csv:5)
- [Requirement treats verified as relationship state](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Delegated_Authority_PIA_V1_1_0_Revised_Candidate/REQUIREMENT_REGISTER.csv:5)
- [Purpose-specific verification requirement](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Delegated_Authority_PIA_V1_1_0_Revised_Candidate/REQUIREMENT_REGISTER.csv:56)

Required documentary disposition: make verification a claim/evidence/purpose/time-scoped assessment or computed projection, not an unqualified canonical Relationship lifecycle state.

### CMT05-F-005 — P1 — first-user traceability claims are mechanically incomplete

Classification: `DOCUMENTARY_GAP`

Both PIAs require every first-user requirement to map to acceptance criteria, tests, and evidence. A deterministic join from each `REQUIREMENT_REGISTER.csv` to its `ACCEPTANCE_CRITERIA.csv` shows only 24 of 36 Identity first-user requirements and 32 of 47 Relationships first-user requirements have an explicit acceptance-criterion link. Twelve Identity and fifteen Relationships requirements are unmapped at the first link, so the full AC-test-evidence chain cannot exist as claimed.

Unmapped Identity IDs: `IDENTITY-REQ-002`, `003`, `008`, `012`, `015`, `019`, `024`, `030`, `035`, `036`, `037`, `043`.

Unmapped Relationships IDs: `REL-REQ-005`, `006`, `009`, `013`, `015`, `020`, `021`, `030`, `031`, `034`, `038`, `040`, `048`, `056`, `066`.

Evidence:

- [Identity traceability requirement](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/REQUIREMENT_REGISTER.csv:47)
- [Identity acceptance-criterion register](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/ACCEPTANCE_CRITERIA.csv:1)
- [Relationships traceability requirement](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Delegated_Authority_PIA_V1_1_0_Revised_Candidate/REQUIREMENT_REGISTER.csv:50)
- [Relationships acceptance-criterion register](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Delegated_Authority_PIA_V1_1_0_Revised_Candidate/ACCEPTANCE_CRITERIA.csv:1)

Required documentary disposition: add explicit AC-test-evidence links for every first-user requirement or narrow the traceability claim and gate accordingly.

### CMT05-F-006 — P2 — formal representation ownership wording exceeds the approved boundary wording

Classification: `DOCUMENTARY_GAP`

The approved ADR recommendation says Identity owns canonical actors and principals. The formal ADR adds that Identity owns “representation truth,” while the cross-domain contract separates the represented-principal context supplied by Identity from relationship capacity and source-authority facts supplied by Relationships. “Representation truth” is not qualified as session context only and may absorb the external authority basis into Identity. This is a wording-level boundary ambiguity, not evidence that an implementation currently merges the domains.

Evidence:

- [Approved recommendation boundary](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_ADR_Recommendations_V1_0_0/ADR-REL-001.md:23)
- [Formal ADR adds representation truth ownership](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0/ADR-REL-001_FORMAL.md:52)
- [Contract separates represented context from relationship authority facts](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0/IDENTITY_RELATIONSHIPS_CONTRACT.md:6)
- [Identity RepresentationContext limits legal basis ownership](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/DATA_ENTITY_REGISTER.csv:21)

Required documentary disposition: qualify Identity ownership as the selected and attributed representation context while preserving relationship/agreement ownership of the validity and source-authority basis.

### CMT05-F-007 — P2 — automated actor accountability is classified later than workflows that use automation

Classification: `DOCUMENTARY_GAP`

The accountable-human-owner requirement for every service account, integration account, scheduled process, or AI actor is classified only for general production. The first-user design already relies on system actors and scheduled jobs for invitation expiry, recovery expiry, reminders, transition checks, and other state changes. This creates a release-classification seam where automated actions may exist before their accountable-human-owner control is a gate.

Evidence:

- [Accountable-human-owner requirement classified for general production](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/REQUIREMENT_REGISTER.csv:33)
- [System, scheduled-process, and AI actors](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/PIA_IDENTITY_ACCOUNT_ACTOR_ENROLLMENT_ONBOARDING_V1_1_0.md:240)
- [Scheduled jobs used by enrollment and recovery](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/PIA_IDENTITY_ACCOUNT_ACTOR_ENROLLMENT_ONBOARDING_V1_1_0.md:575)

Required documentary disposition: make accountable ownership a prerequisite whenever automation participates, including first-user workflows, and add corresponding actor lifecycle/transition coverage.

### CMT05-F-008 — P2 — the pre-ratification package carries contradictory PIA status surfaces

Classification: `DOCUMENTARY_GAP`

The pre-ratification package embeds a PIA whose header and baseline table still say revised candidate, pending Founder decisions, and not approved. The same frozen package reports the PIA as Founder-approved design, and the controlled-sequence approval record supports that later status. The addendum explains why the old PIA bytes were not rewritten, but the embedded PIA has no visible superseded-status banner. A reader can therefore derive two different current statuses from the same review set.

Evidence:

- [Embedded PIA stale status surface](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0/PIA_RELATIONSHIPS_DELEGATED_AUTHORITY_V1_1_0.md:3)
- [Pre-ratification current status](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0/PRE_RATIFICATION_STATUS.json:2)
- [Founder approval ingestion result](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Controlled_Sequence_V1_0_0/FOUNDER_APPROVAL_INGESTION_RECORD.md:13)
- [Addendum explains non-rewrite treatment](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Controlled_Sequence_V1_0_0/PIA_V1_1_0_APPROVAL_AND_ADR_INTEGRATION_ADDENDUM.md:45)

Required documentary disposition: add an unmistakable package-level status precedence rule or controlled successor wrapper so the stale embedded header cannot be mistaken for current status.

## Required-theme challenge coverage

| Theme | Documentary outcome | Finding or controlling evidence |
|---|---|---|
| Authority inflation | `GAP` | CMT05-F-001; CMT05-F-006 |
| Identity/relationship merge | `CONTROL_PRESENT_WITH_BOUNDARY_AMBIGUITY` | Automatic merges are prohibited; CMT05-F-006 remains |
| Recovery authority | `GAP` | CMT05-F-002 |
| Hidden human actor | `GAP` | CMT05-F-007 |
| Delegation excess | `GAP` | Scope/chain controls are strong, but CMT05-F-001 weakens disputed-source handling |
| Cycles | `CONTROL_PRESENT` | ADR-REL-003 requires pre-activation cycle detection and bounded depth |
| Stale revocation | `CONTROL_PRESENT_DOCUMENTARY_ONLY` | Watermarks and fan-out are specified; no runtime evidence was reviewed |
| Offline risk | `CONTROL_PRESENT_DOCUMENTARY_ONLY` | Offline authority remains proposal-only and is revalidated online |
| Guardian inflation | `CONTROL_PRESENT_WITH_ACCOUNT_CONTRADICTION` | Payment/contact cannot create guardian authority; CMT05-F-003 remains |
| Privacy enumeration | `CONTROL_PRESENT_DOCUMENTARY_ONLY` | Purpose-specific projections and no unauthorized existence signal are specified |
| Universal verification | `GAP` | CMT05-F-004 |
| Unsafe migration | `CONTROL_PRESENT_DOCUMENTARY_ONLY` | Additive migration, lineage, quarantine, and no silent authority conversion are specified |
| `MAIP` drift | `CONTROL_PRESENT` | Exact-token count: 0 |
| `MIAP` drift | `CONTROL_PRESENT_WITH_REGISTERED_DEPENDENCY` | Exact-token count: 62; exact package registration/reconciliation remains openly pending |
| First-user traceability | `GAP` | CMT05-F-005 |

## Implementation concerns outside scope

The frozen materials already record that repository as-built reconciliation, executable tests, revocation infrastructure, operational tooling, rollback evidence, and enrollment evidence do not exist. Those are `IMPLEMENTATION_CONCERN_OUTSIDE_SCOPE` for this documentary lane. They were not converted into new wording findings, tested by running the application, or treated as closed.

Evidence:

- [Relationships open implementation findings](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Relationships_Pre_Ratification_Completion_V1_0_0/OPEN_FINDINGS_REGISTER.csv:2)
- [Identity open implementation findings](/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision/OPEN_FINDINGS_REGISTER.csv:2)

## Limitations

- Documentary review only; no application, repository implementation, environment, provider, database, or runtime behavior was inspected or executed.
- No network or external legal/technical assurance was used.
- No other review-lane output or proposed redline was inspected.
- Evidence links point only to the frozen review materials.
- Passing a documentary challenge means a control is stated, not that it is implemented or effective.

## Self-audit

- [x] Complete controlling lane prompt read before review.
- [x] Generic controlled non-agent identity preserved.
- [x] Both required labels included.
- [x] Frozen input boundary preserved.
- [x] No other lane output or proposed redline inspected.
- [x] No network use or application execution.
- [x] No Git or frozen-input mutation.
- [x] P0/P1/P2 severity vocabulary only.
- [x] Documentary gaps separated from implementation concerns outside scope.
- [x] No remediation implementation, Founder decision, ratification, execution, PR, merge, tag, release, deployment, or F-0001 closure performed.
- [x] Four authorized output files only; output hashes recorded in `OUTPUT_MANIFEST.json`.

## Completion attestation

`COMPLETE_FOR_CMT_05_BLIND_FIRST_PASS_DOCUMENTARY_SCOPE`

This attests only that the directed CMT-05 documentary challenge and its required output set were completed. It does not attest implementation conformity, security effectiveness, operational readiness, enrollment readiness, or governance closure.
