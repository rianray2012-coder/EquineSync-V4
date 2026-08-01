from __future__ import annotations
import csv
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

PACKAGE = Path(__file__).resolve().parents[1]
VALIDATOR = PACKAGE / "validators" / "validate_master_product_feature_coverage_matrix.py"
spec = importlib.util.spec_from_file_location("validator", VALIDATOR)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def payload():
    rows = read_csv(PACKAGE / "EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv")
    obj = json.loads((PACKAGE / "EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.json").read_text(encoding="utf-8"))
    sources = read_csv(PACKAGE / "SOURCE_AND_AUTHORITY_REGISTER.csv")
    pias = read_csv(PACKAGE / "PIA_FEATURE_COVERAGE_SUMMARY.csv")
    gov = read_csv(PACKAGE / "GOVERNANCE_ARTIFACT_INVENTORY.csv")
    decisions = read_csv(PACKAGE / "PROPOSED_NEW_PIA_AND_SUPPLEMENT_DECISION_REGISTER.csv")
    gaps = read_csv(PACKAGE / "NON_PIA_DOCUMENT_AND_CONTROL_GAP_REGISTER.csv")
    return rows, obj, sources, pias, gov, decisions, gaps

def test_current_payload_validates_without_payload_errors():
    rows, obj, sources, pias, gov, decisions, gaps = payload()
    assert validator.validate_payload(rows, obj, sources, pias, gov, decisions, gaps) == []

def test_duplicate_feature_id_is_rejected():
    rows, obj, sources, pias, gov, decisions, gaps = payload()
    mutated = [dict(r) for r in rows]
    mutated[1]["Feature ID"] = mutated[0]["Feature ID"]
    obj2 = dict(obj)
    obj2["features"] = mutated
    errors = validator.validate_payload(mutated, obj2, sources, pias, gov, decisions, gaps)
    assert any("Duplicate Feature ID" in e for e in errors)

def test_new_pia_row_requires_decision_register_entry():
    rows, obj, sources, pias, gov, decisions, gaps = payload()
    mutated = [dict(r) for r in rows]
    target = next(r for r in mutated if r["Final disposition"] == "DRAFT_NEW_PIA")
    target["Required new document or supplement"] = "DOC-MISSING-NEW-PIA"
    obj2 = dict(obj)
    obj2["features"] = mutated
    errors = validator.validate_payload(mutated, obj2, sources, pias, gov, decisions, gaps)
    assert any("DRAFT_NEW_PIA missing decision register row" in e for e in errors)

if __name__ == "__main__":
    test_current_payload_validates_without_payload_errors()
    test_duplicate_feature_id_is_rejected()
    test_new_pia_row_requires_decision_register_entry()
    print("VALIDATOR_TESTS_PASS")
