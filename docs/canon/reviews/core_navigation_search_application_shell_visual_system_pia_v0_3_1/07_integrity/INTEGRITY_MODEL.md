# Package Integrity Model

**Model ID:** `ES-PKG-INTEGRITY-NONCIRCULAR-V1.0`  
**Applies to:** `EquineSync_Core_Navigation_Visual_System_Founder_Approved_Content_V0_3_2_Technical_Correction`

## Verification Layers

### Layer 1: Outer archive

The sidecar `.zip.sha256` verifies the entire ZIP byte stream. This layer binds every archived byte, including `CHECKSUMS.sha256` and `PACKAGE_MANIFEST.csv`.

### Layer 2: Internal checksum ledger

`CHECKSUMS.sha256` verifies every extracted package file except:

- `07_integrity/CHECKSUMS.sha256`
- `07_integrity/PACKAGE_MANIFEST.csv`

Those two exclusions prevent circular and self-referential hashes.

### Layer 3: Full inventory manifest

`PACKAGE_MANIFEST.csv` lists every extracted file, including both integrity-control files.

- Ordinary files are verified by the checksum ledger, manifest metadata, and outer archive hash.
- `CHECKSUMS.sha256` is verified by its exact hash in the manifest and by the outer archive hash.
- `PACKAGE_MANIFEST.csv` uses `SELF_REFERENCE_EXCLUDED` for its own SHA-256 field and is verified by the outer archive hash.

## Required Count Relationship

- `actual_extracted_file_count == package_manifest_data_rows`
- `checksum_ledger_lines == actual_extracted_file_count - 2`
- The two ledger exclusions must be exactly the checksum ledger and package manifest.

Any other omission, extra file, path mismatch, size mismatch, or hash mismatch is a blocking integrity failure.
