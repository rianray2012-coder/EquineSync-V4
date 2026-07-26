# CGP-003 Search Coverage Report

## Reproducible Search Method

1. Enumerated tracked files with `git ls-files` (`3961` tracked files).
2. Counted top-level source families and inspected canonical directories under `docs/canon`, `docs/governance_v1_0`, `governance/pia`, `docs/implementation`, `.github`, `backend`, `frontend`, `tests`, and `test_reports`.
3. Searched filenames and text for PIA, atlas, Founder, approval, adoption, disposition, governance, architecture, ADR, review, validation, manifest, checksum, receipt, evidence, source, supersession, implementation, security, privacy, safeguarding, external-standard, provider, CI, and test terms.
4. Deduplicated source records by stable repository path and class.
5. Generated file SHA-256 checksums and deterministic directory aggregate checksums from tracked bytes.

## Excluded Classes

- `.git`, generated caches, `__pycache__`, virtual environments, dependency folders, image binaries, ZIP/DOCX/PDF internals, and build outputs were not treated as individually parsed governing sources.
- ZIP, DOCX, PDF, image, and other binary files may be represented by checksum or directory/package rows where they are repository-tracked source evidence.
- Current application code and tests were inventoried as implementation/test evidence, not as governing authority.

## Search Result

The process produced `2620` source records and `14176` guide mappings. All 14 guide placeholders have initial source coverage assessments.
