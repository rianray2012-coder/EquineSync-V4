# Equine Health V1.1 Requirement-to-Section Traceability

| Requirement | Requirement | Candidate section | Verification | Implementation |
| --- | --- | --- | --- | --- |
| `EH-REQ-001` | Observation, routine care, measurement, judgment, diagnosis, and instruction shall remain distinct | 19 | Record classification tests | `NOT_AUTHORIZED` |
| `EH-REQ-002` | Clinical authority shall require scoped current evidence | 20 | Provider authority tests | `NOT_AUTHORIZED` |
| `EH-REQ-003` | Provider category shall not imply another profession's authority | 20 | Cross-role denial | `NOT_AUTHORIZED` |
| `EH-REQ-004` | Every material health record shall preserve author/source/revision/time | 21 | Provenance tests | `NOT_AUTHORIZED` |
| `EH-REQ-005` | Amendments shall be non-destructive | 21 | Amendment lineage test | `NOT_AUTHORIZED` |
| `EH-REQ-006` | Private, operational, canonical, and projected notes shall remain classified | 21 and 29 | Projection tests | `NOT_AUTHORIZED` |
| `EH-REQ-007` | Medication order and administration shall remain separate | 22 | Event tests | `NOT_AUTHORIZED` |
| `EH-REQ-008` | Dose value, unit, route, timing, and source revision shall be explicit | 22 | Validation tests | `NOT_AUTHORIZED` |
| `EH-REQ-009` | Missed, refused, late, duplicate, and unknown doses shall remain distinct | 22 | State tests | `NOT_AUTHORIZED` |
| `EH-REQ-010` | Restricted treatments shall require applicable governed authority and enhanced audit | 22 | Policy denial tests | `NOT_AUTHORIZED` |
| `EH-REQ-011` | Alerts shall preserve source, severity, verification, expiry, and review | 23 | Alert lifecycle test | `NOT_AUTHORIZED` |
| `EH-REQ-012` | Medical-sensitive status shall be backend-redacted without medical permission | 4 and 11 | Payload regression tests | `NOT_AUTHORIZED` |
| `EH-REQ-013` | Biosecurity restrictions shall preserve source, scope, period, and release criteria | 24 | Restriction tests | `NOT_AUTHORIZED` |
| `EH-REQ-014` | Minimum operational alert shall not expose diagnosis unnecessarily | 24 | Projection tests | `NOT_AUTHORIZED` |
| `EH-REQ-015` | Welfare observations shall preserve observer, method, context, and confidence | 25 | Observation tests | `NOT_AUTHORIZED` |
| `EH-REQ-016` | Scores shall identify scale/version and limitations | 25 | Display/API tests | `NOT_AUTHORIZED` |
| `EH-REQ-017` | Emergency contact attempts, advice, handoff, and review shall be preserved | 26 and 34 | Emergency scenarios | `NOT_AUTHORIZED` |
| `EH-REQ-018` | Treatment authority and financial responsibility shall remain separate | 9, 28, and 34 | Authority tests | `NOT_AUTHORIZED` |
| `EH-REQ-019` | Euthanasia shall require accountable human and professional authority | 26 and 37 | High-consequence denial tests | `NOT_AUTHORIZED` |
| `EH-REQ-020` | AI shall not diagnose, prescribe, select treatment, or execute care | 16, 27, and 37 | Policy rejection tests | `NOT_AUTHORIZED` |
| `EH-REQ-021` | Clinical support shall show sources, freshness, uncertainty, and assumptions | 27 | Output validation | `NOT_AUTHORIZED` |
| `EH-REQ-022` | Conflicting instructions shall route to Claims, not latest-write resolution | 28 | Conflict tests | `NOT_AUTHORIZED` |
| `EH-REQ-023` | Health continuity shall use classified minimum-necessary projection | 29 | Transfer tests | `NOT_AUTHORIZED` |
| `EH-REQ-024` | Competition/regulatory claims shall not exceed authoritative evidence | 30 | Claim scan | `NOT_AUTHORIZED` |
| `EH-REQ-025` | Offline medication conflicts shall fail closed | 31 | Sync conflict tests | `NOT_AUTHORIZED` |
| `EH-REQ-026` | Offline data shall be horse/barn/actor/device/session scoped | 31 | Isolation tests | `NOT_AUTHORIZED` |
| `EH-REQ-027` | Device/import data shall preserve raw source, quality, and transformations | 32 | Import tests | `NOT_AUTHORIZED` |
| `EH-REQ-028` | Ambiguous horse identity shall quarantine imported health data | 32 | Match ambiguity tests | `NOT_AUTHORIZED` |
| `EH-REQ-029` | Retention shall not imply live access | 13 and 33 | Former-party tests | `NOT_AUTHORIZED` |
| `EH-REQ-030` | Welfare escalation shall preserve neutral state and spending uncertainty | 34 | Owner-unreachable tests | `NOT_AUTHORIZED` |
| `EH-REQ-031` | Minor health access shall be minimum necessary for safe participation | 35 | Minor projection tests | `NOT_AUTHORIZED` |
| `EH-REQ-032` | Research/model training shall require separate governed authority | 15 | Secondary-use denial | `NOT_AUTHORIZED` |
| `EH-REQ-033` | Consequential clinical access and changes shall be audited | 36 | Event tests | `NOT_AUTHORIZED` |
| `EH-REQ-034` | External systems shall not create authority or silently overwrite canonical truth | 14 and 32 | Adapter tests | `NOT_AUTHORIZED` |
| `EH-REQ-035` | Financial delinquency shall not block emergency recording or welfare escalation | 9 and 34 | Delinquency scenarios | `NOT_AUTHORIZED` |
