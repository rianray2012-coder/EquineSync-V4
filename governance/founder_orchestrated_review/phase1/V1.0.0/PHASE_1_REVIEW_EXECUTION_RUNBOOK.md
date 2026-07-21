# Phase 1 Review Execution Runbook

## 1. Authorize and identify

Create the review-cycle ID, package ID, authorization record, scope denominator, data classification, state record, and reserved-Founder-decision list. Stop if authorization or baseline identity is missing.

## 2. Freeze candidate

Copy authorized inputs into a controlled package, reject traversal and forbidden paths, compute SHA-256 hashes, write the manifest, and make the substantive candidate read-only. A later byte change creates a new package version.

## 3. Prepare role packets

For each assigned role, verify `profiles/*.json`; include only permitted inputs, the shared contract, approved prompt, relevant requirements, output schema, and one unique canary. Record excluded inputs and prohibited predecessor outputs. Do not reuse sessions or scratchpads.

## 4. Permission gate

Create the pre-execution permission record required by `RUNTIME_PERMISSION_CONTROL.md`. Compare parent, configured, expected, and observed modes. Formal execution requires `PASS`; `FAIL` or `UNRESOLVED` produces a preserved blocked attempt and no substantive role work.

## 5. Blind execution

Launch ES-RA-02, ES-RA-03, and each ES-RA-06 instance in separate fresh contexts. Do not pass drafting conversation, expected findings, another reviewer’s canary, prior blind outputs, reconciliation text, or a proposed Founder conclusion. Capture the invocation and output without modification.

## 6. Seal and validate outputs

Hash every output; validate its schema, citations, finding IDs, confidence, completeness ledger, self-audit, attestation, and prohibited claims. A failed output remains sealed as a failed attempt. A retry receives a new ID and explicit predecessor link.

## 7. Reconcile

After all initial blind outputs are sealed, create a discrepancy register. Preserve original findings and map duplicates without deleting them. Do not decide by vote or average severity. Escalate material conflict.

## 8. Machine validation and custody

ES-RA-04 may select only allowlisted validators; deterministic results remain authoritative for the checks executed. ES-RA-05 inventories expected, received, missing, unused, conflicting, and derivative evidence and verifies all references and hashes.

## 9. Replay when required

Reproduce configuration, input hashes, permissions, model/runtime identifiers, and settings; never promise byte-identical LLM output. Classify variance using the replay standard and escalate material variance.

## 10. Founder handoff

Advance only through `FOUNDER_REVIEW_PACKAGE_READY` and `FOUNDER_DECISION_PENDING`. Present unresolved findings, limitations, assurance classification, failed attempts, and exact decisions requested. Do not simulate the Founder response.

## Required state order

`CREATED → SOURCE_INVENTORIED → CANDIDATE_FROZEN → ROLE_PACKETS_PREPARED → BLIND_REVIEW_IN_PROGRESS → BLIND_REVIEW_OUTPUTS_SEALED → RECONCILIATION_IN_PROGRESS → MACHINE_VALIDATION_COMPLETE → EVIDENCE_CUSTODY_COMPLETE → FOUNDER_REVIEW_PACKAGE_READY → FOUNDER_DECISION_PENDING`
