# Master Minor, Guardianship, Safeguarding, and Delegated-Assistance Canon V1.0

**Status:** Controlled draft for founder review  
**Constitutional state:** Not adopted; not locked; non-controlling  
**Authority:** Planning and companion-artifact reconciliation only

## 1. Purpose

This candidate defines the heightened constitutional safeguards EquineSync must apply when a person is a minor, protected participant, dependent adult, assisted user, or subject to guardian, delegated-assistance, prohibited-contact, or safety restrictions.

It is a broad baseline for currently identified safeguarding domains, subject to explicit edge-case review and governed extension. It does not determine legal capacity, adjudicate guardianship, create custody, or replace professional or legal advice.

## 2. Governing Boundaries

- The Identity model governs durable person, account, actor, representative, and session identity.
- The Relationship model governs guardian, dependent, participant, caregiver, organization, and delegation relationship semantics.
- The Agreement and Consent model governs assent, consent, acceptance, withdrawal, purpose, and evidence.
- The Permission model makes final authorization and field-projection decisions.
- The Claims and Authority model governs contested assertions, disputes, and temporary restrictions.
- Record Stewardship governs retention, lawful erasure, legal hold, restoration, authorship, and historical access.
- Communications governs notice eligibility, delivery, evidence, failures, and escalation.
- Media governance controls image, video, file, consent, use, and publication restrictions.
- Calendar governs event identity and participation; this canon adds safeguarding visibility and contact limits.
- Physical barn and facility canons govern operational work and location; this canon adds participant protections.
- Audit governance controls evidence quality and minimization.

Relationship or guardian evidence informs authorization but never independently grants field-level access.

## 3. Protected Subjects and Actors

The model must distinguish:

- minor and age-of-majority status;
- guardian, parent, custodian, authorized representative, emergency contact, and payer;
- protected participant and dependent adult;
- assisted user and accessibility support person;
- delegated helper, staff member, trainer, volunteer, provider, transporter, and photographer;
- alleged, verified, expired, revoked, superseded, disputed, and prohibited relationships.

One actor may hold multiple roles, but those roles must not be collapsed. Payer status does not create guardianship. Guardian status does not create horse ownership. Emergency contact status does not create routine access.

## 4. Evidence and Verification

Material safeguarding authority requires a versioned record of source, scope, subject, actor, jurisdiction where applicable, effective period, verification state, confidence, reviewer, policy version, and audit correlation.

Imported, inferred, OCR-derived, AI-extracted, self-asserted, or display-only relationships remain unverified and must not become durable authority without governed promotion and review.

Periodic or event-driven reverification is required for expiring guardianship, delegated authority, transport authority, emergency contacts, temporary Care Circle access, and organization representatives.

## 5. Consent, Assent, and Capacity

Consent and assent must be purpose-limited, versioned, revocable where permitted, and separate from authorization. The system must preserve:

- the exact purpose and scope;
- presented text and version;
- subject and accepting actor;
- authority basis;
- assent and guardian consent separately when both are required;
- effective, expiration, withdrawal, and supersession times;
- jurisdiction and recipient or processor;
- evidence and notice lineage.

A user interface acknowledgment is not proof of legal capacity. Lack of capacity must not be inferred solely from age, disability, assistance, or account state.

## 6. Delegated Assistance

Delegated assistance must identify delegator, delegate, purpose, permitted actions, prohibited actions, data classes, horses, barns, facilities, effective period, acceptance, revocation, re-delegation rule, and audit lineage.

A delegate cannot receive more authority than the delegator currently holds. Delegation cannot bypass mandatory review, guardian rules, medical restrictions, financial limits, prohibited-contact controls, or field-level projection.

Account sharing is not delegation. Assistance must use distinct actor identity and attributable actions.

## 7. Contact and Visibility

Safeguarding-sensitive relationships and contact details require restricted visibility. The system must support:

- confidential and restricted contacts;
- prohibited contact and do-not-notify rules;
- guardian copies and alternate recipients;
- emergency escalation;
- post-termination notices;
- minimum necessary disclosure;
- non-existence or busy-only projection where relationship existence is sensitive.

Notification eligibility remains separate from authority. Failed delivery does not prove notice unless the controlling notice model says otherwise.

## 8. Search, Media, and Discovery

Minors and protected participants must not be broadly discoverable by default. Search, rosters, directories, leaderboards, public profiles, media galleries, exports, analytics, and external projections must apply minimum-exposure rules.

Media capture, storage, sharing, marketing use, biometric use, and publication require the governing media and consent controls. Withdrawal must stop future authorized use where required without silently destroying retained evidence.

## 9. Calendar, Lessons, and Physical Operations

Calendar and operational views must prevent leakage of confidential participation, location, medical, financial, transportation, and contact information. Guardian visibility must be scoped to the participant, event, purpose, and effective relationship.

Pickup, release, transport, lesson attendance, overnight stay, emergency handoff, and restricted-access events require explicit operational authority. A calendar invitation does not create pickup, transport, treatment, or custody authority.

## 10. Health and Emergency Boundaries

Emergency safety action may preserve life and welfare but must be narrowly scoped, time-bound, attributable, and reviewed. Emergency action does not create durable guardian, treatment, financial, or access authority.

Medical details remain governed by the Equine Health candidate for horse data and applicable human privacy/safety controls for participant data. Safeguarding status must not be used to expose diagnosis, medication, disability, or protected health information.

## 11. Financial and Agreement Boundaries

Guardian, owner, participant, payer, guarantor, invoice recipient, refund recipient, and payment-method owner remain distinct. A payment relationship must not expose safeguarding records or create decision authority.

Agreements signed by or for a protected participant must preserve actor, claimed authority, acceptance basis, text version, and later dispute or revocation evidence. EquineSync records claims and evidence but does not adjudicate legal validity.

## 12. Transfer, Departure, and Historical Continuity

Horse transfer, participant departure, organization change, account closure, and relationship termination must trigger permission recalculation. Historical authorship, audit evidence, lawful retention, dispute participation, and required notices may survive while direct application access ends.

Inactive accounts do not erase people or historical relationships. Reactivation must recalculate current authority rather than restore prior access automatically.

## 13. Offline, Mobile, and Session Safety

Protected data stored locally must be actor-, barn-, and authenticated-session-scoped, encrypted where required, minimized, and purged or invalidated on logout and relationship revocation. Offline queues and drafts must not cross users, barns, or sessions.

Offline uncertainty must fail closed for high-risk actions including pickup release, transport, guardian changes, prohibited-contact overrides, financial authorization, and sensitive disclosure.

## 14. AI and Automation

AI may not infer, create, promote, resolve, suspend, or supersede guardianship, capacity, prohibited-contact, or safeguarding authority. It may not autonomously contact a minor, recommend bypassing a guardian restriction, or disclose protected information.

Any future AI support must use permission-safe projections, explicit uncertainty, source lineage, human review, and the RF30 default-off boundaries. High-risk actions remain prohibited unless separately governed.

## 15. Incidents and Safety Restrictions

Reports of abuse, harassment, neglect, prohibited contact, unsafe transport, identity misuse, or boundary violations require restricted intake, evidence minimization, need-to-know access, retaliation protection, escalation, preservation, and documented closure criteria.

EquineSync must distinguish allegation, observation, evidence, temporary restriction, decision, and outcome. The platform does not determine criminal, civil, custody, or guardianship liability.

## 16. Required Safeguarding Events

Material changes must emit idempotent, retryable, observable, and auditable impact events for permission recalculation, session review, Calendar participation, notifications, Care Circle, media visibility, local-data invalidation, agreements, and external adapter projections.

Events must include actor, subject, barn or organization scope, reason, source revision, policy version, correlation, causation, before/after state, and privacy classification.

## 17. Prohibited Outcomes

The system must not:

- treat self-assertion as verified guardian authority;
- expose a protected participant through broad search or public media by default;
- allow prohibited actors to regain access through another role;
- use payer status as guardian authority;
- restore access automatically after account reactivation;
- permit shared accounts or unattributed delegated actions;
- let external vendors create EquineSync authority;
- represent this draft as adopted, implemented, or operational.

## 18. Canonical Definitions

- **Minor:** a person who has not reached the applicable age of majority, subject to verified emancipation or other controlling status. Age alone does not prove capacity or authority.
- **Guardian:** a verified person or entity with scoped, current authority concerning a minor or protected participant. Parent, payer, emergency contact, or account creator is not automatically a guardian.
- **Authorized adult:** an adult granted a defined purpose, scope, duration, and action set by valid authority; not a substitute guardian.
- **Caregiver:** a person responsible for specified care or supervision activities without implied legal, financial, or platform-wide authority.
- **Instructor or trainer:** a professional or operational actor providing instruction or training within an active relationship and approved scope.
- **Provider:** a professional or service actor whose access is limited to the service purpose, horse or participant, time, and permitted records.
- **Staff member:** a person acting for an organization under an attributable membership and assigned duties.
- **Volunteer:** a non-employee actor with explicit, narrow, supervised duties and no authority implied by presence or goodwill.
- **Delegated assistant:** a distinct actor permitted to perform enumerated assistance for a delegator; shared credentials are prohibited.
- **Safeguarding authority:** verified, scoped authority to receive, triage, restrict, review, escalate, or decide safeguarding matters. It is separate from guardian, employment, and platform-administration status.
- **Protected participant:** a person subject to heightened safety, privacy, capacity, dependency, or retaliation protections under policy or verified circumstances.
- **Safeguarding record:** an allegation, observation, report, triage, restriction, review, decision, evidence, notice, or outcome whose disclosure could create safety, privacy, retaliation, or due-process risk.

## 19. Guardian Lifecycle and Conflicts

Guardian authority must preserve identity, authority source, scope, subject, effective and expiry time, jurisdiction where applicable, verification state, restrictions, substitution, revocation, and dispute state.

Multiple guardians must remain distinct. The system must not use latest update, account seniority, payment history, or a broad `parent` label to resolve conflicting instructions. A conflict must trigger a minimum-necessary temporary safety posture and designated human review under the Claims canon.

Substitution, death, incapacity, court-order change, expiration, and revocation must trigger permission recalculation, session review, notification-route review, and local-data invalidation. Historical attribution and required evidence survive.

## 20. Age Transition and Account Development

Reaching majority is a governed transition, not an automatic midnight transfer of all access or records. The transition must verify applicable age and status, notify affected parties as permitted, recalculate permissions, preserve historical guardian attribution, review active consents and delegations, and give the new adult meaningful control consistent with law and policy.

Youth experiences must be developmentally appropriate, privacy-preserving, and limited by capability. Minor-facing interfaces must not expose adult financial, dispute, allegation, medical, location, or contact records merely because the minor is the subject of an event.

Supervised access must preserve the minor as a distinct person and actor where appropriate. Guardian-managed access must not conceal which human performed an action.

## 21. Communications and Contact Controls

Direct messages, group messages, attachments, media, live location, contact details, schedules, transportation plans, and invitation links require safeguarding-aware recipient and content projection.

One-to-one adult/minor communication must follow a founder-approved policy defining permitted relationship, purpose, guardian visibility or approved organizational oversight, quiet hours, deletion restrictions, reporting access, and auditable metadata. Private channels must not defeat prohibited-contact or organization-removal controls.

Observable controls should preserve safety evidence while minimizing unnecessary inspection of ordinary communications. Monitoring must be disclosed, purpose-limited, role-separated, and itself audited.

## 22. Boundary-Risk Indicators

The platform may support reporting or human-review cues concerning grooming, harassment, exploitation, retaliation, intimidation, coercion, sexualized conduct, secrecy demands, inappropriate gifts, isolation, repeated boundary crossing, or prohibited contact.

Indicators are not findings of fact. Automated scoring must not determine credibility, guilt, guardian fitness, professional fitness, or disciplinary outcome. Consequential classifications require trained human review and neutral language.

## 23. Reporting, Triage, and Anti-Retaliation

Reports must support safe intake, anonymous or confidential handling where policy permits, immediate-risk flags, evidence preservation, restricted access, conflict-of-interest routing, status communication, and anti-retaliation controls.

Good-faith reports must not be discouraged because they are incomplete or later unsubstantiated. Deliberately malicious conduct may be handled separately only through evidence-based human review. Mistaken, duplicate, unsupported, malicious, and withdrawn reports are distinct states.

EquineSync may route a matter to an authorized human or external reporting channel but must not claim to decide whether a legal reporting duty exists. Jurisdiction-specific mandated-reporting policy requires separate founder-approved rules and qualified review.

## 24. Emergency and Imminent Risk

Imminent-risk handling must prioritize immediate safety, emergency services where appropriate, minimum-necessary disclosure, reliable recipient escalation, failed-contact handling, and preservation of the actor and evidence chain.

Emergency controls must expire, be reviewed, and never become permanent authority by inertia. A safety restriction does not prove the underlying allegation.

## 25. Responsibility Boundaries

Facilities and organizations govern their personnel, supervision, operating policies, and response duties. Instructors and trainers govern professional conduct within their role. Guardians govern only their verified scope. EquineSync governs platform controls, evidence, access enforcement, and truthful status representation.

No party may shift its legal or professional duty to another simply because EquineSync stores a record or delivers a notice.

## 26. External Frameworks and Credentials

SafeSport, governing bodies, background-check services, credential registries, and similar frameworks remain external evidence or adapters. EquineSync must not claim certification, clearance, continuous monitoring, legal compliance, or suitability unless supported by current authoritative evidence and accurately scoped.

Background-check state must distinguish not requested, pending, completed, unable to verify, expired, adverse information reported, and restricted. A `passed` badge must not imply universal safety or fitness.

## 27. Safeguarding Record Segregation

Safeguarding records must be logically and permissionally separated from ordinary task, lesson, barn, billing, profile, and communication views. General administrators must not receive allegation access solely through broad administrative roles.

Sensitive records may require sealing, segmented evidence, redacted summaries, conflict-screened reviewers, legal hold, non-destructive correction, and production controls. A subject's ordinary account access must not reveal reporter identity where protected.

## 28. Offline and Degraded-State Safeguarding

Offline intake must preserve actor, subject, device, event time, recorded time, encryption, integrity, and pending-sync state. It must not falsely claim notice delivery, external reporting, restriction activation, or case assignment before authoritative acceptance.

Conflicting or delayed offline entries must be quarantined for review. Emergency guidance must remain available without presenting stale contacts or expired authority as current.

## 29. Transfer, Departure, and Community Surfaces

Horse transfer, barn departure, staff termination, volunteer removal, provider expiration, account closure, and organization separation must revoke current contact and visibility while preserving lawful evidence and required notices.

Public discovery, recommendations, community groups, event rosters, rankings, media, and search must default to minimum exposure for minors and protected participants. No engagement or growth objective may override safeguarding visibility.

## 30. Non-Delegable Human Decisions

The following decisions must not be delegated to AI or unattended automation: credibility, malicious-report finding, guardian fitness, mandated-reporting determination, disciplinary responsibility, emergency-services necessity, prohibited-contact override, record unsealing, professional suitability, or final case outcome.

Automation may route, deduplicate, remind, and enforce already-approved restrictions only when deterministic, reviewable, and separately authorized.

## 31. Draft Acceptance Questions

Founder review must decide jurisdiction policy, age and capacity evidence rules, multiple-guardian conflict posture, emergency override limits, required reverification cadence, prohibited-contact governance, direct-message policy, media and location defaults, minor search defaults, guardian notice defaults, mandated-reporting governance, background-check representations, record sealing, and cross-organization succession behavior.

## 32. Non-Authority Attestation

This draft creates no schema, migration, role, permission, route, workflow, provider action, onboarding rule, production behavior, public claim, or launch authority.
