# Controlled Startup Failure Process Residue

- Classification: `CONTROLLED_STARTUP_FAILURE_PROCESS_RESIDUE`
- API PID/PGID: `67982/67982`
- Controlled port: `8019`, verified closed and not yet bound
- Action: `SIGTERM` to only the completely reverified API process group, followed by normal verified Mongo shutdown
- Result: both controlled ports closed, PID records absent, and runtime directory removed
- Test disposition: the incomplete lifecycle attempt was discarded and no result was promoted
- Sealed or repository-controlled artifacts changed by the processes: `false`
- Relationship to `RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE`: none established; do not conflate

The first shutdown refusal was correct fail-closed behavior under the then-current listener requirement. Independent executable, command-line, CWD, PPID, PGID, nonce, and closed-port checks established exact ownership before termination.
