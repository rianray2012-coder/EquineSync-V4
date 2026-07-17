# W1-RF01 Authentication Flow Map

## Public Registration

`/auth/register` forces `horse_owner`; `/auth/signup` accepts five marketplace roles. Both create `users`, hash passwords with bcrypt, issue verification tokens, and may issue access/refresh tokens when verification enforcement is disabled.

## Login and Session

Login applies endpoint rate limiting, optional account lockout, bcrypt verification, suspension and optional email-verification checks, then issues a four-hour JWT and 30-day hashed refresh token. Product requests decode JWT but re-read `users`, making the user document authoritative for role, barn, suspension, and verification.

## Refresh and Logout

Refresh validates a hashed token, checks the current user, revokes the old token, and issues a replacement. Logout revokes the submitted refresh token; logout-all revokes all refresh tokens. Existing access JWTs remain valid until expiry unless account state blocks them.

## Recovery and Verification

Forgot-password is non-enumerating. Reset and verification tokens are random, hashed, expiring, and single-use. Password reset revokes refresh tokens.

## Invite Acceptance

Invite tokens are hashed and expiring. Existing users authenticate with their password; new users are created. An account-membership row is added, but the existing user's legacy `role` and `barn_id` remain unchanged.

