# Project Trust and Config Provenance

## Result

`PASS` — the exact repository/worktree path was already explicitly trusted before project-agent testing:

`/Users/rianray/Documents/Codex/2026-07-19/place-the-approved-equinesync-founder-orchestrated/work/EquineSync-V4-founder-review-package`

The containing Codex task directory was also trusted. No trust correction or session restart was required.

## Effective configuration

- `HOME`: `/Users/rianray`
- `CODEX_HOME` environment variable: unset
- effective Codex home: `/Users/rianray/.codex`
- user config: `/Users/rianray/.codex/config.toml`
- project config: `/Users/rianray/Documents/Codex/2026-07-19/place-the-approved-equinesync-founder-orchestrated/work/EquineSync-V4-founder-review-package/.codex/config.toml`
- project config strict parse: `PASS`
- `[agents].max_threads`: `6`
- `[agents].max_depth`: `1`
- project standalone agents: `/Users/rianray/Documents/Codex/2026-07-19/place-the-approved-equinesync-founder-orchestrated/work/EquineSync-V4-founder-review-package/.codex/agents`
- personal standalone-agent directory: absent

No secret-bearing user configuration is copied into this evidence package. The trust fact is recorded as a sanitized value only.

The controlled batch design used three read-only children in one parent session and five workspace-write children in another. This stays within six threads including the parent and requires only depth 1.
