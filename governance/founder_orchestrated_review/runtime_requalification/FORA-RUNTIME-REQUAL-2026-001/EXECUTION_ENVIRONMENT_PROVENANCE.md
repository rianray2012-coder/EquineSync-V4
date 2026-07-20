# Execution Environment Provenance

- Run: `FORA-RUNTIME-REQUAL-2026-001`
- Captured: `2026-07-20T19:01:37+00:00`
- Platform: `macOS-26.5.2-arm64-arm-64bit-Mach-O`
- Machine: `arm64`
- Codex: `codex-cli 0.144.6`
- Git: `git version 2.50.1 (Apple Git-155)`
- Node: `v24.11.0`
- Python used by this evidence builder: `3.14.6`
- Repository source commit: `57210494c1e82e60efd4c329ebf34fda236972d8`
- Remediation branch: `codex/founder-review-agent-runtime-requalification-v1`

## Sanitized runtime state

- CLI interactive canary: read-only sandbox, on-request approvals, restricted network, isolated profile, zero plugins/connectors/MCP servers.
- CLI noninteractive canary: read-only sandbox, noninteractive effective approval `never`, restricted network, isolated profile, zero plugins/connectors/MCP servers.
- App-server diagnostic: isolated profile; config-read and schema generation only; no child execution.
- Desktop observation: `danger-full-access`, approval `never`; no formal role spawn attempted because the repository permission control prohibits this combination without a Founder exception.

## Controlled source inputs

- Sealed package checksum entries: 63/63 passed.
- Installed-system validation: 16/16 passed.
- Controlled files recorded: 184.
- Agent configuration package ZIP SHA-256: `604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3`.
- Founder handoff ZIP SHA-256: `7b1076f9eda1640936d07f72fac7aba6a3d83e9ed04f965ccb668043f8c144de`; its internal checksum verification passed.

The installed-system validator used a disposable Python environment pinned to `jsonschema[format]==4.26.0`. The initial missing-dependency failure and a later harness-scoring error are retained in the failed-attempt register. The corrected validation result is `raw/static_validation_retry_03/result.json`.
