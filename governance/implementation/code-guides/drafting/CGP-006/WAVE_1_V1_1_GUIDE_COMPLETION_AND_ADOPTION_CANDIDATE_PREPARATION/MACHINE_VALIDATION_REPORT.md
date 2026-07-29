# Machine Validation Report

**Validator:** `validators/validate_guide_completion_adoption_candidate.py`
**Test suite:** `tests/test_guide_completion_adoption_candidate.py`
**Reliability state:** `PACKAGE_LOCAL_SHADOW_VALIDATION`
**Validator result:** `PASS`
**Unit-test result:** `OK`
**Negative-test result:** `24 tests passed, including required Stage 22 negative tests`
**Global validator result:** `PASS`
**git diff --check result:** `PASS`

The package-local validator identifies required Stage 21 and Stage 22 inputs, parses JSON and CSV, checks controlled values, unique identifiers, cross references, adoption and activation boundaries, prohibited implementation mappings, exact reviewed guide byte identity, Stage 22 adoption rows, retained findings, evidence grades, assurance classes, manifests, checksums, historical PR #42 preservation, frozen-source preservation, current-status consistency, custody-claim safety, and authorized changed paths. It returns nonzero on failure and supports `--json` output.

The unit tests exercise positive validation and required negative checks for missing file, malformed CSV, malformed JSON, duplicate ID, invalid controlled value, incomplete question, prohibited implementation mapping, unreviewed hash, changed adopted bytes, active guide state, activation date, warning closure, GAP-0004 closure, Stage 22 row missing Founder disposition, premature custody claim, custody receipt missing merge metadata, historical PR #42 rewrite, implementation claim, runtime evidence claim, unsupported evidence grade, broken reference, checksum failure, and unauthorized path.
