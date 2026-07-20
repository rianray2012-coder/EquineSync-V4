# Identity and Relationships Cross-PIA Alignment

`NON_AGENT_CONTROLLED_THREAD_REVIEW`

`NOT_ES_RA_AGENT_EVIDENCE`

## Aligned boundaries

- Authentication is not authorization.
- A relationship is not a permission or legal-authority decision.
- Acting-for context must be explicit, attributed, scoped, versioned, and fail closed when its basis is invalid.
- Provisional claims, offline proposals, evidence, provider responses, and verification assessments do not create authority.
- Historical identity and relationship facts are preserved rather than destructively merged.

## Open conflicts

- Minor-account separation and recovery assurance are weakened at the Identity-to-Protected-Participant and Identity-to-Authorization boundaries.
- Identity claims an organization/tenancy default owned by multiple other domains.
- Cross-domain party and representation-basis fields are not fully typed/versioned.
- Authorization counterparty authority is incomplete because the Authorization PIA/approval is missing.
- Relationships source IDs/lifecycles and decision-to-ADR mappings are not deterministically reconciled.
- Canonical unqualified `VERIFIED` conflicts with purpose-scoped verification.

Cross-PIA disposition: `REQUIRES_BOUNDED_REMEDIATION`. The documentary golden paths are traceable, but no cross-domain contract is treated as final, executable, or implementation-authorized.
