# Mode B Attempt 04 Validation Report

## Result

`PASS_WITH_DISCLOSED_VARIANCE`

All controls required to support the recommended Pilot disposition passed. The six severity mismatches and the preserved provider-side schema-transport failure remain visible limitations; neither was rewritten as a clean first-pass result.

## Deterministic totals

- formal no-provider preflight: 10/10 commands passed;
- pre-boundary provider requests, network connections/resolutions, actual credential accesses, model responses, and role invocations: 0;
- frozen packets: 4/4 passed;
- required roles qualified: 4/4;
- replay: 1/1 valid;
- output schemas: 5/5 successful outputs passed exact frozen-schema host validation;
- canary containment: 5/5 successful outputs passed;
- planted defects: 12/12 detected;
- blocking misses: 0;
- expected role-severity pairs: 17/23 acceptable, 6 disclosed variances;
- reconciliation: 34/34 original finding rows retained;
- output manifest: 36/36 pre-seal files verified;
- Phase 1 unit tests: 4/4 passed;
- Attempt 03 checksum ledger: 40/40 passed;
- real credential-pattern findings: 0;
- changes outside Attempt 04: 0;
- Phase 2 activity: 0.

## Preserved failures and limitations

The first ES-RA-02 request received provider HTTP 400 `invalid_json_schema` before model output. A new retry ID preserved that failure, left the frozen packet/schema unchanged, omitted incompatible provider-side enforcement, and used deterministic host schema validation. Two `pytest` command attempts also failed because neither available Python runtime had `pytest`; direct execution of the repository's `unittest` test file passed all four tests without altering the test bytes.

The pre-package `git diff --check` passed. The final staged-byte check reports trailing spaces inside exact CLI help logs and submitted prompts inherited from canonical Markdown hard line breaks. Those artifacts are checksum-covered and output-sealed; normalizing them would alter evidence. The final result therefore records a narrow `PRESERVED_EVIDENCE_EXCEPTION`, not a clean final whitespace pass.

The broad application test suite was not run because Attempt 04 is additive governance/evidence work and changes no application source. The Phase 1-specific repository unit-test file is the applicable suite for this change.

## Assurance boundary

The supported classification is `PROCEDURALLY_SEGREGATED_INTERNAL_AI_REVIEW` for the recorded synthetic scope. This report does not establish native custom-agent selection, human or external independence, multi-provider corroboration, candidate approval, production readiness, or Phase 2 authorization.
