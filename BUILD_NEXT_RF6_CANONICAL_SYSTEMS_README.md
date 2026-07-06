# Build-Next RF6 Canonical Systems Consolidation README

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Scope

RF6 is a canonical-systems consolidation gate. It chooses source-of-truth
posture for duplicated systems and packages evidence for review.

Included:

- Canonical decision matrix for operational tasks, inventory, owner updates,
  documents/signatures, billing entitlements, and integration readiness.
- Explicit migrate, alias, read-only, hide, or defer next actions.
- Founder-decision rows for source-of-truth acceptance and later migration/hide
  work.
- Source-backed proof script, focused tests, generated report, and review
  package.

Not included:

- Data migration.
- Route hiding, redirects, or frontend navigation changes.
- Backend schemas, auth, permissions, billing behavior, or provider calls.
- Stripe, Apple, Google, DocuSign, Resend, MongoDB, Vercel, Render, or Atlas
  mutations.
- Founder acceptance auto-marking.

## Evidence

- `docs/RF6_CANONICAL_SYSTEMS_CONSOLIDATION.md`
- `backend/core/rf6_canonical_systems_consolidation.py`
- `backend/scripts/build_rf6_canonical_systems_consolidation.py`
- `backend/tests/test_rf6_canonical_systems_consolidation.py`
- `outputs/rf6_canonical_systems_consolidation_report.md`

## Package

`outputs/build_next_rf6_canonical_systems_consolidation.zip`

## Review Posture

RF6 may say:

- Task Engine is the canonical operational task system.
- Inventory is the canonical stock/supply system.
- Owner Updates is canonical over feature-module owner media updates.
- Document Signatures is canonical for legal signature workflows.
- Account subscription records are canonical billing entitlement truth.
- Integration readiness surfaces are manifest/status evidence only until later
  provider phases.

RF6 must not say:

- Staff Tasks, Supply Inventory, owner media updates, digital forms, or legacy
  membership/payment feature records have been migrated.
- Any duplicate route has been hidden or redirected.
- Legal signatures, provider sync, billing refunds, payment collection, or
  owner/trainer/provider workflow depth is complete.
- Founder decisions or RF18 UAT are accepted.

## Lock Verification

RF6 is locked after Codex review found no remaining blockers. Verification
covered focused RF6 tests, report generation with blocker failure enabled, zip
integrity, expected zip manifest review, `git diff --check`, and a
secret-shape scan over the RF6 package files.

RF6 must not be expanded after lock. RF7 is the next gated phase.
