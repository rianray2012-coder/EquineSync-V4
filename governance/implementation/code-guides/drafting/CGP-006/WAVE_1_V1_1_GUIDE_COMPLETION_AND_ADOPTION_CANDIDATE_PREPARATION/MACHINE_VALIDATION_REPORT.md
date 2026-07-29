# Machine Validation Report

**Validator:** `validators/validate_guide_completion_adoption_candidate.py`
**Test suite:** `tests/test_guide_completion_adoption_candidate.py`
**Reliability state:** `PACKAGE_LOCAL_SHADOW_VALIDATION`
**Validator result:** `PASS`
**Unit-test result:** `OK`
**Negative-test result:** `PASS`
**git diff --check result:** `PASS`

The package-local validator identifies required inputs, parses JSON and CSV, checks controlled values, unique identifiers, cross references, adoption and activation boundaries, prohibited implementation mappings, evidence grades, assurance classes, manifests, checksums, historical-byte preservation, frozen-source preservation, and authorized changed paths. It returns nonzero on failure and supports `--json` output.

The unit tests exercise positive validation and required negative fixtures for missing file, malformed CSV, malformed JSON, duplicate ID, invalid controlled value, incomplete question, prohibited implementation mapping, false adoption, false activation, unsupported evidence grade, broken reference, checksum failure, and unauthorized path.
