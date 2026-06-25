# Equine Sync Build Packet README

## Purpose

This packet turns the current "items still needed" list into build-ready guidance for product, UX, engineering, QA, and launch planning.

The documents are intended to answer four questions:

- What are we building?
- Who can do what?
- What flows must work before launch?
- How do we test and release safely?

## Documents included

| Document | Use it for |
|---|---|
| 00_Build_Packet_README.md | Orientation and recommended order of use. |
| 01_Product_Requirements_Document.md | Product scope, personas, modules, priorities, and acceptance criteria. |
| 02_Roles_and_Permissions_Matrix.md | Role definitions and access-control rules. This should drive engineering. |
| 03_User_Flows_and_Acceptance_Criteria.md | Step-by-step workflows for invites, onboarding, transfers, tasks, messaging, payments, documents, and events. |
| 04_Data_Model_and_Technical_Guide.md | Suggested entities, relationships, state machines, APIs, audit logging, notifications, and security notes. |
| 05_Roadmap_and_Feature_Backlog.md | Phased delivery plan, epics, dependencies, and risk register. |
| 06_QA_and_UAT_Test_Plan.md | Functional, role-based, regression, mobile, payment, document, and launch testing. |
| 07_Compliance_Payments_and_Legal_Docs_Notes.md | Product requirements for minor safety, parent profiles, payments, electronic signatures, and privacy review. Not legal advice. |
| 08_Launch_Checklist.md | Go-live checklist, launch runbook, and post-launch monitoring. |
| 09_Decision_Log_and_Open_Questions.md | Decisions the team still needs to make before development or release. |

## Recommended order for the build team

1. Start with the Product Requirements Document.
2. Approve the Roles and Permissions Matrix before engineering starts core access-control work.
3. Walk through User Flows with product, design, and engineering.
4. Confirm the Data Model and Technical Guide with engineering.
5. Convert the Roadmap and Feature Backlog into tickets.
6. Use the QA and UAT Test Plan as the release gate.
7. Review Compliance, Payments, and Legal Docs with legal/accounting/payment advisors.
8. Use the Launch Checklist for go-live readiness.

## Build principle

Equine Sync is not just a horse profile app. It is a role-based barn operating system. The highest-risk build area is permissions: one user can have multiple roles across multiple barns, and one horse can be connected to owners, trainers, staff, parents, students, and vendors.

## MVP definition

The first production-ready release should include:

- Working admin access with no accidental read-only limitations.
- User, barn, horse, membership, and role models.
- Invitation and registration flows.
- Basic horse profile with care and location data.
- Whiteboard/action logging for daily barn operations.
- Barn calendar and notifications.
- Group and direct messaging, with parent/guardian inclusion for minors.
- Parent profile for lesson students.
- Basic document upload/signing status tracking or integration decision.
- Basic payment flow or confirmed payment integration plan.
- QA test coverage for every role.

## Build gate warning

Do not launch public client onboarding until the following are verified:

- Admin can create, edit, archive, delete, invite, approve, and manage settings.
- Barn Owner and Barn Manager permissions work as expected.
- Client and parent roles cannot see private data they should not see.
- Minor/student messaging cannot happen privately without parent/guardian inclusion.
- Horse transfer and barn transfer do not leak old-barn data.
- Payment and document flows have been reviewed by the appropriate professional advisors.

## Source links used in compliance/integration notes

| Topic | Link |
|---|---|
| Google Identity | https://developers.google.com/identity/ |
| Stripe Connect documentation | https://docs.stripe.com/connect |
| Stripe Connect product overview | https://stripe.com/connect |
| FTC COPPA Rule | https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa |
| FTC 2025 COPPA amendments | https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule |
| U.S. Center for SafeSport MAAPP | https://maapp.uscenterforsafesport.org/ |
| 2025 MAAPP | https://maapp.uscenterforsafesport.org/2025-maapp/ |
