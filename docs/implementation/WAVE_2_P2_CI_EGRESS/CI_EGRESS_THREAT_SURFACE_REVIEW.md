# CI Egress Threat Surface Review

| Surface | Risk | Control |
| --- | --- | --- |
| Inherited provider credentials | accidental live provider contact | expanded credential scrub list and startup rejection |
| Repository secrets in ordinary CI | secret-backed network activity | workflow validator rejects `${{ secrets.* }}` |
| Sandbox opt-in drift | ordinary tests become integration tests | validator rejects truthy sandbox opt-in |
| Python TCP clients | outbound provider/API calls | process-wide loopback-only connect guard |
| DNS resolution | pre-connect DNS leakage | process-wide non-loopback `getaddrinfo` denial |
| UDP clients | direct `sendto` bypass | process-wide non-loopback `sendto` denial |
| Child processes | guard bypass by subprocess | `sitecustomize` inherited through `PYTHONPATH` |
| Shell network tools | curl/wget/deploy/publish bypass | static command denylist requiring governed annotation |
| Third-party actions | opaque bootstrap/runtime behavior | action allowlist limited to checkout and setup-python |
| Linux test process | language-level guard bypass | isolated `unshare --net` test step with no default route |
| Production configuration inheritance | test/live environment confusion | `APP_ENV=test`, explicit scrubbed variables, provider guard |

Webhook routes are inbound surfaces and were not activated or modified. Deployment helpers and provider smoke scripts remain outside ordinary CI and received no authority.

