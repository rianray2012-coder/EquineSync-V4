# Phase 1 Evidence Custody Report

## Identity and sources

- Authoritative predecessor: `75c56ac67b0de694436c093fc2dc5ff5dffe4ff3`
- Current Founder directive SHA-256: `da245bd5e051564e62dbc25dfad00f0f546ab4738425f5970369e4e9ab1af328`
- Framework: Founder-Orchestrated Review Agent Framework V1.3, configuration package V1.0.0
- Role profiles: eight entries in `profiles/PROFILE_MANIFEST.json`

All prior framework, calibration, installation, activation, runtime-remediation, runtime-requalification, failed canary, generic-fallback, and fallback-authorization artifacts remain unchanged. Phase 1 additions are confined to `governance/founder_orchestrated_review/phase1/V1.0.0/`.

## Preserved failures and retries

- Pilot packet-preparation attempt 01: failed cross-role canary containment; preserved.
- Pilot packet-preparation attempt 02: corrected retry with predecessor, reason, changed conditions, and unchanged conditions; preserved separately.
- Validation run 01: failed filename validator rule plus blocked Pilot execution; preserved.
- Validation run 02: separate retry correcting only the filename rule; preserved.
- Validation run 03: failed post-assembly revalidation because the filename checker treated the new profile manifest as a role profile; preserved separately.
- Validation run 04: separate retry changing only that filename-check scope; preserved as the final post-assembly run.
- Push attempt 01: rejected by GitHub push protection because the deliberately Stripe-shaped simulated test value matched a secret rule; no remote branch was created; preserved under `evidence/delivery/`.
- Validation run 05: post-remediation run after replacing the test value with a non-key-shaped synthetic marker and strengthening the secret scanner; preserved separately.
- Four permission records: failed closed before spawn; preserved; no role output exists.

## Deterministic custody outputs

`PACKAGE_MANIFEST.json` records relative path, byte count, and SHA-256 for the static Phase 1 package scope. `PACKAGE_SHA256SUMS.txt` provides the corresponding register. `profiles/PROFILE_MANIFEST.json` and `profiles/PROFILE_FILES.sha256` identify role-source hashes, payload checksums, and profile-file hashes. The ZIP and sidecar under `packages/` are generated locally and archive parity is rechecked by `scripts/phase1_validate.py`.

The package manifest intentionally excludes its own bytes, checksum register, ZIP self-references, change manifest, and validation run logs to avoid recursive hashes. Validation run directories are separately immutable by run ID and are never reused.

## Custody limitations

Filesystem permissions alone do not prove organizational immutability. Git commit and remote publication provide versioned preservation after delivery, not external custody. No provider-hosted trace, external assurance, or independent human custody is claimed.
