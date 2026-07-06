# BN15F.1 Credentialed Live Today's Pulse Walkthrough Report

Status: Ready for Codex review - credentialed screenshots complete; founder acceptance not recorded

Generated: 2026-07-03

## Scope

BN15F.1 is the credentialed follow-up to locked BN15F. It uses the current
production-like frontend, backend, and database label and attempts to capture
fresh Today’s Pulse evidence for the BN15E TP-1 through TP-11 rows.

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
| Credential source | PASS | TP-1 through TP-10 role sessions were available through safe browser handoff; TP-11 completed as screenshot privacy sweep across the captured role evidence. |
| Screenshots | PASS | TP-1 through TP-10 screenshots captured; TP-11 screenshot privacy sweep complete. |
| Founder acceptance | BLOCKED | BN15F.1 does not mark rows founder-accepted. |

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
| TP-1 | Platform admin Today's Pulse scope | `uat.platform@equine-sync.com` | `/admin/portal/dashboard` or platform role-home Pulse scope | PASS | `outputs/build_next_15f1_screenshots/uat-r1-platform-admin.png` | Fresh credentialed Platform Admin screenshot captured from official live app. |
| TP-2 | Facility admin / barn owner manager-safe Pulse | `uat.facility-admin@equine-sync.com`, `uat.barn-owner@equine-sync.com` | facility admin dashboard and barn-owner role home | PASS | `outputs/build_next_15f1_screenshots/uat-r2a-facility-admin.png`; `outputs/build_next_15f1_screenshots/uat-r2a-facility-admin-dashboard-top.png`; `outputs/build_next_15f1_screenshots/uat-r2a-facility-admin-dashboard-pulse.png`; `outputs/build_next_15f1_screenshots/uat-r2b-barn-owner.png`; `outputs/build_next_15f1_screenshots/uat-r2b-barn-owner-dashboard-top.png`; `outputs/build_next_15f1_screenshots/uat-r2b-barn-owner-dashboard-pulse.png` | Fresh credentialed Facility Admin and Barn Owner screenshots captured from official live app. Facility Admin and Barn Owner dashboards were each captured in two supporting parts due viewport constraints. |
| TP-3 | Barn manager Pulse | `uat.manager@equine-sync.com` | manager role-home Pulse cards | PASS | `outputs/build_next_15f1_screenshots/uat-r3-barn-manager-dashboard-top.png`; `outputs/build_next_15f1_screenshots/uat-r3-barn-manager-dashboard-pulse.png` | Fresh credentialed Barn Manager dashboard screenshots captured from official live app in two supporting parts due viewport constraints. |
| TP-4 | Staff/groom Pulse | `uat.staff@equine-sync.com` | staff role-home Pulse cards | PASS | `outputs/build_next_15f1_screenshots/uat-r4a-groom.png` | Fresh credentialed Staff/Groom Operational Pulse screenshot captured from official live app. |
| TP-5 | Trainer Pulse | `uat.trainer@equine-sync.com` | trainer role-home Pulse cards | PASS | `outputs/build_next_15f1_screenshots/bn13m-t1-trainer.png` | Fresh credentialed Trainer dashboard screenshot captured from official live app. |
| TP-6 | Working student Pulse | `uat.working-student@equine-sync.com` | working-student role-home Pulse cards | PASS | `outputs/build_next_15f1_screenshots/bn13m-w1-working-student.png` | Fresh credentialed Working Student role-home screenshot captured from official live app. |
| TP-7 | Horse owner facility context | `uat.owner@equine-sync.com` | owner-safe horse context | PASS | `outputs/build_next_15f1_screenshots/uat-r5-horse-owner.png` | Fresh credentialed Horse Owner owner-portal screenshot captured from official live app. |
| TP-8 | Guardian / parent context | `uat.guardian@equine-sync.com` | guardian owner-safe context | PASS | `outputs/build_next_15f1_screenshots/uat-r6-guardian-parent.png` | Fresh credentialed Guardian/Parent role-home screenshot captured from official live app. |
| TP-9 | Rider / lesson participant context | `uat.participant@equine-sync.com` | rider owner-safe context | PASS | `outputs/build_next_15f1_screenshots/uat-r7-rider.png` | Fresh credentialed Lesson Participant role-home screenshot captured from official live app. |
| TP-10 | Standalone individual owner | `uat.individual-owner@equine-sync.com` | standalone owner-safe context | PASS | `outputs/build_next_15f1_screenshots/uat-r8-individual-owner.png` | Fresh credentialed Individual Owner role-home screenshot captured from official live app. |
| TP-11 | Privacy exclusions | all role rows | verify no private fields appear in screenshots/responses | PASS | all captured screenshots | Screenshot privacy sweep across TP-1 through TP-10 found no visible staff notes, raw daily-check payload internals, alert triggers, source_check_id, audit diffs, auth tokens, passwords, Stripe IDs, DocuSign IDs, private keys, or private horse/admin-only fields. No credentialed API response payloads were captured in BN15F.1. |

## Screenshot Inventory

Sixteen fresh screenshot files were captured in this BN15F.1 run: ten role
identity/page captures plus two supporting Facility Admin dashboard parts, two
supporting Barn Owner dashboard parts, and two supporting Barn Manager
dashboard parts. No TP role screenshot remains pending.

Captured files:

- `outputs/build_next_15f1_screenshots/uat-r1-platform-admin.png`
- `outputs/build_next_15f1_screenshots/uat-r2a-facility-admin.png`
- `outputs/build_next_15f1_screenshots/uat-r2a-facility-admin-dashboard-top.png`
- `outputs/build_next_15f1_screenshots/uat-r2a-facility-admin-dashboard-pulse.png`
- `outputs/build_next_15f1_screenshots/uat-r2b-barn-owner.png`
- `outputs/build_next_15f1_screenshots/uat-r2b-barn-owner-dashboard-top.png`
- `outputs/build_next_15f1_screenshots/uat-r2b-barn-owner-dashboard-pulse.png`
- `outputs/build_next_15f1_screenshots/uat-r3-barn-manager-dashboard-top.png`
- `outputs/build_next_15f1_screenshots/uat-r3-barn-manager-dashboard-pulse.png`
- `outputs/build_next_15f1_screenshots/uat-r4a-groom.png`
- `outputs/build_next_15f1_screenshots/bn13m-t1-trainer.png`
- `outputs/build_next_15f1_screenshots/bn13m-w1-working-student.png`
- `outputs/build_next_15f1_screenshots/uat-r5-horse-owner.png`
- `outputs/build_next_15f1_screenshots/uat-r6-guardian-parent.png`
- `outputs/build_next_15f1_screenshots/uat-r7-rider.png`
- `outputs/build_next_15f1_screenshots/uat-r8-individual-owner.png`

Placeholder note:

- `outputs/build_next_15f1_screenshots/README.md`

Expected future files:

- None. Role screenshot capture is complete for this BN15F.1 pass.

## Privacy Boundary

This BN15F.1 report includes sixteen credentialed page screenshots and no
credentialed API response payloads. The TP-11 privacy sweep is screenshot-only.
It also contains no passwords, tokens,
reset links, API keys, Stripe IDs, DocuSign IDs, private keys, raw alert
payloads, audit diffs, staff notes, or private horse records.

The screenshot privacy sweep verified that captured evidence does not visibly
expose:

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

The live frontend and API are reachable. TP-1 through TP-10 have fresh
credentialed role screenshots captured from the official live app, and TP-11 is
complete as a screenshot-only privacy sweep. BN15F.1 is ready for Codex review
as a complete credentialed walkthrough evidence packet. No TP row is
founder-accepted by this report.

No TP row is founder-accepted.

Verification completed for this package:

- BN15F.1 focused guard: `8 passed`.
- Broader BN15 evidence regression: `61 passed`.

## Package

- `outputs/build_next_15f1_live_today_pulse_walkthrough.zip`
