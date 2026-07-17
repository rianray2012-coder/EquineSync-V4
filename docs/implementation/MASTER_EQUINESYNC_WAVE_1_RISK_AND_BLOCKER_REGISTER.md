# Master EquineSync Wave 1 Risk and Blocker Register

| ID | Severity | Risk/blocker | Treatment |
| --- | --- | --- | --- |
| `W1-P1-01` | P1 | Canonical account/actor/source-of-truth mapping is not yet executable evidence | Complete read-only inventory and mapping before runtime scope |
| `W1-P1-02` | P1 | Role, platform-role, membership, barn/facility and relationship authority may drift across backend/frontend | Build comparison matrix and backend-enforcement tests |
| `W1-P1-03` | P1 | Threat model for custom auth, recovery, refresh rotation, suspension and seed paths is incomplete | Complete threat model before implementation authorization |
| `W1-P1-04` | P1 | Schema/index and migration impact is not fully inventoried | Produce collection/index/history inventory; no changes |
| `W1-P1-05` | P1 | Audit attribution and revocation continuity are not proven across all auth paths | Define and test expected evidence contract |
| `W1-P2-01` | P2 | Identity/provider selection remains undecided | Keep provider-neutral; defer selection |
| `W1-P2-02` | P2 | Environment/secret ownership and observability evidence is incomplete | Carry to Platform Operations and future readiness |
| `W1-P2-03` | P2 | High-risk minors/biometric/international/deceased/merge scenarios need specialists | Trigger Identity P2 review when scoped |

No P0 was found. All five P1s block runtime implementation, not the readiness-analysis package.
