#!/usr/bin/env python3
"""Extract safe custom-agent runtime provenance without copying hidden instructions."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
REMEDIATION = HERE.parent
CODEX_HOME = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser()
INTERACTIVE_PARENT_IDS = {
    "runs/canary_project_standalone/interactive_cli/run-01": "019f7c39-fe01-7780-a4df-ca47147a48f3",
    "runs/canary_project_standalone/interactive_cli/run-02": "019f7c3b-74ad-7520-880d-228cf2f7c861",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def records(path: Path):
    result = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            result.append(value)
    return result


def parent_id_from_events(path: Path):
    for record in records(path):
        if record.get("type") == "thread.started":
            return record.get("thread_id")
    return None


def safe_turn_context(items):
    contexts = [item.get("payload", {}) for item in items if item.get("type") == "turn_context"]
    if not contexts:
        return {}
    context = contexts[-1]
    sandbox = context.get("sandbox_policy") if isinstance(context.get("sandbox_policy"), dict) else {}
    profile = context.get("permission_profile") if isinstance(context.get("permission_profile"), dict) else {}
    return {
        "approval_policy": context.get("approval_policy"),
        "sandbox_policy": sandbox,
        "permission_profile": {
            key: profile.get(key) for key in ("type", "network") if key in profile
        },
        "model": context.get("model"),
        "reasoning_effort": context.get("effort"),
    }


def final_assistant_text(items):
    texts = []
    for item in items:
        payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
        if item.get("type") == "event_msg" and payload.get("type") == "task_complete":
            text = payload.get("last_agent_message")
            if isinstance(text, str):
                texts.append(text)
    return texts[-1] if texts else None


def safe_tool_names(items):
    names = []
    for item in items:
        payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
        if item.get("type") != "response_item":
            continue
        kind = payload.get("type")
        if kind == "function_call":
            names.append(payload.get("name"))
        elif kind == "custom_tool_call":
            names.append(payload.get("name") or payload.get("tool_name") or "custom_tool")
    return [name for name in names if isinstance(name, str)]


def safe_spawn_calls(items):
    calls = []
    for item in items:
        payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
        if item.get("type") != "response_item" or payload.get("type") != "function_call":
            continue
        if payload.get("name") != "spawn_agent":
            continue
        try:
            args = json.loads(payload.get("arguments", "{}"))
        except (TypeError, json.JSONDecodeError):
            args = {}
        calls.append({key: args.get(key) for key in ("task_name", "agent_type", "fork_turns")})
    return calls


def main():
    sessions = []
    for path in sorted((CODEX_HOME / "sessions").rglob("*.jsonl")):
        try:
            first = json.loads(path.open("r", encoding="utf-8", errors="replace").readline())
        except (OSError, json.JSONDecodeError):
            continue
        payload = first.get("payload") if isinstance(first.get("payload"), dict) else {}
        source = payload.get("source") if isinstance(payload.get("source"), dict) else {}
        subagent = source.get("subagent") if isinstance(source.get("subagent"), dict) else {}
        spawn = subagent.get("thread_spawn") if isinstance(subagent.get("thread_spawn"), dict) else {}
        if spawn.get("parent_thread_id"):
            sessions.append((path, payload, spawn))

    run_sources = []
    for path in REMEDIATION.rglob("stdout.jsonl"):
        run_sources.append((path.parent, parent_id_from_events(path), path))
    for path in REMEDIATION.rglob("events.jsonl"):
        run_sources.append((path.parent, parent_id_from_events(path), path))
    for relative, parent_id in INTERACTIVE_PARENT_IDS.items():
        run_dir = REMEDIATION / relative
        run_sources.append((run_dir, parent_id, run_dir / "raw_terminal.log"))

    written = 0
    for run_dir, parent_id, raw_parent in run_sources:
        if not isinstance(parent_id, str):
            continue
        parent_rollouts = sorted((CODEX_HOME / "sessions").rglob(f"*{parent_id}.jsonl"))
        parent_records = records(parent_rollouts[-1]) if parent_rollouts else []
        children = []
        for child_path, child_meta, spawn in sessions:
            if spawn.get("parent_thread_id") != parent_id:
                continue
            child_records = records(child_path)
            children.append(
                {
                    "child_thread_id": child_meta.get("id"),
                    "agent_path": spawn.get("agent_path"),
                    "agent_role": spawn.get("agent_role"),
                    "depth": spawn.get("depth"),
                    "cli_version": child_meta.get("cli_version"),
                    "cwd": child_meta.get("cwd"),
                    "runtime": safe_turn_context(child_records),
                    "tool_names_only": safe_tool_names(child_records),
                    "final_assistant_response": final_assistant_text(child_records),
                    "source_rollout_basename": child_path.name,
                    "source_rollout_sha256": sha256(child_path),
                    "source_rollout_bytes": child_path.stat().st_size,
                }
            )
        evidence = {
            "sanitization": {
                "hidden_system_or_developer_instructions_copied": False,
                "encrypted_reasoning_or_messages_copied": False,
                "scope": "session identity, selected custom-agent role, runtime policy, tool names, final child response, and source hash only",
            },
            "parent_thread_id": parent_id,
            "parent_runtime": safe_turn_context(parent_records),
            "parent_spawn_calls": safe_spawn_calls(parent_records),
            "parent_source_rollout_basename": parent_rollouts[-1].name if parent_rollouts else None,
            "parent_source_rollout_sha256": sha256(parent_rollouts[-1]) if parent_rollouts else None,
            "raw_parent_artifact": str(raw_parent.relative_to(REMEDIATION)),
            "children": sorted(children, key=lambda item: item.get("agent_path") or ""),
        }
        (run_dir / "sanitized_child_sessions.json").write_text(
            json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        written += 1
    print(f"wrote {written} sanitized provenance artifact(s)")


if __name__ == "__main__":
    main()
