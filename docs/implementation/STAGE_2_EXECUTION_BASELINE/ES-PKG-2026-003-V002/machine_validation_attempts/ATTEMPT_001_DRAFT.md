# Machine Validation Attempt 001 - Draft

- Phase: `draft`
- Result: `FAIL`
- Score: `27/29`
- Package files observed: `66`
- Required draft outputs: `66/66`
- Application execution: `NOT_PERFORMED`

Two checks failed:

1. `no_unresolved_placeholders`
2. `no_secret_values`

Root cause: the content scanner included `validate_successor_package.py`, so the validator's own detection-pattern literals triggered both checks. No package document, JSON record, CSV record, or checksum contained the detected value. Corrective action: exclude only the validator source file from content-value scanning while continuing to include it in path, manifest, checksum, syntax, and inventory controls.

This failed attempt is retained as required validation history.
