# Mode B Attempt 02 Execution Environment Specification

**Attempt:** `ES-PH1-PILOT-A-MODE-B-ATTEMPT-02`  
**Mode:** `CONFIGURATION_IDENTIFIED_MANUAL_ROLE_EXECUTION`  
**Starting commit:** `624d01af32fa3c04333be7ac2e65222d17d70a44`  
**Branch:** `codex/founder-review-phase1-pilot-a-mode-b-attempt-02-v1`  
**Host:** macOS arm64  
**Planned generic runtime:** `codex-cli 0.144.6`  
**Planned model/provider:** `gpt-5.6-sol` / OpenAI

## Separated host boundaries

- orchestration: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_02_orchestration/EquineSync-V4`
- role inputs: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_02_role_inputs/<ROLE_ID>`
- role outputs: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_02_role_outputs/<ROLE_ID>`
- hidden oracle: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_02_hidden_oracle`

All paths were outside `/tmp`. Each planned role profile granted read to only its assigned input, write to only its assigned output, read to the minimal runtime baseline and exact checksum dependencies, and denied direct network. Sibling packets and outputs, orchestration, historical evidence, the hidden oracle, credentials, and unrelated paths were outside the allowlist.

## Checksum boundary

The selected mechanism was `/usr/bin/shasum -a 256`, accepted by the Phase 1 build requirements. The planned implementation was the system Perl `Digest::SHA` runtime. Exact additional readable dependencies were:

- `/usr/bin/shasum`
- `/usr/bin/perl`
- `/System/Library/Perl/5.34/darwin-thread-multi-2level/CORE/libperl.dylib`
- `/System/Library/Perl/5.34/darwin-thread-multi-2level/Digest/SHA.pm`
- `/System/Library/Perl/5.34/Digest/base.pm`
- `/System/Library/Perl/5.34/Exporter.pm`
- `/System/Library/Perl/5.34/Exporter/Heavy.pm`
- `/System/Library/Perl/5.34/darwin-thread-multi-2level/Fcntl.pm`
- `/System/Library/Perl/5.34/Getopt/Long.pm`
- `/System/Library/Perl/5.34/XSLoader.pm`
- `/System/Library/Perl/5.34/constant.pm`
- `/System/Library/Perl/5.34/integer.pm`
- `/System/Library/Perl/5.34/overload.pm`
- `/System/Library/Perl/5.34/overloading.pm`
- `/System/Library/Perl/5.34/strict.pm`
- `/System/Library/Perl/5.34/vars.pm`
- `/System/Library/Perl/5.34/warnings.pm`
- `/System/Library/Perl/5.34/warnings/register.pm`
- `/System/Library/Perl/5.34/darwin-thread-multi-2level/auto/Digest/SHA/SHA.bundle`
- `/System/Library/Perl/5.34/darwin-thread-multi-2level/auto/Fcntl/Fcntl.bundle`

The authorized pre-freeze probe produced the SHA-256 known answer `edeaaff3f1774ad2888673770c6d64097e391bc362d7d6fb34982ddf0efd18cb` for the exact bytes `abc\n`, passed an assigned-file checksum, permitted assigned-output write, and denied input write, sibling read, oracle read, unrelated read, credential read, and direct network. It remained diagnostic only and was not carried forward as formal preflight success.

## Provider transport classification

Host-owned provider transport was planned as an orchestration boundary only. Qualification required host-controlled invocation, exact role/profile identity, request/response custody, credential redaction, role credential denial, direct role-network denial, and disabled plugins, MCP, connectors, and unrelated services. Because formal preflight failed before these controls completed, no provider request was made and the transport was not exercised.
