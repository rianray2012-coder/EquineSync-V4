# Controlled Identity Probe Temporary Process Residue

Classification: `CONTROLLED_IDENTITY_PROBE_TEMPORARY_PROCESS_RESIDUE`

During discarded lifecycle attempt 006, PID 49706 (`/usr/sbin/lsof`, process group 49347) remained temporarily in an uninterruptible wait while inspecting controlled port 8019. Its parent validator PID was 49347; after the parent stopped, PID 49706 was reparented to PID 1. The exact command was `lsof -nP -t -iTCP:8019 -sTCP:LISTEN`, and its working directory was `stage2a`.

Only verified process group 49347 received `TERM` and then `KILL`. Both controlled ports were closed, no application or database listener was active, and no sealed or repository-controlled artifact changed. Attempt 006 was discarded in full. This event is not merged with the prior segregated-review MongoDB residue and is not evidence of causation for `RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE`.
