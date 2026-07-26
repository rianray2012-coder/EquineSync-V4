"""Known-failure non-regression gate for PR #3 backend CI.

The non-live suite still runs in full. This gate turns its JUnit output into a
ratchet: reviewed failures may remain, but new failures, new errors, collection
loss, or inventory drift fail the job.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_COUNTS = {
    "total_collected",
    "selected_non_live",
    "live_deselected",
    "passed",
    "failed",
    "errors",
    "skipped",
}


@dataclass(frozen=True)
class CollectCounts:
    selected: int
    total: int
    deselected: int


@dataclass(frozen=True)
class JunitResult:
    total: int
    passed: int
    failed: int
    errors: int
    skipped: int
    failed_nodes: set[str]
    error_nodes: set[str]


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"baseline file missing: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"baseline file is malformed JSON: {exc}") from exc


def load_baseline(path: Path) -> dict[str, str]:
    raw = _load_json(path)
    if raw.get("schema") != "equinesync_pr3_known_failure_baseline_v1":
        raise ValueError("baseline schema is missing or unsupported")

    counts = raw.get("counts")
    if not isinstance(counts, dict) or REQUIRED_COUNTS - counts.keys():
        missing = sorted(REQUIRED_COUNTS - set(counts or ()))
        raise ValueError(f"baseline counts are missing: {missing}")

    entries = raw.get("known_failure_or_error_nodes")
    if not isinstance(entries, list):
        raise ValueError("baseline known_failure_or_error_nodes must be a list")

    baseline: dict[str, str] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ValueError(f"baseline entry {index} is not an object")
        nodeid = entry.get("nodeid")
        outcome = entry.get("outcome")
        if not isinstance(nodeid, str) or not nodeid:
            raise ValueError(f"baseline entry {index} has no nodeid")
        if outcome not in {"failure", "error"}:
            raise ValueError(f"baseline entry {index} has invalid outcome: {outcome}")
        if nodeid in baseline:
            raise ValueError(f"baseline has duplicate nodeid: {nodeid}")
        baseline[nodeid] = outcome

    expected = int(counts["failed"]) + int(counts["errors"])
    if len(baseline) != expected:
        raise ValueError(
            "baseline known node count does not match failed+errors: "
            f"{len(baseline)} != {expected}"
        )
    return baseline


def _last_matching_line(text: str, pattern: str) -> str:
    matches = [line for line in text.splitlines() if re.search(pattern, line)]
    if not matches:
        raise ValueError(f"could not find collection summary matching {pattern!r}")
    return matches[-1]


def parse_collect_counts(path: Path) -> CollectCounts:
    text = path.read_text(encoding="utf-8", errors="replace")
    line = _last_matching_line(text, r"tests collected")

    selected_match = re.search(
        r"(?:(?P<selected>\d+)/)?(?P<total>\d+) tests collected"
        r"(?: \((?P<deselected>\d+) deselected\))?",
        line,
    )
    if not selected_match:
        raise ValueError(f"could not parse collection summary in {path}: {line}")

    total = int(selected_match.group("total"))
    selected = int(selected_match.group("selected") or total)
    deselected = int(selected_match.group("deselected") or 0)
    return CollectCounts(selected=selected, total=total, deselected=deselected)


def _suite_for_junit(path: Path) -> ET.Element:
    try:
        root = ET.parse(path).getroot()
    except FileNotFoundError as exc:
        raise ValueError(f"JUnit report missing: {path}") from exc
    except ET.ParseError as exc:
        raise ValueError(f"JUnit report is malformed XML: {exc}") from exc

    if root.tag == "testsuite":
        return root
    if root.tag == "testsuites":
        suites = root.findall("testsuite")
        if len(suites) == 1:
            return suites[0]
        raise ValueError("JUnit report must contain exactly one testsuite")
    raise ValueError(f"unexpected JUnit root element: {root.tag}")


def _nodeid_for_case(case: ET.Element) -> str:
    classname = case.get("classname", "")
    name = case.get("name", "")
    parts = classname.split(".")

    if len(parts) >= 3 and parts[0] == "backend" and parts[1] == "tests":
        try:
            module_index = next(
                index for index, part in enumerate(parts) if part.startswith("test_")
            )
        except StopIteration:
            module_index = len(parts) - 1
        path = "/".join(parts[: module_index + 1]) + ".py"
        selectors = parts[module_index + 1 :] + [name]
        return "::".join([path, *[selector for selector in selectors if selector]])

    path = classname.replace(".", "/") + ".py"
    return f"{path}::{name}" if name else path


def parse_junit(path: Path) -> JunitResult:
    suite = _suite_for_junit(path)
    total = int(suite.get("tests", 0))
    failed = int(suite.get("failures", 0))
    errors = int(suite.get("errors", 0))
    skipped = int(suite.get("skipped", 0))
    passed = total - failed - errors - skipped

    failed_nodes: set[str] = set()
    error_nodes: set[str] = set()
    for case in suite.iter("testcase"):
        nodeid = _nodeid_for_case(case)
        if case.find("failure") is not None:
            failed_nodes.add(nodeid)
        if case.find("error") is not None:
            error_nodes.add(nodeid)

    if len(failed_nodes) != failed:
        raise ValueError(
            f"JUnit failure count mismatch: attrs={failed} parsed={len(failed_nodes)}"
        )
    if len(error_nodes) != errors:
        raise ValueError(
            f"JUnit error count mismatch: attrs={errors} parsed={len(error_nodes)}"
        )
    return JunitResult(
        total=total,
        passed=passed,
        failed=failed,
        errors=errors,
        skipped=skipped,
        failed_nodes=failed_nodes,
        error_nodes=error_nodes,
    )


def _format_nodes(nodes: Iterable[str], limit: int = 300) -> str:
    sorted_nodes = sorted(nodes)
    if not sorted_nodes:
        return "_None._"
    visible = sorted_nodes[:limit]
    lines = "\n".join(f"- `{node}`" for node in visible)
    if len(sorted_nodes) > limit:
        lines += f"\n- ... {len(sorted_nodes) - limit} more"
    return lines


def build_summary(
    *,
    baseline_raw: dict,
    baseline: dict[str, str],
    collect: CollectCounts,
    live_collect: CollectCounts,
    not_live_collect: CollectCounts,
    junit: JunitResult,
    pytest_exit_code: str,
    failures: list[str],
) -> str:
    baseline_failure_nodes = {
        nodeid for nodeid, outcome in baseline.items() if outcome == "failure"
    }
    baseline_error_nodes = {
        nodeid for nodeid, outcome in baseline.items() if outcome == "error"
    }
    known_failures_remaining = junit.failed_nodes & baseline_failure_nodes
    known_errors_remaining = junit.error_nodes & baseline_error_nodes
    new_failures = junit.failed_nodes - baseline_failure_nodes
    new_errors = junit.error_nodes - baseline_error_nodes
    resolved = set(baseline) - junit.failed_nodes - junit.error_nodes

    status = "PASS" if not failures else "FAIL"
    lines = [
        "## Backend known-failure non-regression gate",
        "",
        f"**Non-regression gate:** {status}",
        "",
        f"Baseline commit: `{baseline_raw.get('baseline_commit', 'unknown')}`",
        f"Raw pytest exit code: `{pytest_exit_code}`",
        "",
        "| Result | Count |",
        "| --- | ---: |",
        f"| Total collected | {collect.total} |",
        f"| Selected non-live | {not_live_collect.selected} |",
        f"| Deselected live | {not_live_collect.deselected} |",
        f"| Passed | {junit.passed} |",
        f"| Failed | {junit.failed} |",
        f"| Errored | {junit.errors} |",
        f"| Skipped | {junit.skipped} |",
        "",
        "### KNOWN FAILURES REMAINING",
        "",
        f"Count: {len(known_failures_remaining)}",
        "",
        _format_nodes(known_failures_remaining),
        "",
        "### KNOWN ERRORS REMAINING",
        "",
        f"Count: {len(known_errors_remaining)}",
        "",
        _format_nodes(known_errors_remaining),
        "",
        "### NEW FAILURES",
        "",
        f"Count: {len(new_failures)}",
        "",
        _format_nodes(new_failures),
        "",
        "### NEW ERRORS",
        "",
        f"Count: {len(new_errors)}",
        "",
        _format_nodes(new_errors),
        "",
        "### RESOLVED SINCE BASELINE",
        "",
        f"Count: {len(resolved)}",
        "",
        _format_nodes(resolved),
        "",
    ]

    if failures:
        lines.extend(["### Gate Failure Reasons", ""])
        lines.extend(f"- {failure}" for failure in failures)
        lines.append("")

    lines.append(
        "Known failures are retained as a reviewed baseline only. This gate does "
        "not release, accept, skip, xfail, or weaken the underlying behavior."
    )
    lines.append("")
    return "\n".join(lines)


def evaluate(
    *,
    baseline_raw: dict,
    baseline: dict[str, str],
    collect: CollectCounts,
    live_collect: CollectCounts,
    not_live_collect: CollectCounts,
    junit: JunitResult,
) -> list[str]:
    counts = baseline_raw["counts"]
    failures: list[str] = []

    if collect.total < int(counts["total_collected"]):
        failures.append(
            "total collection decreased: "
            f"{collect.total} < baseline {counts['total_collected']}"
        )
    if not_live_collect.selected < int(counts["selected_non_live"]):
        failures.append(
            "selected non-live inventory decreased: "
            f"{not_live_collect.selected} < baseline {counts['selected_non_live']}"
        )
    if live_collect.selected > int(counts["live_deselected"]):
        failures.append(
            "live allowlist inventory expanded without baseline update: "
            f"{live_collect.selected} > baseline {counts['live_deselected']}"
        )
    if not_live_collect.deselected > int(counts["live_deselected"]):
        failures.append(
            "non-live deselection count expanded without baseline update: "
            f"{not_live_collect.deselected} > baseline {counts['live_deselected']}"
        )
    if junit.total != not_live_collect.selected:
        failures.append(
            "JUnit selected count does not match non-live collection: "
            f"{junit.total} != {not_live_collect.selected}"
        )
    if junit.skipped > int(counts["skipped"]):
        failures.append(
            "skipped count increased: "
            f"{junit.skipped} > baseline {counts['skipped']}"
        )

    baseline_failure_nodes = {
        nodeid for nodeid, outcome in baseline.items() if outcome == "failure"
    }
    baseline_error_nodes = {
        nodeid for nodeid, outcome in baseline.items() if outcome == "error"
    }
    new_failures = junit.failed_nodes - baseline_failure_nodes
    new_errors = junit.error_nodes - baseline_error_nodes
    if new_failures:
        failures.append(f"new failing node IDs appeared: {len(new_failures)}")
    if new_errors:
        failures.append(f"new erroring node IDs appeared: {len(new_errors)}")

    return failures


def read_exit_code(path: Path | None) -> str:
    if path is None:
        return "not-recorded"
    try:
        return path.read_text(encoding="utf-8").strip() or "empty"
    except FileNotFoundError:
        return "missing"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--junit", required=True, type=Path)
    parser.add_argument("--collect-log", required=True, type=Path)
    parser.add_argument("--live-collect-log", required=True, type=Path)
    parser.add_argument("--not-live-collect-log", required=True, type=Path)
    parser.add_argument("--pytest-exit-code-file", type=Path)
    parser.add_argument("--summary-output", type=Path)
    args = parser.parse_args(argv)

    try:
        baseline_raw = _load_json(args.baseline)
        baseline = load_baseline(args.baseline)
        collect = parse_collect_counts(args.collect_log)
        live_collect = parse_collect_counts(args.live_collect_log)
        not_live_collect = parse_collect_counts(args.not_live_collect_log)
        junit = parse_junit(args.junit)
        failures = evaluate(
            baseline_raw=baseline_raw,
            baseline=baseline,
            collect=collect,
            live_collect=live_collect,
            not_live_collect=not_live_collect,
            junit=junit,
        )
        summary = build_summary(
            baseline_raw=baseline_raw,
            baseline=baseline,
            collect=collect,
            live_collect=live_collect,
            not_live_collect=not_live_collect,
            junit=junit,
            pytest_exit_code=read_exit_code(args.pytest_exit_code_file),
            failures=failures,
        )
    except Exception as exc:  # noqa: BLE001 - this is a CI diagnostics tool
        summary = (
            "## Backend known-failure non-regression gate\n\n"
            "**Non-regression gate:** FAIL\n\n"
            f"Parser or baseline validation failed: `{exc}`\n"
        )
        failures = [str(exc)]

    print(summary)
    if args.summary_output:
        args.summary_output.write_text(summary, encoding="utf-8")
    github_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_summary:
        with Path(github_summary).open("a", encoding="utf-8") as handle:
            handle.write(summary)
            handle.write("\n")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
