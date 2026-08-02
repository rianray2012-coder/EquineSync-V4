#!/bin/sh
# Reproduce the Tier 1 package validation and record an attestation row.
#
# Usage:  sh VALIDATION/reproduce.sh <package-root>
#
# The script prints the validator report, the self-test report, and one CSV row
# suitable for appending to VALIDATION/INDEPENDENT_REPRODUCTION_ATTESTATIONS.csv.
# It does not append the row itself: an attestation must be added by the party
# who ran it, not by the script they ran.
set -eu
PKG="${1:-$(pwd)}"
V="$PKG/VALIDATION/validate_tier1_documents_03_10_rr2.py"

echo "=== self-test ==="
python3 "$V" --self-test

echo "=== validation ==="
python3 "$V" --package-root "$PKG" --mode package-only > /tmp/t1_report.json
cat /tmp/t1_report.json

ROOT_HASH=$(python3 -c "import json,sys;print(json.load(open('$PKG/00_PROGRAM_CONTROL/ROUND_3_INTEGRITY_ROOT.json'))['manifest_of_manifests_sha256'])")
STATUS=$(python3 -c "import json;print(json.load(open('/tmp/t1_report.json'))['status'])")
FAILURES=$(python3 -c "import json;print(json.load(open('/tmp/t1_report.json'))['failures'])")

echo "=== attestation row ==="
python3 - "$ROOT_HASH" "$STATUS" "$FAILURES" <<'PY'
import csv, datetime, io, platform, sys
root_hash, status, failures = sys.argv[1], sys.argv[2], sys.argv[3]
buf = io.StringIO()
csv.writer(buf, lineterminator="").writerow([
    "ATTESTATION_ID_ASSIGN_ON_APPEND",
    datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    platform.platform(), platform.machine(),
    "Python " + platform.python_version(),
    status, failures, root_hash,
    "ATTESTOR_NAME_REQUIRED", "ATTESTOR_ROLE_REQUIRED",
    "NOT_SIGNED_NO_SIGNING_KEY_PROVISIONED",
])
print(buf.getvalue())
PY
