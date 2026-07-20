#!/usr/bin/env python3
"""Shared, secret-safe support for the disposable requalification runtime."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess


RUN_ID = "FORA-REMEDIATION-2026-001"
STARTING_COMMIT = "e93d3acc65a45835d3f3c63473f5dd98e1d1bcf5"
BRANCH = "agent/install-founder-review-agents-v1.0.0"
PACKAGE_SHA256 = "604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3"
SCRIPT = Path(__file__).resolve()
RUN_ROOT = SCRIPT.parent.parent
REPO_ROOT = SCRIPT.parents[6]
TEMPLATE = RUN_ROOT / "runtime" / "isolated_codex_config.template.toml"

SENSITIVE_NAME = re.compile(
    r"(?:SECRET|TOKEN|PASSWORD|PASSWD|API_?KEY|PRIVATE_?KEY|DATABASE_URL|"
    r"STRIPE|SUPABASE|AWS_|GCP_|GOOGLE_APPLICATION_CREDENTIALS|AZURE_|"
    r"RENDER|VERCEL|CLOUDFLARE|PRODUCTION|PROD_)", re.IGNORECASE
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=False
    )
    if check and completed.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed


def repository_snapshot(root: Path) -> list[dict]:
    result = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.relative_to(root).parts:
            continue
        result.append({
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    return result


def records(path: Path) -> list[dict]:
    result = []
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            result.append(item)
    return result


def final_assistant_text(items: list[dict]) -> str | None:
    values = []
    for item in items:
        payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
        if item.get("type") == "event_msg" and payload.get("type") == "task_complete":
            message = payload.get("last_agent_message")
            if isinstance(message, str):
                values.append(message)
    return values[-1] if values else None


def safe_turn_context(items: list[dict]) -> dict:
    contexts = [item.get("payload", {}) for item in items if item.get("type") == "turn_context"]
    if not contexts:
        return {}
    context = contexts[-1]
    sandbox = context.get("sandbox_policy") if isinstance(context.get("sandbox_policy"), dict) else {}
    profile = context.get("permission_profile") if isinstance(context.get("permission_profile"), dict) else {}
    return {
        "approval_policy": context.get("approval_policy"),
        "sandbox_policy": sandbox,
        "permission_profile": {key: profile.get(key) for key in ("type", "network") if key in profile},
        "model": context.get("model"),
        "reasoning_effort": context.get("effort"),
    }


def safe_tool_names(items: list[dict]) -> list[str]:
    names = []
    for item in items:
        payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
        if item.get("type") != "response_item":
            continue
        if payload.get("type") == "function_call":
            names.append(payload.get("name"))
        elif payload.get("type") == "custom_tool_call":
            names.append(payload.get("name") or payload.get("tool_name") or "custom_tool")
    return [name for name in names if isinstance(name, str)]


def safe_spawn_calls(items: list[dict]) -> list[dict]:
    calls = []
    for item in items:
        payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
        if item.get("type") != "response_item" or payload.get("type") != "function_call" or payload.get("name") != "spawn_agent":
            continue
        try:
            args = json.loads(payload.get("arguments", "{}"))
        except (TypeError, json.JSONDecodeError):
            args = {}
        calls.append({key: args.get(key) for key in ("task_name", "agent_type", "fork_turns")})
    return calls


def parent_thread_id(events_path: Path) -> str | None:
    for item in records(events_path):
        if item.get("type") == "thread.started" and isinstance(item.get("thread_id"), str):
            return item["thread_id"]
    return None


def sanitized_provenance(events_path: Path, codex_home: Path) -> dict:
    parent_id = parent_thread_id(events_path)
    parent_paths = sorted((codex_home / "sessions").rglob(f"*{parent_id}.jsonl")) if parent_id else []
    parent_items = records(parent_paths[-1]) if parent_paths else []
    children = []
    if parent_id:
        for child_path in sorted((codex_home / "sessions").rglob("*.jsonl")):
            try:
                first = json.loads(child_path.open("r", encoding="utf-8", errors="replace").readline())
            except (OSError, json.JSONDecodeError):
                continue
            payload = first.get("payload") if isinstance(first.get("payload"), dict) else {}
            source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
            subagent = source.get("subagent") if isinstance(source.get("subagent"), dict) else {}
            spawn = subagent.get("thread_spawn") if isinstance(subagent.get("thread_spawn"), dict) else {}
            if spawn.get("parent_thread_id") != parent_id:
                continue
            child_items = records(child_path)
            children.append({
                "child_thread_id": payload.get("id"),
                "agent_path": spawn.get("agent_path"),
                "agent_role": spawn.get("agent_role"),
                "depth": spawn.get("depth"),
                "cli_version": payload.get("cli_version"),
                "cwd": payload.get("cwd"),
                "runtime": safe_turn_context(child_items),
                "tool_names_only": safe_tool_names(child_items),
                "final_assistant_response": final_assistant_text(child_items),
                "source_rollout_basename": child_path.name,
                "source_rollout_sha256": sha256(child_path),
                "source_rollout_bytes": child_path.stat().st_size,
            })
    return {
        "sanitization": {
            "credential_material_copied": False,
            "hidden_instruction_text_copied": False,
            "scope": "Runtime identity, policy, tool names, direct child response, and source hash only."
        },
        "parent_thread_id": parent_id,
        "parent_runtime": safe_turn_context(parent_items),
        "parent_tool_names_only": safe_tool_names(parent_items),
        "parent_spawn_calls": safe_spawn_calls(parent_items),
        "parent_source_rollout_basename": parent_paths[-1].name if parent_paths else None,
        "parent_source_rollout_sha256": sha256(parent_paths[-1]) if parent_paths else None,
        "children": sorted(children, key=lambda item: item.get("agent_path") or ""),
    }


def parse_json_object(value: object) -> dict:
    if not isinstance(value, str):
        return {}
    text = value.strip()
    if text.startswith("```") and text.endswith("```"):
        text = "\n".join(text.splitlines()[1:-1]).strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def create_isolated_runtime(runtime_root: Path, execution_root: Path, auth_file: Path, codex_binary: Path) -> tuple[Path, Path, dict[str, str], dict]:
    if runtime_root.exists():
        raise RuntimeError(f"runtime root already exists: {runtime_root}")
    codex_home = runtime_root / "codex-home"
    home = runtime_root / "home"
    temp = runtime_root / "tmp"
    output = runtime_root / "output"
    for path in (codex_home, home, temp, output):
        path.mkdir(parents=True)
    if not auth_file.is_file():
        raise RuntimeError("Codex control-plane authentication is unavailable")
    auth_target = codex_home / "auth.json"
    shutil.copyfile(auth_file, auth_target)
    auth_target.chmod(stat.S_IRUSR | stat.S_IWUSR)
    rendered = TEMPLATE.read_text(encoding="utf-8").replace("__EXECUTION_ROOT__", str(execution_root).replace('"', '\\"'))
    config_path = codex_home / "config.toml"
    config_path.write_text(rendered, encoding="utf-8")
    config_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    minimal_path = ":".join(dict.fromkeys([
        str(codex_binary.parent), "/usr/local/bin", "/usr/bin", "/bin", "/usr/sbin", "/sbin"
    ]))
    env = {
        "PATH": minimal_path,
        "HOME": str(home),
        "CODEX_HOME": str(codex_home),
        "USER": os.environ.get("USER", "codex"),
        "LOGNAME": os.environ.get("LOGNAME", os.environ.get("USER", "codex")),
        "SHELL": "/bin/zsh",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TMPDIR": str(temp),
        "TERM": "dumb",
        "NO_COLOR": "1",
        "CI": "1",
    }
    metadata = {
        "config_sha256": sha256(config_path),
        "template_sha256": sha256(TEMPLATE),
        "execution_root": str(execution_root),
        "environment_variable_names_only": sorted(env),
        "ambient_sensitive_environment_variable_names_not_inherited": sorted(name for name in os.environ if SENSITIVE_NAME.search(name)),
        "control_plane_auth_copied": True,
        "control_plane_auth_content_or_hash_recorded": False,
        "mcp_servers_declared": 0,
        "plugins_declared": 0,
    }
    return codex_home, output, env, metadata


def remove_auth(codex_home: Path) -> None:
    auth = codex_home / "auth.json"
    if auth.exists():
        auth.unlink()
