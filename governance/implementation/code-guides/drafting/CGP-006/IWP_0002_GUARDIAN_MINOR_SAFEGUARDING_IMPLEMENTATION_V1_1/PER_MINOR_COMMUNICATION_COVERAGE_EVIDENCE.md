# Per-Minor Communication Coverage Evidence

Status: `IMPLEMENTED_AND_TESTED`

The messaging guard derives minor participants from explicit student profile fields and actual message participants/recipients. For each minor, `guardian_minor_workflow_gate` requires a qualifying active guardian with `COMMUNICATION` authority and, for guarded conversations, the guardian must be present in the participant set.

Evidence:
- `GMS-T-016`: private adult-minor messaging without guardian is denied.
- `GMS-T-017`: missing second-minor guardian coverage is denied.
- `GMS-T-033`: omitted metadata cannot bypass participant-derived coverage.
- `GMS-T-035`: send after last guardian removal is denied.
- `GMS-T-043`: unrelated adult-to-adult message remains allowed.
