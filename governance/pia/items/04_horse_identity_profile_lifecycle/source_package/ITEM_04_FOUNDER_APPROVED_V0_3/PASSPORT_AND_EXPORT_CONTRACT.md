# Passport and Export Contract

**Source artifact:** `ES-PIA-HORSE-IDENTITY-LIFECYCLE_V0_3_FOUNDER_APPROVED_DESIGN_BASELINE.md`
**Source sections:** `15.3`, `16`, `18`, `20`, `21`, `23`, `29`, `30`, `33`, `37`
**Decision controls:** `HOR-FD-004`, `HOR-FD-014`, `HOR-FD-015`, `HOR-FD-016`
**Authority:** `DOCUMENTARY_DESIGN_ONLY`

## Required Design Contract

Horse Passport, profile, search, report, public, emergency, provider, transfer, memorial, and export views are bounded projections. They are not unrestricted copies of the canonical horse record, legal-title certificates, complete medical files, completeness guarantees, or permission grants.

Every Passport or export projection must be purpose-specific, permission-filtered, source-versioned, time-stamped, watermarked, and attributable to a requesting actor and authority context. The projection must disclose omissions, limits, expiry where applicable, generation time, policy version, source versions, verification reference, and a statement that the projection is not proof of legal title or completeness.

Revocation, expiry, supersession, or invalidation blocks future platform access or trusted reliance. EquineSync must never claim that it remotely deleted a copy outside EquineSync control after a download or external transfer.

Verification of a Passport or export must return only minimum safe validity metadata and must not expand access to protected horse facts.

## Covered IDs

- Requirements: `HOR-REQ-019` through `HOR-REQ-026`, `HOR-REQ-071`, `HOR-REQ-073`, `HOR-REQ-104`, `HOR-REQ-113`, `HOR-REQ-114`, `HOR-REQ-116`
- Acceptance criteria: `HOR-AC-013`, `HOR-AC-014`, `HOR-AC-015`, `HOR-AC-024`, `HOR-AC-027`, `HOR-AC-042`, `HOR-AC-047`, `HOR-AC-048`
- Tests: `HOR-TST-011`, `HOR-TST-012`, `HOR-TST-013`, `HOR-TST-026`, `HOR-TST-028`, `HOR-TST-048`, `HOR-TST-056`, `HOR-TST-057`

## Deferred or Prohibited

No Passport endpoint, public profile, export process, document generation, verification service, schema, migration, marketplace, provider, registry, AI, external-service activation, deployment, production use, or enrollment action is authorized by this package.
