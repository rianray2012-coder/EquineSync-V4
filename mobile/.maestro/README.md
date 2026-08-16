# EquineSync Phase 3 Maestro Harness

This directory contains local/EAS mobile end-to-end flows for the React Native / Expo native app.

## Scope

- Launch the installed native app by `com.equinesync.app`.
- Sign in through the normal product login screen.
- Confirm the backend-authoritative role home for each approved pilot role.
- Confirm at least one denied role home remains unavailable.

The flows do not store passwords. Provide the local UAT role password at runtime.

## Local Run

1. Start the native-dev backend.
2. Install/open the app on an iOS Simulator or Android emulator.
3. Run:

```sh
EQUINESYNC_UAT_PASSWORD="..." ./scripts/run-maestro-role-matrix.sh
```

For Android, use the Android-specific flow:

```sh
MAESTRO_PLATFORM=android MAESTRO_DEVICE=emulator-5554 MAESTRO_FLOW="$PWD/.maestro/role-home-android.yml" EQUINESYNC_UAT_PASSWORD="..." ./scripts/run-maestro-role-matrix.sh
```

To run one role:

```sh
ROLE_FILTER=horse-owner EQUINESYNC_UAT_PASSWORD="..." ./scripts/run-maestro-role-matrix.sh
```

## Privacy-Denial Probe

The unrelated-facility and unrelated-horse checks are backend authorization checks. Run them separately so the removed local-only evidence hook does not need to return to the app:

```sh
PHASE3_UAT_PASSWORD="..." ../backend/.venv/bin/python ../backend/scripts/phase3_privacy_denial_probe.py
```

## Boundary

This is internal native-dev evidence. It is not a production, store-submission, provider-live, billing-live, or public-launch claim.
