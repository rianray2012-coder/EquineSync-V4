# Commit-Time Revalidation And Concurrency Evidence

Status: `CORRECTED`

The central guard continues to compute a state token from student, guardian-link, and workflow-consent rows. Corrected route callers now pass persisted or supplied `guardian_state_token` values into `guardian_minor_workflow_gate` through `expected_state_token`.

## Enforced Transitions

- Lesson and training creates accept supplied `guardian_state_token` and persist the resulting token.
- Event-signup create persists the resulting token; event approval re-runs the full guard with the persisted token before approving.
- Invoice create/pay and recurring-charge create/update/materialize persist and enforce guard state tokens.
- Document request create and sandbox-envelope transition persist and enforce guard state tokens.

Evidence:

- `GMS-T-028`: stale state token blocks document-signature retry.
- `GMS-T-034`: revocation after a previously observed token is rejected.
- `GMS-T-036`: stale message token after revocation is rejected.
- `GMS-T-048`: consent withdrawal after a previously observed token is rejected.
- `GMS-T-051`: event approval revalidates before status mutation and uses the stored token.
- `GMS-T-054`: document transitions persist and enforce stored tokens.
