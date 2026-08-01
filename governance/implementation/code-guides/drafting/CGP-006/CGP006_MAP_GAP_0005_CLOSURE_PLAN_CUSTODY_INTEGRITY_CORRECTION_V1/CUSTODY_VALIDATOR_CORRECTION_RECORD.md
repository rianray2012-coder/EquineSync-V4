# Custody Validator Correction Record

The custody validator was hardened to:

- execute the corrected accession validator as a mandatory dependency;
- independently verify the approved ZIP from the committed Git object;
- enforce accession placeholder prohibitions in the accession tree;
- require boundary tokens in explicit authoritative custody governance files;
- reject validator, test, manifest, checksum, filename, and diagnostic-output token self-satisfaction;
- reject unauthorized provider-assurance or production-readiness claims;
- validate source identity rows from Git objects; and
- enforce correction-scoped authorized paths.

This validator no longer relies on a subset of accession controls.
