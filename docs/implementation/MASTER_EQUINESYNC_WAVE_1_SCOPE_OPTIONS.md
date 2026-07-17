# Master EquineSync Wave 1 Scope Options

## Option A - Identity Foundation Readiness and Security Hardening Assessment

- **Exact scope:** Read-only auth/account/actor inventory; threat model; role/permission mapping; session/recovery/revocation review; audit-attribution contract; schema/index/migration inventory; focused test plan.
- **Excluded:** Runtime fixes, schema/index changes, migrations, provider selection, credential activity, production access.
- **Dependencies:** Locked Identity/Relationship/External Architecture; Permission; Stewardship; Audit candidate; Wave 0.
- **Affected files/domains:** Auth, token, login-attempt, tenancy, account-context, membership, permission, audit, frontend permission/navigation, config and lifespan files as read-only evidence.
- **Data/schema/migration impact:** None; inventory only.
- **Authentication/permission impact:** None; compare intended and existing behavior.
- **Security/external-service impact:** Threat analysis only; no provider activity.
- **Testing:** Static contracts, focused existing-test execution, gap matrix, proposed regression suite.
- **Rollback:** Not applicable; documentation-only outputs can be superseded.
- **Observability:** Inventory current logs/audits/metrics and define gaps.
- **Risk:** Low.
- **Evidence:** Inventory, threat model, source-of-truth matrix, permission matrix, test baseline, blocker report.
- **Founder decisions:** Approve bounded assessment; later decide whether any implementation RF opens.

## Option B - Existing Identity Foundation Convergence

- **Exact scope:** Later bounded corrections to canonical account/actor mapping, backend permission enforcement, and audit attribution using the existing custom identity runtime.
- **Excluded:** Provider replacement, broad migration, production activation, unrelated onboarding redesign.
- **Dependencies:** Option A evidence complete; source-of-truth decision; threat model; migration/rollback and tests approved.
- **Affected files/domains:** Auth/core auth, tokens, tenancy, memberships, permissions, audit, selected routes and frontend mirrors.
- **Data/schema/migration impact:** Potentially material; unknown until Option A.
- **Authentication/permission impact:** Direct and high-risk.
- **Security/external-service impact:** Security-critical; no external provider required.
- **Testing:** Full auth/authorization/session/tenancy/audit regression suite and negative cross-barn cases.
- **Rollback:** Feature flags, compatibility adapter, reversible data mapping or forward recovery.
- **Observability:** Auth failure, token/session invalidation, permission denial and audit-correlation telemetry.
- **Risk:** High until Option A closes P1s.
- **Evidence:** Approved design, diffs, tests, fixture migration, rollback rehearsal.
- **Founder decisions:** Separate implementation authorization and environment/data scope.

## Option C - Identity-Provider Transition Preparation

- **Exact scope:** Provider-neutral architecture, account-linking design, assurance mapping, export/import contract, staged transition, rollback and vendor evaluation criteria.
- **Excluded:** Provider selection, OAuth/OIDC/SAML/MFA activation, credentials, migration execution, runtime change.
- **Dependencies:** Option A; locked External Architecture; Identity P2 treatment; privacy/security/legal review where material.
- **Affected files/domains:** Planning artifacts only initially; future auth/token/account/session surfaces.
- **Data/schema/migration impact:** Potentially very high; planning only.
- **Authentication/permission impact:** Future high impact; none now.
- **Security/external-service impact:** Provider, credential, assurance, outage, portability and lock-in risks.
- **Testing:** Contract tests, account-linking fixtures, duplicate/rollback/recovery scenarios.
- **Rollback:** Retain canonical EquineSync identity and reversible provider bindings.
- **Observability:** Provider status, linking failures, fallback, security events and audit lineage.
- **Risk:** Medium for planning; very high for future execution.
- **Evidence:** Neutral ADR, provider criteria, data-flow/threat model, migration rehearsal plan.
- **Founder decisions:** Whether transition is needed; provider shortlist only through later authority.

## Recommendation

Choose Option A. It is the only option that is currently reversible, non-mutating, provider-neutral, and capable of producing the evidence required to scope Options B or C safely.
