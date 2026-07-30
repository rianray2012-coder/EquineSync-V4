# Validation Report

## Package Validation Result

`PASS` after PR #62 Copilot reconciliation.

Commands run from repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/drafting/CGP-006/REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AND_CURRENT_STATE_GAP_AUDIT_V1/validators/validate_repository_mapping_gap_audit.py
```

Expected validator result after this reconciliation:

```json
{
  "status": "PASS",
  "mandatory_artifacts": 32,
  "mapping_rows": 22,
  "gap_rows": 18,
  "finding_rows": 16,
  "cited_file_identities": 100,
  "copilot_disposition_rows": 10
}
```

## Package Test Result

`PASS` expected after reconciliation with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 governance/implementation/code-guides/drafting/CGP-006/REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AND_CURRENT_STATE_GAP_AUDIT_V1/tests/test_repository_mapping_gap_audit.py
```

## PR #62 Copilot Source Validation

- Outer ZIP SHA-256: `67a50c31e9a4c529339b6ba06c3317e486dd015f7bafe1be0910257db6cd70cf`.
- Outer ZIP byte length: `14762`.
- Embedded Copilot source SHA-256: `cd6e1315615d0f65664485d4ebc2f8906ff4e1f9c0bd19f3b7a6765da026386b`.
- Embedded Copilot source byte length: `12416`.
- Embedded directive SHA-256: `2e58dc1f0d0b4c3f8aaaa60b4a89b4368fb18e3a014ac41cbebabfe9b64d031f`.
- Embedded directive byte length: `14297`.

## Copilot Reconciliation Validation

- Disposition rows: `10`.
- Classification totals: `{"CONTEXT_DEPENDENT_REQUIRES_FOUNDER_DECISION": 1, "DUPLICATE_OF_OTHER_FINDING": 1, "REJECTED_AS_DEFECT_WITH_RECORDED_RATIONALE": 1, "UNVERIFIED_RISK_REQUIRES_EVIDENCE": 1, "VALID_MAINTAINABILITY_OBSERVATION": 1, "VALID_NEW_GAP": 3, "VALID_PARTIALLY_CAPTURED_REQUIRES_EXPANSION": 1, "VALID_REPOSITORY_POLICY_DECISION_REQUIRED": 1}`.
- New gaps: `6`.
- Expanded gaps: `1` (`CGP006-MAP-GAP-0011`).
- Duplicate findings not double-counted: `1`.
- Unverified risks not presented as confirmed defects: `1`.
- Rejected findings retained with rationale: `1`.
- Candidate IWPs after reconciliation: `15`.

## JSON And CSV Parse Results

`PASS`: all package-local JSON and CSV artifacts parse.

## Checksum Result

`PASS`: `CHECKSUM_MANIFEST.sha256` validates all listed package files after refresh.

## Authorized Path Result

`PASS`: current reconciliation writes are confined to `governance/implementation/code-guides/drafting/CGP-006/REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AND_CURRENT_STATE_GAP_AUDIT_V1/`.

## git diff --check Result

`PASS`: `git diff --check 1ad6fa436c31316ee192844106ca748cd6dc6d0b HEAD` produced no output after applying the package-local `.gitattributes` custody exception for the exact Copilot source file. The Copilot source bytes remain unchanged.

## Existing Governance / Stage 24 Validation

Applicable existing custody/status tests remain applicable and should pass after reconciliation:

```bash
python3 -m unittest governance/implementation/code-guides/validation/tests/test_wave1_current_status_custody_table.py -q
python3 -m unittest governance/implementation/code-guides/validation/tests/test_validate_activation_records.py -q
```

## Limitations

- No Copilot recommendation, command, or remediation was executed.
- No root README, license, product code, dependency manifest, lockfile, CI workflow, schema, migration, deployment configuration, staging, pilot, or production system was modified.
- No package-manager install/audit command, linter, formatter, typechecker, SAST, dependency audit, secret scan, CodeQL, Dependabot, Docker, deployment, or external-tool setup command was run.
- Repository evidence is static/documentary evidence, not runtime or external-tool evidence.
