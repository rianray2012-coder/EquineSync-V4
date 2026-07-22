# Data Dictionary

| Entity | Purpose | Stable identifier | Lifecycle | Tenant scoping | Public exposure |
|---|---|---|---|---|---|
| Tenant | Application isolation and operating-context boundary | `tenant_id` | DRAFT through ARCHIVED | Self | No |
| Facility | Stable physical or operational place identity | `facility_id` | DRAFT through ARCHIVED | Via TenantFacilityAssociation | No |
| Organization | Legal, operating, administrative, or service entity | `organization_id` | DRAFT through ARCHIVED | Via OrganizationTenantControl | No |
| FacilityArea | Contained structure, zone, space, or managed area | `facility_area_id` | DRAFT/ACTIVE/RESTRICTED/RETIRED/ARCHIVED | Inherited from facility association | No |
| TopologyEdge | Containment, adjacency, route, overlap, or shared-resource fact | `topology_edge_id` | PROPOSED/ACTIVE/SUPERSEDED/RETIRED | Same as subject facility | No |
| OrganizationTenantControl | Temporal organization control or administration of a tenant | `organization_tenant_control_id` | PROPOSED/ACTIVE/SUSPENDED/ENDED/DISPUTED/ARCHIVED | Tenant | No |
| TenantFacilityAssociation | Temporal tenant use or operation of a facility | `tenant_facility_association_id` | PROPOSED/ACTIVE/RESTRICTED/SUSPENDED/ENDED/DISPUTED/ARCHIVED | Tenant | No |
| FacilityStewardshipAssertion | Evidenced stewardship claim without permission effect | `stewardship_assertion_id` | SUBMITTED/UNDER_REVIEW/VERIFIED/REJECTED/DISPUTED/EXPIRED/ARCHIVED | Tenant | No |
| ActiveContext | Selected tenant and optional facility bound to a session | `context_id` | ACTIVE/STALE/REVOKED/EXPIRED | Tenant | No |
| ContextSwitchEvent | Audit evidence for prior/new active context | `context_switch_event_id` | IMMUTABLE_EVENT | Tenant | No |
| FacilityPublicProjection | Minimal separately governed discoverable projection | `public_projection_id` | DRAFT/ACTIVE/SUSPENDED/REVOKED/ARCHIVED | Source tenant | Yes, only active approved fields |
| DuplicateCandidate | Possible duplicate pair with confidence and evidence | `duplicate_candidate_id` | OPEN/UNDER_REVIEW/CONFIRMED/REJECTED/MERGED/ARCHIVED | Impacted tenant set | No |
| TopologyChange | Proposed/effective transfer, merge, split, restriction, or closure | `topology_change_id` | PROPOSED/UNDER_REVIEW/APPROVED/EFFECTIVE/RECONCILING/COMPLETE/REJECTED/ROLLED_BACK | Impacted tenant set | No |
| LegacyQuarantineRecord | Ambiguous imported legacy record | `legacy_quarantine_id` | QUARANTINED/UNDER_REVIEW/MAPPED/REJECTED/ARCHIVED | Known tenant or isolation quarantine | No |
| AddressVersion | Structured postal/geospatial address with source and precision | `address_version_id` | PROPOSED/VERIFIED/DISPUTED/SUPERSEDED | Same as subject | Public only through projection |
| ExternalIdentifier | Provider-neutral external reference | `external_identifier_id` | ACTIVE/DISPUTED/SUPERSEDED/REVOKED | Same as subject | No |
| LifecycleEvidence | Evidence supporting a material transition | `lifecycle_evidence_id` | SUBMITTED/VERIFIED/REJECTED/PRESERVED | Same as subject | No |
| ReconciliationCase | Cross-domain follow-up required by topology change | `reconciliation_case_id` | OPEN/IN_PROGRESS/BLOCKED/RESOLVED/ARCHIVED | Impacted tenant set | No |

Every material record also carries created/effective/updated time, provenance, actor attribution, lifecycle version, and record-stewardship metadata. Fields governed by another domain are references, not copied authority.
## V1.0.1 adaptive-onboarding additions

- `onboarding_purpose`: plain-language immediate purpose; never permission-bearing.
- `seed_justification`: why a minimum record is required.
- `authority_conferred`: always false for a seed or association absent a Permission-owned decision.
- `organization_id` and `facility_id`: optional during horse-first onboarding.
- `tenant_id`: isolation context only; does not imply a legal or physical entity.
- `association_effective_period`: temporal scope for later Facility/Organization association.
- `reversal_reference`: controlled reversal path preserving audit and history.
