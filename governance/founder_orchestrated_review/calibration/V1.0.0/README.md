# Founder-Orchestrated Review Agent Runtime Calibration V1.0.0

This suite calibrates the eight installed EquineSync custom agents with synthetic evidence only. It does not review an actual EquineSync governance or implementation artifact and does not create a substantive Founder-Orchestrated Review Cycle.

## Contents

- `CALIBRATION_PLAN.md` defines scope, metrics, and stop conditions.
- `SYNTHETIC_FOUNDER_REVIEW_AUTHORIZATION.json` authorizes calibration only.
- `SYNTHETIC_PERMISSION_RECORDS.json` records the parent mode expected for each role.
- `cases/CALIBRATION_CASES.json` defines 15 common tests and role mappings.
- `cases/RUNTIME_AGENT_RESPONSE.schema.json` defines the required runtime response.
- `fixtures/` contains known-good and known-bad synthetic materials.
- `run_runtime_calibration.py` starts isolated Codex parent sessions and requires each parent to spawn the named registered custom agent.
- `runtime_runs/` preserves prompts, JSONL events, final responses, scoring, commands, failures, and reruns.

## Safety boundary

The suite must never be pointed at actual governance, implementation, customer, credential, payment, child, health, communication, or production data. Agents must not edit the repository or any sealed package file during calibration. Runtime-generated evidence is written by the calibration harness, not by the calibrated role.

## Running

Run one role at a time so first failures remain clear:

```text
python3 governance/founder_orchestrated_review/calibration/V1.0.0/run_runtime_calibration.py --role equinesync_drafting_agent
```

Run without `--role` to execute all roles sequentially. The harness never overwrites an earlier run directory.
