#!/usr/bin/env python3
"""Historical non-operative validator retained for custody.

This validator is not authoritative for `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V4_BOUNDED_REREVIEW_REMEDIATION_CANDIDATE`. Use:
  python3 VALIDATION/validate_tier1_documents_03_10_v4.py --package-root <package>
"""
import json
print(json.dumps({
  "status": "NON_OPERATIVE_HISTORICAL",
  "validator": "validate_tier1_documents_03_10_v2.py",
  "authoritative_v4_invocation": "python3 VALIDATION/validate_tier1_documents_03_10_v4.py --package-root <package>"
}, indent=2))
