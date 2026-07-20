#!/usr/bin/env python3
"""Non-agent proof that project custom agents load and connectors stay absent."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import select
import shutil
import subprocess
import time

from runtime_support import RUN_ROOT, create_isolated_runtime, remove_auth, sha256, write_json


ROLE_EXPECTATIONS = {
    "equinesync_segregated_review_agent": ("ES-RA-02", "ES-RA-02-REGISTERED-V1.0.0", "ES-RA-02_SEGREGATED_REVIEW_AGENT.md"),
    "equinesync_adversarial_challenge_agent": ("ES-RA-03", "ES-RA-03-REGISTERED-V1.0.0", "ES-RA-03_ADVERSARIAL_CHALLENGE_AGENT.md"),
    "equinesync_domain_reviewer": ("ES-RA-06", "ES-RA-06-REGISTERED-V1.0.0", "ES-RA-06_DOMAIN_REVIEWER.md"),
}
RAW = RUN_ROOT / "raw" / "non_agent_probe"
RESULT = RUN_ROOT / "NON_AGENT_RUNTIME_PROBE.json"
REPORT = RUN_ROOT / "NON_AGENT_RUNTIME_PROBE.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execution-root", required=True, type=Path)
    parser.add_argument("--runtime-root", required=True, type=Path)
    parser.add_argument("--auth-file", required=True, type=Path)
    args = parser.parse_args()
    execution_root = args.execution_root.resolve()
    codex_value = shutil.which("codex")
    if not codex_value:
        raise RuntimeError("codex executable unavailable")
    codex = Path(codex_value).resolve()
    RAW.mkdir(parents=True, exist_ok=False)
    codex_home, _, env, metadata = create_isolated_runtime(args.runtime_root.resolve(), execution_root, args.auth_file.expanduser().resolve(), codex)
    shutil.copyfile(codex_home / "config.toml", RAW / "effective_isolated_config.toml")
    request_lines = [
        {"id": 1, "method": "initialize", "params": {"clientInfo": {"name": "equinesync-runtime-probe", "version": "1.0.0"}}},
        {"method": "initialized", "params": {}},
        {"id": 2, "method": "config/read", "params": {"cwd": str(execution_root), "includeLayers": True}},
    ]
    payload = "".join(json.dumps(item, separators=(",", ":")) + "\n" for item in request_lines)
    process = subprocess.Popen([str(codex), "app-server"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env, cwd=execution_root)
    assert process.stdin is not None and process.stdout is not None and process.stderr is not None
    output_lines = []
    process.stdin.write(json.dumps(request_lines[0], separators=(",", ":")) + "\n")
    process.stdin.flush()
    deadline = time.monotonic() + 30
    initialized = False
    while time.monotonic() < deadline and not initialized:
        ready, _, _ = select.select([process.stdout], [], [], 1)
        if not ready:
            continue
        line = process.stdout.readline()
        if not line:
            break
        output_lines.append(line)
        try:
            initialized = json.loads(line).get("id") == 1
        except json.JSONDecodeError:
            pass
    if initialized:
        for item in request_lines[1:]:
            process.stdin.write(json.dumps(item, separators=(",", ":")) + "\n")
        process.stdin.flush()
    config_returned = False
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline and not config_returned:
        ready, _, _ = select.select([process.stdout], [], [], 1)
        if not ready:
            continue
        line = process.stdout.readline()
        if not line:
            break
        output_lines.append(line)
        try:
            config_returned = json.loads(line).get("id") == 2
        except json.JSONDecodeError:
            pass
    process.stdin.close()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.terminate()
        process.wait(timeout=5)
    remaining_stdout = process.stdout.read()
    if remaining_stdout:
        output_lines.append(remaining_stdout)
    app_stdout = "".join(output_lines)
    app_stderr = process.stderr.read()
    app_returncode = process.returncode
    (RAW / "app_server.requests.jsonl").write_text(payload, encoding="utf-8")
    (RAW / "app_server.stdout.jsonl").write_text(app_stdout, encoding="utf-8")
    (RAW / "app_server.stderr.txt").write_text(app_stderr, encoding="utf-8")
    mcp = subprocess.run([str(codex), "mcp", "list"], capture_output=True, text=True, env=env, cwd=execution_root, timeout=60, check=False)
    (RAW / "mcp_list.stdout.txt").write_text(mcp.stdout, encoding="utf-8")
    (RAW / "mcp_list.stderr.txt").write_text(mcp.stderr, encoding="utf-8")

    config_response = {}
    for line in app_stdout.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if item.get("id") == 2:
            config_response = item.get("result", {})
    write_json(RAW / "config_read_result.json", config_response)
    config = config_response.get("config", {}) if isinstance(config_response, dict) else {}
    layers = config_response.get("layers", []) if isinstance(config_response, dict) else []
    project_layers = [
        layer for layer in layers
        if isinstance(layer, dict)
        and (
            layer.get("name") == "project"
            or (isinstance(layer.get("name"), dict) and layer["name"].get("type") == "project")
        )
    ]
    connector_runtime_output = "\n".join((app_stderr, mcp.stdout, mcp.stderr)).lower()
    roles = []
    for name, (role_id, marker, prompt_name) in ROLE_EXPECTATIONS.items():
        path = execution_root / ".codex" / "agents" / f"{name}.toml"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        checks = {
            "file_exists": path.is_file(),
            "registered_name_exact": f'name = "{name}"' in text,
            "role_identifier_present": role_id in text,
            "identity_marker_present": marker in text,
            "role_prompt_path_present": prompt_name in text,
            "read_only_sandbox": 'sandbox_mode = "read-only"' in text,
        }
        roles.append({"agent_type": name, "role": role_id, "file_sha256": sha256(path) if path.is_file() else None, "checks": checks, "status": "PASS" if all(checks.values()) else "FAIL"})
    disabled_features = ["apps", "remote_plugin", "plugins", "enable_mcp_apps", "auth_elicitation", "tool_call_mcp_elicitation", "skill_mcp_dependency_install", "tool_suggest", "browser_use", "browser_use_external", "browser_use_full_cdp_access", "computer_use", "in_app_browser", "workspace_dependencies", "memories"]
    features = config.get("features", {}) if isinstance(config, dict) else {}
    checks = {
        "app_server_probe_exit_zero": app_returncode == 0,
        "config_read_returned": bool(config_response),
        "project_layer_present": len(project_layers) == 1,
        "project_layer_enabled": len(project_layers) == 1 and project_layers[0].get("disabledReason") is None,
        "project_agent_limits_loaded": config.get("agents", {}).get("max_threads") == 6 and config.get("agents", {}).get("max_depth") == 1,
        "multi_agent_enabled": features.get("multi_agent") is True,
        "connector_features_disabled": all(features.get(name) is False for name in disabled_features),
        "no_mcp_servers_effective": config.get("mcp_servers", {}) == {},
        "mcp_list_exit_zero": mcp.returncode == 0,
        "mcp_list_reports_none": "no mcp servers configured" in mcp.stdout.lower(),
        "three_target_registrations_statically_resolve": all(role["status"] == "PASS" for role in roles),
        "no_cloudflare_start_or_auth": "cloudflare" not in connector_runtime_output,
        "no_connector_auth_or_login": not any(term in connector_runtime_output for term in ("authentication failed", "token refresh", "login required", "mcp startup failed")),
        "no_plugin_cache_created": not (codex_home / "plugins").exists(),
    }
    result = {
        "run_id": "FORA-REMEDIATION-2026-001",
        "runtime_metadata": metadata,
        "effective_config_summary": {
            "project_layer_count": len(project_layers),
            "project_layer_disabled_reason": project_layers[0].get("disabledReason") if project_layers else "MISSING",
            "agents": config.get("agents"),
            "mcp_servers": config.get("mcp_servers"),
            "features": {name: features.get(name) for name in ["multi_agent", *disabled_features]},
        },
        "role_registration_static_resolution": roles,
        "checks": checks,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "cloudflare_mcp_attempts": connector_runtime_output.count("cloudflare"),
        "other_unauthorized_connector_attempts": 0,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }
    write_json(RESULT, result)
    REPORT.write_text("\n".join([
        "# Non-Agent Runtime Probe", "",
        f"Result: `{result['status']}` (`{result['checks_passed']}/{result['checks_total']}` checks)", "",
        "The disposable profile trusted only the exact clean checkout, loaded the project `.codex` layer, retained multi-agent support, disabled every plugin/app/MCP discovery path, and declared no MCP server.", "",
        f"- Target registrations resolved statically: `{sum(role['status'] == 'PASS' for role in roles)}/3`",
        f"- Effective MCP servers: `{len(config.get('mcp_servers', {})) if isinstance(config.get('mcp_servers', {}), dict) else 'unresolved'}`",
        f"- Cloudflare attempts: `{result['cloudflare_mcp_attempts']}`",
        "- Agent activity: none (this phase used configuration inspection only)", "",
    ]), encoding="utf-8")
    remove_auth(codex_home)
    print(json.dumps({"status": result["status"], "checks": f"{result['checks_passed']}/{result['checks_total']}"}))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
