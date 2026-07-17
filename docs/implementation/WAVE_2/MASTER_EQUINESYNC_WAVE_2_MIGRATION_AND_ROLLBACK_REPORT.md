# Master EquineSync Wave 2 Migration and Rollback Report

Gate: `WAVE_2_ADDITIVE_SCHEMA_AND_MIGRATION_GATE_PASSED`

The rehearsal ran only against a local database named for Wave 2. It added canonical IDs, revisions, and provenance while tracking exact changed fields. Results: one horse and four facility locations converged; replay changed zero; rollback removed only Wave 2 additions; forward recovery reproduced the same result. Legacy before, rollback, and recovery digests matched. No ambiguous rows were guessed and no production endpoint or credential was used.

Evidence: `outputs/wave2_core_convergence_rehearsal.json`.

