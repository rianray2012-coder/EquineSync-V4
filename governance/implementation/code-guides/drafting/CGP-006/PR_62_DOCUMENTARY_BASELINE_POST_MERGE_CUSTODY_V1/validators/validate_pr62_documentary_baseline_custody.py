#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import subprocess

BASE = "1ad6fa436c31316ee192844106ca748cd6dc6d0b"
PR_HEAD = "e61912b673da65556767cd8fb463c9d86debe5ff"
PR62_MERGE = "185d37987c11eccabba4436619bdf11e91494711"
PROTECTED_BRANCH = "integrate-emergent-final-zip"
AUDIT_PATH = pathlib.Path("governance/implementation/code-guides/drafting/CGP-006/REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AND_CURRENT_STATE_GAP_AUDIT_V1")
CUSTODY_PATH = pathlib.Path("governance/implementation/code-guides/drafting/CGP-006/PR_62_DOCUMENTARY_BASELINE_POST_MERGE_CUSTODY_V1")
SOURCE = pathlib.Path("governance/implementation/code-guides/drafting/CGP-006/REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AND_CURRENT_STATE_GAP_AUDIT_V1/COPILOT_REPOSITORY_REVIEW_SOURCE_2026-07-30.txt")
SOURCE_SHA = "cd6e1315615d0f65664485d4ebc2f8906ff4e1f9c0bd19f3b7a6765da026386b"
SOURCE_BYTES = 12416
SOURCE_BLOB = "0d4e81ab45fac4feb77324a3f253f970c79fb803"
REQUIRED_FILES = {
    "README.md",
    "PR_62_FOUNDER_DOCUMENTARY_BASELINE_APPROVAL_RECORD.md",
    "PR_62_PROTECTED_MERGE_RECEIPT.json",
    "PR_62_BASELINE_SOURCE_IDENTITY_REGISTER.csv",
    "PR_62_GAP_FINDING_AND_IWP_CUSTODY_TABLE.csv",
    "PR_62_COPILOT_RECONCILIATION_CUSTODY_RECORD.md",
    "PR_62_COUNT_AND_CLASSIFICATION_RECONCILIATION_RECORD.md",
    "PR_62_NON_AUTHORIZATION_AND_OPEN_STATE_RECORD.md",
    "PR_62_POST_MERGE_PROTECTED_HEAD_RECORD.json",
    "VALIDATION_REPORT.md",
    "AUTHORIZED_PATH_REPORT.md",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validators/validate_pr62_documentary_baseline_custody.py",
    "tests/test_pr62_documentary_baseline_custody.py",
}
NON_AUTHORIZATIONS = ['IMPLEMENTATION_NOT_AUTHORIZED', 'PRODUCT_CODE_CHANGE_NOT_AUTHORIZED', 'DEPENDENCY_CHANGE_NOT_AUTHORIZED', 'LOCKFILE_CHANGE_NOT_AUTHORIZED', 'CI_WORKFLOW_CHANGE_NOT_AUTHORIZED', 'ROOT_README_CHANGE_NOT_AUTHORIZED', 'LICENSE_SELECTION_OR_ADDITION_NOT_AUTHORIZED', 'SCHEMA_OR_MIGRATION_CHANGE_NOT_AUTHORIZED', 'SECRET_SCANNER_SETUP_NOT_AUTHORIZED', 'EXTERNAL_TOOL_SETUP_NOT_AUTHORIZED', 'STRIPE_RUNTIME_TESTING_NOT_AUTHORIZED_BY_THIS_DIRECTIVE', 'STRIPE_KEY_OR_WEBHOOK_CONFIGURATION_NOT_AUTHORIZED', 'DOCUSIGN_CONFIGURATION_NOT_AUTHORIZED', 'DEPLOYMENT_NOT_AUTHORIZED', 'STAGING_NOT_AUTHORIZED', 'PILOT_NOT_AUTHORIZED', 'PRODUCTION_USE_NOT_AUTHORIZED', 'WAVE_2_NOT_AUTHORIZED', 'CGP_007_NOT_AUTHORIZED', 'GAP_CLOSURE_NOT_AUTHORIZED', 'FINDING_CLOSURE_NOT_AUTHORIZED', 'IWP_ACTIVATION_NOT_AUTHORIZED']
TERMINAL = ['PROGRAM_PLAN_V1_1_CONTROLLING', 'PR_62_DOCUMENTARY_BASELINE_APPROVED_AND_ACCESSIONED', 'PR_62_COPILOT_RECONCILIATION_ACCESSIONED', 'PR_62_POST_MERGE_CUSTODY_COMPLETE', 'REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_BASELINE_CUSTODY_COMPLETE', 'ALL_18_GAPS_REMAIN_OPEN', 'ALL_16_FINDINGS_RETAIN_RECORDED_STATUS', 'ALL_15_IWPS_REMAIN_CANDIDATES_ONLY', 'AUTHORIZED_IWPS_TOTAL_0', 'GAP_0004_REMAINS_OPEN', 'MERGE_GATE_NOT_ACTIVE', 'RELEASE_GATE_NOT_ACTIVE', 'OPERATIONS_REFERENCE_NOT_ACTIVE', 'IMPLEMENTATION_NOT_AUTHORIZED', 'PRODUCT_CODE_CHANGE_NOT_AUTHORIZED', 'DEPENDENCY_CHANGE_NOT_AUTHORIZED', 'CI_WORKFLOW_CHANGE_NOT_AUTHORIZED', 'EXTERNAL_TOOL_SETUP_NOT_AUTHORIZED', 'STRIPE_RUNTIME_TESTING_NOT_AUTHORIZED_BY_THIS_DIRECTIVE', 'DEPLOYMENT_NOT_AUTHORIZED', 'STAGING_NOT_AUTHORIZED', 'PILOT_NOT_AUTHORIZED', 'PRODUCTION_USE_NOT_AUTHORIZED', 'WAVE_2_NOT_AUTHORIZED', 'CGP_007_NOT_AUTHORIZED', 'PRIOR_PREFLIGHT_BLOCK_WAS_CORRECT', 'AUTHENTICATED_SOURCE_WHITESPACE_EXCEPTION_APPROVED', 'COPILOT_SOURCE_EXACT_BYTES_PRESERVED', 'COPILOT_SOURCE_SHA256_VERIFIED', 'COPILOT_SOURCE_BYTE_LENGTH_VERIFIED', 'NON_SOURCE_DIFF_CHECK_PASS', 'WHITESPACE_EXCEPTION_NARROWLY_CONTAINED', 'NO_PR_62_AMENDMENT_OCCURRED']

REPO = pathlib.Path(__file__).resolve().parents[7]
PACKAGE_ROOT = REPO / CUSTODY_PATH


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(cmd, cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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


def read_csv(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def assert_checksum_manifest() -> None:
    for raw in (PACKAGE_ROOT / 'CHECKSUM_MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        if not raw.strip():
            continue
        expected, rel = raw.split(None, 1)
        rel = rel.strip()
        actual = sha256(PACKAGE_ROOT / rel)
        assert actual == expected, f"checksum mismatch {rel}"


def validate() -> dict[str, object]:
    missing = sorted(str(p) for p in REQUIRED_FILES if not (PACKAGE_ROOT / p).exists())
    assert not missing, f"missing custody artifacts: {missing}"

    for path in PACKAGE_ROOT.rglob('*.json'):
        json.loads(path.read_text(encoding='utf-8'))
    for path in PACKAGE_ROOT.rglob('*.csv'):
        read_csv(path)
    assert_checksum_manifest()

    receipt = json.loads((PACKAGE_ROOT / 'PR_62_PROTECTED_MERGE_RECEIPT.json').read_text(encoding='utf-8'))
    head_record = json.loads((PACKAGE_ROOT / 'PR_62_POST_MERGE_PROTECTED_HEAD_RECORD.json').read_text(encoding='utf-8'))
    assert receipt['pre_merge_protected_head'] == BASE
    assert receipt['approved_pr_head'] == PR_HEAD
    assert receipt['merge_commit_sha'] == PR62_MERGE
    assert receipt['protected_branch_head_after_merge'] == PR62_MERGE
    assert head_record['protected_head_after_pr62_merge'] == PR62_MERGE
    assert head_record['pr62_head_is_ancestor_of_post_merge_head'] is True

    parents = run(['git', 'show', '--no-patch', '--format=%P', PR62_MERGE]).stdout.strip().split()
    assert parents == [BASE, PR_HEAD], parents
    run(['git', 'merge-base', '--is-ancestor', PR_HEAD, PR62_MERGE])
    run(['git', 'merge-base', '--is-ancestor', PR62_MERGE, 'HEAD'])

    source_bytes = run(['git', 'show', f'{PR_HEAD}:{SOURCE.as_posix()}']).stdout.encode('utf-8')
    assert hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA
    assert len(source_bytes) == SOURCE_BYTES
    assert run(['git', 'rev-parse', f'{PR_HEAD}:{SOURCE.as_posix()}']).stdout.strip() == SOURCE_BLOB
    attrs = run(['git', 'show', f'{PR_HEAD}:{(AUDIT_PATH / ".gitattributes").as_posix()}']).stdout.strip().splitlines()
    assert attrs == ['COPILOT_REPOSITORY_REVIEW_SOURCE_2026-07-30.txt -whitespace']
    run(['git', 'diff', '--check', BASE, PR_HEAD, '--', '.', f':(exclude){SOURCE.as_posix()}'])

    audit_manifest = json.loads((REPO / AUDIT_PATH / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    for item in audit_manifest['files']:
        path = REPO / AUDIT_PATH / item['path']
        assert sha256(path) == item['sha256'], item['path']
        assert path.stat().st_size == item['byte_length'], item['path']
    source_rows = read_csv(PACKAGE_ROOT / 'PR_62_BASELINE_SOURCE_IDENTITY_REGISTER.csv')
    assert any(r['path_or_ref'] == SOURCE.as_posix() and r['sha256'] == SOURCE_SHA and r['byte_length'] == str(SOURCE_BYTES) for r in source_rows)

    custody = read_csv(PACKAGE_ROOT / 'PR_62_GAP_FINDING_AND_IWP_CUSTODY_TABLE.csv')
    gaps = read_csv(REPO / AUDIT_PATH / 'CURRENT_STATE_GAP_REGISTER.csv')
    findings = read_csv(REPO / AUDIT_PATH / 'SECURITY_PRIVACY_AND_SAFEGUARDING_FINDINGS_REGISTER.csv')
    iwps = read_csv(REPO / AUDIT_PATH / 'IMPLEMENTATION_WORK_PACKAGE_CANDIDATE_BACKLOG.csv')
    gap_rows = [r for r in custody if r['record_type'] == 'GAP']
    finding_rows = [r for r in custody if r['record_type'] == 'FINDING']
    iwp_rows = [r for r in custody if r['record_type'] == 'IWP_CANDIDATE']
    assert len(gap_rows) == 18
    assert len(finding_rows) == 16
    assert len(iwp_rows) == 15
    assert all(r['recorded_status'] == 'OPEN' for r in gap_rows)
    assert sorted(r['record_id'] for r in gap_rows) == sorted(r['gap_id'] for r in gaps)
    assert {r['recorded_status'] for r in finding_rows} == {r['status'] for r in findings}
    assert sorted(r['record_id'] for r in finding_rows) == sorted(r['finding_id'] for r in findings)
    assert all(r['recorded_status'] == 'IMPLEMENTATION_NOT_AUTHORIZED' for r in iwp_rows)
    assert sorted(r['record_id'] for r in iwp_rows) == sorted(r['work_package_id'] for r in iwps)
    assert sum(1 for r in gap_rows if r['severity'] == 'P1_HIGH') == 5
    assert sum(1 for r in gap_rows if r['severity'] == 'P2_MEDIUM') == 11
    assert sum(1 for r in gap_rows if r['severity'] == 'P3_LOW') == 2
    assert sum(1 for r in finding_rows if r['severity'] == 'P1_HIGH') == 5
    assert sum(1 for r in finding_rows if r['severity'] == 'P2_MEDIUM') == 8
    assert sum(1 for r in finding_rows if r['severity'] == 'P3_LOW') == 2
    assert sum(1 for r in finding_rows if r['severity'] == 'OBSERVATION') == 1

    gap_0011 = next(r for r in gaps if r['gap_id'] == 'CGP006-MAP-GAP-0011')
    expanded_text = ' '.join(gap_0011.values()).lower()
    for token in ['lint', 'format', 'type', 'sast', 'secret', 'license', 'dependency-audit']:
        assert token in expanded_text, token
    for gap_id in [f'CGP006-MAP-GAP-{i:04d}' for i in range(13, 19)]:
        assert any(r['record_id'] == gap_id for r in gap_rows), gap_id

    package_text = '\n'.join(
        p.read_text(encoding='utf-8', errors='ignore') for p in PACKAGE_ROOT.rglob('*') if p.is_file()
    )
    for token in TERMINAL + NON_AUTHORIZATIONS:
        assert token in package_text, token
    assert 'MACHINE_ASSISTED_REVIEW_NON_INDEPENDENCE' in package_text or 'Machine-assisted review remains non-independent' in package_text

    changed = run(['git', 'diff', '--name-only', PR62_MERGE, 'HEAD'], check=False).stdout.splitlines()
    bad = [p for p in changed if p and not p.startswith(CUSTODY_PATH.as_posix() + '/')]
    assert not bad, bad
    status = run(['git', 'status', '--short', '--untracked-files=all'], check=False).stdout.splitlines()
    bad_status = []
    for line in status:
        path = line[3:].strip()
        if ' -> ' in path:
            path = path.split(' -> ', 1)[1]
        if path and not path.startswith(CUSTODY_PATH.as_posix() + '/'):
            bad_status.append(line)
    assert not bad_status, bad_status
    run(['git', 'diff', '--check', PR62_MERGE, 'HEAD'])

    manifest = json.loads((PACKAGE_ROOT / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    assert manifest['package_id'] == 'ES-CGP-006-PR62-DOCUMENTARY-BASELINE-POST-MERGE-CUSTODY-V1'
    return {
        'status': 'PASS',
        'required_artifacts': len(REQUIRED_FILES),
        'source_identity_rows': len(source_rows),
        'gap_rows': len(gap_rows),
        'finding_rows': len(finding_rows),
        'candidate_iwp_rows': len(iwp_rows),
        'authorized_iwps': sum(1 for r in iwp_rows if r['recorded_status'] != 'IMPLEMENTATION_NOT_AUTHORIZED'),
        'pr62_merge_commit': PR62_MERGE,
    }


def main() -> int:
    try:
        result = validate()
    except Exception as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, indent=2))
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
