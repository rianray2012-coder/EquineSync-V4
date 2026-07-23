# EquineSync Core Navigation Visual-System Package Technical Correction Record

**Correction ID:** `ES-NAV-VISUAL-PKG-CORR-2026-07-22-01`  
**Correction package:** `V0.3.2`  
**Approved PIA content version:** `V0.3.1`  
**Correction class:** `INTEGRITY_CONTROL_ONLY`  
**Substantive PIA change:** `FALSE`  
**Founder disposition changed:** `FALSE`  
**Implementation authority:** `FALSE`  
**Deployment authority:** `FALSE`  
**Production authority:** `FALSE`  
**Enrollment authority:** `FALSE`

## 1. Trigger

Codex stopped fail-closed before repository mutation because the V0.3.1 archive contained 25 files while `PACKAGE_MANIFEST.csv` contained 24 data rows and omitted itself. The manifest also recorded a stale SHA-256 value for `CHECKSUMS.sha256`.

## 2. Correction

This package preserves the Founder-approved PIA V0.3.1, founder records, reference assets, historical drafts, and review evidence without substantive modification. It makes only the following technical corrections:

1. preserves the fail-closed stop receipt as review evidence;
2. preserves the superseded Codex directive V1.0.0 as historical evidence;
3. replaces the active directive with V1.0.1;
4. defines a non-circular three-layer integrity model;
5. rebuilds `CHECKSUMS.sha256` over every package file except the checksum ledger and package manifest;
6. rebuilds `PACKAGE_MANIFEST.csv` so it lists the complete extracted inventory, including itself and the checksum ledger;
7. records the actual checksum-ledger hash in the manifest;
8. marks the package-manifest self-hash as `SELF_REFERENCE_EXCLUDED` and binds that control file through the outer archive SHA-256; and
9. updates package metadata, README, counts, and validation instructions.

## 3. Non-Circular Integrity Rule

- The outer archive SHA-256 verifies the complete ZIP byte stream, including both internal integrity-control files.
- `07_integrity/CHECKSUMS.sha256` verifies every extracted file except itself and `07_integrity/PACKAGE_MANIFEST.csv`.
- `07_integrity/PACKAGE_MANIFEST.csv` lists every extracted file and records the actual checksum-ledger hash.
- The manifest's own hash is intentionally not embedded within itself because that would create an impossible self-reference. Its row uses `SELF_REFERENCE_EXCLUDED` and is verified by the matching outer archive SHA-256.

## 4. Authority Boundary

This correction does not authorize source-code changes, schema changes, UI implementation, font installation, icon export, app-store submission, Stead activation, deployment, production use, pilot enrollment, or first-user enrollment.
