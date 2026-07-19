# Codex Orchestration Directive

**Directive version:** 1.0.0  
**Controlling framework:** EquineSync Founder-Orchestrated Review Agent Framework V1.3  
**Final authority:** Rian Ray

## 1. Purpose

Orchestrate the eight agents as segregated internal-assurance functions while preserving package identity, evidence lineage, role boundaries, completion proof, and Founder control.

## 2. Non-negotiable orchestration rules

1. Every review begins with a Founder Review Authorization.
2. Every run has unique review-cycle, agent, and agent-run IDs.
3. Every agent runs in a separate session or isolated context.
4. Reviewers receive a frozen package, not a mutable drafting workspace.
5. No agent may approve, adopt, lock, waive, accept risk, or authorize release.
6. No reviewing agent may modify the frozen candidate.
7. Agent-to-agent communication occurs only through registered handoff artifacts.
8. Original reports, failures, and disagreements remain preserved.
9. Post-freeze changes create a new package version and rerun determination.
10. The final package must satisfy the Cross-Agent Completion Gate before Founder disposition.

## 3. Required identifiers

Recommended formats:

- Review cycle: `ES-REV-YYYY-NNN`
- Package: `ES-PKG-YYYY-NNN-V###`
- Agent run: `<AGENT-ID>-<REVIEW-CYCLE>-RUN-##`
- Finding: `<REVIEW-CYCLE>-F-####`
- Evidence: `<REVIEW-CYCLE>-E-#####`
- Golden path: `<REVIEW-CYCLE>-GP-###`
- Execution: `<REVIEW-CYCLE>-EXEC-###`
- Founder decision: `<REVIEW-CYCLE>-FD-###`

## 4. Standard execution sequence

### Phase 0: Authorization

Create and validate the Founder Review Authorization. Resolve scope, gate, agents, tools, environments, prohibited actions, and Founder-reserved decisions.

### Phase 1: Custody intake

Invoke ES-RA-05. Inventory sources, classify evidence, calculate hashes where possible, create the source-authority register, and freeze the initial package.

**Gate:** No substantive agent starts without a uniquely identified package or an explicit baseline-investigation assignment.

### Phase 2: Drafting or remediation

Invoke ES-RA-01 against authorized sources. Create a new candidate version, ledgers, change log, and handoff package.

Return outputs to ES-RA-05. Freeze a new candidate package.

### Phase 3: Initial structural validation

Invoke ES-RA-04 for manifest, schema, required-file, link, identifier, and structural checks. This phase may block expensive review but does not replace later full validation.

### Phase 4: Independent review

Invoke ES-RA-02 in a clean context. Require independent-detection and structured-coverage passes.

Invoke one ES-RA-06 instance per required domain. Domain instances may run in parallel if they do not share mutable state.

### Phase 5: Adversarial challenge

Invoke ES-RA-03 after the candidate package is frozen. Withhold remediation plans until the initial challenge pass is complete.

### Phase 6: Full machine validation

Invoke ES-RA-04 against the exact frozen package reviewed by the other agents. Preserve first failures and all reruns.

### Phase 7: Golden-path specification

Invoke ES-RA-07 for each critical operational workflow. Register specifications and fixtures with ES-RA-05.

### Phase 8: Executable reproduction

Invoke ES-RA-08 in a Founder-authorized environment. Preserve planned-versus-executed reconciliation, failures, deviations, reruns, cleanup, and reproduction level.

### Phase 9: Findings reconciliation

Create the cross-agent discrepancy register. Do not resolve by vote. Authorize targeted source inspection, blind rereview, re-performance, expanded sampling, different-model review, or human specialist review as needed.

### Phase 10: Remediation

Return authorized P0, P1, and selected P2 findings to the drafting or implementation function. Create a new package version. Do not modify the reviewed package in place.

### Phase 11: Fresh verification

Use fresh ES-RA-02, ES-RA-04, ES-RA-06, and ES-RA-08 runs as affected. Verify the exact remediation, dependencies, regressions, and evidence.

### Phase 12: Cross-Agent Completion Gate

ES-RA-05 or a designated completion verifier confirms:

- all assigned reports exist;
- all denominators and completeness ledgers exist;
- all self-audits and attestations exist;
- all evidence and output references resolve;
- all P0/P1 statuses are current;
- all material claims have evidence links;
- all discrepancies are recorded;
- all required reruns occurred;
- all affected golden paths were rerun;
- completeness and reliability classifications are justified; and
- What This Review Did Not Establish is complete.

Failure disposition: `NOT_READY_FOR_FINAL_FOUNDER_DISPOSITION`.

### Phase 13: Founder decision package

Assemble the Founder Decision Package. Clearly separate agent recommendations from Founder authority.

### Phase 14: Founder disposition and closure

Record the express Founder decision. ES-RA-05 creates the final manifest, hash register, closure record, retained findings, and revalidation triggers.

Lock, implementation, pilot, release, or production action requires separate authorization where applicable.

## 5. Parallelism rules

May run in parallel after candidate freeze:

- distinct Domain Reviewers;
- Segregated Review and initial Adversarial analysis, if neither sees the other’s conclusions;
- nonmutating machine checks;
- evidence registration.

Must run sequentially:

- drafting before candidate freeze;
- candidate freeze before formal review;
- specification before execution;
- remediation before verification;
- completion gate before Founder decision package.

## 6. Handoff contract

Every handoff must identify:

- sender and recipient roles;
- review-cycle and package IDs;
- exact files and hashes;
- authorized purpose;
- scope and exclusions;
- unresolved questions;
- expected outputs;
- required schemas;
- prohibited actions; and
- whether prior conclusions are intentionally withheld for blind review.

## 7. Review contamination controls

- Do not pass private drafting reasoning to segregated reviewers.
- Do not show duplicate reviewers each other’s conclusions until both finish.
- Do not show the adversarial agent remediation plans before initial challenge completion.
- Do not provide the Controller undocumented workarounds.
- Preserve initial reports before reconciliation.

## 8. High-risk escalation

Use enhanced review for safeguarding, equine welfare, payments, identity recovery, access bypass, privacy breach, security incidents, irreversible deletion, audit integrity, constitutional lock, production deployment, emergency authority, or high-impact automation.

Enhanced review may require duplicate agents, a different model, human specialist consultation, independent machine rerun, Level 3 or 4 reproduction, expanded evidence inspection, or direct Founder review.

## 9. Completion and confidence

Do not convert classifications into automatic approval. Confidence is supported by scope completeness, reliability, evidence sufficiency, finding status, reproduction, and residual-risk disclosure. Founder judgment remains controlling.
