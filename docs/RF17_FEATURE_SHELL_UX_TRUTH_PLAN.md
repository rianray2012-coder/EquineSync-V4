# RF17 Feature-Shell Retirement and UX Truth Plan

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Purpose

RF17 reduces launch trust risk by ensuring visible EquineSync surfaces are real
workflow, truthful readiness/admin setup, or hidden/redirected. It does not
attempt broad feature completion.

## Founder-Approved Defaults

The founder approved proceeding with the tighter RF17 posture:

| Decision | RF17 Action |
| --- | --- |
| Daily role navigation shows only real supported workflows. | Remove duplicate/readiness/scaffold links from daily role nav. |
| Inventory is canonical over Supply Inventory. | Redirect `/supply-inventory` to `/inventory`. |
| Task Engine is canonical over Staff Tasks. | Redirect `/staff-tasks` to `/today`. |
| Canonical Owner Updates / Review Queue win over feature-module owner media updates. | Redirect `/owner-updates` to `/review-queue`. |
| Group Messaging is local-log/readiness only. | Redirect `/group-messaging` to `/messaging`; keep local-log wording as evidence. |
| Advanced Reports is manifest/readiness only. | Redirect `/advanced-reports` to `/reports`; keep manifest wording as evidence. |
| Store submission, native billing, provider sync, full offline, and destructive migration remain out of RF17. | Record explicit deferrals. |

## Verification Plan

- Focused RF17 tests prove route redirects, nav absence, truth labels, and
  report/package generation.
- Frontend build proves route/nav edits compile.
- Report generation with blocker failure enabled proves the RF17 package is
  reviewable.
- Zip integrity, manifest parity, stale-claim scan, and secret-shape scan close
  the evidence package.

## Stop Condition

Stop after RF17 package generation and review. Do not start RF18 until RF17 is
reviewed and locked.
