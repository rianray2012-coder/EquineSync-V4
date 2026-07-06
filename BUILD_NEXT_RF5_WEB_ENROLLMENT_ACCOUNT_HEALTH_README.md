# Build-Next RF5 Web Enrollment / Account Health README

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Scope

RF5 begins with a narrow web enrollment and account-health opening gate.

Included:

- Public `/enroll` path selector.
- Home-page Join actions routed to enrollment before credential collection.
- Login-page Join action for users without accounts.
- Signup role preselection, visible enrollment context, and locked role/path
  alignment.
- Critical signup data inventory by path.
- Invite-only public posture for rider, guardian, and staff role access.
- Limited-trial fallback copy for rider/guardian/staff users without an invite.
- Limited-trial signup branch that avoids standard paid-plan trial copy.
- Leasee invite caveat with owner/trainer-controlled access and preserved owner
  oversight.
- Admin Portal account-health/customer-success inventory evidence.
- Report generation, focused tests, and package.

Not included:

- Backend enrollment schemas or required-field validation.
- Backend limited-trial enforcement.
- Leasee invite/grant implementation.
- Owner portal hardening or individual owner workflow depth beyond the entry
  path.
- Trainer operating-center implementation.
- Service-provider grant model.
- Billing intervention mutations, discounts, credits, dunning enforcement, or
  Stripe/provider changes.
- Founder acceptance auto-marking.

## Evidence

- `docs/RF5_WEB_ENROLLMENT_ACCOUNT_HEALTH.md`
- `backend/core/rf5_web_enrollment_account_health.py`
- `backend/scripts/build_rf5_web_enrollment_account_health.py`
- `backend/tests/test_rf5_web_enrollment_account_health.py`
- `outputs/rf5_web_enrollment_account_health_report.md`

## Package

`outputs/build_next_rf5_web_enrollment_account_health.zip`

## Review Posture

RF5 may say:

- EquineSync now has a web enrollment selector route before public signup.
- Home and login entry points route no-account users to enrollment.
- Signup can display and carry enrollment-path context while keeping public role
  selection aligned to that path.
- The main public selector has four paths: Individual Horse Owner, Barn Owner /
  Manager, Service Provider, and Trainer.
- Rider, guardian, and staff users are invite-first, with a limited trial
  fallback recorded but not server-enforced in RF5.
- Admin Portal account-health surfaces are inventoried for RF5 follow-up.

RF5 must not say:

- Individual horse enrollment is complete.
- Rider/guardian/staff limited-trial enforcement is complete.
- Leasee access grants are complete.
- Trainer onboarding/workflows are complete.
- Service-provider multi-barn access is complete.
- Billing intervention workflows are live.
- Founder decisions or RF18 UAT are accepted.

## Lock Verification

RF5 is locked after Codex review found no remaining blockers. Verification
covered focused RF5 tests, report generation with blocker failure enabled,
frontend build, zip integrity, zip manifest review, `git diff --check`, and a
secret-shape scan over the RF5 package files.

RF5 must not be expanded after lock. RF6 is the next gated phase.
