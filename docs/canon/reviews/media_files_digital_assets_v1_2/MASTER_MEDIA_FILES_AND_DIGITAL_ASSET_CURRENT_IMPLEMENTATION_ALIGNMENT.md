# Master Media, Files, and Digital Asset Current Implementation Alignment

## Classification

These are nonblocking implementation-alignment observations. They are not evidence that the candidate is defective, not production findings, and not authorization to change code or data.

| Observation | Repository evidence | Future governed action |
| --- | --- | --- |
| Media records use `public_url` as a persisted field | `backend/storage.py:58-87` | Introduce canonical asset references and permission-safe delivery projections |
| Storage provider exposes a public-base URL contract | `backend/storage.py:138-182` | Reclassify public delivery as an explicit publication/CDN projection |
| Provider initialization can fall back to a local stub | `backend/storage.py:194-215` | Add environment-aware fail-closed production startup policy |
| Scan upload records client-declared MIME/size and a URL after client transfer | `backend/routes/backlog.py:1908-1955`, `frontend/src/pages/MobileReadiness.jsx:180-205` | Add server-side finalization, exact-byte verification, quarantine, scan, and commit |
| Health documents accept and directly open raw URLs | `frontend/src/pages/HealthDocuments.jsx:9-15`, `frontend/src/pages/HealthDocuments.jsx:180-184` | Classify external references; add validation, controlled projections, and compatibility migration |
| Passport and horse lists project raw photo/document URLs | `backend/routes/equine_passport.py:686-702`, `backend/routes/equine_passport.py:773-781`, `frontend/src/pages/Horses.jsx:80-88` | Replace with permission-safe canonical asset envelopes through a separately authorized migration |

## Required future migration posture

1. Inventory actual fields, collections, routes, data classes, environments, and public exposure.
2. Stop creation of new legacy URL drift only after compatibility behavior is designed and authorized.
3. Add canonical asset and version records without deleting legacy values.
4. Classify external references without automatically fetching customer or production content.
5. Reconcile barn, horse, actor, provider, consent, rights, retention, and access deltas.
6. Introduce read adapters and permission-safe projections.
7. Validate synthetic and expressly approved non-production fixtures.
8. Migrate only under separate environment-specific Founder authority.
9. Preserve rollback eligibility and exception ledgers.
10. Deprecate raw fields only after lineage, access, export, and deletion behavior is proven.

## Current restrictions

No runtime correction, remote fetch, customer-data inspection, migration, provider activation, schema change, or production action is authorized by this report.
