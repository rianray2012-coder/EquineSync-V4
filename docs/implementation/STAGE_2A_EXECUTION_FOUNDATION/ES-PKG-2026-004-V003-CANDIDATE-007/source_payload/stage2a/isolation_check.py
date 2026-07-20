#!/usr/bin/env python3
"""Static fail-closed isolation check; records names and classes, never values."""
from __future__ import annotations

import json
from lib.control import ambient_name_attestation, load_env, validate_env

if __name__ == "__main__":
    env=load_env(); posture=validate_env(env)
    print(json.dumps({"posture":posture,"ambient_name_attestation":ambient_name_attestation(),"provider_runtime_measurement":"REQUIRES_ACTIVE_PROCESS_BOUND_GUARD_SESSION","provider_attempt_count":"NOT_MEASURED_BY_STATIC_CHECK","production_access_count":0,"production_access_count_basis":"loopback-only","live_data_access_count":0,"live_data_access_count_basis":"synthetic-only owned fixtures"},indent=2,sort_keys=True))
