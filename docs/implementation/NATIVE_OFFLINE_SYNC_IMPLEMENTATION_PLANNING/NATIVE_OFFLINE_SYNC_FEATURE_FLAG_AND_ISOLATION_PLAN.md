# Native Offline Synchronization Feature Flag and Isolation Plan

These proposed names are planning contracts only; no environment or manifest is
changed.

## Control Layers

| Control | Proposed default | Purpose |
| --- | --- | --- |
| `NATIVE_OFFLINE_IMPLEMENTATION_ALLOWED` | `false` | Top-level server/build authorization; false outside an approved harness. |
| `NATIVE_OFFLINE_TEST_ENVIRONMENT` | unset | Must equal a named synthetic environment and reject production-like hosts/credentials. |
| `NATIVE_OFFLINE_LOCAL_STORE_ENABLED` | `false` | Enables only the approved adapter. |
| `NATIVE_OFFLINE_OUTBOX_ENABLED` | `false` | Enables local operation creation; cannot imply replay. |
| `NATIVE_OFFLINE_REPLAY_ENABLED` | `false` | Enables foreground replay only in a separately approved phase. |
| `NATIVE_OFFLINE_TASKS_ENABLED` | `false` | Gates task slice independently. |
| `NATIVE_OFFLINE_QUICKADD_DRAFTS_ENABLED` | `false` | Gates scoped draft behavior independently. |
| `NATIVE_OFFLINE_CONFLICT_UI_ENABLED` | `false` | Gates conflict/recovery surface independently. |
| `NATIVE_OFFLINE_ATTACHMENTS_ENABLED` | `false` | Remains false for first slice. |
| `NATIVE_OFFLINE_BACKGROUND_ENABLED` | `false` | Remains false; no background worker authority. |

## Evaluation Rules

All required controls must be true at build and runtime, the environment must be
allowlisted, data must be synthetic, the actor/barn must be approved, and the
requested capability must be individually enabled. Missing, malformed, unknown,
or contradictory configuration fails closed to current online-first behavior.

The server independently rejects sync routes unless its top-level test control
and environment classification pass. A frontend flag cannot activate a backend
route. Production builds include a policy test proving all controls false.

## Isolation

- Separate local database namespace and keys for the experiment.
- No reads from or writes to production/staging stores.
- No provider SDK, webhook, email, SMS, push, Calendar mutation, or external URL.
- No production credentials; startup rejects production-like credential shapes.
- No service worker or background scheduler registration.
- Synthetic personas and barns only; unsupported users see current behavior.
- Egress controls and local endpoint allowlist apply to test harnesses.

## Disable and Removal

Disable order: replay, workflow flags, outbox, conflict UI, then store creation.
Existing unsynced evidence is exported or quarantined under test policy before
store deletion. Removal deletes flags, adapters, routes, test data, and local
stores only after manifest-backed verification; canonical server records are not
rolled back by deleting local state.

## Accidental Activation Tests

Test absent flags, partial flags, production environment, production-like URL,
credential presence, unknown barn/user, unsupported build, route probing,
worker registration, and second activation. Every case must return disabled or
not found and produce no store, route effect, network call, or mutation.
