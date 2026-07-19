# Runtime Discovery Diagnostic Report

## Outcome

Project-scoped custom-agent discovery is supported and proven on Codex CLI `0.144.6`. All eight installed roles were selected by exact standalone `agent_type`, and each child returned its deliberately embedded registration marker. The current installation is nevertheless not ready for Founder activation review because ES-RA-04 and ES-RA-06 failed the downstream behavioral calibration.

## Controlled baseline

- branch: `agent/install-founder-review-agents-v1.0.0`
- immutable pre-remediation commit: `f885a617332bb0a91b8adf15ae7b0e345cfb597f`
- parent installation commit: `a1caf346fe7b07b1be7dde12f1b805a62b2e5f9b`
- initial worktree: clean
- package ZIP SHA-256: `604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3`
- substantive review: not started

## Root cause

The project was trusted and the standalone TOML layout was valid. The pre-remediation orchestration path selected named task paths without reliably supplying the standalone custom-agent `agent_type`; the calibration harness also launched with `--ignore-user-config`, removing the effective trusted configuration stack used by successful custom-agent selection. A task path alone is not proof of instruction loading.

The minimum remediation is therefore invocation-level:

1. retain the trusted user/project configuration stack;
2. start at the repository root;
3. call `spawn_agent` with both `task_name` and exact `agent_type`;
4. set `fork_turns="none"` so the custom type is not overridden by full-history inheritance; and
5. accept loading only when child session metadata names the exact custom role and the child returns the embedded marker without reading `.codex/agents`.

No operational role semantics, sealed package file, prior failed-run evidence, or package-controlled calibration artifact was changed.

## Test results

- project trust: `PASS`
- standalone TOML discovery: `9/9` including temporary canary
- canary surfaces: interactive CLI `PASS`; `codex exec --json` `PASS`
- individual operational roles: `8/8` discovered and `8/8` instruction layers loaded
- representative read-only behavior: `PASS`, including refusal to draft/modify controlled content
- representative workspace-write behavior: `PASS`, exactly one authorized disposable probe file
- bounded orchestration: `8/8 PASS` by controlled 3+5 batching
- behavioral suite: `90/120` accepted; six roles passed and two failed

## Behavioral blockers

- ES-RA-04 returned an incorrect marker (`V1.0`), incorrect loaded name, non-prescribed decisions, and the wrong permitted disposition.
- ES-RA-06 returned a domain placeholder as its marker and remained schema/decision-nonconforming after corrections in the same child session.

These are genuine role-calibration failures, not discovery failures. They are preserved without modifying the agents during this narrowly scoped remediation.
