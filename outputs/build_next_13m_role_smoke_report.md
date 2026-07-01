# Build-Next-13M Credentialed Role Smoke Report

Status: READY FOR CODEX REVIEW

Generated: 2026-07-01

## Scope

BN13M attempts the credentialed role-smoke evidence phase defined by BN13L. In
this run, the official frontend and API are reachable, but credentialed role
sessions are unavailable, so every role login row remains blocked.

Founder acceptance: not recorded.

## Environment Evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Frontend reachability | PASS | `https://app.equine-sync.com` returned HTTP 200 from Vercel. |
| API health | PASS | `https://equine-sync-api.onrender.com/api/health` returned `status=ok`, `database=connected`, `environment=production`. |
| Database label | PASS | `MongoDB Atlas / Equine Sync / EsProduction / ES_Members`. |
| Frontend deploy marker | PASS | Vercel Production Deploy / 2026-06-30 / commit `5aeea66` / Ready. |
| Backend deploy marker | PASS | Render deploy / 2026-06-30 / commit `5aeea66` / Live. |
| Credential source | BLOCKED | No safe UAT role credentials or authenticated sessions were available to this run. |
| Screenshots | BLOCKED | No credentialed role sessions means no role screenshots were captured. |
| Founder acceptance | BLOCKED | Founder acceptance is not recorded in this blocked evidence run. |

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

## Role Smoke Results

| Row | Role | Candidate account | Expected first landing | Status | Screenshot | Evidence / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| UAT-R1 | `platform_admin` | `uat.platform@equine-sync.com` | `/admin/portal/dashboard` | BLOCKED | not captured | Missing safe credential/session for official browser login. |
| UAT-R2a | `admin` | `uat.facility-admin@equine-sync.com` | `/onboarding` when setup incomplete, else `/dashboard` | BLOCKED | not captured | Missing safe credential/session and setup-state confirmation. |
| UAT-R2b | `barn_owner` | TBD | `/role-home/barn-owner` | BLOCKED | not captured | Dedicated barn-owner credential or confirmed UAT-R2 role marker needed. |
| BN13M-T1 | `trainer` | TBD | `/role-home/trainer` | BLOCKED | not captured | Dedicated trainer credential needed. |
| UAT-R3 | `barn_manager` | `uat.manager@equine-sync.com` | `/role-home/manager` | BLOCKED | not captured | Missing safe credential/session for official browser login. |
| UAT-R4a | `groom` | `uat.staff@equine-sync.com` or TBD | `/role-home/staff` | BLOCKED | not captured | Safe credential and exact `groom` role marker confirmation needed. |
| BN13M-W1 | `working_student` | TBD | `/role-home/staff` | BLOCKED | not captured | Dedicated working-student credential needed. |
| UAT-R5 | `horse_owner` | `uat.owner@equine-sync.com` | `/owner/horses/{horseId}` when linked, else `/role-home/owner` | BLOCKED | not captured | Safe credential/session and owner-horse linkage confirmation needed. |
| UAT-R6 | `parent` | `uat.guardian@equine-sync.com` | `/role-home/guardian` | BLOCKED | not captured | Missing safe credential/session for official browser login. |
| UAT-R7 | `rider` | `uat.participant@equine-sync.com` or TBD | `/role-home/rider` | BLOCKED | not captured | Safe credential and exact `rider` role marker confirmation needed. |
| UAT-R8 | `horse_owner` standalone | `uat.individual-owner@equine-sync.com` | `/role-home/owner` unless linked to a horse | BLOCKED | not captured | Safe credential/session and individual-owner marker confirmation needed. |

## Screenshot Inventory

No screenshot files were created in this BN13M run. This is intentional: a
screenshot without a credentialed role session would not satisfy the BN13M
evidence gate.

Expected future folder:

- `outputs/build_next_13m_role_smoke_screenshots/`

## Secret Safety

This report contains no passwords, tokens, reset links, API keys, Stripe IDs,
DocuSign IDs, private keys, or authenticated session data. It records only
candidate account emails, expected routes, status, and sanitized blockers.

## Required To Clear The Blockers

1. Supply role credentials out of band or log into each role manually during a
   supervised browser evidence run.
2. Confirm or create the missing dedicated role accounts:
   - barn owner,
   - trainer,
   - working student.
3. Confirm exact markers for shared/ambiguous UAT accounts:
   - UAT-R2 facility admin vs barn owner,
   - UAT-R4 staff vs groom,
   - UAT-R7 lesson participant vs rider.
4. Capture sanitized screenshots for every role row.
5. Re-run BN13M with the screenshot files and completed result rows.

## Strictly Unchanged

- No product behavior changes.
- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, launch, UAT, Stripe, Apple, or DocuSign changes.
- No role-routing changes.
- No intake-field changes.
- No seeded-demo or UAT-account mutation.
