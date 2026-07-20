from __future__ import annotations

import json
import os
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from jsonschema import Draft202012Validator, FormatChecker

from evidence_capture import sanitize_arguments
from lib.control import IsolationError, PROVIDER_NAMES, ROOT, digest, fixture_data, load_env, provider_register, validate_env


class ControlTests(unittest.TestCase):
    def test_authorized_environment_passes(self):
        self.assertEqual(validate_env(load_env())["status"], "PASS")

    def test_production_database_denied(self):
        env=deepcopy(load_env()); env["MONGO_URL"]="mongodb+srv://prod.example/equinesync"
        with self.assertRaises(IsolationError): validate_env(env)

    def test_provider_credential_denied(self):
        env=deepcopy(load_env()); env["STRIPE_API_KEY"]="present-but-never-recorded"
        with self.assertRaises(IsolationError): validate_env(env)

    def test_fixture_is_synthetic_and_deterministic(self):
        value=fixture_data(); self.assertTrue(value["synthetic_only"]); self.assertEqual(digest(value),digest(fixture_data()))

    def test_provider_register_has_zero_attempts(self):
        env=load_env(); register=provider_register(env)
        self.assertTrue(all(x["attempt_count"]==0 and not x["configured"] for x in register))

    def test_every_provider_name_fails_closed(self):
        for name in PROVIDER_NAMES:
            with self.subTest(name=name):
                env=deepcopy(load_env()); env[name]="REDACTED_PRESENT"
                with self.assertRaises(IsolationError): validate_env(env)

    def test_inherited_provider_name_fails_closed(self):
        with patch.dict(os.environ,{"STRIPE_API_KEY":"REDACTED_PRESENT"}):
            with self.assertRaises(IsolationError): load_env()

    def test_argument_sanitizer_redacts_values_and_local_paths(self):
        values=sanitize_arguments(["--token","secret-value",str(ROOT/"example_command.py"),"PASSWORD=value"])
        self.assertEqual(values[1],"<REDACTED>")
        self.assertEqual(values[2],"stage2a/example_command.py")
        self.assertEqual(values[3],"PASSWORD=<REDACTED>")
        self.assertNotIn("secret-value",values)

    def test_schema_rejects_semantically_empty_record(self):
        schema=json.loads((ROOT/"execution-evidence-schema.json").read_text())
        empty={name:"" for name in schema["required"]}
        self.assertTrue(list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(empty)))

    def test_sandbox_is_exact_port_and_signal_scoped(self):
        profile=(ROOT/"config/loopback-only.sb").read_text()
        self.assertIn('(allow signal (target same-sandbox))',profile)
        self.assertNotIn('localhost:*',profile)
        self.assertIn('localhost:27029',profile)
        self.assertIn('localhost:8019',profile)


if __name__=="__main__": unittest.main()
