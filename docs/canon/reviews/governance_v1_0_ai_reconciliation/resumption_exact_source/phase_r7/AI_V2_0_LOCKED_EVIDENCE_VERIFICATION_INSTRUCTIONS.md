# AI V2.0 Locked Evidence Verification Instructions

1. Verify the exact source SHA-256 is `414e912c9caec58573558a5fa3e7519db59506b7a903879db3af33e840c0d1e8`.
2. Validate the DOCX with `unzip -t` without resaving it.
3. Verify every file against the replacement package manifest.
4. Confirm the Founder Decision Register contains AI-FD01 through AI-FD12 exactly once.
5. Confirm the Requirement Index contains 112 unique IDs and the traceability matrix reports zero orphans and zero unmapped decisions.
6. Confirm the adoption-record SHA-256 recorded by the lock record.
7. Confirm P0 and open P1 are zero and lock-blocking P2 is zero.
8. Confirm implementation, runtime, provider, customer-data transfer, training, production, public-claim, and public-launch authority are false.
9. Treat any checksum drift as a lock failure requiring founder review; never repair locked bytes in place.
