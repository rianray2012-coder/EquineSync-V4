# BN15F Live Today's Pulse Walkthrough Report

Status: Codex-approved & locked - blocked pending safe role sessions

Generated: 2026-07-03

## Scope

BN15F attempts a fresh live/staging walkthrough for the locked BN15E Today's
Pulse founder acceptance ledger. This run verifies live environment reachability
and records the credential blocker that prevents fresh role screenshots in this
Codex session.

No product behavior, role routing, privacy rule, billing/provider flow,
production data, UAT account, credential, or password was changed.

## Environment Evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Frontend reachability | PASS | `https://app.equine-sync.com` returned HTTP 200 from Vercel. |
| API health | PASS | `https://equine-sync-api.onrender.com/api/health` returned `status=ok`, `database=connected`, `environment=production`, `mailer_configured=true`. |
| Database label | PASS | `MongoDB Atlas / Equine Sync / EsProduction / ES_Members`. |
| Frontend deploy marker | PASS | Vercel Production Deploy / 2026-06-30 / commit `5aeea66` / Ready. |
| Backend deploy marker | PASS | Render deploy / 2026-06-30 / commit `5aeea66` / Live. |
| Credential source | BLOCKED | No safe UAT role passwords or authenticated sessions were available to this Codex run. |
| Screenshots | BLOCKED | No credentialed role sessions means no fresh role screenshots were captured. |
| Founder acceptance | BLOCKED | BN15F does not mark rows founder-accepted. |

## Sanitized API Health Snapshot

```json
{
  "status": "ok",
  "service": "equinesync-api",
  "version": "0.1.0",
  "database": "connected",
  "config": {
    "jwt_configured": true,
    "cors_configured": true,
    "environment": "production"
  },
  "dependencies": {
    "mailer_configured": true,
    "email_verification_enforced": false,
    "rate_limiting_enabled": true,
    "auto_seed_enabled": false,
    "seed_route_enabled": false
  }
}
```

## TP Row Walkthrough Results

| TP row | Surface | Candidate account | Expected landing / evidence target | Status | Screenshot | Evidence / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| TP-1 | Platform admin Today's Pulse scope | `uat.platform@equine-sync.com` | `/admin/portal/dashboard` or platform role-home Pulse scope | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Missing safe credential/session for official browser login. |
| TP-2 | Facility admin / barn owner manager-safe Pulse | `uat.facility-admin@equine-sync.com`, `uat.barn-owner@equine-sync.com` | facility admin dashboard and barn-owner role home | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Missing safe credential/session for official browser login. |
| TP-3 | Barn manager Pulse | `uat.manager@equine-sync.com` | manager role-home Pulse cards | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Missing safe credential/session for official browser login. |
| TP-4 | Staff/groom Pulse | `uat.staff@equine-sync.com` | staff role-home Pulse cards | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Missing safe credential/session for official browser login. |
| TP-5 | Trainer Pulse | `uat.trainer@equine-sync.com` | trainer role-home Pulse cards | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Missing safe credential/session for official browser login. |
| TP-6 | Working student Pulse | `uat.working-student@equine-sync.com` | working-student role-home Pulse cards | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Missing safe credential/session for official browser login. |
| TP-7 | Horse owner facility context | `uat.owner@equine-sync.com` | owner-safe horse context | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Missing safe credential/session for official browser login. |
| TP-8 | Guardian / parent context | `uat.guardian@equine-sync.com` | guardian owner-safe context | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Missing safe credential/session for official browser login. |
| TP-9 | Rider / lesson participant context | `uat.participant@equine-sync.com` | rider owner-safe context | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Missing safe credential/session for official browser login. |
| TP-10 | Standalone individual owner | `uat.individual-owner@equine-sync.com` | standalone owner-safe context | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Missing safe credential/session for official browser login. |
| TP-11 | Privacy exclusions | all role rows | verify no private fields appear in screenshots/responses | BLOCKED_PENDING_CREDENTIAL_SESSION | not captured | Requires credentialed screenshots/responses to complete live privacy review. |

## Screenshot Inventory

No fresh role screenshot files were captured in this BN15F run. This is
intentional: a screenshot without a credentialed role session would not satisfy
the fresh live walkthrough gate.

Placeholder folder:

- `outputs/build_next_15f_screenshots/README.md`

Expected future files:

- `outputs/build_next_15f_screenshots/uat-r1-platform-admin.png`
- `outputs/build_next_15f_screenshots/uat-r2a-facility-admin.png`
- `outputs/build_next_15f_screenshots/uat-r2b-barn-owner.png`
- `outputs/build_next_15f_screenshots/uat-r3-barn-manager.png`
- `outputs/build_next_15f_screenshots/uat-r4a-groom.png`
- `outputs/build_next_15f_screenshots/bn13m-t1-trainer.png`
- `outputs/build_next_15f_screenshots/bn13m-w1-working-student.png`
- `outputs/build_next_15f_screenshots/uat-r5-horse-owner.png`
- `outputs/build_next_15f_screenshots/uat-r6-guardian-parent.png`
- `outputs/build_next_15f_screenshots/uat-r7-rider.png`
- `outputs/build_next_15f_screenshots/uat-r8-individual-owner.png`

## Privacy Boundary

This blocked BN15F report includes no credentialed page payloads. It also
contains no passwords, tokens, reset links, API keys, Stripe IDs, DocuSign IDs,
private keys, raw alert payloads, audit diffs, staff notes, or private horse
records.

When BN15F is rerun with safe sessions, screenshots and responses must verify
that they do not expose:

- staff notes;
- raw daily-check payload internals;
- alert triggers;
- `source_check_id`;
- audit diffs;
- auth tokens;
- passwords;
- Stripe IDs;
- DocuSign IDs;
- private owner/admin-only fields;
- private horse records.

## Current Verdict

The live frontend and API are reachable, but BN15F is not lockable as a passing
fresh walkthrough until safe role sessions are supplied and sanitized
screenshots are captured. No TP row is founder-accepted by this report.

Codex lock note: BN15F is approved and locked as a blocked evidence packet. It
does not approve the fresh credentialed walkthrough itself.

## Package

- `outputs/build_next_15f_live_today_pulse_walkthrough.zip`
