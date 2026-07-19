# EquineSync Founder-Orchestrated Review Agent Configuration Package

**Package version:** 1.0.0  
**Controlling framework:** EquineSync Founder-Orchestrated Review Agent Framework V1.3  
**Framework status:** Founder approved  
**Founder and final authority:** Rian Ray

## Purpose

This package converts the founder-approved framework into a Codex-ready operating kit for eight segregated agents:

1. Drafting Agent
2. Segregated Review Agent
3. Adversarial Challenge Agent
4. Machine Validation Agent
5. Evidence Custodian
6. Domain Reviewer
7. Synthetic Golden-Path Specification Agent
8. Executable Golden-Path Reproduction Controller

The package includes:

- eight standalone agent prompts;
- a shared operating contract;
- JSON Schemas for review records and evidence;
- reusable Markdown, CSV, and JSON templates;
- Codex orchestration, handoff, and state-machine directives;
- package validation and review-cycle initialization scripts; and
- a machine-generated package manifest and SHA-256 register.

## Controlling rule

Agents may draft, inspect, challenge, validate, preserve evidence, specify tests, and execute authorized tests. Agents may not approve, adopt, lock, waive, accept risk, authorize production, or impersonate Founder authority.

## Recommended Codex loading order

1. `orchestration/CODEX_ORCHESTRATION_DIRECTIVE.md`
2. `shared/COMMON_AGENT_OPERATING_CONTRACT.md`
3. The assigned file in `prompts/`
4. The review authorization and frozen package
5. Applicable schemas and templates

## Quick start

Create a review-cycle workspace:

```bash
python3 scripts/create_review_cycle.py --cycle-id ES-REV-YYYY-NNN --output /path/to/reviews
```

Validate this configuration package:

```bash
python3 scripts/validate_package.py
```

## Independence limitation

Separate agents and sessions create procedural segregation, not external professional independence. Shared model families may retain correlated blind spots. High-risk gates should use method diversity, independent reruns, a different model where available, or qualified human review.
