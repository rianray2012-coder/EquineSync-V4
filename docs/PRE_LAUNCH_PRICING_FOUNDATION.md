# Pre-Launch Pricing Foundation

Updated: 2026-06-19

This is the build direction for the pricing foundation that must exist before launch hardening. It turns the pricing addendum into concrete product and data contracts without requiring full overage billing automation yet.

## Goal

Prevent billing, permissions, HorseOps, and owner portal access from becoming tangled by separating four concepts early:

1. Horse operational status.
2. Billing-active horse count.
3. User permission role.
4. Billable seat type.

## Required Foundation Items

### 1. Active / Inactive Horse Status

Add an explicit billing-facing horse status instead of relying only on the existing operational horse status.

Required horse fields:

| Field | Values | Purpose |
| --- | --- | --- |
| `billing_status` | `active`, `inactive` | Determines whether the horse counts toward plan limits and overages. |
| `billing_status_reason` | short string or null | Human-readable reason for inactive/excluded status. |
| `billing_status_updated_at` | ISO datetime | Audit-friendly timestamp for the last billing-status change. |
| `billing_status_updated_by` | user id | Actor who changed the billing status. |

Rules:

- Existing non-archived horses should default to `billing_status = "active"`.
- Archived horses should not count as active horses unless a future approved rule explicitly says otherwise.
- Changing `billing_status` must be manager/admin-only.
- Changing `billing_status` must emit a safe audit event with field names only, not private horse notes.
- Owner portal users should never control or see billing-status internals.

### 2. Usage Counters

Create one canonical usage calculation that all billing UI, admin portal, and soft-warn surfaces use.

Required counters:

| Counter | Counts |
| --- | --- |
| `active_horses` | Horses in the organization with `billing_status = "active"` and not archived. |
| `staff_seats` | Active users whose billing seat type is staff. |
| `owner_manager_seats` | Active users whose billing seat type is owner/manager. |
| `helper_family_seats` | Active users whose billing seat type is helper/family. |
| `client_owner_portal_accounts` | Free invited horse-owner portal accounts attached to subscribed barn/trainer organizations. |
| `lesson_participants` | Active lesson participants when lesson-program modules are enabled. |

Rules:

- The usage endpoint must remain soft-warn only until a separate hard-enforcement phase is approved.
- Usage counts must be barn/facility scoped.
- Usage counts must not mutate database state.
- Usage results should include both `used` and `limit` for each relevant counter.
- Admin portal should show count source and last refresh time where possible.

### 3. Free Invited Owner Portal Rules

Client owner portal accounts must remain free when invited by a subscribed barn, trainer, or facility.

Required user/account fields:

| Field | Values | Purpose |
| --- | --- | --- |
| `account_origin` | `self_subscribed`, `invited_by_barn`, `invited_by_trainer`, `platform_created` | Separates independent paid owners from free invited owner portal users. |
| `billing_seat_type` | `owner_manager`, `staff`, `helper_family`, `client_owner_portal`, `lesson_participant`, `platform_admin`, `none` | Determines billing count bucket. |
| `portal_access_status` | `active`, `invited`, `disabled` | Controls owner portal access without implying paid subscription. |

Rules:

- A horse owner invited by a subscribed barn should use `billing_seat_type = "client_owner_portal"`.
- `client_owner_portal` accounts do not count as staff seats.
- `client_owner_portal` accounts do not count as owner/manager seats.
- Invited owner portal users can view only approved horses, invoices, updates, photos, documents, and requests.
- Invited owner portal users should not see upgrade prompts that imply they must pay to view a horse through a subscribed barn.
- A horse owner who independently signs up outside a barn should use a paid owner plan path, not the free invited portal path.

### 4. Role-Based Seat Tracking

Do not use `role` alone as the billing source of truth. Permission role and billing seat type must be separate fields.

Examples:

| Permission Role | Possible Billing Seat Type |
| --- | --- |
| `admin` | `owner_manager`, `platform_admin` |
| `barn_manager` | `owner_manager` |
| `trainer` | `staff` or `owner_manager` depending on organization setup |
| `groom` | `staff` |
| `working_student` | `staff` or `helper_family` |
| `horse_owner` | `client_owner_portal` or paid owner-plan account |
| `parent` | `client_owner_portal` or lesson participant guardian |

Rules:

- Permissions come from role/capability.
- Billing counts come from `billing_seat_type`.
- Status comes from account status fields.
- The admin portal must allow authorized admins to inspect the mapping, but changes should be audited.
- Seat changes must not silently elevate app permissions.
- Permission changes must not silently change billable seat type unless the UI explicitly says so.

## API And UI Requirements

### Backend

- Add a canonical helper/service for usage calculation.
- Update `/api/billing/usage` to use the canonical helper.
- Add tests for active/inactive horses and every billable seat bucket.
- Add tests proving free invited owner portal accounts do not count as paid seats.
- Add tests proving usage calculation is read-only.

### Admin Portal

- Add a usage summary with active horses, inactive horses, staff seats, owner/manager seats, helper seats, free owner portal accounts, and lesson participants.
- Add a horse billing-status control for authorized admin/manager users.
- Add a seat-type inspector for users.
- Add audit trail references for billing-sensitive changes.

### HorseOps

- Show active/inactive horse state to staff/admin in horse management surfaces.
- Keep owner-facing horse screens free of billing-status internals.
- Make adding/reactivating a horse trigger soft-warn usage messaging when applicable.

### Mobile

- Limit messages must fit small screens and be understandable in the barn aisle.
- Adding a horse, inviting staff, inviting an owner, or changing active status must show soft-warn messages without blocking daily care work.
- Staff daily-care execution must not be interrupted by subscription/upgrade flows.

## Explicit Non-Goals

- No hard 402-style enforcement.
- No automatic overage charging.
- No native mobile app work.
- No broad Stripe catalog rewrite beyond what is required to support the updated plan metadata.
- No owner-visible billing-status controls.
- No permission elevation through billing seat changes.

## Acceptance Criteria

- There is one canonical usage calculation.
- Active horse counts exclude inactive/archived horses.
- Staff seats, owner/manager seats, helper/family seats, owner portal accounts, and lesson participants are counted separately.
- Free invited owner portal accounts do not count as staff or owner/manager seats.
- Role and billing seat type are stored and reasoned about separately.
- Admin-facing usage visibility exists before launch hardening.
- Soft-warn behavior remains the only plan-limit behavior until a later approved enforcement phase.
