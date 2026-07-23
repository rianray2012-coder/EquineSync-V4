# Integrity Model

This package uses a non-circular three-layer model:

1. The outer ZIP is bound by a SHA-256 sidecar generated after archive creation.
2. `CHECKSUMS.sha256` binds every payload file except the two integrity-control files.
3. `PACKAGE_MANIFEST.csv` inventories every regular file. The manifest and checksum ledger are marked as integrity-control files and are bound by the outer ZIP hash rather than attempting impossible self-hashing.

The approved visual-system component is not included as recreated bytes. Its exact filename and expected SHA-256 are bound by the component lock and must be verified at controlled repository assembly.
