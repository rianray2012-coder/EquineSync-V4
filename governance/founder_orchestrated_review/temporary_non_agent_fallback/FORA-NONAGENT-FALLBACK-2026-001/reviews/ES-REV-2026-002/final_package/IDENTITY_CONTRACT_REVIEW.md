# Identity Contract Review

`NON_AGENT_CONTROLLED_THREAD_REVIEW`

`NOT_ES_RA_AGENT_EVIDENCE`

Identity cross-domain contracts are not ready for exact-text ratification.

- Identity-to-Authorization must fail closed when required identity, session, relationship, policy, or authority facts are stale, missing, disputed, or version-incompatible; it must preserve the full authenticated/acting/represented/approving/executing actor chain where applicable.
- The recovery-assurance invariant must preserve the Founder-required additional step-up, risk-check, or controlled-review condition for high-risk action. Current wording is a P0 weakening.
- Identity-to-Protected-Participant must preserve mandatory separate minor identity/account/credentials and define versioned inputs/outputs, authority ownership, disputes, revocation, holds, attribution, privacy, audit, and contract tests. Current optional/ordinary wording is a P0 weakening.
- Identity-to-Relationships must use typed party references and a versioned representation basis while keeping representation-context attribution separate from relationship or permission authority.
- Multi-location organization/tenancy topology is not an Identity-owned decision and requires the owning Business, Facility, Relationships, Authorization, Privacy, contractual, financial, and operational authorities.

All contract changes remain `PROPOSED_NOT_APPROVED`; Authorization and Facility PIA drafting is out of scope.
