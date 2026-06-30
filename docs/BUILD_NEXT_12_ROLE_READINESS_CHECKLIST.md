# Build-Next-12 Role Account Readiness Checklist

Generated: 2026-06-30

## Purpose

This checklist records whether the official production environment has role
accounts ready for BN12 UAT. It does not mark the UAT workflows as passed.

Account readiness means an account exists, can sign in, and is assigned the
intended role/context. Workflow pass still requires sanitized evidence from the
role walkthrough.

BN12A provides a CLI helper for creating these accounts:
`backend/scripts/seed_bn12_uat_accounts.py`.

## Environment

| Field | Value |
| --- | --- |
| Environment label | final production |
| Frontend URL | `https://app.equine-sync.com` |
| API URL | `https://equine-sync-api.onrender.com` |
| Database label | MongoDB Atlas / Equine Sync / EsProduction / ES_Members |

## Status Terms

| Status | Meaning |
| --- | --- |
| `ready` | Account exists, can sign in, and has intended role/context. |
| `pending` | Account not yet confirmed. |
| `blocked` | Account cannot be used until a setup issue is fixed. |
| `founder-accepted` | Rian explicitly accepts a caveat for first-client pilot only. |

## Role Readiness Matrix

| UAT ID | Role | Account Readiness | Evidence Needed Next |
| --- | --- | --- | --- |
| UAT-R1 | Platform admin | pending | Confirm platform admin can sign in and reach Admin Portal. |
| UAT-R2 | Facility admin / barn owner | pending | Confirm facility admin can sign in to the intended facility context. |
| UAT-R3 | Barn manager | pending | Confirm barn manager can sign in and reach Care Ledger manager tools. |
| UAT-R4 | Staff | pending | Confirm staff can sign in and reach assigned work/daily-check context. |
| UAT-R5 | Horse owner | pending | Confirm horse owner can sign in and reach linked owner-safe horse context. |
| UAT-R6 | Guardian / parent | pending | Confirm guardian/parent can sign in and reach linked minor/student context. |
| UAT-R7 | Lesson participant | pending | Confirm participant can sign in and reach lesson context. |
| UAT-R8 | Standalone individual owner | pending | Confirm individual owner can sign in without active facility membership. |

## BN12A Seed Roster

If the role accounts do not exist yet, run the BN12A seed script and copy the
one-time passwords privately.

| UAT ID | Seeded Email |
| --- | --- |
| `UAT-R1` | `uat.platform@equine-sync.com` |
| `UAT-R2` | `uat.facility-admin@equine-sync.com` |
| `UAT-R3` | `uat.manager@equine-sync.com` |
| `UAT-R4` | `uat.staff@equine-sync.com` |
| `UAT-R5` | `uat.owner@equine-sync.com` |
| `UAT-R6` | `uat.guardian@equine-sync.com` |
| `UAT-R7` | `uat.participant@equine-sync.com` |
| `UAT-R8` | `uat.individual-owner@equine-sync.com` |

## Evidence Rules

For each role row, record only:

- account exists: yes/no,
- sign-in works: yes/no,
- role/context is correct: yes/no,
- sanitized screenshot or short operator note,
- tester/operator name,
- timestamp.

Never record passwords, auth tokens, reset links, invite tokens, API keys,
webhook secrets, private keys, Mongo connection strings, raw provider payloads,
payment data, full audit diffs, or private customer data.

## Current Verdict

`role readiness pending`

BN12 cannot close until UAT-R1 through UAT-R8 are either `ready` and then
walked through with sanitized evidence, or explicitly founder-accepted by Rian
with a caveat.
