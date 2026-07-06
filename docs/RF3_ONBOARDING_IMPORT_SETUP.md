# RF3 Onboarding Import Setup

Date: 2026-07-06

Status: CODEX-REVIEWED & LOCKED.

## Objective

RF3 addresses the RF0 onboarding pain-point finding by making the existing CSV
import path more explicitly review-first and by documenting setup readiness
truth. It does not attempt to build every future import, AI concierge, provider
setup, or customer-success surface.

## Source Changes

### Import Kind Registry

`backend/routes/onboarding.py` now declares:

- `RF3_ACTIVE_IMPORT_KINDS`
- `RF3_DEFERRED_IMPORT_KINDS`

Active RF3 imports:

- `horses`
- `owners`

Deferred import kinds:

- `riders`
- `staff`
- `service_providers`
- `feed_medication_lists`

Deferred kinds return or raise explicit deferred metadata instead of pretending
they are ready for bulk apply.

### CSV Preview

`POST /onboarding/csv-preview` now returns review metadata:

- `review_required`
- `import_kind_status`
- `row_reviews`
- `review_summary`
- `commit_allowed`

Preview remains non-mutating. It parses rows, checks required identity fields,
flags duplicate warnings, and classifies deferred kinds.

### CSV Commit

`POST /onboarding/csv-commit` now requires the explicit reviewed marker:

```json
{
  "kind": "owners",
  "rows": [],
  "reviewed": true
}
```

If `reviewed` is missing or false, the backend returns a `409` with
`review_required: true`.

### Onboarding UI

`frontend/src/components/onboarding/RecordsStep.jsx` now sends `reviewed: true`
only from the preview-driven commit path and disables commit when
`commit_allowed` is false.

### Setup Readiness

RF3 keeps the existing backend-authoritative readiness shape:

- required steps
- optional steps
- deferred steps
- blockers
- completion roles
- view roles

RF3 does not weaken the BN16B completion gate.

### Integration Readiness

Integration setup remains manifest/configuration readiness:

- credentials required
- app token required
- partner required
- internal readiness where applicable

RF3 does not configure live provider credentials or call providers.

## Evidence Rows

The generated report at `outputs/rf3_onboarding_import_setup_report.md`
contains these rows:

- `rf3_import_kind_registry`
- `csv_preview_review_contract`
- `csv_commit_review_gate`
- `frontend_review_marker`
- `setup_readiness_truth`
- `integration_setup_truth`
- `ai_auto_apply_excluded`
- `deferred_import_expansion`

Overall RF3 status can be `ready` while carrying deferred rows because those
rows belong to later model phases rather than this narrow RF3 gate.

## Deferred Work

RF3 does not complete:

- RF8 staff workforce import/backfill.
- RF10 service provider grant/import model.
- RF13 message-recipient import or delivery truth.
- RF14 document/signature storage import.
- RF17 feature-shell UX truth pass.
- RF18 full UAT migration and launch re-readiness.

## Founder Review

| Decision | Status | Notes |
| --- | --- | --- |
| Accept RF3 active import scope of horses and owners only. | accepted in RF3 lock | This avoids unsafe bulk apply for relationship-heavy records. |
| Decide whether richer row-level mapping UI is needed before first-client UAT. | deferred by RF3 lock | Backend metadata now exists; the UI remains compact. |
| Keep integration setup readiness manifest-only. | accepted boundary in RF3 lock | RF3 does not configure credentials or call providers. |

## Lock Note

RF3 is Codex-reviewed and locked as a narrow onboarding/import/setup gate. RF3
does not authorize claims that all onboarding import paths, AI mapping, provider
setup, or first-value analytics are complete. RF4 may proceed next.

## Verification

Focused RF3 verification:

```bash
./.venv/bin/python -m pytest backend/tests/test_rf3_onboarding_import_setup.py -q
./.venv/bin/python -m backend.scripts.build_rf3_onboarding_import_setup_proof --output outputs/rf3_onboarding_import_setup_report.md --fail-on-blockers
```

Package verification:

```bash
unzip -t outputs/build_next_rf3_onboarding_import_setup.zip
```
