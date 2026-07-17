# Native Offline Sync Platform Implementation Strategy

## Shared Core

Implement future synchronization as a standalone TypeScript domain package shared by web and Capacitor. It owns operation envelopes, state transitions, schema validation, dependency ordering, idempotency, checkpoints, conflict outcomes, projection metadata, and sanitized telemetry. It must not own platform keys or bypass server authorization.

## Browser/PWA

- IndexedDB is the recommended durable adapter; `localStorage` is insufficient for a general outbox or sensitive cache.
- A service worker may cache the static shell and explicitly approved public/static assets only in its first phase.
- Business-data caching and background sync require separate security and browser-support approval.
- Browser limitations in key protection, eviction, private mode, quota, and background execution require reduced sensitive capability compared with native.
- Unsupported browsers fall back to current online-first behavior, not degraded unsafe storage.

## iOS and Android

- Use a versioned SQLite-compatible native database adapter with encryption.
- Store wrapping keys and device registration material in Keychain/Keystore.
- Treat OS background execution as opportunistic; foreground synchronization is the reliability baseline.
- Use platform connectivity signals only as hints. Successful authenticated requests establish actual connectivity.
- Account for app suspension, force quit, low-power modes, storage pressure, reinstall, backup restore, and device clock changes.

No native plugin, database vendor, or background scheduler is selected or approved by this package.

## Attachments and Rural Connectivity

- Hash and encrypt staged files.
- Upload in resumable bounded chunks with per-chunk and whole-object verification.
- Support pause, retry, explicit cellular policy, and user-visible pending state.
- Prioritize small safety events before large media.
- Never block text incident capture on media upload.

## Compatibility

The client advertises schema and protocol versions. The server returns minimum supported versions and migration requirements. Incompatible clients become read-only or online-only; they do not guess at new schemas.

## Observability and Support

User-visible status includes pending, syncing, conflict, blocked, failed, and last canonical sync. A sanitized diagnostic bundle may include app/protocol/schema versions, device pseudonym, counts, checkpoints, reason codes, retry ages, and hashes, but no tokens or record payloads.

Administrative support tools are read-only by default and permission scoped. Any queue repair or forced resolution requires a separate audited action and cannot rewrite authorship.

## Recommended Implementation Order

1. Shared envelope/state-machine library and synthetic in-memory adapter.
2. Server protocol and permission/conflict contract behind default-off controls.
3. Native encrypted store and device lifecycle tests.
4. Browser IndexedDB adapter for non-sensitive pilot scope.
5. Read-only projections.
6. Low-risk task mutations.
7. Inventory delta and maintenance pilots.
8. Safety-critical workflows only after domain and clinical governance approval.
9. Attachments and optional platform background scheduling last.

