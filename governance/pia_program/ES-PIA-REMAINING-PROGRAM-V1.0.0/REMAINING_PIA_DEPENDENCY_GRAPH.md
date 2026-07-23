# Remaining PIA Dependency Graph

**Status:** `ITEM04_DOCUMENTARY_DESIGN_INTEGRATED_FOUNDER_APPROVED_PENDING_REVIEW`
**Implementation authority:** `FALSE`

```mermaid
flowchart TD
  G["Locked Governance and Founder Documentary Decisions"] --> S["PIA Master Standard V1.1"]
  G --> M["MIAP Planning Authority"]
  S --> P01["01 Identity Account Actor Onboarding"]
  M --> P01
  P01 --> P02["02 Facility Tenant Organization"]
  P01 --> P03["03 Relationship Authorization Permission"]
  P02 <--> P03
  P01 --> P04["04 Horse Identity Profile Lifecycle V0.3 Documentary"]
  P02 --> P04
  P03 --> P04
  P04 --> P07["07 Care Operations"]
  P02 --> P07
  P03 --> P07
  P04 --> P08["08 Lessons Training Rider Guardian"]
  P03 --> P08
  P07 --> P08
  P07 --> P06["06 Task Calendar Scheduling Notification"]
  P08 --> P06
  P06 --> P09["09 Billing Payments Financial Operations"]
  P07 --> P09
  P08 --> P09
  P06 --> P10["10 Owner Portal Communications"]
  P07 --> P10
  P08 --> P10
  P09 --> P10
  P02 --> P05["05 Core Navigation Search Application Shell"]
  P03 --> P05
  P04 --> P05
  P06 --> P05
  P07 --> P05
  P08 --> P05
  P09 --> P05
  P10 --> P05
  X["Cross-PIA Privacy Audit Records Offline AI Integration Configuration Resilience"] -.-> P01
  X -.-> P02
  X -.-> P03
  X -.-> P04
  X -.-> P05
  X -.-> P06
  X -.-> P07
  X -.-> P08
  X -.-> P09
  X -.-> P10
  D1["GFD-001 competition/show/travel allocation"] -.-> P04
  D1 -.-> P06
  D1 -.-> P08
  D1 -.-> P09
  D2["GFD-002 asset/service-request allocation"] -.-> P02
  D2 -.-> P06
  D2 -.-> P07
  D2 -.-> P09
  D3["GFD-003 provider allocation"] -.-> P03
  D3 -.-> P07
  D3 -.-> P09
  D3 -.-> P10
  D4["GFD-004 no Item 11; domain truth plus Item 05 surfaces"] -.-> P05
  HFD["HOR-FD-001 through HOR-FD-017 Item 04 documentary approvals"] -.-> P04
  R["GFD-007 compliant review runtime policy"] -. "approved policy; runtime not provisioned" .-> P02
  R -. "fresh review pending" .-> P03
  R -. "fresh review pending" .-> P04
```

Arrows express documentary authority or contract dependencies, not implementation sequence or execution authority. Item 04 V0.3 may inform downstream documentary drafting, but it is not independently reviewed, adopted, ratified, implementation-ready, operational, released, or enrollment-ready. The GFD and HOR-FD approvals do not provision a review runtime, change schemas, modify product behavior, or authorize deployment.
