# RF10 Service Provider / Care Partner Multi-Barn Model Plan

Date: 2026-07-06

Status: CODEX-REVIEWED & LOCKED.

## Purpose

RF10 should turn service-provider access from role-shell visibility into a
truthful care-partner model for vets, farriers, bodyworkers, haulers, and other
equine providers. The core problem is scoped trust: a provider may work across
multiple barns and individual owners, but must only see horses, visits,
documents, notes, and invoices they have been explicitly granted.

## Entry Conditions

- RF9 is Codex-reviewed and locked.
- RF1 tenant and owner-safe data fences remain locked.
- RF2 stable-ID access migration remains locked.
- RF5 public enrollment keeps service providers on a separate path.
- RF6 canonical integration-readiness boundaries remain locked.
- RF7 owner/guardian privacy boundaries remain locked.
- RF8 staff identity work remains locked.

## Strict Scope

RF10 may:

- inventory current service-provider, veterinarian, farrier, health, document,
  invoice, appointment, and enrollment surfaces;
- define provider profile/business identity fields without mutating external
  provider systems;
- add backend-authoritative provider access grants where the existing data model
  supports safe `provider_user_id`, `horse_id`, `owner_user_id`, `barn_id`, and
  grant status fields;
- add revocation and denied-access tests for provider-visible records;
- harden the service-provider dashboard from shell/readiness into a truthful
  care-partner workspace if it can be done without broad billing or messaging
  claims;
- document provider type priority and founder decisions.

RF10 must not:

- grant broad barn-wide provider access without explicit horse/client grants;
- expose owner-only, guardian/minor, staff-only, private barn, or unrelated
  horse records;
- implement Stripe billing, refunds, package pricing, or provider payout truth,
  which remain RF12 unless evidence-only;
- implement live external provider calls, DocuSign, Resend, Apple, Google,
  Vercel, Render, Atlas, or UAT account mutations;
- implement general messaging delivery truth, which remains RF13;
- implement legal signature/storage consolidation, which remains RF14;
- implement offline/native behavior, which remains RF15/RF16/BN22A;
- mark founder decisions accepted automatically.

## Target Workstreams

| Workstream | Goal | Evidence Required |
| --- | --- | --- |
| Provider surface inventory | Map provider dashboard, role home, enrollment, health-care, appointments, documents, invoices, and service request surfaces. | Source scan with file/route references and RF0 finding mapping. |
| Provider profile and type model | Identify provider types and required business/contact/licensing fields for first-client use. | Data inventory plus founder-decision rows for first UAT provider type. |
| Explicit access grants | Ensure provider-visible horses/clients are linked by stable IDs and explicit grant status. | Backend tests for allowed, revoked, denied, cross-barn, and unrelated-horse cases. |
| Visit and care notes | Define what provider notes can be created/read without leaking staff/internal or owner-only content. | Route tests and launch-claim boundary rows. |
| Documents and invoices boundary | Map provider documents/invoices to RF12/RF14 if not safely implemented in RF10. | Deferred rows with owning phases. |
| Dashboard truth | Replace service-provider shell claims with real provider-owned work or a truthful readiness state. | Frontend source evidence and build proof. |

## Acceptance Criteria

- RF10 report status is `ready` with zero blocker rows.
- Provider access is explicit, grant scoped, revocable, and stable-ID based
  where the existing same-barn provider assignment model supports it.
- Account-level stable provider identity across unrelated barns is recorded as
  deferred until a future account-membership policy and RF18 UAT prove it.
- Providers cannot see unrelated barns, unrelated horses, unrelated owner data,
  staff-only notes, guardian/minor restricted content, or private barn records.
- Provider-authored RF10 care entries are limited to provider visit notes until
  founder-approved canonical care-write authority is implemented and tested.
- Service-provider enrollment posture is truthful and separate from barn owner,
  trainer, staff, rider, guardian, and individual owner enrollment paths.
- Any billing, payout, legal document, messaging, external-provider integration,
  or multi-facility provider work not completed in RF10 is recorded as deferred
  with the owning future phase.

## Founder Decision Rows

| Decision | Status | Notes |
| --- | --- | --- |
| Choose first RF10 provider type for UAT. | requires founder review | Recommended first choice: farrier or veterinarian, because both need explicit horse grants and visit notes. |
| Decide service-provider signup review posture. | requires founder review | RF5 separates the service-provider enrollment path; RF10 should decide pending-review fields and approval policy. |
| Decide provider grant authority. | requires founder review | Decide whether barn managers, horse owners, assigned trainers, or platform support can invite/revoke providers. |
| Decide provider invoice/payment timing. | requires founder review | Recommended: defer payment truth to RF12 unless RF10 only records non-billing visit context. |

## Recommended Verification

- Focused RF10 backend tests for provider grants, revocation, and denial.
- RF10 report generation with `--fail-on-blockers`.
- Any touched frontend build.
- Zip integrity and expected manifest check.
- `git diff --check`.
- Secret-shape scan.
