# CMT-02 Identity Domain Review

NON_AGENT_CONTROLLED_THREAD_REVIEW

NOT_ES_RA_AGENT_EVIDENCE

## Control and provenance

- Lane: CMT-02
- Review cycle: ES-REV-2026-002
- Directive: ES-FORA-DIR-CMT-IDENTITY-RELATIONSHIPS-REVIEW-V1.0
- Current thread ID: 019f810e-dcbb-7d03-bfdf-86a83e880a39
- Delegating source thread ID: 019f8104-9235-7f03-8a3e-c68d4b199e09
- Runtime visible to lane: Codex desktop generic controlled thread; GPT-5 family; exact model selector not exposed
- Host visible to lane: Darwin 25.5.0 arm64; zsh 5.9
- Observed review start UTC: 2026-07-20T19:48:31Z
- Report generated UTC: 2026-07-20T19:50:46Z
- Input root: /Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials/EquineSync_Identity_Account_Actor_Enrollment_Onboarding_PIA_V1_1_0_Controlled_Revision
- Output root: /Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/EquineSync-V4-controlled-review/governance/founder_orchestrated_review/temporary_non_agent_fallback/FORA-NONAGENT-FALLBACK-2026-001/reviews/ES-REV-2026-002/lane_outputs/CMT-02

This lane is a generic non-agent review. It did not claim, load, or execute an ES-RA custom-agent identity.

## Outcome

Identity PIA V1.1.0 and ADR-IDENTITY-001 through ADR-IDENTITY-007 are not ready for Founder ratification in their current exact text. The lane found 2 open P0 findings, 15 open P1 findings, and 1 open P2 finding. The directive prohibits a ratification-ready recommendation while any P0 or P1 remains open.

The core design direction is substantially coherent: provider neutrality, authentication/authorization separation, no automatic identity merge, bounded recovery, attributed support, public-signup provisionality, preserved history, MIAP placement, and protected-account transition are present. Ratification is blocked by two control weakenings, incomplete Founder-decision-to-ADR semantics, material ADR additions not traceable to an approved decision, stale source/status statements, and incomplete cross-domain contract controls.

Lane disposition: CMT02_IDENTITY_REQUIRES_BOUNDED_REMEDIATION_BEFORE_FOUNDER_RATIFICATION.

This is a lane recommendation only. It is not Founder approval, adoption, ratification, lock, waiver, risk acceptance, baseline freeze, implementation authority, execution authority, production readiness, enrollment readiness, or F-0001 closure.

## Input integrity and procedure

The lane:

1. Read the complete CMT-02 controlling prompt and the directive vocabulary.
2. Limited semantic review to the authorized Identity controlled-revision package and supplied review controls.
3. Verified SHA256SUMS.txt against all 37 listed package files; result 37/37 OK.
4. Reviewed the PIA, all 12 Founder decisions, all 7 formal ADRs, all 3 cross-domain contracts, MIAP confirmation, source registers, requirements, workflows, permissions, states, acceptance criteria, tests, golden paths, risks, validation, disposition, and freeze/authorization prechecks.
5. Did not read another lane's output.
6. Did not use network, connectors, application runtime, Git mutation, provider activity, or production credentials.
7. Did not modify frozen inputs.

## Open findings

| Finding | Severity | Classification | Claim and evidence | Ratification effect |
|---|---|---|---|---|
| CMT02-F-001 | P0 | CONTROL_WEAKENING | FD-004 requires every minor to retain a separate account and credentials, and REQ-017 says guardians and minors shall use separate accounts and credentials. WF-004 and GP-003 instead make the minor account optional, while the Protected Participant contract says ordinarily separate. Evidence: FOUNDER_DECISION_REGISTER.csv:5; REQUIREMENT_REGISTER.csv:18; WORKFLOW_REGISTER.csv:5; GOLDEN_PATHS.md:55-59; IDENTITY_PROTECTED_PARTICIPANT_CONTRACT.md:5. | Safeguarding control is weakened; exact text cannot be ratified. |
| CMT02-F-002 | P0 | CONTROL_WEAKENING | FD-006 requires high-risk actions to remain restricted until step-up, risk checks, or manual review completes. Authorization contract invariant 3 permits resulting recovery assurance whenever policy explicitly accepts it, without preserving one of those additional conditions. Evidence: FOUNDER_DECISION_REGISTER.csv:7; IDENTITY_AUTHORIZATION_CONTRACT.md:27; ADR-IDENTITY-005_FORMAL.md:17; TEST_MATRIX.csv:19. | Recovery can become an authority bypass; exact contract cannot be ratified. |
| CMT02-F-003 | P1 | MISSING_TRACEABILITY | FD-005 has no formal ADR mapping, and no ADR carries its full invitation controls: single-use, revocable, purpose-bound, recipient-bound where feasible, short-lived, and stricter privileged-invitation controls. Evidence: FOUNDER_DECISION_REGISTER.csv:6; FORMAL_ADR_REGISTER.csv:2-8; ADR-IDENTITY-006_FORMAL.md:19-25. | Founder-approved invitation semantics are absent from the formal ADR set. |
| CMT02-F-004 | P1 | MISSING_TRACEABILITY | Registered mappings overstate or omit exact semantic coverage: FD-002 verified-email/TOTP coverage is fragmented; FD-004 initial minor-account controls are not in ADR-007; FD-009 case, purpose, approval, notice, and immediate-termination terms are incomplete; FD-011 preservation categories are incomplete; FD-012 completion prerequisites are not stated in ADR-006. ADR-001 cites FD-008 without public-signup semantics, and ADR-005 cites FD-007, FD-009, and FD-011 without full corresponding rules. Evidence: FOUNDER_DECISION_REGISTER.csv:3,5,8-10,12-13; FORMAL_ADR_REGISTER.csv:2-8; ADR files decision and normative sections. | Formal ADR traceability is not exact enough for ratification. |
| CMT02-F-005 | P1 | MATERIAL_ADDITION_REQUIRING_FOUNDER_DECISION | ADR-002 adds a single governed relying-party domain strategy and attestation defaults not stated in FD-002 or FD-003. Evidence: ADR-IDENTITY-002_FORMAL.md:15-17,44-49; FOUNDER_DECISION_REGISTER.csv:3-4. | Retain as proposed material for explicit ratification or move to open implementation parameters. |
| CMT02-F-006 | P1 | MATERIAL_ADDITION_REQUIRING_FOUNDER_DECISION | ADR-003 adds ES-AAL1/2/3, fixed TOTP characteristics, and five/fifteen-minute step-up recommendations beyond the recorded Founder decisions. Evidence: ADR-IDENTITY-003_FORMAL.md:15-17,44-49; FOUNDER_DECISION_REGISTER.csv:4,7. | Exact added policy must be expressly decided or made non-normative. |
| CMT02-F-007 | P1 | MATERIAL_ADDITION_REQUIRING_FOUNDER_DECISION | ADR-004 selects opaque web sessions and a native-client token/refresh architecture although the cited decisions establish controls, not this platform architecture. Evidence: ADR-IDENTITY-004_FORMAL.md:15-17,45-50; FOUNDER_DECISION_REGISTER.csv:4,7,10,12. | Exact architecture needs an explicit Founder decision/source or open-parameter treatment. |
| CMT02-F-008 | P1 | MATERIAL_ADDITION_REQUIRING_FOUNDER_DECISION | ADR-005 selects an ordered recovery hierarchy and exactly ten recovery codes; FD-006 approves bounded recovery but not those choices. Evidence: ADR-IDENTITY-005_FORMAL.md:15-17,45-50; FOUNDER_DECISION_REGISTER.csv:7. | Exact recovery mechanism/count requires express decision or parameterization. |
| CMT02-F-009 | P1 | CROSS_DOMAIN_CONFLICT | ADR-006 defaults multi-location trainers to one organization across locations unless isolation conditions require separate tenancy. Organization/tenancy topology implicates Business, Facility, Relationships, Authorization, Privacy, and contractual owners outside Identity. Evidence: ADR-IDENTITY-006_FORMAL.md:17,27-34; PIA lines 185-212; FOUNDER_DECISION_REGISTER.csv:9. | Remove the topology default or ratify it through the owning domains. |
| CMT02-F-010 | P1 | AMBIGUOUS_REQUIRES_REMEDIATION | ADR-007 lists a maximum paused-case duration as an implementation parameter without stating that time alone can never auto-complete an exception. FD-010 requires exceptions to pause automatic transition. Evidence: ADR-IDENTITY-007_FORMAL.md:17,45-50; FOUNDER_DECISION_REGISTER.csv:11. | Clarify escalation timing cannot terminate a protective hold. |
| CMT02-F-011 | P1 | SOURCE_GAP | Each ADR references the PIA and Founder decisions but lacks exact controlling source locators, hashes, lifecycle status, and unresolved-source disclosure. Evidence: ADR-IDENTITY-001 through ADR-IDENTITY-007 lines 3-11; SOURCE_RECONCILIATION_REPORT.md:12-19. | Source authority cannot be independently reconstructed from each exact ADR. |
| CMT02-F-012 | P1 | SOURCE_GAP | SOURCE_REGISTER.csv still says Identity and Relationships exact sources require verification and MIAP placement is unresolved, while SOURCE_RECONCILIATION_REGISTER.csv and MIAP confirmation say those matters are verified/resolved. DEP-003 also describes the Relationship PIA as absent although a local Founder-approved package is registered. Evidence: SOURCE_REGISTER.csv:4,6,18; SOURCE_RECONCILIATION_REGISTER.csv:2-3,12-13; MIAP_TERMINOLOGY_AND_AUTHORITY_CONFIRMATION.md:3-7; DEPENDENCY_REGISTER.csv:4. | Contradictory source/lifecycle truth blocks exact ratification provenance. |
| CMT02-F-013 | P1 | AMBIGUOUS_REQUIRES_REMEDIATION | The PIA status is Founder-approved design, but active text calls decisions proposed, refers to proposed decisions for MFA and rollout, says machine validation precedes Founder design approval, calls the package a draft, and omits the V1.1.0 change-history entry. Evidence: PIA lines 5,31,683,1023,1078,1127-1132,1149,1181-1183. | Lifecycle and approval semantics are internally inconsistent. |
| CMT02-F-014 | P1 | MISSING_TRACEABILITY | The state/event model omits IdentityMerge reversal despite FD-007/REQ-027 and a ReverseIdentityMerge command; it omits ProtectedAccountTransitionCase state transitions and an accepted invitation terminal transition. Evidence: PIA lines 438-452,525-584; STATE_TRANSITION_MATRIX.csv:2-30; FOUNDER_DECISION_REGISTER.csv:8,11; REQUIREMENT_REGISTER.csv:28. | Formal lifecycle behavior is incomplete. |
| CMT02-F-015 | P1 | AMBIGUOUS_REQUIRES_REMEDIATION | PERM-001 and PERM-003 mark Audit Required as No while their evidence fields require recorded requests/acceptance events and REQ-044 requires all material identity lifecycle events to be attributable. Evidence: PERMISSION_MATRIX.csv:2,4; REQUIREMENT_REGISTER.csv:45; PIA lines 549-573. | Audit obligation is contradictory and must be made normative. |
| CMT02-F-016 | P1 | CONTROL_WEAKENING | The Authorization contract says Authorization decides whether stale identity or session facts must be denied rather than requiring fail-closed treatment, and its decision-record invariant omits the complete authenticated/acting/represented/approving/executing actor chain required by REQ-006 and FD-009. Evidence: IDENTITY_AUTHORIZATION_CONTRACT.md:15-21,23-30; REQUIREMENT_REGISTER.csv:7; FOUNDER_DECISION_REGISTER.csv:10. | Stale facts and incomplete attribution can weaken authority/evidence controls. |
| CMT02-F-017 | P1 | AMBIGUOUS_REQUIRES_REMEDIATION | The Protected Participant contract lacks an explicit Implementation authorized: FALSE declaration and does not define versioned inputs/outputs, attribution, dispute/revocation behavior, transition holds, or required contract tests. It also divides guardian authority/effects between Relationships, Safeguarding, and Protected Participant without a decision boundary. Evidence: IDENTITY_PROTECTED_PARTICIPANT_CONTRACT.md:1-10; IDENTITY_RELATIONSHIPS_CONTRACT.md:18-40; PIA lines 149-161. | Contract is too incomplete for exact-text ratification. |
| CMT02-F-018 | P2 | CLARIFICATION_WITHIN_APPROVED_AUTHORITY | The Relationships contract says all cross-domain calls carry a represented principal, while REQ-006 says represented principal where applicable. Evidence: IDENTITY_RELATIONSHIPS_CONTRACT.md:40; REQUIREMENT_REGISTER.csv:7. | Clarify optionality or an explicit not-applicable value; nonblocking after P0/P1 remediation. |

## ADR disposition summary

| ADR | Result | Primary reason |
|---|---|---|
| ADR-IDENTITY-001 | REQUIRES_BOUNDED_REMEDIATION | Inexact FD-002/FD-008 traceability and missing verified-email coverage |
| ADR-IDENTITY-002 | REQUIRES_BOUNDED_REMEDIATION | Material relying-party/attestation additions |
| ADR-IDENTITY-003 | REQUIRES_BOUNDED_REMEDIATION | Material assurance taxonomy and numeric policy additions |
| ADR-IDENTITY-004 | REQUIRES_BOUNDED_REMEDIATION | Material client/session architecture plus incomplete support/closure semantics |
| ADR-IDENTITY-005 | REQUIRES_BOUNDED_REMEDIATION | Material recovery mechanism/count plus overstated mappings |
| ADR-IDENTITY-006 | REQUIRES_BOUNDED_REMEDIATION | Missing invitation/onboarding semantics and cross-domain tenancy default |
| ADR-IDENTITY-007 | REQUIRES_BOUNDED_REMEDIATION | Protected-hold ambiguity and incomplete FD-004 semantics |

## Positive conformance

- All seven ADRs visibly remain pending final ratification and state Implementation authorized: FALSE.
- The PIA consistently rejects authentication-as-authorization, role-as-authority, payment-as-guardianship, and automatic identity merge.
- The Identity-to-Relationships contract preserves separate identity/relationship truth and merge independence.
- The main text of ADR-007 preserves identity/account continuity and pauses automatic transition for exceptions.
- MIAP is correctly expanded as Master Implementation Atlas Program; no active MAIP occurrence was found in the Identity package.
- Source reconciliation candidly preserves remaining Permission, Agreement, Safeguarding, Audit, Communication, Privacy, and repository-registration gaps.
- Baseline freeze, implementation, production, and enrollment remain expressly unauthorized.

## Proposed corrections and approval boundary

PROPOSED_CORRECTIONS.csv contains bounded replacement/addition proposals. They are proposals only. CMT-02 does not approve its own redlines. Material additions require an explicit Founder decision or exact-text Founder ratification after independent review; cross-domain clauses require owning-domain concurrence.

## Limitations

- Documentary review only; no application, provider, schema, migration, code, database, runtime, or production execution occurred.
- The lane did not use the network and did not independently fetch repository bytes.
- Exact constitutional source content outside the supplied Identity package was not re-adjudicated; source conclusions are limited to supplied reconciliation records and their internal consistency.
- No other lane output or proposed redline was read.
- Findings do not adjudicate law, jurisdiction-specific age rules, compliance, or external assurance.
- This lane cannot approve its own proposed corrections or issue the coordinator's final directive disposition.

## Self-audit

- Required classification vocabulary used: PASS.
- Only P0, P1, and P2 used for nonempty severities: PASS.
- Every open finding has a claim-to-evidence locator: PASS.
- Founder approval distinguished from ADR ratification and implementation authority: PASS.
- P0/P1 presence blocks ratification readiness: PASS.
- Frozen-input modifications: 0.
- Writes outside the CMT-02 output directory: 0.
- Other lane outputs read: 0.
- Network calls: 0.
- Application runs: 0.
- Git mutations: 0.
- Custom agents claimed or executed by this lane: 0.
- Self-approval of proposed corrections: 0.

## Completion attestation

CMT-02_DOCUMENTARY_REVIEW_COMPLETE_WITH_OPEN_P0_P1_REMEDIATION_REQUIRED.

All eight required lane artifacts are produced when OUTPUT_MANIFEST.json is present. Output SHA-256 values are recorded in OUTPUT_MANIFEST.json. The manifest intentionally does not embed its own byte hash because that would be recursively self-referential; its final file hash is to be computed by the coordinator or external validator.

