# RF19 Official Staging UAT Evidence Capture

Date: 2026-07-07

Status: Prepared for Codex review.

## Purpose

RF19 converts the locked RF18 UAT ledger into an official staging evidence
capture gate. RF19 does not approve launch; it records whether official
staging evidence exists, which rows are blocked, and what founder decisions
remain.

## Current Status

| Area | RF19 Status |
| --- | --- |
| Locked RF18 input evidence | ready |
| Official staging URL/account roster | blocked pending founder/staging input |
| Sanitized evidence artifact index | blocked pending founder/staging input |
| UAT rows | blocked pending official staging evidence |
| Public launch | no-go until founder acceptance |
| Founder acceptance | required, not auto-marked |

## UAT Rows

| Area | Status | Required Evidence |
| --- | --- | --- |
| Enrollment and signup | blocked pending official staging evidence | Four public signup paths plus invite-first rider/guardian/staff boundaries. |
| Owner/guardian/rider visibility | blocked pending official staging evidence | Relationship-scoped portal views and unrelated-user denial. |
| Staff/trainer workflows | blocked pending official staging evidence | Staff My Work/Today, trainer operating center, assigned-horse, unrelated-horse denial, owner-visible training summary. |
| Service-provider grants | blocked pending official staging evidence | First provider type, grant, revocation, denied access, visit note, unrelated-horse denial. |
| Billing/payment/export truth | blocked pending official staging evidence | Owner billing, admin billing, export, configuration-only payment state, no checkout/client-secret leakage. |
| Documents/signatures/messaging | blocked pending official staging evidence | Guardian-required docs, local form acknowledgement, push-preview/local-log, announcement visibility. |
| Field reliability/native shell | blocked pending official staging evidence | Weak-signal task retry/draft recovery smoke and native shell smoke without store submission. |

## Required Inputs

| Input | Required Content |
| --- | --- |
| `outputs/rf19_official_staging_context.json` | Official staging URL, safe account roster, role mapping, and evidence redaction rules. |
| `outputs/rf19_staging_uat_artifact_index.json` | Sanitized screenshot/log/artifact references, redaction confirmation, and storage paths. |

## Founder Decision Rows

| Decision | Status |
| --- | --- |
| Provide or confirm official staging URL and safe UAT account roster. | requires founder action |
| Confirm evidence redaction and storage rules. | requires founder action |
| Choose the first service-provider type for UAT. | requires founder action |
| Accept, fail, defer, or rerun each RF19 UAT row after evidence capture. | requires founder review |

## Boundary

RF19 does not mutate production, staging, seeded-demo, or UAT accounts by
itself. It does not call providers, submit stores, collect live payments, run
destructive migrations, approve public launch, or auto-mark founder acceptance.
