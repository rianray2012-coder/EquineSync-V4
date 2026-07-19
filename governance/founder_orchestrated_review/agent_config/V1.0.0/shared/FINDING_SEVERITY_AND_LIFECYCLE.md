# Finding Severity, Substantiation, and Lifecycle

## Severity

- **P0 Critical:** Demonstrated or highly credible immediate unacceptable safety, security, legal, financial, welfare, data-integrity, baseline-integrity, or catastrophic authority risk.
- **P1 Blocking:** Material defect that must be resolved before the requested gate may pass.
- **P2 Nonblocking:** Meaningful weakness that may be retained only through express Founder disposition.
- **Observation:** Relevant condition not presently requiring remediation.
- **Founder Decision Required:** Policy, authority, scope, risk, or business choice reserved to the Founder.

## Substantiation

- `CANDIDATE_FINDING`
- `SUBSTANTIATED`
- `REPRODUCED`
- `CORROBORATED`
- `DISPUTED`
- `UNSUBSTANTIATED`
- `WITHDRAWN_WITH_HISTORY`
- `FOUNDER_DISPOSITIONED`

## Required fields

Every finding needs an identifier, source agent, affected requirement and artifact, observed and expected conditions, evidence, severity rationale, confidence, impact, dependencies, remediation, objective verification criteria, owner, gate, status, and Founder disposition when issued.

## Severity changes

A P0 or P1 downgrade requires written rationale, preserved original severity, new evidence or corrected analysis, separate review, and Founder disposition.

## Closure

Closure requires documented remediation, dependency review, executed closure criteria, preserved evidence, separate verification, regression consideration, residual-risk recording, and proper authority.
