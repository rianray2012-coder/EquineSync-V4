# Equine Sync Compliance, Payments, and Legal Docs Notes

## 1. Important disclaimer

This document is product and engineering guidance, not legal, tax, accounting, payment, or compliance advice. Before launch, Equine Sync should review minor/student communication, parent consent, payments, tax reporting, waivers, contracts, electronic signatures, data retention, privacy, and terms of service with qualified advisors.

## 2. Minor/student safety requirements

Product requirement:

- Students under 18 should have a parent/guardian profile.
- Adult-to-minor communication should not be private one-on-one messaging.
- Parent/guardian should be automatically included on communication involving minor lesson students.
- The messaging service should enforce this rule server-side.
- Minor-related thread creation should be audit logged.
- Parent/guardian should be able to view lesson schedule, messages, waivers, payments, and approvals.

Implementation requirements:

- Store student date of birth or minor status.
- Require at least one guardian for users marked under 18.
- Include guardian in trainer/student message threads by default.
- Prevent parent/guardian removal from a minor thread unless a valid alternate guardian/adult policy is satisfied.
- Require parent approval for event signups, waivers, media releases, and payments when configured.

Reference links:

- U.S. Center for SafeSport MAAPP: https://maapp.uscenterforsafesport.org/
- 2025 MAAPP: https://maapp.uscenterforsafesport.org/2025-maapp/

## 3. Children's privacy and under-13 users

Product requirement:

- Decide whether Equine Sync will allow accounts for children under 13.
- If yes, design a parent-controlled onboarding flow and avoid collecting more child data than necessary.
- If no, block under-13 direct accounts and require parent-managed profiles only.

Implementation requirements:

- Add age gate or parent-managed student profile flow.
- Do not allow an under-13 child to create an independent account unless legal review approves the process.
- Keep parent consent records if collecting personal information from children under 13.
- Limit student profile fields to operational needs.

Reference links:

- FTC COPPA Rule: https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa
- FTC 2025 COPPA amendments: https://www.federalregister.gov/documents/2025/04/22/2025-05904/childrens-online-privacy-protection-rule

## 4. Payments requirements

If Equine Sync allows clients to pay barn owners and trainers, it may need a platform payment model rather than a simple store checkout.

Product decisions needed:

- Who is the merchant of record?
- Does money go directly to barn/trainer, or to Equine Sync first?
- Will Equine Sync charge a platform fee?
- Are ACH, card, autopay, and saved payment methods supported?
- Who handles refunds, disputes, chargebacks, and failed payments?
- How are taxes, receipts, and payout reporting handled?
- Can a trainer and barn both receive funds for the same client/event?

Implementation requirements:

- Use a payment processor for card/bank data; do not store raw card data directly.
- Store processor IDs, payment status, invoice status, receipt URLs, and refund records.
- Build idempotency into payment creation and webhook processing.
- Use webhooks as source of truth for payment success/failure.
- Keep payment features behind a feature flag until payment model is approved.

Reference links:

- Stripe Connect docs: https://docs.stripe.com/connect
- Stripe Connect product overview: https://stripe.com/connect

## 5. Legal documents and electronic signatures

Product requirement:

- Barn Owners and Trainers need to send, sign, save, and track legal documents.
- Examples: boarding contract, lesson agreement, liability waiver, vet approval, emergency care authorization, media release, payment authorization, cancellation policy.
- Signed documents should be stored with user, horse, barn, and event where applicable.
- Required documents should block onboarding, participation, or signup when configured.

Decisions needed:

- Build in-house e-signature or integrate with a third-party signature provider?
- What counts as a valid signature for each document type?
- Does a countersignature need to be captured?
- How long are signed documents retained?
- How are updated template versions handled?
- Who can download signed documents?
- How are parent/guardian signatures handled for minors?

Implementation requirements:

- Document templates have versioning.
- Sent documents create an envelope record.
- Signatures create signature records.
- Final signed copy is immutable or tamper-evident.
- System tracks draft, sent, viewed, signed, declined, expired, voided, and completed.
- Parent/guardian signature is required for minor documents when configured.

## 6. Google sign-in and account linking

Product requirement:

- Users can sign up/sign in with Google.
- Existing users can link a Google account.
- Invited users can accept invites using Google sign-in.
- Duplicate accounts should be prevented.

Implementation requirements:

- Store Google provider subject ID separately from email.
- Treat verified email as a matching signal but not the only identity key.
- If a user with same verified email exists, prompt account linking rather than silently creating duplicate.
- Keep password/account recovery option where appropriate.
- Protect invite acceptance against token replay and wrong-account linking.

Reference link:

- Google Identity: https://developers.google.com/identity/

## 7. Privacy and data retention decisions

Decisions needed:

- What data does a barn retain after a client leaves?
- What data does a client retain after leaving a barn?
- What data transfers when a horse is sold?
- What health photos/documents are shared with a new owner?
- What message history remains visible after transfer?
- Can a user request export or deletion?
- How are audit logs retained?
- How is minor data archived when the student becomes an adult?

Recommended product rules:

- Keep historical action logs for operational integrity.
- Remove active access immediately when membership ends.
- Provide export options before horse transfer or membership termination.
- Separate horse-owned records from barn-owned operational records.
- Make transfer data choices explicit in the transfer wizard.

## 8. Barn directory privacy

Directory should not simply expose all contact information to all users by default.

Recommended controls:

- User chooses visibility for phone/email where possible.
- Barn staff can access emergency contacts as needed.
- Minor student contact info should not be broadly visible.
- Parent/guardian contact should be used for lesson student communication.
- Vendors should see only appointment-relevant information.

## 9. Launch review checklist for advisors

Before launch, ask qualified advisors to review:

- Terms of Service.
- Privacy Policy.
- Payment processing and funds flow.
- Refund/dispute policy.
- Tax reporting responsibilities.
- Electronic signature process.
- Liability waiver handling.
- Minor/student communication policy.
- Parent consent and under-13 handling.
- Data retention and deletion policy.
- Vendor access and emergency contact visibility.
