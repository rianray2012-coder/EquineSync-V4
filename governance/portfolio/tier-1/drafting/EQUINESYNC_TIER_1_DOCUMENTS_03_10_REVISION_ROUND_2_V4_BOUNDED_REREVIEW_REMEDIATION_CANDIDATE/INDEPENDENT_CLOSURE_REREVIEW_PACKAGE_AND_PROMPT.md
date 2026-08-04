# Bounded Independent Closure Rereview Prompt

Review only the authenticated V4 package rooted at `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V4_BOUNDED_REREVIEW_REMEDIATION_CANDIDATE` and its detached ZIP checksum.

Expected package status unless independently closed by the reviewer: `PACKAGING_READY_FOR_BOUNDED_REREVIEW; CONTENT_REVISION_REQUIRED; NOT_ADOPTED; NOT_ACTIVE; MERGE_NOT_AUTHORIZED; FOUNDER_REVIEW_REQUIRED`.

Authoritative validator for this package:

```bash
python3 VALIDATION/validate_tier1_documents_03_10_v4.py --package-root .
```

Negative fixture harness:

```bash
python3 VALIDATION/execute_negative_fixtures_v4.py --package-root .
```

Treat `validate_tier1_documents_03_10_v2.py`, `validate_tier1_documents_03_10_v3.py`, and RR2-era per-document validators as historical/non-operative unless their file header states otherwise. The V4 validator is authoritative for V4 rereview.

Determine whether each T1C item can be closed by independent reviewer judgment, retained nonblocking, or must remain open. Do not infer adoption, activation, production authorization, protected-branch merge authority, certification, waiver approval, Founder approval, or risk acceptance.

Required reviewer output:

- authenticated target SHA-256, byte length, and file count;
- disposition for T1C-001 through T1C-020;
- validation of negative fixture behavior;
- explicit statement of reviewer independence, conflict status, and scope limitations;
- explicit treatment of Doc 10 template-purpose dispute.
