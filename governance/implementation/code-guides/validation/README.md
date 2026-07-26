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

## Output Classifications

`PASS`, `FAIL`, `WARNING`, `NOT_YET_APPLICABLE`, and `BLOCKED` are supported. `NOT_YET_APPLICABLE` is not counted as a passing substantive validation.

## Fixtures

Fixtures live under `validation/tests/fixtures/`. Positive fixtures are minimal valid examples. Negative fixtures isolate one failure reason where practical.

## Future Validators

Add new validators by implementing a function in `cgp_validation.py`, adding a wrapper entrypoint, and adding fixtures plus tests.
