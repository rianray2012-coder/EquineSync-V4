# Equine Sync Decision Log and Open Questions

## 1. How to use this document

Use this as a decision tracker. Each unresolved decision should receive an owner and due date before engineering work starts on that module.

Suggested status values:

- Open.
- Proposed.
- Approved.
- Rejected.
- Deferred.

## 2. Product scope decisions

| Question | Why it matters | Owner | Status |
|---|---|---|---|
| What is the MVP launch scope? | Prevents endless build expansion. | Product | Open |
| Which features are disabled behind feature flags at launch? | Allows safe phased release. | Product/Engineering | Open |
| Is Equine Sync web-only first, or web plus mobile app? | Affects authentication, push, camera upload, and offline support. | Product | Open |
| Which customer type launches first: boarding barns, trainers, lesson programs, or mixed barns? | Affects onboarding and prioritization. | Product | Open |

## 3. Roles and permissions decisions

| Question | Why it matters | Owner | Status |
|---|---|---|---|
| Can Barn Managers invite/remove users or only recommend changes? | Controls operational authority. | Product | Open |
| Can Trainers invite clients independently under a barn account? | Affects barn/trainer hierarchy. | Product | Open |
| Can Clients edit horse care data directly or submit change requests? | Affects trust and data quality. | Product | Open |
| Can Staff see client contact info? | Privacy issue. | Product/Legal | Open |
| Can Vendors access the app? | Adds role complexity. | Product | Open |
| What can Read-Only Guest see? | Useful for demos but risky if broad. | Product | Open |

## 4. Horse data and transfer decisions

| Question | Why it matters | Owner | Status |
|---|---|---|---|
| What records transfer when a horse is sold? | Prevents privacy disputes. | Product/Legal | Open |
| Does old owner keep archived access to historical records? | Important for invoices, documents, and health data. | Product/Legal | Open |
| Can new owner see old vet/health photos automatically? | Sensitive data decision. | Product/Legal | Open |
| Can barns keep copies of records after horse leaves? | Operational/legal retention. | Product/Legal | Open |
| Should transfers require approval from current owner only, barn owner only, or both? | Affects fraud/error prevention. | Product | Open |

## 5. Barn transfer decisions

| Question | Why it matters | Owner | Status |
|---|---|---|---|
| What happens to unpaid invoices when a client leaves a barn? | Payment/accounting issue. | Product/Finance | Open |
| What happens to signed documents after a client leaves? | Legal retention. | Product/Legal | Open |
| What message history remains visible after leaving? | Privacy issue. | Product/Legal | Open |
| Can a client self-remove from a barn? | Control and support issue. | Product | Open |

## 6. Minor/student decisions

| Question | Why it matters | Owner | Status |
|---|---|---|---|
| Will under-13 students have independent logins? | COPPA/privacy design. | Product/Legal | Open |
| Is parent/guardian inclusion required for all under-18 communication? | Core safety requirement. | Product/Legal | Proposed |
| Can a minor student send a message first? | Safety and moderation. | Product | Open |
| Can multiple guardians be included? | Real family structures. | Product | Open |
| What happens when a student turns 18? | Account transition flow. | Product/Legal | Open |

## 7. Messaging decisions

| Question | Why it matters | Owner | Status |
|---|---|---|---|
| Are barn admins allowed to review message history? | Privacy and safety tradeoff. | Product/Legal | Open |
| Are read receipts required? | Useful but may create pressure/privacy concerns. | Product | Open |
| Will SMS be supported? | Cost and compliance. | Product/Finance | Open |
| How are emergency alerts handled? | Safety-critical communication. | Product | Open |

## 8. Payment decisions

| Question | Why it matters | Owner | Status |
|---|---|---|---|
| Who is merchant of record? | Core payment/legal/accounting decision. | Finance/Legal | Open |
| Does Equine Sync charge a platform fee? | Business model. | Leadership/Finance | Open |
| Are funds paid to barns/trainers directly? | Processor integration design. | Finance/Engineering | Open |
| Are ACH payments supported? | Lower fees but more complexity. | Finance/Product | Open |
| Are autopay and saved methods supported? | Convenience but more compliance UX. | Product/Finance | Open |
| How are refunds, disputes, and chargebacks handled? | Support/accounting risk. | Finance/Support | Open |

## 9. Document/signature decisions

| Question | Why it matters | Owner | Status |
|---|---|---|---|
| Build in-house signing or integrate third-party e-signature? | Major build/scope decision. | Product/Engineering/Legal | Open |
| What document types are supported at launch? | Scope control. | Product | Open |
| Are templates editable inside Equine Sync? | Product complexity. | Product/Engineering | Open |
| Do documents require countersignature? | Legal workflow. | Legal/Product | Open |
| How long are signed documents retained? | Legal/privacy. | Legal | Open |

## 10. Maps/location decisions

| Question | Why it matters | Owner | Status |
|---|---|---|---|
| Is drag/drop map required for MVP or can location assignment launch first? | UX/build complexity. | Product | Open |
| Can clients see full barn map or only their horse? | Privacy/security. | Product | Open |
| Are GPS maps needed, or schematic barn maps only? | Scope. | Product/UX | Open |
| Should capacity limits be hard stops or warnings? | Operational flexibility. | Product | Open |

## 11. Open technical decisions

| Question | Why it matters | Owner | Status |
|---|---|---|---|
| What auth provider will be used? | Impacts Google sign-in and security. | Engineering | Open |
| What file storage service will be used? | Health photos, docs, messages. | Engineering | Open |
| What notification provider will be used? | Email/push/SMS. | Engineering | Open |
| What payment processor will be used? | Payment model. | Engineering/Finance | Open |
| What e-signature provider, if any, will be used? | Legal docs. | Engineering/Legal | Open |
| What reporting/export format is required? | Customer support and data portability. | Product/Engineering | Open |

## 12. Initial recommended decisions

These are recommended starting points for speed and safety:

- Build scoped role-based access control before feature expansion.
- Treat horse transfer as a controlled workflow, not a simple owner field edit.
- Require parent/guardian profiles for lesson students under 18.
- Enforce minor messaging rules on the server.
- Launch with location assignment first if drag/drop maps slow down MVP.
- Keep payments and legal document signing behind feature flags until reviewed.
- Archive rather than hard-delete operational records.
- Use audit logs for all high-risk actions.
