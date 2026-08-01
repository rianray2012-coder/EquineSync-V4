#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, json, sys

ROOT = Path(__file__).resolve().parent
REQUIRED = {
    'README.md',
    'PACKAGE_REVIEW_AND_REVISION_RECORD_V1_0_0.md',
    'REVIEW_FINDINGS_AND_DISPOSITION_MATRIX_V1_0_0.csv',
    'ORIGINAL_PACKAGE_SOURCE_IDENTITY_AND_SUPERSESSION_RECORD_V1_0_0.json',
    'PROPOSED_FOUNDER_IMPLEMENTATION_AUTHORIZATION_AND_SCOPE_DISPOSITION_CGP006_IWP_0002_V1_1_0_2026-07-30.md',
    'CGP_006_IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_IMPLEMENTATION_DIRECTIVE_V1_1_0.md',
    'GUARDIAN_MINOR_SAFEGUARDING_PATCH_CONTRACT_V1_1_0.md',
    'GUARDIAN_MINOR_SECURITY_INVARIANT_AND_WORKFLOW_SPECIFICATION_V1_1_0.md',
    'GUARDIAN_RELATIONSHIP_AUTHORITY_CONSENT_AND_LIFECYCLE_DECISION_RECORD_V1_1_0.md',
    'GUARDIAN_MINOR_WORKFLOW_ENFORCEMENT_MATRIX_V1_1_0.csv',
    'GUARDIAN_MINOR_REGRESSION_AND_ABUSE_CASE_TEST_MATRIX_V1_1_0.csv',
    'GUARDIAN_MINOR_ROLLBACK_SUSPENSION_AND_EVIDENCE_PLAN_V1_1_0.md',
    'FOUNDER_REAPPROVAL_RECORD_CGP006_IWP_0002_V1_1_0_2026-07-30.md',
    'PACKAGE_MANIFEST.json',
    'CHECKSUM_MANIFEST.sha256',
}

def digest(path):
    data=path.read_bytes(); return hashlib.sha256(data).hexdigest(), len(data)

def fail(msg):
    print('FAIL:', msg); sys.exit(1)

missing = REQUIRED - {p.name for p in ROOT.iterdir() if p.is_file()}
if missing: fail(f'missing files: {sorted(missing)}')

manifest=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())
if manifest.get('status') != 'REVIEWED_REVISION_CANDIDATE_PENDING_EXACT_BYTE_FOUNDER_REAPPROVAL':
    fail('manifest status')
for name, meta in manifest['files'].items():
    p=ROOT/name
    if not p.is_file(): fail(f'manifest missing file {name}')
    sha, size=digest(p)
    if sha != meta['sha256'] or size != meta['bytes']:
        fail(f'manifest mismatch {name}')

for line in (ROOT/'CHECKSUM_MANIFEST.sha256').read_text().splitlines():
    if not line.strip(): continue
    sha, name = line.split('  ',1)
    p=ROOT/name
    if not p.is_file(): fail(f'checksum missing file {name}')
    actual,_=digest(p)
    if actual != sha: fail(f'checksum mismatch {name}')

with (ROOT/'GUARDIAN_MINOR_WORKFLOW_ENFORCEMENT_MATRIX_V1_1_0.csv').open(newline='', encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
if len(rows) != 8: fail(f'expected 8 workflows, got {len(rows)}')
workflows={r['workflow'] for r in rows}
if 'document_signature' not in workflows: fail('document_signature missing')
if 'messaging' not in workflows: fail('messaging missing')

with (ROOT/'GUARDIAN_MINOR_REGRESSION_AND_ABUSE_CASE_TEST_MATRIX_V1_1_0.csv').open(newline='', encoding='utf-8') as f:
    tests=list(csv.DictReader(f))
ids=[r['test_id'] for r in tests]
if len(ids) != len(set(ids)): fail('duplicate test IDs')
if len(tests) < 40: fail('insufficient test coverage')
required_terms=['multi-minor','concurr','cache','document','public error','legacy']
blob=' '.join(' '.join(r.values()).lower() for r in tests)
for term in required_terms:
    if term not in blob: fail(f'missing test concept {term}')

control_files = [
'PROPOSED_FOUNDER_IMPLEMENTATION_AUTHORIZATION_AND_SCOPE_DISPOSITION_CGP006_IWP_0002_V1_1_0_2026-07-30.md',
'CGP_006_IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_IMPLEMENTATION_DIRECTIVE_V1_1_0.md',
'GUARDIAN_MINOR_SAFEGUARDING_PATCH_CONTRACT_V1_1_0.md',
'GUARDIAN_MINOR_SECURITY_INVARIANT_AND_WORKFLOW_SPECIFICATION_V1_1_0.md',
'GUARDIAN_RELATIONSHIP_AUTHORITY_CONSENT_AND_LIFECYCLE_DECISION_RECORD_V1_1_0.md',
'GUARDIAN_MINOR_ROLLBACK_SUSPENSION_AND_EVIDENCE_PLAN_V1_1_0.md',
]
for name in control_files:
    text=(ROOT/name).read_text()
    if 'PENDING_EXACT_BYTE_FOUNDER_REAPPROVAL' not in text and 'NOT_EXECUTABLE_UNTIL_EXACT_BYTE_FOUNDER_REAPPROVAL' not in text:
        fail(f'reapproval status missing in {name}')

reapproval=(ROOT/'FOUNDER_REAPPROVAL_RECORD_CGP006_IWP_0002_V1_1_0_2026-07-30.md').read_text()
if 'FOUNDER_REAPPROVAL_NOT_RECORDED' not in reapproval:
    fail('reapproval record must remain pending')

print(f'PASS guardian/minor revision package: {len(manifest["files"])} manifested files, {len(rows)} workflows, {len(tests)} tests')
