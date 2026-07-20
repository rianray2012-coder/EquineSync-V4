# Activation Operator Command Log

Activation run: `FORA-ACT-2026-001`

The exact parent canary invocation and environment-variable names are preserved in `canaries/read-only-batch/command.json`. The exact parent prompt is preserved in `canaries/read-only-batch/parent_prompt.txt`; parent events, stderr, final response, permission records, sanitized child provenance, snapshots, status, diff, and score are preserved beside it.

## Material operator commands

Pre-invocation clean-checkout and package-hash confirmation:

```text
git -C /private/tmp/equinesync-controlled-activation.du8NIc/approved-checkout status --porcelain=v1 --untracked-files=all
git -C /private/tmp/equinesync-controlled-activation.du8NIc/approved-checkout rev-parse HEAD
shasum -a 256 /private/tmp/equinesync-controlled-activation.du8NIc/approved-checkout/governance/founder_orchestrated_review/agent_config/packages/EquineSync_Founder_Orchestrated_Review_Agent_Config_Package_V1.0.0.zip
```

Activation harness invocation:

```text
PYTHONDONTWRITEBYTECODE=1 python3 governance/founder_orchestrated_review/activation/scripts/run_post_activation_canaries.py --execution-root /private/tmp/equinesync-controlled-activation.du8NIc/approved-checkout --runtime-root /private/tmp/equinesync-controlled-activation.du8NIc/runtime-FORA-ACT-2026-001
```

Post-failure inactive-state verification:

```text
git diff --quiet 45c3bada313ba1196a52398780d1129255a000ee -- .codex/agents governance/founder_orchestrated_review/agent_config/V1.0.0 governance/founder_orchestrated_review/runtime_remediation
git -C /private/tmp/equinesync-controlled-activation.du8NIc/approved-checkout status --porcelain=v1 --untracked-files=all
git -C /private/tmp/equinesync-controlled-activation.du8NIc/approved-checkout diff --quiet HEAD --
```

No rerun command exists because no retry was performed. No command for a workspace-write canary batch, substantive review, production access, provider write, deployment, pull request, merge, default-branch change, tag, or release was executed.
