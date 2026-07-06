# BN15C-C Today Pulse Role-Home Evidence Report

Generated: 2026-07-03

## Scope

BN15C-C verifies Today's Pulse role-home behavior after locked BN15A,
BN15C-A, and BN15C-B. The pass is evidence and read-only UX hardening only.
It does not add backend behavior, new routes, or new workflow surfaces.

## Evidence Summary

| Evidence area | Result |
| --- | --- |
| Manager-safe cards | Manager role can see count-only work, horse-care, owner requests, and plan usage summaries. |
| Staff/trainer cards | Staff and trainer roles can see count-only work and horse-care summaries; owner requests and plan usage are hidden. |
| Owner-safe siloed policy | Owner, guardian, and rider roles see owner-safe horse-care card with barn-wide horse count `0`. |
| Owner-safe community policy | Owner, guardian, and rider roles may see total horse count only. |
| Rider/guardian frontend wiring | Rider and guardian pages now consume the existing `useTodayPulse()` hook through the `horse_care` helper only. |
| Private field scan | Role-home Pulse helper remains free of staff notes, raw payloads, source check IDs, triggers, audits, Stripe IDs, passwords, and tokens. |

## Role Matrix

| Role | Today's work | Horse count | Alert counts | Owner requests | Plan usage |
| --- | --- | --- | --- | --- | --- |
| barn_manager | visible | visible | visible counts only | visible count only | visible count only |
| groom | visible | visible | visible counts only | hidden | hidden |
| working_student | visible | visible | visible counts only | hidden | hidden |
| trainer | visible | visible | visible counts only | hidden | hidden |
| horse_owner, siloed | hidden | `0` | `0` | hidden | hidden |
| parent, siloed | hidden | `0` | `0` | hidden | hidden |
| rider, siloed | hidden | `0` | `0` | hidden | hidden |
| horse_owner, community | hidden | total count only | `0` | hidden | hidden |
| parent, community | hidden | total count only | `0` | hidden | hidden |
| rider, community | hidden | total count only | `0` | hidden | hidden |

## Privacy Assertions

The focused tests assert serialized owner-safe responses do not include:

- staff notes;
- private request notes;
- raw alert triggers;
- `source_check_id`;
- private horse notes;
- Stripe-shaped subscription fields.

## Strict Exclusions

- No owner projection changes.
- No Stripe, Apple, checkout, Customer Portal, or entitlement changes.
- No DocuSign changes.
- No Text/SMS, push, native mobile, offline sync, AI, scheduler, or workflow-engine changes.
- No Admin Portal capability changes.
- No landing page changes.

## Package

Package target:

- `outputs/build_next_15c_c_today_pulse_role_home_evidence.zip`
