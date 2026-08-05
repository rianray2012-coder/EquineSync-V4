# FOUNDER DIRECTIVE

## GOVERNANCE PORTFOLIO SCOPE, TAXONOMY, CLOSURE, AND MAINTENANCE STANDARD

### ROUND 2 TARGETED RE-REVIEW FINDINGS REMEDIATION AND RETURN DIRECTIVE

**Directive status:** FOUNDER-ISSUED TARGETED REVISION DIRECTIVE
**Target package:** `EQUINESYNC_GOVERNANCE_PORTFOLIO_SCOPE_TAXONOMY_CLOSURE_AND_MAINTENANCE_STANDARD_V1_0`
**Current revision candidate:** Commit `77d58949e3f3ca3082e5cc3598c6607b7a3786f6`
**Pull request:** PR #77
**Review round:** Targeted Outside Re-Review, Round 2
**Reviewers:** Cursor, Claude, and Perplexity
**Current truthful status:** `TARGETED_REREVIEW_COMPLETE_ADDITIONAL_REVISION_REQUIRED`
**Authority granted:** Documentary revision, package-local validation, repository-scoped correction, and preparation of a new targeted re-review candidate only
**Authority not granted:** Adoption, authoritative designation, activation, implementation, pilot authorization, production authorization, FCR issuance, risk acceptance, procedural override, protected-branch merge, or automatic finding closure

---

# 1. PURPOSE

Codex shall revise the Governance Portfolio Scope, Taxonomy, Closure, and Maintenance Standard package in response to the Round 2 targeted independent re-review findings returned by Cursor, Claude, and Perplexity.

All three reviewers concluded that the revised candidate materially improved the standard but still requires additional revision before Founder review.

Codex shall treat the following as controlling:

`NEEDS_ADDITIONAL_REVISION_BEFORE_FOUNDER_REVIEW`

The purpose of this directive is not to redesign the full governance framework.

The purpose is to:

1. correct the remaining truthfulness and validation defects;
2. repair broken machine-readable and human-readable references;
3. correct lifecycle and certification dimensional conflicts;
4. strengthen evidence traceability;
5. remove schema pathways that permit empty authority records;
6. correct generator and CI behavior;
7. resolve retained legacy artifacts and missing supersession records;
8. operationalize independent review controls; and
9. return a complete, independently reviewable Round 3 candidate.

---

# 2. CONTROLLING REVIEW SOURCES

Codex shall use the following Round 2 review reports as controlling inputs:

1. Cursor Targeted Independent Re-Review Report, dated August 3, 2026;
2. Claude Round 2 Targeted Independent Re-Review; and
3. Perplexity Governance Standard Re-Review.

Codex shall preserve each reviewer’s finding identity, severity, reasoning, and evidence.

Findings shall not be collapsed merely because they arise from a common theme.

Where two or more reviewers identify substantially similar defects, Codex shall record:

`CONSENSUS_FINDING`

Where only one reviewer identifies a defect, Codex shall evaluate it on its substance and evidence.

No finding shall be rejected solely because another reviewer did not raise it.

---

# 3. REQUIRED INITIAL STATUS RECORD

Before revision begins, Codex shall record the current package status as:

`ROUND_2_TARGETED_REREVIEW_COMPLETE_ADDITIONAL_REVISION_REQUIRED_NOT_READY_FOR_FOUNDER_APPROVAL`

The package shall not be described as:

* Founder-review ready;
* adoption ready;
* authoritative;
* fully validated;
* independently validated;
* implementation verified;
* production verified;
* closure complete; or
* approved.

---

# 4. ROUND 2 FINDING DISPOSITION REQUIREMENT

Codex shall create or replace the outside-review finding disposition matrix with one row for every individual Round 2 finding.

The matrix shall not use generic consolidated rows in place of reviewer findings.

Required fields:

* `round`;
* `reviewer`;
* `review_report_filename`;
* `review_report_sha256`;
* `review_finding_id`;
* `reviewer_severity`;
* `normalized_severity`;
* `finding_title`;
* `finding_text_summary`;
* `affected_artifacts`;
* `consensus_classification`;
* `founder_disposition`;
* `accepted`;
* `accepted_with_modification`;
* `rejected`;
* `deferred`;
* `disposition_reason`;
* `remediation_required`;
* `changed_files`;
* `changed_sections_or_fields`;
* `validation_method`;
* `validation_command`;
* `validation_result`;
* `remaining_limitation`;
* `follow_up_review_required`;
* `closure_status`; and
* `closure_evidence`.

No `changed_files` field may be blank where remediation is claimed.

The existence of a file shall not, by itself, constitute closure evidence.

Closure evidence shall identify the exact:

* rule;
* field;
* schema condition;
* transition;
* template;
* validator assertion;
* test fixture;
* generated output; or
* recorded execution result

that resolves the finding.

Permitted closure statuses:

* `OPEN`;
* `PARTIALLY_REMEDIATED`;
* `REMEDIATED_PENDING_VALIDATION`;
* `REMEDIATED_PENDING_REREVIEW`;
* `CLOSED_BY_INDEPENDENT_REREVIEW`;
* `REJECTED_WITH_RECORDED_RATIONALE`; and
* `DEFERRED_WITH_BLOCKING_LIMITATION`.

Codex shall not use `CLOSED` merely because it made a change.

---

# 5. BLOCKING REMEDIATION REQUIREMENTS

The following items are mandatory and blocking.

## 5.1 Make validation reports derive from actual executions

The validation report shall no longer be generated from hardcoded result constants.

Codex shall redesign validation so that:

1. each executable check is actually executed;
2. the actual result is captured;
3. the actual exit code is captured;
4. stdout and stderr are retained;
5. the execution timestamp is recorded;
6. the executable or process identity is recorded;
7. the evidence artifact is referenced; and
8. the validation report is generated from captured results, not expected results.

The generator shall not assign `PASS` before executing the relevant check.

Required design:

* validator functions shall return structured result objects;
* a validation runner shall execute each validator function;
* the report builder shall consume only those structured results;
* a check without a captured execution result shall be `NOT_EXECUTED`, `PENDING`, or `BLOCKED`;
* a failed required check shall cause overall failure;
* a pending required check shall prevent overall `PASS`; and
* retained execution logs shall be included in the package.

At minimum, each machine-executable result shall include:

* `check_id`;
* `requirement`;
* `check_type`;
* `command_or_function`;
* `started_at_utc`;
* `completed_at_utc`;
* `executed_by`;
* `exit_code`;
* `stdout_artifact`;
* `stderr_artifact`;
* `evidence_reference`;
* `result`;
* `blocking_effect`; and
* `limitations`.

The generator shall not invoke itself as evidence that the validator passed.

The validator shall not rely on a report generated by the same code path as evidence of its correctness.

## 5.2 Correct all PASS results for human, legal, privacy, and external-review work

The following types of review may not be marked `PASS` based solely on Codex, the package generator, or the package validator:

* human semantic review;
* independent outside review;
* legal review;
* privacy-law review;
* regulatory applicability review;
* external-obligation review;
* independent exception-authority review;
* Founder review;
* production review; and
* implementation verification.

Unless the required qualified reviewer has actually completed the review and a durable record is included, the result shall be:

* `NOT_EXECUTED`;
* `PENDING`;
* `BLOCKED`; or
* `NOT_APPLICABLE`.

The following prior checks shall be re-evaluated specifically:

* `VAL-022`;
* `VAL-023`;
* `VAL-024`;
* `VAL-025`;
* `VCAT-006`; and
* any successor checks covering the same subject.

A limitation stating that legal confirmation remains required cannot coexist with `PASS`.

A check requiring targeted outside re-review cannot be marked `PASS` before that re-review is received.

Judgment-based checks shall not carry invented machine exit codes.

## 5.3 Repair all adversarial JSON and Markdown references

Codex shall repair or replace every reference in the `adversarial_review` structure.

The current dotted machine paths shall not be described as RFC 6901 JSON Pointers unless they are valid RFC 6901 pointers.

Codex shall choose one of the following designs:

### Preferred design

Replace every machine-readable reference with an RFC 6901 JSON Pointer beginning with `/`.

Replace every Markdown section reference with a stable HTML anchor or rule ID.

### Alternative design

Remove the `adversarial_review` reference fields and replace them with:

* `rule_ids`;
* `json_pointers`;
* `markdown_anchors`;
* `validator_check_ids`; and
* `evidence_artifact_paths`.

All adversarial references shall be validated programmatically.

The validator shall:

* enumerate every adversarial scenario;
* resolve every JSON Pointer;
* resolve every Markdown anchor;
* resolve every cited rule ID;
* fail on any unresolved reference; and
* fail if an adversarial scenario reports `PASS` without executable or documentary evidence.

Codex shall not leave all adversarial scenarios as unconditional `PASS`.

Each scenario shall have:

* scenario narrative;
* attack or misuse case;
* expected control behavior;
* evidence examined;
* test method;
* actual result;
* limitations; and
* reopening consequence.

## 5.4 Correct the human-readable source hash and byte length

The normative JSON’s `human_readable_source` object shall be regenerated from the actual current Markdown file.

Codex shall:

1. compute the actual SHA-256;
2. compute the actual byte length;
3. record both values in the normative JSON;
4. add a validator check that recomputes and compares them;
5. fail validation on mismatch; and
6. record the previous stale values as superseded historical data where appropriate.

The generator shall not carry forward the second draft’s digest or length.

## 5.5 Make `--check` strictly read-only

The generator’s `--check` mode shall not:

* write;
* overwrite;
* regenerate;
* repair;
* normalize;
* update timestamps;
* update manifests;
* update checksums; or
* mutate any package file.

Required behavior:

1. generate expected outputs in memory or in a temporary directory;
2. compare expected outputs against committed package files;
3. report differences;
4. exit nonzero if drift exists; and
5. preserve the working tree unchanged.

A separate explicit mode shall perform writes, such as:

`--write`

or:

`--regenerate`

Codex shall add a test proving that `--check` leaves all files byte-identical even when drift exists.

## 5.6 Verify committed checksums before regeneration in CI

The CI workflow shall verify committed integrity evidence before running any process that may regenerate artifacts.

Required order:

1. checkout;
2. verify committed `CHECKSUMS.sha256`;
3. verify committed manifest entries and byte lengths;
4. verify normative-source and Markdown cross-hashes;
5. run read-only generator drift check;
6. run validator;
7. run schema tests and negative fixtures;
8. run reference-resolution tests;
9. run lifecycle graph tests;
10. run finding-disposition completeness tests; and
11. upload retained validation logs.

No checksum file shall be regenerated before committed checksum verification.

The CI workflow shall fail if committed checksums do not match.

Any regeneration shall occur only in an explicit developer workflow, not inside validation CI.

## 5.7 Repair the outside-review disposition matrix one finding at a time

Codex shall ingest the three actual Round 2 reports as exact package sources.

For each report:

* preserve the original filename;
* record SHA-256;
* record byte length;
* preserve the full report bytes;
* assign stable source IDs; and
* map every reviewer finding individually.

Codex shall create one disposition row per:

* Cursor finding;
* Claude finding;
* Perplexity finding; and
* prior finding expressly re-evaluated by a reviewer.

Codex shall not substitute a generic `CONSENSUS` row for individual reviewer findings.

Where multiple findings overlap, add a `consensus_group_id`, but preserve each original row.

Codex shall verify:

* reviewer attribution;
* severity;
* finding ID;
* affected artifacts;
* changed files;
* closure evidence;
* validation result; and
* follow-up status.

The validator shall fail if:

* a source review finding has no disposition row;
* a disposition row has no source finding;
* reviewer attribution differs from the source report;
* `changed_files` is empty for a remediated finding;
* closure evidence merely repeats affected artifact names;
* a finding marked remediated still fails its cited validator check; or
* severity is changed without a recorded rationale.

## 5.8 Prohibit null or empty required FCR payloads

Required FCR payload fields shall not be satisfiable by:

* `null`;
* empty string;
* empty array;
* empty object; or
* whitespace-only content.

Codex shall:

1. remove `null` from required field type unions;
2. add `minLength: 1` to required strings;
3. add `minItems: 1` to required arrays;
4. add `minProperties: 1` to required objects;
5. add exact patterns where appropriate;
6. add semantic formats for dates and identifiers; and
7. add negative fixtures for every FCR class.

For FCR-10, require a valid:

* 40-character Git SHA;
* 64-character digest;
* or controlled release-tag grammar.

Fields identifying production scope shall not permit arbitrary empty strings.

The validator shall test at minimum:

* omitted required key;
* null required value;
* empty required string;
* whitespace-only string;
* empty array;
* empty object;
* malformed date;
* malformed commit SHA;
* invalid status;
* missing truth statement;
* wrong truth statement; and
* valid completed fixture.

## 5.9 Correct lifecycle terminal flags

`LIFECYCLE_STATE_DEFINITION_MATRIX.csv` shall contain a complete and accurate boolean terminal value for every lifecycle state.

Codex shall:

* mark true terminal states `TRUE`;
* mark non-terminal states `FALSE`;
* prohibit blank values;
* compute terminality from the transition graph;
* compare computed terminality to the matrix; and
* fail validation on mismatch.

The terminal state set shall not be hardcoded independently in the validator unless generated from the normative lifecycle source.

The normative source, matrix, generator, and validator shall use one terminal-state definition.

## 5.10 Remove certification and production authority from the lifecycle dimension or expressly redesign the model

Codex shall resolve the conflict between `ES-GPS-CLASS-001` and the current lifecycle design.

The preferred correction is to maintain separate orthogonal dimensions:

### Artifact lifecycle

Examples:

* DRAFTING;
* REVIEW_PENDING;
* REVIEWED;
* APPROVED;
* ADOPTED;
* LOCKED;
* ACCESSION_PENDING;
* REPOSITORY_ACCESSIONED;
* CUSTODY_COMPLETE;
* ACTIVE;
* SUSPENDED;
* REOPENED;
* RECLOSED;
* SUPERSEDED;
* RETIRED; and
* REJECTED.

### Authority-event status

Examples:

* IMPLEMENTATION_AUTHORIZED;
* PILOT_AUTHORIZED;
* PRODUCTION_AUTHORIZED;
* PRODUCTION_AUTHORIZED_WITH_EXCEPTIONS;
* AUTHORIZATION_REVOKED; and
* AUTHORIZATION_EXPIRED.

### Certification status

Examples:

* ACTIVE;
* EXPIRED;
* REVOKED;
* SUSPENDED;
* SUPERSEDED;
* NARROWED; and
* SATISFIED_BY_EVIDENCE.

### Evidence status

Examples:

* VERIFIED;
* NOT_VERIFIED;
* WAIVED;
* DEFERRED;
* SUBSTITUTE_EVIDENCE_ACCEPTED;
* UNAVAILABLE;
* BLOCKED; and
* PENDING.

Codex shall remove from the artifact lifecycle any value that is properly:

* a certification status;
* an authority event;
* an evidence result; or
* a production authorization outcome.

At minimum, Codex shall reassess:

* `FOUNDER_CERTIFIED_EXCEPTION`;
* `PRODUCTION_AUTHORIZED_WITH_EXPRESS_EXCEPTIONS`;
* `IMPLEMENTATION_AUTHORIZED`;
* `PILOT_AUTHORIZED`;
* `EXPIRED`;
* `REVOKED`;
* `NARROWED`; and
* `SATISFIED_BY_EVIDENCE`.

If Codex elects not to separate the dimensions, it shall provide a formal design amendment that:

1. explains why the combined model does not violate `ES-GPS-CLASS-001`;
2. defines concurrent-state semantics;
3. defines precedence rules;
4. defines which model controls claim validity;
5. removes duplicate status representations;
6. updates all matrices consistently; and
7. receives targeted re-review.

Silently retaining the conflict is prohibited.

## 5.11 Add a clean production path with zero exceptions

The lifecycle and authority model shall include an explicit production authorization path for a release with no exceptions.

Required production authority outcomes:

* `PRODUCTION_AUTHORIZED_NO_EXCEPTIONS`; and
* `PRODUCTION_AUTHORIZED_WITH_EXPRESS_EXCEPTIONS`.

A clean authorization shall require:

* exact release identity;
* exact commit or release tag;
* environment;
* feature scope;
* data scope;
* user scope;
* evidence relied upon;
* unresolved-risk statement;
* explicit zero-exception attestation;
* stop conditions;
* rollback conditions;
* effective date;
* expiration or review trigger; and
* required second review.

The clean path shall not require an artificial exception record.

The exception path shall remain distinct and shall require an explicit exception inventory.

No rule shall imply that all production authorizations necessarily contain exceptions.

## 5.12 Supersede or remove legacy templates

The two retained legacy root-level certification templates shall not coexist with the generated FCR template system unless they are regenerated from the same normative schema.

Codex shall either:

### Option A: Remove and supersede

* create an explicit supersession record;
* identify predecessor templates;
* identify successor templates;
* preserve exact predecessor hashes;
* explain retained historical value;
* remove them from active use; and
* update README and manifest.

### Option B: Regenerate

* regenerate them from the normative schema;
* ensure exact field parity;
* remove incompatible terminology;
* include `truth_statement`;
* prohibit permanent waivers;
* validate them against the schema; and
* identify their intended role relative to the per-class templates.

No template may offer “permanent” waiver treatment.

No legacy template may remain active without validator coverage.

## 5.13 Bind the non-waivable core across all FCR mechanisms

The non-waivable core shall apply to every FCR class and every authority mechanism, not only FCR-09.

Codex shall state expressly that FCR-01 through FCR-10 lack authority to waive, substitute, defer, override, or nullify the non-waivable core.

The non-waivable core matrix shall include:

* `core_id`;
* `protected_rule_id`;
* `protected_requirement`;
* `binding_scope`;
* `mechanisms_barred`;
* `permitted_narrowing`;
* `prohibited_effect`;
* `detection_method`;
* `violation_consequence`; and
* `reopening_trigger`.

At minimum, the core shall protect:

* non-falsification;
* external-law limitations;
* durable authority records;
* exact release scope;
* truthful validation;
* unsupported-overclaim prohibition;
* historical preservation;
* revocation and supersession traceability;
* material-defect disclosure;
* machine-readable FCR records;
* pilot privacy minima;
* security and privacy verification baselines where applicable; and
* independent review requirements for high-consequence authority actions.

Every core row shall cite the correct substantive rule IDs rather than generic repeated citations.

## 5.14 Operationalize second review or record it as a blocking limitation

The phrase “where available” shall not constitute an operative second-review control.

Codex shall choose one of the following:

### Preferred option: Operationalize second review

Require second review for:

* FCR-09 procedural override;
* FCR-10 production authorization;
* waiver of a critical control;
* material privacy or safeguarding exception;
* material security exception;
* acceptance of live pilot evidence as substitute evidence;
* closure of a critical finding; and
* any production authorization with exceptions.

The schema shall require:

* reviewer identity;
* reviewer role;
* reviewer competency;
* review timestamp;
* review outcome;
* conflicts disclosure;
* evidence reviewed;
* attestation; and
* signature or durable identity binding.

The second reviewer shall not be the same person as:

* the certifying authority;
* the artifact author;
* the primary validator;
* or the risk owner

for the same decision.

### Alternative option: Record a blocking limitation

If no independent reviewer is currently available:

* record the limitation as `BLOCKING`;
* prohibit FCR-09 and FCR-10 issuance;
* prohibit critical finding closure;
* prohibit production authorization with exceptions;
* define the exact event that cures the block;
* define permitted documentary work while blocked; and
* prevent the package from claiming Founder-review or production-authority readiness.

An FCR-08 risk acceptance shall not be sufficient to bypass a required second review for FCR-09 or FCR-10.

## 5.15 Add the missing Governance Maintenance Standard supersession record

Codex shall identify whether a prior Governance Maintenance Standard existed as:

* a draft;
* proposed artifact;
* adopted artifact;
* source package;
* or planned standard.

If it existed, create a formal supersession record containing:

* predecessor artifact ID;
* predecessor title;
* predecessor version;
* predecessor SHA-256;
* predecessor byte length;
* predecessor lifecycle status;
* successor artifact ID;
* successor title;
* successor version;
* provisions absorbed;
* provisions not absorbed;
* effective scope;
* dependent artifacts;
* historical preservation path;
* authority basis;
* effective date; and
* validation evidence.

If no predecessor artifact ever existed, revise the standard’s language to state:

`NO_SEPARATE_PREDECESSOR_GOVERNANCE_MAINTENANCE_STANDARD_WAS_ISSUED`

The package shall not claim that a standard was “absorbed” without identifying what was absorbed.

---

# 6. ADDITIONAL REQUIRED CORRECTIONS FROM ROUND 2

## 6.1 Validation check implementation parity

Every validation row shall map to actual code.

For each validation check, Codex shall record:

* function name;
* source file;
* source line or stable identifier;
* input artifacts;
* expected result;
* actual result;
* negative test;
* and retained log.

The validator shall actually read every artifact it claims to validate.

Codex shall specifically correct:

* cross-matrix consistency checks;
* controlled-vocabulary checks;
* outside-review disposition completeness checks;
* certification-ID uniqueness checks;
* checksum checks;
* workflow validation;
* overclaim scanning;
* placeholder and boilerplate detection; and
* authority-matrix consistency checks.

Grammar validation shall not be labeled uniqueness validation.

A header-only register shall not create a substantive `PASS` without stating that the test is vacuous because no records exist.

## 6.2 Correct the overclaim scan

The prohibited-overclaim scan shall not be disabled merely because a file contains the word “not.”

Codex shall implement:

* sentence-level claim parsing;
* proximity-based negation;
* explicit allowed claim patterns;
* explicit prohibited claim patterns;
* test fixtures containing genuine overclaims;
* test fixtures containing properly negated statements; and
* failure evidence.

The tools directory shall not be categorically exempt from overclaim or placeholder review where generated governance claims appear in source code.

## 6.3 Correct source register placeholders

Integrity fields shall contain:

* actual SHA-256;
* actual byte length;
* `NOT_APPLICABLE`; or
* `UNAVAILABLE_EVIDENCE`.

Values such as `COMPUTED_IN_MANIFEST` shall not appear in hash or byte-length columns.

## 6.4 Correct rule traceability boilerplate

Codex shall review repeated `rule_ids` fields in:

* non-waivable core matrix;
* privacy matrix;
* term register;
* metrics register;
* validation-category matrix;
* regulatory register;
* finding and exception matrices; and
* disposition matrices.

Uniform values are permissible only where substantively accurate.

Each row shall cite the rule or rules that actually govern it.

## 6.5 Expand retention coverage

The records retention schedule shall address, at minimum:

* FCR records;
* certification registers;
* waivers;
* deferrals;
* overrides;
* risk acceptances;
* production authorizations;
* pilot evidence;
* privacy evidence;
* minors and safeguarding records;
* findings;
* closure evidence;
* delegations;
* revocations;
* supersession records;
* source registers;
* validation logs;
* CI artifacts;
* outside reviews;
* Founder directives;
* custody evidence; and
* personal-data redaction records.

## 6.6 Correct challenge-procedure timing

Add:

* acknowledgement deadline;
* triage deadline;
* investigation deadline;
* interim protection measures;
* escalation path;
* overdue-treatment rule;
* mandatory written disposition;
* and reopening effect.

A credible challenge shall not remain indefinitely open without consequence.

## 6.7 Normalize readiness vocabulary

Codex shall reconcile readiness values with the controlled vocabulary register.

Every readiness term used by the package shall:

* appear in the controlled vocabulary register;
* have a definition;
* identify its dimension;
* identify allowed transitions or changes;
* identify evidence requirements; and
* avoid duplication with lifecycle or authority terms.

## 6.8 Restore or formally narrow source-register scope

Codex shall review the prior source register’s reduction from 39 rows to four.

Either:

1. restore the prior source records under the new controlled model; or
2. create a formal scope-narrowing record identifying:

   * removed records;
   * reason for removal;
   * retained historical location;
   * effect on traceability;
   * effect on prior findings;
   * and authority for narrowing.

Historical reconciliation records shall not silently disappear.

---

# 7. REQUIRED TOOLING TESTS

Codex shall add automated tests for the generator and validator.

At minimum:

## 7.1 Generator tests

* `--check` does not write;
* drift causes nonzero exit;
* clean package causes zero exit;
* write mode regenerates expected files;
* normative JSON changes produce derived-file drift;
* stale Markdown hash is detected;
* hardcoded local paths are not required;
* generation works from a clean checkout; and
* generation is deterministic.

## 7.2 Validator tests

* valid package passes;
* checksum tamper fails;
* manifest byte-length mismatch fails;
* stale human-readable hash fails;
* unresolved JSON Pointer fails;
* unresolved Markdown anchor fails;
* lifecycle terminal mismatch fails;
* unreachable state fails;
* non-terminal sink fails;
* invalid controlled vocabulary fails;
* missing review disposition fails;
* incorrect reviewer attribution fails;
* empty `changed_files` fails for remediated findings;
* null FCR required field fails;
* empty FCR required field fails;
* duplicate certification ID fails;
* malformed production release identity fails;
* invalid truth statement fails;
* unexecuted check reported as PASS fails;
* legal review reported as PASS without legal evidence fails;
* second-review requirement absent fails;
* legacy active template not schema-valid fails;
* unrecorded supersession fails;
* prohibited overclaim fixture fails; and
* properly qualified status statement passes.

Test logs shall be retained.

---

# 8. REPOSITORY AND PR RECONCILIATION

PR #77 is currently behind the protected branch.

Before final return, Codex shall:

1. fetch the current protected branch;
2. record the current protected head;
3. compare it against the previously reviewed protected head;
4. identify intervening commits;
5. identify files changed by those commits;
6. determine whether any change affects this package or its dependencies;
7. reconcile or rebase through the protected PR workflow;
8. rerun generation and validation from the reconciled head;
9. rerun checksums;
10. rerun the read-only drift check;
11. update repository-state validation rows; and
12. keep the PR draft and unmerged unless separately authorized.

If reconciliation changes package content, the targeted outside re-review shall be performed against the reconciled bytes.

---

# 9. REQUIRED NEW REVISION STATUS

After completing the revisions but before outside re-review, the truthful status shall be:

`ROUND_2_FINDINGS_REMEDIATED_READY_FOR_TARGETED_ROUND_3_REREVIEW`

This status may be used only if:

* all blocking requirements are implemented;
* all executable validation checks actually pass;
* judgment and legal checks are accurately pending or blocked;
* repository state is reconciled;
* the finding disposition matrix is complete;
* generator check mode is read-only;
* all adversarial references resolve;
* the FCR schema rejects null and empty mandatory values;
* lifecycle dimensional conflict is resolved;
* the zero-exception production path exists;
* legacy templates are superseded or valid;
* the core binds all FCR classes;
* second review is operative or blocking;
* and the maintenance-standard supersession issue is resolved.

Otherwise use:

`ROUND_2_FINDINGS_REVISION_INCOMPLETE_BLOCKING_DEFECTS_REMAIN`

---

# 10. REQUIRED RETURN PACKAGE

The returned package shall include, at minimum:

1. revised normative JSON;
2. revised Markdown standard;
3. revised lifecycle state-definition matrix;
4. revised lifecycle transition matrix;
5. revised authority-event model;
6. revised production-authorization model;
7. revised FCR schema;
8. revised FCR templates;
9. legacy-template supersession record;
10. Governance Maintenance Standard supersession record;
11. revised non-waivable-core matrix;
12. revised second-review controls;
13. revised role and assignment matrix;
14. revised outside-review disposition matrix;
15. exact Cursor Round 2 review source;
16. exact Claude Round 2 review source;
17. exact Perplexity Round 2 review source;
18. revised source register;
19. revised controlled vocabulary;
20. revised readiness vocabulary;
21. revised privacy matrix;
22. revised retention schedule;
23. revised challenge procedure;
24. revised generator;
25. revised validator;
26. generator test suite;
27. validator test suite;
28. negative fixtures;
29. positive fixtures;
30. revised CI workflow;
31. retained execution logs;
32. revised validation report;
33. revised validation-category matrix;
34. revised adversarial review;
35. machine-readable reference index;
36. revised package manifest;
37. checksum ledger;
38. repository reconciliation report;
39. revision summary;
40. known limitations;
41. Round 2 finding closure report; and
42. targeted Round 3 re-review instructions.

---

# 11. REQUIRED RETURN REPORT

Codex shall return the following sections.

## A. Executive Summary

State:

* what was corrected;
* what was redesigned;
* what was removed;
* what was superseded;
* what remains pending;
* what remains blocked;
* and whether the package is ready for Round 3 targeted re-review.

## B. Repository State

Include:

* repository;
* protected branch;
* prior protected head;
* current protected head;
* working branch;
* starting work head;
* final head;
* PR number;
* PR state;
* merge state;
* behind or ahead state;
* worktree status;
* and confirmation of no unauthorized protected-branch mutation.

## C. Review Source Authentication

For Cursor, Claude, and Perplexity, provide:

* exact filename;
* SHA-256;
* byte length;
* package path;
* reviewer date;
* number of Critical findings;
* number of High findings;
* number of Medium findings;
* number of Low findings;
* number of Editorial findings; and
* number of prior findings re-evaluated.

## D. Finding Disposition Summary

Provide counts by reviewer and status:

* fully remediated;
* partially remediated;
* rejected;
* deferred;
* unresolved;
* pending validation;
* pending re-review; and
* blocking.

## E. File Inventory

List every:

* created file;
* modified file;
* deleted file;
* superseded file;
* renamed file;
* generated file;
* and retained historical file.

## F. Validation Results

For every check, provide:

* check ID;
* actual command or function;
* actual execution time;
* actual exit code;
* actual result;
* retained log path;
* evidence path;
* limitations;
* and blocking effect.

## G. Test Results

Report:

* generator tests;
* validator tests;
* schema fixtures;
* lifecycle tests;
* reference tests;
* checksum tests;
* CI workflow tests;
* tamper tests;
* and negative overclaim tests.

## H. Model Redesign Explanation

Explain:

* lifecycle dimension;
* authority-event dimension;
* certification-status dimension;
* evidence-status dimension;
* readiness dimension;
* production authorization with no exceptions;
* production authorization with exceptions;
* and how concurrent truths are represented.

## I. Known Limitations

State all remaining:

* legal;
* privacy;
* regulatory;
* staffing;
* second-review;
* signing;
* branch-protection;
* repository;
* implementation;
* production;
* and external-validation limitations.

## J. Final Status

Use exactly one:

* `ROUND_2_FINDINGS_REMEDIATED_READY_FOR_TARGETED_ROUND_3_REREVIEW`;
* `ROUND_2_FINDINGS_REVISION_INCOMPLETE_BLOCKING_DEFECTS_REMAIN`; or
* `ROUND_2_FINDINGS_REVISION_BLOCKED_REPOSITORY_OR_SOURCE_CONDITION`.

---

# 12. PROHIBITED ACTIONS

Codex shall not:

* hardcode validation results;
* record human or legal work as machine-passed;
* mark pending legal confirmation as PASS;
* describe dotted paths as RFC 6901 pointers;
* retain broken adversarial references;
* mutate files during `--check`;
* regenerate checksums before verifying committed checksums in CI;
* claim finding completeness without mapping each source finding;
* permit null or empty mandatory FCR fields;
* leave terminal flags blank or false for terminal states;
* silently retain authority events as lifecycle states;
* require exceptions for every production authorization;
* retain incompatible active legacy templates;
* limit the non-waivable core to FCR-09;
* treat “where available” as an operative second-review control;
* bypass second review through FCR-08;
* claim absorption without a supersession record;
* close Round 2 findings without targeted outside re-review;
* merge PR #77 without separate authority;
* issue any FCR record;
* authorize pilot activity;
* authorize production activity; or
* claim Founder approval readiness.

---

# 13. TARGET END STATE

The required end state is a Round 3 candidate that:

* derives validation claims from actual executions;
* accurately distinguishes machine, human, legal, and outside review;
* contains no unsupported `PASS`;
* has fully resolvable adversarial references;
* carries correct cross-file integrity metadata;
* has a genuinely read-only drift check;
* validates committed bytes before regeneration;
* traces every Round 2 finding individually;
* rejects empty authority records;
* has correct lifecycle terminality;
* preserves dimensional separation;
* supports clean production authorization without exceptions;
* contains no conflicting legacy templates;
* binds the non-waivable core across all FCR mechanisms;
* imposes a real second-review requirement or an explicit block;
* records the Governance Maintenance Standard supersession truthfully;
* preserves historical evidence;
* and is ready for a narrow, evidence-based Round 3 re-review.

---

# 14. AUTHORITY LIMITATION

This directive authorizes revision and validation only.

It does not authorize:

* approval;
* adoption;
* lock;
* accession;
* custody completion;
* activation;
* implementation;
* pilot use;
* production use;
* certification;
* procedural override;
* risk acceptance;
* protected-branch merge;
* or automatic closure.

**Controlling authority statement:**

`ROUND_2_DOCUMENTARY_REMEDIATION_AND_REVALIDATION_AUTHORIZED_NO_ADOPTION_ACTIVATION_IMPLEMENTATION_PILOT_PRODUCTION_CERTIFICATION_MERGE_OR_AUTOMATIC_CLOSURE_AUTHORITY`
