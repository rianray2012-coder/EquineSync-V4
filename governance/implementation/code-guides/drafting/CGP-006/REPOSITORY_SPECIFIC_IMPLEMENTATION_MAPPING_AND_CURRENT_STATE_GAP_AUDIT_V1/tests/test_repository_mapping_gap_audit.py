
import importlib.util
import pathlib


def test_repository_mapping_gap_audit_validator_passes():
    validator_path = pathlib.Path(__file__).resolve().parents[1] / 'validators' / 'validate_repository_mapping_gap_audit.py'
    spec = importlib.util.spec_from_file_location('validate_repository_mapping_gap_audit', validator_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    result = module.validate()
    assert result['status'] == 'PASS'
    assert result['mapping_rows'] == 22
    assert result['gap_rows'] == 12


if __name__ == '__main__':
    test_repository_mapping_gap_audit_validator_passes()
    print('PASS test_repository_mapping_gap_audit_validator_passes')
