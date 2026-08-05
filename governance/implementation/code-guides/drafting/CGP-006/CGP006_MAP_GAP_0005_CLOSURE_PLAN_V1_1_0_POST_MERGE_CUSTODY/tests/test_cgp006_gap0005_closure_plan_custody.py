#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


def test_cgp006_gap0005_closure_plan_custody_validator_passes() -> None:
    validator_path = Path(__file__).resolve().parents[1] / "validators" / "validate_cgp006_gap0005_closure_plan_custody.py"
    spec = importlib.util.spec_from_file_location("validate_cgp006_gap0005_closure_plan_custody", validator_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    result = module.validate()
    assert result["status"] == "PASS"
    assert result["accession_merge_commit"] == "95a4c9b4006f4bd4377f75b3d0fef57d5f424dee"
    assert result["gap_status"] == "CGP006_MAP_GAP_0005_REMAINS_OPEN"
    assert result["source_identity_rows"] == 8


if __name__ == "__main__":
    test_cgp006_gap0005_closure_plan_custody_validator_passes()
    print("PASS test_cgp006_gap0005_closure_plan_custody_validator_passes")
