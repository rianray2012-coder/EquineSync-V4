# Master Equine Health, Welfare, Medical Record, and Clinical Support Model V1.0

**Status:** Controlled draft for founder review  
**Constitutional state:** Not adopted; not locked; non-controlling  
**Authority:** Planning and companion-artifact reconciliation only

## 1. Purpose

This candidate defines constitutional semantics for equine welfare, health observations, medical records, medications, diagnostics, treatment plans, rehabilitation, clinical collaboration, emergency care, and permission-safe health projections across EquineSync.

It supports accurate records and coordinated care but does not practice veterinary medicine, diagnose, prescribe, establish a veterinarian-client-patient relationship, or replace licensed professional judgment.

## 2. Canon Boundaries

- Durable horse identity and Passport continuity remain governed by the Relationship and Horse Transfer canons.
- Final access and field projection remain governed by the Permission model.
- Record retention, correction, lawful erasure, legal hold, restoration, and stewardship remain governed by Record Stewardship.
- Contested claims and temporary restrictions remain governed by Claims and Authority.
- Consent and authorization evidence remain governed by Agreements and Consent.
- Financial responsibility, invoices, refunds, held funds, and settlement remain governed by Financial Truth.
- Provider adapters and external systems remain projections under External Architecture; they do not create EquineSync authority.
- Audit evidence and minimization remain governed by Audit.
- AI behavior remains default-off and governed by RF30 and the AI operating canon.
- Notifications and notice evidence remain governed by Communications.

This model owns health and clinical semantics, not identity, permission, payment, external-provider, or record-retention authority.

## 3. Health Information Classes

The model must distinguish:

- routine care and husbandry observations;
- welfare concerns;
- clinical observations and examination findings;
- diagnoses and differential diagnoses;
- medications, supplements, prescriptions, administration, and adherence;
- allergies, sensitivities, contraindications, and adverse reactions;
- laboratory, imaging, pathology, and diagnostic results;
- vaccination, dentistry, farrier, rehabilitation, and therapy records;
- treatment, monitoring, discharge, and follow-up plans;
- emergency, quarantine, infectious-disease, and biosecurity information;
- reproductive, genetic, insurance, and mortality information;
- provider-authored, owner-reported, staff-observed, imported, inferred, and system-projected data.

Source type and confidence must remain visible. Owner-reported or staff-observed information must not be silently relabeled as veterinarian-confirmed.

## 4. Medical Status and Welfare State

Statuses implying injury, illness, treatment restriction, quarantine, lameness, recovery, rehabilitation, stall rest, medical hold, or clinical limitation are medical-sensitive.

Restricted projections must redact medical-sensitive status consistently from core profile, equine profile, care flags, search, rosters, Calendar, analytics, exports, public shares, notifications, and external adapters unless final permission expressly allows it.

Non-medical operational status may remain visible only under the governing visibility model.

## 5. Clinical Authority

The system must represent claimed and verified professional authority, scope of practice, license jurisdiction where applicable, horse relationship, barn scope, effective period, and revocation state.

A provider account, appointment, uploaded document, signature, imported record, payment, or Care Circle membership does not by itself establish clinical authority. EquineSync records evidence and workflow state but does not adjudicate licensure or professional negligence.

## 6. Treatment Authorization and Consent

Treatment authority must remain distinct from legal ownership, custody, boarding, payment responsibility, emergency contact, and record access. A treatment decision must preserve:

- horse and stable identity;
- requesting and acting parties;
- authority basis and scope;
- consent or emergency basis;
- provider identity and role;
- effective time and expiration;
- source records and revisions;
- limitations, refusals, and revocation;
- audit correlation and notices.

Financial responsibility does not create treatment authority. Treatment authority does not create unrestricted record access.

## 7. Medication Safety

Medication records must distinguish order, prescription, dispense, inventory, administration instruction, scheduled dose, actual administration, refusal, omission, waste, reaction, discontinuation, and correction.

Required safety controls include horse identity, drug identity, dose, route, timing, prescriber or authority source, administering actor, duplicate-dose prevention, allergy and contraindication checks, withdrawal periods where relevant, and exception escalation.

Offline or uncertain state must fail closed for high-risk medication changes. AI and deterministic automation may not prescribe, alter dosage, or execute administration.

## 8. Care Plans and Clinical Collaboration

Care plans must be versioned, purpose-limited, attributable, and separated into professional instruction, owner direction, barn execution, and observed outcome. Tasks derived from care plans remain operational projections; completing a task must not rewrite the clinical source record.

Care Circle membership does not grant medical access. Providers, trainers, staff, guardians, owners, and facilities receive only approved projections needed for their current relationship and purpose.

## 9. Emergency and Welfare Escalation

Emergency workflows may support immediate welfare-preserving action within documented policy and law. Emergency access must be narrowly scoped, time-bound, attributable, logged, reviewed, and revoked when the emergency ends.

Emergency action does not create durable ownership, payment, provider, or record-access authority. The model must preserve uncertainty, failed contact attempts, decisions, interventions, transfer of care, and post-event review.

Welfare concerns must distinguish observation, allegation, triage, restriction, professional assessment, action, and outcome. The platform must not present an unverified concern as a diagnosis or adjudicated fact.

## 10. Quarantine, Biosecurity, and Movement

Quarantine and infectious-disease controls may restrict movement, facility assignment, participation, and visibility. Such restrictions require source, authority, scope, duration, review date, and release criteria.

Minimum-necessary operational alerts may be projected without exposing diagnosis or detailed medical records. RF27 retains physical location ownership; this model supplies health restrictions and release state.

## 11. Passport and Care Circle Projection

The backend payload is the primary privacy boundary. Whenever medical permission is false, medical-sensitive fields must be stripped or null before response serialization, including medications, allergies, medical flags, rehab or stall-rest state, and medical-sensitive status aliases.

Frontend hiding is defense in depth only. Every Passport and Care Circle panel must independently refuse to render medical-sensitive data without explicit medical permission.

Shared or public horse views must use a separate allowlisted projection and must never inherit authenticated internal fields by subtraction.

## 12. Corrections, Disputes, and Provenance

Records must be append-only or version-preserving where required. Corrections must retain original value, corrected value, reason, actor, time, authority, and audit lineage. A correction must not erase authorship or silently alter external source evidence.

Disputed ownership, treatment authority, diagnosis, invoice, provider conduct, or record accuracy must route through the controlling claims model. EquineSync preserves competing assertions and restrictions without adjudicating legal or clinical truth.

## 13. Retention, Death, and Historical Continuity

Horse sale, lease, move, retirement, transfer, account closure, provider departure, or death must not destroy clinical history. Direct access must be recalculated while lawful retention, stewardship, authorship, audit, insurance, dispute, and transfer continuity are preserved.

End-of-life, mortality, necropsy, donation, insurance, and memorial data require heightened privacy, respectful handling, and purpose limitation.

## 14. External Clinical Systems

External practice systems, labs, pharmacies, insurers, registries, and devices remain replaceable adapters. Imports require stable horse identity, source identity, revision, provenance, idempotency, reconciliation, and quarantine for ambiguous matches.

No external provider may silently overwrite canonical EquineSync records or broaden authority. Export and synchronization require separate authorization and failure/degraded-state rules.

## 15. Analytics and Research

Analytics must use minimum necessary, permission-safe, purpose-limited data. Operational metrics must not expose medical detail through small cohorts, labels, filters, exports, or inferred status.

Research, model training, benchmarking, or secondary use requires separate governed authority, consent or lawful basis, de-identification assessment, retention limits, and opt-out or withdrawal handling where applicable.

## 16. AI and Clinical Support

AI may summarize or organize only permission-safe, source-grounded context under separately authorized capability classes. It must disclose uncertainty and citations, fail closed on missing authority, and never autonomously diagnose, prescribe, alter treatment, contact providers, execute prepared actions, or mutate records.

Medical-sensitive data must be redacted before provider input where permission is absent. Real model calls, provider credentials, tools, and production inference remain unauthorized unless a later governed phase explicitly allows them.

## 17. Required Health Events

Material changes must emit idempotent, retryable, observable, and auditable impact events for permission recalculation, Passport projection, Care Circle, Calendar participation, tasks, notifications, movement restrictions, external adapters, and local-session invalidation.

Events must include horse identity, barn scope, source and revision, actor, authority basis, reason, policy version, correlation, causation, before/after state, confidentiality, and minimum-necessary audit metadata.

## 18. Prohibited Outcomes

The system must not:

- infer clinical truth from payment, possession, upload, OCR, AI, or informal statement;
- expose medical-sensitive status without medical permission;
- treat Care Circle membership as medical authorization;
- let external systems create canonical authority;
- silently overwrite or delete clinical lineage;
- present operational reminders as prescriptions;
- permit AI or automation to diagnose, prescribe, or execute treatment;
- represent this draft as adopted, implemented, or operational.

## 19. Founder Review Questions

Founder review must decide veterinary verification levels, emergency override limits, high-risk medication classes, biosecurity notice projections, jurisdiction policy, record correction workflow, retention exceptions, research use, reproductive and genetic privacy, insurance access, and end-of-life visibility.

## 20. Non-Authority Attestation

This draft creates no schema, migration, role, permission, route, workflow, clinical act, provider integration, production behavior, public claim, onboarding rule, or launch authority.

