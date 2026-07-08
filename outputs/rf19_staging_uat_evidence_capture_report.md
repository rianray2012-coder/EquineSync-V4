# RF19 Official Staging UAT Evidence Capture Report

Phase: `RF19`
Generated at: `2026-07-08T08:28:16.313455+00:00`
Overall status: `blocked_pending_official_staging_evidence`
Public launch status: `no_go_until_founder_acceptance`
Blocked UAT rows: `7`

## Locked RF18 Input Evidence

| Key | Label | Status | Path | Evidence |
| --- | --- | --- | --- | --- |
| rf18_locked_doc | Locked RF18 readiness doc | ready | docs/RF18_QA_UAT_PUBLIC_LAUNCH_READINESS.md | RF18 readiness doc is locked and still requires staging UAT. |
| rf18_locked_report | Locked RF18 report | ready | outputs/rf18_qa_uat_public_launch_readiness_report.md | RF18 report is locked and records seven open UAT rows. |
| rf18_locked_package | Locked RF18 package | ready | outputs/build_next_rf18_qa_uat_public_launch_readiness.zip | RF18 locked package exists. |

## RF19 Official Staging Preconditions

| Key | Label | Status | Path | Evidence |
| --- | --- | --- | --- | --- |
| official_staging_context | Official staging URL and account roster | ready | outputs/rf19_official_staging_context.json | Official staging URL, safe test accounts, role mapping, and redaction rules must be supplied before UAT rows can pass. |
| evidence_artifact_index | Sanitized evidence artifact index | ready | outputs/rf19_staging_uat_artifact_index.json | Sanitized screenshot/log/artifact index must be supplied before UAT rows can pass. |

## UAT Evidence Rows

| Key | Area | Required Roles | Status | Required Evidence | Blocker |
| --- | --- | --- | --- | --- | --- |
| uat_enrollment | Enrollment and signup | anonymous visitor, individual owner, barn owner/manager, trainer, service provider, invite-first rider/guardian/staff | blocked_pending_official_staging_evidence | Official staging capture for four public signup paths and invite-first rider/guardian/staff boundaries. | Online public entry screenshots are captured and indexed, but completed signup, membership step, and credentialed role-session evidence remain pending. |
| uat_owner_guardian | Owner/guardian/rider visibility | owner, guardian/parent, rider, unrelated user, staff preview | blocked_pending_official_staging_evidence | Official staging capture for relationship-scoped owner-safe projections and unrelated-user denial. | Official online UAT owner/guardian/rider accounts did not authenticate or were not verified before rate limiting; role-scoped portal evidence remains pending. |
| uat_staff_trainer | Staff/trainer workflows | staff, trainer, barn manager/admin, unrelated staff | blocked_pending_official_staging_evidence | Official staging capture for My Work/Today, trainer operating center, assigned-horse, unrelated-horse denial, and owner-visible summaries. | Official online UAT staff/trainer/barn accounts did not authenticate or were not verified before rate limiting; workflow evidence remains pending. |
| uat_provider | Service-provider grants | chosen provider type, barn manager/admin, horse owner, unrelated provider | blocked_pending_official_staging_evidence | Official staging capture for grant, revocation, denied access, visit note, and unrelated-horse denial. | Service-provider free and premium public entries are captured, but the official provider UAT account did not authenticate; grant/revocation/visit-note evidence remains pending. |
| uat_billing | Billing/payment/export truth | owner, barn admin/manager, platform/admin role where applicable | blocked_pending_official_staging_evidence | Official staging capture for owner billing, admin billing, export truth, and no checkout URL/client-secret/live-money exposure. | Billing/export role evidence remains blocked until owner/admin UAT accounts authenticate; live money movement remains out of scope. |
| uat_documents_messaging | Documents, signatures, messaging | owner, guardian/parent, barn admin/manager, staff, recipient user | blocked_pending_official_staging_evidence | Official staging capture for guardian-required document requests, local acknowledgement, push-preview/local-log, and announcement visibility. | Documents/messaging role evidence remains blocked until owner/guardian/admin/staff UAT accounts authenticate; live provider delivery remains out of scope. |
| uat_field_native | Field reliability and native shell | field staff, trainer, native-shell smoke actor, owner where relevant | blocked_pending_official_staging_evidence | Official staging capture for weak-signal task retry, draft recovery, and native shell smoke without store submission/full offline claims. | Field/native evidence remains blocked until staff/trainer UAT accounts authenticate and the weak-signal/native smoke can be run. |

## Issues

| Severity | Category | Key | Message |
| --- | --- | --- | --- |
| blocker | uat_evidence | uat_enrollment | Online public entry screenshots are captured and indexed, but completed signup, membership step, and credentialed role-session evidence remain pending. |
| blocker | uat_evidence | uat_owner_guardian | Official online UAT owner/guardian/rider accounts did not authenticate or were not verified before rate limiting; role-scoped portal evidence remains pending. |
| blocker | uat_evidence | uat_staff_trainer | Official online UAT staff/trainer/barn accounts did not authenticate or were not verified before rate limiting; workflow evidence remains pending. |
| blocker | uat_evidence | uat_provider | Service-provider free and premium public entries are captured, but the official provider UAT account did not authenticate; grant/revocation/visit-note evidence remains pending. |
| blocker | uat_evidence | uat_billing | Billing/export role evidence remains blocked until owner/admin UAT accounts authenticate; live money movement remains out of scope. |
| blocker | uat_evidence | uat_documents_messaging | Documents/messaging role evidence remains blocked until owner/guardian/admin/staff UAT accounts authenticate; live provider delivery remains out of scope. |
| blocker | uat_evidence | uat_field_native | Field/native evidence remains blocked until staff/trainer UAT accounts authenticate and the weak-signal/native smoke can be run. |

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Reset/seed or correct the official online UAT account roster. | requires founder action | The app/API are reachable and public enrollment evidence is captured, but the supplied UAT credentials did not authenticate online. |
| Confirm evidence redaction and storage rules. | requires founder action | Screenshots/logs must not expose credentials, tokens, payment secrets, provider secrets, private barn data, or owner-hidden staff notes. |
| Choose the first service-provider type for UAT. | requires founder action | RF10 supports explicit grants, but RF19 needs a concrete provider type for official staging execution. |
| Accept, fail, defer, or rerun each RF19 UAT row after evidence is captured. | requires founder review | RF19 may mark rows ready for founder review, but does not mark founder acceptance by itself. |

## RF19 Boundary

- RF19 packages the official staging UAT evidence ledger and blocker state.
- RF19 does not mutate production, staging, seeded-demo, or UAT accounts by itself.
- RF19 does not call providers, submit stores, collect live payments, run destructive migrations, approve public launch, or auto-mark founder acceptance.
- Public launch remains `no_go_until_founder_acceptance` until official staging evidence is supplied and founder acceptance is explicit.
