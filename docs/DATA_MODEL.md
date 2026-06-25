# DATA_MODEL.md
# EquineSync Data Model

> Every major operational entity must include: `id`, `barn_id`, `created_at`, `updated_at`, `created_by` (per `ENGINEERING_RULES.md`). See `SCHEMA_CHANGE_POLICY.md` before changing any schema.
>
> **Current-state note:** Some entities below describe the **target** schema. The live code does not yet enforce `barn_id`/`created_by` on every entity (notably the `User` model currently lacks `barn_id`). Gaps are tracked in `KNOWN_TECH_DEBT.md` and sequenced in Phase 4.

---

## Barn
Represents a single operational organization (tenant).

| Field | Type | Notes |
|---|---|---|
| `id` | string | primary key |
| `name` | string | |
| `address` | string | |
| `timezone` | string | IANA tz |
| `subscription_plan` | string | |
| `plan_type` | enum | individual_owner / private_owner / barn / trainer / lesson_program / enterprise / nonprofit_community |
| `created_at` | ISO datetime | |

**Relationships:** has many `User`, `Horse`, `Invoice`, `Task`.

---

## User
Represents a platform user.

| Field | Type | Notes |
|---|---|---|
| `id` | string | primary key |
| `barn_id` | string | **target** (not yet enforced in code) |
| `first_name` | string | |
| `last_name` | string | |
| `email` | string | unique, lowercased |
| `role` | enum | see roles below |
| `billing_seat_type` | enum | owner_manager / staff / helper_family / client_owner_portal / lesson_participant / platform_admin / none |
| `account_origin` | enum | self_subscribed / invited_by_barn / invited_by_trainer / platform_created |
| `portal_access_status` | enum | active / invited / disabled |
| `phone` | string | |
| `status` | string | active / invited / disabled |
| `created_at` | ISO datetime | |

**Roles:** `admin`, `barn_manager`, `trainer`, `groom`, `working_student`, `horse_owner`, `rider`, `parent`, `veterinarian`, `farrier`.

> **Reconciliation note:** Live code stores `full_name` (single field) + `password_hash`; it does not yet store `first_name`/`last_name`/`barn_id`/`phone`/`status`. The role list in code matches the target.
>
> **Pricing foundation note:** `role` controls app permissions; `billing_seat_type` controls plan usage counts. These must not be collapsed into one field. Free invited owner portal accounts should use `billing_seat_type = "client_owner_portal"` and must not count as staff or owner/manager seats.

**Relationships:** has many `Task`.

---

## Horse
Represents an equine profile.

| Field | Type | Notes |
|---|---|---|
| `id` | string | |
| `barn_id` | string | |
| `name` | string | |
| `breed` | string | |
| `sex` | string | |
| `color` | string | |
| `age` | number | |
| `owner_ids` | string[] | |
| `trainer_id` | string | |
| `status` | string | active / archived |
| `billing_status` | string | active / inactive |
| `billing_status_reason` | string | short reason or null |
| `billing_status_updated_at` | ISO datetime | |
| `billing_status_updated_by` | string | user id |
| `special_instructions` | string | |

> **Pricing foundation note:** `status` is the operational lifecycle field. `billing_status` is the billing-facing active/inactive field used for plan limits and overage calculations. Existing non-archived horses should default to `billing_status = "active"` for usage purposes; archived or billing-inactive horses should not count toward active horse limits.

**Relationships:** has many `CareTask`, `MedicationSchedule`, `IncidentReport`, `Invoice`.

---

## CareTask
Tracks operational care actions.

| Field | Type | Notes |
|---|---|---|
| `id` | string | |
| `barn_id` | string | |
| `horse_id` | string | |
| `task_type` | enum | see below |
| `assigned_to` | string | user id |
| `due_date` | ISO datetime | |
| `status` | string | scheduled / completed / missed / delayed |
| `notes` | string | |
| `completed_at` | ISO datetime | |

**Task types:** `feeding`, `turnout`, `medication`, `stall_cleaning`, `rehab`, `grooming`, `exercise`, `show_prep`.

> **Reconciliation note:** Live operational timeline is implemented as `task_events` (unified event-driven engine, see `TASK_ENGINE_ARCHITECTURE` in `/app/memory`). `CareTask` here is the documented logical model; the physical collection is `task_events`.

---

## MedicationSchedule
Tracks horse medication instructions.

| Field | Type |
|---|---|
| `id` | string |
| `horse_id` | string |
| `medication_name` | string |
| `dosage` | string |
| `frequency` | string |
| `start_date` | ISO date |
| `end_date` | ISO date |
| `instructions` | string |

---

## Invoice
Tracks owner billing.

| Field | Type |
|---|---|
| `id` | string |
| `barn_id` | string |
| `owner_id` | string |
| `horse_id` | string |
| `invoice_number` | string |
| `line_items` | object[] |
| `subtotal` | number |
| `tax` | number |
| `total` | number |
| `status` | string |
| `due_date` | ISO date |

---

## AuditLog
Immutable operational history. **(Target — not yet implemented; see Phase 5.)**

| Field | Type |
|---|---|
| `id` | string |
| `barn_id` | string |
| `actor_id` | string |
| `resource_type` | string |
| `resource_id` | string |
| `action` | string |
| `old_value` | object |
| `new_value` | object |
| `timestamp` | ISO datetime |

---

## Known live collections (observed in code, for reference)
`users`, `refresh_tokens`, `auth_tokens`, `login_attempts`, `task_events`, `service_requests`, `horses`, `inventory`, `locations`, `feed_templates`, `recurring_schedules`, `staff_invites`, `onboarding_progress`, `notifications`.

## Feature Backlog Foundation Collections
Added as non-destructive MongoDB collections for the remaining backlog:
`stall_assignments`, `waitlist_entries`, `pasture_schedules`, `equipment_items`, `supply_inventory_items`, `health_reminders`, `health_documents`, `farrier_history`, `medication_administration_logs`, `injury_lameness_cases`, `weight_condition_entries`, `payment_profiles`, `recurring_billing_rules`, `expenses`, `group_messages`, `owner_media_updates`, `digital_forms`, `emergency_contacts`, `emergency_workflows`, `training_plans`, `show_entries`, `ride_gps_tracks`, `staff_shifts`, `staff_task_assignments`, `shift_handoff_reports`, `time_clock_entries`, `automation_suggestions`, `integration_connections`, `offline_sync_queue`, `document_scan_jobs`, `qr_horse_ids`.

Each record follows this wrapper:

| Field | Type | Notes |
|---|---|---|
| `id` | string | primary record id |
| `barn_id` | string | tenant key; defaults to `primary` until Phase 4 tenant enforcement is complete |
| `data` | object | module-specific fields defined by `routes/backlog.py` metadata |
| `created_at` | ISO datetime | set on create |
| `updated_at` | ISO datetime | set on create/update/archive |
| `created_by` | string | user id |
| `updated_by` | string | user id |
| `archived_at` | ISO datetime | set only on soft archive |

See `FEATURE_BACKLOG_FOUNDATIONS.md` for module coverage and placeholder boundaries.

## LoginAttempt (`login_attempts` collection — Phase 2D)
Per-account brute-force tracking. One doc per email; cleared on successful login.

| Field | Type | Notes |
|---|---|---|
| `email` | string | lowercased, unique |
| `count` | int | failures in the current window |
| `first_failed_at` | ISO datetime | window anchor |
| `last_failed_at` | ISO datetime | |
| `last_ip` | string | |
| `locked_until` | ISO datetime | set once `count >= LOGIN_MAX_ATTEMPTS`; login returns 423 until it passes |

## AuthToken (`auth_tokens` collection — Phase 2C)
One-time tokens for password reset & email verification. Tokens are **hashed at rest**, single-use, and expiring.

| Field | Type | Notes |
|---|---|---|
| `id` | string | |
| `user_id` | string | owning user |
| `purpose` | enum | `password_reset` \| `email_verify` |
| `token_hash` | string | sha256 of the raw token (raw never stored) |
| `created_at` | ISO datetime | |
| `expires_at` | ISO datetime | TTL-driven (`PASSWORD_RESET_TTL_HOURS`=1, `EMAIL_VERIFY_TTL_HOURS`=48) |
| `used` | bool | single-use flag |
| `used_at` | ISO datetime | set on consume |

> **User schema update (Phase 2C):** `User` documents now carry `email_verified: bool`. New registrations default to `false`; pre-existing users were backfilled to `true` at startup (no lockout).
