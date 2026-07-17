# Native Offline Synchronization Observability and Support Plan

## Required User-Facing State

Show pending mutation count, failed/rejected count, conflict count, last attempted
sync, last successful canonical confirmation, online/offline/reconciling status,
and actionable recovery guidance. Never display canonical success from local
acceptance alone.

## Allowlisted Telemetry

- state transition and sanitized reason code;
- operation type/class, not payload;
- local/canonical correlation IDs and hashes;
- app, protocol, local schema, projection, and policy versions;
- retry count, latency bucket, queue depth, conflict count;
- device pseudonymous ID plus actor/barn scope references only where authorized;
- storage/quota health and last successful/attempted synchronization times;
- flag/environment classification and cleanup result.

Ordinary logs exclude tokens, keys, raw payloads, horse/owner names, medical
fields, guardian/minor data, financial data, provider-private data, agreements,
contact details, and unrestricted identifiers.

## Diagnostic Bundle

User-initiated and scope-bound bundle: manifest, versions, platform/build, flag
state, queue counts by state/type, redacted transition timeline, sanitized error
codes, dependency/conflict graph using pseudonymous IDs, payload hashes, storage
integrity result, connectivity summary, and reproduction consent. It is encrypted
for approved transfer and expires under the future retention schedule.

Raw queue export is disabled by default. Support can inspect summaries but cannot
replay, rewrite, resolve, or discard operations without a separately approved,
least-privilege, audited action. `NOS-P2-07` remains open until this authority and
retention contract is Founder-approved.

## Recovery and Escalation

Users receive specific guidance for reconnect, reauthenticate, update app,
resolve conflict, free storage, retry, preserve the device for support, or safely
discard a permitted draft. Escalation routes to product support, security/privacy,
or domain safety based on reason code. Medication, emergency, incident, location,
transfer, permission, financial, and agreement events never use ordinary task
support as a substitute for qualified escalation.

## Operational Alerts

Future alerts cover queue age/depth, repeated retry blocks, corruption, duplicate
hash mismatch, cross-scope denial, schema mismatch, conflict rate, purge failure,
and accidental activation attempts. Thresholds remain open under `NOS-P2-06`.
