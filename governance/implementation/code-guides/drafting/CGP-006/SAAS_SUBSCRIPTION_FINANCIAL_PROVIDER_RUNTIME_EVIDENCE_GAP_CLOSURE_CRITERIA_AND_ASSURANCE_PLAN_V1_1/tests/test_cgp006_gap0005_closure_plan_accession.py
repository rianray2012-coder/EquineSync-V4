from pathlib import Path
import importlib.util


def test_cgp006_gap0005_closure_plan_accession_package():
    validator = Path(__file__).resolve().parents[1] / "validators" / "validate_cgp006_gap0005_closure_plan_accession.py"
    spec = importlib.util.spec_from_file_location("cgp006_gap0005_validator", validator)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    module.validate()
