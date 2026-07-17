# Native Offline Synchronization Safety-Critical Exclusion Register

All entries are excluded from the first implementation slice.

| Workflow | Risk | Future prerequisites and controlling canon | Required maturity | Founder gate |
| --- | --- | --- | --- | --- |
| Medication administration/schedule | Duplicate/late dose, stale order, medical privacy | Health policy, Permission, Record Stewardship, Audit; `NOS-P2-02/04` | Completed noncritical phases plus clinical fault testing | Separate medication Tier 5 authorization |
| Allergies/medical alerts | Hidden or stale warning, sensitive disclosure | Passport/Care Circle medical projection and retention policy | Secure projection, revocation, device evidence | Separate medical-view authorization |
| Emergency care/instructions/contacts | Unsafe stale direction, privacy, false notification | Communication/Notice, Health, Identity/Guardian, Audit | Emergency policy, offline disclaimers, escalation evidence | Separate emergency capability gate |
| Injuries/incidents | Safety, legal evidence, immutable authorship | Health, Claims/Disputes, Record Stewardship, Audit | Append-only evidence, media integrity, escalation | Separate incident Tier 5 gate |
| Horse location/quarantine | Safety, custody, cross-barn contamination | RF27 Facility, Relationship, Permission, Horse Lifecycle | Timeline conflicts, current restrictions, supervisor review | Separate location Tier 5 gate |
| Feeding-plan changes | Colic/allergy risk, stale plan | Barn Operations, Health, Permission | Plan revision, qualified roles, duplicate/conflict policy | Separate safety gate |
| Turnout/care restriction changes | Injury/quarantine risk | Barn Operations, Health, Facility, Permission | Restriction projection, stale-state fail closed | Separate safety gate |
| Custody/ownership/facility transfer | Legal authority and Passport continuity | RF31, Relationship, Claims/Authority, Passport | RF31 implementation and evidence | RF31 Founder gate only |
| Financial records/payments/refunds | Financial truth and external effect | Financial Truth, Agreements, Audit | Financial implementation and provider gates | Separate financial authorization |
| Legal agreements/consent | Exact text, signer authority, evidence | Agreement/Consent, Identity, Relationship, Audit | Signing/evidence contract and external boundary | Separate agreement authorization |
| User permissions/roles/membership | Authorization escalation | Identity V2, Permission, Relationship | Canonical online transaction and session revocation | Online-only; separate identity directive |
| Provider data/grants | Private data and external boundary | Provider grants, Relationship, External Architecture | Least privilege, revocation, provider projection | Separate provider gate |
| Destructive deletion | Irreversible loss/retention conflict | Record Stewardship, Claims, Audit | Tombstone, legal hold, recovery, approvals | Separate deletion gate |
| Attachments | Sensitive media, orphaning, bandwidth/storage | Record Stewardship, Audit, Security | Encrypted chunking, hashes, resumability, purge | Later attachment gate |

No completion of task-only phases authorizes an excluded workflow.
Wrapping excluded work in a generic task record does not change its exclusion.
Only a server-owned `LOW_RISK_TASK_V1` classification can admit a first-slice
task, and the client cannot create or broaden that classification.
