# W1-RF01 Security Findings Register

## P1 Findings

| ID | Evidence and failure path | Consequence | Required control |
| --- | --- | --- | --- |
| `W1RF01-P1-06` | `/auth/signup` accepts `trainer`, `barn_owner`, and `service_provider`, issues a session, while central capabilities inspect `role` and not `role_status` | Self-selected operational authority may reach role-gated data or actions before review | Enforce pending-review restrictions server-side; separate enrollment intent from granted authority |
| `W1RF01-P1-07` | `routes/auth.py` and `core/auth.py` duplicate JWT/password/current-user logic and different routes use different dependencies | Security fixes can land in one path and not the other | One canonical auth service/dependency with parity regression tests |
| `W1RF01-P1-08` | Refresh validation reads an unrevoked row, then revocation occurs in a later operation | Concurrent replay can pass validation more than once | Atomic consume-and-rotate with token family/reuse detection |
| `W1RF01-P1-09` | Most routes authorize from `users.role/barn_id`; membership-aware context is read-only and limited | Multi-membership authority can diverge from selected context and historical relationships | Governed active-context enforcement and access-delta tests |

## P2 Findings

| ID | Observation | Treatment |
| --- | --- | --- |
| `W1RF01-P2-04` | Email verification enforcement defaults off | Founder-approved assurance policy before production identity hardening |
| `W1RF01-P2-05` | Access and refresh tokens are stored in browser localStorage; CSP permits unsafe inline/eval | Evaluate HttpOnly/SameSite session design and tighten CSP in a separate runtime RF |
| `W1RF01-P2-06` | Minimum password rule is length eight; MFA, device sessions, and risk-based recovery are absent | Assurance roadmap, not provider activation |
| `W1RF01-P2-07` | Audit is deliberately fail-open and identity-event coverage is incomplete | Durable outbox/health/coverage design under Audit and Platform Operations governance |

P0 findings: `0`. Immediate emergency containment is not required. All P1 controls require separate runtime authority.

