#!/usr/bin/env python3
"""Timeout-bounded, hash-verified backend bootstrap for the Stage 2A profile."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STAGE2A = ROOT / "stage2a"
VENV = STAGE2A / ".venv"
REQUIREMENTS = ROOT / "backend/requirements.txt"
EVIDENCE = STAGE2A / "evidence/latest/BACKEND_BOOTSTRAP_RUN.json"
TIMEOUT = 900


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], *, env: dict[str, str] | None = None) -> dict[str, object]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=TIMEOUT, env=env)
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command[:4])}\n{completed.stderr[-2000:]}")
    sanitized = []
    for value in command:
        path = Path(value)
        if path.is_absolute():
            try:
                value = path.resolve().relative_to(ROOT.resolve()).as_posix()
            except ValueError:
                value = path.name
        sanitized.append(value)
    return {"command": sanitized, "exit_status": completed.returncode, "stdout": completed.stdout}


def main() -> int:
    if sys.version.split()[0] != "3.11.11":
        raise RuntimeError(f"Python 3.11.11 required, got {sys.version.split()[0]}")
    if not REQUIREMENTS.is_file():
        raise RuntimeError("backend requirements file missing")
    (STAGE2A / ".runtime").mkdir(parents=True, exist_ok=True)
    (STAGE2A / ".runtime/.owner.json").write_text('{"disposable": true, "owner": "ES-PKG-2026-004-V003"}\n', encoding="utf-8")
    shutil.rmtree(VENV, ignore_errors=True)
    attempts: list[dict[str, object]] = []
    try:
        base_env = {
            key: os.environ[key]
            for key in ("PATH", "TMPDIR", "LANG", "LC_ALL", "SSL_CERT_FILE")
            if os.environ.get(key)
        }
        attempts.append(run([sys.executable, "-m", "venv", str(VENV)], env=base_env))
        python = str(VENV / "bin/python")
        pip_env = base_env.copy()
        pip_env.update({
            "PIP_CONFIG_FILE": "/dev/null",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            "PIP_NO_INPUT": "1",
            "PIP_REQUIRE_VIRTUALENV": "1",
            "PYTHONNOUSERSITE": "1",
            "PIP_CACHE_DIR": str(STAGE2A / ".runtime/pip-cache"),
        })
        install_report = STAGE2A / ".runtime/pip-install-report.json"
        attempts.append(run([
            python, "-m", "pip", "install", "--no-deps", "--report", str(install_report),
            "--requirement", str(REQUIREMENTS),
        ], env=pip_env))
        attempts.append(run([python, "-m", "pip", "check"], env=pip_env))
        inventory_run = run([
            python, str(STAGE2A / "dependency_inventory.py"),
            "--install-report", str(install_report),
        ], env=pip_env)
        attempts.append(inventory_run)
        inventory_result = json.loads(str(inventory_run["stdout"]))
        inventory = inventory_result["inventory"]
        compatibility = inventory_result["dependency_compatibility"]
        report = {
            "validation": "PASS",
            "python": sys.version.split()[0],
            "requirements": "backend/requirements.txt",
            "requirements_sha256": sha(REQUIREMENTS),
            "all_requirements_exactly_pinned": True,
            "dependency_resolution": "DISABLED_NO_DEPS_ALL_DECLARED_REQUIREMENTS_EXACTLY_PINNED",
            "pip_config": "ISOLATED_DEV_NULL",
            "timeout_seconds_per_command": TIMEOUT,
            "installed_artifact_hash_basis": "PIP_INSTALL_REPORT_ARCHIVE_SHA256_PLUS_DIST_INFO_METADATA_SHA256",
            "inventory": inventory,
            "dependency_compatibility": compatibility,
            "commands": [{"command": x["command"], "exit_status": x["exit_status"]} for x in attempts],
        }
        EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
        EVIDENCE.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"validation": "PASS", "inventory_entries": len(inventory), "dependency_requirements_checked": compatibility["requirements_checked"]}, sort_keys=True))
        return 0
    except Exception:
        shutil.rmtree(VENV, ignore_errors=True)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
