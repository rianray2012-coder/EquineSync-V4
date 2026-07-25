# Invalid Review Notice

- PIA: `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.1.0`
- Date: `2026-07-21`
- Status: `PERMISSION_CHECK_FAILED`
- Affected runs: initial diagnostic review of `b604bf2a4679457e533cc02af33563f51a88bca2`; attempted verification of `a17b82a3896193e355d77e930e300cfd43565409`

## Controlling conflict

Repository `AGENTS.md` and `governance/founder_orchestrated_review/RUNTIME_PERMISSION_CONTROL.md` require ES-RA-02 review to run read-only with on-request approvals. They prohibit unrestricted / danger-full-access operation and `approval_policy=never` without an express Founder exception containing the required controls. This task's environment is unrestricted with approval policy `never`, and no sufficient exception record was located in the controlling Founder directive or frozen evidence.

## Effect

The first isolated review is preserved under `review_evidence/first_fresh_review/` as nonauthoritative diagnostic evidence. Its four P1 and one P2 observations were remediated, but that run cannot establish valid formal segregated-review assurance because the mandatory pre-spawn permission record and compatible effective mode were absent.

The second reviewer stopped before substantive review and returned `PERMISSION_CHECK_FAILED`. It produced no pass, closure, finding verification, or formal review outputs. Author validation and checksum results do not substitute for fresh ES-RA-02 verification.

## Required next action

Rerun under a new read-only/on-request session with a complete `PASS` pre-spawn permission record and the registered ES-RA-02 identity. An alternative Founder exception must satisfy every field in the runtime control and remain narrower than the present unrestricted environment.

No implementation, migration, deployment, enrollment, production action, custom-agent activation, or F-0001 closure is authorized.
