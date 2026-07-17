# Native Offline Synchronization Founder Decision Register

Every decision is `PENDING_FOUNDER_DECISION`. Recommendations are not approvals.

| ID | Question | Recommended option | Alternatives and consequences | Risk | Requested Founder action |
| --- | --- | --- | --- | --- | --- |
| NOS-FD01 | Approve first slice? | Server-classified `LOW_RISK_TASK_V1` create/complete/skip/bulk; update proposal; QuickAdd/routine-care drafts; status/retry/inspection only | Smaller completion-only slice lowers scope; generic task eligibility could hide safety work and is rejected; broader care slice raises safety risk | Operational/security/safety | Accept, modify, or reject exact workflow and policy-class boundary |
| NOS-FD02 | Supported platforms for first implementation? | Browser adapter plus iOS/Android adapters in isolated tests; no public support claim | Browser-only is simpler; native-only misses web parity | Device/platform | Select platform scope |
| NOS-FD03 | Persistence technologies? | IndexedDB typed adapter for browser; encrypted SQLite-compatible native adapter; shared TypeScript core | Separate engines, webview store, or no browser persistence | Security/data integrity | Approve recommendation or require bounded comparison |
| NOS-FD04 | Native versus hybrid architecture? | Shared domain/outbox core with native/browser storage adapters | Fully native engines increase semantic drift; web-only limits field use | Architecture | Approve shared-core boundary |
| NOS-FD05 | Maximum first-slice capability tier? | Tier 4 for approved task operations, Tier 2 drafts, no Tier 5 | Tier 3-only reduces server work; broader Tier 4 expands conflict surface | Data integrity | Approve tier ceiling |
| NOS-FD06 | Safety-critical exclusions? | Approve full exclusion register | Add any item only through separate domain gate | Safety/legal/privacy | Accept or identify explicit exception for later review |
| NOS-FD07 | Phase sequencing? | Phases 0-6 as written; separate approval at each | Combine phases for speed or split by platform; both alter evidence isolation | Governance/complexity | Approve or modify sequence |
| NOS-FD08 | Anticipated schema additions? | Approve planning classifications; no schema work until later directive | Reuse existing routes only may leave idempotency/version gaps | Data integrity | Approve boundary, not implementation |
| NOS-FD09 | Feature-flag model? | Layered build/runtime/server/workflow flags, all default false | One flag is simpler but unsafe; remote flag adds external dependency | Security/release | Approve layered model |
| NOS-FD10 | Device testing scope? | Approved browser matrix, iOS/Android simulator plus physical representative devices before Phase 5 exit | Simulator-only misses storage/suspension; broad matrix increases cost | Verification | Approve minimum matrix approach |
| NOS-FD11 | Mobile test-device requirements? | Founder-approved owned test devices with synthetic data, encryption inspection, low-storage and loss drills | Personal/customer devices are prohibited; cloud farms add vendor boundary | Privacy/device | Approve acquisition/use boundary later |
| NOS-FD12 | P2 closure timing? | Close each only at its named evidence gate; none at plan approval | Batch closure at Phase 6 weakens blocking traceability | Governance | Approve item-by-item closure policy |
| NOS-FD13 | Implementation lock criteria? | P0/P1 zero, all phase evidence reproducible, rollback proven, flags disabled, P2 accurately closed/retained, independent review | Lock with open evidence would overclaim readiness | Governance/security | Approve criteria |
| NOS-FD14 | First future authorization? | Authorize Phase 0 baseline only after these decisions | Direct Phase 1/3 authority skips preflight | Governance | Issue separate Phase 0 directive or return plan |

No default answer is inferred from silence.
