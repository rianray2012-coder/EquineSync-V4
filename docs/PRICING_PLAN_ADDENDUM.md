# EquineSync Pricing Plan Addendum

Updated: 2026-06-19

This addendum is part of the EquineSync build direction file set. It updates the pricing model that future billing, admin portal, HorseOps, owner portal, and mobile-readiness work must honor.

## Pricing Definitions

- Active horse: a horse with active records, tasks, feed plans, health logs, training logs, billing, or owner updates.
- Staff seat: a groom, trainer, assistant, working student, or employee who can complete tasks, enter notes, upload photos, or manage care.
- Owner/manager seat: a stable owner, barn manager, business admin, or user with elevated permissions.
- Client owner portal account: included with barn and trainer plans. Invited horse owners should not count as staff seats and should not pay separately to view approved updates, invoices, photos, or documents.

## Updated Tiers

| Tier | Plan | Monthly | Annual | Included Limits |
| --- | --- | ---: | ---: | --- |
| 0 | Invited Horse Owner Portal | $0 | N/A | Portal access for owners invited by a subscribed barn, trainer, or facility |
| 1 | Individual Horse Owner | $14.99 | $149 | 1 active horse, 1 owner account, 1 emergency contact |
| 2 | Private Owner Plus | $29.99 | $299 | Up to 5 active horses, 1 owner/manager seat, 2 helper/family seats |
| 3 | Starter Barn | $69.99 | $699 | Up to 10 active horses, 3 staff seats, 1 owner/manager seat |
| 4 | Advanced Barn | $149.99 | $1,499 | Up to 30 active horses, 8 staff seats, 2 owner/manager seats |
| 5 | Elite Barn | $299.99 | $2,999 | Up to 50 active horses, 12 staff seats, 4 owner/manager seats |
| 6 | Trainer - No Lesson Program | $59.99 | $599 | Up to 20 active training horses, 1 owner/manager seat, 2 staff/assistant seats |
| 7 | Trainer + Lesson Program - 15 Participants | $99.99 | $999 | Up to 15 active lesson participants, up to 15 active horses, 1 owner/manager seat, 3 staff/trainer seats |
| 8 | Trainer + Lesson Program - 50 Participants | $179.99 | $1,799 | Up to 50 active lesson participants, up to 25 active horses, 3 owner/manager seats, 6 staff/trainer seats |
| 9 | Enterprise / Multi-Location | Starts at $599 | Custom | 100+ active horses, multi-location support, custom seats, API access, SSO if needed |

## Overage Rules

| Item | Price |
| --- | ---: |
| Additional horse on Individual Horse Owner | $5/month per horse |
| Additional horse on Private Owner Plus | $5/month per horse |
| Additional helper seat on Private Owner Plus | $6/month |
| Additional horse on Starter Barn | $7/month per horse |
| Additional horse on Advanced Barn | $6/month per horse |
| Additional horse on Elite Barn | $5/month per horse over 50 |
| Additional staff seat | $8/month |
| Additional owner/manager seat | $15-$20/month, depending on tier |
| Additional participant over 50 on large lesson plan | $3/month per participant |
| Additional horse over 25 on large lesson plan | $5/month per horse |

The 15-participant lesson tier should not support participant overage. Users should upgrade to the 50-participant tier once they exceed 15 active participants.

## Add-Ons

- Additional media/document storage: $10/month per extra storage block.
- Custom branding or white label: $99/month.
- Advanced AI owner update assistant: $29/month.
- QuickBooks integration: $19/month or included in Elite.
- Stripe payment processing: included, with processing fees passed through.
- Data migration service: $299-$1,500 one time.
- Premium onboarding call: $199-$499 one time.
- Enterprise onboarding setup fee: $1,500-$3,500, with complex migration quoted separately.
- Nonprofit / Education / Rescue program: 30-50% discount or custom quote.

## Build Direction Changes

Implementation foundation for these changes is tracked in
`docs/PRE_LAUNCH_PRICING_FOUNDATION.md` and `PHASE_HORSEOPS_1J_README.md`.

### Add Before Launch Hardening

1. Add a canonical pricing configuration source for all plan limits, prices, overages, and included features.
2. Add plan type to organizations/accounts: individual owner, private owner, barn, trainer, lesson program, enterprise, nonprofit/community.
3. Add usage counters for active horses, staff seats, owner/manager seats, helper seats, and lesson participants.
4. Make invited owner portal accounts free when tied to a subscribed barn/trainer organization.
5. Add enforcement rules for plan limits and overages.
6. Add admin portal controls to view plan, usage, overages, billing status, discounts, and manual overrides.
7. Add upgrade prompts when a user reaches horse, seat, or lesson participant limits.
8. Add billing-safe language throughout the app so users understand what counts as an active horse or paid seat.

### Add To HorseOps Phases

- HorseOps 1J should add the pre-launch pricing foundation: active/inactive horse status, canonical usage counters, free invited owner portal rules, and role-based seat tracking.
- HorseOps 1K should include alerts when active horse limits or seat limits are nearing capacity.
- HorseOps 1L should preserve the free invited owner portal model in owner-facing workflow polish. Owner visibility should be tied to approved horse access, not paid staff seat access.
- HorseOps 1M should include reports for active horse count, staff usage, owner/manager seats, participant count, and billing-relevant activity.
- HorseOps 1N should verify mobile usability for billing-affected workflows: adding horses, inviting staff, inviting owners, upgrading, and handling limit messages.

### Add To Admin Portal Scope

- Plan selector and billing status.
- Organization usage dashboard.
- Active horse count and inactive horse count.
- Seat count by role type.
- Invited owner portal account list.
- Lesson participant count.
- Overage summary.
- Discount/community program flag.
- Manual comp/trial/enterprise override.
- Audit trail for billing-sensitive changes.

### Add To Mobile Readiness

- Mobile users must be able to see when adding a horse, staff member, helper, or participant would exceed the current plan.
- Limit and upgrade messages must be short, clear, and non-blocking when possible.
- Invited owners should never see language implying they need to buy a plan when they are accessing a horse through a subscribed barn.
- Staff completing daily care should not be interrupted by billing flows unless their action requires adding a new paid resource.

## Launch Hardening Checks

- Verify every plan maps to the correct Stripe product/price before production.
- Verify yearly pricing is available where specified.
- Verify free owner portal accounts cannot create paid-plan access unless they intentionally start an independent owner plan.
- Verify owner portal users do not count as staff seats.
- Verify active/inactive horse status affects usage counters correctly.
- Verify overage billing is accurate and visible before charges occur.
- Verify admin overrides are permission-gated and audited.
- Verify enterprise, nonprofit, and custom contracts can be handled without forcing them through public checkout.
- Verify plan-limit behavior is tested on desktop and mobile.

## Implementation Note

The next build phases should not implement all billing automation at once. They should add the data model, usage counters, role distinctions, and admin visibility needed so launch hardening is not forced to untangle pricing later.
