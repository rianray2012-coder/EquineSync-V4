# EquineSync Feature Backlog Foundations

## What changed
This pass adds an additive foundation for the remaining EquineSync backlog without changing existing Emergent-built workflows.

New backend files:
- `backend/core/permissions.py`
- `backend/routes/backlog.py`
- `backend/tests/test_backlog_foundations.py`

New frontend files:
- `frontend/src/pages/FeatureWorkspace.jsx`
- `frontend/src/lib/permissions.js`
- `frontend/src/pages/Forbidden.jsx`
- `frontend/src/pages/AuditLog.jsx`
- `frontend/src/pages/BarnLocations.jsx`
- `frontend/src/pages/ArenaSchedule.jsx`
- `frontend/src/pages/StallMap.jsx`
- `frontend/src/pages/Waitlist.jsx`
- `frontend/src/pages/PastureSchedule.jsx`
- `frontend/src/pages/Equipment.jsx`
- `frontend/src/pages/SupplyInventory.jsx`
- `frontend/src/pages/HealthReminders.jsx`
- `frontend/src/pages/HealthDocuments.jsx`
- `frontend/src/pages/HealthCareLogs.jsx`
- `frontend/src/pages/WeightTrends.jsx`
- `frontend/src/pages/Payments.jsx`
- `frontend/src/pages/RecurringBilling.jsx`
- `frontend/src/pages/Expenses.jsx`
- `frontend/src/pages/FinancialDashboard.jsx`
- `frontend/src/pages/GroupMessaging.jsx`
- `frontend/src/pages/OwnerUpdates.jsx`
- `frontend/src/pages/FormsSignatures.jsx`
- `frontend/src/pages/EmergencyContacts.jsx`
- `frontend/src/pages/EmergencyWorkflows.jsx`
- `frontend/src/pages/TrainingPlans.jsx`
- `frontend/src/pages/Competitions.jsx`
- `frontend/src/pages/RideGps.jsx`
- `frontend/src/pages/PerformanceAnalytics.jsx`
- `frontend/src/pages/StaffScheduling.jsx`
- `frontend/src/pages/MyWork.jsx`
- `frontend/src/pages/StaffTasks.jsx`
- `frontend/src/pages/HandoffReports.jsx`
- `frontend/src/pages/TimeClock.jsx`
- `frontend/src/pages/AiAutomation.jsx`
- `frontend/src/pages/Integrations.jsx`
- `frontend/src/pages/MobileReadiness.jsx`
- `frontend/src/pages/AdvancedReports.jsx`

Updated existing files:
- `backend/server.py`
- `frontend/src/App.js`
- `frontend/src/components/Sidebar.jsx`

## Backend schema and collections
The new router creates audit-friendly MongoDB document records for these collections:

`stall_assignments`, `waitlist_entries`, `pasture_schedules`, `equipment_items`, `supply_inventory_items`, `health_reminders`, `health_documents`, `farrier_history`, `medication_administration_logs`, `injury_lameness_cases`, `weight_condition_entries`, `payment_profiles`, `recurring_billing_rules`, `expenses`, `group_messages`, `owner_media_updates`, `digital_forms`, `emergency_contacts`, `emergency_workflows`, `training_plans`, `show_entries`, `ride_gps_tracks`, `staff_shifts`, `staff_task_assignments`, `shift_handoff_reports`, `time_clock_entries`, `automation_suggestions`, `integration_connections`, `offline_sync_queue`, `document_scan_jobs`, `qr_horse_ids`.

Support collection:

`backlog_audit_events`, `barn_location_share_settings`.

Each new record has:
- `id`
- `barn_id`
- `data`
- `created_at`
- `updated_at`
- `created_by`
- `updated_by`

Startup creates non-destructive indexes on `barn_id + created_at` and `barn_id + updated_at`.

## New API surface
- `GET /api/feature-modules`
- `GET /api/feature-modules/{module_key}`
- `POST /api/feature-modules/{module_key}/records`
- `PATCH /api/feature-modules/{module_key}/records/{record_id}`
- `DELETE /api/feature-modules/{module_key}/records/{record_id}` soft-archives records
- `GET /api/barn-location-share`
- `POST /api/barn-location-share`
- `GET /api/integrations/placeholders`
- `POST /api/integrations/{provider}/prepare`
- `POST /api/integrations/google-calendar/export`
- `POST /api/integrations/quickbooks/export`
- `POST /api/integrations/push-notifications/preview`
- `GET /api/integrations/qr-horse-id/{record_id}/stall-card`
- `POST /api/integrations/document-scans/prepare-upload`
- `POST /api/automation/generate-drafts`
- `GET /api/owner-portal/media-updates`
- `GET /api/owner-portal/announcements`
- `GET /api/owner-portal/forms`
- `POST /api/owner-portal/forms/{record_id}/sign`
- `GET /api/owner-portal/health-documents`
- `GET /api/owner-portal/health-summary`
- `GET /api/owner-portal/emergency`
- `GET /api/owner-portal/training-performance`
- `GET /api/owner-portal/billing`
- `POST /api/owner-portal/billing/{invoice_id}/prepare-payment`
- `GET /api/staff-portal/my-work`
- `PATCH /api/staff-portal/tasks/{record_id}/status`
- `POST /api/staff-portal/time-clock/clock-in`
- `POST /api/staff-portal/time-clock/{record_id}/clock-out`
- `POST /api/staff-portal/payroll-export`
- `GET /api/audit/backlog`
- `GET /api/reports/backlog-dashboard`
- `POST /api/reports/custom-builder`
- `POST /api/reports/export`

## Fully functional in this pass
- Role-filtered feature module catalog.
- Record creation with required-field validation.
- Record listing by module.
- Record updates.
- Soft archive.
- Audit timestamps and creator/updater fields.
- Admin audit log for backlog create/update/archive, barn location sharing, signature, staff task, time-clock, payroll export, integration prepare, Google Calendar export, QuickBooks export, push notification preview, QR stall-card generation, document scan upload preparation, payment prepare, and report export actions.
- Sidebar and route access to new module shells.
- Loading, empty, error, and validation states in the reusable workspace.
- Drag-and-drop stall map with grid positions, mobile move controls, occupancy stats, add form, soft archive, optimistic move updates, and API-backed position persistence.
- Barn owner-managed shared location board with publish/pause controls, share link, read-only stall list, pasture map, and horse location list visible to staff, trainers, and owners when enabled.
- Waitlist management with pipeline columns, priority sorting, status advancement, add form, and soft archive.
- Pasture schedule management with turnout blocks, weather holds, active/done status changes, add form, and soft archive.
- Arena schedule sharing with owner-visible availability/reservations, publish/pause controls, share link, and approved request booking.
- Equipment and tack tracking with search, category filters, condition dashboards, assignment/location fields, condition updates, add form, and soft archive.
- Supply inventory tracking for feed, hay, bedding, supplements, reorder thresholds, vendors, stock status, add form, and soft archive.
- Health reminders with overdue/due/scheduled/complete grouping, due-date awareness, completion/reopen actions, add form, and soft archive.
- Health document tracking with search, type filters, expiration status, sharing metadata, document URL links, add form, and soft archive.
- Owner portal shared health document feed scoped by owner horse ownership or explicit recipient sharing.
- Owner portal health snapshot with owner-scoped vaccination/Coggins reminders and weight/body-condition history.
- Health care logs for farrier scheduling/history, medication administration, and injury/lameness cases with status actions, add forms, and soft archive.
- Weight and body-condition trend tracking with per-horse filters, lightweight inline trend charts, measurement history, add form, and soft archive.
- Payments and auto-pay tracking with Stripe-ready readiness metadata, provider refs, enrollment status actions, add form, and soft archive.
- Recurring billing rules with active/paused/draft status, next-run tracking, estimated monthly recurring revenue, add form, and soft archive.
- Expense tracking with category filters, search, receipt links, QuickBooks-ready readiness metadata, audited CSV export manifests, total spend summary, add form, and soft archive.
- Financial dashboard with invoice revenue, overdue totals, auto-pay readiness, recurring revenue, recent expenses, and profit/loss signal summaries.
- Owner portal billing feed with owner-scoped invoices, payment profiles, recurring rules, and a non-charging Stripe-ready payment preparation flow.
- Group messaging with audience/channel/status tracking, push-ready readiness metadata, queue/sent workflow, preview-only push payload manifests, add form, and soft archive.
- Owner portal announcements feed with sent owner-audience messages and push-ready channel metadata.
- Owner photo/video updates with media URL previews, visibility controls, captions, add form, and soft archive.
- Owner portal media feed with scoped owner-visible photo/video updates and periodic refresh while the portal is open.
- Digital forms and signatures with provider readiness metadata, draft/sent/signed/expired workflow, add form, and soft archive.
- Owner portal forms feed with recipient-scoped sent/signed/expired forms and an internal signature action for sent forms.
- Emergency contacts with priority ordering, horse association, tap-to-call links, search, add form, and soft archive.
- Emergency workflows with owner authorization, vet status, contact lookup, resolution actions, add form, and soft archive.
- Owner portal emergency readiness feed with scoped contacts, tap-to-call details, and active workflow statuses.
- Owner portal arena-use requests with 30 minute, 1 hour, half-day, and full-day rental options. Approved requests create reserved arena schedule blocks.
- Training plans and goals with trainer assignment, target dates, status filters, status actions, add form, and soft archive.
- Competition and show-entry tracking with show calendar grouping, entry status workflow, result capture, add form, and soft archive.
- GPS ride tracking with ride distance/duration metrics, external track links, wearable readiness metadata, add form, and soft archive.
- Owner portal training/performance feed with owner-scoped goals, show entries, GPS ride summaries, and existing ride logs.
- Performance analytics with trainer workload, average ride ratings, active/achieved goals, show inputs, GPS mileage, and horse progress summaries.
- Staff scheduling with shift timing, area coverage, shift notes, state summaries, add form, and soft archive.
- Staff task assignment with open/in-progress/blocked/complete lanes, handoff notes, completion actions, add form, and soft archive.
- Shift handoff reports with open-task context, recent shift notes, draft/submitted/reviewed workflow, add form, and soft archive.
- Time clock tracking with open entry state, clock-out action, payroll-hour totals, audited CSV payroll export manifests, add form, and soft archive.
- Staff My Work portal with role-scoped shifts, assigned tasks, handoffs, task status updates, and clock-in/clock-out controls for staff roles.
- AI automation review queue with draft/reviewed/approved/dismissed workflow plus deterministic draft generation for care summaries, health-risk prompts, scheduling reminders, owner updates, and billing recommendations.
- Integration readiness dashboard for Stripe, QuickBooks, Google Calendar, push notifications, wearables, document scanning, and QR horse identification, with provider prepare actions, connection records, Google Calendar ICS export manifests, QuickBooks CSV export manifests, and push notification preview manifests.
- Mobile readiness workspace with local offline action staging, API-backed offline queue records, document scan intake workflow with storage upload intents, QR horse ID/stall-card tracking, and downloadable printable stall-card SVGs.
- Advanced reporting dashboard with occupancy, revenue, profit/loss, health-due metrics, custom report builder, and audited Excel/PDF export manifests.
- Launch-safe starter reset available at `/api/seed`.
- Backend regression tests for catalog, validation, audit fields, RBAC, reporting, and integration readiness.

## Integration-Ready Providers
These are intentionally not live third-party integrations yet:
- Stripe checkout/autopay/webhooks.
- Live QuickBooks expense and invoice sync; CSV-compatible export manifests are implemented for review/import.
- Live Google Calendar OAuth sync; manual ICS export is implemented for competitions, staff shifts, and health reminders.
- Live push notification delivery; preview-only APNs/FCM payload manifests are implemented for group messages and owner media updates.
- Wearables.
- Native GPS capture.
- True QR-code image encoding/native scanning; printable stall-card SVG generation is implemented from QR horse ID records.
- OCR/image cleanup for document scans; storage-backed upload intents and scan record creation are implemented.
- External signature providers; internal acknowledgement/signing is implemented for owner portal forms.
- Native Excel/PDF binary generation; the app now prepares audited export manifests and CSV-compatible spreadsheet downloads.
- External LLM-generated text automation; current generator is deterministic and review-first.

The integration readiness endpoints return provider metadata and avoid storing third-party credentials.

## RBAC notes
New backlog routes use `backend/core/permissions.py` for centralized role gates. Existing legacy routes have not been rewritten in this pass.

Admin and barn manager can manage financial, staff, reporting, automation, and integration shells. Trainers and staff have targeted care/training/operations access. Horse owners continue to use the existing owner portal. The shared barn location board is explicitly owner-visible only when a barn owner/admin publishes it.

Frontend backlog navigation now mirrors those role gates for sensitive backlog pages. Direct URL visits to guarded backlog routes render a permission-needed page instead of exposing a workspace shell.

## Verification checklist
- Backend imports compile with `python3 -m py_compile backend/core/permissions.py backend/routes/backlog.py backend/server.py`.
- Local contract tests pass with `PYTHONPATH=backend pytest backend/tests/test_backlog_contracts.py -q`.
- Frontend production build succeeds with `npm run build`.
- Existing routes remain mounted.
- Existing dashboard, care, task engine, auth, notification, onboarding, and operations routes are not overwritten.
- New collections are additive only.
- Remote API regression coverage is available in `backend/tests/test_backlog_foundations.py` for deployed/staged environments.
