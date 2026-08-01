# Relationship Authority And Consent Data Model Record

Status: `IMPLEMENTED`

Repository-native collections and fields:
- `guardian_links`: relationship lifecycle plus `authority_scopes`, `restricted_scopes`, `restricted_workflows`, `disputed`, `expires_at`, `suspended_at`, and `version`.
- `guardian_workflow_consents`: workflow-specific grant records with `student_profile_id`, `guardian_user_id`, `workflow`, `scope_reference`, `policy_version`, `status`, effective/revocation/expiry timestamps, and `version`.
- `student_profiles`: additive `guardian_safeguarding_version` touch point for relationship/consent changes.
- Billing/document/operation records: additive guard scope and policy fields where needed to preserve versioned evidence.

No destructive migration or data backfill was performed. Missing legacy relationship, authority, or consent evidence remains unresolved and fails closed for guarded minor workflows when canonical minor evidence is present.
