# Equine Sync Roles and Permissions Matrix

## 1. Access-control principle

Equine Sync should use deny-by-default, scope-based access control. A user should receive access only through a defined relationship to a barn, horse, student, event, document, task, or invoice.

The same person may have multiple roles. Example: a user may be a client at Barn A, a trainer at Barn B, and a parent for a lesson student at Barn C.

## 2. Role definitions

| Role | Description |
|---|---|
| Equine Sync Admin | Platform-level support/admin role with full authorized access for troubleshooting and management. |
| Barn Owner | Owns or controls the barn/facility account and can manage operations, users, billing, docs, maps, and settings. |
| Barn Manager | Runs daily barn operations; can manage horses, staff, schedules, whiteboard, and many client-facing functions. |
| Trainer | Manages training/lesson clients, ride logs, event signups, lesson communications, and trainer-related payments/documents. |
| Staff | Performs assigned barn tasks and logs approved horse/facility actions. |
| Client / Horse Owner | Owns or leases horse; views and manages permitted horse, documents, payments, calendar, messages, and ride logs. |
| Parent / Guardian | Controls or monitors a minor student's lesson account, communications, waivers, payments, and approvals. |
| Lesson Student | Limited student role; can view allowed lesson info and log permitted activities if allowed by barn. |
| Vendor | Limited appointment/service access for farrier, vet, bodyworker, saddle fitter, or other service provider. |
| Read-Only Guest | Optional limited view-only role for demos, auditors, or temporary review. |

## 3. Permission matrix legend

| Code | Meaning |
|---|---|
| Full | Can view, create, edit, archive/delete, assign, approve, and manage settings within scope. |
| Manage | Can create/edit/assign but may not delete/archive or change ownership/settings. |
| Edit | Can view and edit permitted records. |
| Log | Can add action/task/ride entries but cannot change core records. |
| View | Can view permitted records only. |
| Limited | Access depends on explicit assignment, consent, or event relationship. |
| None | No access. |

## 4. Core permissions by module

| Module | Admin | Barn Owner | Manager | Trainer | Staff | Client | Parent | Student | Vendor |
|---|---|---|---|---|---|---|---|---|---|
| Platform settings | Full | None | None | None | None | None | None | None | None |
| Barn settings | Full | Full | Manage | Limited | None | None | None | None | None |
| User invites | Full | Full | Manage | Manage clients | None | Request only | Manage student | None | None |
| Role assignment | Full | Full | Manage below owner | Limited | None | None | Student only | None | None |
| Horse profile | Full | Full | Manage | Edit assigned | View/log assigned | Edit owned | View linked | Limited | Limited |
| Horse ownership transfer | Full | Full | Manage | Request | None | Request/approve owned | Limited | None | None |
| Barn transfer/membership | Full | Full | Manage | Manage clients | None | Request | Manage student | None | None |
| Daily whiteboard | Full | Full | Full | Manage assigned | Log/complete | Limited log | View/log student | Limited log | Limited |
| Action logs | Full | Full | Full | Manage assigned | Log | Log permitted | View/log student | Log permitted | Log service |
| Medication actions | Full | Full | Manage approved | Limited approved | Limited approved | Limited | View student | None | Limited service |
| Barn maps | Full | Full | Manage | View assigned | View assigned | View permitted | View student permitted | Limited | Limited |
| Calendar | Full | Full | Full | Manage training | View assigned | View own/horse | View student | View own | View appts |
| Event signups | Full | Full | Manage | Full trainer events | View assigned | Accept/decline | Approve student | Limited | None |
| Group messaging | Full | Full | Manage | Manage assigned groups | Limited | Reply/view groups | Student groups | Limited | Limited |
| Direct messaging | Full | Full | Manage | Permitted only | Permitted only | Permitted only | Included for minor | No private adult DM | Limited |
| Parent/minor messaging rules | Full | Full | Manage | Enforced | Enforced | Enforced | Full guardian | Limited | None |
| Barn directory | Full | Full | Manage | View permitted | View permitted | View permitted | View student permitted | Limited | Limited |
| Health records/photos | Full | Full | Manage | Edit assigned | Log permitted | Edit owned | View student horse if linked | Limited | Limited service |
| Ride logs | Full | Full | Manage | Manage assigned | Limited | Create/share | View student | Create limited | None |
| Documents/templates | Full | Full | Manage | Manage trainer docs | Staff docs only | Sign/view own | Sign/view student | View limited | Sign/view own |
| Payments/invoices | Full | Full | Manage | Manage trainer invoices | None | Pay/view own | Pay/view student | None | None |
| Reports/exports | Full | Full | Manage | Assigned only | None | Own data | Student data | None | None |
| Audit logs | Full | Full barn | Manager scope | Limited own actions | Own actions | Own actions | Student actions | Own actions | Own actions |

## 5. Permission rules that engineering should enforce

### 5.1 Scope before role

A role gives capability, but the user must also be in scope. Example: a Trainer role can edit assigned horses, but only horses assigned to that trainer or trainer's program.

### 5.2 Explicit relationships

Access can come from:

- Barn membership.
- Horse ownership or lease relationship.
- Trainer assignment.
- Staff assignment.
- Parent/guardian relationship.
- Event participation.
- Document recipient status.
- Vendor appointment assignment.

### 5.3 Multi-role conflict rule

When a user has multiple roles in the same barn, use the highest allowed permission within that barn, unless a safety rule overrides it. Minor communication rules override role permission.

### 5.4 Minor safety override

No adult role can privately message a minor student without parent/guardian inclusion. This should be enforced by the messaging service, not left to UI behavior.

### 5.5 Delete versus archive

Prefer archive over hard delete for:

- Horses.
- Users/memberships.
- Documents.
- Invoices/payments.
- Messages.
- Action logs.
- Health records.
- Transfers.

Hard delete should be restricted to platform admin and only where legally/operationally appropriate.

### 5.6 Audit log requirement

Audit these events:

- Role changed.
- User invited, accepted, removed, or transferred.
- Horse created, edited, archived, transferred, or assigned.
- Horse location changed.
- Health record or photo added/deleted.
- Medication/care action logged.
- Payment invoice/payment/refund status changed.
- Document sent/signed/voided/expired.
- Message thread created involving a minor.
- Calendar event created/edited/deleted.
- Admin override used.

## 6. Role test cases

| Test | Expected result |
|---|---|
| Admin opens every module | Admin has full authorized access and is not read-only. |
| Barn Owner invites staff | Invite can be sent, role assigned, status tracked. |
| Manager removes staff from barn | Staff loses barn access but action history remains. |
| Trainer opens unassigned horse | Trainer cannot view unless barn grants access. |
| Client opens another client's invoice | Access denied. |
| Parent opens student messages | Parent can see student-related messages. |
| Adult trainer messages minor student | Parent/guardian is automatically included or message creation is blocked. |
| Student tries to edit barn settings | Access denied. |
| Vendor opens barn directory | Vendor sees only permitted appointment/contact info. |
| User belongs to two barns | Data is separated by selected barn context. |
