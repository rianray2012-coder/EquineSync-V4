# Schema And Index Change Record

Status: `ADDITIVE_ONLY`

Added repository-native index wiring:
- `guardian_links`: `gl_v11_barn_student_guardian_status`, `gl_v11_barn_guardian_status`.
- `guardian_workflow_consents`: `gwc_id_unique`, `gwc_barn_student_workflow_status`, `gwc_barn_guardian_workflow_status`.

Added optional fields without destructive migration:
- Guardian link authority/restriction/lifecycle/version fields.
- Workflow consent records with scope and policy version.
- Student profile `guardian_safeguarding_version` touch counter.
- Minor-bound billing/document/operation guard scope and policy fields.
- Rider subject fields `birthdate`, `minor_status`, and `student_profile_id`.

No backfill, destructive schema migration, or provider-side change was performed.
