# Phase 1 Failure, Retry, and Abstention Rules

Preserve every failed invocation, validator result, incomplete output, permission failure, canary leak, candidate drift event, schema failure, tool failure, timeout, and abstention. Never overwrite or delete an attempt to improve the apparent result.

Every retry requires a new execution ID, predecessor ID, reason, authorization basis, changed conditions, unchanged conditions, timestamps, outputs, logs, hashes, and validation. Retry only when the failure cause and changed condition are explicit; do not rerun solely to conceal failure.

Abstain and escalate when scope, authority, identity, baseline, evidence, classification, permission, tool safety, or required expertise is unresolved. An abstention is valid control behavior and is not a pass. AI roles may recommend a disposition but may not close findings, accept risk, waive requirements, or make a Founder decision.
