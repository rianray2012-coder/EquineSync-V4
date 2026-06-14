# PHASED_EXECUTION_PLAN.md
# EquineSync Refactor Execution Plan

> Production priority order (from `FEATURE_ROADMAP.md`): **Security & Stability → Mobile Workflows → Care Operations → Owner Trust → Billing Clarity → Reporting → AI Assistance → Ecosystem Expansion.**

## Phase 1: Documentation & Governance
**Status: ✅ Complete** (this pass)
Goals:
- Complete the `/docs` folder (in-repo source of truth)
- Add engineering rules
- Add architecture docs
- Add product vision
- Add permission matrix
- Add trust framework
- Reconcile stale/conflicting docs (DESIGN_TOKENS → Brand Guide)
- Create a code-grounded `KNOWN_TECH_DEBT.md`
- Save brand/logo assets

## Phase 2: Security Stabilization
**Status: ✅ Complete (2026-05-30)**
- **2A — ✅:** Removed unsafe JWT fallback; centralized config (`backend/config.py`) + fail-fast startup validation; dev-safe ephemeral secret; `tests/test_config.py`.
- **2B — ✅:** Rate limiting on auth endpoints (`backend/rate_limit.py`, `limits`) + CORS tightening (prod rejects `*`); `tests/test_rate_limit.py`.
- **2C — ✅:** Password reset + email verification (hashed single-use expiring tokens, `backend/auth_tokens.py`) + Resend templates; `email_verified` with safe backfill + off-by-default `ENFORCE_EMAIL_VERIFICATION`; `GET /api/health`; `tests/test_auth_tokens.py`, `tests/test_phase2c_auth.py`.
- **2D — ✅:** Account-level brute-force lockout (`backend/login_attempts.py`, 423 on lock, clear on success); branded `/reset-password` + `/verify-email` pages + Login "Forgot password?" flow; `tests/test_login_lockout.py`.

> Full backend suite: 235 passed, 1 skipped.

## Phase 3: Backend Modularization
**Status: In Progress (3A complete)** — see `PHASE3_MODULARIZATION_MAP.md`.
- **3A — ✅ Complete (2026-05-30):** Moved `config.py`, `rate_limit.py`, `auth_tokens.py`, `login_attempts.py` → `backend/core/` (via `git mv`); updated all imports; no behavior change; `/api/health` gained a `version` field.
- **3B — Planned:** Extract system/admin/analytics routes.
- **3C–3F — Planned:** Horse → Care/Task → Owner/Report → Billing route extraction.
- **3G — Planned:** server.py reduced to app assembly; JWT/auth helpers → `core/security.py`.

Goals:
- Break `server.py` into modular route files
- Move business logic into services
- Move schemas into schema files
- Create centralized config and security utilities

## Phase 4: Multi-Tenancy & Permissions
Goals:
- Enforce `barn_id` on all operational entities
- Add tenant isolation tests
- Add centralized permission service
- Align code with `ROLE_PERMISSION_MATRIX.md`

## Phase 5: Audit Logging
Goals:
- Create `AuditLog` model
- Track critical changes
- Add audit log service
- Add tests

## Phase 6: Care Workflow Strengthening
Goals:
- Improve feeding, turnout, medication, rehab, stall rest, grooming, training workflows
- Align with `WORKFLOW_MAPS.md`

## Phase 7: Owner Trust Layer
Goals:
- Improve owner dashboard
- Add weekly recap framework
- Add owner-facing update controls
- Add approval flow for sensitive updates

## Phase 8: Mobile Optimization
Goals:
- Optimize barn workflows for phone use
- Improve task completion UX
- Improve horse profile mobile view
- Improve quick notes and photo upload

## Phase 9: Billing Improvements
Goals:
- Improve invoice structure
- Add line-item clarity
- Support recurring charges
- Improve owner billing visibility

## Phase 10: Production Readiness
Goals:
- Add release checklist enforcement (`RELEASE_CHECKLIST.md`)
- Improve logging
- Add monitoring
- Prepare deployment checklist

---

## Phase 15: Subscription Billing v2 (True Stripe Subscriptions)

**Locks**: 1c · 2a · 3a · 4a · 5c · 6b (consumer-marketplace MERGE; `facility_id = barn_id`; one user → one facility → one subscription; Enterprise = Contact Sales; soft-warn only; 14-day trial).

### Hard rule — NO hard-blocking anywhere in Phase 15
Throughout Phase 15.A → 15.G, feature enforcement is **soft-warn only**.
No 402 responses. No create-flow blocking on horse/user/storage counts.
Usage endpoints surface counts and entitlements; UI surfaces banners and
upgrade prompts. **Hard enforcement is its own separately approved phase.**

### Sub-phase sequence (locked)
- **15.A** — Subscription foundation, backend-only. ✅ Shipped. Awaiting Codex review.
- **15.B** — Full webhook lifecycle: idempotency table, `subscription_invoices`,
  `payments`, lifecycle sync.
- **15.C** — Facility Owner Billing Portal + pricing-band swap + wizard Step 3 +
  monthly/annual toggle + resume flow + usage/limits display in billing UI.
- **15.D** — Trial email scheduler (env-gated, idempotent, fail-open).
- **15.E** — Platform-admin capability proposal + Admin Billing Dashboard
  (`barn:manage` alone is NOT enough for cross-facility platform billing
  visibility — a separate capability must be proposed and approved first).
- **15.F** — Soft-warn usage indicators in create flows and other operational
  UI surfaces. Still NO hard-blocking.
- **15.G** — Migration cleanup after one quiet release cycle. **Do not** remove
  `/membership/checkout` until telemetry/tests prove no usage.

### Protected during Phase 15
- Phase 9 `invoices` collection and recurring-charges flows are untouched.
  Stripe subscription invoices land in a NEW collection (`subscription_invoices`)
  in 15.B.
- `/api/membership/checkout` (one-time Checkout) stays operational with a
  deprecation comment until 15.G removes it.

