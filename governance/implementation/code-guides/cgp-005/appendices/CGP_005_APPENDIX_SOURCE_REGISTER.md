# CGP-005 Appendix Source Register

Package ID: `ES-CGP-005-TECHNICAL-AUDIT-APPENDIX-V1.0.0`
Repository: `rianray2012-coder/EquineSync-V4`
Base branch: `integrate-emergent-final-zip`
Reviewed head: `4afe3ccd84d9f8be1bc5c79bb27068676d993a70`

## Source-Treatment Determination

`CGP005_APPENDIX_REQUIRED`

The Technical Audit Founder decisions are recorded as governing constraints for CGP-006 input refresh. They are not inserted into the original CGP-005 selected source set, and they do not replace any CGP-005 source-freeze artifact.

## Primary Decision Sources

| Source | Role | SHA-256 |
| --- | --- | --- |
| `governance/implementation/technical-audit/founder-decisions/ES-TA-FD-001-008-V1.1.0/TECHNICAL_AUDIT_FOUNDER_DECISION_PACKET_V1_1_0.md` | Controlling decision language for ES-TA-FD-001 through ES-TA-FD-008 | `e39e2ab714cfe6f62b0df2cf1f7fba1b2c416abef52106c58a285ffd06a405e2` |
| `governance/implementation/technical-audit/founder-decisions/ES-TA-FD-001-008-V1.1.0/FOUNDER_APPROVAL_RECORD_ES_TA_FD_001_008.md` | Founder approval record and exact approval language | `6dbe5b61f6412cb5762e98b505fa0aed75f1694579edd111b0c00e090f2366fc` |
| `governance/implementation/technical-audit/founder-decisions/ES-TA-FD-001-008-V1.1.0/TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER_V1_1_0.csv` | Machine-readable decision effects and pilot-gate effects | `237ec73b165d16d8dd516851e17b4244a724a8dcf17640b1719a1da76e28a002` |
| `governance/implementation/technical-audit/founder-decisions/ES-TA-FD-001-008-V1.1.0/DECISION_TO_FINDING_CROSSWALK_V1_1_0.csv` | Mapping from decisions to technical audit findings and remediation evidence | `cdf570f949efee5f9fe3bc88c4af8435138aeee76bb082466d10b3348e7fb58d` |
| `governance/implementation/technical-audit/founder-decisions/ES-TA-FD-001-008-V1.1.0/PROPOSED_REMEDIATION_SEQUENCE_V1_1_0.md` | Remediation sequence context and sequencing implications | `da05ab1260471e06fb6df9fa9e097cd73d34743c6955ce26b328f39492ddc92e` |

## Custody And Verification Sources

| Source | Role | SHA-256 |
| --- | --- | --- |
| `governance/implementation/technical-audit/founder-decisions/ES-TA-FD-001-008-V1.1.0/FOUNDER_DECISION_PACKAGE_SHA256SUMS.txt` | Technical Audit Founder decision package checksum ledger | `6f3302a7159e767be8ef6c68fd396749365e67e63f266d0b92e03a0831772d23` |
| `governance/implementation/code-guides/packages/CGP_005_SHA256SUMS.txt` | CGP-005 package checksum ledger | `e32589f37eee638fd72f0c8ca9efd214bbf06f364643667a79c9dbe411bc5685` |
| `governance/implementation/code-guides/initiation/CGP-006/CGP_006_CHECKSUMS.sha256` | CGP-006 initiation checksum ledger | `ae7a1c72c92d4f8ed7cfacf5802ec24cce560adc49195345308928fcbb227ac2` |
| `governance/implementation/document-authority-classification/INITIAL_CLASSIFICATION_REPORT.md` from PR `#29` | Classification basis identifying PR `#23` as requiring a CGP-005 appendix | PR `#29` ledger hash: `825fe4b8c02adbcda90774c35da1a9e80e62faca5c5db3fda9b01dc3d70e3659` |

## Repository PR Evidence

| PR | Status at review | Treatment |
| --- | --- | --- |
| `#23` | `MERGED`; merge commit `3eb6825091241709f255b8ccf296987fa9b20724` | Source of Technical Audit Founder decisions. Added Technical Audit files only. |
| `#29` | `OPEN`; draft; merge state `CLEAN`; checks successful | Document Authority Classification Framework reviewed as the classification basis. Not treated as merged into default. |
| `#30` | `OPEN`; draft; not merged into reviewed default head | Observed governance drift for CGP-006 classification. Not used as a controlling source for this appendix. |

## Verification Results

| Check | Result |
| --- | --- |
| CGP-005 ledger verification | `PASS` |
| CGP-006 initiation ledger verification | `PASS` |
| Technical Audit Founder decision package ledger verification | `PASS` |
| Default branch expected head | `PASS` |
| PR `#23` merged-state verification | `PASS` |
| PR `#29` draft/open-state verification | `PASS` |
| Existing CGP-005 source bytes unchanged | `PASS` |

## Source Authority Boundary

The decision package files remain outside the original CGP-005 source-freeze membership. This appendix records their governing-constraint effect for later CGP-006 drafting. No source-file hash, source-set membership, or controlling artifact in the original CGP-005 freeze is changed by this package.
