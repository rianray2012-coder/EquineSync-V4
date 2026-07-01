# Build-Next-13O Credentialed Role Screenshot Pass Report

Status: READY FOR CODEX REVIEW - BLOCKED EVIDENCE RUN

Generated: 2026-07-01

## Scope

BN13O attempts the credentialed screenshot pass after BN13N created the
production-safe account seeding script. In this run, the official frontend and
API are reachable, but the BN13N production script was not run here and no safe
role credentials or authenticated sessions were available.

Founder acceptance: not recorded.

This report is a blocked evidence run, not a credentialed role-smoke completion.

## Environment Evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Frontend reachability | PASS | `https://app.equine-sync.com` returned HTTP 200 from Vercel. |
| API health | PASS | `https://equine-sync-api.onrender.com/api/health` returned `status=ok`, `database=connected`, `environment=production`. |
| Database label | PASS | `MongoDB Atlas / Equine Sync / EsProduction / ES_Members`. |
| Frontend deploy marker | PASS | Vercel Production Deploy / 2026-06-30 / commit `5aeea66` / Ready. |
| Backend deploy marker | PASS | Render deploy / 2026-06-30 / commit `5aeea66` / Live. |
| BN13N script execution | BLOCKED | No safe production Render shell session was available to this Codex run, so the script was not executed. |
| Credential source | BLOCKED | No safe UAT role passwords or authenticated sessions were available to this run. |
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

## BN13N Script Status

The locked BN13N script remains the approved way to prepare these accounts:

- `backend/scripts/seed_bn13_role_smoke_accounts.py`
- dry-run first,
- production writes require `--allow-prod`,
- password rotation requires `--reset-passwords`,
- password values must be copied out of band only.

This BN13O package did not run that script and did not write to production
MongoDB.

## Role Screenshot Results

| Row | Role | Candidate account | Expected first landing | Status | Screenshot | Evidence / blocker |
| --- | --- | --- | --- | --- | --- | --- |
| UAT-R1 | `platform_admin` | `uat.platform@equine-sync.com` | `/admin/portal/dashboard` | BLOCKED | not captured | BN13N script execution and safe credential/session unavailable to this run. |
| UAT-R2a | `admin` | `uat.facility-admin@equine-sync.com` | `/onboarding` when setup incomplete, else `/dashboard` | BLOCKED | not captured | BN13N script execution, setup-state confirmation, and safe credential/session unavailable to this run. |
| UAT-R2b | `barn_owner` | `uat.barn-owner@equine-sync.com` | `/role-home/barn-owner` | BLOCKED | not captured | Dedicated barn-owner credential must be seeded or confirmed through BN13N. |
| BN13M-T1 | `trainer` | `uat.trainer@equine-sync.com` | `/role-home/trainer` | BLOCKED | not captured | Dedicated trainer credential must be seeded or confirmed through BN13N. |
| UAT-R3 | `barn_manager` | `uat.manager@equine-sync.com` | `/role-home/manager` | BLOCKED | not captured | BN13N script execution and safe credential/session unavailable to this run. |
| UAT-R4a | `groom` | `uat.staff@equine-sync.com` | `/role-home/staff` | BLOCKED | not captured | Groom marker and credential must be seeded or confirmed through BN13N. |
| BN13M-W1 | `working_student` | `uat.working-student@equine-sync.com` | `/role-home/staff` | BLOCKED | not captured | Dedicated working-student credential must be seeded or confirmed through BN13N. |
| UAT-R5 | `horse_owner` | `uat.owner@equine-sync.com` | `/owner/horses/{horseId}` when linked, else `/role-home/owner` | BLOCKED | not captured | Owner-horse linkage and safe credential/session unavailable to this run. |
| UAT-R6 | `parent` | `uat.guardian@equine-sync.com` | `/role-home/guardian` | BLOCKED | not captured | BN13N script execution and safe credential/session unavailable to this run. |
| UAT-R7 | `rider` | `uat.participant@equine-sync.com` | `/role-home/rider` | BLOCKED | not captured | Rider marker and credential must be seeded or confirmed through BN13N. |
| UAT-R8 | `horse_owner` standalone | `uat.individual-owner@equine-sync.com` | `/role-home/owner` unless linked to a horse | BLOCKED | not captured | Standalone owner marker and safe credential/session unavailable to this run. |

## Screenshot Inventory

No screenshot files were created in this BN13O run. This is intentional: a
screenshot without a credentialed role session would not satisfy the evidence
gate.

Expected future folder:

- `outputs/build_next_13o_role_smoke_screenshots/`

## Secret Safety

This report contains no passwords, tokens, reset links, API keys, Stripe IDs,
DocuSign IDs, private keys, or authenticated session data. It records only
candidate account emails, expected routes, status, and sanitized blockers.

## Required To Clear The Blockers

1. Run the BN13N script in the production Render shell.
2. Review the dry-run output before applying.
3. Copy any one-time passwords out of band.
4. Log into each role through a clean browser session.
5. Capture sanitized screenshots for every role row.
6. Mark each row PASS, BLOCKED, or FAIL with screenshot evidence for PASS rows.

## Strictly Unchanged

- No product behavior changes.
- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, launch, UAT, Stripe, Apple, or DocuSign changes.
- No role-routing changes.
- No intake-field changes.
- No seeded-demo or UAT-account mutation.
