# Mode B Attempt 02 Validation Report

## Result

`FAILED — PILOT QUALIFICATION NOT ESTABLISHED`

All four frozen packet manifests matched their listed files, all approved-source hashes matched, and all four profile payload checksums matched when recalculated with the governing canonical JSON serializer (`sort_keys=True`, compact separators, UTF-8, `ensure_ascii=False`). A separate `jq -cS` experiment produced different bytes and hashes; that was classified as an incompatible serialization method, not a role-profile defect.

Every role packet contained its own canary in the canary file and manifest, and contained zero foreign canaries. All assigned role-output directories were empty after temporary preflight-sentinel cleanup. The hidden oracle retained SHA-256 `f6d3d58a21f424d3d1229a50579833bbc0557824e4ce0755e44b8009f44c1c52`.

Those mechanical results cannot cure the formal preflight failures. No role output schema, prompt-injection response, hidden-oracle detection score, reconciliation, replay, or variance qualification exists because zero roles executed.
