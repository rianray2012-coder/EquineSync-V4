# Vercel Frontend Deployment

EquineSync's frontend deploys as a Create React App from the `frontend` folder.

## Vercel Project Settings

- Git repository: `EquineSync-V4`
- Root Directory: `frontend`
- Framework Preset: Create React App
- Install Command: `npm ci --legacy-peer-deps --include=dev --no-audit --no-fund`
- Build Command: `npm run build`
- Output Directory: `build`

The `frontend/vercel.json` file pins the install/build/output settings and rewrites deep links back to `index.html` so React Router routes like `/admin/portal/login` and `/billing/subscription` load correctly.

## Environment Variables

Set these in Vercel Project Settings before the first production deploy:

- `REACT_APP_BACKEND_URL`
  - Production: `https://api.equine-sync.com`
  - Staging / Preview: `https://staging-api.equine-sync.com`
- `REACT_APP_STRIPE_PUBLISHABLE_KEY`
  - Paste the Stripe publishable key from Stripe. Do not use a secret or restricted key here.

Do not put Stripe secret keys, restricted keys, DocuSign private keys, JWT secrets, or database URLs in the frontend project.

## Staging Backend Settings

When the staging backend is created, set these backend environment values in the backend host:

- `APP_ENV=production`
- `PUBLIC_FRONTEND_URL=https://staging.equine-sync.com`
- `FRONTEND_URL=https://staging.equine-sync.com`
- `CORS_ORIGINS=https://staging.equine-sync.com`

If the staging frontend also uses Vercel preview URLs, add those exact origins to `CORS_ORIGINS` as a comma-separated list:

```env
CORS_ORIGINS=https://staging.equine-sync.com,https://your-preview-url.vercel.app
```

Production should stay separate:

```env
PUBLIC_FRONTEND_URL=https://app.equine-sync.com
FRONTEND_URL=https://app.equine-sync.com
CORS_ORIGINS=https://app.equine-sync.com
```

## Smoke Checks After Deploy

- `/login`
- `/admin/portal/login`
- `/billing/subscription`
- A direct deep link refresh, such as `/horses/example-id`, to confirm Vercel rewrites are working.
