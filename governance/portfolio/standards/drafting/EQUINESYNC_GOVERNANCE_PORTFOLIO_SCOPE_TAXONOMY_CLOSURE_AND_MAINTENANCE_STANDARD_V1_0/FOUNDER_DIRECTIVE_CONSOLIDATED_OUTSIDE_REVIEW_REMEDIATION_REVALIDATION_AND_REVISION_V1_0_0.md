# FOUNDER DIRECTIVE

## EQUINESYNC GOVERNANCE PORTFOLIO SCOPE, TAXONOMY, CLOSURE, AND MAINTENANCE STANDARD

### CONSOLIDATED OUTSIDE-REVIEW REMEDIATION, REVALIDATION, AND REVISION DIRECTIVE

**Directive status:** FOUNDER-ISSUED REVISION DIRECTIVE
**Target artifact:** `EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0`
**Current reviewed version:** Second Draft / strengthened revision candidate
**Review inputs:** Cursor independent review, Claude independent review, and Perplexity independent expert review
**Authority effect:** Authorization to revise, validate, and prepare a new documentary candidate only
**No authority granted for:** adoption, activation, implementation, pilot authorization, production use, certification issuance, automatic finding closure, or representation that the standard is authoritative or verified

---

# 1. PURPOSE

Codex shall revise the Governance Portfolio Scope, Taxonomy, Closure, and Maintenance Standard and its complete supporting package in response to the consolidated findings of the Cursor, Claude, and Perplexity reviews.

The reviewers broadly agree that the conceptual framework is strong, particularly its separation of:

* artifact class;
* lifecycle state;
* authority event;
* readiness result;
* evidence status;
* documentary evidence;
* implementation evidence;
* adoption;
* lock;
* custody;
* activation;
* pilot authorization; and
* production authorization.

Those strengths shall be preserved.

The principal deficiency is not the conceptual model. It is the present package’s execution, internal consistency, validation integrity, enforceability, machine readability, maintainability, and operational proportionality.

The next revision shall therefore preserve the governance architecture while correcting all material defects identified through the outside-review process.

---

# 2. CONTROLLING REVIEW POSTURE

Codex shall treat the three outside reviews as complementary rather than competing.

The consolidated review posture is:

1. **Cursor:** operational clarity, lifecycle usability, workflow practicality, document ambiguity, and implementation feasibility.
2. **Claude:** governance completeness, semantic validation, evidence classification, missing governance domains, risk differentiation, and avoidance of documentary overclaim.
3. **Perplexity:** formal assurance, schema integrity, validation truthfulness, machine-readable traceability, exception controls, auditability, privacy, succession, revocation, records, and maintainability.

Where multiple reviewers raised the same theme, Codex shall treat the issue as a mandatory consensus finding.

Where only one reviewer identified a defect, Codex shall assess it on its substance and severity rather than excluding it because it was not independently duplicated.

The Perplexity review’s `NOT READY` determination shall be treated as controlling for the current package because it identifies specific fail-closed defects in the validation and machine-readable evidence.

---

# 3. REQUIRED STATUS OF THE CURRENT PACKAGE

Before making substantive revisions, Codex shall record the present package status truthfully as:

`OUTSIDE_REVIEW_COMPLETE_REVISION_REQUIRED_NOT_READY_FOR_FOUNDER_APPROVAL`

Codex shall not describe the reviewed second draft as:

* validated;
* closure-ready;
* adoption-ready;
* authoritative;
* verified;
* production-ready;
* implementation-verified;
* audit-ready; or
* approved.

Any existing statement that implies those outcomes shall be corrected or expressly qualified.

---

# 4. MANDATORY CONSENSUS FINDINGS

The following findings reflect material convergence across the outside reviews and shall be treated as mandatory.

## 4.1 Validation must not overstate verification

Codex shall ensure that:

* no unexecuted check is reported as `PASS`;
* no pending check contributes to an overall passing status;
* automated structural validation is not represented as semantic governance validation;
* documentary validation is not represented as implementation verification;
* repository discovery is not represented as proof of implementation;
* source-location assertions are not represented as independently verified unless the exact bytes are available;
* every validation result identifies the evidence actually examined; and
* every check records whether it was executed, not executed, pending, failed, or passed.

At minimum, the validation result vocabulary shall include:

* `PASS`;
* `FAIL`;
* `NOT_EXECUTED`;
* `PENDING`;
* `NOT_APPLICABLE`; and
* `BLOCKED`.

A package containing any required `NOT_EXECUTED`, `PENDING`, `FAIL`, or unresolved `BLOCKED` check shall not receive an overall `PASS`.

## 4.2 Structural validation and substantive validation must be separated

Codex shall distinguish:

1. file presence validation;
2. checksum and byte-length validation;
3. schema validation;
4. pointer and reference resolution;
5. internal consistency validation;
6. semantic human review;
7. repository evidence review;
8. implementation verification; and
9. production-operational verification.

Each category shall have a separate result.

No category shall substitute for another.

## 4.3 Machine-readable controls must be functional

Codex shall repair:

* unresolved machine-readable pointers;
* schema-to-template contradictions;
* inconsistent field names;
* missing class-specific schema requirements;
* missing revocation status;
* missing supersession relationships;
* missing certification indexing;
* unresolved section references;
* inconsistent lifecycle values; and
* any field that appears populated but contains boilerplate instead of meaningful information.

## 4.4 Evidence provenance must be explicit

Each source and evidence record shall distinguish among:

* exact repository-native source bytes;
* exact non-repository attachment bytes;
* documentary discovery;
* keyword-matched repository evidence;
* manually reviewed repository evidence;
* implementation-verified evidence;
* production-observed evidence;
* unavailable evidence; and
* evidence accepted through an authorized exception.

Codex shall not use `RESOLVED` where the evidence is not independently retrievable.

## 4.5 Governance must be maintainable

Codex shall eliminate unnecessary duplication and establish one declared normative source of truth.

Derived Markdown, CSV, JSON, templates, manifests, and validation artifacts shall be generated or deterministically reconciled from the normative source wherever practical.

The package shall include the generator or transformation logic necessary to reproduce derived artifacts.

## 4.6 Founder authority must be bounded and operationally defensible

Codex shall preserve Founder authority while defining:

* a non-waivable governance core;
* the limits of procedural override authority;
* the effect of external law;
* delegation mechanics;
* succession and incapacity treatment;
* revocation;
* expiration;
* required durable records;
* challenge and defect-reporting mechanisms; and
* treatment of conflicts where the Founder is drafter, certifier, risk acceptor, and production authorizer.

## 4.7 Terminology must be precise

Codex shall define all terms that carry material governance effect, including:

* Founder;
* delegated authority;
* durable record;
* material;
* non-material;
* proportionate;
* disproportionate;
* sound;
* incident;
* competent authority;
* protected repository state;
* exact source bytes;
* implementation-verified;
* production-observed;
* accepted residual risk;
* temporary waiver;
* exception;
* substitution;
* override;
* revocation;
* suspension; and
* closure.

---

# 5. PHASE 1: BLOCKING CORRECTIONS

Phase 1 shall be completed before Codex represents the package as ready for another substantive review.

## 5.1 Regenerate the validation report truthfully

Codex shall replace or regenerate `DOCUMENTARY_VALIDATION_REPORT.json`.

Every validation row shall include, where applicable:

* `check_id`;
* `requirement`;
* `check_type`;
* `command`;
* `executed_at_utc`;
* `executed_by`;
* `exit_code`;
* `evidence_reference`;
* `result`;
* `blocking_effect`;
* `limitations`; and
* `remediation_status`.

Any previously recorded `PASS` for an unexecuted check shall be corrected to `NOT_EXECUTED` or `PENDING`.

Codex shall specifically re-evaluate all validation checks corresponding to the findings identified in the outside reviews, including the checks previously labeled `VAL-016`, `VAL-019`, `VAL-023`, `VAL-024`, and `VAL-025`.

The validation report shall include a machine-readable acknowledgement that the prior report contained overstated results and has been superseded.

## 5.2 Add a validation-integrity rule

Add a normative rule equivalent to:

`ES-GPS-VALID-001`

A validation record may not report an unexecuted, incomplete, unresolved, or unsupported check as passed. Doing so constitutes a non-falsification violation and blocks overall validation.

## 5.3 Repair machine-readable pointers

All machine-readable references shall resolve deterministically.

Codex shall use one stable reference method, preferably RFC 6901 JSON Pointer or another clearly documented canonical scheme.

Every pointer shall be tested automatically.

The build shall fail if any pointer does not resolve.

## 5.4 Repair section references

Numeric section references that are vulnerable to renumbering shall be replaced with stable anchors or rule identifiers.

Every section or anchor reference shall be validated automatically.

## 5.5 Reconcile certification requirements

Codex shall designate one normative source for certification field requirements.

Recommended approach:

* JSON Schema is normative for field structure;
* the Markdown standard, certification matrix, templates, and examples are generated from or checked against the schema.

The following must agree:

* Section 15 or its successor section;
* `FOUNDER_CERTIFICATION_WAIVER_SUBSTITUTION_AND_OVERRIDE_MATRIX.csv`;
* `FOUNDER_CERTIFICATION_MACHINE_READABLE_SCHEMA.json`;
* all certification templates;
* worked examples; and
* validation rules.

## 5.6 Add class-specific schema requirements

The schema shall use conditional requirements for each certification class.

At minimum:

### FCR-01 Historical evidence certification

Require:

* unavailable historical source;
* efforts to locate the source;
* substituted evidence;
* limitations;
* affected claims;
* review trigger;
* expiration or review date; and
* explicit statement that historical fact is not being rewritten.

### FCR-02 Current-state certification

Require:

* exact current baseline;
* inspected repository state;
* evidence examined;
* exclusions;
* unresolved uncertainty;
* affected claims; and
* scope limitations.

### FCR-03 Test waiver

Require:

* exact waived test;
* reason;
* risk;
* duration;
* compensating controls;
* expiration;
* reopening trigger; and
* prohibited claims.

Permanent waivers shall not be allowed.

### FCR-04 Test deferral

Require:

* deferred test;
* due date;
* interim controls;
* owner;
* blocking consequences;
* expiration; and
* trigger for mandatory completion.

### FCR-05 Alternative evidence acceptance

Require:

* original evidence requirement;
* alternative evidence;
* equivalence analysis;
* known limitations;
* residual risk;
* expiration or review trigger; and
* affected claims.

### FCR-06 Pilot evidence substitution

Require:

* environment;
* exact build or commit;
* cohort;
* duration;
* feature scope;
* data scope;
* provenance;
* lawful basis or consent;
* participant notice;
* privacy minimization;
* retention period;
* limitations;
* anomalies;
* substituted requirement;
* stop conditions;
* incident treatment; and
* DPIA or documented DPIA-not-required determination.

### FCR-07 Soundness certification

Require:

* reviewed scope;
* evidence relied upon;
* technical basis;
* documentary basis;
* operational basis;
* unresolved defects;
* reviewer identity;
* prohibited inferences; and
* expiration or reopening trigger.

### FCR-08 Residual-risk acceptance

Require:

* risk statement;
* likelihood;
* impact;
* affected scope;
* compensating controls;
* owner;
* review date;
* trigger for reconsideration;
* hiring or maturity trigger where segregation of duties is unavailable; and
* consequences if the risk materializes.

### FCR-09 Procedural override

Require:

* exact gate being overridden;
* harm or burden caused by the gate;
* proportionality analysis;
* external-obligation check;
* compensating control;
* duration;
* scope;
* independent or second-party review where available;
* non-waivable-core confirmation; and
* revocation trigger.

### FCR-10 Production authorization

Require:

* exact commit SHA or release identifier;
* environment;
* feature scope;
* data scope;
* user scope;
* accepted exceptions;
* unresolved risks;
* stop conditions;
* rollback conditions;
* effective date;
* expiration or review trigger;
* second-reviewer attestation where available; and
* explicit statement that the authorization applies only to the identified release and scope.

## 5.7 Add certification status and relationship fields

The certification schema and register shall include:

* `status`;
* `issued_at`;
* `effective_at`;
* `expires_at`;
* `supersedes`;
* `superseded_by`;
* `revokes`;
* `revoked_by`;
* `revocation_date`;
* `suspension_reason`;
* `narrowed_scope`;
* `dependent_claim_effect`; and
* `review_trigger`.

Permitted status values shall include:

* `ACTIVE`;
* `EXPIRED`;
* `REVOKED`;
* `SUSPENDED`;
* `SUPERSEDED`;
* `NARROWED`; and
* `SATISFIED_BY_EVIDENCE`.

## 5.8 Add the non-waivable core

Add a normative rule:

`ES-GPS-CORE-001`

The following shall be non-waivable:

* non-falsification;
* external-law limitations;
* requirement for a durable authority record;
* prohibition on unsupported overclaim;
* exact-scope requirement for production authorization;
* record of procedural override;
* machine-readable record for FCR-09 and FCR-10;
* preservation of historical facts;
* revocation and supersession traceability; and
* truthful reporting of unexecuted validation.

FCR-09 shall expressly lack authority to override the non-waivable core.

---

# 6. PHASE 2: CONTROL-CLOSURE REQUIREMENTS

## 6.1 Close the lifecycle state machine

Codex shall review all lifecycle states for inbound and outbound transition completeness.

Add or correct transitions for:

* `LOCKED`;
* `SUSPENDED`;
* `REOPENED`;
* `FOUNDER_CERTIFIED_EXCEPTION`;
* `REJECTED`;
* `RETIRED`;
* `SUPERSEDED`;
* `PILOT_AUTHORIZED`; and
* any other state currently terminal or unreachable without express intent.

At minimum, add:

* `LOCKED → ACCESSION_PENDING`;
* `SUSPENDED → prior authorized state, NARROWED, SUPERSEDED, or RETIRED`;
* `REOPENED → RECLOSED, SUSPENDED, SUPERSEDED, or RETIRED`;
* `FOUNDER_CERTIFIED_EXCEPTION → EXPIRED, REVOKED, SATISFIED_BY_EVIDENCE, or SUPERSEDED`;
* permitted paths into `REJECTED`; and
* permitted paths into `RETIRED`.

Add automated checks that:

* every non-terminal state has an outbound transition;
* every non-initial state has an inbound transition;
* authority matrices and lifecycle transition matrices agree; and
* every `allowed_next_event` maps to a permitted transition.

## 6.2 Prohibit permanent waivers

Replace permanent waivers with:

* a maximum duration;
* a mandatory review date;
* a renewal record; or
* a formal amendment removing the underlying control.

Default maximum waiver duration shall be 12 months unless a shorter period is required by the risk.

Any waiver open longer than 180 days shall be highlighted in the quarterly governance review.

## 6.3 Establish an exception budget

Add automatic review triggers when:

* more than five waivers are open;
* any critical control is waived;
* any waiver exceeds 180 days;
* multiple waivers affect the same artifact or release;
* a waiver reaches its expiration date;
* an FCR-09 override remains open beyond its approved period; or
* exception density exceeds a defined threshold.

## 6.4 Create a certification register

Add `CERTIFICATION_REGISTER.csv` or an equivalent machine-readable authoritative register.

Required fields:

* certification ID;
* class;
* status;
* issue date;
* effective date;
* expiration date;
* scope summary;
* artifact path;
* SHA-256;
* certifying authority;
* second reviewer, if applicable;
* supersedes;
* superseded by;
* revokes;
* revoked by;
* review trigger;
* current owner; and
* limitations.

Define and enforce a certification ID grammar.

Recommended grammar:

`ES-FCR-[CLASS]-[YEAR]-[SEQUENCE]`

Example:

`ES-FCR-10-2026-001`

## 6.5 Add revocation and narrowing instruments

Codex shall create:

* a revocation record;
* a narrowing record;
* a suspension record;
* a supersession record; and
* corresponding templates or generated forms.

A downstream consumer shall be able to determine whether a certification remains active without manually inspecting unrelated documents.

## 6.6 Add role definitions and assignments

Create `ROLE_DEFINITION_AND_ASSIGNMENT_MATRIX.csv`.

For each governance role, include:

* role ID;
* role name;
* responsibilities;
* authority;
* required competency;
* current holder;
* backup holder;
* conflict-of-interest limitations;
* vacancy treatment; and
* default-holder rule.

Where the Founder currently fills multiple roles, record the concentration of authority explicitly rather than implying segregation that does not exist.

Where appropriate, create an FCR-08 record accepting the temporary segregation-of-duties risk and defining a trigger for reassignment upon hiring or governance expansion.

## 6.7 Add delegation and succession controls

Create:

* a Founder delegation instrument;
* a delegation register;
* revocation treatment;
* scope and duration requirements;
* incapacity and unavailability provisions;
* standing alternate authority provisions; and
* treatment of expiring certifications during Founder unavailability.

A delegation shall not exceed its written scope.

Delegated authority shall not include the ability to expand its own delegation.

## 6.8 Add second-review safeguards

For FCR-09 and FCR-10, require a second named reviewer’s attestation where a qualified second reviewer is available.

Where none is available:

* disclose the absence;
* record the risk through FCR-08;
* impose a later-review trigger;
* require outside review for material production or procedural override decisions; and
* prohibit describing the decision as independently approved.

## 6.9 Add a defect-reporting and challenge channel

Create a documented method through which an employee, contractor, reviewer, advisor, customer representative, or other authorized person may report:

* suspected non-falsification violations;
* unsupported overclaims;
* invalid certifications;
* undisclosed conflicts;
* privacy concerns;
* implementation discrepancies; or
* incorrect closure claims.

A credible report shall automatically create a reopening trigger.

Disposition shall require a written record.

## 6.10 Add privacy and pilot evidence controls

Pilot authorization and pilot-evidence substitution shall require:

* lawful basis or participant consent;
* participant notice;
* data minimization;
* retention limits;
* pseudonymization where practical;
* protection of minors’ data;
* treatment of payment and financial data;
* subprocessor or vendor treatment;
* incident response;
* breach escalation;
* data deletion or redaction procedures;
* DPIA or documented DPIA-not-required determination; and
* automatic suspension following a material personal-data incident.

The governance evidence package shall preserve the record of evidence without unnecessarily retaining raw personal data.

## 6.11 Add regulatory applicability mapping

Create a regulatory and external-obligation applicability register addressing, where applicable:

* state privacy laws;
* CCPA/CPRA;
* GDPR or UK GDPR;
* children’s and minors’ privacy requirements;
* PCI DSS boundaries;
* employment or contractor records;
* safeguarding duties;
* contractual obligations;
* vendor obligations; and
* any equine, facility, veterinary, or professional requirements relevant to the governed product scope.

The register shall distinguish:

* applicable;
* potentially applicable;
* not currently applicable;
* outside product scope; and
* requires legal confirmation.

## 6.12 Add records retention rules

Codex shall define:

* retention periods;
* archival location;
* immutable record treatment;
* deletion and redaction procedures;
* legal-hold treatment;
* format migration;
* checksum preservation;
* access controls; and
* reconciliation of evidence preservation with privacy erasure duties.

---

# 7. PHASE 3: MAINTAINABILITY AND AUTOMATION

## 7.1 Declare a single normative source

Codex shall identify one authoritative machine-readable source.

Recommended source:

`EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0.json`

The Markdown standard, matrices, templates, field dictionaries, and validation views shall be generated from or deterministically checked against that source.

## 7.2 Commit the generator

The package shall contain or reference repository-native generator logic.

The generator shall:

* generate Markdown;
* generate CSV matrices;
* generate certification templates;
* generate field dictionaries;
* generate reference indexes;
* regenerate manifests;
* regenerate checksums; and
* fail if derived artifacts drift.

## 7.3 Commit the validator

The package shall include a validator with a documented CLI contract.

It shall verify:

* schema conformance;
* template conformance;
* pointer resolution;
* heading and anchor resolution;
* lifecycle transition closure;
* matrix agreement;
* rule-ID resolution;
* duplicate IDs;
* certification-ID grammar;
* checksum integrity;
* manifest completeness;
* derived-file regeneration;
* unresolved placeholder values;
* unavailable sources;
* prohibited overclaims;
* validation result truthfulness; and
* restricted path scope.

## 7.4 Require CI enforcement

Governance-path changes shall not pass validation solely because a local report says they passed.

Codex shall define a required CI status check for governance changes.

The next draft shall identify:

* workflow path;
* command;
* expected exit-code behavior;
* required branch protection;
* failure consequences; and
* evidence artifact produced by CI.

## 7.5 Add tamper-evidence controls

Codex shall evaluate and implement, where feasible:

* signed commits;
* signed annotated tags;
* CODEOWNERS for governance paths;
* protected branches;
* signed checksum manifests;
* independent package hash anchoring; and
* immutable release references.

If a recommended tamper-evidence mechanism cannot be implemented immediately, record the limitation and compensating control truthfully.

## 7.6 Normalize package naming and versioning

Use semver or another deterministic version scheme.

Do not embed lifecycle prose such as `strengthened-revision-candidate` inside the version identifier.

Maintain status in a separate status field.

Shorten excessively long directory and file paths where practical.

## 7.7 Remove duplicated normative content

Where prose duplicates a matrix field-for-field, either:

* generate it automatically; or
* reference the matrix.

Do not maintain parallel handwritten versions of the same rule unless one is expressly declared non-normative.

---

# 8. PHASE 4: OPERATIONAL PROPORTIONALITY

The reviewers raised a legitimate concern that the standard may impose enterprise-scale ceremony on a founder-led organization.

Codex shall not solve that concern by weakening truthful controls or deleting important safeguards.

Instead, Codex shall design a proportionate operating model.

## 8.1 Create governance tiers

Consider at least two operational profiles:

### Full-control profile

Required for:

* Tier 1 governance canon;
* production authorizations;
* procedural overrides;
* personal-data processing;
* safeguarding;
* financial operations;
* security;
* privacy;
* AI governance;
* minors;
* critical implementation atlases;
* code guides governing production behavior; and
* material residual-risk acceptance.

### Lightweight profile

Permitted for:

* low-risk internal guidance;
* non-authoritative working documents;
* non-material corrections;
* editorial changes;
* low-impact reference material; and
* artifacts that do not authorize implementation, pilot, or production activity.

The lightweight profile shall not be used to bypass full controls for high-risk artifacts.

## 8.2 Dry-run the maintenance cycle

Before Founder approval, Codex shall prepare a documented dry-run plan for:

* monthly integrity review;
* quarterly governance review;
* pre-release review; and
* annual portfolio recertification.

The plan shall estimate:

* artifacts reviewed;
* sample size;
* expected hours;
* automation coverage;
* required human effort;
* unresolved staffing gaps; and
* recommended reductions where the workload is not sustainable.

## 8.3 Add governance health metrics

At minimum, define:

* open certifications by class;
* open waivers;
* waiver age;
* expired records;
* revoked records;
* unresolved findings;
* findings by severity;
* overdue reviews;
* unresolved source gaps;
* lifecycle-state distribution;
* evidence-status distribution;
* pointer failures;
* schema failures;
* mean time to closure;
* reopened findings;
* exception density by artifact;
* implementation-verification coverage; and
* production-verification coverage.

---

# 9. REVIEWER-SPECIFIC REQUIREMENTS

## 9.1 Cursor-derived requirements

Codex shall incorporate Cursor’s operational emphasis by:

* simplifying ambiguous workflows;
* ensuring lifecycle states can be applied by a practitioner;
* reducing unnecessary complexity;
* clarifying entry and exit criteria;
* clarifying who performs each action;
* clarifying which steps are mandatory;
* avoiding dead-end lifecycle states;
* ensuring the standard can be used during real product and governance work; and
* distinguishing documentary approval from implementation and production authority.

## 9.2 Claude-derived requirements

Codex shall incorporate Claude’s semantic and governance-completeness emphasis by:

* adding human semantic validation;
* distinguishing keyword matches from implementation proof;
* improving source lineage;
* improving risk differentiation;
* avoiding clustered or low-signal risk scores;
* breaking broad findings into actionable findings;
* assigning owners and resolution paths;
* reassessing missing governance domains;
* explicitly considering accessibility;
* vendor and third-party risk;
* AI model governance;
* independent security assessment;
* regulatory mapping;
* safeguarding;
* minors;
* privacy;
* repository evidence quality; and
* the accuracy of any PIA or foundational source relied upon by downstream mappings.

## 9.3 Perplexity-derived requirements

Codex shall incorporate the formal assurance findings, including:

* correction of false `PASS` attestations;
* repair of all broken machine-readable pointers;
* reconciliation of all certification schemas, matrices, and templates;
* class-specific schema controls;
* non-waivable governance core;
* succession and delegation;
* dual-control or explicit risk acceptance;
* pilot privacy and lawful-basis controls;
* lifecycle state-machine closure;
* prohibition on permanent waivers;
* revocation;
* certification register;
* stable section anchors;
* durable repository-native authority sources;
* role definition and assignment;
* generator and single source of truth;
* signed or anchored checksums;
* explicit supersession records;
* operational definitions;
* controlled lifecycle vocabulary in source registers;
* retention and archive policy;
* automation enforcement;
* governance metrics;
* AI authorship disclosure; and
* independent re-execution of machine-generated validation.

---

# 10. REQUIRED NEW OR REVISED ARTIFACTS

The next package shall include, as applicable:

1. revised human-readable standard;
2. revised normative JSON standard;
3. revised lifecycle-state and transition matrix;
4. revised authority-effect matrix;
5. revised adoption, lock, accession, custody, and activation matrix;
6. revised FCR matrix;
7. revised certification JSON Schema;
8. one generated template for each FCR class;
9. certification register;
10. revocation and supersession register or equivalent status fields;
11. role definition and assignment matrix;
12. Founder delegation template;
13. delegation register;
14. succession and incapacity section;
15. regulatory applicability register;
16. records-retention schedule;
17. governance health-metrics definition;
18. exception-budget rules;
19. machine-authorship and human-review rule;
20. validation-integrity rule;
21. non-waivable-core rule;
22. defect-reporting and challenge procedure;
23. generator source;
24. validator source;
25. CI workflow or draft workflow configuration;
26. regenerated documentary validation report;
27. outside-review finding disposition matrix;
28. source and authority register;
29. supersession and correction register;
30. package manifest;
31. checksum file;
32. signed checksum or signed tag evidence, if implemented;
33. README with accurate reading order; and
34. revision summary.

---

# 11. OUTSIDE-REVIEW FINDING DISPOSITION MATRIX

Codex shall create a complete matrix containing one row per outside-review finding.

Required fields:

* finding ID;
* reviewer;
* reviewer severity;
* normalized severity;
* finding title;
* affected artifacts;
* consensus or reviewer-specific classification;
* Founder disposition;
* accepted;
* accepted with modification;
* rejected;
* deferred;
* reason;
* remediation;
* changed files;
* validation method;
* remaining limitation;
* follow-up review required;
* closure status; and
* closure evidence.

No finding shall be silently omitted.

If a finding is rejected, Codex shall state the substantive reason.

“Not raised by other reviewers” is not a sufficient rejection rationale.

---

# 12. RISK MODEL REVISION

Codex shall revise any risk model that produces low differentiation or clusters most artifacts into a small number of values.

The revised model shall consider:

* authority consequence;
* personal-data sensitivity;
* minors and safeguarding;
* security impact;
* financial impact;
* production impact;
* external-law exposure;
* operational dependency;
* reversibility;
* evidence quality;
* implementation maturity;
* number and age of exceptions;
* concentration of authority;
* vendor dependence;
* AI involvement;
* scope breadth; and
* likelihood of overclaim.

The methodology shall explain how scores differ and why.

Risk scoring shall not create false mathematical precision.

---

# 13. SOURCE AND AUTHORITY CORRECTIONS

Codex shall:

* commit the controlling Founder directive into a stable repository-native governance path where possible;
* replace ephemeral local attachment paths with durable references;
* issue an FCR-01 where exact historical bytes remain unavailable;
* add unavailable foundational PIA or governance sources to the source register;
* distinguish unresolved source absence from resolved evidence;
* normalize lifecycle states in the source register;
* replace boilerplate predecessor and successor fields with actual values or null values;
* identify exact repository heads and commit ranges reviewed;
* record any protected-base movement;
* identify files changed in the intervening commit range; and
* explain the basis for any non-materiality conclusion.

---

# 14. HUMAN REVIEW AND AI AUTHORSHIP

Add a normative rule requiring each governance artifact to record:

* whether it was human-authored, AI-assisted, or AI-generated;
* the generating system or process, where applicable;
* the named human reviewer;
* the scope of human review;
* whether validation was independently re-executed;
* known limitations; and
* final accountable owner.

Machine-generated validation results shall not be relied upon solely because they were produced by the same process that generated the artifact.

A materially important validation shall be re-executed independently or by a separate process before being represented as passed.

---

# 15. REQUIRED VALIDATION BEFORE RETURN

Before returning the revised package, Codex shall execute and report:

1. package integrity validation;
2. manifest completeness validation;
3. checksum validation;
4. byte-length validation;
5. schema validation;
6. template-instantiation validation for every FCR class;
7. pointer-resolution validation;
8. section-anchor validation;
9. rule-ID resolution validation;
10. certification-ID uniqueness validation;
11. lifecycle inbound/outbound validation;
12. cross-matrix consistency validation;
13. generated-artifact no-diff validation;
14. controlled-vocabulary validation;
15. source-resolution validation;
16. placeholder and boilerplate detection;
17. prohibited-overclaim scan;
18. repository path-scope validation;
19. Git diff validation;
20. branch and head verification;
21. CI configuration validation;
22. human semantic review;
23. privacy-control review;
24. exception-authority review;
25. external-law limitation review; and
26. outside-review disposition completeness validation.

Each result shall be truthful and independently supportable.

---

# 16. REQUIRED RETURN FORMAT

Codex shall return:

## A. Executive summary

State:

* what changed;
* what remains unresolved;
* whether the package is ready for re-review;
* whether any blocking defect remains; and
* the exact truthful readiness status.

## B. Repository state

Include:

* repository;
* protected branch;
* starting head;
* working branch;
* final head;
* worktree status;
* PR number, if created;
* merge status; and
* confirmation that no unauthorized direct protected-branch mutation occurred.

## C. Artifact inventory

List every created, revised, superseded, or deleted file.

## D. Review disposition summary

Report:

* findings accepted;
* accepted with modification;
* rejected;
* deferred;
* unresolved;
* closed;
* requiring re-review; and
* reviewer-specific counts.

## E. Validation results

Provide all executed commands, exit codes, timestamps, and outputs or artifact references.

## F. Known limitations

Do not conceal:

* unavailable sources;
* pending CI;
* missing reviewers;
* unimplemented signing;
* staffing limitations;
* unresolved segregation of duties;
* external-law questions;
* repository constraints; or
* deferred controls.

## G. Final status

Use one truthful status only.

Permitted statuses include:

* `REVISION_COMPLETE_READY_FOR_TARGETED_OUTSIDE_REREVIEW`;
* `REVISION_COMPLETE_WITH_RETAINED_NONBLOCKING_LIMITATIONS`;
* `REVISION_INCOMPLETE_BLOCKING_DEFECTS_REMAIN`; or
* `REVISION_BLOCKED_SOURCE_OR_REPOSITORY_CONDITION`.

Do not use `READY_FOR_FOUNDER_APPROVAL` unless all blocking findings are closed and the critical corrections have received targeted independent re-review.

---

# 17. PROHIBITED ACTIONS

Codex shall not:

* mark unexecuted checks as passed;
* infer implementation from documentary coverage;
* infer production readiness from repository presence;
* treat Founder approval as adoption, activation, or production authorization;
* use a procedural override to waive the non-waivable core;
* retain permanent waivers;
* represent ephemeral source paths as durable evidence;
* close findings without explicit disposition and evidence;
* silently omit reviewer findings;
* create unsupported legal conclusions;
* claim regulatory compliance without a mapped basis;
* describe the package as independently validated where the generator validated itself;
* merge to a protected branch without express authority;
* activate any governance standard;
* authorize pilot use;
* authorize production use; or
* issue any FCR certification under this directive.

---

# 18. TARGET END STATE

The intended end state is a revised governance standard that:

* preserves the conceptual strengths recognized by all reviewers;
* reports validation truthfully;
* separates documentary, repository, implementation, and production evidence;
* has enforceable machine-readable controls;
* has a closed and usable lifecycle model;
* bounds Founder exception authority;
* supports delegation, succession, revocation, and challenge;
* protects pilot participants and personal data;
* provides durable, repository-native evidence;
* can be maintained without uncontrolled drift;
* is proportionate to EquineSync’s current organizational capacity;
* can survive enterprise, audit, legal, privacy, security, and regulatory scrutiny; and
* is ready for targeted independent re-review before Founder approval.

---

# 19. AUTHORITY LIMITATION

This directive authorizes documentary revision, repository-scoped validation, and creation of a new review candidate only.

It does not authorize:

* adoption;
* authoritative designation;
* activation;
* implementation;
* pilot use;
* production use;
* waiver issuance;
* risk acceptance;
* procedural override;
* production authorization;
* automatic closure of findings;
* merger without separate authority; or
* any representation that the standard has completed final review.

**Required controlling statement:**

`DOCUMENTARY_REVISION_AND_REVALIDATION_AUTHORIZED_NO_ADOPTION_ACTIVATION_IMPLEMENTATION_PILOT_PRODUCTION_OR_AUTOMATIC_CLOSURE_AUTHORITY`
