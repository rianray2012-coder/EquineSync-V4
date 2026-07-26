# Adversarial, Negative, and Abuse Scenarios

**Status:** `DESIGN_SCENARIOS_NOT_EXECUTED`

| Scenario | Attack or failure | Required result | Evidence |
| --- | --- | --- | --- |
| `RAP-ADV-001` | Role label presented without source authority | Deny without enumeration | Actor, role claim, missing basis, denial reason |
| `RAP-ADV-002` | Forged or wrong-principal representation | Deny and preserve attributed claim | Principal chain, source mismatch, denial |
| `RAP-ADV-003` | Delegation exceeds source scope or chain depth | Deny excess scope; do not partially expand silently | Source/delegation versions, evaluated scope |
| `RAP-ADV-004` | Source authority revoked during session | Advance watermark and invalidate affected projection | Revocation, watermark, session/action result |
| `RAP-ADV-005` | Tenant identifier substituted | Deny without disclosing target existence | Tenant/context, request, denial class |
| `RAP-ADV-006` | Cached allow used after restriction | Deny at trusted boundary | Cached/current versions, restriction, result |
| `RAP-ADV-007` | Provider self-activates via profile or directory | Deny; profile remains non-authoritative | Profile claim, absent relationship basis |
| `RAP-ADV-008` | API key or integration treated as authority | Deny action beyond separately evaluated projection | Credential, actor/principal, decision |
| `RAP-ADV-009` | Appointment or schedule assignment creates access | Deny unless independent authority chain passes | Schedule state, source chain, result |
| `RAP-ADV-010` | Payment or payout treated as permission | Deny; preserve financial/domain separation | Payment state, absent authority basis |
| `RAP-ADV-011` | Portal visibility or invitation creates relationship | Deny authority; preserve surface-only state | Portal event, decision, safe explanation |
| `RAP-ADV-012` | Guardian claim conflicts with protective restriction | Restriction prevails; block and escalate safely | Guardian basis, restriction, safeguarding evidence |
| `RAP-ADV-013` | AI infers representation or emergency authority | Reject inferred truth and require approved source/human action | Prompt/output reference, denial, escalation |
| `RAP-ADV-014` | Offline proposal replayed after expiry | Deduplicate and deny stale action | Idempotency, expiry, watermark, result |
| `RAP-ADV-015` | Clock manipulation extends delegation | Deny or step up on clock uncertainty | Device/server time, confidence, decision |
| `RAP-ADV-016` | Mass enumeration/export through reporting | Deny or return minimum aggregate under policy | Query, projection, suppression, reason |
| `RAP-ADV-017` | Support actor impersonates user invisibly | Deny invisible impersonation; require ticketed bounded access | Ticket, actor chain, scope, notice |
| `RAP-ADV-018` | Correction attempts to erase prior denial | Preserve prior evidence and create successor | Original and successor IDs/digests |

These scenarios define expected documentary outcomes only. No adversarial reviewer or executable scenario was run.
