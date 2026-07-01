# Build-Next-13O Credentialed Role Screenshot Pass Report

Status: READY FOR CODEX REVIEW - SCREENSHOTS CAPTURED

Generated: 2026-07-01

## Scope

BN13O completes the credentialed screenshot pass after BN13N created the
production-safe account seeding script. The official frontend and API are
reachable, role credentials were used out of band, and screenshots were captured
for all 11 role rows.

Founder acceptance: not recorded.

This report proves role-session screenshot capture. It does not clear broad
public launch.

## Environment Evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Frontend reachability | PASS | `https://app.equine-sync.com` returned HTTP 200 from Vercel. |
| API health | PASS | `https://equine-sync-api.onrender.com/api/health` returned `status=ok`, `database=connected`, `environment=production`. |
| Database label | PASS | `MongoDB Atlas / Equine Sync / EsProduction / ES_Members`. |
| Frontend deploy marker | PASS | Vercel Production Deploy / 2026-06-30 / commit `5aeea66` / Ready. |
| Backend deploy marker | PASS | Render deploy / 2026-06-30 / commit `5aeea66` / Live. |
| BN13N targeted reset support | PASS | Targeted one-account reset support was added and pushed in commit `f171cf8`. |
| Credential source | PASS | Role passwords were handled out of band and are not included in this package. |
| Screenshots | PASS | 11/11 credentialed role screenshots captured. |
| Founder acceptance | BLOCKED | Founder acceptance is not recorded in this evidence run. |

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

## Role Screenshot Results

| Row | Role | Candidate account | Expected first landing | Status | Screenshot | Evidence / note |
| --- | --- | --- | --- | --- | --- | --- |
| UAT-R1 | `platform_admin` | `uat.platform@equine-sync.com` | `/admin/portal/dashboard` | PASS | `outputs/build_next_13o_role_smoke_screenshots/uat-r1-platform-admin.png` | Admin Portal dashboard visible with platform-admin shell. |
| UAT-R2a | `admin` | `uat.facility-admin@equine-sync.com` | facility dashboard or setup state | PASS | `outputs/build_next_13o_role_smoke_screenshots/uat-r2a-facility-admin.png` | Stable Command / facility-admin shell visible. |
| UAT-R2b | `barn_owner` | `uat.barn-owner@equine-sync.com` | `/role-home/barn-owner` | PASS | `outputs/build_next_13o_role_smoke_screenshots/uat-r2b-barn-owner.png` | Facility Founder setup intent visible with barn-owner shell. |
| BN13M-T1 | `trainer` | `uat.trainer@equine-sync.com` | `/role-home/trainer` | PASS | `outputs/build_next_13o_role_smoke_screenshots/bn13m-t1-trainer.png` | Trainer setup intent visible with trainer shell. |
| UAT-R3 | `barn_manager` | `uat.manager@equine-sync.com` | `/role-home/manager` | PASS_WITH_RESIDUAL | `outputs/build_next_13o_role_smoke_screenshots/uat-r3-barn-manager.png` | Manager shell loads; intake panel shows `Not Found` residual. |
| UAT-R4a | `groom` | `uat.staff@equine-sync.com` | `/role-home/staff` | PASS_WITH_RESIDUAL | `outputs/build_next_13o_role_smoke_screenshots/uat-r4a-groom.png` | Staff/groom shell loads; intake panel shows `Not Found` residual. |
| BN13M-W1 | `working_student` | `uat.working-student@equine-sync.com` | `/role-home/staff` | PASS | `outputs/build_next_13o_role_smoke_screenshots/bn13m-w1-working-student.png` | Staff setup intent visible with working-student shell. |
| UAT-R5 | `horse_owner` | `uat.owner@equine-sync.com` | owner home / owner horse surface | PASS_WITH_RESIDUAL | `outputs/build_next_13o_role_smoke_screenshots/uat-r5-horse-owner.png` | Horse-owner shell loads; intake panel shows `Not Found` residual. |
| UAT-R6 | `parent` | `uat.guardian@equine-sync.com` | `/role-home/guardian` | PASS_WITH_RESIDUAL | `outputs/build_next_13o_role_smoke_screenshots/uat-r6-guardian-parent.png` | Guardian shell loads; intake panel shows `Not Found` residual. |
| UAT-R7 | `rider` | `uat.participant@equine-sync.com` | `/role-home/rider` | PASS_WITH_RESIDUAL | `outputs/build_next_13o_role_smoke_screenshots/uat-r7-rider.png` | Rider shell loads; intake panel shows `Not Found` residual. |
| UAT-R8 | `horse_owner` standalone | `uat.individual-owner@equine-sync.com` | `/role-home/owner` unless linked to a horse | PASS | `outputs/build_next_13o_role_smoke_screenshots/uat-r8-individual-owner.png` | Standalone owner setup visible with individual-owner shell. |

## Screenshot Inventory

All screenshot files are PNGs and were verified for signature and dimensions.

| File | Dimensions |
| --- | --- |
| `uat-r1-platform-admin.png` | 3420x1872 |
| `uat-r2a-facility-admin.png` | 3420x1872 |
| `uat-r2b-barn-owner.png` | 3420x1872 |
| `bn13m-t1-trainer.png` | 3420x1872 |
| `uat-r3-barn-manager.png` | 3420x1872 |
| `uat-r4a-groom.png` | 3420x1872 |
| `bn13m-w1-working-student.png` | 3420x1872 |
| `uat-r5-horse-owner.png` | 3420x1872 |
| `uat-r6-guardian-parent.png` | 3420x1872 |
| `uat-r7-rider.png` | 3420x1872 |
| `uat-r8-individual-owner.png` | 3420x1872 |

## Residual QA Notes

BN13O is an evidence phase, so no product behavior was changed. The screenshot
pass found a residual role-home data issue: the manager, groom, horse-owner,
guardian, and rider surfaces load the correct role shell but display a `Not
Found` message in the central intake/profile panel. This should be handled in a
follow-up UX/data-hardening phase before founder acceptance.

The screenshots also reinforce the future title-case convention: role/profile
landing page titles should use consistent Title Case during the next profile
landing page build-out.

## Secret Safety

This report contains no passwords, tokens, reset links, API keys, Stripe IDs,
DocuSign IDs, private keys, or authenticated session data. It records only
candidate account emails, expected routes, screenshot file paths, and sanitized
QA notes.

## Required Before Founder Acceptance

1. Review the 11 screenshots.
2. Decide whether the `Not Found` intake-panel residual blocks acceptance or
   moves into the next UX/data-hardening phase.
3. Confirm no screenshot exposes passwords, tokens, private staff-only owner
   data, raw alert payloads, Stripe IDs, or DocuSign IDs.
4. Record founder acceptance separately if the evidence is approved.

## Strictly Unchanged

- No product behavior changes.
- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, launch, UAT, Stripe, Apple, or DocuSign changes.
- No role-routing changes.
- No intake-field changes.
- No seeded-demo or UAT-account mutation in this package.
