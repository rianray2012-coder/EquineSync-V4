# Code Guide Validation

Validators are deterministic Python entrypoints with no network access and no repository mutations.

## Invocation

Run all validation:

```bash
python3 governance/implementation/code-guides/validation/run_all_validations.py
```

Run a single validator:

```bash
python3 governance/implementation/code-guides/validation/validate_control_registry.py --json
```

Run the CGP-003 source-accession validator:

```bash
python3 governance/implementation/code-guides/validation/validate_source_accession.py --json
```

Run the CGP-005 source-freeze validators:

```bash
python3 governance/implementation/code-guides/validation/validate_source_freeze.py --json
python3 governance/implementation/code-guides/validation/validate_wave_1_drafting_readiness.py --json
```

## Output Classifications

`PASS`, `FAIL`, `WARNING`, `NOT_YET_APPLICABLE`, and `BLOCKED` are supported. `NOT_YET_APPLICABLE` is not counted as a passing substantive validation.

## Fixtures

Fixtures live under `validation/tests/fixtures/`. Positive fixtures are minimal valid examples. Negative fixtures isolate one failure reason where practical.

## Future Validators

Add new validators by implementing a function in `cgp_validation.py`, adding a wrapper entrypoint, and adding fixtures plus tests.

## CGP-003 Source Accession

`validate_source_accession.py` validates the master source register, source-to-guide map, retained source gaps, conflicts, and supersession records. It verifies source IDs, controlled values, repository path resolution, file checksums, deterministic directory aggregate checksums, guide mappings, and controlling-source approval basis. It does not validate or create substantive Code Guide controls.

## CGP-005 Source Freeze

`validate_source_freeze.py` validates the two-layer Wave 1 model: a non-normative reference corpus plus curated guide-specific normative freezes. It rejects bulk CGP-003 map passthrough, generic rationales, reference-corpus rows treated as normative, unnecessary package-child promotion, and implementation evidence without a CGP-004 component or Code Guide program evidence basis.

`validate_wave_1_drafting_readiness.py` validates that the CGP-005 revision leaves Wave 1 guides `PLANNED`, keeps CGP-006 not ready before Founder acceptance, preserves required freeze artifacts and drafting-question inventories, and remains not adopted, not active, and not implementation-authorizing.
