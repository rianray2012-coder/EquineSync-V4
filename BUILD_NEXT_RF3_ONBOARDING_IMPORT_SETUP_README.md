# Build Next RF3 - Onboarding Import Setup

Date: 2026-07-06

Status: CODEX-REVIEWED & LOCKED.

## Purpose

RF3 turns onboarding/import/setup into a review-first launch gate without
pretending the full onboarding future is complete. It hardens active CSV imports
for horses and owners, records deferred import kinds, and proves setup and
integration readiness remains truthful.

## Scope

Included:

- CSV preview row-review metadata for active horse and owner imports.
- Explicit `reviewed: true` commit marker from the onboarding UI.
- Backend commit refusal when a CSV import is not marked reviewed.
- Deferred import classification for riders, staff, service providers, and
  feed/medication lists.
- Evidence that setup readiness has required, optional, deferred, blocker, and
  role-based completion states.
- Evidence that integration setup remains manifest/configuration readiness only.

Excluded:

- Full importer rewrite or rich mapping grid.
- AI-assisted auto-mapping or auto-apply.
- Service provider grants or multi-barn provider setup.
- Staff workforce/member import backfill.
- Live Stripe, QuickBooks, Google, DocuSign, Resend, storage, push, or wearable
  credential setup.
- UAT account mutation or provider calls.

## Artifacts

- `docs/RF3_ONBOARDING_IMPORT_SETUP.md`
- `backend/core/rf3_onboarding_import_setup_proof.py`
- `backend/scripts/build_rf3_onboarding_import_setup_proof.py`
- `backend/tests/test_rf3_onboarding_import_setup.py`
- `outputs/rf3_onboarding_import_setup_report.md`
- `outputs/build_next_rf3_onboarding_import_setup.zip`

## Founder Decisions

| Decision | Status | Notes |
| --- | --- | --- |
| Accept RF3 active import scope of horses and owners only. | accepted in RF3 lock | Riders, staff, service providers, and feed/medication list imports need later relationship/model work. |
| Decide whether richer row-level mapping UI is needed before first-client UAT. | deferred by RF3 lock | RF3 exposes backend row-review metadata; UI remains compact preview/commit. |
| Keep integration setup readiness manifest-only. | accepted boundary in RF3 lock | RF3 does not configure credentials or call providers. |

## Lock Note

RF3 is Codex-reviewed and locked. Do not expand RF3 into a full importer rewrite,
AI auto-mapping, live provider setup, service-provider grants, or staff
workforce backfill. RF4 may proceed next as the feature completion
certification and placeholder elimination gate.

## Verification

Run:

```bash
./.venv/bin/python -m pytest backend/tests/test_rf3_onboarding_import_setup.py -q
./.venv/bin/python -m py_compile backend/routes/onboarding.py backend/core/rf3_onboarding_import_setup_proof.py backend/scripts/build_rf3_onboarding_import_setup_proof.py backend/tests/test_rf3_onboarding_import_setup.py
./.venv/bin/python -m backend.scripts.build_rf3_onboarding_import_setup_proof --output outputs/rf3_onboarding_import_setup_report.md --fail-on-blockers
unzip -t outputs/build_next_rf3_onboarding_import_setup.zip
```
