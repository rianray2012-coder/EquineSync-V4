# Runtime Remediation Baseline

Captured: `2026-07-20T03:58:47Z`

## Repository trust

- Repository: `https://github.com/rianray2012-coder/EquineSync-V4.git`
- Branch: `agent/install-founder-review-agents-v1.0.0`
- Starting and remote branch-tip commit: `e93d3acc65a45835d3f3c63473f5dd98e1d1bcf5`
- Default branch: `integrate-emergent-final-zip` at `acb518ea5a160820e64681ff95a16b010fe1156c`
- Starting commit in default branch: no
- Pull requests for the authorized branch: `0`
- Initial Git status and diff: clean

The local remote-tracking ref was initially stale at `45c3bada313ba1196a52398780d1129255a000ee`. `git ls-remote` established that GitHub remained at the reported `e93d3acc...` tip, and an explicit refspec refresh brought the local tracking ref current before evidence capture.

## Identity and package

- Founder-approved review-package commit: `45c3bada313ba1196a52398780d1129255a000ee`
- Technical installation evidence: `860da19970604197117b94a2ef7f23dba2dca694`
- Package ZIP SHA-256: `604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3`
- Prior activation evidence: `34/34` manifest and `35/35` checksum entries, `PASS`
- Installed-system validator in a disposable checkout: `16/16 PASS`

## Runtime and configuration

- Codex CLI: `0.144.6`
- OS: macOS `26.5.2` build `25F84`, arm64
- Repository config hash: `b29e973bbba4a05769f443bb6bb4e34a52513e2dc27aaa21373712dceaed033c`
- User config hash: `5fa449041f0c1d023236d3b6706cfb95f990794d06ced5ec50f63e09a2d817e9`
- Prior isolated runtime config hash: `29d57a7ee4bd7e5eed45f9e8694d0b7127e3206e1d42256dcc30366f15c1328b`

The normal user profile enables multiple plugins and MCP servers, including `cloudflare-api`. The remediation canary will not use or modify that profile. It will use a new disposable profile with explicit project trust, no configured MCP servers, disabled plugin/app/remote-plugin features, and a minimal environment.

No secret values, credential fingerprints, tokens, cookies, or private keys are recorded. Environment and connector evidence records names and status only.
