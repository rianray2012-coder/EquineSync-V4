from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import subprocess
import sys

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[5]
AUTHORIZED_PACKAGE_PATH = "governance/implementation/code-guides/drafting/CGP-006/REPOSITORY_HYGIENE_DEPENDENCY_AND_CI_ASSURANCE_V1/"
REQUIRED_HEAD = "396f82c8a7600cae363142175d1d1448e9d2ece2"
REQUIRED_FILES = [
    "README.md",
    "REPOSITORY_STATE_VERIFICATION_RECEIPT.json",
    "COPILOT_FINDING_VALIDATION_MATRIX.csv",
    "DEPENDENCY_CLASSIFICATION_INVENTORY.csv",
    "FRONTEND_PEER_CONFLICT_MATRIX.csv",
    "CI_ASSURANCE_GAP_ANALYSIS.csv",
    "SECRET_AND_CONFIGURATION_REVIEW_REPORT.md",
    "LICENSE_AND_DISTRIBUTION_DECISION_MEMORANDUM.md",
    "DEPLOYMENT_MODEL_DETERMINATION.md",
    "LARGE_MODULE_RISK_OBSERVATION_REGISTER.csv",
    "PROPOSED_PR_SEGMENTATION_AND_DEPENDENCY_PLAN.md",
    "FOUNDER_DECISION_REGISTER.csv",
    "COMMAND_EXECUTION_AND_LIMITATION_LOG.md",
    "VALIDATION_REPORT.md",
    "AUTHORIZED_PATH_REPORT.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validators/validate_repository_hygiene_ci_assurance_review.py",
    "tests/test_repository_hygiene_ci_assurance_review.py",
]
ALLOWED_CLASSIFICATIONS = {
    "CONFIRMED",
    "PARTIALLY_CONFIRMED",
    "NOT_CONFIRMED",
    "SUPERSEDED_BY_CURRENT_REPOSITORY_STATE",
    "REQUIRES_FOUNDER_DECISION",
    "REQUIRES_SEPARATE_TECHNICAL_DESIGN",
    "BLOCKED_BY_INSUFFICIENT_EVIDENCE",
}
REQUIRED_TOKENS = [
    "DOCUMENTARY_REVIEW_PACKAGE_COMPLETE",
    "COPILOT_LEADS_INDEPENDENTLY_VALIDATED",
    "ALL_18_GAPS_REMAIN_OPEN",
    "ALL_16_FINDINGS_RETAIN_RECORDED_STATUS",
    "ALL_15_IWPS_REMAIN_CANDIDATES_ONLY",
    "AUTHORIZED_IWPS_TOTAL_0",
    "GAP_0004_REMAINS_OPEN",
    "IMPLEMENTATION_NOT_EFFECTIVE",
    "DEPLOYMENT_NOT_AUTHORIZED",
    "STAGING_NOT_AUTHORIZED",
    "PILOT_NOT_AUTHORIZED",
    "PRODUCTION_USE_NOT_AUTHORIZED",
    "WAVE_2_NOT_AUTHORIZED",
    "CGP_007_NOT_AUTHORIZED",
    "NO_DIRECT_PROTECTED_BRANCH_PUSH",
    "NO_PROTECTED_MERGE_AUTHORIZED",
    "NO_OPEN_SOURCE_LICENSE_GRANT_AUTHORIZED",
    "NO_EXTERNAL_SCANNER_OR_REPOSITORY_APP_SETUP_AUTHORIZED",
    "NO_GAP_CLOSURE_AUTHORIZED",
    "NO_FINDING_CLOSURE_AUTHORIZED",
    "NO_IWP_ACTIVATION_AUTHORIZED",
]


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(cmd, cwd=REPO_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and cp.returncode != 0:
        raise AssertionError(
            f"command failed {' '.join(cmd)}\nSTDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}"
        )
    return cp


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_csv(rel: str) -> list[dict[str, str]]:
    with (PACKAGE_ROOT / rel).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def validate() -> dict[str, object]:
    missing = [rel for rel in REQUIRED_FILES if not (PACKAGE_ROOT / rel).exists()]
    assert not missing, f"missing required files: {missing}"

    receipt = json.loads((PACKAGE_ROOT / 'REPOSITORY_STATE_VERIFICATION_RECEIPT.json').read_text())
    assert receipt['required_starting_protected_head'] == REQUIRED_HEAD
    assert receipt['verified_starting_protected_head'] == REQUIRED_HEAD
    assert receipt['pr62_merge_commit'] == '185d37987c11eccabba4436619bdf11e91494711'
    assert receipt['pr63_custody_merge_commit'] == REQUIRED_HEAD
    assert receipt['open_gaps_total'] == 18
    assert receipt['findings_total'] == 16
    assert receipt['candidate_iwps_total'] == 15
    assert receipt['authorized_iwps_total'] == 0
    assert receipt['protected_merge_authorized'] is False

    for rel in REQUIRED_FILES:
        if rel.endswith('.json'):
            json.loads((PACKAGE_ROOT / rel).read_text())
        if rel.endswith('.csv'):
            rows = read_csv(rel)
            assert rows, f"empty CSV {rel}"

    matrix = read_csv('COPILOT_FINDING_VALIDATION_MATRIX.csv')
    assert len(matrix) == 10, len(matrix)
    assert [r['copilot_lead_id'] for r in matrix] == [f"CGP006-COPILOT-FIND-{i:04d}" for i in range(1, 11)]
    for row in matrix:
        assert row['classification'] in ALLOWED_CLASSIFICATIONS, row
        assert row['reviewed_commit'] == REQUIRED_HEAD, row
        assert row['mapped_gap'], row
        assert row['mapped_iwp'], row
        assert row['validation_requirements'], row
        assert row['rollback_requirements'], row

    dep_rows = read_csv('DEPENDENCY_CLASSIFICATION_INVENTORY.csv')
    moved = {r['package'] for r in dep_rows if r['moved_in_pr2'] == 'YES'}
    assert moved == {'black', 'flake8', 'isort', 'mypy', 'pycodestyle', 'pyflakes', 'pytest'}
    assert all('version change' in r['safety_gate'].lower() or r['moved_in_pr2'] == 'NO' for r in dep_rows)

    peer_rows = read_csv('FRONTEND_PEER_CONFLICT_MATRIX.csv')
    assert any(r['classification'] == 'CONFIRMED_PEER_CONFLICT' for r in peer_rows)
    assert any('FRONTEND_DEPENDENCY_RESOLUTION_PLAN_READY_FOR_SEPARATE_FOUNDER_DISPOSITION' in r['remediation_status'] for r in peer_rows)

    ci_rows = read_csv('CI_ASSURANCE_GAP_ANALYSIS.csv')
    assert any(r['area'] == 'Dependabot' and r['current_status'] == 'MISSING' for r in ci_rows)
    assert any(r['area'] == 'secret scan' and 'report-only' in r['blocking_recommendation'] for r in ci_rows)

    package_text = '\n'.join(
        p.read_text(errors='ignore')
        for p in PACKAGE_ROOT.rglob('*')
        if p.is_file() and p.suffix in {'.md', '.csv', '.json', '.py', '.sha256'}
    )
    for token in REQUIRED_TOKENS:
        assert token in package_text, f"missing token {token}"
    forbidden = [
        'sk_' + 'live_',
        'sk_' + 'test_',
        'BEGIN ' + 'PRIVATE KEY',
        'POTENTIAL_SECRET_EXPOSURE_' + 'REQUIRES_IMMEDIATE_CREDENTIAL_ROTATION_REVIEW',
    ]
    for token in forbidden:
        assert token not in package_text, f"forbidden token {token}"

    checksum_lines = [line.strip().split(None, 1) for line in (PACKAGE_ROOT / 'CHECKSUM_MANIFEST.sha256').read_text().splitlines() if line.strip()]
    checksum_paths = {rel for _, rel in checksum_lines}
    expected_checksum_paths = {rel for rel in REQUIRED_FILES if rel != 'CHECKSUM_MANIFEST.sha256'}
    assert expected_checksum_paths.issubset(checksum_paths)
    for expected_hash, rel in checksum_lines:
        assert sha256(PACKAGE_ROOT / rel) == expected_hash, f"checksum mismatch {rel}"

    run(['git', 'merge-base', '--is-ancestor', REQUIRED_HEAD, 'HEAD'])
    diff_names = run(
        ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'],
        check=False,
    ).stdout.splitlines()
    bad = [p for p in diff_names if p and not p.startswith(AUTHORIZED_PACKAGE_PATH)]
    assert not bad, f"unauthorized committed diff: {bad}"

    return {
        'status': 'PASS',
        'required_files': len(REQUIRED_FILES),
        'copilot_leads': len(matrix),
        'dependency_rows': len(dep_rows),
        'ci_rows': len(ci_rows),
        'authorized_iwps': receipt['authorized_iwps_total'],
    }


if __name__ == '__main__':
    try:
        print(json.dumps(validate(), indent=2, sort_keys=True))
    except Exception as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, indent=2, sort_keys=True))
        sys.exit(1)
