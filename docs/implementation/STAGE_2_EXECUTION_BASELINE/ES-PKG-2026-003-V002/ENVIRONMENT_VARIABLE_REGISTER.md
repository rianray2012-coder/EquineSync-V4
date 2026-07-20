# Environment Variable Register

- Package: `ES-PKG-2026-003-V002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| Name | Class | Boundary | Source | Status |
|---|---|---|---|---|
| APP_ENV | configuration | Required environment identity; exact allowed Stage 2 value UNKNOWN | docs/ONBOARDING_GUIDE.md | REQUIRED_UNKNOWN_VALUE |
| MONGO_URL | secret_or_sensitive_locator | Disposable non-production database only; value prohibited | backend/core/config.py | REQUIRED_NAME_ONLY |
| DB_NAME | configuration | Unique synthetic database name; exact value UNKNOWN | backend/core/config.py | REQUIRED_UNKNOWN_VALUE |
| JWT_SECRET | secret | Synthetic non-production secret; value prohibited | backend/core/config.py | REQUIRED_NAME_ONLY |
| CORS_ORIGINS | configuration | Localhost-only future profile; exact committed value absent | backend/core/config.py | REQUIRED_UNKNOWN_VALUE |
| REACT_APP_BACKEND_URL | configuration | Local API endpoint; exact approved value absent | frontend source and README | REQUIRED_UNKNOWN_VALUE |
| ALLOW_AUTO_SEED | safety_control | Must not enable unbounded/demo mutations; approved value contract absent | backend/core/lifespan.py | BLOCKING_DECISION |
| DISABLE_TASK_MATERIALIZER | safety_control | Future isolated profile must disable or explicitly bound task materialization | backend/core/lifespan.py | BLOCKING_DECISION |
| DISABLE_NOTIFICATIONS | safety_control | Future profile must prevent external notification activity | backend/core/lifespan.py | BLOCKING_DECISION |
| DISABLE_OWNER_DIGEST | safety_control | Future profile must disable background provider activity | backend/core/lifespan.py | BLOCKING_DECISION |
| DISABLE_OWNER_WEEKLY_RECAP | safety_control | Future profile must disable background provider activity | backend/core/lifespan.py | BLOCKING_DECISION |
| DISABLE_AUTO_NUDGES | safety_control | Future profile must disable background provider activity | backend/core/lifespan.py | BLOCKING_DECISION |
| DISABLE_SUBSCRIPTION_EMAIL_DISPATCHER | safety_control | Future profile must disable email dispatch | backend/core/lifespan.py | BLOCKING_DECISION |
| ENFORCE_EMAIL_VERIFICATION | security_control | Exact isolated-run value requires approval | backend/core/config.py | REQUIRED_UNKNOWN_VALUE |
| RATE_LIMIT_ENABLED | security_control | Exact isolated-run value requires approval | backend/core/config.py | REQUIRED_UNKNOWN_VALUE |
| AUTH_RATE_LIMIT | security_control | Exact value UNKNOWN | backend/core/config.py | UNKNOWN |
| LOGIN_LOCKOUT_ENABLED | security_control | Exact value UNKNOWN | backend/core/config.py | UNKNOWN |
| LOGIN_MAX_ATTEMPTS | security_control | Exact value UNKNOWN | backend/core/config.py | UNKNOWN |
| LOGIN_LOCKOUT_MINUTES | security_control | Exact value UNKNOWN | backend/core/config.py | UNKNOWN |
| LOGIN_ATTEMPT_WINDOW_MINUTES | security_control | Exact value UNKNOWN | backend/core/config.py | UNKNOWN |
| EMAIL_VERIFY_TTL_HOURS | security_control | Exact value UNKNOWN | backend/core/config.py | UNKNOWN |
| PASSWORD_RESET_TTL_HOURS | security_control | Exact value UNKNOWN | backend/core/config.py | UNKNOWN |
| JWT_EXP_HOURS | security_control | Repository default exists; approved Stage 2 value UNKNOWN | backend/core/config.py | UNKNOWN |
| REFRESH_EXP_DAYS | security_control | Repository default exists; approved Stage 2 value UNKNOWN | backend/core/config.py | UNKNOWN |
| STRIPE_API_KEY | prohibited_secret | Payment processing prohibited | provider configuration | PROHIBITED |
| STRIPE_SECRET_KEY | prohibited_secret | Payment processing prohibited | provider configuration | PROHIBITED |
| STRIPE_WEBHOOK_SECRET | prohibited_secret | Payment processing prohibited | provider configuration | PROHIBITED |
| RESEND_API_KEY | prohibited_secret | External email/provider interaction prohibited | provider configuration | PROHIBITED |
| DOCUSIGN_* | prohibited_secret_family | Provider interaction prohibited | provider configuration | PROHIBITED |
| AWS_* / object-storage credentials | prohibited_secret_family | External storage interaction prohibited | provider configuration | PROHIBITED |
| AI/provider API keys | prohibited_secret_family | External AI/provider interaction prohibited | provider configuration | PROHIBITED |

Secret values are prohibited. Wildcard families identify names/categories only.
