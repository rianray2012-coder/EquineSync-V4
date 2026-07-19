# Canary Runtime Results

The project-scoped canary loaded on both required CLI surfaces. Only the exact child response `ES_RUNTIME_CANARY_LOADED_V1` is accepted as loading proof.

| Surface | Attempt | Exit | Marker | Classification |
|---|---|---:|---|---|
| interactive CLI | `runs/canary_project_standalone/interactive_cli/run-01` | 0 | `absent` | `INVOCATION_FAILED` |
| interactive CLI | `runs/canary_project_standalone/interactive_cli/run-02` | 0 | `present` | `CUSTOM_AGENT_LOADED` |
| codex exec --json | `runs/canary_project_standalone/exec_json/run-01` | 2 | `absent` | `INVOCATION_FAILED` |
| codex exec --json | `runs/canary_project_standalone/exec_json/run-02` | 0 | `absent` | `INVOCATION_FAILED` |
| codex exec --json | `runs/canary_project_standalone/exec_json/run-03` | 0 | `present` | `CUSTOM_AGENT_LOADED` |

The preserved failures isolate invocation errors: a full-history fork cannot override `agent_type`; `-a` must precede the `exec` subcommand; and `task_name` remains required alongside `agent_type`. Because both project-scoped tests passed, no personal-agent copy was necessary.
