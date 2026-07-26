# CGP-002 Validation And Usage Guide

**Prompt ID:** `CGP-002`
**Execution ID:** `CGEXEC-20260726-0001`
**Baseline:** `7975cf2d88540a9b7c9cbfdfa6d6d5b0ec1912c0`

CGP-002 creates the common foundation that Guides `ES-CG-00` through `ES-CG-13` will consume: controlled values, schemas, templates, validators, fixtures, and custody records.

## How Guides Consume The Foundation

Future guide prompts use the schema files for machine-readable companions, templates for consistent drafting, controlled values for status and evidence fields, and validators for deterministic checks.

## Placeholder Handling

Planned guide placeholders are valid as placeholders. They are not complete guides, not adopted, not active, and not implementation controls.

## What CGP-002 Does Not Validate

CGP-002 does not validate guide completeness, product correctness, application implementation, production CI gating, deployment readiness, pilot readiness, AI activation, financial activation, messaging/community activation, moderation activation, archival migration, or enrollment readiness.

## Maintenance

Controlled values should be changed first in `schemas/CODE_GUIDE_CONTROLLED_VALUES.json`, then reflected in reader-facing documentation. Validators should continue to load the JSON source.
