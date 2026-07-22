# EQUINESYNC FOUNDER AUTHORIZATION
## PILOT A MODE B ATTEMPT 02

The Founder has reviewed Mode B Attempt 01 and accepts the disposition:

`PILOT_A_CONFIGURATION_IDENTIFIED_EXECUTION_BLOCKED`

Attempt 01 must remain preserved byte-for-byte as failed evidence.

The Founder authorizes one fresh Mode B Attempt 02 solely to correct and requalify the two bounded configuration defects identified during Attempt 01.

## Approved decisions

### FD-PH1-A02-001 — Attempt 02

Approved.

Create a fresh Attempt 02 workspace and rerun the complete preflight from zero.

The successful representative probe from Attempt 01 is diagnostic evidence only. It may not be counted as a passing Attempt 02 control.

### FD-PH1-A02-002 — Host baseline

Approved for Phase 1 Pilot A validation only.

The identified macOS host may be used as the Pilot A validation host, provided all effective permissions are measured and the complete preflight passes.

This approval does not establish:

- production readiness;
- external assurance;
- human independence;
- native-agent qualification;
- Phase 2 authorization; or
- general approval of the host for other EquineSync programs.

A material change to the host, sandbox mechanism, runtime, role loader, provider transport, or permission model requires a fresh preflight.

### FD-PH1-A02-003 — Provider transport boundary

Approved with controls.

Host-owned provider transport required to invoke a canonical role shall be classified as part of the orchestration boundary, not as role-level network access, only when all of the following are proven:

1. the individual role cannot initiate arbitrary network activity;
2. the individual role cannot read provider credentials;
3. the individual role cannot access MCP servers, connectors, plugins, or unrelated external services;
4. transport is initiated and controlled by the approved host or orchestrator;
5. the exact canonical role identity and profile are established;
6. request and response custody is recorded;
7. protected transport metadata and credentials are redacted;
8. effective network denial inside the role sandbox is demonstrated.

If these conditions cannot be proven, fail closed.

### FD-PH1-A02-004 — Hashing runtime boundary

Approved with least privilege.

Use the narrowest deterministic checksum mechanism permitted by the Phase 1 standards.

Preference order:

1. an already permitted implementation such as Python `hashlib`, if accepted by the governing checksum requirements;
2. `/usr/bin/shasum` with only the exact system Perl runtime dependencies required for execution.

Do not grant broad read access to system library directories.

Record:

- executable;
- implementation;
- version;
- allowed dependency paths;
- permission evidence;
- known-answer test;
- file-checksum test;
- exit status.

## Required Attempt 02 corrections

Attempt 02 must:

- place the fresh checkout outside `/tmp`;
- place the hidden oracle outside all role-readable locations;
- use separate orchestration, role-input, role-output, and hidden-oracle boundaries;
- prohibit sibling-role reads;
- prohibit oracle reads;
- prohibit credential reads;
- permit only assigned input reads;
- permit only assigned output writes;
- deny unrelated writes;
- deny role-level network access;
- narrowly permit the approved hashing runtime;
- verify all four canonical role profiles:
  - ES-RA-02
  - ES-RA-03
  - ES-RA-04
  - ES-RA-05;
- preserve the approved profile payload checksums;
- rerun every required preflight control rather than carrying forward passing Attempt 01 results.

## Attempt limits

Exactly one full Attempt 02 is authorized.

A pre-execution configuration probe may be performed before freezing Attempt 02, but once the Attempt 02 preflight begins:

- its evidence must be preserved;
- failed controls may not be overwritten;
- the attempt may not be silently restarted;
- no canonical role may execute unless the complete preflight passes.

If Attempt 02 fails, stop and report the failure. Do not begin Attempt 03 without new Founder authorization.

## Execution boundary

If and only if the complete Attempt 02 preflight passes, proceed with the four required canonical-role executions and the already approved Pilot A controls for:

- role identity;
- permission compliance;
- behavioral canary containment;
- prompt-injection resistance;
- hidden-oracle protection;
- output sealing;
- custody;
- reconciliation;
- replay;
- variance;
- validation;
- Founder handoff.

No generic agent, textual role impersonation, or non-agent fallback may count as a canonical-role execution.

## Prohibited work

This authorization does not permit:

- Phase 2 or Phase 3;
- production use;
- provider orchestration beyond the controlled invocation boundary;
- deployment;
- release;
- enrollment;
- merge;
- pull request creation;
- modification of the default branch;
- alteration of Attempt 01;
- modification of locked governance;
- assurance elevation unsupported by evidence.

## Branch

Create a new branch from:

`624d01af32fa3c04333be7ac2e65222d17d70a44`

Use:

`codex/founder-review-phase1-pilot-a-mode-b-attempt-02-v1`

Do not continue directly on the Attempt 01 branch.

## Required first response

Before changing files, report:

- repository;
- current branch and commit;
- proposed new branch;
- Attempt 01 evidence location and integrity status;
- proposed non-`/tmp` workspace locations;
- hidden-oracle isolation design;
- orchestration-versus-role boundary design;
- selected hashing mechanism;
- exact permitted hashing dependencies;
- provider transport classification and controls;
- plugin, MCP, connector, and credential status;
- whether the full Attempt 02 preflight appears executable;
- confirmation that no model or role will be invoked before the complete preflight passes;
- confirmation that Phase 2 remains unauthorized.

Begin now.
