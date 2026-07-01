# Build-Next-13L Role Smoke Execution Checklist

Status: CODEX-APPROVED & LOCKED

Prepared: 2026-07-01

## Scope

This checklist is the operator packet for BN13M. It defines what to verify for
each credentialed role session. It does not contain credentials and does not
record founder acceptance.

Codex review found no blocking findings. This checklist is locked as prep-only
execution guidance; it does not prove that credentialed role smoke has run.

## Official Environment Gate

Before executing BN13M, confirm:

- Frontend URL: `https://app.equine-sync.com` or founder-approved equivalent.
- API target: the production-like Render API connected to that frontend.
- Database label: founder-approved staging/production-like database label.
- Build marker: commit SHA recorded before screenshots begin.
- Screenshots are sanitized and contain no passwords, tokens, API keys, Stripe
  IDs, DocuSign IDs, private notes, or unrelated client data.

If any item is missing, mark every row `BLOCKED - environment not confirmed`.

## Result Status Values

- `PASS`: row was executed in the official environment and evidence matched.
- `BLOCKED`: row could not be completed because of missing credentials,
  environment uncertainty, wrong role marker, missing screenshot, or access
  failure.
- `FAIL`: row executed but actual behavior did not match the expected route,
  shell, sidebar, or forbidden-link boundary.

## Screenshot Naming

Use these filenames in BN13M:

- `outputs/build_next_13m_role_smoke_screenshots/uat-r1-platform-admin.jpg`
- `outputs/build_next_13m_role_smoke_screenshots/uat-r2a-facility-admin.jpg`
- `outputs/build_next_13m_role_smoke_screenshots/uat-r2b-barn-owner.jpg`
- `outputs/build_next_13m_role_smoke_screenshots/bn13m-t1-trainer.jpg`
- `outputs/build_next_13m_role_smoke_screenshots/uat-r3-barn-manager.jpg`
- `outputs/build_next_13m_role_smoke_screenshots/uat-r4a-groom.jpg`
- `outputs/build_next_13m_role_smoke_screenshots/bn13m-w1-working-student.jpg`
- `outputs/build_next_13m_role_smoke_screenshots/uat-r5-horse-owner.jpg`
- `outputs/build_next_13m_role_smoke_screenshots/uat-r6-guardian.jpg`
- `outputs/build_next_13m_role_smoke_screenshots/uat-r7-rider.jpg`
- `outputs/build_next_13m_role_smoke_screenshots/uat-r8-individual-owner.jpg`

## Role Rows

| Row | Role | Candidate account | Expected first landing | Expected surface | Sidebar/menu expectation | Forbidden checks | BN13M screenshot |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UAT-R1 | `platform_admin` | `uat.platform@equine-sync.com` | `/admin/portal/dashboard` | Platform Admin Portal dashboard | Admin Portal navigation visible; platform admin identity visible | No facility-only setup redirect; no client role-home shell | `uat-r1-platform-admin.jpg` |
| UAT-R2a | `admin` | `uat.facility-admin@equine-sync.com` | `/onboarding` when setup incomplete, else `/dashboard` | Facility admin shell | Facility admin tools visible: dashboard, setup, horses, owners, staff, schedule, tasks | No Admin Portal unless a platform role is also present | `uat-r2a-facility-admin.jpg` |
| UAT-R2b | `barn_owner` | dedicated barn-owner account or confirmed UAT-R2 marker | `/role-home/barn-owner` | Barn owner intake shell | Barn owner navigation visible; setup/profile affordance visible | No staff admin, platform admin, advanced reports, checkout, or document-signature direct workflow | `uat-r2b-barn-owner.jpg` |
| BN13M-T1 | `trainer` | dedicated trainer account | `/role-home/trainer` | Trainer intake shell | Trainer navigation visible; training/program tools scoped to trainer | No platform admin, facility setup mutation, billing admin, or staff payroll surface | `bn13m-t1-trainer.jpg` |
| UAT-R3 | `barn_manager` | `uat.manager@equine-sync.com` | `/role-home/manager` | Manager intake shell | Manager navigation visible; operations/task context visible | No platform admin, billing admin, checkout, or founder-only setup route | `uat-r3-barn-manager.jpg` |
| UAT-R4a | `groom` | `uat.staff@equine-sync.com` if role marker is `groom` | `/role-home/staff` | Staff intake shell | Staff daily-work navigation visible | No billing, reports, staff management, platform admin, or facility setup route | `uat-r4a-groom.jpg` |
| BN13M-W1 | `working_student` | dedicated working-student account | `/role-home/staff` | Staff intake shell | Staff daily-work navigation visible | No billing, reports, staff management, platform admin, or facility setup route | `bn13m-w1-working-student.jpg` |
| UAT-R5 | `horse_owner` | `uat.owner@equine-sync.com` | `/owner/horses/{horseId}` when linked, else `/role-home/owner` | Owner-safe horse page or owner shell | Owner navigation visible; owner-safe care/request entries only | No staff notes, admin routes, alert internals, audit diffs, raw daily-check payloads, billing admin, or reports | `uat-r5-horse-owner.jpg` |
| UAT-R6 | `parent` | `uat.guardian@equine-sync.com` | `/role-home/guardian` | Guardian intake shell | Guardian navigation visible; rider overview context visible | No staff management, platform admin, facility setup, billing admin, or private HorseOps internals | `uat-r6-guardian.jpg` |
| UAT-R7 | `rider` | `uat.participant@equine-sync.com` if role marker is `rider` | `/role-home/rider` | Rider intake shell | Rider navigation visible; lessons/progress context visible | No billing admin, staff management, facility setup, platform admin, or private HorseOps internals | `uat-r7-rider.jpg` |
| UAT-R8 | `horse_owner` standalone | `uat.individual-owner@equine-sync.com` | `/role-home/owner` unless linked to a horse | Individual owner shell | Individual owner navigation visible | No facility staff tools, platform admin, reports, staff notes, alert internals, or audit diffs | `uat-r8-individual-owner.jpg` |

## Per-Row Steps

For each row:

1. Start a clean browser session or sign out fully.
2. Sign in with the row's role account.
3. Record the final landing URL after redirects settle.
4. Confirm the expected surface is visible.
5. Confirm the sidebar/menu expectation.
6. Confirm forbidden links are absent.
7. Capture the screenshot named above.
8. Fill the result template with `PASS`, `BLOCKED`, or `FAIL`.
9. Sign out before the next row.

## Stop Conditions

Stop BN13M and record a blocker if:

- The environment label or build marker is unclear.
- A credential is missing or fails.
- A row resolves to an unexpected role marker.
- A screenshot would expose private data.
- Any client role sees platform admin, staff management, private HorseOps
  internals, raw alert triggers, raw daily-check payloads, audit diffs, or
  secrets.

## Deferred

- Founder acceptance.
- Public launch approval.
- Any product behavior fix found during smoke. A behavior mismatch should open a
  new phase instead of being fixed inside BN13M evidence capture.
