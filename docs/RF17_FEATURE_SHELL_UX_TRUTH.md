# RF17 Feature-Shell Retirement and UX Truth

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Purpose

RF17 applies the founder-approved truth-first cleanup posture to visible
feature shells. Daily navigation and direct routes now prefer canonical
workflows where EquineSync already has a stronger source of truth.

## Implemented In RF17

| Former Surface | RF17 Status | Canonical Surface |
| --- | --- | --- |
| Supply Inventory | redirected | `/inventory` |
| Staff Tasks | redirected | `/today` |
| Owner media updates | redirected | `/review-queue` |
| Group Messaging | redirected | `/messaging` |
| Advanced Reports | redirected | `/reports` |

Daily Manager and Trainer navigation now uses `/review-queue` for Owner
Requests. Trainer Reports now uses `/reports`.

## Truth-Labeled Readiness Surfaces

| Surface | RF17 Posture |
| --- | --- |
| Group Messaging | Local-log/readiness only; no external delivery claim. |
| Advanced Reports | Export manifest/readiness only; no native Excel/PDF claim. |
| Mobile Readiness | Limited field-recovery/readiness language only. |
| Integrations | Provider-readiness evidence only; no live provider sync claim. |
| Forms & Signatures | Local acknowledgement/provider-readiness; no live legal signing claim. |

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Daily role navigation shows only real supported workflows. | accepted by founder review | Readiness, scaffold, placeholder, and proof surfaces may be hidden, redirected, or truth-labeled. |
| Inventory is canonical over Supply Inventory. | accepted by founder review | RF17 redirects only; it does not delete feature-module records. |
| Task Engine is canonical over Staff Tasks. | accepted by founder review | RF17 redirects only; it does not migrate `staff_task_assignments`. |
| Canonical Owner Updates are canonical over feature-module owner media updates. | accepted by founder review | RF17 redirects to Review Queue; media migration remains non-destructive future work. |
| Group Messaging remains local-log/readiness only until true delivery evidence exists. | accepted by founder review | RF17 redirects to operational Messaging and keeps local-log labels. |
| Advanced Reports remains manifest/readiness until real Excel/PDF export exists. | accepted by founder review | RF17 redirects to Reports and keeps manifest labels. |
| Store submission, native billing, provider sync, full offline support, and destructive migration. | deferred | These require later external/store/provider/legal or migration phases. |

## Deferred Boundaries

RF17 does not:

- delete feature-module data;
- perform data migrations;
- call providers;
- submit to App Store Connect or Google Play Console;
- implement native billing or Apple/Google in-app purchase compliance;
- implement true provider delivery/sync;
- implement full offline/native background support;
- mutate UAT accounts;
- broaden RF15/RF16 claims.

## Verification

RF17 is verified by:

- `backend/tests/test_rf17_feature_shell_ux_truth.py`;
- `backend/scripts/build_rf17_feature_shell_ux_truth.py`;
- frontend production build if route/nav files change;
- package integrity and manifest parity for
  `outputs/build_next_rf17_feature_shell_ux_truth.zip`;
- secret-shape and stale-overclaim scans over the RF17 package.
