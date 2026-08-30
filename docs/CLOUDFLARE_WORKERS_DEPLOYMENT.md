# Cloudflare Workers Deployment

EquineSync currently uses Vercel as the production frontend route. The
Cloudflare Workers project `equinesync-v4` is retained as an infrastructure
path, but it must not rely on Cloudflare automatic monorepo detection.

## Required Workers Build Settings

In Cloudflare Workers Builds for `equinesync-v4`, use:

- Root directory: repository root, blank, or `.`
- Install command: `npm install`
- Deploy command: `npm run deploy`
- Production branch: `release/production`

The root `npm run deploy` command runs the frontend build first, then deploys
the generated `frontend/build` directory through Wrangler.

## Local Verification

From the repository root:

```sh
npm run build
npm run deploy:cloudflare:dry-run
```

Expected result:

- frontend production build succeeds;
- Wrangler reads files from `frontend/build`;
- Wrangler exits successfully in dry-run mode.

## Production Boundary

Do not promote Workers as the production frontend route until Founder approval.
`https://app.equine-sync.com` remains the Vercel-served production frontend
unless this boundary is explicitly changed.
