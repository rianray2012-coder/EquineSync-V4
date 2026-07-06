# RF3 Onboarding Import Setup Report

Phase: `RF3`

Lock status: `Codex-reviewed and locked`

Overall status: `ready`

## Readiness Rows

| Key | Status | Evidence | Next Action |
| --- | --- | --- | --- |
| `rf3_import_kind_registry` | `ready` | `backend/routes/onboarding.py` declares active and deferred import kinds for RF3. | Founder should confirm whether RF4/RF8/RF10/RF13 should expand the deferred import kinds. |
| `csv_preview_review_contract` | `ready` | CSV preview returns review metadata and does not mutate collections. | RF3 review can decide whether to add richer field-level mapping before RF18 UAT. |
| `csv_commit_review_gate` | `ready` | CSV commit requires an explicit reviewed marker and returns review-required metadata. | RF3 does not add auto-apply or AI-generated mapping. |
| `frontend_review_marker` | `ready` | Onboarding CSV UI only sends commit after preview and passes `reviewed: true`. | RF3 review can decide whether to show row-level warnings in a richer grid. |
| `setup_readiness_truth` | `ready` | Setup readiness distinguishes required, optional, deferred, blocker, and completion-role states. | RF5 can add setup health analytics without weakening completion gates. |
| `integration_setup_truth` | `ready` | Integration setup surfaces remain readiness/configuration manifests and do not claim live provider sync. | Provider-specific live setup remains RF10/RF12/RF13/RF14/RF16 work. |
| `ai_auto_apply_excluded` | `ready` | RF3 onboarding/import paths do not call AI or auto-apply generated mappings. | If AI mapping is added later, it must remain draft/review-first. |
| `deferred_import_expansion` | `deferred` | Riders, staff, service providers, and feed/medication list imports are intentionally deferred until relationship, membership, provider, and care-ledger mapping models are reviewed. | Handle these in RF8/RF10/RF14/RF17 or a later RF3 follow-up only after founder acceptance. |

## Founder Decision Rows

| Decision | Status | RF Phase | Notes |
| --- | --- | --- | --- |
| Accept RF3 active import scope of horses and owners only. | accepted in RF3 lock | RF3 | Additional kinds are documented but deferred because they need relationship and provider models. |
| Decide whether richer row-level mapping UI is needed before first-client UAT. | deferred by RF3 lock | RF3, RF18 | RF3 adds backend row-review metadata; the UI remains a compact preview/commit flow. |
| Keep integration setup readiness manifest-only. | accepted boundary in RF3 lock | RF3, RF10, RF12, RF13, RF14, RF16 | RF3 makes no provider calls and does not configure live credentials. |

## Acceptance Boundary

- RF3 makes CSV import review-first for active horse and owner imports.
- RF3 records deferred import kinds instead of pretending every onboarding domain is bulk-import ready.
- RF3 does not call providers, configure credentials, mutate Stripe/DocuSign/Resend/Google/QuickBooks, or auto-apply AI mappings.
- RF3 does not complete RF8 workforce, RF10 provider, RF13 messaging, RF14 document storage, or RF17 feature-shell work.
