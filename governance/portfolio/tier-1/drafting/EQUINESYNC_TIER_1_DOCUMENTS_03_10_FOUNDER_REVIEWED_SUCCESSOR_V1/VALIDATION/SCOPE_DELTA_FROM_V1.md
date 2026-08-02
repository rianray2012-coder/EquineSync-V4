# Scope Delta from V1 to Revision Round 2 and Round 3

Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

## Why This Record Exists

Finding F-16 of the external standards benchmark review recorded that the V1 package shipped `validators/validate_document_0N.py` and `tests/test_document_0N.py` for each of Documents 03 to 10, sixteen files in total, and that Revision Round 2 shipped one package-level validator and no tests without disclosing the removal anywhere in the package. A reduction in verification scope that is discoverable only by diffing two packages is not a disclosed reduction. This record discloses it.

## Files Removed

| V1 path | V1 SHA-256 | V1 byte length |
|---|---|---|
| `03_IMPLEMENTATION_TRACEABILITY/tests/test_document_03.py` | `ab96e085153fa1437e14d7ac7a831f617c92604f74954b6171cc46f378397bfb` | 540 |
| `03_IMPLEMENTATION_TRACEABILITY/validators/validate_document_03.py` | `6b2e46214b629164fefeba4ef6e126e256bd82656df2468ed0975e9eb5e2ea51` | 2413 |
| `04_AUTHORITY_LIFECYCLE_REGISTER/tests/test_document_04.py` | `26271f3748f1831d85ac1e409b1ec60b829365d3c6ee263e29c5786436bdd5bb` | 540 |
| `04_AUTHORITY_LIFECYCLE_REGISTER/validators/validate_document_04.py` | `cb92316bc042a645ba656c96f529926d149fa25a10b12488bae5545f7aabbc6f` | 2180 |
| `05_FOUNDER_DECISION_REGISTER/tests/test_document_05.py` | `1ddf3141a813ea7a5baa9a38535b188cd8717eeb921d8065fcb41ceef7b3d380` | 540 |
| `05_FOUNDER_DECISION_REGISTER/validators/validate_document_05.py` | `e8439d40fe2cfe477fd834cd5015b6d6af38e7ea2a15906ca94a826af4cdf80b` | 2128 |
| `06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/tests/test_document_06.py` | `a2aafd6dc05502fbd5a26789dff565676f122d94b76e9d8658d67529719fb892` | 540 |
| `06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/validators/validate_document_06.py` | `e2b82e95e6afe53c86e2755e5dd0c1af3e37ca75a974f9e3685e6af6ac974bff` | 2189 |
| `07_OWNERSHIP_STEWARDSHIP_REVIEW/tests/test_document_07.py` | `af0c751f963b137dbd74c1085b8c92f8562a7145141aa4dd824fe6980f105666` | 540 |
| `07_OWNERSHIP_STEWARDSHIP_REVIEW/validators/validate_document_07.py` | `fe4ea9ced4ba50bc54d661c1c09be259fb887dc95f514090f9dfc08079c78b4b` | 2122 |
| `08_SOURCE_RECONCILIATION/tests/test_document_08.py` | `aeb4ccde852cdfb0d5a7942c817d9f7e577cfd85e1fda94c39307f42e75f659d` | 540 |
| `08_SOURCE_RECONCILIATION/validators/validate_document_08.py` | `9f4b5efbe50329d76c558c06a80fff6e5726c6f6c7afcdca27302d1643dd4ca8` | 2180 |
| `09_WORKSTREAM_PR_BRANCH_DISPOSITION/tests/test_document_09.py` | `69719d9fe5a9ca63956376f01694829d3c02344cb103506e1a1ca7f74f8e4925` | 540 |
| `09_WORKSTREAM_PR_BRANCH_DISPOSITION/validators/validate_document_09.py` | `181ecfb26f1b9ed345c2c4b7965faf7bd75dc82090ea37e9dec37e2472ad4e64` | 2175 |
| `10_CLOSING_AUDIT_PROTOCOL/tests/test_document_10.py` | `298630ae1f6599af4413d5a1dc6365791def2c7c01c549b245a0c1e63bc87525` | 540 |
| `10_CLOSING_AUDIT_PROTOCOL/validators/validate_document_10.py` | `48e8c225119a7bc2832f83c8a8a6884f8b0bcf8f8477066a2b51a22414638b45` | 2088 |

The hashes above were computed from the V1 source package `EQUINESYNC_TIER_1_DOCUMENTS_03_10_V1`. They allow any reader to confirm the removed files independently.

## What The Removed Files Checked

Each `validate_document_0N.py` performed four checks scoped to its own document directory: (a) every filename in a hard-coded required-file list exists; (b) every `.csv` file in the directory parses as CSV; (c) every `.json` file parses as JSON; (d) no file of type `.md`, `.csv`, `.json` or `.py` contains a placeholder marker. Each `test_document_0N.py` invoked the corresponding validator as a subprocess and asserted a zero exit code and the presence of the string `DOCUMENT_0N_VALIDATION_PASS` in standard output.

## Where That Coverage Now Lives

| V1 check | Round 3 Part B replacement | Check name in the package validator |
|---|---|---|
| Required files exist, per document | Retained and widened to the whole package | `required_file:<path>` and `per_document_required_files` |
| CSV and JSON parse | Retained and widened to every parseable file in the package | `parse_integrity` |
| Placeholder marker scan | Retained and widened to the whole package | `placeholder_marker_scan` |
| Validator invoked by a test that asserts it passes | Replaced by `--self-test`, which drives each failure-capable check with synthetic violating data and asserts the check returns FAIL | `--self-test` |

The V1 test files asserted only that the validator passed. A test that asserts a validator passes on data the validator was written against cannot detect a validator that is incapable of failing. `--self-test` asserts the opposite property and is the stronger control; it is not, however, a restoration of per-document scoping, which is recorded below as an accepted reduction.

## Reductions Not Restored

- Per-document scoping. The Round 3 validator reports one package-level result per check rather than one result per document. A failure in Document 07 and a failure in Document 09 are reported by the same check name. This is a real reduction in diagnostic resolution relative to V1 and is not restored in Round 3 Part B.
- Independent test invocation. V1 could be exercised with a test runner over sixteen discoverable test files. Round 3 exposes one `--self-test` flag. Coverage measurement tools that discover tests by filename will find nothing in this package.

## Status

`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`
