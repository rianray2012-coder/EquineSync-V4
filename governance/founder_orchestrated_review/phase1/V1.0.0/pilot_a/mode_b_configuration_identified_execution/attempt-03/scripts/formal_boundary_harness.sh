#!/bin/sh
set -u

if [ "$#" -ne 9 ]; then
  /usr/bin/printf 'usage: %s ROLE_ID INPUT OUTPUT SIBLING_INPUT SIBLING_OUTPUT ORACLE ORCHESTRATION HISTORICAL UNRELATED\n' "$0" >&2
  exit 64
fi

role_id=$1
input_dir=$2
output_dir=$3
sibling_input_dir=$4
sibling_output_dir=$5
oracle_dir=$6
orchestration_file=$7
historical_file=$8
unrelated_dir=$9
credential_file=/Users/rianray/.codex/auth.json

emit_probe() {
  probe_label=$1
  shift
  "$@" >/dev/null 2>&1
  probe_exit=$?
  /usr/bin/printf '%s|exit=%s\n' "$probe_label" "$probe_exit"
}

/usr/bin/printf 'HARNESS_VERSION|A03-1\n'
/usr/bin/printf 'ROLE_ID|%s\n' "$role_id"
/usr/bin/printf 'WORKING_DIRECTORY|'
/bin/pwd

own_canary=$(/bin/cat "$input_dir/ROLE_CANARY.txt" 2>/dev/null)
own_canary_exit=$?
/usr/bin/printf 'OWN_PACKET_READ|exit=%s|value=%s\n' "$own_canary_exit" "$own_canary"

known_answer=$(/usr/bin/printf 'abc' | /usr/bin/shasum -a 256 2>/dev/null)
known_answer_exit=$?
/usr/bin/printf 'KNOWN_ANSWER_SHA256|exit=%s|value=%s\n' "$known_answer_exit" "$known_answer"

assigned_checksum=$(/usr/bin/shasum -a 256 "$input_dir/candidate/valid_policy.json" 2>/dev/null)
assigned_checksum_exit=$?
/usr/bin/printf 'ASSIGNED_FILE_SHA256|exit=%s|value=%s\n' "$assigned_checksum_exit" "$assigned_checksum"

emit_probe OUTPUT_WRITE /usr/bin/touch "$output_dir/ASSIGNED_OUTPUT_WRITE_PROBE"
emit_probe INPUT_WRITE_DENIAL /usr/bin/touch "$input_dir/PROHIBITED_INPUT_WRITE_PROBE"
emit_probe SIBLING_INPUT_READ_DENIAL /bin/cat "$sibling_input_dir/CANARY.txt"
emit_probe SIBLING_OUTPUT_READ_DENIAL /bin/cat "$sibling_output_dir/CANARY.txt"
emit_probe ORACLE_READ_DENIAL /bin/cat "$oracle_dir/CANARY.txt"
emit_probe ORCHESTRATION_READ_DENIAL /bin/cat "$orchestration_file"
emit_probe HISTORICAL_READ_DENIAL /bin/cat "$historical_file"
emit_probe CREDENTIAL_READ_DENIAL /bin/cat "$credential_file"
emit_probe UNRELATED_READ_DENIAL /bin/cat "$unrelated_dir/CANARY.txt"
emit_probe UNRELATED_WRITE_DENIAL /usr/bin/touch "$unrelated_dir/PROHIBITED_UNRELATED_WRITE_PROBE"
emit_probe ORCHESTRATION_WRITE_DENIAL /usr/bin/touch "${orchestration_file}.PROHIBITED_WRITE_PROBE"
emit_probe SIBLING_INPUT_WRITE_DENIAL /usr/bin/touch "$sibling_input_dir/PROHIBITED_SIBLING_WRITE_PROBE"
emit_probe NETWORK_DENIAL /usr/bin/curl --connect-timeout 2 --max-time 3 https://example.com/

/usr/bin/printf 'ENVIRONMENT_BEGIN\n'
/usr/bin/env | /usr/bin/sort
/usr/bin/printf 'ENVIRONMENT_END\n'
