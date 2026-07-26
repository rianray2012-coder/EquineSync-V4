# PRODUCTION_RELEASE_PROCEDURE

**Procedure ID:** `ES-PRODUCTION-RELEASE-PROCEDURE-2026-07-26-02`
**Repository:** `rianray2012-coder/EquineSync-V4`
**Integration branch:** `integrate-emergent-final-zip`
**Production release branch:** `release/production`
**Status:** `ACTIVE_RELEASE_BRANCH_MODEL_WITH_SEPARATE_RELEASE_AUTHORIZATION_REQUIRED`

## Purpose

Separate repository integration from production release.

`integrate-emergent-final-zip` remains the protected integration branch for reviewed repository integration and governance custody. `release/production` is the only branch configured for production promotion.

## Future Production Release Workflow

1. Prepare a release pull request from the approved integration commit into `release/production`.
2. Name the exact integration commit proposed for release.
3. Confirm all required checks pass on the release pull request:
   - `Backend suite is collectable`
   - `Backend known-failure non-regression gate`
   - `Frontend build`
4. Record included pull requests, included security fixes, unresolved risks, database migration effect, environment-variable requirements, rollback commit, and production smoke-test plan.
5. Obtain exact-head Founder production-release authorization.
6. Merge the release pull request using a GitHub merge commit unless separately authorized otherwise.
7. Verify Vercel and Render deploy the same approved release commit.
8. Perform bounded smoke tests.
9. Produce a production-release receipt.

## Minimum Release Receipt Fields

Each production-release receipt must record:

- release pull request number;
- approved release pull request head;
- merge commit into `release/production`;
- Vercel deployment ID, target, aliases, ready time, and commit SHA;
- Render deploy ID, service ID, ready time, and commit SHA;
- required-check run IDs;
- backend health result;
- frontend domain smoke-test result;
- Stripe/payment boundary status;
- rollback commit and rollback method;
- exact Founder production-release authorization reference.

## Stripe Boundary

Do not configure `STRIPE_WEBHOOK_SECRET` without a separate Stripe readiness package and exact Founder financial-activation authorization.

Before activating Stripe payments, require:

- production Stripe account ownership verification;
- production webhook endpoint registration;
- signing-secret configuration;
- secret-custody procedure;
- successful signed webhook smoke test;
- replay and idempotency verification;
- transaction reconciliation procedure;
- refund and dispute handling;
- observability and alerting;
- exact Founder financial-activation authorization.

Unsigned webhook processing must not be restored.

## Retained Limitations

- Existing backend known failures and errors remain controlled technical debt, not accepted behavior.
- Branch separation does not prove pilot readiness.
- Branch separation does not authorize payment activation or money movement.
- Branch separation does not authorize database migrations or production configuration changes.
- Branch separation does not supersede governance, security, privacy, operational, financial, or readiness gates.

## Non-Authorization Boundary

This procedure does not authorize production deployment, a new product release, Stripe secret configuration, payment activation, money movement, database migration, pilot activity, enrollment, acceptance of retained failures, governance supersession, archival deletion, or M4 work.
