# Remaining PIA Dependency Graph

**Status:** `RECOMMENDED_NOT_APPROVED`  
**Implementation authority:** `FALSE`

```mermaid
flowchart TD
  G["Locked Governance and Founder Decisions"] --> S["PIA Master Standard V1.1"]
  G --> M["MIAP Planning Authority"]
  S --> P01["01 Identity Account Actor Onboarding"]
  M --> P01
  P01 --> P02["02 Facility Tenant Organization"]
  P01 --> P03["03 Relationship Authorization Permission"]
  P02 <--> P03
  P01 --> P04["04 Horse Identity Profile Lifecycle"]
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
  R["Qualified Review Runtime"] -. "currently unavailable" .-> P02
```

Arrows express authority or contract dependencies, not implementation sequence alone. The bidirectional 02/03 edge must be resolved through explicit interfaces: context informs permission evaluation, while authority constrains who may create, change, or use facility/tenant/organization records.
