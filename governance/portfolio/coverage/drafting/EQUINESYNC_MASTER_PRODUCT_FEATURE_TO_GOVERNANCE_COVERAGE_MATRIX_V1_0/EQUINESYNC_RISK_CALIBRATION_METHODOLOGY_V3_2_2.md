# EquineSync Risk Calibration Methodology V3.2.2
## Feature-to-Governance Matrix Risk, Governance Urgency, Calibration, and Review Standard

**Legal Entity:** EquineSync LLC  
**Document ID:** `EQUINESYNC_RISK_CALIBRATION_METHODOLOGY_V3_2`  
**Version:** `3.2.2`  
**Version Label:** `3.2.2-calibration-exercise-clarified-freeze-candidate.1`  
**Date:** August 9, 2026  
**Immediate Predecessor:** `3.2.1-final-targeted-correction-candidate.1`  
**Historical Predecessors:** V3.1, V3.0, V2.2, V2.1, V2.0, V1.0  
**Primary Decision Question:** `FDQ-003`  
**Initial Feature Population:** `314`  
**Canonical Risk Identity Unit:** `RISK_SCENARIO`  
**Canonical Calibration Unit:** `RISK_SCENARIO × ASSESSMENT_SCOPE`  
**Authority Class:** `DOCUMENTARY_GOVERNANCE_PLANNING_STANDARD`  
**Status:** `FULLY_CONSOLIDATED_CALIBRATION_EXERCISE_CLARIFIED_FREEZE_CANDIDATE`  
**Bounded Exercise Evidence:** `ES-RCM-V3_2-BCE-001`  
**Bounded Exercise Disposition:** `METHODOLOGY_CALIBRATION_EXERCISE_PASS_WITH_NONBLOCKING_CLARIFICATIONS`

---

# 1. Purpose

This methodology governs how EquineSync identifies, calibrates, compares, prioritizes, reviews, and evidences risk scenarios associated with product features and governance planning.

It exists to make the Feature-to-Governance Matrix risk signal:

- feature-specific rather than templated;
- consequence-based rather than governance-gap-based;
- evidence-aware without disguising uncertainty as likelihood;
- scope-aware without averaging materially different environments or cohorts;
- reproducible enough for independent review;
- subordinate to actual governance authority;
- nonauthoritative for implementation, release, pilot, production, conformity, or risk acceptance.

This methodology is a planning and governance-sequencing instrument. It is not a substitute for domain-specific security, safeguarding, privacy, financial-control, legal, equine-health, human-safety, operational, or release review.

---

# 2. Standalone Successor Rule

Version 3.2.2 is the complete current operating methodology for this family.

A competent reviewer shall be able to operate the methodology using:

1. this document;
2. its current machine-readable companion registers and schemas;
3. the current frozen evidence set for the assessment being performed.

No prior methodology version is required for ordinary operation.

Historical versions remain evidence of evolution and finding closure, but they do not supply missing operating rules to this version.

`STANDALONE_SUCCESSOR = TRUE`

`PRIOR_METHODOLOGY_REQUIRED_FOR_OPERATION = FALSE`

---

# 3. Authority and Non-Authority

This methodology may:

- identify a risk scenario;
- identify a governance question;
- identify an already-existing governance gate;
- assign a documentary planning priority;
- route evidence gaps for review;
- support governance sequencing;
- support bounded methodology exercises;
- support later documentary recalibration.

This methodology does **not** itself authorize:

- implementation;
- source-code changes;
- schema changes;
- migrations;
- permission expansion;
- provider or vendor activation;
- AI activation;
- deployment;
- release;
- pilot activation or pilot-scope expansion;
- production use;
- public launch;
- certification;
- conformity claims;
- public trust claims;
- legal compliance claims;
- risk acceptance;
- medical or veterinary conclusions;
- safeguarding decisions;
- consequential financial decisions.

`IMPLEMENTATION_AUTHORIZED_BY_THIS_ARTIFACT = FALSE`

`DEPLOYMENT_AUTHORIZED_BY_THIS_ARTIFACT = FALSE`

`PILOT_AUTHORIZED_BY_THIS_ARTIFACT = FALSE`

`PRODUCTION_AUTHORIZED_BY_THIS_ARTIFACT = FALSE`

`PUBLIC_LAUNCH_AUTHORIZED_BY_THIS_ARTIFACT = FALSE`

---

# 4. Core Principles

## 4.1 Risk is scenario-specific

Risk belongs to a defined failure or misuse scenario, not merely to a feature name, product domain, governance-gap label, or document status.

## 4.2 Severity measures consequence

Severity answers:

> If this scenario occurs under the stated conditions, how serious is the supported consequence?

Severity shall not be reduced merely because current exposure is small, a capability is inactive, implementation is incomplete, or governance documentation exists.

## 4.3 Likelihood measures plausible exposure

Likelihood answers:

> Under the stated assessment scope and current supported assumptions, how plausibly may this scenario occur?

Likelihood shall not be increased merely because governance is incomplete, nor reduced merely because evidence is sparse.

## 4.4 Evidence uncertainty is separate

Confidence and calibration state express evidence sufficiency.

Evidence uncertainty shall not be disguised as lower likelihood.

## 4.5 No cross-scope averaging

Materially different scopes shall be calibrated separately.

Public/private, current/future, tenant/cohort, provider, jurisdictional, or activation differences shall not be averaged into a single synthetic score.

## 4.6 Authority is separate from risk

Risk severity, likelihood, score, or priority does not create authority.

Governance urgency does not create authority.

A reviewer may identify an already-existing gate but may not invent one.

## 4.7 Operating-control credit requires operating evidence

Governance text and product design may establish expected behavior or a gate, but they do not by themselves prove operating enforcement.

## 4.8 Reproducibility over cosmetic balance

Reviewers shall not manufacture LOW, RARE, LIKELY, CRITICAL, or other values merely to create an aesthetically balanced distribution.

---

# 5. Canonical Data Model

The canonical identity unit is:

`RISK_SCENARIO`

The canonical calibration unit is:

`RISK_SCENARIO × ASSESSMENT_SCOPE`

A feature may have:

- zero material scenarios after complete screening;
- one material scenario;
- multiple material scenarios;
- one scenario calibrated in multiple scopes;
- multiple scenarios in multiple scopes.

Feature-level summaries are derived from scenario-scope calibrations. They do not replace the underlying scenario records.

---

# 6. Required Scenario Families

Every feature shall be screened against these controlled scenario families:

1. `AUTHORITY_ACCESS`
2. `PRIVACY_DISCLOSURE`
3. `DATA_RECORD_INTEGRITY`
4. `AVAILABILITY_CONTINUITY`
5. `HUMAN_SAFETY`
6. `HORSE_HEALTH_WELFARE`
7. `SAFEGUARDING_PROTECTED_PARTICIPANT`
8. `FINANCIAL`
9. `LEGAL_REGULATORY`
10. `EXTERNAL_PROVIDER_DEPENDENCY`
11. `OFFLINE_SYNCHRONIZATION`
12. `AUTOMATION_AI`
13. `MISUSE_ABUSE`
14. `RECOVERY_ROLLBACK`
15. `EVIDENCE_AUDIT`
16. `CROSS_TENANT_BOUNDARY`
17. `COMMUNICATION_DELIVERY`
18. `CONFIGURATION_FEATURE_FLAG`
19. `PUBLIC_TRUST_REPUTATION`

A scenario may have one primary family and multiple secondary families.

Family overlap shall not create duplicate scenarios where the underlying failure mode, affected subject, and consequence are materially the same.

---

# 7. Scenario Discovery Protocol

For each feature and applicable scope-planning context, reviewers shall ask at minimum:

- Could this feature grant, deny, or distort authority?
- Could it expose information to an unauthorized audience?
- Could records be created, lost, corrupted, duplicated, stale, or misattributed?
- Could the feature become unavailable when materially needed?
- Could a person be physically harmed?
- Could a horse's health or welfare be harmed?
- Could a minor or protected participant be harmed, contacted, exposed, or inadequately safeguarded?
- Could money move incorrectly or without authority?
- Could legal, contractual, regulatory, or consent obligations be implicated?
- Could an external provider fail, diverge, or become unavailable?
- Could offline, retry, replay, merge, ordering, or synchronization behavior cause harm?
- Could AI or automation exceed evidence, authority, or human-review boundaries?
- Could the feature be abused or deliberately misused?
- Could recovery, rollback, restoration, or reversal fail?
- Could evidence, attribution, or audit truth be lost?
- Could tenant or facility boundaries be crossed?
- Could communications fail, misroute, duplicate, or disclose protected content?
- Could configuration or feature-flag state create unsafe divergence?
- Could public-facing output materially damage trust through false, misleading, unsafe, or unsupported representation?

---

# 8. Discovery Completeness and Screened-Nonmaterial Records — V3.2.2 Clarification 01

**Clarification ID:** `V322-CLR-AMB-01`

The bounded calibration exercise established that the methodology must distinguish proof of complete family screening from scenario-register population.

The controlling rule is:

1. The `RISK_SCENARIO_DISCOVERY_REGISTER.csv` shall prove that every required scenario family was screened for every feature in the assessment population.
2. The `RISK_SCENARIO_REGISTER.csv` shall contain:
   - material scenarios;
   - `INSUFFICIENT_EVIDENCE_RETAINED` scenarios;
   - candidate scenarios requiring scenario-level lifecycle tracking;
   - other scenarios expressly required by the methodology.
3. A separate Risk Scenario row is **not required** for every feature/family pairing dispositioned as screened nonmaterial, provided the Discovery Register records the screening and disposition in machine-readable form.
4. A family may not disappear merely because no scenario row is created.
5. Validators shall fail where required family screening cannot be proven.

This rule prevents unnecessary scenario-register inflation while preserving complete discovery evidence.

`AMB_01 = RESOLVED`

---

# 9. Discovery State

Each feature/scope discovery record shall use:

- `NOT_STARTED`
- `IN_PROGRESS`
- `COMPLETE`
- `COMPLETE_WITH_OPEN_EVIDENCE_GAP`
- `REVIEW_REQUIRED`

Where no material scenario is identified in a family, the discovery record shall retain the basis for that conclusion.

Where plausible material consequence cannot responsibly be dismissed but evidence is insufficient to calibrate, use:

`INSUFFICIENT_EVIDENCE_RETAINED`

rather than silently dropping the scenario.

---

# 10. Materiality

A scenario is material when it could reasonably affect one or more of:

- governance sequencing;
- authority or access;
- privacy;
- safeguarding;
- human safety;
- horse health or welfare;
- financial correctness;
- legal or regulatory posture;
- continuity of materially important operations;
- evidence integrity;
- cross-tenant isolation;
- recovery or rollback;
- provider dependency;
- public trust;
- product or operational decisions.

A scenario may be dispositioned:

- `MATERIAL_SCENARIO_CONFIRMED`
- `INSUFFICIENT_EVIDENCE_RETAINED`
- `SCREENED_NONMATERIAL`
- `DUPLICATE`
- `SUPERSEDED`
- `NOT_APPLICABLE`

A reviewer shall not classify a scenario nonmaterial merely because the feature is not currently active.

---

# 11. Scenario Identity

Scenario identity shall be scope-independent.

`SCENARIO_IDENTITY_SIGNATURE` shall derive from controlled, scope-independent identity elements such as:

- feature ID;
- failure-mode class;
- affected-subject class;
- consequence class.

Assessment scope shall not be part of the base scenario identity.

For a scenario in a particular scope:

`SCENARIO_SCOPE_KEY = RISK_SCENARIO_ID + "::" + ASSESSMENT_SCOPE_ID`

This pair key is the canonical machine identity for a calibration row.

---

# 12. Duplicate and Related Scenario Handling

Allowed scenario relationships include:

- `DISTINCT`
- `POTENTIAL_DUPLICATE`
- `DUPLICATE`
- `PARENT`
- `CHILD`
- `RELATED_DIFFERENT_FAILURE_MODE`
- `SUPERSEDING`
- `SUPERSEDED`

Duplicate detection shall not collapse scenarios that share a consequence but arise from materially different failure modes, controls, or remediation paths.

---

# 13. Scenario Lifecycle

Scenario lifecycle states:

- `DRAFT`
- `DISCOVERED`
- `UNDER_CALIBRATION`
- `ACTIVE`
- `REVIEW_REQUIRED`
- `SUPERSEDED`
- `CLOSED_NO_LONGER_APPLICABLE`
- `DUPLICATE_RETIRED`

Historical records shall remain reconstructable.

---

# 14. Assessment Scope

Every calibration shall reference a controlled `ASSESSMENT_SCOPE_ID`.

The Scope Register shall record at minimum:

- scope ID;
- scope name;
- environment;
- cohort;
- tenant/facility context;
- public/private state;
- jurisdiction where material;
- provider state where material;
- activation proximity;
- authorization state;
- effective dates;
- source references;
- status;
- notes.

A scope describes the conditions under which a risk calibration is interpreted. A snapshot records the evidence state used at a particular assessment time. Scope and snapshot are distinct.

---

# 15. Assessment Snapshot

Every formal calibration package shall use an assessment snapshot.

Minimum snapshot schema includes:

- snapshot ID;
- snapshot status;
- assessment scope ID;
- methodology ID/version;
- Matrix ID/version;
- repository name;
- repository commit or equivalent source revision;
- assessment timestamp/effective-at;
- environment;
- activation state;
- public/private state;
- material configuration/feature-flag references;
- provider state/configuration references;
- cohort/tenant/jurisdiction fields where applicable;
- authorization/gate source references;
- material control versions/states;
- evidence package references;
- runtime/test/repository references where applicable;
- `snapshot_sha256`;
- `snapshot_byte_length`;
- `finalized_at`;
- `finalized_by`;
- `supersedes_snapshot_id`;
- notes.

`UNKNOWN` and `NOT_APPLICABLE` shall be represented distinctly.

---

# 16. Snapshot Canonicalization and Immutability

The canonical snapshot payload shall use deterministic UTF-8 JSON serialization with:

- schema-defined field order;
- no insignificant whitespace;
- standard JSON escaping;
- controlled literal representation of `UNKNOWN` and `NOT_APPLICABLE`;
- controlled empty collections as `[]`;
- no semantic empty-string substitution.

The hash payload excludes only:

- `snapshot_sha256`
- `snapshot_byte_length`

All other finalized fields, including finalization metadata and supersession linkage, are included.

`snapshot_byte_length` equals the UTF-8 byte length of the exact canonical payload used for SHA-256.

A finalized snapshot is immutable. Correction requires a successor snapshot with new integrity values and predecessor linkage.

---

# 17. Consequence Dimensions

Severity shall consider applicable consequence dimensions independently, including:

- human safety;
- horse health and welfare;
- safeguarding/protected participants;
- privacy/confidentiality;
- authorization/access;
- financial consequence;
- legal/regulatory consequence;
- availability/continuity;
- evidence/record integrity;
- public trust/reputation.

The final scenario severity is the highest supported dimension severity unless a methodology-valid severity-reduction control is specifically evidenced.

Consequence dimensions shall not be averaged.

---

# 18. Severity Scale

## LOW

Limited, reversible, localized consequence with low materiality and no supported pathway to significant safety, welfare, safeguarding, privacy, authority, financial, legal, continuity, or evidence harm.

## MEDIUM

Material but bounded consequence requiring correction, operational attention, or controlled remediation, without evidence of severe or catastrophic impact.

## HIGH

Serious consequence that may materially impair safety, welfare, privacy, authorization, financial correctness, continuity, evidence integrity, or protected workflows; may require urgent remediation or significant recovery.

## CRITICAL

Catastrophic, systemic, or otherwise highest-consequence outcome supported by evidence, such as severe human harm, severe horse-welfare harm, grave safeguarding failure, systemic cross-tenant or privilege compromise, major unauthorized financial movement, or platform-wide loss of critical integrity/availability where the evidence supports that pathway.

CRITICAL shall not be inferred merely from a feature's foundational role, broad domain importance, or governance sensitivity.

---

# 19. Inherent Risk

`INHERENT_SEVERITY` is mandatory for material scenarios unless evidence is insufficient even to support a consequence anchor.

`INHERENT_LIKELIHOOD` is conditional and may use:

- `RARE`
- `UNLIKELY`
- `POSSIBLE`
- `LIKELY`
- `NOT_MEANINGFULLY_ESTIMABLE`

The inherent baseline assumes the intended capability is available in the assessment scope and scenario-specific preventive/detective controls are absent, while unrelated platform assumptions remain.

---

# 20. Residual Severity

Residual severity normally remains equal to inherent severity.

Severity may be reduced only where a control changes the supported consequence itself, not merely the chance of occurrence.

Any residual severity reduction shall record:

- control ID;
- control layer;
- effectiveness state;
- evidence basis;
- severity-reduction rationale;
- reviewer.

---

# 21. Likelihood Decision Framework

Residual likelihood shall be assessed using supported evidence across these factors:

1. reachability in the assessment scope;
2. trigger frequency;
3. exposure population/breadth;
4. operating control effectiveness;
5. trigger complexity or preconditions;
6. known evidence/history;
7. automation or scale amplification.

Reviewers shall record the factor basis.

---

# 22. Likelihood Scale

## RARE

Occurrence requires exceptional or highly constrained conditions under the stated scope and supported controls/evidence.

## UNLIKELY

Occurrence is plausible but requires meaningful constraints, uncommon triggers, narrow exposure, or other supported limiting conditions.

## POSSIBLE

Occurrence is credibly reachable under ordinary or reasonably foreseeable conditions; neither exceptional nor expected as routine inevitability.

## LIKELY

Occurrence is expected or strongly plausible under common operating conditions, frequent triggers, broad reachability, or weak/absent controls supported by evidence.

A high severity does not imply high likelihood.

A missing governance artifact does not imply high likelihood.

Insufficient evidence does not imply RARE or UNLIKELY.

---

# 23. Documentary Methodology Exercise Reachability — V3.2.2 Clarification 07

**Clarification ID:** `V322-CLR-AMB-07`

For an assessment scope whose type is:

`PLANNED_DOCUMENTARY_METHODOLOGY_EXERCISE`

"reachability in the assessment scope" means:

> structural reachability under the feature's intended normal-use workflow, independent of present deployment, pilot, production, or activation status.

Therefore:

- current inactivity shall not automatically produce `RARE`;
- contemplated future activation shall not automatically produce `POSSIBLE`;
- the reviewer shall evaluate normal-use structural reachability using the feature's workflow, trigger, exposure, evidence, and control facts;
- the exercise scope shall not generate a current-exposure controller.

`AMB_07 = RESOLVED`

---

# 24. Calibration State

Allowed states:

- `CALIBRATED`
- `PROVISIONAL`
- `INSUFFICIENT_EVIDENCE`
- `NOT_APPLICABLE`
- `SUPERSEDED`

Where evidence does not support a defensible residual likelihood or severity:

`RISK_CALIBRATION_STATE = INSUFFICIENT_EVIDENCE`

and numeric score shall remain blank.

---

# 25. Provisional Calibration

A provisional calibration requires:

- provisional reason;
- assumptions;
- approving documentary calibration authority;
- effective date;
- expiration;
- required evidence;
- recalibration trigger.

A provisional calibration may support temporary sequencing or evidence planning.

It shall not:

- count as final methodology evidence where final calibration is required;
- establish release, pilot, production, conformity, or risk acceptance;
- silently become permanent.

Expiration routes the record to `REVIEW_REQUIRED` unless renewed, recalibrated, or superseded.

---

# 26. Confidence

Confidence records evidence strength and calibration support. It does not modify likelihood.

Controlled states may include:

- `HIGH_CONFIDENCE`
- `MODERATE_CONFIDENCE`
- `LOW_CONFIDENCE`
- `INSUFFICIENT_EVIDENCE`

LOW confidence shall route to evidence review where required, especially for high-consequence scenarios.

Confidence shall not break substantive controller ties.

---

# 27. Risk Score

Where calibration is permitted:

Severity values:

- LOW = 1
- MEDIUM = 2
- HIGH = 3
- CRITICAL = 4

Likelihood values:

- RARE = 1
- UNLIKELY = 2
- POSSIBLE = 3
- LIKELY = 4

`RISK_SCORE = SEVERITY_VALUE × LIKELIHOOD_VALUE`

Valid scores are:

`{1,2,3,4,6,8,9,12,16}`

Invalid product scores:

`{5,7,10,11,13,14,15}`

A score is a documentary planning signal only.

---

# 28. Priority Matrix

| Residual Severity | RARE | UNLIKELY | POSSIBLE | LIKELY |
|---|---|---|---|---|
| LOW | LOW | LOW | MODERATE | MODERATE |
| MEDIUM | LOW | MODERATE | MODERATE | HIGH |
| HIGH | MODERATE | MODERATE | HIGH | VERY_HIGH |
| CRITICAL | HIGH | HIGH | VERY_HIGH | VERY_HIGH |

A residual CRITICAL scenario shall never fall below HIGH priority.

Insufficient-evidence scenarios use:

`EVIDENCE_REVIEW_REQUIRED`

rather than a fabricated score.

---

# 29. Control Layers

Controlled layers:

- `CONSTITUTIONAL_GOVERNANCE`
- `PRODUCT_DESIGN`
- `IMPLEMENTATION`
- `RUNTIME`
- `MANUAL_OPERATIONAL`
- `EXTERNAL_PROVIDER`

Controls shall be represented separately from scenario-control mappings.

Common-mode dependencies shall be recorded where multiple controls depend on the same underlying enforcement mechanism or provider.

---

# 30. Control Effectiveness States

Controlled effectiveness states:

- `VERIFIED_EFFECTIVE`
- `PARTIALLY_VERIFIED`
- `IMPLEMENTED_UNVERIFIED`
- `DESIGNED_NOT_IMPLEMENTED`
- `ABSENT`
- `UNKNOWN`
- `NOT_APPLICABLE`

---

# 31. Operating Credit Classes

- `NO_OPERATING_CREDIT`
- `LIMITED_OPERATING_CREDIT`
- `SUPPORTED_OPERATING_CREDIT`
- `VERIFIED_OPERATING_CREDIT`

Maximum credit ceiling:

| Layer | Effectiveness | Maximum Credit |
|---|---|---|
| Constitutional governance | any | NO_OPERATING_CREDIT |
| Product design | any | NO_OPERATING_CREDIT |
| Implementation | DESIGNED_NOT_IMPLEMENTED / ABSENT / UNKNOWN / NOT_APPLICABLE | NO_OPERATING_CREDIT |
| Implementation | IMPLEMENTED_UNVERIFIED | LIMITED_OPERATING_CREDIT |
| Implementation | PARTIALLY_VERIFIED | SUPPORTED_OPERATING_CREDIT |
| Implementation | VERIFIED_EFFECTIVE | SUPPORTED_OPERATING_CREDIT |
| Runtime | IMPLEMENTED_UNVERIFIED | LIMITED_OPERATING_CREDIT |
| Runtime | PARTIALLY_VERIFIED | SUPPORTED_OPERATING_CREDIT |
| Runtime | VERIFIED_EFFECTIVE | VERIFIED_OPERATING_CREDIT |
| Manual operational | IMPLEMENTED_UNVERIFIED | LIMITED_OPERATING_CREDIT |
| Manual operational | PARTIALLY_VERIFIED | SUPPORTED_OPERATING_CREDIT |
| Manual operational | VERIFIED_EFFECTIVE | VERIFIED_OPERATING_CREDIT |
| External provider | IMPLEMENTED_UNVERIFIED | LIMITED_OPERATING_CREDIT |
| External provider | PARTIALLY_VERIFIED | SUPPORTED_OPERATING_CREDIT |
| External provider | VERIFIED_EFFECTIVE | VERIFIED_OPERATING_CREDIT |

Overrides may reduce credit below the ceiling.

Overrides shall not increase credit above the ceiling.

Stronger evidence requires updating the effectiveness state, preserving history, and recalculating.

Source-code presence alone does not establish `VERIFIED_EFFECTIVE`.

Governance text alone does not establish operating credit.

---

# 32. Legacy PARTIAL_IMPLEMENTATION Mapping — V3.2.2 Clarification 02

**Clarification ID:** `V322-CLR-AMB-02`

Where a legacy or Matrix evidence taxonomy uses:

`PARTIAL_IMPLEMENTATION`

that label maps to:

`IMPLEMENTED_UNVERIFIED`

unless accepted verification evidence independently establishes `PARTIALLY_VERIFIED` or a stronger effectiveness state.

The word "partial" in an implementation-status label is not verification evidence.

Without accepted verification evidence, maximum control credit is:

`LIMITED_OPERATING_CREDIT`

This clarification applies prospectively to recalibration and does not rewrite historical locked review files.

`AMB_02 = RESOLVED`

---

# 33. Governance Source Requirements

A governance gate may be identified only from a source whose authority and lifecycle are sufficiently established.

Gate source assessment shall record:

- source ID;
- authority type;
- subject/scope;
- effective date;
- lifecycle status;
- version;
- authority/precedence rank where controlled;
- supersession status;
- conflict status;
- source reference.

Only a current effective source may establish a gate.

A newer source is not automatically controlling merely because it is newer.

Where material source authority conflicts or precedence cannot be resolved:

`GOVERNANCE_GATE_STATE = GATE_STATUS_UNKNOWN`

and the item routes to `GOVERNANCE_AUTHORITY_REVIEW_QUEUE`.

---

# 34. Governance Gate States

Allowed states:

- `NO_GATE_IDENTIFIED`
- `EXISTING_GATE_BLOCKS_CURRENT_USE`
- `EXISTING_GATE_BLOCKS_ACTIVATION`
- `EXISTING_GATE_REQUIRES_REMEDIATION`
- `GATE_STATUS_UNKNOWN`

`GATE_STATUS_UNKNOWN` is not equivalent to `NO_GATE_IDENTIFIED`.

A statement that a particular artifact **does not itself authorize** an activity is not automatically an affirmative product-wide gate blocking that activity.

The reviewer must establish that the cited source has authority over the exact activity and scope and remains effective and non-superseded.

---

# 35. Governance Urgency

Allowed urgency states, highest first:

1. `IMMEDIATE_BLOCKING`
2. `ACTIVE_REMEDIATION_REQUIRED`
3. `PRE_ACTIVATION_REQUIRED`
4. `PLANNED`
5. `DEFERRED`

Urgency is a planning classification. It does not create authority.

---

# 36. Governance Coverage Does Not Mechanically Determine Urgency — V3.2.2 Clarification 03

**Clarification ID:** `V322-CLR-AMB-03`

There shall be no direct lookup from Matrix governance-coverage state to Governance Urgency.

The following labels, alone, do not mechanically determine urgency:

- `NEW_PIA_CANDIDATE`
- `CODE_GUIDE_GAP`
- `ADR_GAP`
- `OPERATING_STANDARD_GAP`
- `RUNBOOK_GAP`
- `PIA_SUPPLEMENT_CANDIDATE`
- `COVERED_WITH_RETAINED_GAP`
- other governance-completeness states.

Governance coverage describes documentary completeness or ownership state.

Governance urgency shall derive from:

- current effective authority;
- governance-gate state;
- whether current use is affected;
- activation proximity;
- independently established remediation need.

Matrix gap type may inform planning context, but it does not create urgency or authority.

`AMB_03 = RESOLVED`

---

# 37. Unknown Gate Urgency — V3.2.2 Clarification 08

**Clarification ID:** `V322-CLR-AMB-08`

Where:

`GOVERNANCE_GATE_STATE = GATE_STATUS_UNKNOWN`

and no stronger current-use, activation, or remediation condition applies:

`GOVERNANCE_URGENCY = PLANNED`

not `DEFERRED`.

Rationale: an unresolved authority question must be intentionally resolved before a relevant activation or governance decision, even where no current use is affected.

Higher urgency may apply where:

- current use is already affected;
- activation is authorized, imminent, or otherwise materially near;
- an active remediation obligation is independently established;
- another effective authority source establishes a stronger condition.

The record shall also route to:

`GOVERNANCE_AUTHORITY_REVIEW_QUEUE`

This clarification is prospective and does not alter locked historical calibration files.

`AMB_08 = RESOLVED`

---

# 38. Activation Proximity

Allowed values:

- `ACTIVE_NOW`
- `AUTHORIZED_NOT_ACTIVE`
- `PLANNED_NEAR_TERM`
- `PLANNED_LATER`
- `NOT_AUTHORIZED`
- `DEFERRED`
- `UNKNOWN`

`NOT_AUTHORIZED` may describe the current authority fact even where a governance-horizon scope is being considered.

A reviewer shall not invent an activation timeline.

---

# 39. Current Exposure Eligibility

A calibration is eligible for a normal Current Exposure Summary only where:

1. scenario lifecycle is `ACTIVE` or `REVIEW_REQUIRED`;
2. assessment scope is active;
3. `ACTIVATION_PROXIMITY = ACTIVE_NOW` or documented equivalent actual present reachability;
4. calibration state is `CALIBRATED` or expressly permitted `PROVISIONAL`;
5. scenario is not duplicate, superseded, or closed;
6. calibration is not `NOT_APPLICABLE` or `INSUFFICIENT_EVIDENCE`.

`AUTHORIZED_NOT_ACTIVE` is not current merely because authorization exists.

---

# 40. Current Freshness

Freshness states:

- `CURRENT`
- `REVIEW_DUE`
- `STALE_REVIEW_REQUIRED`
- `SUPERSEDED`

Normal current controller selection uses `CURRENT` and `REVIEW_DUE`.

If no fresh/review-due calibration exists but a materially active stale exposure exists:

`CURRENT_RISK_SUMMARY_STATE = STALE_REVIEW_REQUIRED`

and the stale controlling pair may be identified for visibility.

It shall not be represented as `CALIBRATED_CURRENT`.

---

# 41. Current Risk Controller

Substantive ordering:

1. Risk Priority Signal descending;
2. Residual Severity descending;
3. Risk Score descending.

All records tied through those fields are substantively co-controlling.

Confidence shall not break substantive ties.

`SCENARIO_SCOPE_KEY` lexical ascending may select one stable machine primary after the co-controlling set is established.

Required outputs include:

- `CURRENT_CONTROLLING_RISK_SCENARIO_SCOPE_KEY`
- `CURRENT_CONTROLLING_RISK_SCENARIO_ID`
- `CURRENT_CONTROLLING_SCOPE_ID`
- `CURRENT_MAX_RISK_PRIORITY_SIGNAL`
- `CURRENT_MAX_RESIDUAL_SEVERITY`
- `CURRENT_CONTROLLING_RISK_SCORE`
- `CO_CONTROLLING_RISK_SCENARIO_SCOPE_KEYS`

---

# 42. Governance Horizon Eligibility

A scenario-scope calibration may be governance-horizon eligible where:

- the scenario is material and applicable;
- it is not duplicate, superseded, or closed;
- the scope is active or planned;
- governance urgency is assigned;
- governance relevance is material.

A risk calibration in `INSUFFICIENT_EVIDENCE` may remain governance-horizon eligible where a governance gate is independently established or the authority question itself requires planned review.

No numeric risk shall be fabricated.

---

# 43. Governance Controller

Substantive ordering:

1. Governance Urgency descending;
2. Governance Gate Sort Rank descending;
3. populated Risk Priority Signal descending;
4. populated Residual Severity descending;
5. populated Risk Score descending.

For sorting purposes only, the gate ordering is:

1. `EXISTING_GATE_BLOCKS_CURRENT_USE`
2. `EXISTING_GATE_BLOCKS_ACTIVATION`
3. `EXISTING_GATE_REQUIRES_REMEDIATION`
4. `GATE_STATUS_UNKNOWN`
5. `NO_GATE_IDENTIFIED`

This is a deterministic sort rank, not a statement that `GATE_STATUS_UNKNOWN` is a verified gate.

Where one otherwise-equal record has populated risk and another does not, populated risk ranks ahead as a secondary deterministic aid. The blank-risk record's independently verified or unresolved governance state remains valid and visible.

---

# 44. Governance Co-Controller Rule

Governance records are substantively co-controlling when they are equal across all applicable substantive ranking fields before lexical pair-key tie-breaking.

Where both have populated risk, equality requires:

- Governance Urgency;
- Governance Gate Sort Rank;
- Risk Priority Signal;
- Residual Severity;
- Risk Score.

Where both lack populated risk, equality on:

- Governance Urgency;
- Governance Gate Sort Rank

is sufficient.

Where one has populated risk and the other does not, they are not substantively co-controlling under the current calibration state.

All co-controllers shall be preserved as:

`CO_CONTROLLING_GOVERNANCE_SCENARIO_SCOPE_KEYS`

using canonical `SCENARIO_SCOPE_KEY` values.

Lexical ordering selects a machine primary only and does not imply substantive superiority.

---

# 45. Multi-Scope Rule

The same scenario may have separate calibrations for different scopes.

No cross-scope averaging is permitted.

Feature summaries may use explicit summary modes such as:

- `SINGLE_SCOPE`
- `HIGHEST_APPLICABLE_CURRENT_RISK`
- `HIGHEST_APPLICABLE_GOVERNANCE_URGENCY`

Material scope change triggers recalibration.

---

# 46. Evidence Classes and Source Discipline

Every material calibration shall distinguish the nature of evidence relied upon, including where applicable:

- primary verified evidence;
- hash-verified documentary evidence;
- derived verified evidence;
- repository implementation evidence;
- test verification;
- runtime verification;
- external-provider evidence;
- historical reported evidence;
- conflicted evidence;
- unreproducible evidence;
- insufficient evidence.

Documentary presence does not prove implementation.

Implementation presence does not prove runtime effectiveness.

Runtime claims require runtime-compatible evidence.

---

# 47. Evidence Freshness

Default review interval is 365 days unless a shorter interval is required.

Residual CRITICAL scenarios default to a maximum 180-day review interval unless stricter governance applies.

Material changes in scope, authority, controls, implementation, provider behavior, evidence, or scenario reachability may trigger earlier review.

---

# 48. Reviewer Governance

A calibration shall identify:

- preparer;
- reviewer;
- review date;
- conflict-of-interest status;
- adjudicator where required.

Material reviewer disagreement shall be recorded rather than silently harmonized.

Disagreement states:

- `CONSISTENT`
- `MINOR`
- `MATERIAL`
- `ADJUDICATED`
- `UNRESOLVED`

Reconciliation shall preserve original values and record the final reconciled value separately.

---

# 49. Reconciliation Outcomes

Allowed material-disagreement outcomes:

- `RECONCILED_TO_A`
- `RECONCILED_TO_B`
- `RECONCILED_TO_THIRD_RESULT_FROM_EXISTING_RULE`
- `UNRESOLVED_METHODOLOGY_AMBIGUITY`

A third result is permitted only where existing methodology rules support it. It shall not be used to invent new policy.

Scenario-discovery differences may result in retaining both scenarios where they represent distinct evidence-supported failure modes.

---

# 50. Anti-Templating Controls

Validators and reviewers shall check for:

- domain-constant severity without feature-specific basis;
- governance-state-driven likelihood;
- governance-gap-driven severity;
- suspicious concentration of likelihood values;
- missing LOW or RARE values caused by artificial floors;
- copied scenario language without feature-specific failure mode;
- persona or domain tags used as substitutes for risk analysis;
- identical control-credit treatment without evidence review.

A distribution warning does not require artificial rebalancing.

A concentration greater than or equal to 95% in one likelihood state across a sufficiently varied calibrated population triggers review, not automatic failure.

---

# 51. Risk Summary States

Feature or scenario summary states shall distinguish at minimum:

- calibrated current risk;
- provisional risk;
- stale review required;
- insufficient evidence;
- not applicable;
- superseded.

Summary labels shall not hide calibration-state differences.

---

# 52. Required Queues

At minimum the methodology shall support:

- risk-priority queue;
- evidence-review queue;
- low-confidence evidence-review queue;
- governance-authority review queue;
- provisional-calibration review queue;
- stale-review queue;
- adjudication queue;
- unresolved-methodology-ambiguity queue.

Queue inclusion criteria shall be machine-readable.

Machine sort ranks shall be explicit rather than inferred from label text.

---

# 53. Pre-Exercise Category Candidate Register

Before any bounded methodology exercise begins, create:

`RISK_METHODOLOGY_EXERCISE_CATEGORY_CANDIDATE_REGISTER.csv`

Mandatory categories where pre-identifiable include:

- human safety;
- horse welfare;
- safeguarding;
- privacy;
- authorization/access;
- financial;
- low-consequence/common workflow;
- disabled high-consequence capability;
- external provider;
- insufficient-evidence candidate;
- multi-risk-scenario feature;
- multi-scope feature;
- governance-source conflict;
- offline/synchronization;
- automation/AI.

Category qualification occurs before exercise calibration results exist.

Exercise results shall not retroactively define the sampling population.

---

# 54. No-Candidate Category Record

Every mandatory exercise category shall have a Candidate Register record.

`CATEGORY_QUALIFICATION_STATE` values:

- `QUALIFIED_FEATURE`
- `CATEGORY_NOT_PREIDENTIFIABLE`

For `QUALIFIED_FEATURE`, Feature ID is required.

For `CATEGORY_NOT_PREIDENTIFIABLE`:

- `feature_id = NOT_APPLICABLE`;
- `qualified_before_exercise = FALSE`;
- `NONIDENTIFIABILITY_BASIS` is required.

Synthetic or placeholder Feature IDs are prohibited.

A category discovered during the exercise may be reported as:

`CATEGORY_DISCOVERED_DURING_EXERCISE = TRUE`

without rewriting the frozen pre-exercise candidate population.

---

# 55. Deterministic Exercise Selection

Define:

`MANDATORY_CATEGORY_SELECTION_SET`

and:

`REQUIRED_DOMAIN_COVERAGE_SET`

Then:

`BASE_REQUIRED_SELECTION_SET = UNION(MANDATORY_CATEGORY_SELECTION_SET, REQUIRED_DOMAIN_COVERAGE_SET)`

`BASE_REQUIRED_SELECTION_COUNT = CARDINALITY(BASE_REQUIRED_SELECTION_SET)`

If `BASE_REQUIRED_SELECTION_COUNT <= 30`:

`TARGET_EXERCISE_SIZE = MIN(30, MAX(20, BASE_REQUIRED_SELECTION_COUNT))`

If `BASE_REQUIRED_SELECTION_COUNT > 30`:

`TARGET_EXERCISE_SIZE = BASE_REQUIRED_SELECTION_COUNT`

and record:

`EXERCISE_SIZE_EXCEPTION = REQUIRED_COVERAGE_EXCEEDS_NORMAL_CAP`

No required feature may be removed merely to satisfy the normal 30-feature cap.

If fill is needed, use deterministic domain round-robin selection with canonical domain order and Feature ID order.

No discretionary optional fill is permitted after target size is reached.

---

# 56. Independent Review Sampling

Independent review samples shall be deterministic from a predeclared population and selection rule.

For a bounded domain sample where a percentage rule is required:

`SAMPLE_COUNT = MIN(REMAINING_DOMAIN_POPULATION, MAX(3, CEILING(0.20 × REMAINING_DOMAIN_POPULATION)))`

unless another explicit methodology rule controls.

The same population, metadata, candidate register, and methodology version shall produce the same ordered selection.

---

# 57. Bounded Methodology Calibration Exercise

Before scaling a materially revised methodology across the full 314-feature Matrix, run a bounded exercise of normally 20–30 selected features, except where required coverage legitimately exceeds 30.

At minimum the exercise shall test:

- scenario discovery;
- severity anchors;
- likelihood decision rules;
- insufficient-evidence treatment;
- multi-scope behavior;
- control-credit ceilings;
- governance-gate handling;
- governance urgency;
- controller logic;
- anti-templating behavior;
- independent reviewer reproducibility;
- reconciliation behavior.

---

# 58. Bounded Exercise Pass Conditions

A bounded exercise may pass only where:

`UNRESOLVED_MATERIAL_DISAGREEMENTS = 0`

`AUTHORITY_GATE_INVENTIONS = 0`

`DOCUMENTARY_CONTROLS_WRONGLY_CREDITED_AS_RUNTIME = 0`

`CROSS_SCOPE_AVERAGING_DEFECTS = 0`

`UNHANDLED_MATERIAL_SCENARIOS_AFTER_RECONCILIATION = 0`

`SYSTEMATIC_DOMAIN_SCORING_DRIFT = 0_OR_NOT_DETECTED`

`SYSTEMATIC_GOVERNANCE_STATE_LIKELIHOOD_DRIFT = 0_OR_NOT_DETECTED`

`REPEATED_METHODOLOGY_AMBIGUITIES_REQUIRING_RULE_CHANGE = 0`

The exercise does not require perfect numeric agreement.

It requires that independent judgment remain constrained enough to yield materially compatible, evidence-supported governance outcomes after reconciliation.

---

# 59. Bounded Exercise ES-RCM-V3_2-BCE-001

The V3.2 bounded calibration exercise completed on August 9, 2026.

Coordinator disposition:

`METHODOLOGY_CALIBRATION_EXERCISE_PASS_WITH_NONBLOCKING_CLARIFICATIONS`

Final exercise facts:

`FEATURES = 23`

`FINAL_SCENARIO_IDENTITIES_AT_MCE_SCOPE = 32`

`CALIBRATED_SCENARIOS = 29`

`INSUFFICIENT_EVIDENCE_SCENARIOS = 3`

`UNRESOLVED_MATERIAL_DISAGREEMENTS = 0`

`AUTHORITY_GATE_INVENTIONS = 0`

`DOCUMENTARY_CONTROLS_WRONGLY_CREDITED_AS_VERIFIED_RUNTIME = 0`

`CROSS_SCOPE_AVERAGING_DEFECTS = 0`

`UNHANDLED_DISCLOSED_MATERIAL_SCENARIOS_AFTER_RECONCILIATION = 0`

`SYSTEMATIC_DOMAIN_SCORING_DRIFT = NOT_DETECTED_IN_BOUNDED_SAMPLE`

`SYSTEMATIC_GOVERNANCE_STATE_LIKELIHOOD_DRIFT = NOT_DETECTED_AFTER_CLARIFICATION`

`REPEATED_METHODOLOGY_AMBIGUITIES_REQUIRING_FURTHER_RULE_CHANGE = 0`

Retained evidence limitation:

Reviewer A's complete 38-scenario discovery register was not separately accessioned and hash-locked before comparison. Exact reproducible raw scenario-discovery-overlap percentage therefore cannot be produced from two immutable full raw registers. This custody limitation remains part of the evidence record and does not erase the explicit reconciliation of known material scenario-discovery differences.

---

# 60. Exercise Clarification Disposition

The bounded exercise produced eight ambiguity identifiers.

This successor resolves the five requiring clarification:

| Ambiguity | V3.2.2 Disposition |
|---|---|
| AMB-01 | Resolved by §8 discovery completeness rule |
| AMB-02 | Resolved by §32 legacy partial-implementation mapping |
| AMB-03 | Resolved by §36 urgency derivation rule |
| AMB-07 | Resolved by §23 documentary-exercise reachability rule |
| AMB-08 | Resolved by §37 unknown-gate urgency rule |

The remaining exercise ambiguities require no methodology rule change:

- AMB-04: existing activation-proximity rule sufficient;
- AMB-05: `INSUFFICIENT_EVIDENCE_RETAINED` rule sufficient;
- AMB-06: `NOT_MEANINGFULLY_ESTIMABLE` inherent-likelihood rule sufficient.

`OPEN_EXERCISE_METHODOLOGY_AMBIGUITIES = 0`

---

# 61. Required Artifact Family

The methodology package shall maintain, as applicable:

1. methodology document;
2. scenario register;
3. scenario discovery register;
4. scenario calibration register;
5. factor-definition register;
6. consequence-anchor register;
7. likelihood-decision register;
8. rating-scale register;
9. control catalog;
10. scenario-control mapping;
11. exception register;
12. provisional-calibration register;
13. assessment-scope register;
14. assessment-snapshot register;
15. calibration-history register;
16. adjudication register;
17. queue register;
18. methodology-exercise category candidate register;
19. methodology-exercise selection register;
20. field dictionary;
21. validator;
22. validator tests;
23. review report;
24. recalibration-change report;
25. methodology-exercise report;
26. accession record;
27. package manifest;
28. checksum manifest.

Additional artifacts may be added without changing methodology authority where they preserve, rather than alter, the controlling rules.

---

# 62. Minimum Scenario Calibration Fields

A scenario calibration record shall include at minimum:

- Feature ID;
- Risk Scenario ID;
- Scenario Scope Key;
- scenario title;
- primary family;
- secondary families;
- failure-mode class;
- affected-subject class;
- consequence class;
- materiality disposition;
- assessment scope ID;
- calibration state;
- inherent severity;
- inherent likelihood;
- residual severity;
- residual likelihood;
- severity basis;
- likelihood factor basis;
- confidence;
- risk score where permitted;
- risk priority signal;
- control IDs;
- control layers;
- control effectiveness states;
- operating-credit class;
- governance-gate state;
- governance source references;
- governance urgency;
- activation proximity;
- evidence references;
- reviewer;
- review date;
- freshness state;
- notes.

---

# 63. History and Recalibration

Every material recalibration shall preserve predecessor values and record:

- change type;
- prior calibration ID;
- new calibration ID;
- trigger;
- changed evidence;
- changed scope;
- changed control state;
- changed authority state;
- reviewer;
- date;
- rationale.

Scope migration shall be explicit rather than silently overwriting the original calibration.

---

# 64. Risk Acceptance Boundary

This methodology does not perform risk acceptance.

A planning score, priority, or reconciled reviewer result shall not be represented as acceptance of residual risk.

Risk acceptance requires separate authorized governance appropriate to the subject.

---

# 65. Legal and Regulatory Inference Boundary

Reviewers may identify that a scenario appears to involve a legal, regulatory, contractual, consent, privacy, safeguarding, or compliance dependency.

They shall not convert an unverified legal proposition into established legal truth.

Where legal authority is material and not verified, route to the appropriate legal/governance review process.

---

# 66. Public Trust Boundary

Public trust/reputation may support a risk scenario where a supported failure mode could materially mislead, misrepresent, expose, or undermine legitimate reliance.

Reputation shall not be used as a vague severity multiplier detached from a concrete failure mode and consequence.

---

# 67. Validator Requirements

Validators shall test at minimum:

1. canonical scenario identity fields;
2. canonical scenario-scope pair keys;
3. duplicate IDs;
4. required family screening completeness;
5. material scenario registration;
6. no synthetic no-candidate Feature IDs;
7. no retroactive exercise category qualification;
8. valid severity values;
9. valid likelihood values;
10. valid score products;
11. invalid product scores rejected;
12. priority-matrix correctness;
13. CRITICAL priority floor;
14. insufficient-evidence blank score;
15. confidence not used as likelihood;
16. confidence not used as substantive controller tie-break;
17. no cross-scope averaging;
18. current exposure requires ACTIVE_NOW or equivalent current reachability;
19. `AUTHORIZED_NOT_ACTIVE` excluded from normal current exposure;
20. stale fallback not represented as calibrated current;
21. governance blank-risk ordering;
22. governance co-controller pair integrity;
23. snapshot canonical hash reproduction;
24. snapshot byte-length reproduction;
25. finalized snapshot immutability;
26. no upward control-credit override;
27. legacy `PARTIAL_IMPLEMENTATION` does not map to `PARTIALLY_VERIFIED` without verification evidence;
28. governance coverage state does not mechanically set urgency;
29. `GATE_STATUS_UNKNOWN` routes to authority review;
30. `GATE_STATUS_UNKNOWN` defaults to `PLANNED` absent stronger condition;
31. documentary exercise reachability does not derive from current inactivity;
32. deterministic exercise candidate qualification;
33. deterministic required-selection union;
34. deterministic exercise target size;
35. required-union over-30 exception;
36. no down-selection of required exercise features;
37. methodology freeze requires accession integrity evidence.

---

# 68. Change Control

A methodology change is material where it changes:

- scenario identity;
- required scenario families;
- materiality test;
- consequence anchors;
- likelihood definitions;
- control-credit ceiling;
- risk arithmetic;
- priority matrix;
- governance-gate rules;
- governance urgency;
- controller algorithms;
- scope semantics;
- exercise selection or pass criteria;
- authority boundaries.

Material changes require controlled review before broad recalibration.

Clarifications that resolve demonstrated ambiguity without altering product policy shall still be versioned, reviewed, accessioned, and frozen before broad use.

---

# 69. V3.2.2 Change Scope

Version 3.2.2 intentionally makes only the five bounded clarification changes identified by the completed calibration exercise:

- `V322-CLR-AMB-01`
- `V322-CLR-AMB-02`
- `V322-CLR-AMB-03`
- `V322-CLR-AMB-07`
- `V322-CLR-AMB-08`

No new Founder product-policy decision is introduced.

No risk arithmetic is changed.

No priority matrix is changed.

No severity scale is changed.

No likelihood scale is changed.

No controller substantive ranking is changed except the explicit unknown-gate urgency default already identified by the exercise as necessary clarification.

No implementation or runtime authority is created.

`NEW_FOUNDER_PRODUCT_DECISION_REQUIRED = NO`

---

# 70. Methodology Freeze Preconditions

Canonical methodology freeze requires:

1. exact final methodology bytes;
2. final version identifier;
3. final canonical path;
4. repository/source identity;
5. accession commit or equivalent canonical custody reference;
6. SHA-256;
7. byte length;
8. manifest;
9. checksum verification;
10. clarification verification report;
11. bounded exercise evidence reference;
12. authority-boundary confirmation;
13. freeze disposition/receipt.

A local file or detached archive may be checksum-frozen as evidence, but shall not be represented as canonical repository accession unless the canonical repository custody step actually occurs.

---

# 71. Full 314-Feature Recalibration Gate

The 314-feature documentary recalibration may begin only after:

- V3.2.2 clarification integration is complete;
- clarification verification passes;
- exact methodology bytes are accessioned and frozen in canonical custody;
- required companion schemas/registers for recalibration are fixed;
- the recalibration work package identifies the authoritative 314-feature source population;
- no implementation/runtime authority is inferred from the documentary recalibration.

The recalibration shall then perform:

1. complete 19-family discovery screening for all 314 features;
2. registration of all material and insufficient-evidence-retained scenarios;
3. required scope-specific calibrations;
4. control/evidence classification;
5. governance-gate and urgency classification;
6. controller derivation;
7. anti-templating validation;
8. queue regeneration;
9. Matrix derivative regeneration;
10. targeted independent rereview;
11. FDQ-003 Founder disposition.

---

# 72. FDQ-003 Closure Gate

FDQ-003 remains open until all of the following are complete:

1. methodology clean closure;
2. bounded methodology exercise pass;
3. methodology accession/freeze;
4. 314/314 feature discovery screening;
5. all material scenarios registered;
6. all required scope calibrations complete;
7. anti-templating validation passed;
8. risk queues regenerated;
9. Matrix derivatives regenerated;
10. independent risk rereview passed;
11. Founder disposition recorded.

Recommended final disposition, if all gates later pass:

`FDQ-003 = APPROVED_AS_NONAUTHORITATIVE_GOVERNANCE_PLANNING_SIGNAL`

---

# 73. Mandatory Qualifiers

`RISK_SCORE_DOES_NOT_ESTABLISH_PILOT_AUTHORITY = TRUE`

`RISK_SCORE_DOES_NOT_ESTABLISH_RELEASE_AUTHORITY = TRUE`

`RISK_SCORE_DOES_NOT_ESTABLISH_PRODUCTION_AUTHORITY = TRUE`

`RISK_SCORE_DOES_NOT_ESTABLISH_CONFORMITY = TRUE`

`RISK_SCORE_DOES_NOT_ESTABLISH_RISK_ACCEPTANCE = TRUE`

`RISK_SCORE_DOES_NOT_REPLACE_DOMAIN_SPECIFIC_SAFETY_REVIEW = TRUE`

`RISK_SCORE_DOES_NOT_REPLACE_SAFEGUARDING_REVIEW = TRUE`

`RISK_SCORE_DOES_NOT_REPLACE_SECURITY_REVIEW = TRUE`

`RISK_SCORE_DOES_NOT_REPLACE_FINANCIAL_CONTROL_REVIEW = TRUE`

`RISK_SCORE_DOES_NOT_REPLACE_LEGAL_REVIEW = TRUE`

---

# 74. Readiness Questions

## 74.1 Can a reviewer operate the methodology without unauthorized product decisions?

`YES_WITH_EVIDENCE`

## 74.2 Can QA objectively test the methodology rules?

`YES_WITH_EVIDENCE`

## 74.3 Can a reviewer trace outputs to governance, evidence, and the Matrix source?

`YES_WITH_EVIDENCE`, subject to the accession package and source snapshot used for each recalibration.

## 74.4 Is the product capability operationally ready because this methodology exists?

`NO`

## 74.5 Is first-user enrollment authorized by this methodology?

`NO`

---

# 75. Current Documentary State

`DOCUMENT_ID = EQUINESYNC_RISK_CALIBRATION_METHODOLOGY_V3_2`

`VERSION = 3.2.2`

`STANDALONE_SUCCESSOR = TRUE`

`PRIOR_METHODOLOGY_REQUIRED_FOR_OPERATION = FALSE`

`BOUND_CALIBRATION_EXERCISE_COMPLETE = TRUE`

`BOUND_CALIBRATION_EXERCISE_PASS = TRUE`

`AMB_01_RESOLVED = TRUE`

`AMB_02_RESOLVED = TRUE`

`AMB_03_RESOLVED = TRUE`

`AMB_07_RESOLVED = TRUE`

`AMB_08_RESOLVED = TRUE`

`OPEN_EXERCISE_METHODOLOGY_AMBIGUITIES = 0`

`METHODOLOGY_CLARIFICATION_INTEGRATION_COMPLETE = TRUE`

`METHODOLOGY_FREEZE_CANDIDATE = TRUE`

`CANONICAL_REPOSITORY_ACCESSION_COMPLETE = FALSE_PENDING_REPOSITORY_PUBLISH`

`CANONICAL_METHODOLOGY_FROZEN = FALSE_PENDING_REPOSITORY_ACCESSION`

`314_FEATURE_RECALIBRATION_READY = FALSE_PENDING_CANONICAL_ACCESSION_AND_FREEZE`

`FDQ_003_CLOSED = FALSE`

`IMPLEMENTATION_AUTHORIZED = FALSE`

`PILOT_AUTHORIZED_BY_THIS_ARTIFACT = FALSE`

`PRODUCTION_AUTHORIZED = FALSE`

`PUBLIC_LAUNCH_AUTHORIZED = FALSE`

---

# Appendix A — Priority Signal Sort Rank

For deterministic machine sorting:

- `VERY_HIGH_PRIORITY_SIGNAL = 4`
- `HIGH_PRIORITY_SIGNAL = 3`
- `MODERATE_PRIORITY_SIGNAL = 2`
- `LOW_PRIORITY_SIGNAL = 1`
- `EVIDENCE_REVIEW_REQUIRED` is routed separately and shall not receive a fabricated numeric risk rank.

---

# Appendix B — Governance Urgency Sort Rank

- `IMMEDIATE_BLOCKING = 5`
- `ACTIVE_REMEDIATION_REQUIRED = 4`
- `PRE_ACTIVATION_REQUIRED = 3`
- `PLANNED = 2`
- `DEFERRED = 1`

---

# Appendix C — Clarification Traceability

| Clarification | Exercise Source | Final Rule Location |
|---|---|---|
| AMB-01 | Reviewer B ambiguity log; coordinator exercise closure | §8 |
| AMB-02 | Reviewer B ambiguity log; coordinator exercise closure | §32 |
| AMB-03 | Reviewer B ambiguity log; coordinator exercise closure | §36 |
| AMB-07 | Reviewer B blind normalization supplement | §23 |
| AMB-08 | Reviewer B blind normalization supplement; coordinator prospective normalization | §37 |

---

# Appendix D — Exercise Evidence Limitation

The bounded exercise demonstrates that the methodology can be applied independently and reconciled without unresolved material disagreement after the identified clarifications.

The exercise does **not** establish a complete raw scenario-discovery-overlap statistic because Reviewer A's full 38-scenario discovery register was not independently hash-locked before comparison.

This is a custody/evidence limitation, not a license to erase known scenario-discovery differences or to overstate reproducibility.

The full 314-feature recalibration shall preserve complete scenario discovery and calibration artifacts with accession-grade hashes from the outset.

---

# Final Documentary Disposition

`EQUINESYNC_RISK_CALIBRATION_METHODOLOGY_V3_2_VERSION_3_2_2 = FULLY_CONSOLIDATED_CALIBRATION_EXERCISE_CLARIFIED_FREEZE_CANDIDATE`

This version is ready for targeted clarification verification and canonical accession/freeze.

It does not itself authorize the 314-feature recalibration until canonical methodology accession and freeze are complete.
