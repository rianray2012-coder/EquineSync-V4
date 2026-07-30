#!/usr/bin/env python3
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED = [
    'README.md',
    'FOUNDER_REVIEW_AND_DISPOSITION_PACKET.md',
    'DIRECTIVE_AUTHORITY_RECORD.md',
    'POST_MERGE_CUSTODY_LEDGER.csv',
    'REPOSITORY_AND_PR_AUTHENTICATION_RECORD.json',
    'PR64_DOCUMENTARY_REVIEW.md',
    'PR65_TECHNICAL_REVIEW.md',
    'PR66_DEPENDENCY_CLASSIFICATION_AND_VALIDATION_REVIEW.md',
    'PR67_CI_PERMISSIONS_DEPENDABOT_REPORTING_REVIEW.md',
    'CROSS_PR_INTERACTION_AND_SEQUENCE_ANALYSIS.md',
    'FINDINGS_TO_REMEDIATION_TRACEABILITY_MATRIX.csv',
    'FOUNDER_DECISION_MATRIX.csv',
    'RETAINED_RISKS_AND_NON_AUTHORIZATIONS.md',
    'VALIDATION_RECORD.md',
    'PACKAGE_MANIFEST.json',
    'CHECKSUM_MANIFEST.sha256',
    'validators/validate_founder_review_packet.py',
    'tests/test_founder_review_packet.py',
]
REQUIRED_STATEMENTS = [
    'NO_DIRECT_PROTECTED_BRANCH_PUSH',
    'PR_64_66_POST_MERGE_CUSTODY_RECONCILED',
    'PR_67_MERGE_NOT_AUTHORIZED',
    'PR_68_MERGE_NOT_AUTHORIZED',
    'NO_FOUNDER_DECISION_RECORDED',
    'NO_FINDING_OR_GAP_CLOSED',
    'NO_CLEAN_STATIC_ANALYSIS_CLAIM',
    'NO_EXISTING_STATIC_FINDING_REMEDIATION_AUTHORIZED',
    'NO_DEPENDENCY_VERSION_UPGRADE_AUTHORIZED',
    'NO_BROAD_LOCKFILE_REGENERATION_AUTHORIZED',
    'NO_BRANCH_PROTECTION_CHANGE_AUTHORIZED',
    'NO_EXTERNAL_SCANNER_CONFIGURATION_AUTHORIZED',
    'NO_DEPLOYMENT_CONFIGURATION_CHANGE_AUTHORIZED',
    'NO_SECRET_DISCLOSURE_AUTHORIZED',
    'NO_IWP_ACTIVATION_AUTHORIZED',
    'NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED',
    'PRODUCTION_USE_NOT_AUTHORIZED',
]
ALLOWED_DISPOSITIONS = {
    'PARTIALLY_ADDRESSED',
    'DOCUMENTED_BUT_NOT_REMEDIATED',
    'INTENTIONALLY_DEFERRED',
}
PR_DISPOSITIONS = {
    '64': 'MERGED_UNDER_AUTHENTICATED_DIRECTIVE_POST_MERGE_CUSTODY_VALIDATED',
    '65': 'MERGED_UNDER_AUTHENTICATED_DIRECTIVE_POST_MERGE_CUSTODY_VALIDATED',
    '66': 'MERGED_UNDER_AUTHENTICATED_DIRECTIVE_POST_MERGE_CUSTODY_VALIDATED',
    '67': 'CORRECTIONS_VERIFIED_READY_FOR_FOUNDER_DISPOSITION',
}

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()

def fail(msg):
    print(json.dumps({'status': 'FAIL', 'error': msg}, indent=2))
    sys.exit(1)

def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    root = root.resolve()
    for rel in REQUIRED:
        if not (root / rel).is_file():
            fail(f'missing required file: {rel}')

    manifest = json.loads((root / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    record = json.loads((root / 'REPOSITORY_AND_PR_AUTHENTICATION_RECORD.json').read_text(encoding='utf-8'))
    if record.get('repository') != 'rianray2012-coder/EquineSync-V4':
        fail('repository mismatch')
    if record.get('verified_protected_head') != '9996e948ede39a968b8facd8afe15c2b1a345204':
        fail('protected head mismatch in authentication record')
    if record.get('starting_protected_head') != '396f82c8a7600cae363142175d1d1448e9d2ece2':
        fail('starting protected head mismatch')
    if record.get('authority_result') != 'PR_64_66_MERGES_AND_PR_67_CORRECTION_AUTHENTICATED_AS_DIRECTIVE_AUTHORIZED':
        fail('authority result mismatch')
    if record.get('repository_drift_detected') is not False:
        fail('repository drift flag must be false for this packet')
    if record.get('reviewed_prs', {}).get('67', {}).get('corrected_head') != '76842397debf37780bea850933b1102779e2b502':
        fail('PR #67 corrected head mismatch')

    all_text = '\n'.join(
        p.read_text(encoding='utf-8', errors='ignore')
        for p in root.rglob('*')
        if p.is_file() and p.suffix in {'.md', '.csv', '.json', '.py', '.sha256'}
    )
    for statement in REQUIRED_STATEMENTS:
        if statement not in all_text:
            fail(f'missing continuing statement: {statement}')
    for disposition in PR_DISPOSITIONS.values():
        if disposition not in all_text:
            fail(f'missing PR disposition: {disposition}')

    with (root / 'FINDINGS_TO_REMEDIATION_TRACEABILITY_MATRIX.csv').open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 10:
        fail(f'expected 10 finding rows, found {len(rows)}')
    for row in rows:
        if row.get('finding_closed') != 'NO':
            fail('a finding was marked closed')
        if row.get('current_disposition') not in ALLOWED_DISPOSITIONS:
            fail(f"invalid disposition {row.get('current_disposition')}")

    with (root / 'FOUNDER_DECISION_MATRIX.csv').open(newline='', encoding='utf-8') as f:
        decision_rows = list(csv.DictReader(f))
    if len(decision_rows) != 4:
        fail(f'expected 4 founder decision rows, found {len(decision_rows)}')
    for row in decision_rows:
        if row.get('founder_decision') != 'NO_FOUNDER_DECISION_RECORDED':
            fail('Founder decision field was executed or changed')
        if row.get('recommendation_self_executing') != 'NO':
            fail('recommendation self-executing flag must be NO')
    pr67 = next(row for row in decision_rows if row.get('pr_number') == '67')
    for option in [
        'FOUNDER_APPROVES_PR_67_FOR_CONTROLLED_MERGE',
        'FOUNDER_APPROVES_PR_67_WITH_MANDATORY_CORRECTIONS',
        'FOUNDER_HOLDS_PR_67_PENDING_ADDITIONAL_EVIDENCE',
        'FOUNDER_REJECTS_PR_67',
        'NO_FOUNDER_DECISION_RECORDED',
    ]:
        if option not in pr67.get('founder_decision_options', ''):
            fail(f'missing PR #67 Founder option: {option}')

    with (root / 'POST_MERGE_CUSTODY_LEDGER.csv').open(newline='', encoding='utf-8') as f:
        custody_rows = list(csv.DictReader(f))
    if len(custody_rows) != 4:
        fail(f'expected 4 custody rows, found {len(custody_rows)}')
    for row in custody_rows:
        expected = PR_DISPOSITIONS.get(row.get('pr_number'))
        if row.get('disposition') != expected:
            fail(f"custody disposition mismatch for PR #{row.get('pr_number')}")
        if row.get('founder_decision') != 'NO_FOUNDER_DECISION_RECORDED':
            fail('custody ledger founder decision was executed')

    checksum_rows = []
    with (root / 'CHECKSUM_MANIFEST.sha256').open(encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            digest, rel = line.split('  ', 1)
            checksum_rows.append((digest, rel))
            if rel == 'CHECKSUM_MANIFEST.sha256':
                fail('checksum manifest must not include itself')
            if sha256(root / rel) != digest:
                fail(f'checksum mismatch: {rel}')
    manifest_files = manifest.get('files', {})
    for rel, meta in manifest_files.items():
        if rel == 'CHECKSUM_MANIFEST.sha256':
            continue
        if sha256(root / rel) != meta.get('sha256'):
            fail(f'manifest hash mismatch: {rel}')
    checksum_file_set = sorted(rel for _, rel in checksum_rows)
    expected_checksum_set = sorted(set(manifest_files) | {'PACKAGE_MANIFEST.json'})
    if checksum_file_set != expected_checksum_set:
        fail('checksum manifest and package manifest file sets differ')

    strong_secret_patterns = [
        re.compile(r'AKIA[0-9A-Z]{16}'),
        re.compile(r'\b[prsk]k_(?:live|test)_[A-Za-z0-9]{16,}'),
        re.compile(r'BEGIN [A-Z ]*PRIVATE KEY'),
    ]
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        for pat in strong_secret_patterns:
            if pat.search(text):
                fail(f'strong secret-shaped value found in {path.relative_to(root)}')

    print(json.dumps({
        'status': 'PASS',
        'required_files': len(REQUIRED),
        'finding_rows': len(rows),
        'founder_decision_rows': len(decision_rows),
        'custody_rows': len(custody_rows),
        'checksum_rows': len(checksum_rows),
        'protected_head': record.get('verified_protected_head'),
        'authority_result': record.get('authority_result'),
        'completion_token': record.get('completion_token'),
    }, indent=2))

if __name__ == '__main__':
    main()
