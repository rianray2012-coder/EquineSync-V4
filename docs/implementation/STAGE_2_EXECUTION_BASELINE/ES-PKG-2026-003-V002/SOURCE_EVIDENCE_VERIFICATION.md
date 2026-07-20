# Source Evidence Verification

- Result: `PASS`
- Registered rows verified: `142`
- Immutable Git rows: `111`
- Nested candidate rows: `15`
- Predecessor: `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Nested Stage 1: `78f433ac5619861fd99b73a725507292c69433f7215c22d076ea72df888b1d33`
- Nested internal-assurance candidate: `e46fc2cc70ae994061937e5e90cb502d9453d197bb0f3322f433db1c3bfffd92`
- Nested MIAP baseline: `5e494c785feb6b8a2dad9d8289fc1ac5af254223bd88cf439611773a4082314f`

Every immutable Git row was checked against the file SHA-256 and pinned Git blob. Every candidate row was read from the actual nested candidate archive. The complete outer-to-inner archive chain was opened and hashed. This validates custody and source identity; it does not promote candidate authority or prove implementation/runtime behavior.
