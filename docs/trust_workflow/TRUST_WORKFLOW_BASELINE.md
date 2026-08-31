# EquineSync Trust And Workflow Baseline

Status: TW-0/TW-1 BASELINE CREATED
Date: 2026-08-30
Authority: Planning and guardrail evidence only. This baseline does not authorize production launch, provider activation, billing expansion, broad messaging activation, document-signature activation, AI live mutation, or multi-facility expansion.

## Purpose

This baseline starts the approved TW-0/TW-1 trust-and-workflow workstream. It translates the deeper UX/UI review into controlled implementation gates before product behavior is expanded.

The immediate product goal is trust clarity:

1. Users can tell what is live, gated, draft-only, provider-required, or unavailable.
2. Pending and empty states explain what is missing and who can act.
3. Public and in-app copy does not claim unsupported capability.
4. Route, navigation, and role promises stay aligned.

## Current Product Truth

EquineSync has broad frontend coverage across care, training, owner, billing, document, messaging, admin, and provider-adjacent surfaces. The current risk is not lack of screens. The risk is that users may see many destinations before the product clearly explains status, authority, visibility, and next action.

Current strengths:

- Role-specific dashboards and navigation are present for facility, manager, staff, trainer, owner, guardian, rider, and service-provider roles.
- Existing route helpers separate dashboard paths, intake paths, setup routing, and safe redirect behavior.
- The admin portal has a dedicated namespace under `/admin/portal`.
- The trainer intake and operating-center work intentionally preserves reviewed/read-only and facility-gated boundaries.
- Existing docs already distinguish several readiness states for billing, messaging, documents, offline behavior, provider proof, and public launch.

Current trust risks:

- Some user-facing copy still relies on broad future-state phrasing instead of an explicit product status.
- Many role navigation items route to the same dashboard anchor, which can look like separate functionality even where separate workflow screens are not live.
- Provider-facing status must remain tightly scoped until invite, expiration, audit, and review controls are proven.
- Billing, payments, document signatures, media storage, external messaging, and AI automation must not be implied as broadly live merely because shell UI exists.
- Historical docs may retain legacy naming for provenance, while current product surfaces must use EquineSync consistently.

## Product Status Vocabulary

Use these status values in TW-0/TW-1 artifacts and follow-on UI copy:

| Status | Meaning | Copy Rule |
|---|---|---|
| `live` | Implemented and available within current role and permission boundaries. | State the action plainly and include proof/status where relevant. |
| `pilot` | Available only for bounded pilot use or specific approved accounts. | State pilot scope and avoid public launch language. |
| `gated` | Built or planned but blocked by review, permission, facility setup, or governance dependency. | Explain who reviews it and what unlocks. |
| `draft_only` | Users may draft or preview, but the system does not officially write/send/activate. | Label the draft state and next required approval or sync step. |
| `provider_required` | Capability depends on external provider credentials, webhook, storage, domain, or account setup. | Name the provider dependency without claiming activation. |
| `unavailable` | Not implemented or not approved for use. | Do not show as available; route users to support, roadmap, or setup context only if appropriate. |

## TW-1 Copy Rules

- Use `EquineSync` for current product copy.
- Use `Equine-Sync` only for domain styling or legacy asset titles that already contain the hyphenated form.
- Replace generic "coming soon" language with setup-aware or status-aware text.
- Do not say a provider integration, external message, document signature, billing workflow, storage upload, AI workflow, or multi-facility capability is live unless it has matching runtime proof and provider state.
- Empty states should answer: what is missing, who can fix it, and what useful action remains available.
- Permission-limited states should answer: what the user can see, why access is limited, and who can grant or review access.

## TW-1 Stop Rules

Stop before merge or release if:

- Current product copy uses legacy brand variants in active frontend surfaces.
- A user-visible statement claims public launch, live provider access, live signatures, live payments, live storage, broad offline sync, broad external messaging, broad AI mutation, or multi-facility switching without accepted evidence.
- A role surface links users into unauthorized workflow categories.
- A gated or pending state does not identify the review/dependency boundary.
- A new registry row lacks owner, status, user-facing promise, evidence path, and next action.

## Accepted TW-0/TW-1 Deliverables

- `docs/trust_workflow/TRUST_WORKFLOW_BASELINE.md`
- `docs/trust_workflow/PRODUCT_STATUS_REGISTRY.csv`
- `docs/trust_workflow/RECOMMENDATION_TRACEABILITY_MATRIX.csv`
- `backend/tests/test_trust_workflow_tw0_tw1.py`

## Out Of Scope

The following recommendations are planned but not implemented in TW-0/TW-1:

- Trainer Today command center.
- Owner wellbeing home.
- Unified decision workflow implementation.
- Handoff mode and last-verified labels.
- Facility launch checklist and operations readiness score.
- Provider scoped access and emergency provider mode.
- New billing, payment, document-signature, storage, SMS, push, email, AI, or multi-facility runtime behavior.

## Next Gate

After TW-0/TW-1 is reviewed, the next implementation gate should be TW-2 Role Home North Stars and TW-3 Unified Decision And Notification System. Those gates may only proceed after the product-status registry and copy/overclaim tests remain clean.
