#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

DIRECTIVE_ID = "CGP_006_SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_AND_STAGE_24_READINESS_REBASE_DIRECTIVE_V1_0_0"
START_HEAD = "150b24d65d25f79255959ee07a185e7b04601bcf"
PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_AND_STAGE_24_READINESS_REBASE_V1")
DETERMINATION_PATH = Path("governance/implementation/code-guides/founder-determinations/ES-FD-SOLO-FOUNDER-COMPENSATING-ASSURANCE-2026-07-29/FOUNDER_DETERMINATION_SOLO_FOUNDER_COMPENSATING_ASSURANCE_MODEL_2026-07-29.md")
DETERMINATION_SHA = "e777598974887456f22bfc77d8db6c9a235502fc552fb28ce6ff52a77ca3fb61"
DETERMINATION_BYTES = 29240
REQUIRED_GUIDES = {
    "ES-CG-00": {"sha256": "2275ca1b9674b4e05390f134470a37e7ee63ca423705b6579b1bc8eef874f0c1", "byte_length": 2986, "path": "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-00/ES-CG-00_V1_1_ADOPTION_CANDIDATE.md"},
    "ES-CG-01": {"sha256": "e35ea6b9031bd4c727852b124ef9968fe0ef30afbc4e83efabd270f18248e9e6", "byte_length": 3008, "path": "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-01/ES-CG-01_V1_1_ADOPTION_CANDIDATE.md"},
    "ES-CG-10": {"sha256": "435eb4940da15e6ffbbd66bbc207a05b4fa3ffd3405ff436a8ca15950dfd32c7", "byte_length": 3250, "path": "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-10/ES-CG-10_V1_1_ADOPTION_CANDIDATE.md"},
    "ES-CG-13": {"sha256": "bf79a3762625bfaaa3ebbd4c446c460ab6a60ff9bbd264d2f4b9e9cdb55305e9", "byte_length": 3227, "path": "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-13/ES-CG-13_V1_1_ADOPTION_CANDIDATE.md"},
}
REQUIRED_FILES = ['README.md', 'WORKSTREAM_CHARTER.md', 'SOURCE_REGISTER.md', 'SOURCE_FREEZE_MANIFEST.json', 'SOURCE_SHA256SUMS.txt', 'SOURCE_AUTHORITY_MATRIX.csv', 'ES-CODE-GUIDE-SOLO-FOUNDER-COMPENSATING-ASSURANCE-PROFILE-V1.0.0_CANDIDATE.md', 'FOUNDER_QUALIFICATION_AND_NON_INDEPENDENCE_DISCLOSURE.md', 'FOUNDER_DOMAIN_OWNER_REVIEW_INSTRUMENT.md', 'FOUNDER_DOMAIN_OWNER_REVIEW_RECORD.md', 'FOUNDER_TECHNICAL_GOVERNANCE_REVIEW_PROTOCOL.md', 'FOUNDER_TECHNICAL_GOVERNANCE_REVIEW_RECORD.md', 'PASS_A_AUTHORITY_AND_SOURCE_FIDELITY_REVIEW.md', 'PASS_B_ARCHITECTURE_AND_IMPLEMENTABILITY_REVIEW.md', 'PASS_C_SECURITY_TENANCY_PRIVACY_AND_SAFEGUARDING_REVIEW.md', 'PASS_D_TESTABILITY_VERIFICATION_AND_EVIDENCE_REVIEW.md', 'PASS_E_FAILURE_RECOVERY_AND_OPERATIONAL_RELIABILITY_REVIEW.md', 'PASS_F_CLEAN_ROOM_IMPLEMENTER_USABILITY_REVIEW.md', 'PASS_G_CROSS_GUIDE_RECONCILIATION_REVIEW.md', 'PASS_H_ADVERSARIAL_AND_RED_TEAM_REVIEW.md', 'MULTI_PASS_REVIEW_RECONCILIATION_REPORT.md', 'WAVE_1_FINDING_TREATMENT_MATRIX.csv', 'RETAINED_CONDITION_WARNING_GAP_AND_BLOCKER_MATRIX.csv', 'WAVE_1_STAGE_24_READINESS_MATRIX.csv', 'WAVE_1_STAGE_24_READINESS_REPORT.md', 'PROPOSED_STAGE_24_ACTIVATION_SCOPE_MATRIX.csv', 'SOLO_FOUNDER_ASSURANCE_RESIDUAL_RISK_REGISTER.csv', 'FOUNDER_STAGE_24_LIMITED_ACTIVATION_DECISION_PACKET.md', 'AUTHORIZED_PATH_REPORT.md', 'DIRECTIVE_EXECUTION_RECORD.md', 'VALIDATION_REPORT.md', 'PACKAGE_MANIFEST.json', 'CHECKSUM_MANIFEST.sha256', 'validators/validate_solo_founder_assurance_stage24_readiness.py', 'tests/test_solo_founder_assurance_stage24_readiness.py']
REQUIRED_CLOSING = ['PROGRAM_PLAN_V1_1_CONTROLLING', 'SOLO_FOUNDER_COMPENSATING_ASSURANCE_DETERMINATION_CONTROLLING', 'FOUNDER_SOLO_COMPENSATING_ASSURANCE_MODEL_APPLIES', 'EQUINESYNC_IS_A_SOLO_FOUNDER_PROJECT', 'FOUNDER_DOMAIN_OWNER_REVIEW_IS_NOT_INDEPENDENT', 'FOUNDER_TECHNICAL_GOVERNANCE_REVIEW_IS_NOT_INDEPENDENT', 'MACHINE_ASSISTED_REVIEW_IS_NOT_INDEPENDENT_HUMAN_REVIEW', 'NO_INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PERFORMED', 'NO_THIRD_PARTY_TECHNICAL_CERTIFICATION_CLAIMED', 'NO_THIRD_PARTY_DOMAIN_CERTIFICATION_CLAIMED', 'OBJECTIVE_TEST_AND_EVIDENCE_GATES_REQUIRED', 'FOUNDER_RESIDUAL_RISK_ACCEPTANCE_REQUIRED', 'GAP_0004_REMAINS_OPEN', 'NO_SILENT_FINDING_CLOSURE', 'NO_SILENT_WARNING_CLOSURE', 'NO_SILENT_CONDITION_CLOSURE', 'STAGE_24_GUIDE_ACTIVATION_NOT_AUTHORIZED', 'ES_CG_00_REMAINS_NOT_ACTIVE', 'ES_CG_01_REMAINS_NOT_ACTIVE', 'ES_CG_10_REMAINS_NOT_ACTIVE', 'ES_CG_13_REMAINS_NOT_ACTIVE', 'NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED', 'REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED', 'IMPLEMENTATION_NOT_AUTHORIZED', 'DEPLOYMENT_NOT_AUTHORIZED', 'PILOT_NOT_AUTHORIZED', 'PRODUCTION_NOT_AUTHORIZED', 'WAVE_2_NOT_AUTHORIZED', 'CGP_007_NOT_AUTHORIZED', 'DRAFT_PR_OPEN_UNMERGED_PENDING_FOUNDER_STAGE_24_DISPOSITION']
BAD_AUTHORITY_TOKENS = [
    "SOLO_FOUNDER_ASSURANCE_PROFILE_ADOPTED",
    "SOLO_FOUNDER_ASSURANCE_PROFILE_PROTECTED_ACCESSIONED",
    "SOLO_FOUNDER_ASSURANCE_PROFILE_CUSTODY_COMPLETE",
    "STAGE_24_GUIDE_ACTIVATION_AUTHORIZED",
    "ANY_GUIDE_ACTIVE_STATUS",
    "ACTIVATION_EFFECTIVE_DATE_ESTABLISHED",
    "IMPLEMENTATION_CONTROL_ACTIVATION_AUTHORIZED",
    "PULL_REQUEST_REVIEW_ACTIVATION_AUTHORIZED",
    "MERGE_GATE_ACTIVATION_AUTHORIZED",
    "RELEASE_GATE_ACTIVATION_AUTHORIZED",
    "OPERATIONS_REFERENCE_ACTIVATION_AUTHORIZED",
    "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AUTHORIZED",
    "IMPLEMENTATION_AUTHORIZED",
    "DEPLOYMENT_AUTHORIZED",
    "STAGING_USE_AUTHORIZED",
    "PILOT_AUTHORIZED",
    "PRODUCTION_AUTHORIZED",
    "GAP_0004_CLOSED",
    "CANONICAL_FINDING_STATUS_CHANGED",
    "CANONICAL_WARNING_STATUS_CHANGED",
    "CANONICAL_CONDITION_STATUS_CHANGED",
    "INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PERFORMED",
    "THIRD_PARTY_TECHNICAL_CERTIFICATION_CLAIMED",
    "THIRD_PARTY_DOMAIN_CERTIFICATION_CLAIMED",
    "IMPLEMENTATION_EVIDENCE_EXISTS",
    "RUNTIME_EVIDENCE_EXISTS",
]

class ValidationError(Exception):
    pass

def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def package_dir(root: Path, override: Path | None = None) -> Path:
    return override if override is not None else root / PACKAGE_REL

def check_authorized_paths(paths: list[str]) -> None:
    prefix = PACKAGE_REL.as_posix() + "/"
    outside = [p for p in paths if p and not p.startswith(prefix)]
    if outside:
        raise ValidationError(f"files outside authorized package path changed: {outside}")

def git_changed_paths(root: Path) -> list[str]:
    result = subprocess.run(["git", "diff", "--name-only", START_HEAD, "HEAD"], cwd=root, text=True, capture_output=True, check=True)
    return [line for line in result.stdout.splitlines() if line.strip()]

def contains_controlled_token(text: str, token: str) -> bool:
    return re.search(rf"(?<![A-Z0-9_]){re.escape(token)}(?![A-Z0-9_])", text) is not None

def validate(root: Path | None = None, *, package_override: Path | None = None, enforce_git_paths: bool = True) -> dict[str, object]:
    root = (root or Path.cwd()).resolve()
    pkg = package_dir(root, package_override)
    if not pkg.exists():
        raise ValidationError(f"package missing: {pkg}")

    for rel in REQUIRED_FILES:
        if not (pkg / rel).exists():
            raise ValidationError(f"required file missing: {rel}")

    det = root / DETERMINATION_PATH
    if sha256_path(det) != DETERMINATION_SHA:
        raise ValidationError("controlling Founder determination hash mismatch")
    if len(det.read_bytes()) != DETERMINATION_BYTES:
        raise ValidationError("controlling Founder determination byte length mismatch")

    for guide_id, expected in REQUIRED_GUIDES.items():
        path = root / expected["path"]
        if sha256_path(path) != expected["sha256"]:
            raise ValidationError(f"{guide_id} adopted guide bytes changed")
        if len(path.read_bytes()) != expected["byte_length"]:
            raise ValidationError(f"{guide_id} adopted guide byte length changed")

    text_by_rel = {rel: (pkg / rel).read_text(encoding='utf-8') for rel in REQUIRED_FILES if (pkg / rel).suffix in {'.md', '.csv', '.txt'}}
    all_text = "\n".join(text_by_rel.values())
    for token in BAD_AUTHORITY_TOKENS:
        if contains_controlled_token(all_text, token):
            raise ValidationError(f"prohibited authority or evidence token present: {token}")

    important = [rel for rel in REQUIRED_FILES if rel.endswith(('.md', '.csv')) and rel not in {'SOURCE_SHA256SUMS.txt'}]
    for rel in important:
        text = (pkg / rel).read_text(encoding='utf-8')
        for token in REQUIRED_CLOSING:
            if token not in text:
                raise ValidationError(f"required continuing statement {token} missing from {rel}")

    manifest = json.loads((pkg / 'SOURCE_FREEZE_MANIFEST.json').read_text(encoding='utf-8'))
    if manifest.get('required_starting_head') != START_HEAD:
        raise ValidationError("source freeze required starting head mismatch")
    if manifest.get('controlling_determination_sha256') != DETERMINATION_SHA:
        raise ValidationError("source freeze determination hash mismatch")
    if manifest.get('controlling_determination_byte_length') != DETERMINATION_BYTES:
        raise ValidationError("source freeze determination byte length mismatch")
    sources = manifest.get('sources') or []
    if not sources:
        raise ValidationError("source freeze has no sources")
    for entry in sources:
        if not entry.get('sha256') or not entry.get('byte_length'):
            raise ValidationError("source freeze entry missing hash or byte length")
    guide_entries = {g.get('guide_id'): g for g in manifest.get('guides', [])}
    for guide_id, expected in REQUIRED_GUIDES.items():
        got = guide_entries.get(guide_id)
        if not got:
            raise ValidationError(f"source freeze missing guide {guide_id}")
        if got.get('sha256') != expected['sha256'] or int(got.get('byte_length')) != expected['byte_length']:
            raise ValidationError(f"source freeze guide identity mismatch for {guide_id}")

    profile = (pkg / 'ES-CODE-GUIDE-SOLO-FOUNDER-COMPENSATING-ASSURANCE-PROFILE-V1.0.0_CANDIDATE.md').read_text(encoding='utf-8')
    if 'FOUNDER_ADOPTION_CANDIDATE_ONLY' not in profile:
        raise ValidationError("profile is not clearly candidate-only")

    domain = (pkg / 'FOUNDER_DOMAIN_OWNER_REVIEW_RECORD.md').read_text(encoding='utf-8')
    if 'FOUNDER_DOMAIN_OWNER_REVIEW_COMPLETE_WITH_DISCLOSED_NON_INDEPENDENCE' in domain and 'FOUNDER_CONFIRMATION_REQUIRED' in domain:
        raise ValidationError("domain review claims completion with unresolved Founder-confirmation row")

    readiness = read_csv(pkg / 'WAVE_1_STAGE_24_READINESS_MATRIX.csv')
    if len(readiness) != 4:
        raise ValidationError("readiness matrix must contain four guide rows")
    for row in readiness:
        if row.get('readiness_result','').startswith('READY') and (row.get('open_p0_count') != '0' or row.get('open_p1_count') != '0'):
            raise ValidationError("ready result paired with open P0 or P1")
        if row.get('activation_state_after_package') != 'NOT_ACTIVE':
            raise ValidationError("guide marked active by readiness matrix")

    findings = read_csv(pkg / 'WAVE_1_FINDING_TREATMENT_MATRIX.csv')
    expected_fids = {f"W1-V11-FIND-{i:04d}" for i in range(1, 7)}
    if {r.get('finding_id') for r in findings} != expected_fids:
        raise ValidationError("finding treatment matrix missing required W1-V11 findings")
    for row in findings:
        if row.get('current_canonical_status') != 'OPEN':
            raise ValidationError("canonical finding status changed or not open")
        if contains_controlled_token(row.get('proposed_disposition',''), 'CLOSED') or contains_controlled_token(row.get('closure_eligibility',''), 'CLOSED'):
            raise ValidationError("silent finding closure detected")
        if row.get('canonical_update_authorization_state') != 'NOT_AUTHORIZED_IN_THIS_WORKSTREAM':
            raise ValidationError("canonical finding update authorized incorrectly")

    retained = read_csv(pkg / 'RETAINED_CONDITION_WARNING_GAP_AND_BLOCKER_MATRIX.csv')
    if len(retained) < 29:
        raise ValidationError("retained condition/warning/gap/blocker matrix incomplete")
    for row in retained:
        if row.get('canonical_update_authorization_state') != 'NOT_AUTHORIZED_IN_THIS_WORKSTREAM':
            raise ValidationError("canonical retained-item update authorized incorrectly")
        if row.get('record_type') == 'RETAINED_WARNING' and 'CLOSED' in row.get('proposed_treatment',''):
            raise ValidationError("silent warning closure detected")
        if row.get('source_id') == 'CGP005-TA-APP-GAP-0004' and 'CLOSED' in row.get('proposed_treatment',''):
            raise ValidationError("GAP-0004 closure detected")

    risks = read_csv(pkg / 'SOLO_FOUNDER_ASSURANCE_RESIDUAL_RISK_REGISTER.csv')
    if not risks:
        raise ValidationError("residual risk register empty")
    for row in risks:
        if row.get('founder_acceptance_status') != 'PENDING_FOUNDER_DECISION':
            raise ValidationError("Founder residual risk accepted without decision")

    scope = read_csv(pkg / 'PROPOSED_STAGE_24_ACTIVATION_SCOPE_MATRIX.csv')
    if len(scope) != 24:
        raise ValidationError("activation scope matrix must contain 24 rows")
    for row in scope:
        if row.get('activation_state_after_package') != 'NOT_ACTIVE':
            raise ValidationError("activation scope matrix activates a guide")
        if row.get('effective_date_recommendation') != 'NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED_IN_THIS_PACKAGE':
            raise ValidationError("activation effective date established")

    package_manifest = json.loads((pkg / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    manifest_files = package_manifest.get('files', [])
    if not manifest_files:
        raise ValidationError("package manifest contains no files")
    for entry in manifest_files:
        rel = entry['path']
        data = (pkg / rel).read_bytes()
        if hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValidationError(f"package manifest hash mismatch: {rel}")
        if len(data) != entry['byte_length']:
            raise ValidationError(f"package manifest byte length mismatch: {rel}")

    checksum_lines = (pkg / 'CHECKSUM_MANIFEST.sha256').read_text(encoding='utf-8').splitlines()
    if not checksum_lines:
        raise ValidationError("checksum manifest empty")
    for line in checksum_lines:
        digest, rel = line.split('  ', 1)
        data = (pkg / rel).read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValidationError(f"checksum mismatch: {rel}")

    if enforce_git_paths:
        check_authorized_paths(git_changed_paths(root))

    return {
        'status': 'PASS',
        'package': str(pkg),
        'source_count': len(sources),
        'guide_count': len(REQUIRED_GUIDES),
        'finding_rows': len(findings),
        'retained_rows': len(retained),
        'readiness_rows': len(readiness),
        'scope_rows': len(scope),
        'residual_risk_rows': len(risks),
    }

def main() -> int:
    try:
        result = validate(Path.cwd())
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
