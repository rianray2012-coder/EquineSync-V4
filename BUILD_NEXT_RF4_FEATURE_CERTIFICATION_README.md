# Build-Next RF4 Feature Certification README

Date: 2026-07-06

Status: Codex-reviewed and locked.

RF4 is a narrow feature-completion certification and placeholder-elimination
gate. It inventories the current feature-module registry, classifies visible
surfaces, and pins source evidence that readiness/scaffold surfaces do not
overclaim live functionality.

## Scope

- Evidence, docs, source scan, focused truth-label copy, tests, report, and
  packaging only.
- No provider calls.
- No backend route, schema, permission, billing, privacy, or native-app
  implementation.
- No feature completion for RF5-RF18 domains.
- No founder acceptance auto-marking and no lock until RF4 review is clean.

## Key Outputs

- `docs/RF4_FEATURE_COMPLETION_CERTIFICATION.md`
- `backend/core/rf4_feature_completion_certification.py`
- `backend/scripts/build_rf4_feature_completion_certification.py`
- `backend/tests/test_rf4_feature_completion_certification.py`
- `outputs/rf4_feature_completion_certification_report.md`
- `outputs/build_next_rf4_feature_completion_certification.zip`

## Current RF4 Result

RF4 report status is `ready` with zero blocker rows. Deferred work
remains for RF6/RF8/RF12/RF13/RF14/RF15/RF16/RF17 where the product must build,
merge, hide, or complete the underlying workflows.

Founder also added a pre-lock enrollment note. It is tracked as RF0-F19 and
mapped to RF5/RF7/RF9/RF10/RF18, not implemented in RF4.

## Acceptance Boundary

RF4 may say:

- feature-module keys are classified as `live`, `pilot beta`, `readiness`,
  `scaffold`, `hidden`, or `deprecated`;
- Advanced Reports currently prepares export manifests;
- Group Messaging currently records local status and prepares push previews;
- Forms & Signatures currently tracks local records and provider readiness;
- Mobile Readiness currently represents limited field-recovery and stall-card
  readiness only;
- Integration surfaces are readiness/configuration records only;
- Admin Portal permissions and owner role-intake fallback panels use
  production-safe readiness copy instead of phase/placeholder/shell-shipping
  language.

RF4 must not say:

- full feature completion is achieved across every module;
- live push delivery, provider sync, true PDF/XLSX export generation, native app
  distribution, full offline app support, universal cached reads, or universal
  queued writes are complete;
- Staff Tasks, Supply Inventory, forms/signatures, owner updates, payments, or
  reporting are fully canonicalized.
- general web-based enrollment, individual horse enrollment, or role-specific
  signup flows are implemented by RF4.
