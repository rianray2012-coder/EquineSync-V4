# Global Governance V1.0 Historical Manifest Classification

## Decision

Existing `SHA256SUMS`, package manifests, adoption manifests, and lock manifests are preserved exactly as historical lifecycle evidence.

They fall into two classes:

1. **Self-contained evidence manifests.** Their referenced bytes are preserved in the same directory or evidence archive and remain independently verifiable.
2. **Point-in-time cross-repository manifests.** They recorded mutable registries, implementation records, outputs, or application evidence as those files existed during an earlier lifecycle event. Later governed changes to those targets do not rewrite the historical manifest and do not imply post-lock drift in the immutable canon source named by the corresponding lock certificate.

## Current baseline authority

`GLOBAL_GOVERNANCE_V1_0_BASELINE_MANIFEST.json` is the sole aggregate current-state manifest for the Global Governance V1.0 GitHub baseline. It hashes every in-scope file from the exact baseline commit.

This classification does not:

- alter or regenerate historical checksum evidence;
- make a failed historical checksum appear to pass;
- erase missing historical external-output references;
- change any adopted or locked source byte;
- grant implementation or operational authority; or
- convert the Implementation Atlas from its recorded `ADOPTED_PLANNING_ATLAS_NOT_LOCKED` state.

Historical cross-repository differences remain retained provenance observations. The global lock depends on the new complete current-state manifest, exact lock-certificate source checks, and clean-clone reproduction.

