# Reproducibility of the Tier 1 Package Validation

Authority boundary: `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

## What Finding F-28 Recorded

Revision Round 2 recorded a single validation run on a single host (`macOS-26.5.2-arm64`, Python 3.14.6, working directory `/tmp/tier1_rr2_standalone.04VWbt`). The run was unsigned and had never been reproduced. A validation result produced once, by the party who wrote both the package and the validator, on that party's own machine, is not independent evidence that the package validates.

## What Round 3 Part B Adds

- `VALIDATION/Containerfile`, a pinned container definition, so the interpreter and the operating system are fixed rather than inherited from whatever host runs the check.
- `VALIDATION/reproduce.sh`, which runs the self-test and the validator and prints an attestation row. The script deliberately does not append its own row: a party attesting to a result must add the row themselves.
- `VALIDATION/INDEPENDENT_REPRODUCTION_ATTESTATIONS.csv`, one row per run, recording host, architecture, interpreter, result, the integrity-root hash the run applies to, who ran it, and whether the run is independent.

## Current Attestation State

See `VALIDATION/INDEPENDENT_REPRODUCTION_ATTESTATIONS.csv`. `T1-ATTEST-001` is the Revision Round 2 run on macOS under Python 3.14.6. `T1-ATTEST-002` is a second run on `Linux-6.1.155+-x86_64-with-glibc2.43` under Python 3.14.3, a different operating system, architecture and interpreter version, performed after the Round 3 Part B manifests and integrity root were rebuilt.

Both rows carry `independence_state` values beginning `NOT_INDEPENDENT`, because both were run by the package preparer. Reproducing a result on a second machine demonstrates that the result does not depend on one host; it does not demonstrate independence. Independence requires a party with no role in preparing the package, and no such party has run this validator.

## Signing

`signature_state` is `NOT_SIGNED_NO_SIGNING_KEY_PROVISIONED` on every row, and `external_attestation_state` in `00_PROGRAM_CONTROL/ROUND_3_INTEGRITY_ROOT.json` remains `NOT_ATTESTED`. Signing the integrity root requires a key held by a named party under a stated key-management practice. No key has been provisioned, no such practice has been written, and none is asserted here.

The container base image in `VALIDATION/Containerfile` carries the placeholder digest `PIN_NOT_RECORDED_SEE_REPRODUCIBILITY_MD` rather than a real digest, because pinning to a digest that has not been fetched and verified would be a fabricated pin. The digest must be filled in by whoever first builds the image, and recorded here with the date it was fetched.

## Status

`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`
