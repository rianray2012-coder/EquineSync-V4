# Native Offline Sync Capability Matrix

These classifications are target governance recommendations, not current runtime claims.

| Workflow | Current state | Recommended target class | Rule |
| --- | --- | --- | --- |
| Sign-in, password reset, MFA, account recovery | Online only | `ONLINE_ONLY` | Identity proof and revocation require server authority. |
| Permission, role, membership, guardian, and provider-grant changes | Online only | `OFFLINE_PROHIBITED` | Offline state may never grant or expand authority. |
| Billing, refunds, payouts, agreements, legal submission | Online only | `OFFLINE_PROHIBITED` | Financial and legal side effects require current canonical validation. |
| Horse transfer, ownership, custody, Passport authority | Online only | `OFFLINE_PROHIBITED` | RF31 and relationship/claims canon govern contested authority. |
| Horse roster and basic assigned-horse summary | Online only | `OFFLINE_READ_ONLY` | Cache only projected, lease-authorized fields with visible age. |
| Medical history, allergies, emergency instructions | Online only | `OFFLINE_READ_ONLY` | Encrypted minimal cache; explicit sensitivity and staleness warnings. |
| General profile edits | Online only | `OFFLINE_DRAFT_ALLOWED` | Draft locally; canonical write after permission and revision validation. |
| Task completion and skip | Limited queued mutation | `OFFLINE_MUTATION_ALLOWED` | Stable idempotency, original actor, current permission revalidation, conflict result. |
| Feed and turnout completion | Online only | `OFFLINE_CRITICAL_OPERATION` | Append-only observation with stale-plan warning and supervisor exception review. |
| Medication administration | Online only | `OFFLINE_CRITICAL_OPERATION` | Strict authorization lease, immutable administration event, duplicate-dose defense, mandatory reconciliation. |
| Medication order or schedule change | Online only | `OFFLINE_PROHIBITED` | Clinical/source authority must be current. |
| Incident and injury observation | Online only | `OFFLINE_CRITICAL_OPERATION` | Preserve original observation and time; correction is additive. |
| Horse location observation | Online only | `OFFLINE_CRITICAL_OPERATION` | Never silently overwrite a newer canonical location; conflict review required. |
| Facility assignment or quarantine change | Online only | `OFFLINE_PROHIBITED` | Safety and capacity authority require current server state. |
| Inventory consumption or adjustment | Online only | `OFFLINE_MUTATION_ALLOWED` | Record delta events, never stale absolute quantity replacement. |
| Equipment inspection and maintenance note | Online only | `OFFLINE_MUTATION_ALLOWED` | Append event with idempotency and revision lineage. |
| Lesson, appointment, and calendar changes | Online only | `OFFLINE_DRAFT_ALLOWED` | Resource conflicts and invitations require server confirmation. |
| Messages and notices | Online only | `OFFLINE_DRAFT_ALLOWED` | Draft only; delivery and recipient authorization remain online. |
| Photos and attachments | Online only | `OFFLINE_DRAFT_ALLOWED` | Encrypted staged blob with resumable upload and orphan cleanup. |
| Analytics and dashboards | Online only | `OFFLINE_READ_ONLY` | Clearly aged local projection; never presented as current operational truth. |
| Administrative exports and support access | Online only | `OFFLINE_PROHIBITED` | Broad data extraction is not compatible with offline least privilege. |

## Classification Rules

- `ONLINE_ONLY`: no local business-data guarantee; server required.
- `OFFLINE_READ_ONLY`: permission-projected cache only, with age and source indicators.
- `OFFLINE_DRAFT_ALLOWED`: local content is explicitly unsubmitted and noncanonical.
- `OFFLINE_MUTATION_ALLOWED`: durable operation envelope may synchronize later.
- `OFFLINE_CRITICAL_OPERATION`: offline entry is allowed only with stronger safety, authority, acknowledgment, and reconciliation controls.
- `OFFLINE_PROHIBITED`: local execution or queued side effect is not permitted.

