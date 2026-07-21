# Phase 1 Data Classification and External Processing Standard

Every input is classified before packet assembly as `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `PRIVILEGED_OR_LEGALLY_SENSITIVE`, `PERSONAL_DATA`, `SECURITY_SENSITIVE`, or `PROHIBITED_FROM_EXTERNAL_PROCESSING`.

Phase 1 permits no external-provider request, provider-hosted tracing, production credential, production data, customer data, or personal data in a synthetic pilot. Pilot A must use disposable synthetic content. Privileged or legally sensitive content is prohibited from Pilot A.

If redaction is authorized, retain and hash the authoritative source, create a separately hashed redacted derivative, and record a transformation manifest listing parent evidence ID, method, redactions, operator, timestamp, and validation. A derivative never replaces the authoritative source.

Secrets, tokens, credentials, private keys, authentication cookies, and live connection strings are forbidden in packets and evidence. Synthetic secret patterns must be conspicuously marked, nonfunctional, and allowlisted only for the test that requires them.
