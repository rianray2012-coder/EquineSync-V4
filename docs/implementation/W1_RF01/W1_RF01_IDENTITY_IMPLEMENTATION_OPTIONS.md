# W1-RF01 Identity Implementation Options

## Option A - Existing-Foundation Security Hardening

Close pending-review role elevation, unify auth authority, make refresh rotation atomic, strengthen session/recovery evidence, and add focused tests. No provider replacement and no canonical schema migration. Lowest immediate risk and highest urgency.

## Option B - Canonical Identity Convergence

Add canonical account/actor mappings, active membership context, relationship-aware authorization, provenance, and access-delta evidence. Additive schema and controlled migration likely required. Valuable, but unsafe before Option A.

## Option C - External Identity-Provider Transition

Use a managed provider for authentication while EquineSync retains canonical actors, relationships, permissions, and audit truth. Highest dependency and migration burden; provider selection and activation remain unauthorized.

## Option D - Staged Hybrid

Authorize Option A as a narrow RF, then Option B through separate schema/migration gates, while deferring Option C until assurance requirements and provider-neutral research are approved.

**Recommendation:** Option D, beginning only with the bounded Option A RF.

