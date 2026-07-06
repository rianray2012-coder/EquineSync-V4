# RF5 Web Enrollment and Account Health Opening Gate Report

Phase: `RF5`
Overall status: `ready`

## Proof Rows

| Key | Status | Evidence | Next Action |
| --- | --- | --- | --- |
| public_enrollment_route | ready | `/enroll` is registered as a public route before credential collection. | RF18 should run end-to-end enrollment UAT across supported device sizes. |
| home_signup_entry_points_route_to_enrollment | ready | Landing navigation, hero, role cards, pricing CTAs, and footer Join actions route to `/enroll`. | Founder should approve path order and copy before broader launch. |
| login_signup_entry_point | ready | The sign-in page now gives no-account users a Join EquineSync action. | RF18 should test the login-to-enrollment path with analytics and support instrumentation. |
| required_enrollment_paths_inventory | ready | 4 required enrollment paths are declared with role mapping, critical data, and deferred phase ownership. | RF7/RF9/RF10 should deepen the owner, trainer, and provider workflows without changing RF5 claims. |
| invite_only_roles_excluded_from_public_enrollment | ready | Rider, guardian, and staff accounts are not public main enrollment paths; RF5 offers invite guidance and a separate limited individual-owner signup branch. | RF7/RF18 must implement and test the limited-trial/access-cap semantics before stronger claims. |
| signup_receives_enrollment_context | ready | Signup requires enrollment context, locks the public role to the selected path, and displays a changeable enrollment context. | Decide which path data becomes server-validated in RF7/RF9/RF10. |
| leasee_invite_caveat_recorded | ready | Leasee access is recorded as invite-only from owner or assigned trainer while preserving owner oversight. | RF7 must implement leasee invite/grant semantics before leasee access is claimed live. |
| signup_backend_contract_not_expanded | ready | RF5 does not add signup schema or auth permission changes; extra client enrollment context remains non-authoritative evidence. | Backend persistence and validation for enrollment-specific data should be explicit future work. |
| admin_account_health_inventory | ready | 11 platform-admin support/account-health route surfaces are present for RF5 inventory. | A later RF5 pass can add privacy-scrubbed metrics without exposing sensitive free text. |
| later_phase_boundaries_preserved | ready | Enrollment UI names later phase ownership rather than claiming completed owner/trainer/provider depth. | Keep RF7/RF9/RF10/RF18 open until those workflows are implemented and tested. |

## Enrollment Paths

| Path | Signup Role | Deferred Depth Phase |
| --- | --- | --- |
| individual_horse_owner | horse_owner | RF7 |
| barn_facility_owner | barn_owner | RF5/RF12 |
| service_provider | service_provider | RF10 |
| trainer | trainer | RF9 |

## Invite-Only / Limited Trial Caveats

- Rider, guardian, and staff accounts are not public main enrollment paths.
- Those users should normally enroll from a trainer, barn owner, barn manager, or boss invite.
- RF5 records a limited seven-day individual-owner trial option when contact information for a facility, trainer, or provider is supplied.
- Leasee access must be invite-only from the horse owner or assigned trainer while owner oversight remains intact.

## Account-Health Inventory

| Admin Route | RF5 Status |
| --- | --- |
| /admin/portal/users | inventory present |
| /admin/portal/approvals | inventory present |
| /admin/portal/facilities | inventory present |
| /admin/portal/subscriptions | inventory present |
| /admin/portal/billing | inventory present |
| /admin/portal/support | inventory present |
| /admin/portal/alerts | inventory present |
| /admin/portal/reports | inventory present |
| /admin/portal/integrations | inventory present |
| /admin/portal/settings | inventory present |
| /admin/portal/audit-logs | inventory present |

## Founder Decision Rows

| Decision | Status | Phase | Notes |
| --- | --- | --- | --- |
| Accept the first public enrollment path order and labels. | requires founder review | RF5, RF7, RF9, RF10 | Current order is Individual Horse Owner, Barn Owner / Manager, Service Provider, Trainer. |
| Decide which critical signup fields become required by path. | requires founder decision | RF5, RF7, RF9, RF10 | RF5 lists critical data without adding backend validation or deeper enrollment schemas. |
| Decide whether trainer and service-provider self-signup stays review-gated. | requires founder decision | RF9, RF10 | Existing signup marks trainer, barn owner, and service provider roles pending review. |
| Accept rider, guardian, and staff access as invite-first with a limited-trial fallback. | requires founder review | RF5, RF7, RF18 | RF5 records the fallback but does not enforce limited-trial access caps server-side. |
| Accept leasee invites as owner/trainer controlled with owner oversight preserved. | requires founder review | RF7 | RF5 records the leasee policy only; RF7 must implement the grant and revocation model. |
| Accept admin account-health inventory as RF5 opening evidence only. | requires founder review | RF5 | RF5 does not add new admin analytics, billing intervention mutations, or privacy-sensitive content inspection. |

## Boundaries

- RF5 adds the public web enrollment selector and routes home/login Join actions to it.
- RF5 limits the main selector to four public paths: Individual Horse Owner, Barn Owner / Manager, Service Provider, and Trainer.
- RF5 records account-health/admin surfaces as inventory evidence only.
- RF5 does not add backend enrollment schemas, limited-trial enforcement, leasee grants, billing intervention mutations, provider grants, trainer operating workflows, owner-portal depth, or RF18 UAT acceptance.
- Trainer and service-provider marketplace signup remain review-gated under the existing signup posture.
