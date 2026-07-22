# Mode B Attempt 03 Execution Environment Specification

**Attempt:** `ES-PH1-PILOT-A-MODE-B-ATTEMPT-03`

**Mode:** `CONFIGURATION_IDENTIFIED_MANUAL_ROLE_EXECUTION`

**Starting commit:** `dc5dc547df84eca59c265c355f86331f80c2ee59`

**Branch:** `codex/founder-review-phase1-pilot-a-mode-b-attempt-03-v1`

**Host:** macOS arm64

**Planned generic runtime:** `codex-cli 0.144.6`

**Planned model/provider:** `gpt-5.6-sol` / OpenAI

## Separated `.nosync` boundaries

- orchestration checkout: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_execution.nosync/EquineSync-V4`
- role inputs: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_runtime.nosync/role_inputs/<ROLE_ID>`
- role outputs: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_runtime.nosync/role_outputs/<ROLE_ID>`
- evidence: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_runtime.nosync/evidence`
- hidden oracle: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_runtime.nosync/hidden_oracle`
- isolated no-config probe home: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_isolated_codex_home.nosync`

Each formal role profile granted read to only its assigned packet, write to only its assigned output, read to the minimal runtime baseline and exact checksum dependencies, and denied direct network. The host provider transport was planned as an orchestration-only boundary. No Role Execution reached that transport because the preflight provider-request prohibition was violated by the host diagnostic itself.

## Runtime surface controls

The planned invocation used `--ephemeral`, `--ignore-user-config`, `--skip-git-repo-check`, approval policy `on-request`, a custom restricted permission profile, no inherited shell environment, history persistence `none`, empty OpenTelemetry configuration, and disabled plugin/app/MCP/connector/browser/computer-use/memory/multi-agent features.

The isolated configuration probe successfully resolved the custom permission profile. Plugin enumeration returned `installed: []` and MCP enumeration returned `[]`. However, the subsequent doctor command performed live provider reachability tests. That command is prohibited from substitution or rerun within this frozen attempt.
