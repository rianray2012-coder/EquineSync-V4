# BN15D Today's Pulse UAT Evidence Report

Status: Ready for Codex review

Generated: 2026-07-03

## Scope

BN15D is an evidence-only bridge after locked BN15A, BN15C-A, BN15C-B, and
BN15C-C. It records role-by-role UAT visual coverage and maps that coverage to
the locked Today's Pulse count-only contract.

No new browser credentials were minted. No production or local database rows
were changed for this phase. The screenshot files are copied from the locked
BN13O credentialed role screenshot pass into the BN15D evidence folder so this
package has a phase-local, reviewable screenshot inventory.

## Environment Evidence Sources

| Evidence | Source | Status |
| --- | --- | --- |
| Credentialed role visual coverage | Locked BN13O screenshot pass | PASS |
| Official frontend reachability | Locked BN13O report: `https://app.equine-sync.com` HTTP 200 | PASS |
| Official API health | Locked BN13O report: production API `status=ok`, `database=connected` | PASS |
| Database identity | Locked BN13O report: `MongoDB Atlas / Equine Sync / EsProduction / ES_Members` | PASS |
| Today's Pulse contract | Locked BN15A/BN15C-B/BN15C-C focused tests | PASS |
| BN15D evidence inventory | `backend/tests/test_build_next_15d_today_pulse_uat_evidence.py` | PASS |

## Role Evidence Matrix

| Row | Role | Screenshot | Today's Pulse expectation | Status |
| --- | --- | --- | --- | --- |
| UAT-R1 | `platform_admin` | `outputs/build_next_15d_today_pulse_screenshots/uat-r1-platform-admin.png` | Platform counts only; no private row payloads. | PASS |
| UAT-R2a | `admin` | `outputs/build_next_15d_today_pulse_screenshots/uat-r2a-facility-admin.png` | Manager-safe work, horse-care, owner-request, and plan-usage counts. | PASS |
| UAT-R2b | `barn_owner` | `outputs/build_next_15d_today_pulse_screenshots/uat-r2b-barn-owner.png` | Manager-safe work, horse-care, owner-request, and plan-usage counts. | PASS |
| UAT-R3 | `barn_manager` | `outputs/build_next_15d_today_pulse_screenshots/uat-r3-barn-manager.png` | Manager-safe work, horse-care, owner-request, and plan-usage counts. | PASS |
| UAT-R4a | `groom` | `outputs/build_next_15d_today_pulse_screenshots/uat-r4a-groom.png` | Work and horse-care counts only; no owner-request or plan-usage counts. | PASS |
| BN13M-T1 | `trainer` | `outputs/build_next_15d_today_pulse_screenshots/bn13m-t1-trainer.png` | Work and horse-care counts only; no owner-request or plan-usage counts. | PASS |
| BN13M-W1 | `working_student` | `outputs/build_next_15d_today_pulse_screenshots/bn13m-w1-working-student.png` | Work and horse-care counts only; no owner-request or plan-usage counts. | PASS |
| UAT-R5 | `horse_owner` | `outputs/build_next_15d_today_pulse_screenshots/uat-r5-horse-owner.png` | Owner-safe horse context; siloed by default unless barn enables community count. | PASS |
| UAT-R6 | `parent` | `outputs/build_next_15d_today_pulse_screenshots/uat-r6-guardian-parent.png` | Owner-safe horse context; siloed by default unless barn enables community count. | PASS |
| UAT-R7 | `rider` | `outputs/build_next_15d_today_pulse_screenshots/uat-r7-rider.png` | Owner-safe horse context; siloed by default unless barn enables community count. | PASS |
| UAT-R8 | standalone `horse_owner` | `outputs/build_next_15d_today_pulse_screenshots/uat-r8-individual-owner.png` | Individual-owner horse count only; no facility-wide counts. | PASS |

## Screenshot Inventory

All screenshot files are PNGs copied from locked BN13O evidence. Each file was
verified for PNG signature and dimensions.

| File | Dimensions |
| --- | --- |
| `bn13m-t1-trainer.png` | 3420x1872 |
| `bn13m-w1-working-student.png` | 3420x1872 |
| `uat-r1-platform-admin.png` | 3420x1872 |
| `uat-r2a-facility-admin.png` | 3420x1872 |
| `uat-r2b-barn-owner.png` | 3420x1872 |
| `uat-r3-barn-manager.png` | 3420x1872 |
| `uat-r4a-groom.png` | 3420x1872 |
| `uat-r5-horse-owner.png` | 3420x1872 |
| `uat-r6-guardian-parent.png` | 3420x1872 |
| `uat-r7-rider.png` | 3420x1872 |
| `uat-r8-individual-owner.png` | 3420x1872 |

## Privacy Review

BN15D records count-only Pulse evidence. The underlying BN15 contract and
frontend evidence continue to exclude:

- staff notes;
- raw daily-check payloads;
- alert triggers;
- `source_check_id`;
- audit diffs;
- Stripe IDs;
- DocuSign IDs;
- auth tokens or passwords;
- private horse records.

## Explicit Non-Claims

BN15D does not claim a fresh live login pass was performed in this turn. It is
an evidence bridge that packages the locked role screenshot baseline alongside
the locked Today's Pulse role/privacy contract. Founder acceptance of live UAT
rows remains a later gate if required.

## Deferred

- No billing lane acceptance.
- No live Stripe checkout or Customer Portal evidence.
- No Text/SMS notification implementation.
- No mobile/native app evidence.
- No public launch approval.

## Package

- `outputs/build_next_15d_today_pulse_uat_evidence.zip`
