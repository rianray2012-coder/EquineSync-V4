# Equine Health Requirement Extraction Index

**Status:** `NONAUTHORITATIVE_PRELIMINARY_REVIEW_ANALYSIS`; does not replace the exact Governance Requirement Index V1.1.

| ID | Requirement | Risk | Proposed verification |
| --- | --- | --- | --- |
| EH-REQ-001 | Observation, routine care, measurement, judgment, diagnosis, and instruction shall remain distinct | Clinical/Data integrity | Record classification tests |
| EH-REQ-002 | Clinical authority shall require scoped current evidence | Safety/Legal | Provider authority tests |
| EH-REQ-003 | Provider category shall not imply another profession's authority | Safety | Cross-role denial |
| EH-REQ-004 | Every material health record shall preserve author/source/revision/time | Data integrity | Provenance tests |
| EH-REQ-005 | Amendments shall be non-destructive | Clinical/Audit | Amendment lineage test |
| EH-REQ-006 | Private, operational, canonical, and projected notes shall remain classified | Privacy/Continuity | Projection tests |
| EH-REQ-007 | Medication order and administration shall remain separate | Medication safety | Event tests |
| EH-REQ-008 | Dose value, unit, route, timing, and source revision shall be explicit | Medication safety | Validation tests |
| EH-REQ-009 | Missed, refused, late, duplicate, and unknown doses shall remain distinct | Medication safety | State tests |
| EH-REQ-010 | Restricted treatments shall require applicable governed authority and enhanced audit | Legal/Safety | Policy denial tests |
| EH-REQ-011 | Alerts shall preserve source, severity, verification, expiry, and review | Safety | Alert lifecycle test |
| EH-REQ-012 | Medical-sensitive status shall be backend-redacted without medical permission | Privacy | Payload regression tests |
| EH-REQ-013 | Biosecurity restrictions shall preserve source, scope, period, and release criteria | Welfare/Operations | Restriction tests |
| EH-REQ-014 | Minimum operational alert shall not expose diagnosis unnecessarily | Privacy/Safety | Projection tests |
| EH-REQ-015 | Welfare observations shall preserve observer, method, context, and confidence | Welfare/Data integrity | Observation tests |
| EH-REQ-016 | Scores shall identify scale/version and limitations | Clinical trust | Display/API tests |
| EH-REQ-017 | Emergency contact attempts, advice, handoff, and review shall be preserved | Welfare/Audit | Emergency scenarios |
| EH-REQ-018 | Treatment authority and financial responsibility shall remain separate | Legal/Financial | Authority tests |
| EH-REQ-019 | Euthanasia shall require accountable human and professional authority | Welfare/Legal | High-consequence denial tests |
| EH-REQ-020 | AI shall not diagnose, prescribe, select treatment, or execute care | AI/Safety | Policy rejection tests |
| EH-REQ-021 | Clinical support shall show sources, freshness, uncertainty, and assumptions | Clinical trust | Output validation |
| EH-REQ-022 | Conflicting instructions shall route to Claims, not latest-write resolution | Safety | Conflict tests |
| EH-REQ-023 | Health continuity shall use classified minimum-necessary projection | Privacy/Continuity | Transfer tests |
| EH-REQ-024 | Competition/regulatory claims shall not exceed authoritative evidence | Legal/Trust | Claim scan |
| EH-REQ-025 | Offline medication conflicts shall fail closed | Medication safety/Offline | Sync conflict tests |
| EH-REQ-026 | Offline data shall be horse/barn/actor/device/session scoped | Security | Isolation tests |
| EH-REQ-027 | Device/import data shall preserve raw source, quality, and transformations | Data integrity | Import tests |
| EH-REQ-028 | Ambiguous horse identity shall quarantine imported health data | Identity/Safety | Match ambiguity tests |
| EH-REQ-029 | Retention shall not imply live access | Privacy/Stewardship | Former-party tests |
| EH-REQ-030 | Welfare escalation shall preserve neutral state and spending uncertainty | Welfare/Legal | Owner-unreachable tests |
| EH-REQ-031 | Minor health access shall be minimum necessary for safe participation | Safeguarding/Privacy | Minor projection tests |
| EH-REQ-032 | Research/model training shall require separate governed authority | Privacy/AI | Secondary-use denial |
| EH-REQ-033 | Consequential clinical access and changes shall be audited | Audit | Event tests |
| EH-REQ-034 | External systems shall not create authority or silently overwrite canonical truth | Integration/Data integrity | Adapter tests |
| EH-REQ-035 | Financial delinquency shall not block emergency recording or welfare escalation | Welfare/Financial | Delinquency scenarios |

