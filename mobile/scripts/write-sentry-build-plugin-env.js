const fs = require('fs');
const path = require('path');

const required = ['SENTRY_AUTH_TOKEN'];
const missing = required.filter((key) => !process.env[key]);

if (missing.length > 0) {
  console.log('Sentry build plugin env not written; missing required Sentry upload env.');
  process.exit(0);
}

const values = {
  SENTRY_AUTH_TOKEN: process.env.SENTRY_AUTH_TOKEN,
  SENTRY_ORG: process.env.SENTRY_ORG || 'equine-sync',
  SENTRY_PROJECT: process.env.SENTRY_PROJECT || 'equinesync-mobile',
  SENTRY_URL: process.env.SENTRY_URL || 'https://sentry.io/',
};

const body = Object.entries(values)
  .map(([key, value]) => `${key}=${String(value).replace(/\n/g, '')}`)
  .join('\n') + '\n';

const target = path.join(process.cwd(), '.env.sentry-build-plugin');
fs.writeFileSync(target, body, { mode: 0o600 });
console.log('Sentry build plugin env written for native artifact upload.');
