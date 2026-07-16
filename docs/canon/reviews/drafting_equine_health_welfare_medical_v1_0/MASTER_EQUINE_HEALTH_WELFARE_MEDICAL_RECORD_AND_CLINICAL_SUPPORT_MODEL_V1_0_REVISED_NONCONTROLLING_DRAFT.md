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

## 19. Clinical Record and Judgment Separation

The model must preserve explicit distinctions among welfare observation, routine care record, clinical measurement, medical record, professional judgment, diagnosis, treatment instruction, medication order, emergency directive, and operational task.

An observation may prompt escalation but must not be relabeled as a diagnosis. A task completion records operational performance but does not prove treatment effectiveness. A clinical decision remains attributable to the qualified professional who made it.

## 20. Actor and Professional Boundaries

- Veterinarians may create professional clinical judgments and treatment instructions only within verified scope and relationship.
- Owners or authorized care decision-makers may consent, report history, and choose among professionally presented options within their authority.
- Facilities, trainers, and staff may observe, execute authorized care, document administration, and escalate; they may not convert operations into diagnosis or prescription.
- Farriers, therapists, nutritionists, bodyworkers, laboratories, and other providers retain distinct professional scopes. One provider category does not inherit another's authority.
- Guardians managing a minor's participation do not gain horse treatment authority unless separately established.

Professional credential display must preserve issuer, jurisdiction, scope, verification method, verification time, expiration, limitations, and dispute state. Credential status is not a platform endorsement or guarantee of quality.

## 21. Medical Record Provenance and Amendment

Every material health record must preserve horse identity, author, effective actor, professional role where claimed, source system, event time, recorded time, verification state, source revision, confidentiality, and audit correlation.

Amendments must be non-destructive. Late entries, corrections, addenda, retractions, disputed entries, and superseding instructions remain distinct. The system must not silently rewrite a provider-authored record because another party disagrees.

Private provider notes, facility execution notes, owner observations, and horse-canonical continuity records require separate classifications. Transferability and disclosure depend on purpose, authority, permission, and governing record policy.

## 22. Medication Order and Administration Model

Medication data must preserve normalized and source text for drug, concentration, dose value and unit, route, frequency, start/end, as-needed conditions, maximum limits, withdrawal period, refill status, ordering authority, and source revision.

Administration records must preserve scheduled time, actual time, actor, amount, route, outcome, refusal, omission, delay, waste, adverse reaction, and correction. Missed, refused, late, duplicate, and uncertain doses are not interchangeable.

Controlled substances and legally restricted treatments require jurisdiction-specific policy, restricted access, enhanced audit, inventory reconciliation where applicable, and licensed-professional involvement. This candidate does not define drug schedules or authorize controlled-substance handling.

## 23. Alerts and Emergency Information

Allergies, sensitivities, contraindications, prior reactions, emergency contacts, advance instructions, and critical alerts require source, verification, severity, effective period, and review date.

Alerts must be conspicuous to authorized care actors but must not broaden access to unrelated clinical history. A stale or unverified alert must be visibly qualified rather than silently discarded or presented as certain.

## 24. Infectious Disease and Biosecurity

Vaccination, test, exposure, infectious-disease, quarantine, isolation, clearance, and biosecurity records must preserve pathogen or condition terminology, source, specimen or administration time, result state, uncertainty, authority, facility impact, restriction period, and release criteria.

Minimum-necessary operational alerts may support separation and movement controls without exposing diagnosis. Cross-facility disclosure and public-health reporting require separate lawful authority and verified routing.

## 25. Welfare Observation Vocabulary

Welfare observations may include injury, illness signs, lameness, pain behavior, body-condition change, hydration, appetite, feeding, manure, urination, mobility, behavior change, environment, neglect indicators, and inability to obtain care.

Observations must preserve the observer, method, context, confidence, media provenance, and escalation status. Scales and scores must identify their version and limitations. They must not be presented as diagnoses or guaranteed welfare outcomes.

## 26. Referral, Hospitalization, Transport, and End of Life

Emergency escalation must preserve contact attempts, professional advice, transport decision, destination, referral, handoff, hospitalization, discharge, and follow-up. Transport authorization, treatment authorization, and payment responsibility remain separate.

Euthanasia and other end-of-life decisions require verified authority, licensed-professional involvement where required, explicit consent or lawful emergency basis, humane-welfare priority, role separation, and enhanced audit. EquineSync must not make or automate the decision.

Death, necropsy, remains disposition, insurance, memorial, and historical Passport records require respectful, restricted, purpose-limited handling.

## 27. Clinical Decision Support

Any future clinical support output must be labeled as support rather than diagnosis or treatment, identify its sources and freshness, state uncertainty and missing information, expose material assumptions, and require qualified human review.

AI must not determine lameness, diagnosis, prognosis, emergency necessity, treatment selection, dose, withdrawal compliance, euthanasia, neglect, or professional misconduct. Model confidence cannot substitute for clinical authority.

## 28. Consent, Advance Instructions, and Authority Disputes

The system must preserve owner or authorized decision-maker consent, refusal, advance instruction, spending limit, emergency instruction, delegated care authority, expiration, revocation, and provider acknowledgment as distinct records.

Conflicting instructions must not be resolved by newest timestamp, payment status, possession, or role label. Immediate welfare may support a narrow temporary action, while the authority dispute routes to Claims review.

## 29. Continuity and Note Classification

Sale, lease, transfer, boarding departure, provider change, facility closure, and account closure must recalculate access without fragmenting the horse's durable clinical history.

The continuity package must distinguish transferable horse-health facts, active care plans, critical alerts, source documents, private provider notes, facility-retained operations, disputed records, and restricted third-party information. No blanket transfer is permitted.

## 30. Competition and Regulatory Documentation

Competition medication, vaccination, health certificate, withdrawal, testing, registry, insurance, and governing-body documents may be stored with source and validity metadata. EquineSync must not claim eligibility, compliance, certification, or acceptance unless an authoritative source has confirmed the exact claim and scope.

Rules change by jurisdiction and governing body. Stale or conflicting rules must fail to qualified review rather than produce a compliance guarantee.

## 31. Offline Clinical Operations

Offline administration and observation must be actor-, horse-, barn-, device-, and session-scoped. The local system must preserve event time, recorded time, source instruction revision, pending state, and integrity evidence.

Conflicting medication entries, stale instructions, duplicate-dose risk, revoked authority, and uncertain synchronization must fail closed and require reconciliation. Offline state must never claim provider notice, external prescription verification, or canonical acceptance before synchronization.

Emergency minimum data may be cached only under approved permission, encryption, expiry, logout purge, and revocation controls.

## 32. Devices, Sensors, Laboratories, Imaging, and Uploads

Device, wearable, sensor, laboratory, imaging, OCR, and uploaded-document data must preserve device or source identity, calibration or quality metadata where available, capture time, import time, transformations, original artifact, confidence, and verification.

Imported measurements remain source evidence. They do not become verified diagnosis, provider-authored judgment, or canonical authority through ingestion alone. Ambiguous horse identity must be quarantined.

## 33. Retention and Cryptographic Deletion Boundary

Retention schedules, legal holds, restoration, deletion eligibility, and cryptographic deletion remain owned by Record Stewardship and Data Protection. This model supplies health sensitivity, continuity, safety, and professional-record requirements for those decisions.

Deletion must not silently remove active safety alerts, legal-hold evidence, correction history, or required clinical continuity. Retention does not imply continuing application access.

## 34. Welfare Escalation When Authority Is Unavailable

When an owner or authorized decision-maker cannot be reached, the platform may support policy-based escalation to verified contacts and qualified professionals. It must distinguish contact failure, professional advice, immediate welfare action, temporary authority basis, expense uncertainty, and later ratification or dispute.

Financial delinquency must not block emergency recording or welfare escalation. This model does not create authority to incur unlimited expense.

## 35. Minors and Horse Health Information

Minor participation in horse care must be developmentally appropriate, supervised where required, and limited to the minimum information needed for safe assigned activity. Guardian status concerning the minor does not automatically grant the guardian the horse's medical record.

Safeguarding restrictions, prohibited contact, clinical privacy, and horse-owner authority must be evaluated together. Minor-facing interfaces must not expose private provider notes, financial data, disputes, or unrelated owner information.

## 36. Required Clinical Audit Evidence

Consequential events include record creation and amendment, medical-sensitive access, alert changes, medication order and administration, missed or refused dose, adverse reaction, emergency access, authority change, quarantine, release, referral, transfer package creation, export, external adapter event, AI support generation, and deletion or hold action.

Audit evidence must preserve actor chain, source revision, authority snapshot, before/after state, reason, event and recorded times, confidentiality, correlation, and minimum-necessary metadata.

## 37. Non-Delegable Professional and Human Decisions

Diagnosis, prescription, dosage change, prognosis, euthanasia, controlled-substance authority, final neglect finding, professional misconduct, quarantine release where professional authority is required, and emergency clinical decision must not be delegated to AI or unattended automation.

Deterministic systems may enforce an already-authorized schedule or restriction only under a separately approved implementation plan with human override and audit.

## 38. Founder Review Questions

Founder review must decide veterinary and provider verification levels, clinical versus operational record classifications, emergency override and spending limits, high-risk medication and controlled-substance boundaries, biosecurity notice projections, jurisdiction policy, private-note transferability, offline medication conflict posture, device-data trust, continuity-package defaults, research and model-training use, reproductive and genetic privacy, competition claim posture, minor access, insurance access, welfare escalation, and end-of-life visibility.

## 39. Non-Authority Attestation

This draft creates no schema, migration, role, permission, route, workflow, clinical act, provider integration, production behavior, public claim, onboarding rule, or launch authority.
