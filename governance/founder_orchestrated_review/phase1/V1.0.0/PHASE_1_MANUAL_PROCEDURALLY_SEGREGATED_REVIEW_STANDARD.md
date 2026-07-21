# Phase 1 Manual Procedurally Segregated Review Standard

## Applicability

This standard governs every Phase 1 review cycle. Compliance creates procedural segregation only; it does not create a distinct natural-person Reviewer Identity, organizational independence, external assurance, or a runtime-native custom-agent identity.

## Mandatory cycle controls

1. Record Founder authorization, scope, exclusions, reserved decisions, package ID, and review-cycle ID.
2. Freeze the candidate into a read-only package and generate its manifest with a deterministic utility.
3. Select the exact versioned profile for every assigned role and verify source and profile checksums.
4. Classify every input and exclude prohibited data.
5. Build separate input manifests and unique harmless canaries.
6. Record the effective permission mode before each execution. `UNRESOLVED` or broader-than-authorized permissions fail closed.
7. Start each Role Execution in a fresh isolated context with no shared scratchpad or drafting conversation.
8. Preserve the complete input manifest, invocation record, output, validation result, timestamps, model/provider/runtime identifiers, and hashes.
9. Seal ES-RA-02, ES-RA-03, and ES-RA-06 initial outputs before any sees another blind reviewer’s result.
10. Reconcile only after sealing; retain original wording, severity, citations, execution ID, disagreement, and disposition.
11. Run approved deterministic validators against the exact frozen bytes. An AI controller cannot override a failure.
12. Preserve first failures and create a new execution ID for every retry.
13. Prepare a Founder handoff that separates evidence, agent recommendations, unresolved conflicts, and Founder-reserved decisions.

## Identity rule

Every run is configuration-identified by its Execution Identity. The role label, prompt, response, or session name does not prove Reviewer Identity. If the runtime does not expose the requested role identity, record that fact and do not state that the canonical role executed.

## Modification rule

A substantive reviewer may write only its assigned output. It may not edit the frozen candidate, another role’s output, historical evidence, `.git`, role configurations, or acceptance requirements. Remediation requires a separately authorized mutable worktree and a new candidate version.

## Completion rule

No silent omissions are permitted. Every requirement, source, expected output, and procedure receives an explicit status in a Work Completeness Ledger. “No issue found” is limited to the recorded scope, methods, sources, and limitations.
