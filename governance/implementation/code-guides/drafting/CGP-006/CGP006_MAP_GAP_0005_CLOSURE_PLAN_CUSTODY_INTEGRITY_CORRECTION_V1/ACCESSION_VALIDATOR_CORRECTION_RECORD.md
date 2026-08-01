# Accession Validator Correction Record

The accession validator was hardened to:

- prove the approved ZIP from the committed Git object using `git ls-files`, `git cat-file`, and `git show`;
- reject local ignored ZIP substitution;
- verify ZIP SHA-256, byte length, inventory, integrity, internal checksums, and approved-source Git objects;
- verify controlling Markdown exact bytes from Git;
- require boundary tokens in explicit authoritative governance files;
- reject validator, test, manifest, checksum, filename, and diagnostic-output token self-satisfaction;
- reject prohibited future-evidence placeholders and unexpected approved-source files; and
- enforce correction-scoped authorized paths.

The validator still preserves the original non-authority and open-gap controls.
