from __future__ import annotations

import json
import hashlib
import os
import sys
import tempfile
import unittest
import datetime as dt
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from jsonschema import Draft202012Validator, FormatChecker

from evidence_capture import redact_output, sanitize_arguments, sensitive_output_matches
from lib.control import REPO, IsolationError, PROVIDER_NAMES, ROOT, digest, fixture_data, load_env, provider_register, validate_env
from network_guard import _approved
import network_guard
import orchestrate
from orchestrate import _expected
from semantic_projection import project_outputs
from validate_stage2a_package import KNOWN_SECRET_VALUE as PACKAGE_SECRET_VALUE, locate_repository


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

    def test_provider_register_rejects_supplied_zero_ledger(self):
        with self.assertRaises(TypeError):
            provider_register(load_env(), {"provider_or_external_attempt_count": 0})

    def test_provider_events_are_process_bound_hash_chained_and_attributable(self):
        with tempfile.TemporaryDirectory() as temporary:
            runtime = Path(temporary)
            ledger_path = runtime / "network-guard.json"
            nonce = "unit-test-launch-nonce"
            with patch.object(network_guard, "RUNTIME", runtime), patch.object(network_guard, "LEDGER", ledger_path), patch.dict(os.environ, {"STAGE2A_LAUNCH_NONCE": nonce}):
                value = network_guard._initial()
                ledger_path.write_text(json.dumps(value), encoding="utf-8")
                (runtime / "api.pid").write_text(json.dumps({
                    "pid": os.getpid(), "process_group_id": os.getpgrp(),
                    "launch_nonce_sha256": hashlib.sha256(nonce.encode()).hexdigest(),
                }), encoding="utf-8")
                network_guard.record_provider_capabilities(load_env(), ROOT / "provider-capability-registry.json")
                register, proof = network_guard.derive_provider_register(ROOT / "provider-capability-registry.json")
                self.assertEqual(len(register), 11)
                self.assertTrue(proof["event_chain_valid"])
                self.assertTrue(proof["process_identity_bound"])
                self.assertEqual(proof["unattributed_attempt_count"], 0)
                states = {row["provider_id"]: row["state"] for row in register}
                self.assertEqual(states["stripe"], "SKIPPED_CONTROLLED_STAGE2A_OVERRIDE")
                self.assertEqual(states["resend"], "SKIPPED_NOT_CONFIGURED")
                self.assertEqual(states["sendgrid"], "UNAVAILABLE_INTEGRATION_ABSENT")
                self.assertTrue(all(row["attempted_count"] == 0 for row in register))
                tampered = json.loads(ledger_path.read_text())
                tampered["provider_events"][0]["reason_code"] = "TAMPERED"
                ledger_path.write_text(json.dumps(tampered), encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "event hash mismatch"):
                    network_guard.derive_provider_register(ROOT / "provider-capability-registry.json")

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
        self.assertEqual(sanitize_arguments(["--token-count=3", "authorization_mode=disabled"]), ["--token-count=3", "authorization_mode=disabled"])

    def test_schema_rejects_semantically_empty_record(self):
        schema=json.loads((ROOT/"execution-evidence-schema.json").read_text())
        empty={name:"" for name in schema["required"]}
        self.assertTrue(list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(empty)))

    def test_output_redaction_preserves_required_nonsensitive_meaning(self):
        redacted, replacements = redact_output("operation=fixture-load api_key=do-not-preserve result=pass\n")
        self.assertEqual(replacements, 1)
        self.assertIn("operation=fixture-load", redacted)
        self.assertIn("result=pass", redacted)
        self.assertIn("api_key=<REDACTED>", redacted)
        self.assertEqual(sensitive_output_matches(redacted), [])

    def test_output_redaction_covers_quoted_multiword_and_bearer_values(self):
        probes = [
            ('"password": "correct horse battery staple"\n', '"password": "<REDACTED>"'),
            ('password=correct horse battery staple\n', 'password=<REDACTED>'),
            ('bearer=supersecret\n', 'bearer=<REDACTED>'),
            ('Authorization: Bearer synthetic-credential-value\n', 'Authorization: Bearer <REDACTED>'),
            ('Bearer abc.def.ghi\n', 'Bearer <REDACTED>'),
            ('access_token=synthetic-token result=pass\n', 'access_token=<REDACTED> result=pass'),
            ('client_secret=synthetic-secret operation=ok\n', 'client_secret=<REDACTED> operation=ok'),
        ]
        for raw, expected in probes:
            with self.subTest(raw=raw):
                redacted, replacements = redact_output(raw)
                self.assertGreaterEqual(replacements, 1)
                self.assertIn(expected, redacted)
                self.assertEqual(sensitive_output_matches(redacted), [])

    def test_independent_semantic_projection_rejects_over_redaction(self):
        raw = "operation=login password=hunter2 authentication denied\n"
        redacted, _ = redact_output(raw)
        before = project_outputs(raw, "", sanitized=False)
        after = project_outputs(redacted, "", sanitized=True)
        self.assertNotEqual(before.sha256, after.sha256)
        self.assertNotIn("hunter2", before.serialization)

    def test_semantic_projection_detects_unexpected_placeholder_and_near_misses(self):
        ordinary = "token_count=3 secretary=present bearer_species=horse authorization_mode=disabled\n"
        redacted, count = redact_output(ordinary)
        self.assertEqual((redacted, count), (ordinary, 0))
        projection = project_outputs("operation=<REDACTED>\n", "", sanitized=True)
        self.assertEqual(projection.unexpected_placeholder_count, 1)

    def test_sandbox_is_exact_port_and_signal_scoped(self):
        profile=(ROOT/"config/loopback-only.sb").read_text()
        self.assertIn('(allow signal (target same-sandbox))',profile)
        self.assertNotIn('localhost:*',profile)
        self.assertIn('localhost:27029',profile)
        self.assertIn('localhost:8019',profile)

    def test_validator_root_resolution_is_working_directory_independent(self):
        self.assertEqual(locate_repository(ROOT / "validate_stage2a_package.py"), REPO)
        packaged = REPO / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION/ES-PKG-2026-004-V003/validate_stage2a_package.py"
        self.assertEqual(locate_repository(packaged), REPO)
        self.assertIsNone(locate_repository(Path("/private/tmp/detached-candidate/validate_stage2a_package.py")))

    def test_packaged_secret_scanner_distinguishes_rules_from_values(self):
        detector_source = r"whsec_[A-Za-z0-9_-]+|AKIA[A-Z0-9]{12,}"
        self.assertIsNone(PACKAGE_SECRET_VALUE.search(detector_source))
        stripe_probe = "wh" + "sec_" + "example0123456789"
        aws_probe = "AK" + "IA" + "1234567890ABCD"
        self.assertIsNotNone(PACKAGE_SECRET_VALUE.search(stripe_probe))
        self.assertIsNotNone(PACKAGE_SECRET_VALUE.search(aws_probe))

    def test_application_network_guard_allows_only_controlled_endpoints(self):
        self.assertTrue(_approved(("127.0.0.1", 27029)))
        self.assertTrue(_approved(("127.0.0.1", 8019)))
        self.assertFalse(_approved(("127.0.0.1", 9)))
        self.assertFalse(_approved(("192.0.2.1", 443)))

    def test_process_identity_fails_closed_on_command_or_group_conflict(self):
        observed = "python -m uvicorn controlled"
        record = {
            "owner": "ES-PKG-2026-004-V003", "kind": "api", "pid": 42,
            "process_group_id": 42, "parent_pid": 7,
            "parent_pid_policy": "CREATION_PARENT_OR_INIT_REPARENT_ONLY",
            "executable_path": "/controlled/python", "working_directory": "/controlled/work",
            "controlled_port": 8019, "command_line_sha256": hashlib.sha256(observed.encode()).hexdigest(),
            "launch_nonce_sha256": "a" * 64,
            "observed_command_line": observed, "command_display": observed,
            "identity_recorded_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
        files = {"cwd": "/controlled/work", "txt_paths": {"/controlled/python"}}
        identity = {"parent_pid": 7, "process_group_id": 42, "command_line": observed, "observed_executable": "/controlled/python", "launch_nonce_sha256": "a" * 64}
        with patch("orchestrate._process_files", return_value=files), patch("orchestrate._ps_identity", return_value=identity), patch("orchestrate._process_exists", return_value=True):
            self.assertTrue(_expected(record, "api"))
            conflicted = deepcopy(record); conflicted["process_group_id"] = 43
            self.assertFalse(_expected(conflicted, "api"))
            conflicted = deepcopy(record); conflicted["command_line_sha256"] = "0" * 64
            self.assertFalse(_expected(conflicted, "api"))
            conflicted = deepcopy(record); conflicted["launch_nonce_sha256"] = "0" * 64
            self.assertFalse(_expected(conflicted, "api"))
            conflicted = deepcopy(record); conflicted["controlled_port"] = 9999
            self.assertFalse(_expected(conflicted, "api"))
            conflicted = deepcopy(record); conflicted["working_directory"] = "/controlled"
            self.assertFalse(_expected(conflicted, "api"))

    def test_process_identity_timestamp_and_reparenting_fail_closed(self):
        now = dt.datetime.now(dt.timezone.utc)
        self.assertTrue(orchestrate._identity_timestamp_valid(now.isoformat(), now))
        self.assertFalse(orchestrate._identity_timestamp_valid(now.replace(tzinfo=None).isoformat(), now))
        self.assertFalse(orchestrate._identity_timestamp_valid((now + dt.timedelta(minutes=1)).isoformat(), now))
        observed = "python -m uvicorn controlled"
        record = {
            "kind": "api", "pid": 42, "process_group_id": 42, "parent_pid": 7,
            "executable_path": "/controlled/python", "working_directory": "/controlled/work",
            "controlled_port": 8019, "command_line_sha256": hashlib.sha256(observed.encode()).hexdigest(),
            "launch_nonce_sha256": "a" * 64, "identity_recorded_utc": now.isoformat(),
        }
        files = {"cwd": "/controlled/work", "txt_paths": {"/controlled/python"}}
        identity = {"parent_pid": 1, "process_group_id": 42, "command_line": observed, "observed_executable": "/controlled/python", "launch_nonce_sha256": "a" * 64}
        with patch("orchestrate._process_files", return_value=files), patch("orchestrate._ps_identity", return_value=identity):
            with patch("orchestrate._process_exists", return_value=True):
                self.assertFalse(_expected(record, "api"))
            with patch("orchestrate._process_exists", return_value=False):
                self.assertTrue(_expected(record, "api"))

    def test_status_fails_closed_when_listener_pid_conflicts(self):
        mongo = {"pid": 42}; api = {"pid": 43}
        with patch("orchestrate._read_record", side_effect=[mongo, api]), patch("orchestrate._listener_pid", side_effect=[9002, 9001]), patch("orchestrate._alive", return_value=True), patch("orchestrate._port_open", return_value=True):
            result = orchestrate.status()
        self.assertFalse(result["mongo_alive"])
        self.assertFalse(result["api_alive"])
        self.assertEqual(result["mongo_foreign_listener_pid"], 9002)
        self.assertEqual(result["api_foreign_listener_pid"], 9001)

    def test_closed_port_skips_process_identity_probe(self):
        with patch("orchestrate._port_open", return_value=False), patch("orchestrate.subprocess.run") as run:
            self.assertIsNone(orchestrate._listener_pid(8019))
            run.assert_not_called()

    def test_listener_identity_probe_timeout_fails_closed(self):
        with patch("orchestrate._port_open", return_value=True), patch(
            "orchestrate.subprocess.run", side_effect=orchestrate.subprocess.TimeoutExpired("lsof", 5)
        ):
            with self.assertRaisesRegex(RuntimeError, "listener identity probe timed out"):
                orchestrate._listener_pid(8019)

    def test_listener_identity_probe_can_scope_to_expected_pid(self):
        completed = orchestrate.subprocess.CompletedProcess([], 0, stdout="42\n", stderr="")
        with patch("orchestrate._port_open", return_value=True), patch(
            "orchestrate.subprocess.run", return_value=completed
        ) as run:
            self.assertEqual(orchestrate._listener_pid(8019, 42), 42)
        command = run.call_args.args[0]
        self.assertIn("-a", command)
        self.assertEqual(command[command.index("-p") + 1], "42")


if __name__=="__main__": unittest.main()
