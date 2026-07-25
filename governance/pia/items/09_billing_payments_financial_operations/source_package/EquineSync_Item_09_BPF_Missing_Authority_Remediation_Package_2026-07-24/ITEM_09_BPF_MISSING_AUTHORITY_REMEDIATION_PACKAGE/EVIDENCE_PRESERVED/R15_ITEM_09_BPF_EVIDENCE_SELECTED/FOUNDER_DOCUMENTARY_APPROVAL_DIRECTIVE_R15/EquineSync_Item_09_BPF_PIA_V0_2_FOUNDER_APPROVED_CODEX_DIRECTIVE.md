# Founder-Approved Directive to Codex

## EquineSync Billing, Payments, Payroll, and Financial Operations PIA V0.2

**Directive ID:** `ES-DIR-BPF-PIA-V0.2-CODEX-HANDOFF-2026-07-23-02`  
**Founder:** Rian Ray  
**Founder approval ID:** `ES-FA-BPF-PIA-V0.2-2026-07-23-01`  
**Founder approval date:** `2026-07-23`  
**Founder approval record:** `FOUNDER_APPROVAL/EquineSync_Item_09_BPF_PIA_V0_2_FOUNDER_APPROVAL_RECORD.md`  
**Founder approval disposition:** `FOUNDER_APPROVED_FOR_DOCUMENTARY_REPOSITORY_INTEGRATION_AND_FRESH_STRUCTURED_REVIEW`  
**Official repository:** `rianray2012-coder/EquineSync-V4`  
**Requested operation:** Controlled documentary package intake, canonical identity verification, repository integration, and fresh structured review  
**Source package:** `EquineSync_Item_09_BPF_PIA_V0_2_Strengthened_Review_Package.zip`  
**Expected source-package SHA-256:** `882556c0c8553ddad8f4f8164d688473ff00300f57c389235b94189220b19a40`  
**Authority effect:** `DOCUMENTARY_ONLY`  

## 1. Mission

Integrate the supplied Founder-approved strengthened V0.2 documentary candidate for the EquineSync Billing, Payments, Payroll, and Financial Operations Product Implementation Atlas into the official EquineSync V4 repository, then conduct a fresh repository-governed structured review if and only if every intake, identity, custody, runtime, and repository precondition passes.

This is not an implementation directive. It does not authorize schemas, migrations, application code, provider configuration, live credentials, payment processing, connected-account activation, movement of funds, payroll execution, deployment, production use, pilot enrollment, or first-user enrollment.

## 2. Controlling Package Identity

The supplied candidate represents:

- Package ID: `ES-PIA-BPF-V0.2-STRENGTHENED-REVIEW-PACKAGE`
- Candidate PIA ID: `ES-PIA-BILLING-PAYMENTS-FINANCIAL-OPS-V0.2.0`
- Package portfolio label: `Item 09`
- Version: `0.2.0`
- Canonical template claim: `ES-PIA-MASTER-STANDARD-V1.1`
- Founder decisions incorporated: `BPF-FD-001` through `BPF-FD-025`
- Candidate disposition: `ITEM_09_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`
- Founder approval disposition: `FOUNDER_APPROVED_FOR_DOCUMENTARY_REPOSITORY_INTEGRATION_AND_FRESH_STRUCTURED_REVIEW`
- Founder approval record: `FOUNDER_APPROVAL/EquineSync_Item_09_BPF_PIA_V0_2_FOUNDER_APPROVAL_RECORD.md`
- Documentary validation: `PASS`
- Authority effect: `NONE`
- Mandatory readiness answers:
  1. Engineering buildability: `YES_WITH_EVIDENCE`
  2. Objective QA verification: `YES_WITH_EVIDENCE`
  3. Governance and MIAP traceability: `YES_WITH_EVIDENCE`
  4. Operational safety, support, recovery, and maintenance: `NO`
  5. First-user enrollment readiness: `NO`

Treat all package identity claims as candidate claims until independently reconciled against the repository's current controlling records. The enclosed Founder Approval Record is authoritative only for documentary approval, repository integration, and fresh structured review. It does not establish adoption, lock, implementation authority, operational readiness, or enrollment readiness.

## 3. Absolute Repository Boundary

Use only the official repository:

`rianray2012-coder/EquineSync-V4`

Do not use, modify, or cite a predecessor repository such as `Equine-Sync`, `Equine-Sync-v2`, or another similarly named repository as the integration target.

Before any mutation:

1. Confirm the configured remote resolves to the official repository.
2. Fetch all relevant remote refs without pruning or rewriting history.
3. Confirm the worktree and index are clean.
4. Read all applicable repository instructions, including root and path-scoped `AGENTS.md`, governance instructions, PIA program records, package-control rules, and runtime review gates.
5. Identify the current authorized integration baseline from repository evidence. Do not assume the default branch is the correct baseline merely because it is the default branch.
6. Record the exact baseline branch and commit before creating any new branch.

Do not mutate a preserved, locked, historical, or Founder-controlled branch.

## 4. Mandatory Fail-Closed Intake

Perform all steps below in a disposable staging directory outside the repository before creating a branch or writing repository files.

### 4.1 Outer handoff

- Verify the handoff ZIP with `unzip -t`.
- Verify the handoff checksum ledger.
- Read the handoff manifest, the Founder Approval Record, and this directive.
- Verify the Founder Approval Record filename, approval ID, approval date, subject, disposition, source-package SHA-256, and authority ceiling against the handoff manifest.

### 4.2 Inner source package

- Confirm the source ZIP filename is exact.
- Compute its SHA-256 and require the exact value:

`882556c0c8553ddad8f4f8164d688473ff00300f57c389235b94189220b19a40`

- Run `unzip -t` against the source ZIP.
- Extract it to a new disposable directory.
- Require one package root: `bpf_item09_v02_package/`.
- Run `sha256sum -c CHECKSUMS.sha256` from the extracted package root.
- Recompute and compare the manifest-listed byte sizes and hashes.
- Confirm the manifest states `authority_effect` or equivalent authority flags as false.
- Confirm the documentary validation reports `pass: true` and `authority_effect: NONE`.
- Confirm no archive path traversal, symlink escape, executable payload, hidden repository metadata, nested Git repository, credential, secret, environment file, or unexpected binary is present.

Stop before repository mutation if any archive, checksum, manifest, file-count, byte-size, path, or authority check fails.

## 5. Canonical PIA Identity Gate

This gate is mandatory because package-local numbering is not allowed to silently override the repository program registry.

Before branch creation, locate the repository's current authoritative PIA program registry, sequence, manifest, index, or equivalent controlling record. Determine the canonical values for the Billing, Payments, Payroll, and Financial Operations PIA:

- portfolio position or item number;
- canonical PIA ID;
- official title;
- predecessor and successor relationship;
- required repository destination;
- current lifecycle status;
- permitted review workflow.

Require exact agreement between the repository and the supplied candidate for the canonical portfolio position and identity.

### Stop condition

If the repository assigns this PIA any item number other than `09`, uses a materially different canonical ID or title, identifies a conflicting active candidate, or requires a different predecessor relationship, stop before branch creation, file copying, staging, commit, or push.

Report:

- the package claim;
- the repository claim;
- exact repository paths and line references;
- the controlling precedence rule;
- the smallest Founder decision required to resolve the mismatch.

Do not rename, renumber, rewrite, normalize, or partially integrate the package without a new Founder instruction.

## 6. Runtime and Review-Permission Gate

Read and obey the repository's current runtime permission and structured-review controls.

- Do not bypass a required approval policy, sandbox, provider restriction, model restriction, agent requirement, or preflight gate.
- Do not claim a fresh review passed when the required review runtime was unavailable or blocked.
- Do not invoke provider-bound diagnostics before the repository-defined formal preflight permits them.
- If the repository requires a runtime state unavailable in the current environment, stop fail-closed before mutation unless the repository explicitly permits package intake and integration independently of formal review.
- If documentary integration is separately permitted but fresh review is blocked, clearly separate the two dispositions. Never convert `INTEGRATED_REVIEW_BLOCKED` into `REVIEW_PASSED`.

## 7. Branch and Mutation Rules

Only after Sections 3 through 6 pass:

1. Create a new branch from the exact authorized integration baseline.
2. Preferred branch name, only if the repository confirms Item 09:

`codex/item-09-bpf-pia-v0-2-founder-approved-review-v1`

3. Follow the repository's existing directory and naming pattern for neighboring PIA program items. Do not invent a parallel governance tree.
4. Preserve every supplied source-package byte exactly.
5. Preserve V0.1 as historical predecessor evidence.
6. Preserve V0.2 as the immutable supplied review candidate.
7. Preserve the enclosed Founder Approval Record byte-for-byte as the controlling documentary approval evidence.
8. Do not edit the bundled V0.1 or V0.2 DOCX, Markdown, machine-readable JSON, audit outputs, manifest, or checksum ledger.
9. If repository-native wrapper records are required, create new additive records outside the immutable supplied package.
10. Do not delete, replace, or rewrite any existing PIA, program registry, review history, checksum record, or Founder decision record.
11. Do not create a V0.3 successor. If the fresh review identifies material defects, record findings and stop for Founder direction.

## 8. Required Fresh Structured Review

The bundled internal review report is evidence of drafting work, not an independent repository review. Conduct the repository's formal fresh structured review from the V0.2 source documents and machine-readable companion.

At minimum, independently verify:

- 43 required Master Standard sections are present and in canonical order;
- `BPF-FD-001` through `BPF-FD-025` are represented without dilution or contradiction;
- all Founder modifications are preserved, including initial controlled scope for Stripe Connect and payroll and payment connections for Stripe, Venmo, PayPal, Cash App, bank transfer, and QuickBooks Payments;
- 104 normative requirements are present, uniquely identified, and structurally complete;
- 48 acceptance criteria are present and traceable;
- 60 tests are present and traceable;
- 10 golden-path scenarios are present;
- 36 adversarial, negative, and abuse scenarios are present;
- 24 evidence families are present;
- 19 dependencies are present;
- machine-readable identifiers are unique;
- requirement references are valid;
- Questions 1 through 5 are fully answered using permitted answer states;
- Questions 4 and 5 remain `NO` absent executed operational and enrollment evidence;
- no implementation or activation authority is implied;
- provider-specific documentation does not override EquineSync's canonical financial semantics;
- distinct financial facts remain distinct, including obligation, charge, invoice, authorization, capture, settlement, transfer, payout, bank receipt, payroll submission, payroll acceptance, payroll payment, accounting projection, dispute, refund, reversal, and reconciliation;
- tenant, legal-entity, merchant, payee, beneficiary, payer, worker, guardian, owner, and service-recipient boundaries remain explicit;
- emergency horse care, welfare-critical information, identity, legally required records, and transfer continuity are not automatically restricted for nonpayment;
- AI remains advisory and cannot issue invoices, move money, approve refunds, run payroll, decide legal responsibility, impose restrictions, or adjudicate disputes.

Use independent scripts or repository-native validators where available. Do not merely copy the supplied validation result into a new review record.

## 9. Required Repository-Native Outputs

Create only the outputs required by the repository's established PIA review pattern. At minimum, the completed branch should contain additive repository-native evidence equivalent to:

1. package intake receipt;
2. Founder approval custody and recognition record;
3. canonical identity reconciliation record;
4. fresh structured review report;
5. deterministic validation result;
6. review finding register;
7. package or repository checksum ledger;
8. integration manifest or custody record;
9. final branch receipt.

Use existing repository filenames and schemas when they exist. Do not create duplicate formats merely to satisfy this list.

The fresh review report must state one of these bounded outcomes:

- `PASS_FOUNDER_APPROVED_DOCUMENTARY_CANDIDATE_VALIDATED`
- `PASS_WITH_NONBLOCKING_FINDINGS_FOUNDER_APPROVED_DOCUMENTARY_CANDIDATE_VALIDATED`
- `BLOCKED_BY_CANONICAL_IDENTITY_CONFLICT`
- `BLOCKED_BY_RUNTIME_OR_PERMISSION_GATE`
- `BLOCKED_BY_PACKAGE_INTEGRITY_FAILURE`
- `REVIEW_FAILED_MATERIAL_REVISION_REQUIRED`

The supplied Founder Approval may be recorded only as `FOUNDER_APPROVED_FOR_DOCUMENTARY_REPOSITORY_INTEGRATION_AND_FRESH_STRUCTURED_REVIEW`. Do not broaden that phrase into `ADOPTED`, `LOCKED`, `IMPLEMENTATION_AUTHORIZED`, `PRODUCTION_READY`, `OPERATIONALLY_READY`, or `ENROLLMENT_READY`.

## 10. Validation Before Commit

Before committing:

- verify only intended additive documentary files are changed;
- confirm no source package byte changed;
- rerun all package checksums;
- rerun repository-required validators;
- verify every new manifest and checksum ledger;
- inspect `git diff --check`;
- inspect staged paths and staged diff statistics;
- confirm there are no secrets, credentials, provider keys, payment data, payroll personal data, environment files, generated caches, temporary files, render intermediates, or unrelated changes;
- confirm the worktree contains no untracked residue outside the intended package;
- confirm documentary integration and fresh-review authority are true only as expressly granted, and every implementation, activation, funds-movement, payroll-execution, deployment, production, pilot, enrollment, PR, and merge authority flag remains false.

Do not use broad formatting, line-ending normalization, document regeneration, or bulk cleanup on supplied files.

## 11. Commit, Push, and Remote Verification

If and only if every required gate passes:

1. Stage only the exact intended documentary paths.
2. Create one bounded commit.
3. Preferred commit message:

`docs(governance): integrate Founder-approved Item 09 BPF PIA v0.2`

4. Push only the new branch to the official remote.
5. Verify the remote branch resolves to the exact local commit SHA.
6. Confirm the local worktree and index are clean.
7. Do not create a pull request.
8. Do not merge, rebase, tag, release, deploy, or modify branch protection.

If repository policy requires more than one commit, explain why and keep each commit documentary and bounded.

## 12. Required Final Receipt

Return a concise but complete receipt containing:

- official repository and remote URL;
- authorized baseline branch and starting commit;
- canonical PIA registry path and resolved Item/ID;
- resulting branch and commit;
- remote-ref verification result;
- Founder approval ID, date, disposition, and preserved repository path;
- package filename and verified SHA-256;
- package intake and checksum results;
- exact repository paths added;
- fresh-review disposition;
- five mandatory readiness answers;
- review findings by severity;
- tests and validators executed with pass/fail counts;
- runtime or permission limitations;
- confirmation that no implementation, schema, migration, provider activation, connected-account activation, funds movement, payroll execution, deployment, production use, pilot, enrollment, PR, or merge occurred;
- clean-worktree status.

If stopped, provide the same receipt through the stop point and identify the exact failed gate. Do not perform later phases after a stop condition.

## 13. Founder Authority Ceiling

The Founder approves the supplied V0.2 strengthened documentary candidate for the controlled documentary intake, canonical identity verification, repository integration, and fresh structured review described above. This approval is documentary only and is bounded by the enclosed Founder Approval Record.

It does not authorize:

- application implementation or refactoring;
- schema or migration creation;
- Stripe, Stripe Connect, PayPal, Venmo, Cash App, bank-transfer, QuickBooks Payments, QuickBooks Online, or payroll-provider activation;
- account creation, credential loading, webhook registration, sandbox execution, or live provider calls unless the repository's formal documentary-review procedure explicitly requires and permits a bounded non-transactional check;
- merchant, payee, employer, tax, payroll, money-transmission, escrow, custodial, legal, or compliance conclusions;
- payment, transfer, payout, refund, debit, credit, payroll submission, payroll payment, or movement of funds;
- production configuration or deployment;
- pilot or first-user enrollment;
- PIA adoption, constitutional lock, release approval, or enrollment approval;
- pull request creation or merge.

When ambiguity exists, stop fail-closed and request the smallest necessary Founder decision.
