# Recommended Founder Answers

**Status:** `RECOMMENDED_NOT_APPROVED`  
**PIA:** `ES-PIA-FACILITY-TENANT-ORGANIZATION` V0.2 conformance candidate

## ES-PIA-GFD-002 - Asset and maintenance ownership

`RECOMMENDED_NOT_APPROVED`

Approve Option A: Item 02 owns stable asset and location identity and topology; Item 07 owns care use, condition observations, and safety consequences; Item 06 owns maintenance/service-request scheduling, assignment, and work state. Each handoff uses stable versioned references. No asset association, work assignment, vendor relationship, payment, or completion status grants Tenant, Facility, Organization, relationship, or permission authority.

This supports individual owners and complex facilities, keeps onboarding adaptive, prevents duplicate asset truth, and allows low-connectivity work queues without turning a task system into the facility source of truth.

## ES-PIA-GFD-007 - Qualified review runtime

`RECOMMENDED_NOT_APPROVED`

Provision read-only/on-request/network-disabled sessions for documentary review roles and isolated bounded workspace-write/on-request/network-disabled sessions for writable machine-validation and custody roles. Record a complete `PASS` before every role. Do not grant a broad unrestricted exception.

This preserves the exact frozen candidate, permits credible independent review, and avoids repeating `FACILITY_PIA_REVIEW_BLOCKED_BY_RUNTIME_PERMISSION_FAILURE`.
