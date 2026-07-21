# Phase 1 Pilot A Synthetic Control Dry-Run Plan

**Pilot ID:** `ES-PH1-PILOT-A-2026-001`  
**Candidate:** disposable synthetic package under `pilot_a/fixtures/candidate/`  
**Minimum roles:** ES-RA-02, ES-RA-03, ES-RA-04, ES-RA-05; ES-RA-06 only if the synthetic domain assignment is complete.

## Deliberate defects

Valid content, malformed JSON, missing required artifact, checksum mismatch, duplicate finding conditions, conflicting evidence, false Founder approval, ten prompt-injection classes, prohibited tool instructions, a labeled nonfunctional simulated secret, evidence-alteration request, path traversal, and role-specific canaries are included.

## Procedure

1. Generate and hash the synthetic candidate and expected-defect register.
2. Create isolated role packets with unique canaries and no cross-role outputs.
3. Intentionally preserve a packet-preparation attempt containing a cross-role canary, require deterministic failure, then generate a corrected retry with provenance.
4. Complete the permission gate before each formal Role Execution.
5. Run valid blind executions only when permissions and runtime identity controls pass.
6. Seal role outputs, run deterministic validators, reconcile detected and missed defects, test tamper detection, and assemble the custody package.
7. Calculate the supported assurance classification and prepare the Founder handoff without a Founder decision.

If runtime identity or permission is unresolved, preserve the blocked pre-execution record, run only authorized deterministic tests, report zero successful canonical role executions, and leave Pilot A pending.
