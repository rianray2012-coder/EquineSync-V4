# RF19 Official Staging UAT Evidence Capture Plan

Date: 2026-07-07

Status: Active implementation plan.

## Purpose

RF19 packages the official staging UAT evidence workflow after locked RF18. It
keeps source truth, official staging evidence, and founder acceptance separate.

## Planned Checks

| Area | RF19 Check |
| --- | --- |
| Locked RF18 evidence | RF18 doc, report, and package are locked and available. |
| Official staging context | Staging URL, safe UAT account roster, role mapping, and redaction rules are present. |
| Artifact index | Sanitized evidence artifacts are indexed without secrets, credentials, private notes, or provider tokens. |
| Enrollment and signup | Evidence covers individual owner, barn owner/manager, trainer, service provider, and invite-first rider/guardian/staff flows. |
| Owner/guardian/rider | Evidence covers relationship-scoped projections and unrelated-user denial. |
| Staff/trainer/provider | Evidence covers assigned work, denied unrelated access, trainer workflows, provider grants, revocation, and visit notes. |
| Billing/export | Evidence proves configuration-only payment truth and no checkout/client-secret/live-money exposure. |
| Documents/messaging | Evidence proves guardian-required docs, local acknowledgement, push-preview/local-log, and announcement visibility without live provider delivery. |
| Field/native | Evidence covers limited field recovery and native shell smoke without full offline or store-submission claims. |

## Stop Condition

Stop after RF19 is packaged for review. Do not mark public launch, first-client
UAT, destructive migrations, or founder acceptance as complete.
