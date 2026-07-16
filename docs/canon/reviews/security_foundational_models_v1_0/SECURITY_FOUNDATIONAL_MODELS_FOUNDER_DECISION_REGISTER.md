# SECURITY FOUNDATIONAL MODELS FOUNDER DECISION REGISTER

**Status:** Pending Founder Review
**Implementation Authority:** False
**Production Authority:** False

## A. Data Protection, Encryption, and Key Management

| ID | Decision | Recommended disposition | State |
| --- | --- | --- | --- |
| DPKM-FD01 | Adopt a dedicated data-protection and key-management model | ACCEPT | pending |
| DPKM-FD02 | Place it as a security constitutional peer or subordinate | ACCEPT_WITH_MODIFICATION: decide tier | pending |
| DPKM-FD03 | Confirm encryption never grants permission | ACCEPT | pending |
| DPKM-FD04 | Require environment and purpose key isolation | ACCEPT | pending |
| DPKM-FD05 | Require governed key hierarchy and lifecycle | ACCEPT | pending |
| DPKM-FD06 | Require dual control for high-consequence key operations | ACCEPT_WITH_MODIFICATION: define threshold later | pending |
| DPKM-FD07 | Keep provider selection outside canon | ACCEPT | pending |
| DPKM-FD08 | Require algorithm and protocol registries | ACCEPT | pending |
| DPKM-FD09 | Keep cryptographic erasure subordinate to stewardship | ACCEPT | pending |
| DPKM-FD10 | Require current authorization after restore | ACCEPT | pending |
| DPKM-FD11 | Treat key loss as security and availability incident | ACCEPT | pending |
| DPKM-FD12 | Keep customer-managed keys and BYOK disabled pending separate governance | ACCEPT | pending |

## B. Security Incident Response and Disclosure

| ID | Decision | Recommended disposition | State |
| --- | --- | --- | --- |
| SIRD-FD01 | Adopt a dedicated incident-response and disclosure model | ACCEPT | pending |
| SIRD-FD02 | Place it as a Security peer or subordinate model | ACCEPT_WITH_MODIFICATION: decide tier | pending |
| SIRD-FD03 | Adopt consequence-based SEV-0 through SEV-4 | ACCEPT | pending |
| SIRD-FD04 | Require one accountable Incident Commander | ACCEPT | pending |
| SIRD-FD05 | Separate incident, privacy incident, breach, and safety incident | ACCEPT | pending |
| SIRD-FD06 | Require evidence-qualified known/suspected/unknown language | ACCEPT | pending |
| SIRD-FD07 | Keep universal legal deadlines out of canon | ACCEPT | pending |
| SIRD-FD08 | Require controlled jurisdiction and obligation registry | ACCEPT | pending |
| SIRD-FD09 | Require guardian and prohibited-contact validation for notices | ACCEPT | pending |
| SIRD-FD10 | Permit time-bounded emergency restriction without lasting authority | ACCEPT | pending |
| SIRD-FD11 | Require independent validation before closure | ACCEPT | pending |
| SIRD-FD12 | Establish vulnerability-report intake without authorizing a bounty | ACCEPT | pending |

## C. Platform Resilience, Backup, and Recovery

| ID | Decision | Recommended disposition | State |
| --- | --- | --- | --- |
| PRBR-FD01 | Adopt resilience as subordinate Platform Operations governance | ACCEPT | pending |
| PRBR-FD02 | Preserve Record Stewardship ownership of restoration semantics | ACCEPT | pending |
| PRBR-FD03 | Preserve Security ownership of threat and containment controls | ACCEPT | pending |
| PRBR-FD04 | Treat backups as unproven until restoration is tested | ACCEPT | pending |
| PRBR-FD05 | Require current permission recalculation after restore | ACCEPT | pending |
| PRBR-FD06 | Require explicit service criticality and dependency registry | ACCEPT | pending |
| PRBR-FD07 | Treat RTO/RPO as measured objectives, not guarantees | ACCEPT | pending |
| PRBR-FD08 | Require split-brain and dual-write prevention | ACCEPT | pending |
| PRBR-FD09 | Require honest, bounded degraded modes | ACCEPT | pending |
| PRBR-FD10 | Require isolated restore and disaster-recovery exercises | ACCEPT | pending |
| PRBR-FD11 | Require provider exit and recovery planning | ACCEPT | pending |
| PRBR-FD12 | Keep all backup, restore, failover, and production execution separately gated | ACCEPT | pending |

## Founder Review Guidance

Review the boundary decisions first: `DPKM-FD02`, `SIRD-FD02`, `PRBR-FD01`, `PRBR-FD02`, and `PRBR-FD03`. If those are accepted, the remaining decisions can be reviewed by domain. Any modification that gives cryptography business authority, gives Platform Operations record-restoration authority, or gives incident command lasting permission authority should return the package for correction.

