#!/usr/bin/env python3
"""Run fresh post-remediation calibration without changing preserved prior evidence."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROLE_REMEDIATION_DIR = HERE.parent
CYCLE_DIR = ROLE_REMEDIATION_DIR / "FORA-RCR-2026-001"
REPO_ROOT = ROLE_REMEDIATION_DIR.parents[3]
BASE_RUNNER_PATH = (
    REPO_ROOT
    / "governance"
    / "founder_orchestrated_review"
    / "runtime_remediation"
    / "scripts"
    / "run_behavioral_calibration.py"
)
RUNS_DIR = CYCLE_DIR / "runs" / "behavioral_calibration" / "ES-CAL-2026-001"
RESULT_PATH = CYCLE_DIR / "BEHAVIORAL_CALIBRATION_RESULT.json"
REPORT_PATH = CYCLE_DIR / "BEHAVIORAL_CALIBRATION_REPORT.md"
SUCCESS_DISPOSITION = "INSTALLATION_TECHNICALLY_READY_FOR_FOUNDER_ACTIVATION_REVIEW"
FAILURE_DISPOSITION = "INSTALLATION_NOT_READY_ROLE_CALIBRATION_FAILED"


def load_base_runner():
    spec = importlib.util.spec_from_file_location("equinesync_runtime_remediation_runner", BASE_RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load additive calibration runner: {BASE_RUNNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_base_runner()
base.RUNS_DIR = RUNS_DIR
base.RESULT_PATH = RESULT_PATH
base.REPORT_PATH = REPORT_PATH
base.runner.RUNS_DIR = RUNS_DIR
base.runner.MAIN_RESULT_PATH = RESULT_PATH
base.runner.MAIN_REPORT_PATH = REPORT_PATH

base_build_prompt = base.build_prompt


def build_prompt(agent_name, run_id, role, cases, permission_record):
    correction_rule = ""
    if agent_name == "equinesync_executable_golden_path_controller":
        correction_rule = (
            "ES-RA-08 RESPONSE CONTROL: In the initial child task, require the child to self-check its "
            "first object against every explicit fixed fact, required field name, CAL-01 through CAL-15 "
            "order, and supplied decision value before returning. It must use the private registration "
            "marker verbatim from its loaded instruction layer and must not abbreviate or reconstruct it. "
            "After the exact child finishes, compare its object with the "
            "explicit fixed facts, CAL-01 through CAL-15 order, and decision vocabulary below. If its "
            "first response renames fields, shortens the private marker, substitutes identifiers or "
            "decisions, or omits required facts, send exactly one correction request to that same child "
            "session. Restate the original synthetic payload and fixed facts without inventing or "
            "disclosing the marker. Wait for the corrected child response and return it verbatim. Do not "
            "spawn a replacement and do not manufacture a pass.\n\n"
        )
    return (
        "POST-REMEDIATION AUTHORIZATION: Founder authorization FORA-RCR-2026-001 expressly "
        "permits this fresh synthetic calibration run. Existing failed evidence is immutable. "
        "This run remains non-substantive, offline, non-production, and limited to a response-only "
        "child session. The child must use the exact registered agent_type and fork_turns=\"none\". "
        "No activation, pull request, merge, or default-branch action is authorized.\n\n"
        + correction_rule
        + base_build_prompt(agent_name, run_id, role, cases, permission_record)
    )


base.build_prompt = build_prompt

base_command_record = base.runner.command_record


def command_record(command, role, run_id):
    record = base_command_record(command, role, run_id)
    record["founder_authorization_id"] = "FORA-RCR-2026-001"
    record["authorization_path"] = str(CYCLE_DIR / "FOUNDER_AUTHORIZATION.md")
    record["prior_failed_evidence_preserved"] = True
    return record


base.runner.command_record = command_record


def aggregate():
    result = base.sealed_aggregate()
    ready = (
        result["roles_with_passing_run"] == result["roles_expected"] == 8
        and result["custom_instruction_layers_loaded"] == 8
        and result["sandbox_modes_verified"] == 8
        and result["accepted_behavior_passes"] == result["behavior_denominator"] == 120
    )
    result["recommended_installation_disposition"] = (
        SUCCESS_DISPOSITION if ready else FAILURE_DISPOSITION
    )
    result["founder_activation_approval"] = False
    result["authorization_id"] = "FORA-RCR-2026-001"
    result["preserved_prior_evidence_commit"] = "35119dbfb873e0fd19fef2a1e574d2f8100286f3"
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    base.runner.write_report(result)
    return result


base.aggregate = aggregate
base.runner.aggregate = aggregate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Run all eight roles sequentially")
    parser.add_argument("--agent", help="Run one exact registered custom-agent type")
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()
    if sum((args.all, bool(args.agent), args.aggregate_only)) != 1:
        parser.error("choose exactly one of --all, --agent, or --aggregate-only")

    cases = base.runner.read_json(base.runner.CASES_PATH)
    names = list(cases["roles"]) if args.all else ([args.agent] if args.agent else [])
    failed = False
    for name in names:
        if name not in cases["roles"]:
            parser.error(f"unknown registered custom-agent type: {name}")
        print(f"Starting {name}", flush=True)
        run_dir = base.runner.execute_agent(name)
        status = base.runner.read_json(run_dir / "score.json")["status"]
        print(f"Preserved {run_dir.relative_to(REPO_ROOT)}: {status}", flush=True)
        failed = failed or status != "PASS"
        aggregate()
    if args.aggregate_only:
        aggregate()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
