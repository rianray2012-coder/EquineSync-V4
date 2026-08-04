#!/usr/bin/env python3
"""Non-operative historical validator retained for custody.

Use python3 VALIDATION/validate_tier1_documents_03_10_v5.py --package-root <package>.
This stub exits 2 so automation cannot mistake it for an operative pass.
"""
import json, sys
print(json.dumps({
  "status": "NON_OPERATIVE_HISTORICAL",
  "validator": "validate_tier1_documents_03_10_v2.py",
  "authoritative_v5_invocation": "python3 VALIDATION/validate_tier1_documents_03_10_v5.py --package-root <package>",
  "exit_code": 2
}, indent=2))
sys.exit(2)
