# Build-Next-13J Role First-Login Matrix

Status: READY FOR CODEX REVIEW

BN13J is evidence-only. It does not approve public launch, does not replace
official staging UAT, and does not change product behavior. localhost is not official staging evidence.

## First-Login Destinations

| User type | Role marker | Locked first-login destination | Evidence source |
| --- | --- | --- | --- |
| Platform admin | `platform_admin` / any platform role | `/admin/portal/dashboard` | `isPlatformAdmin(user)` in `roleLanding.js` |
| Facility admin, setup incomplete | `admin`, `onboarding_completed=false` or `facility_setup_complete=false` | `/onboarding` | `resolvePostLoginPath` admin branch |
| Facility admin, setup complete | `admin` | `/dashboard` | `ROLE_HOME_PATHS.facilityAdmin` |
| Barn owner | `barn_owner` | `/role-home/barn-owner` | BN13F barn owner intake shell |
| Trainer | `trainer` | `/role-home/trainer` | BN13G trainer intake shell |
| Barn manager | `barn_manager` | `/role-home/manager` | BN13H manager intake shell |
| Groom | `groom` | `/role-home/staff` | BN13I staff intake shell |
| Working student | `working_student` | `/role-home/staff` | BN13I staff intake shell |
| Horse owner, linked horse | `horse_owner` plus primary/linked horse marker | `/owner/horses/{horse_id}` | `ownerHorsePath(user)` |
| Horse owner, no linked horse | `horse_owner` | `/role-home/owner` | BN13E owner intake shell |
| Guardian / parent | `parent` | `/role-home/guardian` | BN13D guardian intake shell |
| Rider | `rider` | `/role-home/rider` | BN13C rider intake shell |

## Intake Surfaces

| Surface | Endpoint | Allowed role(s) | Product facility gate |
| --- | --- | --- | --- |
| Rider intake | `GET/PATCH /api/rider/profile` | `rider` | Not attached |
| Guardian intake | `GET/PATCH /api/guardian/minor-rider-profile` | `parent` | Not attached |
| Owner intake | `GET/PATCH /api/owner-intake/profile` | `horse_owner` | Not attached |
| Barn owner intake | `GET/PATCH /api/barn-owner-intake/profile` | `barn_owner` | Not attached |
| Trainer intake | `GET/PATCH /api/trainer-intake/profile` | `trainer` | Not attached |
| Manager intake | `GET/PATCH /api/manager-intake/profile` | `barn_manager` | Not attached |
| Staff intake | `GET/PATCH /api/staff-intake/profile` | `groom`, `working_student` | Not attached |

## Navigation Evidence

BN13 keeps client-role navigation narrow:

- Platform admins stay in Admin Portal navigation.
- Facility admins keep setup/business tools.
- Barn owner navigation avoids staff, billing, reports, Admin Portal, and
  facility-settings surfaces.
- Staff navigation avoids billing, setup, staff management, facility settings,
  Admin Portal, audit logs, and integrations.
- Owner, guardian, and rider navigation use role-home placeholders for
  unfinished tools instead of direct private workflow links.

## Deferred

- This is not official staging UAT.
- This is not public launch approval.
- Screenshots are deferred unless a stable staging environment is explicitly
  selected for official evidence.
- BN13J does not create or mutate tasks, horses, staff permissions, HorseOps
  records, subscriptions, billing records, Stripe objects, DocuSign envelopes,
  facility setup state, or Admin Portal data.
