# BN15E Today's Pulse Founder Acceptance Ledger

Status: Codex-approved & locked

Generated: 2026-07-03

## Scope

BN15E records a founder-facing acceptance ledger for Today's Pulse after locked
BN15A, BN15C-A, BN15C-B, BN15C-C, and BN15D. It does not perform a fresh live
login pass and does not mark any row founder-accepted.

Lock note: Codex approved this ledger as a review artifact. The approval locks
the evidence ledger only; founder acceptance remains pending explicit founder
action row by row.

## Authority

| Decision | Rule |
| --- | --- |
| Founder acceptance authority | Rian only |
| Operator/Codex authority | Can mark rows ready for founder review, not founder-accepted |
| Evidence source | Locked BN13O screenshots + locked BN15 tests/reports |
| Official launch authority | Not granted by BN15E |
| Billing/provider acceptance | Deferred to live Stripe/billing evidence lane |

## Evidence Summary

| Evidence | Artifact | Status |
| --- | --- | --- |
| Data contract | BN15A focused tests | PASS |
| Frontend wiring | BN15C-A focused tests | PASS |
| Barn visibility policy | BN15C-B focused tests | PASS |
| Role-home evidence | BN15C-C focused tests/report | PASS |
| UAT evidence bridge | BN15D screenshots/report/tests | PASS |
| Founder acceptance | This ledger | Pending explicit founder action |

## Acceptance Ledger

| Row | Surface | Evidence | Current status | Founder action needed |
| --- | --- | --- | --- | --- |
| TP-1 | Platform admin Today's Pulse scope | BN15A platform contract + BN15D UAT-R1 screenshot | ready_for_founder_review | Confirm platform count-only summary is acceptable. |
| TP-2 | Facility admin / barn owner manager-safe Pulse | BN15A/BN15C-C manager-safe contract + BN15D UAT-R2a/R2b screenshots | ready_for_founder_review | Confirm manager-safe counts are useful and not overexposed. |
| TP-3 | Barn manager Pulse | BN15C-C manager role evidence + BN15D UAT-R3 screenshot | ready_for_founder_review | Confirm manager role home can show work, care, owner-request, and plan-usage counts. |
| TP-4 | Staff/groom Pulse | BN15C-C staff role evidence + BN15D UAT-R4a screenshot | ready_for_founder_review | Confirm staff can see work and horse-care counts only. |
| TP-5 | Trainer Pulse | BN15C-C trainer role evidence + BN15D BN13M-T1 screenshot | ready_for_founder_review | Confirm trainer can see work and horse-care counts only. |
| TP-6 | Working student Pulse | BN15C-C working-student evidence + BN15D BN13M-W1 screenshot | ready_for_founder_review | Confirm working student mirrors staff-safe count boundaries. |
| TP-7 | Horse owner facility context | BN15C-B owner-safe policy + BN15D UAT-R5 screenshot | ready_for_founder_review | Confirm siloed default and community-count option are acceptable. |
| TP-8 | Guardian / parent context | BN15C-B owner-safe policy + BN15D UAT-R6 screenshot | ready_for_founder_review | Confirm guardian sees only owner-safe horse context. |
| TP-9 | Rider / lesson participant context | BN15C-B owner-safe policy + BN15D UAT-R7 screenshot | ready_for_founder_review | Confirm rider sees only owner-safe horse context. |
| TP-10 | Standalone individual owner | BN15A individual-owner contract + BN15D UAT-R8 screenshot | ready_for_founder_review | Confirm individual-owner horse count behavior is acceptable. |
| TP-11 | Privacy exclusions | BN15A/BN15C-B/BN15C-C/BN15D privacy guards | ready_for_founder_review | Confirm no staff notes, raw payloads, alert triggers, audit diffs, provider IDs, or private horse records appear. |

## Explicit Non-Acceptances

The following are not accepted or cleared by BN15E:

- public launch;
- first-client pilot;
- live Stripe checkout;
- Customer Portal;
- Apple billing;
- DocuSign live workflow;
- Text/SMS notification delivery;
- mobile/native app behavior;
- owner projection changes;
- HorseOps write behavior;
- Admin Portal behavior.

## Founder Sign-Off Template

Use this template outside the codebase when Rian is ready to accept a row:

```text
Row:
Accepted by:
Date:
Environment:
Evidence reviewed:
Caveat, if any:
Decision: founder-accepted | needs_live_uat | blocked | deferred
```

## Current Verdict

Today's Pulse is ready for founder review, not automatically founder-accepted.
No launch-clearing claim is made by this ledger.

## Package

- `outputs/build_next_15e_today_pulse_founder_acceptance_ledger.zip`
