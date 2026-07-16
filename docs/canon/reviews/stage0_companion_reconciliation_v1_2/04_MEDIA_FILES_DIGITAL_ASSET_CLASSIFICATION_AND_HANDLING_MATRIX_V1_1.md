# EQUINESYNC MEDIA, FILES, AND DIGITAL ASSET CLASSIFICATION AND HANDLING MATRIX

**FOUNDER-ACCEPTED SUBORDINATE GOVERNANCE AND IMPLEMENTATION-PLANNING ARTIFACT - NOT CANON - NOT ADOPTED - NOT LOCKED - NO IMPLEMENTATION AUTHORITY**

## Document Control

| Field | Value |
|---|---|
| Document Type | Digital Asset Classification, Sensitivity, and Handling Matrix |
| Artifact Number | 04 |
| Canonical Name | Media, Files, and Digital Asset Classification and Handling Matrix |
| Version | 1.1 |
| Draft Date | July 14, 2026 |
| Lifecycle State | FOUNDER_ACCEPTED_SUBORDINATE_GOVERNANCE_ARTIFACT |
| Target Constitutional Model | `MASTER_MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE_MODEL_V2_1.md` |
| Founder Authority | Founder acceptance of Media Governance V2.1 and this classification-and-handling control definition |
| Prior Package Artifacts | `02_MEDIA_FILES_DIGITAL_ASSET_CROSS_CANON_RECONCILIATION_MATRIX.md`; `03_MEDIA_FILES_DIGITAL_ASSET_GOVERNANCE_GAP_MATRIX_V1_1.md` |
| Constitutional Authority | None; subordinate governance and implementation-planning evidence only |
| Adoption Authorized | No |
| Lock Authorized | No |
| Implementation Authorized | No |
| Runtime Activation Authorized | No |
| Schema Mutation Authorized | No |
| Data Migration Authorized | No |
| Vendor or Processor Activation Authorized | No |
| AI Media Processing Authorized | No |
| Production Authority | No |
| Public Trust Claim Authority | No |
| Public Launch Authority | No |
| Primary Steward | Founder until formally delegated |
| Next Artifact | `05_MEDIA_FILES_DIGITAL_ASSET_STATE_AND_TRANSITION_MATRIX.md` |

---

# 1. Purpose

This Matrix translates the constitutional classification rules of the `MASTER_MEDIA_FILES_AND_DIGITAL_ASSET_GOVERNANCE_MODEL_V2_1.md` controlling substantive model into a comprehensive, reviewable handling framework.

It establishes how EquineSync should classify and govern digital assets based on:

1. what the asset is;
2. whose rights and interests it carries;
3. how sensitive it is;
4. whether it may become authoritative, evidentiary, historic, or operationally critical;
5. whether it may follow the horse;
6. which actors may view, download, transform, share, export, or retain it;
7. which derived assets may be created;
8. which controls must follow the asset through search, offline use, migration, backup, and deletion; and
9. which actions require heightened review, explicit consent, or founder-reserved authority.

This Matrix is not a storage-provider configuration, database schema, retention schedule, product specification, or production authorization. It provides the control logic those later artifacts must implement and prove.

---

# 2. Classification Is Multi-Dimensional

No material EquineSync asset shall be governed by a single label such as "medical," "private," or "photo."

Every permanent asset must be evaluated across the following independent dimensions:

| Dimension | Required Question | Example Values |
|---|---|---|
| Primary Constitutional Category | What operational or legal domain gives the asset its primary meaning? | Veterinary Imaging; Ownership and Transfer; Training and Instructional |
| Secondary Category | What additional domain meaning applies? | Evidence; Historic; Imported Third-Party |
| Sensitivity Tier | How narrowly must access and processing be controlled? | Internal Operational; Restricted; Safeguarding-Critical |
| Authority Status | Does the asset merely inform, or is it accepted as controlling for a defined purpose? | Informational; Pending Validation; Authoritative |
| Evidence Status | Does the asset require enhanced preservation and chain of custody? | Potential Evidence; Submitted Evidence; Preserved Evidence |
| Lifecycle State | What is the asset's present governance condition? | Scanning; Active; Restricted; Held; Archived |
| Rights and Consent Status | What rights permit storage, use, sharing, or publication? | Operational License; Public Consent; Disputed Rights |
| Horse Continuity Status | Does the asset follow the horse, remain with the creator, or require a scoped continuity view? | Enduring Horse Record; Context-Limited; Non-Transferable |
| Operational Criticality | How quickly must the asset remain available or recoverable? | Routine; Important; Welfare-Critical; Emergency-Critical |
| Source and Provenance Status | How trustworthy and attributable is the source? | Verified Issuer; User Submitted; Imported; System Generated |
| Transformation Status | Is this an original, version, derivative, or synthetic object? | Original; Redacted Copy; OCR Text; AI-Modified |
| Retention Basis | Why must the asset be kept, and what may suspend disposition? | Horse History; Contract; Claim; Legal Hold; Transitory |

A category label may describe meaning. A sensitivity tier controls handling. An authority or evidence designation controls weight and preservation. None of these may be inferred solely from a filename, file extension, folder location, uploader role, or visual appearance.

---

# 3. Governing Classification Rules

## 3.1 Private by Default

All newly received assets are private by default unless a valid, attributable, current authorization establishes a broader audience.

"Publicly Authorized" is an affirmative sensitivity and publication state. It is never inferred from prior posting elsewhere, a public competition, a public facility, an uploader's administrative role, or the fact that a horse is publicly known.

## 3.2 Most-Protective Valid Control

Where an asset has multiple categories, subjects, rights, or sensitivity indicators, the most protective valid control governs unless a narrower, specifically authorized relationship-level view can be produced without exposing the protected context.

Examples:

- A competition video that includes an identifiable minor is not handled merely as Competition and Performance. Minor protections also apply.
- A public-facing horse sale photograph that reveals precise barn geolocation must suppress location metadata even when the image itself is authorized for publication.
- A veterinary invoice may be both Financial and Equine Medical. Access to payment information does not automatically grant access to diagnosis details, and access to medical details does not automatically grant access to payment credentials.
- A horse-transfer package may expose a current Coggins certificate while withholding private provider notes embedded in the same source bundle.

## 3.3 No Down-Classification by Convenience

An asset may not be assigned a lower sensitivity tier because:

- the intended audience is large;
- an administrator wishes to simplify access;
- storage or preview costs are lower;
- the same content was previously emailed;
- a user has already downloaded it;
- an external provider cannot support the required controls;
- a public link is easier than authenticated access; or
- a technical system lacks field-level or relationship-level filtering.

A system that cannot safely enforce the required classification must restrict, defer, redact, or decline the action.

## 3.4 Classification Does Not Establish Truth

Classification is a governance determination, not a factual adjudication.

An asset labeled Medical remains subject to provider validation. An asset labeled Evidence remains subject to authenticity, credibility, and admissibility analysis. An asset labeled Ownership and Transfer does not itself prove title.

## 3.5 Category and Sensitivity Must Be Separately Recorded

The implementation model must not collapse category and sensitivity into a single enum. The following are valid combinations:

- Training and Instructional + Internal Operational;
- Training and Instructional + Restricted because a minor is depicted;
- Veterinary Imaging + Confidential;
- Veterinary Imaging + Evidence-Critical because it is associated with a claim;
- Marketing and Promotional + Publicly Authorized;
- Marketing and Promotional + Restricted because consent has been withdrawn;
- Legal and Contractual + Confidential;
- Legal and Contractual + Privileged or Sealed.

## 3.6 Derived Assets Inherit Before They Diverge

A thumbnail, preview, OCR output, transcript, translation, annotation, embedding, redacted copy, watermark, AI summary, or extracted field must initially inherit the source asset's category, sensitivity, tenant boundary, retention basis, rights restrictions, and hold status.

A derived asset may later receive a different handling profile only through an explicit, auditable determination. A redacted copy may be less sensitive than the original, but only after the redaction is validated and hidden content, metadata, and recoverability risks are addressed.

## 3.7 Restricted Metadata May Be More Sensitive Than the Asset

An asset may be viewable while certain metadata remains restricted.

Examples include:

- GPS coordinates;
- exact facility address;
- device identifier;
- uploader legal name;
- minor identity;
- claim number;
- hidden document comments;
- prior revision history;
- internal provider notes;
- source-system credentials;
- malware-analysis indicators; and
- legal-hold details.

## 3.8 Classification Must Be Reviewable

Every material classification decision must be explainable through recorded rules, source facts, actor authority, and timestamps. Automated classification may recommend or provisionally restrict. It may not silently make a final high-impact determination where human or founder approval is required.

---

## 3.9 Dimensional Constitutional Ownership

Classification is a coordinated set of independent constitutional dimensions. No single enum, field, interface label, or technical service may silently collapse them.

- **Master Privacy and Data Protection Model** owns personal-information classification, privacy sensitivity, processing purpose, and privacy-specific handling obligations.
- **Master Media, Files, and Digital Asset Governance Model** owns digital-asset category, transformation state, media-specific handling, rights and publication status, evidence designation, and horse-continuity treatment.
- **Master Security and Trust Model** owns security control floors, threat state, quarantine, and security-specific restrictions.
- **Master Record Stewardship and Retention Model** owns record class, retention basis, legal hold, archive, restoration semantics, and disposition.
- **Master Platform Resilience, Backup, and Recovery Operational Model V1.0**, under the founder-designated security-package exception, owns operational criticality, recovery priority, backup, restore, failover, failback, and recovery evidence within its reconciled scope.
- **Master Permission and Access-Control Model** evaluates the combined dimensions and converts them into actor-, purpose-, action-, object-, field-, rendition-, environment-, and time-specific capabilities.

Compatible controls apply together. A classification owner may narrow handling within its domain but may not silently redefine another domain's classification, authority, retention, or evidence meaning.

---

# 4. Sensitivity Tier Definitions

| Tier Code | Sensitivity Tier | Definition | Default Audience | Default Handling Posture |
|---|---|---|---|---|
| S0 | Publicly Authorized | Content expressly approved for public exposure for a defined purpose, audience, channel, and duration | Public or specifically approved broad audience | Publication permitted only within recorded authorization; underlying private metadata remains protected |
| S1 | Internal Operational | Routine business or horse-care content that is not public but may be accessed by appropriately related operational actors | Authorized tenant or relationship-scoped users | Authenticated access; ordinary audit; limited external sharing |
| S2 | Confidential | Personal, medical, financial, contractual, provider, or operational information requiring narrowed access | Purpose-limited authorized actors | Strong access controls; restricted download and sharing; enhanced audit |
| S3 | Restricted | Content whose disclosure could materially harm a person, horse, organization, legal position, financial interest, or safety | Specifically authorized roles and relationships | No default offline use; no public links; reasoned access and heightened logging |
| S4 | Highly Restricted | Highly sensitive medical, identity, security, investigation, ownership-dispute, financial, or graphic content | Named or narrowly qualified actors | Explicit authorization; limited preview; download restrictions; strong review and alerting |
| S5 | Privileged or Sealed | Attorney-client, work-product, sealed, court-restricted, confidential settlement, or equivalent legally protected material | Validly authorized legal or designated custodial actors | No routine indexing or AI processing; access and export require heightened authority |
| S6 | Safeguarding-Critical | Content involving minors, abuse, neglect, exploitation, mandatory reporting, or protected safeguarding investigations | Safeguarding-authorized actors only, subject to law and guardian limits | Strongest privacy, evidence, viewing, sharing, and notification controls |
| S7 | Evidence-Critical | Content placed under enhanced evidentiary preservation or chain-of-custody requirements | Claim, legal, insurance, regulatory, or investigation actors with authority | Immutable preservation; transformation control; export manifest; access and custody evidence |
| S8 | Security-Quarantined | Content restricted due to malware, unsafe format, corruption, rights uncertainty, unidentified source, or security concern | Security, records, legal, or designated reviewers | No ordinary access, preview, search, download, offline use, or external sharing |

## 4.1 Tier Precedence

The tier codes are not a simple linear ladder in every context. S5, S6, S7, and S8 are special-purpose heightened regimes. When one of these applies, its specific controls supplement or override ordinary S0-S4 handling.

## 4.2 Publicly Authorized Does Not Mean Unrestricted

S0 permits only the approved public use. It does not authorize:

- resale;
- AI model training;
- biometric processing;
- removal of attribution;
- unrelated advertising;
- disclosure of hidden metadata;
- perpetual use after consent withdrawal;
- or republication beyond the licensed purpose.

## 4.3 Provisional Restriction

When sensitivity is uncertain, the asset shall be provisionally assigned the most reasonably protective tier until review. Uncertainty shall not produce ordinary availability.

---

# 5. Sensitivity Handling Control Matrix

Legend:

- **Allowed**: permitted under ordinary authorized workflow.
- **Conditional**: permitted only when additional stated controls are satisfied.
- **Restricted**: not ordinarily permitted; requires heightened authority.
- **Prohibited**: not permitted under the current constitutional posture.
- **N/A**: not applicable to the tier or action.

| Control | S0 Publicly Authorized | S1 Internal Operational | S2 Confidential | S3 Restricted | S4 Highly Restricted | S5 Privileged or Sealed | S6 Safeguarding-Critical | S7 Evidence-Critical | S8 Security-Quarantined |
|---|---|---|---|---|---|---|---|---|---|
| Authentication for ordinary view | Conditional, depending on publication channel | Required | Required | Required | Required | Required | Required | Required | Restricted reviewers only |
| Anonymous public view | Conditional to approved publication | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited unless separately authorized exhibit | Prohibited |
| Preview generation | Allowed with metadata stripping | Allowed | Conditional | Conditional | Restricted | Restricted | Restricted | Conditional, evidence-safe rendition only | Prohibited outside isolated processing |
| Full original view | Conditional | Allowed to authorized actors | Conditional | Restricted | Restricted | Restricted | Restricted | Conditional and logged | Restricted security review only |
| Search indexing | Public index only if approved | Tenant- and permission-scoped | Permission-scoped | Restricted fields only | Minimal or disabled | Disabled unless legal-approved | Disabled or safeguarding-scoped | Evidence index only | Disabled |
| Snippet or thumbnail in search | Conditional | Allowed | Conditional | Restricted | Restricted | Prohibited by default | Prohibited by default | Conditional | Prohibited |
| Download | Conditional by license | Allowed to authorized actors | Conditional | Restricted | Restricted | Heightened authority | Heightened authority | Heightened authority and custody record | Prohibited except controlled security extraction |
| Bulk download or export | Restricted | Conditional | Restricted | Restricted | Restricted | Heightened legal authority | Heightened safeguarding or legal authority | Heightened authority and manifest | Prohibited |
| External authenticated share | Conditional | Conditional | Conditional | Restricted | Restricted | Heightened authority | Heightened authority | Heightened authority | Prohibited |
| Public link | Conditional and purpose-scoped | Prohibited by default | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited except separately authorized public filing | Prohibited |
| Link expiration | Required where link-based | Required | Required | Required | Required | Required | Required | Required | N/A |
| Recipient limitation | Conditional | Required for external share | Required | Required | Required | Required | Required | Required | N/A |
| Watermark | Conditional | Optional | Conditional | Recommended | Required where appropriate | Required where appropriate | Required where appropriate | Evidence-safe only; must not alter original | Analysis copy only |
| Offline storage | Conditional | Conditional | Restricted | Prohibited by default | Prohibited by default | Prohibited by default | Prohibited by default | Restricted, explicit purpose | Prohibited |
| Mobile camera-roll export | Conditional by consent | Conditional | Restricted | Prohibited by default | Prohibited | Prohibited | Prohibited | Prohibited unless evidence collection workflow | Prohibited |
| AI analysis | Conditional and purpose-limited | Conditional | Restricted | Heightened review | Prohibited by default | Prohibited by default | Prohibited by default | Restricted, non-destructive and reviewed | Isolated security tooling only |
| Shared-model training | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited |
| OCR or transcription | Conditional | Allowed | Conditional | Restricted | Restricted | Prohibited by default | Prohibited by default | Conditional with lineage | Isolated processing only |
| Embedding or semantic indexing | Conditional | Conditional | Restricted | Prohibited by default | Prohibited | Prohibited | Prohibited | Restricted and evidence-safe | Prohibited |
| Redaction copy creation | Conditional | Conditional | Allowed through governed workflow | Allowed through heightened workflow | Allowed through heightened workflow | Legal-authorized only | Safeguarding/legal-authorized only | Evidence-preserving workflow only | Security/legal-authorized only |
| Metadata stripping for share | Required for nonessential sensitive metadata | Required as applicable | Required | Required | Required | Required | Required | Conditional; preserve original metadata separately | N/A |
| Geolocation exposure | Only if expressly approved | Conditional operational need | Restricted | Prohibited by default | Prohibited | Prohibited | Prohibited | Conditional if evidentiary | Prohibited |
| Support personnel access | Conditional | Restricted and audited | Heightened and audited | Heightened and reasoned | Exceptional | Exceptional legal-approved | Exceptional safeguarding-approved | Exceptional and custody-recorded | Security-only |
| Administrative bypass | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited |
| Encryption in transit and at rest | Required | Required | Required | Required | Required | Required | Required | Required | Required |
| Enhanced audit | Conditional | Standard | Required | Required | Required plus alerting | Required plus legal review | Required plus safeguarding review | Required chain of custody | Required security chain |
| Retention schedule | Consent/license plus applicable record basis | Record basis | Record basis | Record basis plus restriction | Record basis plus review | Legal basis | Safeguarding/legal basis | Hold/evidence basis | Security/incident basis |
| Destructive overwrite | Prohibited for governed originals | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited |
| Deletion while hold applies | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited | Prohibited |
| Public trust claim based on tier | Prohibited without evidence | Prohibited without evidence | Prohibited without evidence | Prohibited without evidence | Prohibited without evidence | Prohibited without evidence | Prohibited without evidence | Prohibited without evidence | Prohibited without evidence |

---

# 6. Primary Constitutional Category Matrix

The following matrix provides the default posture. A specific asset may require a more protective tier or additional secondary categories.

| ID | Primary Category | Representative Assets | Default Sensitivity | Authority Potential | Horse Continuity | Offline Default | External Share Default | Public Eligibility | Core Handling Requirements |
|---|---|---|---|---|---|---|---|---|---|
| C01 | Identity and Verification | microchip certificate, identity photographs, markings, issuer verification, account identity evidence | S2 Confidential; S3 if government or high-risk identifiers | May become authoritative for defined identity scope | Usually enduring for horse identity; human identity remains person-scoped | Restricted | Restricted | Rare; only selected horse identity data | Verified issuer where available; protect identifiers and location; prevent biometric inference |
| C02 | Equine Medical and Diagnostic | veterinary reports, lab results, diagnoses, discharge instructions, health certificates | S2 Confidential; S3-S4 where sensitive or disputed | Strong authority potential when issued by qualified provider | Enduring where medically or legally significant | Restricted; welfare-critical subsets may be allowed | Restricted to authorized owner/provider/caregiver | Generally no | Provider attribution; purpose limitation; continuity without unrelated provider notes |
| C03 | Veterinary Imaging | radiographs, ultrasound, endoscopy, thermal images, diagnostic series | S2-S4 depending on context | May support provider-authoritative record; image alone not diagnosis | Enduring for significant studies | Prohibited by default except explicit clinical need | Restricted | No | Preserve original fidelity, modality, study date, horse identity, issuer, annotations, and report linkage |
| C04 | Medication and Treatment | prescriptions, administration photos, medication logs, treatment plans | S2 Confidential; S3 for controlled or dispute-related information | May become authoritative within provider or administration workflow | Enduring when relevant to care, safety, or claims | Conditional for active care | Restricted | No | Time-sensitive accuracy; current/superseded distinction; no AI prescribing; access based on care role |
| C05 | Financial | invoices, receipts, statements, estimates, expense evidence | S2 Confidential; S3 for account or tax data | May be authoritative for transaction or accounting scope | Generally not horse-transferable beyond necessary transaction evidence | Restricted | Restricted | No | Financial truth, minimum necessary disclosure, no payment credential exposure |
| C06 | Payment and Billing | payment confirmations, billing authorizations, processor receipts, chargeback evidence | S3 Restricted; S4 if credential-like | Strong transaction authority potential | Context-limited; not automatic horse continuity | Prohibited | Restricted to payer/payee and authorized finance roles | No | Tokenize or exclude credentials; processor provenance; dispute and retention controls |
| C07 | Legal and Contractual | agreements, releases, waivers, court filings, policies, notices | S2-S4 depending on subject | May become authoritative when executed or issued | Transfer only where legally relevant to horse continuity | Prohibited by default | Restricted | Only if lawfully public and separately approved | Version, effective date, signature status, parties, privilege review, hold integration |
| C08 | Privileged or Legally Restricted | attorney-client communications, work product, sealed orders, confidential settlements | S5 Privileged or Sealed | Authority depends on source and legal status | Non-transferable unless lawfully required | Prohibited | Heightened legal authority only | No | No routine AI, OCR, semantic indexing, support access, or broad admin access |
| C09 | Welfare and Safeguarding | injury photos, neglect evidence, incident records, protected reports | S6 Safeguarding-Critical; S7 when evidence designated | May become evidence or official investigation record | Continuity only to extent safety, law, or horse welfare requires | Prohibited by default | Heightened safeguarding/legal authority | No | Minor protection, mandatory-reporting boundaries, graphic warnings, chain of custody |
| C10 | Ownership and Transfer | bills of sale, transfer approvals, custody records, lien notices | S2-S4; S7 if disputed | Strong authority potential, but no automatic title conclusion | Enduring horse record where validated | Restricted | Restricted to parties and authorized coordinators | Rare | Preserve competing claims, effective dates, transfer state, signatures, non-transferable context |
| C11 | Registration, Pedigree, and Passport | breed papers, pedigree, passport, registration certificates | S2 Confidential; selected fields may be S0/S1 | Strong issuer-based authority potential | Enduring horse record | Conditional | Conditional to authorized parties | Selected fields may be public with rights clearance | Issuer verification, historic preservation, identity continuity, version and endorsement tracking |
| C12 | Competition and Performance | official results, score sheets, certificates, competition video | S1 Internal or S2; S0 only with public rights | Official results may be authoritative within event scope | Historic for material achievements | Conditional | Conditional | Eligible with consent and rights | Separate event publication rights, minor protection, no inference of rider skill or horse soundness |
| C13 | Breeding and Reproduction | breeding records, reproductive exams, foaling media, genetic reports | S2-S4 | Provider or registry authority potential | Enduring when medically, identity, or registry significant | Restricted | Restricted | Rare | Sensitive medical and commercial interests; pedigree integrity; foal and mare identity |
| C14 | Training and Instructional | lesson videos, training plans, rider notes, exercise diagrams | S1 Internal; S2-S3 with personal or minor data | Usually informational; instructor records may be scoped authoritative | Usually context-limited; selected horse training history may continue | Conditional | Conditional | Eligible only with separate consent | Protect minors, private notes, coaching context; no automatic rider rating or welfare conclusion |
| C15 | Facility and Operational | maps, stall charts, turnout plans, daily-operation photos | S1 Internal; S2-S4 if security or location-sensitive | May be operationally authoritative for current schedule or assignment | Usually facility-scoped, not horse-transferable | Conditional where operationally necessary | Restricted | Rare | Current-state labeling, location controls, tenant boundaries, safe degradation |
| C16 | Maintenance and Safety | inspection photos, repair records, hazard reports, equipment manuals | S1-S3; S7 if incident evidence | May be authoritative for inspection or work-order scope | Usually facility/equipment scoped | Conditional | Conditional to vendor or insurer | Rare | Hazard priority, incident linkage, no deletion after injury claim, geolocation controls |
| C17 | Communication and Notice | notices, message attachments, acknowledgement receipts, delivery evidence | S1-S3 depending on content | May be authoritative for notice and delivery scope | Context-specific | Restricted | Conditional to intended recipient | Rare | Preserve sent version, recipients, delivery state, attachments, withdrawal and correction evidence |
| C18 | Evidentiary | designated exhibits, preserved incident media, evidence packages | S7 Evidence-Critical plus underlying sensitivity | Evidence status only; not automatic factual truth | Depends on underlying category | Restricted | Heightened authority only | Only through lawful filing or authorized disclosure | Immutable preservation, chain of custody, hash, manifest, transformation history |
| C19 | Claims and Insurance | claim submissions, estimates, adjuster correspondence, loss photos | S3 Restricted; S7 where preserved evidence | May be authoritative for claim process only | Context-limited, with selected horse history continuity | Prohibited by default | Restricted to claimant, insurer, counsel, authorized parties | No | Hold triggers, fraud review, evidence export, minimum necessary disclosure |
| C20 | Human Resources and Personnel | evaluations, discipline, employment records, staff investigations | S3-S5; S6 where safeguarding involved | May be authoritative within employment process | Non-transferable with horse | Prohibited | Heightened HR/legal authority | No | Strict separation from horse record; privilege and employment-law controls |
| C21 | Marketing and Promotional | campaign images, testimonials, approved social media, press materials | S0 only when expressly authorized; otherwise S1-S3 | Not authoritative merely because published | Does not automatically follow horse | Conditional | Conditional | Yes, within consent and rights scope | Copyright, publicity, duration, channel, withdrawal, minor and location controls |
| C22 | System-Generated | reports, receipts, previews, status exports, generated PDFs | Inherits source; minimum S1 | Authority depends on governing workflow and inputs | Inherits source relationship | Inherits source | Inherits source | Only if source and publication authority permit | Provenance, generation version, input references, no false official status |
| C23 | AI-Generated | summaries, diagrams, synthetic illustrations, drafted captions | Inherits inputs; minimum S1; higher where source is sensitive | Not authoritative by generation alone | Context-limited unless validated and adopted into record | Restricted | Restricted | Eligible only if labeled and rights-cleared | Prominent labeling, model/service provenance, uncertainty, no false evidence |
| C24 | AI-Modified | enhanced image, AI annotation, translated transcript, reconstructed media | Inherits source, usually same or higher | Not authoritative unless separately validated | Inherits source | Restricted | Restricted | Rare, with labeling | Preserve original; record transformation; no invented detail; evidence-safe handling |
| C25 | Imported Third-Party | cloud-drive file, email attachment, provider portal download | Provisional S3 until classified | No automatic authority | Determined after validation | Prohibited until classified | Prohibited until classified | No until rights and consent verified | Source capture, malware scan, rights check, duplicate review, classification before use |
| C26 | Temporary or Transitory | upload chunks, processing files, draft previews, conversion cache | Inherits source; provisional S3 if unknown | None | No, unless promoted through governed process | Prohibited | Prohibited | No | Short expiration, encryption, no orphaning, secure disposal, no accidental authority |
| C27 | Archived | superseded, inactive, closed-period, or long-term retained assets | Inherits underlying category and sensitivity | May retain historic or evidentiary authority | Depends on underlying basis | Prohibited by default | Restricted | Only through separate publication copy | Limited ordinary access; retention and restore controls; integrity checks |
| C28 | Historically Significant | lifetime medical history, major competition records, memorial media, lineage records | Inherits underlying sensitivity; historic status never lowers privacy | May be authoritative or informational | Enduring by designation | Restricted | Conditional | Selected copies only with rights | Preservation migration, format monitoring, privacy continuity, no automatic publicity |

---

# 7. Category-Specific Handling Requirements

## 7.1 Identity and Verification

Identity assets must distinguish horse identity from human identity. Horse identity records may include markings, microchip numbers, registration numbers, and identity photographs. Human identity records may include account-verification evidence and must not be exposed merely because the person is related to a horse or facility.

Required controls:

- record the issuer and verification method;
- separate publicly displayable horse descriptors from restricted identifiers;
- prohibit facial recognition and human biometric inference;
- restrict full microchip, registration, account, and legal identifiers to valid purposes;
- preserve identity corrections without silent replacement;
- prevent a photograph alone from conclusively establishing identity; and
- propagate identity disputes to dependent relationships and exports.

## 7.2 Equine Medical, Diagnostic, Medication, and Treatment

Medical and treatment assets must be purpose-limited and provider-aware.

Required controls:

- identify horse, provider, encounter or study date, and document type;
- distinguish provider-issued records from owner notes, uploaded photographs, and AI summaries;
- identify current, expired, cancelled, superseded, and corrected instructions;
- preserve allergy, adverse reaction, and emergency-care information where continuity requires;
- prevent unrelated staff or providers from gaining broad lifetime-record access;
- restrict medication and treatment data to active care, welfare, legal, and continuity purposes;
- prevent an image or extracted field from being treated as a diagnosis; and
- retain the original provider artifact where an extracted structured record is created.

## 7.3 Veterinary Imaging

Imaging controls must preserve clinical and evidentiary fidelity.

Required controls:

- preserve original pixels, bit depth, modality, study metadata, and series structure where available;
- maintain linkage between images, horse identity, provider, date, body region, and interpretive report;
- distinguish diagnostic originals from thumbnails, compressed display copies, annotations, and enhanced renditions;
- prohibit destructive replacement by cropped, sharpened, or AI-enhanced copies;
- restrict download and sharing according to provider, owner, legal, and clinical authority;
- ensure exports preserve available clinical context and limitations; and
- prohibit EquineSync from representing enhancement as provider interpretation.

## 7.4 Financial, Payment, and Billing

Financial assets must follow the Financial Truth and Responsibility canon and must not expose payment credentials or unrelated financial information.

Required controls:

- distinguish invoice, receipt, estimate, processor confirmation, refund, chargeback, and accounting export;
- minimize account, tax, card, bank, and payer information;
- separate horse-care facts from payment details where different audiences apply;
- preserve transaction identifiers and processor provenance without storing prohibited credentials;
- support disputes and legal holds without granting the opposing party access to unrelated account data; and
- prevent AI extraction from creating a final liability or reconciliation decision without review.

## 7.5 Legal, Contractual, Privileged, and Sealed Assets

Required controls:

- preserve executed version, signature package, parties, effective date, amendments, and supersession;
- distinguish drafts, negotiations, final agreements, acknowledgements, and court-filed copies;
- identify privilege, sealing, confidentiality, and protective-order restrictions;
- disable routine AI, OCR, semantic indexing, and broad support access for S5 assets unless specifically authorized;
- prevent horse transfer from carrying unrelated legal advice, negotiations, or confidential settlement terms;
- preserve legal holds and discovery scope; and
- require legal authority for export, disclosure, redaction, or privilege review.

## 7.6 Welfare and Safeguarding

Required controls:

- assign S6 by default when a minor, abuse, neglect, exploitation, or protected report is materially involved;
- prevent public, promotional, or routine operational reuse;
- limit previews and require graphic-content warnings where applicable;
- record reason for access and material custody events;
- preserve mandatory-reporting and legal obligations without exposing the reporter beyond lawful need;
- prevent guardian authority from overriding mandatory safeguarding or preservation duties;
- separate protected investigation content from ordinary horse-health or incident summaries; and
- apply S7 evidence controls where the content is designated for investigation, claim, or proceeding.

## 7.7 Ownership, Transfer, Registration, Pedigree, and Passport

Required controls:

- identify issuer, parties, horse, effective date, status, and competing claims;
- distinguish proof submitted from title or transfer formally accepted;
- preserve endorsement, correction, cancellation, and transfer history;
- permit horse continuity without transferring photographer rights, privileged notes, or unrelated party data;
- restrict lien, dispute, payment, and identity details to authorized actors;
- preserve enduring registration and pedigree records; and
- prohibit automated ownership adjudication.

## 7.8 Competition, Performance, Training, and Instructional Assets

Required controls:

- distinguish official results from personal observations, coaching notes, and promotional edits;
- apply minor and guardian protections to youth content;
- preserve event, date, class, source, and publication rights;
- prevent training video from becoming an automated rider-level, horse-soundness, or welfare determination;
- protect private trainer notes from automatic transfer with the horse;
- permit selected historic achievements to follow the horse while retaining rights and consent limitations; and
- ensure public competition does not imply unrestricted media use.

## 7.9 Facility, Operational, Maintenance, and Safety Assets

Required controls:

- distinguish current operational maps and plans from historical or draft versions;
- restrict precise locations, security systems, access points, camera placements, and emergency vulnerabilities;
- identify facility, area, equipment, date, inspector, and work order where relevant;
- preserve hazard and maintenance evidence when an incident, claim, or legal duty exists;
- support offline availability only where operational need and device controls justify it;
- prevent former facility relationships from retaining current operational access; and
- assign operational criticality separately from sensitivity.

## 7.10 Communication and Notice Assets

Required controls:

- preserve the exact sent or published version;
- record sender, recipient, channel, time, attachments, acknowledgement, and delivery evidence where applicable;
- prevent a later attachment replacement from changing the historical notice;
- apply the underlying attachment's classification independently;
- distinguish draft communication from delivered notice;
- support correction and supersession without erasing the original event; and
- restrict message content according to purpose and relationship.

## 7.11 Evidence, Claims, and Insurance

Required controls:

- apply S7 only through an authorized evidence or preservation process;
- preserve original and custody history;
- prohibit destructive edits and silent metadata removal;
- permit analysis copies only when linked to the original;
- record claim, incident, matter, or proceeding scope;
- restrict opposing-party or insurer access to the minimum authorized package;
- include manifests and verification instructions in governed exports; and
- distinguish evidence integrity from factual credibility and legal admissibility.

## 7.12 Human Resources and Personnel

Required controls:

- maintain strict separation from horse continuity and ordinary barn relationships;
- restrict to authorized HR, management, safeguarding, or legal actors;
- prevent owner, boarder, trainer, or former employee access merely through facility relationship;
- identify employment, evaluation, discipline, accommodation, investigation, or payroll context;
- apply privilege and safeguarding overlays where relevant; and
- prohibit use for unrelated AI profiling, ranking, or cross-tenant learning.

## 7.13 Marketing and Promotional Assets

Required controls:

- require separately recorded copyright, publicity, consent, channel, audience, duration, and purpose;
- identify every materially depicted person where consent obligations apply;
- prohibit inference that the horse owner owns the photographer's rights;
- strip unnecessary geolocation and device metadata;
- propagate consent withdrawal to public pages, campaigns, caches, thumbnails, and controlled processors;
- retain evidence of prior lawful use without continuing public display; and
- prohibit minor or safeguarding content from promotional reuse without the strongest lawful authority.

## 7.14 System-Generated, AI-Generated, and AI-Modified Assets

Required controls:

- identify system, model or service category, generation time, source assets, and transformation type;
- inherit source permissions, sensitivity, tenant, retention, and hold state;
- label synthetic and materially modified content;
- preserve the original and version lineage;
- separate fact, extraction, inference, and generated language;
- prohibit final medical, legal, financial, safeguarding, ownership, or rider-ability conclusions;
- prevent provider training or shared-model learning with customer assets; and
- retain failure, review, and correction status.

## 7.15 Imported Third-Party Assets

Imported assets begin in provisional restricted handling until source, rights, malware, category, subject, and relationship are resolved.

Required controls:

- capture source system, importer, original filename, time, and available metadata;
- scan before ordinary availability;
- avoid assuming external permissions map to EquineSync permissions;
- identify duplicates without automatic deletion;
- prevent imported content from becoming authoritative by import alone;
- quarantine password-protected or unsupported content where controls cannot be applied; and
- record any loss of metadata or fidelity during import.

## 7.16 Temporary, Archived, and Historic Assets

Temporary assets must expire securely and may not become permanent through neglect. Archived and historic assets retain underlying rights, sensitivity, holds, and access restrictions.

Required controls:

- define promotion from transitory to permanent;
- prevent abandoned upload chunks, caches, and previews from persisting indefinitely;
- limit ordinary access to archived assets;
- validate restored assets before activation;
- monitor historic formats for obsolescence;
- preserve migration lineage and originals; and
- ensure historic designation never creates public authorization.

---

# 8. Secondary Classification Overlays

The following overlays may apply to any primary category.

| Overlay | Trigger | Required Effect |
|---|---|---|
| O01 - Minor Depicted or Identified | An identifiable person under the applicable age threshold appears or is described | Apply heightened privacy, search, sharing, location, and guardian/safeguarding rules |
| O02 - Graphic or Distressing | Injury, surgery, abuse, neglect, post-mortem, necropsy, or other disturbing content | Limit previews; require warnings; restrict routine exposure and promotional use |
| O03 - Precise Location | GPS, address, stall, pasture, route, camera placement, or other precise location | Suppress ordinary sharing; expose only for valid operational or evidentiary purpose |
| O04 - Human Identity or Biometrics Risk | Face, voice, gait, identity document, or uniquely identifying characteristic | Prohibit biometric inference; restrict indexing and public exposure |
| O05 - Privilege or Legal Restriction | Attorney-client, work product, sealed, protective order, confidential settlement | Apply S5; limit indexing, AI, support, export, and access |
| O06 - Safeguarding Matter | Abuse, neglect, exploitation, mandatory report, protected investigation | Apply S6 and safeguarding workflow |
| O07 - Evidence or Hold | Legal, claim, investigation, insurance, regulatory, or preservation designation | Apply S7, chain of custody, immutability, and disposition suspension |
| O08 - Security Concern | Malware, corruption, suspicious archive, unsafe macro, rights uncertainty | Apply S8 quarantine and isolated review |
| O09 - Public Consent | Valid permission for defined public use | Permit only approved publication; preserve private source and withdrawal controls |
| O10 - Horse Enduring History | Material identity, medical, registration, ownership, competition, breeding, or welfare significance | Preserve continuity; prevent unrelated context transfer |
| O11 - Operational Criticality | Required for active care, emergency response, safety, or facility continuity | Increase availability and recovery priority without lowering sensitivity |
| O12 - Disputed Rights or Truth | Ownership, authenticity, issuer, consent, classification, or factual dispute | Restrict as needed; preserve competing positions; prevent automated resolution |
| O13 - External Provider Restriction | Contract, license, professional obligation, or source limitation | Apply source-specific use, export, and retention limits without weakening higher protections |
| O14 - Cross-Border or Residency Restriction | Tenant, law, contract, or processing-region requirement | Limit storage, processing, replication, export, and vendor location |
| O15 - Public Record or Lawful Filing | Asset is lawfully public through court, registry, or government process | Do not assume all copies or metadata are unrestricted; apply purpose and rights review |

---

# 9. Authority Status Matrix

| Authority Code | Status | Meaning | Permitted Representation | Required Controls |
|---|---|---|---|---|
| A0 | Unassessed | No authority determination has been made | "Uploaded" or "received" only | No official or controlling label |
| A1 | Informational | Useful context but not accepted as controlling | "User-provided," "reference," or equivalent | Preserve source and limitations |
| A2 | Pending Validation | Candidate record awaiting issuer, completeness, or workflow validation | "Pending verification" | Restricted reliance; review required |
| A3 | Verified Copy | Copy validated against a recognized source or issuer, but not necessarily the controlling original | "Verified copy" within defined scope | Record verification method and date |
| A4 | Authoritative | Accepted as controlling for a specifically defined purpose | "Authoritative for [scope]" | Issuer, basis, effective date, version, and supersession controls |
| A5 | Superseded Authority | Was authoritative but replaced prospectively | "Superseded" | Preserve history and successor linkage |
| A6 | Withdrawn or Revoked | Authority removed or invalidated | "Withdrawn" or "revoked" | Prevent current reliance; preserve basis and timing |
| A7 | Disputed Authority | Material dispute affects authority | "Disputed" | Restrict automated use and preserve competing evidence |

Authority is scope-specific. A veterinary health certificate may be authoritative for a stated examination date and purpose, not for all future health questions. A signed invoice may be authoritative as to the billed amount, not as conclusive proof that the charge is legally owed.

---

# 10. Evidence Status Matrix

| Evidence Code | Status | Meaning | Handling Consequence |
|---|---|---|---|
| E0 | Not Evidence-Designated | Ordinary record handling applies | No special evidentiary claim |
| E1 | Potential Evidence | May become relevant to an incident, claim, or investigation | Preserve against foreseeable loss; restrict destructive actions |
| E2 | Submitted Evidence | Formally submitted to a claim, report, matter, or review | Record submitter, time, context, and source |
| E3 | Preserved Evidence | Subject to enhanced preservation or hold | Apply S7, immutability, chain of custody, and disposition suspension |
| E4 | Verified Integrity | Hash, lineage, and custody checks have been completed | May state integrity verification, not factual truth |
| E5 | Disputed Evidence | Authenticity, completeness, context, or rights are contested | Preserve dispute and competing materials; restrict conclusory labeling |
| E6 | Produced or Exported Evidence | Included in a governed evidence package | Preserve package manifest, recipient, authority, and verification evidence |
| E7 | Resolved or Closed-Matter Evidence | Matter has concluded but retention remains governed | Continue hold or retention until formal release and disposition authority |

---

# 11. Horse Continuity Classification

| Continuity Code | Status | Meaning | Transfer or Departure Effect |
|---|---|---|---|
| H0 | Not Horse-Linked | Asset has no governed horse relationship | No horse continuity effect |
| H1 | Horse-Associated Context | Asset relates to a horse but is not part of enduring history | Access ends or narrows with relationship unless another basis applies |
| H2 | Operational Horse Record | Needed for current care, schedule, service, or facility operation | Transfer only to authorized active-care actors and only as necessary |
| H3 | Enduring Horse Record | Identity, medical, ownership, registration, significant competition, breeding, or welfare history | Follows the horse through governed continuity process |
| H4 | Context-Limited Continuity | A fact or redacted rendition follows, but private annotations or surrounding context do not | Produce scoped continuity view or derivative |
| H5 | Non-Transferable Private Context | HR, privileged, internal investigation, private trainer/provider notes, unrelated financial or facility material | Does not transfer merely because horse-linked |
| H6 | Disputed Continuity | Parties dispute whether the asset or part of it should follow | Preserve and restrict pending governed resolution |

Horse continuity never transfers copyright, publicity rights, privilege, unrelated personal information, or broad access to the source account.

---

# 12. Operational Criticality Classification

Sensitivity and criticality must remain separate.

| Criticality Code | Level | Examples | Availability and Recovery Posture |
|---|---|---|---|
| K0 | Transitory | upload chunks, temporary previews | No continuity guarantee beyond controlled processing |
| K1 | Routine | marketing drafts, historic nonurgent media | Ordinary service and recovery priority |
| K2 | Operationally Important | current facility maps, active invoices, training plans | Timely availability; monitored restoration |
| K3 | Care-Critical | active medication instructions, allergy record, current health certificate, emergency contact attachment | High availability; safe offline eligibility may be considered; rapid restoration |
| K4 | Welfare or Safety-Critical | emergency treatment instructions, active hazard evidence, safeguarding routing record | Highest justified availability and recovery; safe degradation and alternate access required |
| K5 | Evidence Preservation-Critical | held evidence, chain-of-custody package | Integrity and preservation outrank ordinary convenience; controlled restore and verification |

A K4 asset may still be S4 or S6. High criticality does not authorize broad access. It requires reliable access for the narrow actors already authorized.

---

# 13. Asset State Handling Overlay

The state matrix does not replace category or sensitivity. It modifies what may occur while the asset is in a given lifecycle condition.

| State | View | Download | Search | Transform | Share | Retention or Deletion | Required Review |
|---|---|---|---|---|---|---|---|
| Pending Upload | No | No | No | No | No | Expire failed session safely | Upload integrity and authorization |
| Incomplete | Limited status only | No | No | No | No | Preserve briefly for retry or dispose | Completeness and duplicate review |
| Received | Restricted | No | No | Security and classification processing only | No | Preserve pending decision | Source, rights, malware, classification |
| Scanning | No ordinary view | No | No | Isolated security processing only | No | No destructive action except safe rejection workflow | Security result |
| Quarantined | Security/legal reviewers only | Restricted | No | Isolated analysis copy only | No | Preserve per incident or dispute | Security, rights, legal, records |
| Rejected | Status and reason to authorized actor | No | No | No | No | Dispose or preserve according to reason | Appeal, incident, or evidence need |
| Active | According to classification | According to capability | Permission-scoped | Governed | Governed | According to retention | Ordinary controls |
| Restricted | Narrowed actors | Restricted | Limited or suppressed | Heightened | Restricted | No silent disposition | Reason and periodic review |
| Under Review | Limited | Restricted | Suppressed or marked | Analysis copies only | No by default | Preserve | Reviewer authority and outcome |
| Authoritative | Scoped authorized view | Conditional | Scoped | New version only | Conditional | Preserve supersession history | Authority owner |
| Evidentiary | Heightened | Heightened | Evidence-scoped | Non-destructive analysis only | Heightened | Hold or evidence basis controls | Chain-of-custody owner |
| Disputed | Limited and labeled | Restricted | Suppressed or labeled | Analysis only | No by default | Preserve competing positions | Rights, legal, records, or domain review |
| Superseded | Historical access | Conditional | Current result should prefer successor | No overwrite | Restricted | Preserve according to record basis | Successor linkage |
| Corrected | Scoped | Conditional | Surface current version with history | No overwrite | Conditional | Preserve correction lineage | Correction authority |
| Withdrawn | No ordinary use | Restricted | Suppressed | No | No | Preserve if required; otherwise dispose through process | Withdrawal basis |
| Archived | Limited | Heightened | Archive search only | Preservation migration only | Restricted | Retain per basis | Restore or access authority |
| Held | Narrowed | Heightened | Matter-scoped | No destructive transform | Heightened | Deletion suspended | Hold authority |
| Scheduled for Disposition | Limited | Restricted | Suppressed | No | No | Await approval and verification | Records and hold check |
| Deleted from Active Service | No | No | No | No | No | Backup and replica lifecycle continues as governed | Deletion verification |
| Cryptographically Deleted | No | No | No | No | No | Retain non-content deletion evidence | Key destruction evidence |
| Recovery-Restored | Limited until validation | No by default | Suppressed | Validation only | No | Preserve source and restored copy | Integrity, permissions, version, relationships |
| Orphaned | No or tightly limited | No | No | No | No | Reconcile steward, relationship, export, or disposition | Records and organization lifecycle |

---

# 14. Ingestion Classification Defaults

| Ingestion Channel | Initial Category | Initial Sensitivity | Initial State | Ordinary Availability Before Review |
|---|---|---|---|---|
| Direct user upload | User-selected category plus provisional validation | At least S2 when content is unknown | Received or Scanning | No |
| Mobile camera capture | Workflow category | Inherit workflow; otherwise S2 | Received or Scanning | No |
| Offline capture | Workflow category | Inherit workflow; otherwise S3 | Pending Sync then Received | No beyond authorized local capture view |
| Email attachment import | Imported Third-Party plus likely domain | S3 | Scanning | No |
| Cloud-drive import | Imported Third-Party plus likely domain | S3 | Scanning | No |
| External provider upload | Provider domain category plus Imported Third-Party | At least S2 | Received or Scanning | No until source and authorization validated |
| API or plugin upload | Integration-declared category plus Imported Third-Party | At least S2 | Received or Scanning | No |
| System-generated report | System-Generated plus source category | Inherit highest source tier | Active only after successful generation and lineage capture | Conditional |
| AI-generated output | AI-Generated plus source category | Inherit highest source tier | Under Review or Active depending on risk | Only within approved assistive workflow |
| Migration import | Imported Third-Party plus mapped source category | Inherit source or provisional S3 | Under Review | No until reconciliation |
| Recovery restore | Existing category and tier | Existing tier | Recovery-Restored | No until validation |

Unknown content must not default to S1 or public visibility.

---

# 15. Preview and Rendition Classification

| Rendition | Default Classification Rule | Special Requirement |
|---|---|---|
| Thumbnail | Inherits source category and sensitivity | Must not expose graphic, minor, identity, medical, or privileged content in search without authorization |
| Low-resolution preview | Inherits source | Must strip unnecessary metadata; may require blur, warning, or suppression |
| Streaming rendition | Inherits source | Enforce session authorization and prevent unauthorized direct-object access |
| Compressed copy | Inherits source | Record transformation; never replace required original |
| Redacted copy | Inherits source until validated; may receive narrower tier after approval | Preserve original, redaction reason, actor, and hidden-content testing |
| Watermarked copy | Inherits source | Watermark may show recipient or purpose but does not prove authenticity |
| OCR text | Inherits source | Mark as machine-extracted; no automatic authority; correctable with history |
| Transcript | Inherits source | Identify automated versus human-reviewed; preserve timing and uncertainty where relevant |
| Translation | Inherits source | Label translator or system; preserve original language; no legal or medical equivalence claim without review |
| Structured extraction | Inherits source | Link every field to source; distinguish confirmed from inferred values |
| Search index | Inherits source permission and tenant boundary | Purge or update when access, consent, deletion, or classification changes |
| Embedding | Inherits source and is treated as sensitive derived data | No identifiable cross-tenant learning; delete or restrict with source |
| AI summary | Inherits highest source tier and AI-Generated category | Separate facts, inferences, uncertainty, and human review status |
| AI-modified image or audio | Inherits source and AI-Modified category | Preserve original; label material changes; prohibit deceptive use |
| Evidence analysis copy | Inherits S7 and underlying sensitivity | Non-destructive; record analyst, tool, time, and transformation |

---

# 16. Search, Discovery, and Indexing Controls

Classification must control not only direct file access but also all discovery surfaces.

Required rules:

1. Search may not reveal that a restricted asset exists when existence itself is sensitive.
2. Search result titles, filenames, snippets, thumbnails, OCR text, transcript fragments, tags, and relationship labels must be permission-scoped.
3. Publicly authorized copies must not expose private originals, prior versions, consent records, restricted metadata, or internal annotations.
4. Minor, safeguarding, privileged, highly restricted, and quarantined assets must be excluded from general search by default.
5. Evidence indexes must remain matter-scoped and may not become general tenant search.
6. A user's ability to search a horse does not create access to every asset linked to that horse.
7. Revocation, relationship termination, consent withdrawal, reclassification, and deletion must propagate to indexes and caches.
8. AI retrieval must inherit the narrowest permission of the source and must not synthesize restricted facts from multiple inaccessible assets.
9. Cross-tenant indexing or embeddings must not permit identifiable retrieval or inference.
10. Search telemetry must not leak sensitive query terms or asset titles to unauthorized support or analytics systems.

---

# 17. Sharing and Publication Matrix

| Sharing Mode | Eligible Tiers | Required Controls | Prohibited Uses |
|---|---|---|---|
| In-tenant relationship share | S1-S4 as authorized | Current identity, role, relationship, purpose, capability, audit | Access based only on tenant membership or horse association |
| Named external recipient | S0-S4, exceptionally S5-S7 | Recipient verification, expiration, purpose, revocation, access log, minimum necessary rendition | Permanent forwarding authority or unrelated reuse |
| Provider workflow share | S1-S4, S7 where authorized | Provider identity, relationship, purpose, scoped record set, expiration | Broad lifetime record access from a single service event |
| Guardian-controlled share | S1-S4 involving minor where lawful | Guardian authority plus safeguarding limits and child-protection rules | Guardian override of mandatory reporting or legal preservation |
| Claim or legal production | S2-S7 | Authority validation, privilege review, manifest, chain of custody, minimum necessary scope | Informal bulk production without matter control |
| Public publication | S0 only | Rights, consent, audience, channel, duration, metadata stripping, withdrawal propagation | Public-by-default publishing, minor exposure, hidden metadata disclosure |
| Marketing campaign | S0 only for approved campaign | Copyright, publicity, testimonial, sponsor, duration, channel, withdrawal | Reuse beyond consent or rights scope |
| Evidence filing or public record | S7 plus lawful filing authority | Legal review, redaction, filing requirements, retained original | Treating lawful public filing as unlimited commercial license |
| Emergency operational access | S1-S4 and K3-K4 as authorized | Emergency basis, minimum necessary view, attribution, post-event review | General break-glass browsing or silent use |

No share link may broaden rights beyond the underlying authorization. Revocation of a link does not erase prior lawful downloads, but it must stop future platform-mediated access and trigger incident review where compromise is suspected.

---

# 18. Offline Eligibility Matrix

| Asset Profile | Default Offline Eligibility | Conditions |
|---|---|---|
| S0 public copy | Conditional | Rights permit local copy; no hidden metadata; device policy satisfied |
| S1 routine operational | Conditional | Active relationship, encrypted device, local expiration, revocation sync |
| S2 confidential | Restricted | Demonstrated operational need, minimum necessary, encrypted local store, no camera-roll export |
| S3 restricted | Prohibited by default | Explicit policy exception, named device, short retention, heightened audit |
| S4 highly restricted | Prohibited | Only founder- or canon-authorized exceptional workflow |
| S5 privileged or sealed | Prohibited by default | Specific legal workflow and device controls |
| S6 safeguarding-critical | Prohibited by default | Specific safeguarding or legal need; strongest controls |
| S7 evidence-critical | Restricted | Evidence collection or hearing need; immutable local package; custody record |
| S8 quarantined | Prohibited | No ordinary offline use |
| K3-K4 care or welfare-critical | Conditional even if sensitive | Narrow authorized subset, safe degradation, local expiry, emergency review |

Offline denial must not leave horse welfare without a safe alternative. A high-risk source asset may remain online-only while a narrowly redacted emergency instruction is made available offline.

---

# 19. AI, OCR, Transcription, and Analytics Eligibility

| Asset Profile | AI Analysis | OCR or Transcription | Embedding or Semantic Index | Analytics or Research |
|---|---|---|---|---|
| S0 public copy | Conditional | Conditional | Conditional | Conditional, within rights and purpose |
| S1 internal operational | Conditional | Allowed in approved workflow | Conditional | Aggregated or minimum necessary only |
| S2 confidential | Restricted | Conditional | Restricted | Separate authorization and de-identification review |
| S3 restricted | Heightened review | Restricted | Prohibited by default | Prohibited by default |
| S4 highly restricted | Prohibited by default | Restricted | Prohibited | Prohibited |
| S5 privileged or sealed | Prohibited by default | Prohibited by default | Prohibited | Prohibited |
| S6 safeguarding-critical | Prohibited by default | Prohibited by default | Prohibited | Prohibited except approved safety review |
| S7 evidence-critical | Restricted, non-destructive | Conditional with lineage | Prohibited by default | Matter-specific only |
| S8 quarantined | Security analysis tooling only | Isolated security tooling only | Prohibited | Security incident analysis only |

Customer assets may not be used for shared, public, general-purpose, or foundation-model training. Analytics and research authority may not be used as a backdoor to model training or identifiable cross-tenant learning.

---

# 20. Retention and Disposition Rules by Classification

Classification does not alone establish a fixed retention period. It establishes the handling consequences and the record bases that must be consulted.

| Category or Overlay | Primary Retention Basis | Disposition Constraint |
|---|---|---|
| Identity and Verification | Active identity, horse history, legal or fraud need | Preserve corrections and durable identifiers; remove unnecessary human verification artifacts when permitted |
| Medical, Diagnostic, Medication | Medical continuity, provider law, horse history, claim, consent | No destruction during active care need, claim, dispute, or hold |
| Veterinary Imaging | Medical continuity, provider obligation, historic significance, claim | Preserve required original fidelity and report linkage |
| Financial and Payment | Accounting, tax, contract, dispute, processor requirement | Remove prohibited credentials; preserve transaction evidence as required |
| Legal and Contractual | Contract term, limitation period, legal hold, policy version | Preserve executed and superseded versions; privilege survives archive |
| Safeguarding | Law, safeguarding policy, investigation, mandatory reporting, hold | Strong restrictions continue after matter closure; no routine deletion without review |
| Ownership and Transfer | Enduring horse history, title or custody dispute, contract | Preserve transfer lineage and competing claims |
| Registration and Pedigree | Enduring horse history and registry | Long-term preservation; migration and format monitoring |
| Competition and Historic | Event record, consent, historic designation | Public use may end while historic preservation continues privately |
| Training and Operational | Active relationship, service, safety, dispute | Private notes generally do not transfer with horse |
| Evidence and Claims | Hold, claim, proceeding, insurer, limitation period | No deletion until formal release and all bases reconciled |
| HR and Personnel | Employment law, contract, dispute, safeguarding | Strict non-transferability and access limitation |
| Marketing | Consent, license, campaign, claim | Stop public use after withdrawal; preserve consent and use evidence as required |
| System and AI-Generated | Source retention and audit need | Derived asset cannot outlive source restrictions without separate lawful basis |
| Temporary | Processing necessity only | Short expiry and secure disposal; no indefinite orphaning |
| Archived or Historic | Underlying record basis and preservation designation | Periodic integrity and format review; privacy remains |
| Security-Quarantined | Incident, legal, malware-analysis, evidence need | No silent deletion where incident or evidence preservation applies |

Where multiple bases apply, the longest valid preservation requirement ordinarily controls until formal reconciliation. Disposal must include originals, derivatives, indexes, caches, offline copies, replicas, and processor-held copies as applicable.

---

# 21. Classification Authority and Roles

| Action | Minimum Authority | Required Separation or Review |
|---|---|---|
| Select initial category in workflow | Authorized uploader or system within constrained choices | Automated and records validation may follow |
| Confirm ordinary category | Domain steward or trained authorized role | No self-expansion of access |
| Assign S0 Publicly Authorized | Rights/consent authority plus publication role | Separate copyright, publicity, minor, location, and purpose review |
| Assign or remove S5 Privileged or Sealed | Authorized legal role | Legal review and audit |
| Assign or remove S6 Safeguarding-Critical | Safeguarding-authorized role | Safeguarding and legal rules control |
| Assign or remove S7 Evidence-Critical | Claims, legal, safeguarding, security, or records authority | Chain-of-custody and hold review |
| Assign S8 Security-Quarantined | Security system or security-authorized role | Release requires security review |
| Mark Authoritative | Recognized issuer workflow or domain authority | Scope, effective date, validation, and version required |
| Mark Evidentiary | Authorized matter or preservation workflow | Does not establish factual truth |
| Down-classify S3-S8 | Authorized domain owner plus applicable privacy, legal, security, safeguarding, or records review | Reason and downstream propagation required |
| Change horse continuity status | Horse-record steward plus relationship/transfer authority | Protect non-transferable context and rights |
| Approve offline exception | Security, product, domain, and privacy authority as applicable | Device, expiry, revocation, and welfare alternative review |
| Approve public publication | Rights/consent and publication authority | No admin-only approval shortcut |
| Execute deletion | Records and system authority | Hold, retention, rights, backup, derivative, and audit checks |

A user may correct a caption without gaining authority to lower sensitivity, mark a record authoritative, release a hold, or publish the asset.

---

# 22. Reclassification Workflow

Every material reclassification must record:

1. asset identifier;
2. prior and new category;
3. prior and new sensitivity;
4. authority and evidence status impact;
5. continuity impact;
6. requesting actor;
7. approving actor or system;
8. constitutional and factual basis;
9. effective time;
10. affected relationships and audiences;
11. downstream derivatives, search indexes, offline copies, links, exports, caches, and processors;
12. notification requirement;
13. rollback or correction path; and
14. verification that enforcement propagated.

## 22.1 Up-Classification

Up-classification must restrict access promptly and may occur provisionally through automated detection where risk exists. Human review should follow for material impacts.

## 22.2 Down-Classification

Down-classification requires affirmative authority. Silence, elapsed time, prior public exposure, or reduced business interest is not enough.

## 22.3 Classification Dispute

A dispute must not be resolved solely by the uploader, current administrator, or first party to complain. EquineSync must preserve relevant evidence, apply interim protection, and route the matter to the proper rights, privacy, legal, safeguarding, security, records, or domain authority.

## 22.4 Propagation

A classification change is incomplete until all governed representations and access paths are reconciled or an exception is recorded. Updating a database label while leaving a public thumbnail, cached OCR text, active share link, offline copy, or external processor output unchanged is not closure.

---

# 23. Classification Conflict Rules

| Conflict | Governing Rule |
|---|---|
| Public consent conflicts with minor safeguarding | Safeguarding and minor protection govern |
| Horse continuity conflicts with privilege | Privilege remains protected; produce a lawful scoped fact or redacted copy if required |
| Medical need conflicts with ordinary confidentiality | Minimum necessary care access may be granted through authorized workflow; confidentiality remains for all other purposes |
| Legal hold conflicts with deletion request | Hold suspends deletion until valid release |
| Evidence preservation conflicts with metadata stripping | Preserve original metadata; create a controlled sharing copy if disclosure should be narrowed |
| Public record status conflicts with platform privacy | Lawful public status does not automatically authorize all metadata, republication, or marketing use |
| Operational criticality conflicts with high sensitivity | Provide reliable narrow access or safe alternative; do not broaden audience |
| Rights complaint conflicts with horse history | Restrict disputed use while preserving required history and evidence |
| AI feature request conflicts with restricted classification | Restrict or refuse AI processing; no convenience exception |
| External provider limitation conflicts with EquineSync preservation duty | Provider arrangement must satisfy controlling duty or the provider cannot be used |
| Search usefulness conflicts with access control | Access control governs; search may not reveal inaccessible content |
| Storage quota conflicts with historic, held, or welfare-critical asset | Protected asset is preserved; capacity is addressed without destructive surprise |

---

# 24. Classification Exceptions

An exception record must include:

- asset or class of assets;
- requested deviation;
- requesting actor;
- purpose;
- applicable constitutional rule;
- risk assessment;
- affected people, horses, organizations, and rights holders;
- duration;
- compensating controls;
- approvers;
- monitoring;
- revocation trigger;
- and closure evidence.

Exceptions may not authorize:

- public-by-default minor media;
- human biometric identification;
- shared-model training on customer assets;
- silent overwrite of originals;
- deletion during a valid hold;
- removal of material provenance from evidence;
- administrator bypass of access controls;
- cross-tenant disclosure;
- or unsupported public trust claims.

Those matters remain founder-reserved or constitutionally prohibited.

---

# 25. Required Implementation Artifacts Derived from This Matrix

This Matrix requires later creation and approval of, at minimum:

1. machine-readable asset-category dictionary;
2. sensitivity-tier control specification;
3. classification decision tree;
4. category and sensitivity field schema;
5. authority-status schema;
6. evidence-status schema;
7. horse-continuity-status schema;
8. operational-criticality schema;
9. classification role and permission matrix;
10. reclassification workflow specification;
11. automated provisional-classification rules;
12. metadata-restriction specification;
13. rendition and derivative inheritance rules;
14. search and indexing eligibility specification;
15. public-publication and consent checklist;
16. offline eligibility matrix;
17. AI/OCR/transcription eligibility matrix;
18. retention-basis mapping;
19. deletion-propagation specification;
20. classification audit event schema;
21. user-interface label and warning standard;
22. import and migration classification mapping;
23. legacy-asset remediation plan;
24. classification exception register;
25. classification quality metrics and review cadence;
26. support-access and break-glass procedure;
27. test plan and evidence package; and
28. owner and RACI assignment.

Creation of these artifacts does not itself authorize production use. They must pass the applicable implementation gates defined by the target constitutional candidate.

---

# 26. Mandatory Classification Test Scenarios

At minimum, later implementation evidence must prove the following:

1. an unknown upload is not exposed before scanning and classification;
2. a user cannot select S0 without valid publication authority;
3. a publicly authorized image does not expose original GPS metadata;
4. a competition video containing a minor receives minor protections;
5. a public horse profile does not reveal restricted identity documents;
6. access to a horse does not reveal private trainer notes;
7. a veterinarian receives only the authorized medical subset;
8. a provider upload does not become authoritative automatically;
9. a photograph of medication does not become a medication administration record automatically;
10. veterinary imaging preserves the original while generating a display copy;
11. an AI-enhanced image remains linked to and distinguishable from the original;
12. OCR text inherits the source asset's permissions;
13. a search snippet disappears when access is revoked;
14. an embedding is deleted or restricted when its source is deleted or reclassified;
15. a confidential asset cannot be shared through an anonymous permanent link;
16. a link recipient cannot browse related assets without separate authority;
17. forwarding a link does not transfer authorization;
18. an S4 asset is excluded from ordinary offline synchronization;
19. a K4 emergency instruction can be made available through a narrow safe alternative without exposing the full source record;
20. a lost device causes offline asset revocation or protected expiry as designed;
21. a legal hold prevents deletion of originals, derivatives, and indexes;
22. a redacted copy does not contain recoverable hidden text or metadata;
23. a privileged asset is excluded from routine AI and semantic indexing;
24. a safeguarding asset is not displayed in ordinary thumbnails or notifications;
25. a graphic image requires an appropriate warning and authorized purpose;
26. an evidence analysis copy does not mutate the original;
27. an evidence export includes a valid manifest and hash verification;
28. a hash verification result is not represented as proof of factual truth;
29. a superseded authoritative record remains historically available but is not presented as current;
30. a disputed ownership document is labeled and preserved without automated title resolution;
31. a horse transfer carries an enduring medical record but not unrelated provider notes;
32. withdrawal of marketing consent removes controlled public renditions while preserving required consent history;
33. an imported cloud-drive file does not inherit the external drive's permissions as EquineSync authority;
34. duplicate identical binaries preserve distinct submission and custody events;
35. a malware-positive file is quarantined and removed from ordinary search and preview;
36. a rejected upload is disposed of or preserved according to its rejection reason;
37. an orphaned asset is not left broadly accessible after account closure;
38. an archived asset retains its underlying sensitivity and rights;
39. a recovery-restored asset is not activated before identity, hash, permissions, relationships, and versions are validated;
40. a classification change propagates to thumbnails, OCR, search, links, offline copies, and processors;
41. a down-classification requires authorized review and a recorded reason;
42. support personnel cannot use administrative capability to bypass asset permissions;
43. classification audit logs avoid exposing unnecessary sensitive content;
44. a tenant-specific residency restriction follows the original and derived assets;
45. quota enforcement does not delete held, historic, or welfare-critical assets without authority;
46. public-record status does not automatically enable marketing reuse;
47. a system-generated report identifies its inputs and generation version;
48. an AI summary distinguishes source facts, inferences, and uncertainty;
49. a user can challenge a classification and obtain a governed review; and
50. no classification label or badge is used to make an unsupported public trust claim.

---

# 27. Classification Metrics and Monitoring

Later operational governance should measure, at minimum:

- percentage of permanent assets with complete category and sensitivity assignments;
- assets remaining in provisional classification beyond the allowed period;
- rate of up-classification and down-classification;
- classification changes that fail downstream propagation;
- public assets lacking complete rights or consent evidence;
- restricted assets present in general search or thumbnail systems;
- offline copies exceeding policy duration;
- orphaned assets;
- quarantined assets awaiting resolution;
- privileged or safeguarding assets processed by unauthorized tools;
- classification-related access denials and appeals;
- false-positive and false-negative automated classification rates;
- assets with conflicting category, authority, evidence, or continuity states;
- historic assets lacking format-integrity review;
- classification exceptions and overdue expirations;
- and incidents caused by incorrect classification or handling.

Metrics must not become a secondary source of sensitive content. Dashboards and logs must use minimum necessary identifiers and role-scoped access.

---

# 28. P2 Implementation Handoffs

This Matrix closes the policy-definition portion of the classification workstream but leaves the following nonblocking pre-implementation handoffs open:

| ID | Handoff | Required Before |
|---|---|---|
| CL-P2-01 | Final machine-readable category and sensitivity vocabulary | Schema approval |
| CL-P2-02 | Role and capability assignments for classification and reclassification | Implementation |
| CL-P2-03 | Classification decision tree and guided user experience | Implementation |
| CL-P2-04 | Automated provisional-classification model and confidence thresholds | AI or automation activation |
| CL-P2-05 | Search, preview, OCR, transcript, and embedding inheritance specification | Search or processing activation |
| CL-P2-06 | Offline eligibility and local-retention specification | Offline activation |
| CL-P2-07 | Public publication, rights, consent, and withdrawal workflow | Public sharing activation |
| CL-P2-08 | Category-to-retention-basis mapping | Retention execution |
| CL-P2-09 | Legacy and migration classification mapping | Migration |
| CL-P2-10 | Audit event schema and monitoring thresholds | Runtime activation |
| CL-P2-11 | Classification test plan and executed evidence | Production authorization |
| CL-P2-12 | Named owners, RACI, exception workflow, and review cadence | Governance gate closure |

These handoffs are not unresolved founder decisions. They are subordinate implementation and evidence work.

---

# 29. Founder Decision Traceability

| Founder Decision | Matrix Treatment |
|---|---|
| FD01-FD04 | Rights, stewardship, multiple interests, and horse-continuity classifications |
| FD05 | Constitutional category matrix |
| FD06-FD07 | Evidence and authority status matrices |
| FD08-FD10 | Enduring history, non-transferable context, deletion, restriction, and supersession |
| FD11-FD15 | Sensitivity tiers, public use, minors, biometrics, and metadata restrictions |
| FD16-FD20 | AI eligibility, labeling, provenance, and no shared-model training |
| FD21-FD25 | Versioning, original preservation, duplicate treatment, malware, and integrity |
| FD26-FD30 | Encryption, sharing, offline use, large-file handling, and quarantine response |
| FD31-FD34 | Holds, chain of custody, signatures, and evidence exports |
| FD35-FD37 | Copyright, commercial rights, and consent withdrawal |
| FD38-FD40 | Provider-neutral storage, backup, recovery, and residency implications |
| FD41-FD44 | Provider upload, mobile capture, imports, and API parity |
| FD45 | More-protective and subject-matter conflict rules |
| FD46-FD48 | Many-to-many relationships and metadata mutability |
| FD49-FD50 | Sensitive and graphic assets and historic preservation |

All FD01-FD50 are represented. No new implementation authority is created.

---

# 30. Review Determination

## 30.1 Classification Completeness

This Matrix provides a complete controlled classification and handling baseline for the constitutional review package.

It defines:

- 28 primary constitutional categories;
- nine sensitivity regimes;
- 15 secondary overlays;
- eight authority states;
- eight evidence states;
- seven horse-continuity states;
- six operational-criticality levels;
- lifecycle handling overlays;
- ingestion defaults;
- derivative inheritance;
- search, sharing, offline, AI, retention, and reclassification controls;
- 50 mandatory test scenarios; and
- 12 nonblocking P2 implementation handoffs.

## 30.2 Severity Assessment

| Measure | Result |
|---|---:|
| P0 critical findings introduced or remaining in this artifact | 0 |
| P1 adoption-blocking findings introduced or remaining in this artifact | 0 |
| P2 implementation handoffs | 12 |
| Founder decisions traced | 50 of 50 |
| Primary categories defined | 28 |
| Sensitivity regimes defined | 9 |
| Mandatory test scenarios | 50 |

## 30.3 Lifecycle and Authority

The proper disposition is:

`MEDIA_DIGITAL_ASSET_CLASSIFICATION_AND_HANDLING_MATRIX_COMPLETE_READY_FOR_STATE_AND_TRANSITION_MATRIX_WITH_NONBLOCKING_P2`

This disposition authorizes preparation of the next controlled artifact only.

It does not authorize:

- canon adoption;
- canon lock;
- schema creation or mutation;
- classification-engine activation;
- AI classification;
- customer-data ingestion;
- storage configuration;
- public publication;
- external sharing;
- offline synchronization;
- retention or deletion execution;
- migration;
- runtime activation;
- production access;
- public trust claims; or
- public launch.

---

# 31. Final Statement

A useful classification system does more than place files into labeled drawers.

It must preserve the difference between a photograph and a diagnosis, a document and a right, a public image and public ownership, a horse relationship and permission, an intact file and a truthful claim, a historic record and unrestricted publicity, and an urgent care need and broad disclosure.

EquineSync's classification framework must therefore travel with the asset everywhere the asset travels: into thumbnails, transcripts, search results, backups, offline devices, integrations, evidence packages, migrations, archives, and eventual disposition.

A label that does not control those paths is decoration. This Matrix requires classification to function as enforceable governance.
