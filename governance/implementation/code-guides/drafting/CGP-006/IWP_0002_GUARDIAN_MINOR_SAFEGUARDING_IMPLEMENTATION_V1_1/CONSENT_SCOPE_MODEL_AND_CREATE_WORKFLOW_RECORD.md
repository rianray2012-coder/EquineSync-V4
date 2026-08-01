# Consent Scope Model And Create Workflow Record

Status: `CORRECTED`

The corrective implementation preserves exact existing-resource consent matching and adds stable create-time scopes so a Guardian is not required to pre-consent to a database id that does not exist yet.

## Scope Hierarchy

- Exact existing-resource scope: the consent `scope_reference` exactly matches the guarded resource scope.
- Student-and-workflow scope: `student:{student_profile_id}:workflow:{workflow}` authorizes the named workflow for the named student only.
- Stable billing agreement scope: `billing_agreement:{billing_agreement_id}` may be supplied by the client before invoice or recurring-charge creation.
- Stable event scope: `event:{event_id}` may be supplied before event-signup service-request creation.
- Workflow-wide scope: `workflow:{workflow}` is accepted only when the consent row explicitly declares `scope_level=workflow`.

The implementation does not accept an empty consent scope and does not convert ordinary consent into an unlimited blanket grant.

Evidence:

- `GMS-T-047`: lesson create can use student/workflow scope even when the server later creates `lesson:{id}`.
- `GMS-T-053`: payment create can use student/workflow scope even when the server later creates `invoice:{id}`.
- `GMS-T-024` and `GMS-T-031`: wrong workflow/resource scopes remain rejected.
- `GMS-T-023`: stale policy versions remain rejected.
