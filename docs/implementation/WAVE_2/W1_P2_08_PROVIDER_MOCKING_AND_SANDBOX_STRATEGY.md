# W1-P2-08 Provider Mocking and Sandbox Strategy

Ordinary tests use fakes, local fixtures, monkeypatched SDK boundaries, and
loopback services. They never require live Stripe, DocuSign, email, SMS, AI,
calendar, or identity-provider access.

Sandbox tests require explicit authorization, opt-in variables, verified test
mode, allowlisted endpoints, secret-manager injection, cleanup, and evidence.
Production-like credentials are rejected in every non-production mode.
