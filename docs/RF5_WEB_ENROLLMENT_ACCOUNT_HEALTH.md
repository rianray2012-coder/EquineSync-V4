# RF5 Web Enrollment and Account Health Opening Gate

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Purpose

RF5 opens the Admin Portal Intelligence, Customer Success, Web Enrollment,
Billing Intervention, and Account Health phase without expanding every RF5
domain at once.

This pass addresses the RF0-F19 founder note by adding the public web enrollment
foundation:

- Home-page Join actions route no-account users to `/enroll`.
- Sign-in page now gives no-account users a Join EquineSync action.
- `/enroll` presents four public enrollment paths before credential collection.
- `/signup` requires enrollment context and locks the public role to the chosen
  path.
- Critical signup data is listed by path, but deeper validation and models are
  intentionally deferred.
- Rider, guardian, and staff accounts are not main public enrollment paths.

## Enrollment Paths

| Path | Current RF5 Behavior | Later Phase |
| --- | --- | --- |
| Individual Horse Owner | Routes to `horse_owner` signup with owner/horse/location/emergency-contact data prompts. | RF7 |
| Barn Owner / Manager | Routes to `barn_owner` signup with facility identity and capacity prompts. Barn manager depth remains later workflow work. | RF5/RF12 |
| Service Provider | Routes to `service_provider` signup and preserves existing pending-review posture. | RF10 |
| Trainer | Routes to `trainer` signup and preserves existing pending-review posture. | RF9 |

## Invite-Only And Limited-Trial Caveats

Rider, guardian, and staff enrollment should normally happen only from a signup
link sent by a trainer, barn owner, barn manager, or boss. RF5 keeps those roles
out of the main public enrollment grid.

If a rider, parent/guardian, or staff member tries to sign up without an invite,
RF5 presents a limited seven-day individual-owner trial option. This requires
contact information for a boarding facility, trainer, or another equine
provider. Signup keeps this path separate from the standard paid-plan trial
screen and continues with limited individual-owner access copy. RF5 does not
enforce limited-trial access server-side; RF7/RF18 must validate that this
behaves as a modified individual-owner account and does not grant barn owner,
manager, trainer, or provider features.

Leasee access is recorded as invite-only from the horse owner or the horse's
assigned trainer. The horse owner must retain oversight access. RF5 records this
requirement only; RF7 owns the real invite/grant model.

## Account-Health Inventory

RF5 records that the current Admin Portal already exposes platform-admin
inventory surfaces for users, approvals, facilities, subscriptions, billing,
support, alerts, reports, integrations, settings, and audit logs.

This is evidence only. RF5 does not add new analytics, billing intervention
mutations, dunning enforcement, support-note privacy rules, or sensitive content
inspection in this pass.

## Boundaries

RF5 does not complete:

- Individual owner/horse enrollment depth for owners outside EquineSync barns.
- Limited-trial enforcement for riders, guardians, and staff without invites.
- Leasee invite/access grants.
- Trainer operating-center workflows.
- Service-provider multi-barn/client access grants.
- Billing intervention mutations, nonpayment enforcement, discounts, credits,
  refunds, or app-store billing policy changes.
- RF18 UAT acceptance.
- Backend enrollment-specific schemas or required-field validation.

## Founder Decisions

| Decision | Status | Phase |
| --- | --- | --- |
| Accept first public enrollment path order and labels. | requires founder review | RF5/RF7/RF9/RF10 |
| Decide which critical signup fields become required by path. | requires founder decision | RF5/RF7/RF9/RF10 |
| Decide whether trainer and service-provider signup remains review-gated. | requires founder decision | RF9/RF10 |
| Accept rider/guardian/staff invite-only posture plus limited-trial fallback. | requires founder review | RF5/RF7/RF18 |
| Accept leasee invites as owner/trainer controlled with owner oversight preserved. | requires founder review | RF7 |
| Accept admin account-health inventory as opening evidence only. | requires founder review | RF5 |

## RF5 Lock Note

RF5 is Codex-reviewed and locked after a clean re-review. The generated report
status is `ready` with zero blocker rows.

The lock covers the opening web enrollment/account-health gate only: four public
enrollment paths, invite-first rider/guardian/staff posture, a separate limited
trial signup branch, leasee-access requirements recorded for RF7, and Admin
Portal account-health inventory evidence. RF5 does not add backend enrollment
schemas, backend limited-trial enforcement, leasee grant implementation, billing
mutations, provider calls, founder acceptance auto-marking, or RF18 UAT
acceptance.
