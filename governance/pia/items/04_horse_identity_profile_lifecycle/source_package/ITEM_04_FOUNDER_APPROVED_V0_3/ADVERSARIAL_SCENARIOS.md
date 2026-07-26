# Item 04 Adversarial, Negative, and Abuse Scenarios

**Source artifact:** `ES-PIA-HORSE-IDENTITY-LIFECYCLE_V0_3_FOUNDER_APPROVED_DESIGN_BASELINE.md`
**Source section:** `32. Adversarial, Negative, and Abuse Scenarios`
**Execution status:** `DESIGN_SCENARIOS_DEFINED_NOT_EXECUTED`
**Authority:** `DOCUMENTARY_DESIGN_ONLY`


| ID | Attack or failure | Required result |
| --- | --- | --- |
| HOR-ADV-001 | Create duplicate to escape restricted history | Open duplicate investigation; no clean-slate identity. |
| HOR-ADV-002 | Merge same-name horses deliberately | Deny without sufficient evidence. |
| HOR-ADV-003 | Change owner field to self | Deny; Item 03 relationship workflow. |
| HOR-ADV-004 | Claim ownership from payment | Deny inference. |
| HOR-ADV-005 | Claim ownership from possession or facility control | Deny inference. |
| HOR-ADV-006 | Claim continuing access from authorship | Deny or minimum lawful history. |
| HOR-ADV-007 | Enumerate horses by microchip or registry ID | Anti-enumeration denial. |
| HOR-ADV-008 | Seek precise location for stalking or theft | Suppress; preserve security evidence. |
| HOR-ADV-009 | Marketplace or registry overwrite of verified identity | Quarantine conflict. |
| HOR-ADV-010 | AI labels horse dangerous, lame, or low value | Prohibit conclusion and opaque score. |
| HOR-ADV-011 | Create new horse to hide prior injury or dispute | Duplicate/continuity controls preserve history subject to permission. |
| HOR-ADV-012 | Transfer used to erase former-party evidence | Preserve lawful history and audit. |
| HOR-ADV-013 | Transfer marked complete despite access or care failure | Block completion. |
| HOR-ADV-014 | Offline actor finalizes sale or merge | Proposal only. |
| HOR-ADV-015 | Unauthorized actor marks horse deceased | Deny or step-up. |
| HOR-ADV-016 | Memorial exposes cause of death, dispute, or location | Exclude restricted content. |
| HOR-ADV-017 | Bulk support access reveals horse data | Bounded ticketed access; broad access denied. |
| HOR-ADV-018 | Registry retracts prior data | Preserve source history and correction. |
| HOR-ADV-019 | Two tenants claim same horse | Controlled claim review without cross-tenant disclosure. |
| HOR-ADV-020 | Vendor deletion removes horse | Canonical identity remains. |
| HOR-ADV-021 | Eligibility fact manipulated to permit entry | Source/version check; workflow receives current fact only. |
| HOR-ADV-022 | Archived horse edited as active | Ordinary mutation denied. |
| HOR-ADV-023 | Merge used to gain access | Permission recalculated; no access expansion. |
| HOR-ADV-024 | Feature flag enables public profile | Flag cannot bypass approval or permission. |
| HOR-ADV-025 | Expected foal activated before live birth | Deny active-horse activation. |
| HOR-ADV-026 | Recipient mare treated as genetic dam or owner | Preserve distinct reproductive roles. |
| HOR-ADV-027 | Configuration update changes meaning of historical status | Block retroactive reinterpretation. |
| HOR-ADV-028 | OCR error becomes verified identifier | Keep as pending claim. |
| HOR-ADV-029 | Wrong horse selected during transfer or care handoff | Fail closed and preserve incident evidence. |
| HOR-ADV-030 | Stale Passport used after restriction | Revoke or deny at trusted boundary. |
| HOR-ADV-031 | Erroneous death event silently deleted | Require attributable successor correction. |
| HOR-ADV-032 | Migration match score auto-merges records | Quarantine and require governed review. |

| HOR-ADV-033 | Probe cross-tenant match repeatedly to discover whether a horse exists | Return bounded mediation or rate-limited denial without existence disclosure. |
| HOR-ADV-034 | Enumerate canonical Horse IDs through URLs or APIs | Use non-enumerable public-safe references; deny without disclosure. |
| HOR-ADV-035 | Reused registry number forces false merge | Namespace and effective-period qualification prevent convergence. |
| HOR-ADV-036 | DNA match is used to merge twins or clones | Prohibit merge based on genetic similarity alone. |
| HOR-ADV-037 | Forged or replayed share token requests private profile | Verify purpose, expiry, revocation, audience, and permission; deny replay. |
| HOR-ADV-038 | Revoked downloaded PDF is represented as current | Verification marks invalid or superseded; audit attempted reliance. |
| HOR-ADV-039 | Identity image leaks GPS EXIF or owner address | Sanitize derivative and block broad projection until safe. |
| HOR-ADV-040 | Rescue intake forces a guessed owner to satisfy schema | Permit unknown/disputed owner; prohibit relationship manufacture. |
