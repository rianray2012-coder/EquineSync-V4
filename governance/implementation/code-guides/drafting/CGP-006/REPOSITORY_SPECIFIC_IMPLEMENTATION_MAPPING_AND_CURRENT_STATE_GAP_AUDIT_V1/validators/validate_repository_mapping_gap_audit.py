
from __future__ import annotations

import csv
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

EXPECTED_BASE = "1ad6fa436c31316ee192844106ca748cd6dc6d0b"
AUTHORIZED_PACKAGE_PATH = "governance/implementation/code-guides/drafting/CGP-006/REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AND_CURRENT_STATE_GAP_AUDIT_V1/"
PROFILE = "governance/implementation/code-guides/profiles/ES-CODE-GUIDE-SOLO-FOUNDER-COMPENSATING-ASSURANCE-PROFILE-V1.0.0.md"
PROFILE_SHA = "ef82faf0af5f33182014b75b35a59fbee25596f4ea1a5da52378de3ed54d2c2b"
PROFILE_BYTES = 9681
GUIDES = {
    "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-00/ES-CG-00_V1_1_ADOPTION_CANDIDATE.md": ("2275ca1b9674b4e05390f134470a37e7ee63ca423705b6579b1bc8eef874f0c1", 2986),
    "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-01/ES-CG-01_V1_1_ADOPTION_CANDIDATE.md": ("e35ea6b9031bd4c727852b124ef9968fe0ef30afbc4e83efabd270f18248e9e6", 3008),
    "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-10/ES-CG-10_V1_1_ADOPTION_CANDIDATE.md": ("435eb4940da15e6ffbbd66bbc207a05b4fa3ffd3405ff436a8ca15950dfd32c7", 3250),
    "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-13/ES-CG-13_V1_1_ADOPTION_CANDIDATE.md": ("bf79a3762625bfaaa3ebbd4c446c460ab6a60ff9bbd264d2f4b9e9cdb55305e9", 3227),
}
MANDATORY_ARTIFACTS = [
    "README.md",
    "WORKSTREAM_CHARTER.md",
    "REPOSITORY_SNAPSHOT_AND_SOURCE_FREEZE_RECORD.json",
    "SOURCE_REGISTER.md",
    "SOURCE_AUTHORITY_MATRIX.csv",
    "REPOSITORY_ARCHITECTURE_INVENTORY.md",
    "REPOSITORY_COMPONENT_INVENTORY.csv",
    "DATA_FLOW_AND_TRUST_BOUNDARY_MAP.md",
    "CODE_GUIDE_REQUIREMENT_TO_REPOSITORY_TRACEABILITY_MATRIX.csv",
    "PIA_AND_FOUNDER_DECISION_TO_REPOSITORY_TRACEABILITY_MATRIX.csv",
    "AUTHENTICATION_AUTHORIZATION_TENANCY_AND_SUPPORT_ACCESS_MATRIX.csv",
    "GUARDIAN_MINOR_SAFEGUARDING_CONTROL_MAP.csv",
    "DATA_SCHEMA_MIGRATION_AND_STATE_INVENTORY.csv",
    "TEST_CI_AND_EVIDENCE_INVENTORY.csv",
    "EXTERNAL_INTEGRATION_AND_ASSURANCE_TOOLING_INVENTORY.csv",
    "GAP_0004_DECOMPOSITION_AND_EVIDENCE_PLAN.md",
    "CURRENT_STATE_GAP_REGISTER.csv",
    "SECURITY_PRIVACY_AND_SAFEGUARDING_FINDINGS_REGISTER.csv",
    "ASSUMPTION_INFERENCE_AND_UNRESOLVED_QUESTION_REGISTER.csv",
    "IMPLEMENTATION_WORK_PACKAGE_CANDIDATE_BACKLOG.csv",
    "IMPLEMENTATION_SEQUENCE_AND_DEPENDENCY_MAP.md",
    "FOUNDER_IMPLEMENTATION_AUTHORIZATION_DECISION_PACKET.md",
    "VALIDATION_REPORT.md",
    "AUTHORIZED_PATH_REPORT.md",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validators/validate_repository_mapping_gap_audit.py",
    "tests/test_repository_mapping_gap_audit.py",
]

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[5]


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(cmd, cwd=REPO_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and cp.returncode != 0:
        raise AssertionError(f"command failed {' '.join(cmd)}\nSTDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}")
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


def normalize_repo_path(value: str) -> str | None:
    value = (value or '').strip().strip('`')
    if not value or value in {'NONE', 'DIRECTIVE', 'VALIDATION_REPORT.md'}:
        return None
    value = value.split('#', 1)[0]
    value = re.sub(r':\d+(?:-\d+)?$', '', value)
    if value.startswith(str(REPO_ROOT)):
        value = str(pathlib.Path(value).relative_to(REPO_ROOT))
    if value.startswith('/'):
        return None
    if value.startswith(AUTHORIZED_PACKAGE_PATH):
        return None
    candidate = REPO_ROOT / value
    return value if candidate.exists() and candidate.is_file() else None


def assert_hash_size(rel: str, expected_hash: str, expected_size: int) -> None:
    p = REPO_ROOT / rel
    assert p.exists(), f"missing {rel}"
    assert p.stat().st_size == expected_size, f"size mismatch {rel}"
    assert sha256(p) == expected_hash, f"sha mismatch {rel}"


def validate() -> dict[str, object]:
    result: dict[str, object] = {"status": "PASS"}

    # 1. Protected source snapshot.
    run(['git', 'cat-file', '-e', f'{EXPECTED_BASE}^{{commit}}'])
    run(['git', 'merge-base', '--is-ancestor', EXPECTED_BASE, 'HEAD'])
    snapshot = json.loads((PACKAGE_ROOT / 'REPOSITORY_SNAPSHOT_AND_SOURCE_FREEZE_RECORD.json').read_text())
    assert snapshot['required_protected_head'] == EXPECTED_BASE
    assert snapshot['verified_protected_head'] == EXPECTED_BASE

    # 2-3. Active profile and guide identities.
    assert_hash_size(PROFILE, PROFILE_SHA, PROFILE_BYTES)
    for rel, (expected_hash, expected_size) in GUIDES.items():
        assert_hash_size(rel, expected_hash, expected_size)

    # 4. Mandatory artifacts.
    missing = [rel for rel in MANDATORY_ARTIFACTS if not (PACKAGE_ROOT / rel).exists()]
    assert not missing, f"missing artifacts: {missing}"

    # 5. CSV and JSON parse.
    for p in PACKAGE_ROOT.rglob('*.csv'):
        with p.open(newline='', encoding='utf-8') as f:
            list(csv.DictReader(f))
    for p in PACKAGE_ROOT.rglob('*.json'):
        json.loads(p.read_text(encoding='utf-8'))

    # 6-7. Requirement mappings have source and evidence; implemented-and-evidenced rows have both evidence classes.
    mappings = read_csv('CODE_GUIDE_REQUIREMENT_TO_REPOSITORY_TRACEABILITY_MATRIX.csv')
    assert mappings, 'no mapping rows'
    for row in mappings:
        assert row.get('source_citation'), f"missing source {row}"
        assert row.get('evidence_classification'), f"missing evidence classification {row}"
        if row.get('current_state_classification') == 'IMPLEMENTED_AND_EVIDENCED':
            assert row.get('implementation_evidence'), row
            assert row.get('verification_evidence'), row

    # 8. Cited file identities.
    identity_rows = read_csv('CITED_REPOSITORY_FILE_IDENTITIES.csv')
    identities = {r['path']: r for r in identity_rows}
    cited: set[str] = set()
    for rel in [
        'CODE_GUIDE_REQUIREMENT_TO_REPOSITORY_TRACEABILITY_MATRIX.csv',
        'PIA_AND_FOUNDER_DECISION_TO_REPOSITORY_TRACEABILITY_MATRIX.csv',
        'AUTHENTICATION_AUTHORIZATION_TENANCY_AND_SUPPORT_ACCESS_MATRIX.csv',
        'GUARDIAN_MINOR_SAFEGUARDING_CONTROL_MAP.csv',
        'DATA_SCHEMA_MIGRATION_AND_STATE_INVENTORY.csv',
        'TEST_CI_AND_EVIDENCE_INVENTORY.csv',
        'EXTERNAL_INTEGRATION_AND_ASSURANCE_TOOLING_INVENTORY.csv',
        'CURRENT_STATE_GAP_REGISTER.csv',
        'SECURITY_PRIVACY_AND_SAFEGUARDING_FINDINGS_REGISTER.csv',
        'IMPLEMENTATION_WORK_PACKAGE_CANDIDATE_BACKLOG.csv',
    ]:
        for row in read_csv(rel):
            for value in row.values():
                for token in re.split(r'[;|]', value or ''):
                    norm = normalize_repo_path(token)
                    if norm:
                        cited.add(norm)
    missing_identities = sorted(c for c in cited if c not in identities)
    assert not missing_identities, f"missing cited identities: {missing_identities[:20]}"
    for path, row in identities.items():
        p = REPO_ROOT / path
        assert p.exists(), f"identity path missing {path}"
        assert sha256(p) == row['sha256'], f"identity sha mismatch {path}"
        assert str(p.stat().st_size) == row['byte_length'], f"identity size mismatch {path}"

    # 9. Inferences labeled.
    assumption_rows = read_csv('ASSUMPTION_INFERENCE_AND_UNRESOLVED_QUESTION_REGISTER.csv')
    assert assumption_rows, 'missing assumptions'
    assert all(r.get('label') == 'INFERENCE_REQUIRES_CONFIRMATION' for r in assumption_rows), 'unlabeled inference row'
    package_text = '\n'.join(p.read_text(errors='ignore') for p in PACKAGE_ROOT.rglob('*.md'))
    assert 'INFERENCE_REQUIRES_CONFIRMATION' in package_text

    # 10-11. No gap closed, GAP_0004 open.
    gaps = read_csv('CURRENT_STATE_GAP_REGISTER.csv')
    assert gaps, 'missing gaps'
    for row in gaps:
        assert 'CLOSED' not in row.get('status', ''), row
    assert 'GAP_0004_REMAINS_OPEN' in package_text
    assert 'GAP_0004_CLOSED' not in (PACKAGE_ROOT / 'GAP_0004_DECOMPOSITION_AND_EVIDENCE_PLAN.md').read_text().replace('GAP_0004_CLOSED_PROHIBITED', '')

    # 12. All P0/P1 findings in Founder packet.
    findings = read_csv('SECURITY_PRIVACY_AND_SAFEGUARDING_FINDINGS_REGISTER.csv')
    packet = (PACKAGE_ROOT / 'FOUNDER_IMPLEMENTATION_AUTHORIZATION_DECISION_PACKET.md').read_text()
    for row in findings:
        if row.get('severity') in {'P0_CRITICAL', 'P1_HIGH'}:
            assert row['finding_id'] in packet, f"P0/P1 finding absent from packet {row['finding_id']}"

    # 13. Candidate packages keep implementation unauthorized.
    for row in read_csv('IMPLEMENTATION_WORK_PACKAGE_CANDIDATE_BACKLOG.csv'):
        joined = ' '.join(row.values())
        assert 'IMPLEMENTATION_NOT_AUTHORIZED' in joined, row

    # 14. No external tool newly configured.
    for row in read_csv('EXTERNAL_INTEGRATION_AND_ASSURANCE_TOOLING_INVENTORY.csv'):
        assert 'NEWLY_CONFIGURED' not in ' '.join(row.values()).upper(), row
    assert 'NO_EXTERNAL_TOOL_CONNECTED_OR_CONFIGURED' in package_text

    # 15. No changed tracked/untracked file outside authorized package path.
    status = run(['git', 'status', '--short', '--untracked-files=all']).stdout.splitlines()
    bad = []
    for line in status:
        path = line[3:].strip()
        if ' -> ' in path:
            path = path.split(' -> ', 1)[1]
        if path and not path.startswith(AUTHORIZED_PACKAGE_PATH):
            bad.append(line)
    assert not bad, f"unauthorized worktree changes: {bad}"
    diff_names = run(['git', 'diff', '--name-only', f'{EXPECTED_BASE}..HEAD'], check=False).stdout.splitlines()
    bad_diff = [p for p in diff_names if p and not p.startswith(AUTHORIZED_PACKAGE_PATH)]
    assert not bad_diff, f"unauthorized committed diff: {bad_diff}"

    # 16-23. Status boundaries and active scopes.
    program_status = (REPO_ROOT / 'governance/implementation/code-guides/PROGRAM_STATUS.md').read_text()
    for token in [
        'ACTIVE_LIMITED_STAGE_24_FOR_PLANNING_REFERENCE_IMPLEMENTATION_CONTROL_AND_PULL_REQUEST_REVIEW_ONLY',
        'MERGE_GATE_NOT_ACTIVE',
        'RELEASE_GATE_NOT_ACTIVE',
        'OPERATIONS_REFERENCE_NOT_ACTIVE',
        'IMPLEMENTATION_NOT_AUTHORIZED',
        'DEPLOYMENT_NOT_AUTHORIZED',
        'PILOT_NOT_AUTHORIZED',
        'WAVE_2_NOT_AUTHORIZED',
        'CGP_007_NOT_AUTHORIZED',
    ]:
        assert token in program_status or token in package_text, f"missing token {token}"
    assert 'PRODUCTION_USE_NOT_AUTHORIZED' in package_text
    assert 'STAGING_NOT_AUTHORIZED' in package_text

    # 24. Checksum and manifest integrity.
    manifest = json.loads((PACKAGE_ROOT / 'PACKAGE_MANIFEST.json').read_text())
    assert manifest['package_id']
    checksum_lines = [line.strip().split(None, 1) for line in (PACKAGE_ROOT / 'CHECKSUM_MANIFEST.sha256').read_text().splitlines() if line.strip()]
    for expected_hash, rel in checksum_lines:
        rel = rel.strip()
        assert sha256(PACKAGE_ROOT / rel) == expected_hash, f"checksum mismatch {rel}"

    # 25. git diff --check.
    run(['git', 'diff', '--check', EXPECTED_BASE])

    result.update({
        'mandatory_artifacts': len(MANDATORY_ARTIFACTS),
        'mapping_rows': len(mappings),
        'gap_rows': len(gaps),
        'finding_rows': len(findings),
        'cited_file_identities': len(identity_rows),
    })
    return result


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
