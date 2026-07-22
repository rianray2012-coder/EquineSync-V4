#!/bin/sh
set -eu

isolated_home=/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_04_isolated_codex_home.nosync
mkdir -p "$isolated_home"
chmod 700 "$isolated_home"

printf 'PROBE_ID|A04-OFFLINE-DIAGNOSTIC-PROOF-04\n'
printf 'NETWORK_POLICY|DENY_ALL\n'
printf 'CODEX_HOME|%s\n' "$isolated_home"
printf 'COMMAND_01|/usr/bin/which codex\n'
/usr/bin/which codex
printf 'COMMAND_02|codex --version\n'
CODEX_HOME="$isolated_home" codex --version
printf 'COMMAND_03|codex sandbox --help\n'
CODEX_HOME="$isolated_home" codex sandbox --help
printf 'COMMAND_04|codex exec --help\n'
CODEX_HOME="$isolated_home" codex exec --help
printf 'RESULT|PASS_IF_EXIT_ZERO_AND_NO_NETWORK_DENIAL\n'
