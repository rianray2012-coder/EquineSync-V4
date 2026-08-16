#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FLOW="${MAESTRO_FLOW:-$ROOT_DIR/.maestro/role-home.yml}"
PASSWORD="${EQUINESYNC_UAT_PASSWORD:-}"
ROLE_FILTER="${ROLE_FILTER:-}"
MAESTRO_PLATFORM="${MAESTRO_PLATFORM:-}"
MAESTRO_DEVICE="${MAESTRO_DEVICE:-}"

if [[ -z "$PASSWORD" ]]; then
  echo "EQUINESYNC_UAT_PASSWORD is required and must not be committed." >&2
  exit 2
fi
if [[ "$PASSWORD" == "PASTE_UAT_PASSWORD_HERE" ]]; then
  echo "Replace PASTE_UAT_PASSWORD_HERE with the real UAT password before running." >&2
  exit 2
fi

if ! command -v maestro >/dev/null 2>&1; then
  echo "Maestro CLI is not installed. Install it before running this matrix." >&2
  exit 2
fi

export MAESTRO_CLI_NO_ANALYTICS="${MAESTRO_CLI_NO_ANALYTICS:-1}"
export MAESTRO_CLI_ANALYSIS_NOTIFICATION_DISABLED="${MAESTRO_CLI_ANALYSIS_NOTIFICATION_DISABLED:-true}"

denied_home_status_id() {
  case "$1" in
    "Platform Admin Console") echo "role-home-platform-status" ;;
    "Facility Dashboard") echo "role-home-facility-status" ;;
    "Manager Dashboard") echo "role-home-manager-status" ;;
    "Trainer Operating Center") echo "role-home-trainer-status" ;;
    "Staff Work Queue") echo "role-home-staff-status" ;;
    "Owner Dashboard") echo "role-home-owner-status" ;;
    "Guardian Dashboard") echo "role-home-guardian-status" ;;
    "Rider Dashboard") echo "role-home-rider-status" ;;
    "Service Provider Center") echo "role-home-provider-status" ;;
    *) echo "" ;;
  esac
}

run_role() {
  local slug="$1"
  local email="$2"
  local expected_home="$3"
  local expected_role_line="$4"
  local expected_account_line="$5"
  local denied_home="$6"
  local denied_status_id
  denied_status_id="$(denied_home_status_id "$denied_home")"

  if [[ -n "$ROLE_FILTER" && "$ROLE_FILTER" != "$slug" ]]; then
    return 0
  fi

  echo "Running Phase 3 role-home flow: $slug"
  if command -v xcrun >/dev/null 2>&1 && xcrun simctl list devices booted 2>/dev/null | grep -q "iOS"; then
    xcrun simctl terminate booted com.equinesync.app >/dev/null 2>&1 || true
    xcrun simctl keychain booted reset >/dev/null 2>&1 || true
  fi
  local maestro_target_args=()
  if [[ -n "$MAESTRO_PLATFORM" ]]; then
    maestro_target_args+=(--platform "$MAESTRO_PLATFORM")
  fi
  if [[ -n "$MAESTRO_DEVICE" ]]; then
    maestro_target_args+=(--device "$MAESTRO_DEVICE")
  fi
  maestro test \
    "${maestro_target_args[@]}" \
    -e EMAIL="$email" \
    -e PASSWORD="$PASSWORD" \
    -e EXPECTED_HOME="$expected_home" \
    -e EXPECTED_ROLE_LINE="$expected_role_line" \
    -e EXPECTED_ACCOUNT_LINE="$expected_account_line" \
    -e DENIED_HOME="$denied_home" \
    -e DENIED_HOME_STATUS_ID="$denied_status_id" \
    "$FLOW"
}

run_role "platform-admin" "uat.platform@equine-sync.com" "Platform Admin Console" "role=admin" "account=facility" "Facility Dashboard"
run_role "facility-admin" "uat.facility-admin@equine-sync.com" "Facility Dashboard" "role=admin" "account=facility" "Owner Dashboard"
run_role "barn-owner" "uat.barn-owner@equine-sync.com" "Facility Dashboard" "role=barn owner" "account=facility" "Owner Dashboard"
run_role "trainer" "uat.trainer@equine-sync.com" "Trainer Operating Center" "role=trainer" "account=facility" "Owner Dashboard"
run_role "barn-manager" "uat.manager@equine-sync.com" "Manager Dashboard" "role=barn manager" "account=facility" "Owner Dashboard"
run_role "barn-staff" "uat.staff@equine-sync.com" "Staff Work Queue" "role=groom" "account=facility" "Owner Dashboard"
run_role "working-student" "uat.working-student@equine-sync.com" "Staff Work Queue" "role=working student" "account=facility" "Owner Dashboard"
run_role "horse-owner" "uat.owner@equine-sync.com" "Owner Dashboard" "role=horse owner" "account=facility" "Facility Dashboard"
run_role "guardian" "uat.guardian@equine-sync.com" "Guardian Dashboard" "role=parent" "account=facility" "Owner Dashboard"
run_role "participant" "uat.participant@equine-sync.com" "Rider Dashboard" "role=rider" "account=facility" "Owner Dashboard"
run_role "individual-owner" "uat.individual-owner@equine-sync.com" "Individual Owner Home" "role=horse owner" "account=individual owner" "Facility Dashboard"
run_role "service-provider" "uat.service-provider@equine-sync.com" "Service Provider Center" "role=service provider" "account=facility" "Owner Dashboard"

echo "Phase 3 role-home Maestro matrix complete."
