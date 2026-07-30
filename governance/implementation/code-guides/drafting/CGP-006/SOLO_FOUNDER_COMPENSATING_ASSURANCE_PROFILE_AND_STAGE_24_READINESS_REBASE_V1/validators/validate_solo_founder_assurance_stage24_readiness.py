#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

DIRECTIVE_ID = "CGP_006_STAGE_24_PROFILE_ADOPTION_LIMITED_ACTIVATION_PROTECTED_MERGE_AND_CUSTODY_DIRECTIVE_V1_0_0"
START_HEAD = "150b24d65d25f79255959ee07a185e7b04601bcf"
PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_AND_STAGE_24_READINESS_REBASE_V1")
DETERMINATION_PATH = Path("governance/implementation/code-guides/founder-determinations/ES-FD-SOLO-FOUNDER-COMPENSATING-ASSURANCE-2026-07-29/FOUNDER_DETERMINATION_SOLO_FOUNDER_COMPENSATING_ASSURANCE_MODEL_2026-07-29.md")
DETERMINATION_SHA = "e777598974887456f22bfc77d8db6c9a235502fc552fb28ce6ff52a77ca3fb61"
DETERMINATION_BYTES = 29240
DISPOSITION_ID = "ES-FD-CGP-006-STAGE-24-LIMITED-ACTIVATION-2026-07-30"
EFFECTIVE_EVENT = "VERIFIED_PROTECTED_MERGE_OF_THE_POST_PR_59_STAGE_24_CUSTODY_PR"
PHASE_A_STATE = "LIMITED_STAGE_24_ACTIVATION_APPROVED_PENDING_CUSTODY"
NOT_ACTIVE_PENDING_CUSTODY = "NOT_ACTIVE_PENDING_CUSTODY"
RISK_DECISION = "ACCEPTED_FOR_LIMITED_STAGE_24_ACTIVATION_ONLY"

REQUIRED_GUIDES = {
    "ES-CG-00": {"sha256": "2275ca1b9674b4e05390f134470a37e7ee63ca423705b6579b1bc8eef874f0c1", "byte_length": 2986, "path": "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-00/ES-CG-00_V1_1_ADOPTION_CANDIDATE.md"},
    "ES-CG-01": {"sha256": "e35ea6b9031bd4c727852b124ef9968fe0ef30afbc4e83efabd270f18248e9e6", "byte_length": 3008, "path": "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-01/ES-CG-01_V1_1_ADOPTION_CANDIDATE.md"},
    "ES-CG-10": {"sha256": "435eb4940da15e6ffbbd66bbc207a05b4fa3ffd3405ff436a8ca15950dfd32c7", "byte_length": 3250, "path": "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-10/ES-CG-10_V1_1_ADOPTION_CANDIDATE.md"},
    "ES-CG-13": {"sha256": "bf79a3762625bfaaa3ebbd4c446c460ab6a60ff9bbd264d2f4b9e9cdb55305e9", "byte_length": 3227, "path": "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_GUIDE_COMPLETION_AND_ADOPTION_CANDIDATE_PREPARATION/guides/ES-CG-13/ES-CG-13_V1_1_ADOPTION_CANDIDATE.md"},
}
APPROVED_TOOLING_SOURCES = {
    "MULTI_AGENT_AND_ASSURANCE_TOOLING_INTENT_V1_0_0.md": {"sha256": "506326268a199d0641f822a59ecd1310cbd76a11c7b8991860a5258216e403bc", "byte_length": 9262, "source_id": "SFCA-SRC-0051", "authority_class": "FOUNDER_APPROVED_TOOLING_INTENT"},
    "MULTI_AGENT_REVIEW_AND_FINDING_VALIDATION_POLICY_V1_0_0.md": {"sha256": "63066def7fd1a9cdebeef261d156706c0de162cc398b05ce2a7eb1a9e9c9a416", "byte_length": 6182, "source_id": "SFCA-SRC-0052", "authority_class": "FOUNDER_APPROVED_REVIEW_POLICY"},
    "AGENT_FINDING_RECORD_SCHEMA_V1_0_0.md": {"sha256": "f0a992322fef30d70747f5df9d58391a4a191c99e425077c04626b643c6c67c0", "byte_length": 3852, "source_id": "SFCA-SRC-0053", "authority_class": "FOUNDER_APPROVED_FINDING_SCHEMA"},
    "MULTI_AGENT_TOOL_ROLE_AND_ACCESS_MATRIX_V1_0_0.md": {"sha256": "db99cd3cc9361b7a1ee9496bcbada9d6209b475ec1f90c477793af9f7a5dda5f", "byte_length": 3817, "source_id": "SFCA-SRC-0054", "authority_class": "FOUNDER_APPROVED_TOOL_ROLE_MATRIX"},
    "EXTERNAL_AGENT_ACCESS_REGISTER_TEMPLATE_V1_0_0.md": {"sha256": "8c8754f5e5bda5ef36ea342e84f6ff83ac5fd275d95a936364614ac4717614e7", "byte_length": 4621, "source_id": "SFCA-SRC-0055", "authority_class": "FOUNDER_APPROVED_ACCESS_REGISTER_TEMPLATE"},
    "FOUNDER_APPROVAL_AND_DISPOSITION_MULTI_AGENT_TOOLING_INTENT_2026-07-30.md": {"sha256": "5c27311183021d1ff3c5f1ec05c6bfd0b3ceb0dc487a3f46fbd3c20cf80d19d9", "byte_length": 5084, "source_id": "SFCA-SRC-0056", "authority_class": "FOUNDER_APPROVED_TOOLING_DISPOSITION"},
    "FOUNDER_APPROVAL_RECORD_MULTI_AGENT_TOOLING_INTENT_2026-07-30.md": {"sha256": "79533235b659ac7a93f7de652f356ec36bedf3ddb14de6a3ab5ce84944e5dedb", "byte_length": 2488, "source_id": "SFCA-SRC-0057", "authority_class": "FOUNDER_APPROVAL_RECORD"},
}
APPROVED_DISPOSITION_SOURCES = {
    "FOUNDER_DISPOSITION_SOLO_FOUNDER_PROFILE_AND_LIMITED_STAGE_24_ACTIVATION_2026-07-30.md": {"sha256": "9bb300eb66e30410e1d6f56f1d337532310e9544e1c3e39eb7f0d848c3692d8f", "byte_length": 11122, "source_id": "SFCA-SRC-0058", "authority_class": "FOUNDER_APPROVED_STAGE24_DISPOSITION"},
    "FOUNDER_RESIDUAL_RISK_ACCEPTANCE_RECORD_STAGE_24_2026-07-30.md": {"sha256": "d8aa1f45d493bb7be5acb65e68b1eb5cc9af2517bc9423c3cbaa06ee7e2374e9", "byte_length": 4214, "source_id": "SFCA-SRC-0059", "authority_class": "FOUNDER_APPROVED_RESIDUAL_RISK_ACCEPTANCE"},
    "FOUNDER_STAGE_24_ACTIVATION_SCOPE_RECORD_2026-07-30.md": {"sha256": "c5a4c05f25635ce5bec8ff805af7c3c0be3fdb8a8fbf8daa3b5199697ba41142", "byte_length": 1869, "source_id": "SFCA-SRC-0060", "authority_class": "FOUNDER_APPROVED_STAGE24_SCOPE_RECORD"},
    "FOUNDER_APPROVAL_RECORD_CGP_006_STAGE_24_DISPOSITION_2026-07-30.md": {"sha256": "7f228f1d81cf09801d0da951b7494c2639dd5ee317d11e1db6bd3832c005ad24", "byte_length": 1254, "source_id": "SFCA-SRC-0061", "authority_class": "FOUNDER_APPROVAL_RECORD"},
}
CANDIDATE_PROFILE = {
    "path": "ES-CODE-GUIDE-SOLO-FOUNDER-COMPENSATING-ASSURANCE-PROFILE-V1.0.0_CANDIDATE.md",
    "sha256": "11c7b7169ed4c6537f7b9cd91f0a952ccb30c66ea86a94d94c826b19a1c28d99",
    "byte_length": 9245,
}
ADOPTED_PROFILE = "ES-CODE-GUIDE-SOLO-FOUNDER-COMPENSATING-ASSURANCE-PROFILE-V1.0.0.md"
REQUIRED_FILES = [
    'README.md', 'WORKSTREAM_CHARTER.md', 'SOURCE_REGISTER.md', 'SOURCE_FREEZE_MANIFEST.json', 'SOURCE_SHA256SUMS.txt', 'SOURCE_AUTHORITY_MATRIX.csv',
    CANDIDATE_PROFILE['path'], ADOPTED_PROFILE, 'STAGE_24_FOUNDER_DISPOSITION_PRE_CUSTODY_RECORD.md',
    'FOUNDER_QUALIFICATION_AND_NON_INDEPENDENCE_DISCLOSURE.md', 'FOUNDER_DOMAIN_OWNER_REVIEW_INSTRUMENT.md', 'FOUNDER_DOMAIN_OWNER_REVIEW_RECORD.md',
    'FOUNDER_TECHNICAL_GOVERNANCE_REVIEW_PROTOCOL.md', 'FOUNDER_TECHNICAL_GOVERNANCE_REVIEW_RECORD.md',
    'PASS_A_AUTHORITY_AND_SOURCE_FIDELITY_REVIEW.md', 'PASS_B_ARCHITECTURE_AND_IMPLEMENTABILITY_REVIEW.md',
    'PASS_C_SECURITY_TENANCY_PRIVACY_AND_SAFEGUARDING_REVIEW.md', 'PASS_D_TESTABILITY_VERIFICATION_AND_EVIDENCE_REVIEW.md',
    'PASS_E_FAILURE_RECOVERY_AND_OPERATIONAL_RELIABILITY_REVIEW.md', 'PASS_F_CLEAN_ROOM_IMPLEMENTER_USABILITY_REVIEW.md',
    'PASS_G_CROSS_GUIDE_RECONCILIATION_REVIEW.md', 'PASS_H_ADVERSARIAL_AND_RED_TEAM_REVIEW.md',
    'MULTI_PASS_REVIEW_RECONCILIATION_REPORT.md', 'WAVE_1_FINDING_TREATMENT_MATRIX.csv',
    'RETAINED_CONDITION_WARNING_GAP_AND_BLOCKER_MATRIX.csv', 'WAVE_1_STAGE_24_READINESS_MATRIX.csv',
    'WAVE_1_STAGE_24_READINESS_REPORT.md', 'PROPOSED_STAGE_24_ACTIVATION_SCOPE_MATRIX.csv',
    'SOLO_FOUNDER_ASSURANCE_RESIDUAL_RISK_REGISTER.csv', 'SOLO_FOUNDER_ASSURANCE_RESIDUAL_RISK_DECISION_REGISTER_STAGE24.csv',
    'FOUNDER_STAGE_24_LIMITED_ACTIVATION_DECISION_PACKET.md', 'AUTHORIZED_PATH_REPORT.md', 'DIRECTIVE_EXECUTION_RECORD.md',
    'VALIDATION_REPORT.md', 'PACKAGE_MANIFEST.json', 'CHECKSUM_MANIFEST.sha256',
    'BUGBOT_PR59_FINDINGS_REPORT.md',
    'validators/validate_solo_founder_assurance_stage24_readiness.py', 'tests/test_solo_founder_assurance_stage24_readiness.py',
] + list(APPROVED_TOOLING_SOURCES) + list(APPROVED_DISPOSITION_SOURCES)
REQUIRED_PHASE_A_STATEMENTS = [
    "FOUNDER_STAGE_24_DISPOSITION_CONTROLLING",
    "FOUNDER_RESIDUAL_RISK_ACCEPTANCE_COMPLETE_12_OF_12",
    "RESIDUAL_RISKS_ACCEPTED_FOR_LIMITED_STAGE_24_ACTIVATION_ONLY",
    "PROFILE_ADOPTED_PENDING_EFFECTIVE_EVENT",
    PHASE_A_STATE,
    "GUIDES_REMAIN_NOT_ACTIVE_PENDING_CUSTODY",
    "PLANNING_REFERENCE_APPROVED_PENDING_EFFECTIVE_EVENT",
    "IMPLEMENTATION_CONTROL_APPROVED_PENDING_EFFECTIVE_EVENT",
    "PULL_REQUEST_REVIEW_APPROVED_PENDING_EFFECTIVE_EVENT",
    "MERGE_GATE_DEFERRED",
    "RELEASE_GATE_DEFERRED",
    "OPERATIONS_REFERENCE_DEFERRED",
    "ACTIVATION_EFFECTIVE_EVENT_PENDING_CUSTODY_PR",
    "NO_GRACE_PERIOD_FOR_NEWLY_AUTHORIZED_WORK",
    "NO_RETROACTIVE_APPLICATION_TO_HISTORICAL_RECORDS",
    "GAP_0004_REMAINS_OPEN",
    "NO_SILENT_FINDING_CLOSURE",
    "NO_SILENT_WARNING_CLOSURE",
    "NO_SILENT_CONDITION_CLOSURE",
    "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "DEPLOYMENT_NOT_AUTHORIZED",
    "STAGING_USE_NOT_AUTHORIZED",
    "PILOT_NOT_AUTHORIZED",
    "PRODUCTION_NOT_AUTHORIZED",
    "WAVE_2_NOT_AUTHORIZED",
    "CGP_007_NOT_AUTHORIZED",
    "MULTI_AGENT_TOOLING_INTENT_FOUNDER_APPROVED",
    "NAMED_TOOLS_NOT_REQUIRED_FOR_LIMITED_STAGE_24_ACTIVATION",
    "NO_EXTERNAL_TOOL_SETUP_AUTHORIZED_BY_THIS_DISPOSITION",
    "CUSTODY_PR_REQUIRED_BEFORE_ACTIVATION_EFFECTIVE",
]
CENTRAL_PHASE_A_FILES = [
    'README.md',
    'FOUNDER_STAGE_24_LIMITED_ACTIVATION_DECISION_PACKET.md',
    'DIRECTIVE_EXECUTION_RECORD.md',
    'VALIDATION_REPORT.md',
    'AUTHORIZED_PATH_REPORT.md',
    'STAGE_24_FOUNDER_DISPOSITION_PRE_CUSTODY_RECORD.md',
]
HISTORICAL_EVIDENCE_FILES = {
    CANDIDATE_PROFILE['path'],
    'BUGBOT_PR59_FINDINGS_REPORT.md',
    'SOURCE_REGISTER.md',
    'SOURCE_AUTHORITY_MATRIX.csv',
}
BAD_AUTHORITY_TOKENS = [
    "SOLO_FOUNDER_ASSURANCE_PROFILE_PROTECTED_ACCESSIONED",
    "SOLO_FOUNDER_ASSURANCE_PROFILE_CUSTODY_COMPLETE",
    "SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_V1_0_0_ADOPTED_AND_ACTIVE",
    "ES_CG_00_ACTIVE_FOR_PLANNING_REFERENCE_IMPLEMENTATION_CONTROL_AND_PULL_REQUEST_REVIEW",
    "ES_CG_01_ACTIVE_FOR_PLANNING_REFERENCE_IMPLEMENTATION_CONTROL_AND_PULL_REQUEST_REVIEW",
    "ES_CG_10_ACTIVE_FOR_PLANNING_REFERENCE_IMPLEMENTATION_CONTROL_AND_PULL_REQUEST_REVIEW",
    "ES_CG_13_ACTIVE_FOR_PLANNING_REFERENCE_IMPLEMENTATION_CONTROL_AND_PULL_REQUEST_REVIEW",
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
    "EXTERNAL_TOOL_SETUP_AUTHORIZED",
    "GITHUB_APP_INSTALLATION_AUTHORIZED",
    "REPOSITORY_PERMISSION_CHANGE_AUTHORIZED",
    "CI_WORKFLOW_CHANGE_AUTHORIZED",
    "DEPENDENCY_INSTALLATION_AUTHORIZED",
    "PLAYWRIGHT_SETUP_AUTHORIZED",
    "CODEQL_ENABLEMENT_AUTHORIZED",
    "CLAUDE_CODE_WRITE_ACCESS_AUTHORIZED",
    "CLAUDE_CODE_WRITE_AUTHORITY_GRANTED",
    "GOOGLE_JULES_WRITE_ACCESS_AUTHORIZED",
    "GOOGLE_JULES_PRESENT_IMPLEMENTATION_AUTHORITY",
    "JULES_IMPLEMENTATION_AUTHORIZED",
    "CURSOR_BACKGROUND_AGENT_USE_AUTHORIZED",
    "CURSOR_BACKGROUND_AGENTS_AUTHORIZED",
    "CURSOR_BACKGROUND_AGENTS_PRESENTLY_AUTHORIZED",
    "NAMED_TOOLS_REQUIRED_FOR_LIMITED_STAGE_24_ACTIVATION",
    "NAMED_TOOLS_ARE_MANDATORY_FOR_LIMITED_STAGE_24_ACTIVATION",
    "TOOLING_REQUIRED_FOR_LIMITED_STAGE_24_ACTIVATION",
    "AGENT_FINDING_PROVEN_WITHOUT_VALIDATION",
    "AGENT_FINDING_TREATED_AS_PROVEN_WITHOUT_VALIDATION",
    "AGENT_MAY_SELF_APPROVE_AND_MERGE",
    "SELF_APPROVE_AND_MERGE_AUTHORIZED",
    "PENDING_APPROVAL",
    "PENDING_FOUNDER_APPROVAL",
    "TOOLING_INTENT_CANDIDATE",
    "DOCUMENT_STATUS_CANDIDATE",
    "SECOND_PR_OPENED",
    "NEW_PR_OPENED",
]

CONTRADICTORY_TOKEN_RULES = [
    {
        "name": "residual risk acceptance required after completion",
        "tokens": (
            "FOUNDER_RESIDUAL_RISK_ACCEPTANCE_REQUIRED",
            "FOUNDER_RESIDUAL_RISK_ACCEPTANCE_COMPLETE_12_OF_12",
        ),
    },
]

TERMINAL_STAGE24_LIFECYCLE_TOKENS = (
    "FOUNDER_ADOPTED",
    "PROFILE_ADOPTED_PENDING_EFFECTIVE_EVENT",
    PHASE_A_STATE,
    EFFECTIVE_EVENT,
    "CGP_006_STAGE_24_PROFILE_ADOPTION_LIMITED_ACTIVATION_AND_CUSTODY_COMPLETE",
    "SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_V1_0_0_ADOPTED_AND_ACTIVE",
)

CONTRADICTORY_TOKEN_RULES.extend(
    {
        "name": "stale draft PR disposition after terminal Stage 24 lifecycle state",
        "tokens": (
            "DRAFT_PR_OPEN_UNMERGED_PENDING_FOUNDER_STAGE_24_DISPOSITION",
            token,
        ),
    }
    for token in TERMINAL_STAGE24_LIFECYCLE_TOKENS
)

class ValidationError(Exception):
    pass

def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def package_dir(root: Path, override: Path | None = None) -> Path:
    return override if override is not None else root / PACKAGE_REL

def contains_controlled_token(text: str, token: str) -> bool:
    return re.search(rf"(?<![A-Z0-9_]){re.escape(token)}(?![A-Z0-9_])", text) is not None

def package_repo_path(rel: str) -> str:
    return (PACKAGE_REL / rel).as_posix()

def check_authorized_paths(paths: list[str]) -> None:
    prefix = PACKAGE_REL.as_posix() + "/"
    outside = [p for p in paths if p and not p.startswith(prefix)]
    if outside:
        raise ValidationError(f"files outside authorized package path changed: {outside}")

def find_contradictory_governance_tokens(text_by_rel: dict[str, str]) -> list[str]:
    contradictions = []
    for rel, text in sorted(text_by_rel.items()):
        for rule in CONTRADICTORY_TOKEN_RULES:
            tokens = tuple(rule["tokens"])
            if all(contains_controlled_token(text, token) for token in tokens):
                contradictions.append(f"{rel}: {rule['name']} ({' + '.join(tokens)})")
    return contradictions

def check_contradictory_governance_tokens(text_by_rel: dict[str, str]) -> None:
    contradictions = find_contradictory_governance_tokens(text_by_rel)
    if contradictions:
        raise ValidationError("contradictory governance-state tokens present: " + "; ".join(contradictions))

def git_changed_paths(root: Path) -> list[str]:
    result = subprocess.run(["git", "diff", "--name-only", START_HEAD, "HEAD"], cwd=root, text=True, capture_output=True, check=True)
    return [line for line in result.stdout.splitlines() if line.strip()]

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

    candidate = pkg / CANDIDATE_PROFILE["path"]
    if sha256_path(candidate) != CANDIDATE_PROFILE["sha256"]:
        raise ValidationError("candidate profile hash mismatch")
    if len(candidate.read_bytes()) != CANDIDATE_PROFILE["byte_length"]:
        raise ValidationError("candidate profile byte length mismatch")

    for rel, expected in {**APPROVED_TOOLING_SOURCES, **APPROVED_DISPOSITION_SOURCES}.items():
        path = pkg / rel
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise ValidationError(f"approved source hash mismatch: {rel}")
        if len(data) != expected["byte_length"]:
            raise ValidationError(f"approved source byte length mismatch: {rel}")

    adopted_path = pkg / ADOPTED_PROFILE
    adopted_data = adopted_path.read_bytes()
    adopted_sha = hashlib.sha256(adopted_data).hexdigest()
    adopted_bytes = len(adopted_data)
    adopted_text = adopted_data.decode("utf-8")
    if "FOUNDER_ADOPTED" not in adopted_text:
        raise ValidationError("adopted profile missing adopted status")
    if "FOUNDER_ADOPTION_CANDIDATE_ONLY" in adopted_text:
        raise ValidationError("adopted profile still marked candidate-only")
    for token in (DISPOSITION_ID, "PROFILE_ADOPTED_PENDING_EFFECTIVE_EVENT", EFFECTIVE_EVENT, "Founder-Approved Multi-Agent and Deterministic Assurance Tooling Intent"):
        if token not in adopted_text:
            raise ValidationError(f"adopted profile missing required token: {token}")

    text_by_rel = {}
    for rel in REQUIRED_FILES:
        if rel.endswith(('.md', '.csv', '.txt')):
            if rel in APPROVED_DISPOSITION_SOURCES or rel in APPROVED_TOOLING_SOURCES or rel in HISTORICAL_EVIDENCE_FILES:
                continue
            text_by_rel[rel] = (pkg / rel).read_text(encoding='utf-8')
    check_contradictory_governance_tokens(text_by_rel)
    all_text = "\n".join(text_by_rel.values())
    for token in BAD_AUTHORITY_TOKENS:
        if contains_controlled_token(all_text, token):
            raise ValidationError(f"prohibited authority or evidence token present: {token}")

    for rel in CENTRAL_PHASE_A_FILES:
        text = (pkg / rel).read_text(encoding='utf-8')
        for token in REQUIRED_PHASE_A_STATEMENTS:
            if token not in text:
                raise ValidationError(f"required Phase A statement {token} missing from {rel}")

    manifest = json.loads((pkg / 'SOURCE_FREEZE_MANIFEST.json').read_text(encoding='utf-8'))
    if manifest.get('required_starting_head') != START_HEAD:
        raise ValidationError("source freeze required starting head mismatch")
    if manifest.get('controlling_determination_sha256') != DETERMINATION_SHA:
        raise ValidationError("source freeze determination hash mismatch")
    if manifest.get('controlling_determination_byte_length') != DETERMINATION_BYTES:
        raise ValidationError("source freeze determination byte length mismatch")
    if manifest.get('stage24_phase_a_state') != PHASE_A_STATE:
        raise ValidationError("source freeze Phase A state mismatch")
    if manifest.get('effective_event') != EFFECTIVE_EVENT:
        raise ValidationError("source freeze effective event mismatch")
    adopted_manifest = manifest.get('adopted_profile') or {}
    if adopted_manifest.get('sha256') != adopted_sha or int(adopted_manifest.get('byte_length', 0)) != adopted_bytes:
        raise ValidationError("source freeze adopted profile identity mismatch")
    if adopted_manifest.get('candidate_sha256') != CANDIDATE_PROFILE['sha256']:
        raise ValidationError("source freeze adopted profile candidate hash mismatch")
    sources = manifest.get('sources') or []
    source_entries = {entry.get('repository_path'): entry for entry in sources}
    for rel, expected in {**APPROVED_TOOLING_SOURCES, **APPROVED_DISPOSITION_SOURCES}.items():
        repo_path = package_repo_path(rel)
        entry = source_entries.get(repo_path)
        if not entry:
            raise ValidationError(f"source freeze missing approved source: {rel}")
        if entry.get('source_id') != expected['source_id']:
            raise ValidationError(f"source freeze approved source id mismatch: {rel}")
        if entry.get('authority_class') != expected['authority_class']:
            raise ValidationError(f"source freeze approved authority mismatch: {rel}")
        if entry.get('sha256') != expected['sha256'] or int(entry.get('byte_length')) != expected['byte_length']:
            raise ValidationError(f"source freeze approved identity mismatch: {rel}")
    adopted_entry = source_entries.get(package_repo_path(ADOPTED_PROFILE))
    if not adopted_entry:
        raise ValidationError("source freeze missing adopted profile")
    if adopted_entry.get("sha256") != adopted_sha or int(adopted_entry.get("byte_length")) != adopted_bytes:
        raise ValidationError("source freeze adopted profile source entry mismatch")
    guide_entries = {g.get('guide_id'): g for g in manifest.get('guides', [])}
    for guide_id, expected in REQUIRED_GUIDES.items():
        got = guide_entries.get(guide_id)
        if not got:
            raise ValidationError(f"source freeze missing guide {guide_id}")
        if got.get('sha256') != expected['sha256'] or int(got.get('byte_length')) != expected['byte_length']:
            raise ValidationError(f"source freeze guide identity mismatch for {guide_id}")

    readiness = read_csv(pkg / 'WAVE_1_STAGE_24_READINESS_MATRIX.csv')
    if len(readiness) != 4:
        raise ValidationError("readiness matrix must contain four guide rows")
    for row in readiness:
        if row.get('readiness_result','').startswith('READY') and (row.get('open_p0_count') != '0' or row.get('open_p1_count') != '0'):
            raise ValidationError("ready result paired with open P0 or P1")
        if row.get('residual_risk') != RISK_DECISION:
            raise ValidationError("readiness matrix residual risk not Founder-accepted")
        if row.get('activation_state_after_package') != NOT_ACTIVE_PENDING_CUSTODY:
            raise ValidationError("readiness matrix activates a guide or omits custody-pending state")

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
    if len(risks) != 12:
        raise ValidationError("residual risk register must contain twelve rows")
    risk_ids = {row.get('risk_id') for row in risks}
    for row in risks:
        if row.get('founder_acceptance_status') != RISK_DECISION:
            raise ValidationError("Founder residual risk decision incomplete")
        if 'risk_closure_status' in row and row.get('risk_closure_status') != 'OPEN_NOT_CLOSED':
            raise ValidationError("residual risk closed")

    decisions = read_csv(pkg / 'SOLO_FOUNDER_ASSURANCE_RESIDUAL_RISK_DECISION_REGISTER_STAGE24.csv')
    if {row.get('risk_id') for row in decisions} != risk_ids:
        raise ValidationError("residual risk decision companion register mismatch")
    for row in decisions:
        if row.get('founder_decision') != RISK_DECISION:
            raise ValidationError("residual risk companion decision incomplete")
        if row.get('disposition_id') != DISPOSITION_ID:
            raise ValidationError("residual risk companion disposition mismatch")
        if row.get('risk_closure_status') != 'OPEN_NOT_CLOSED':
            raise ValidationError("residual risk companion marks risk closed")

    scope = read_csv(pkg / 'PROPOSED_STAGE_24_ACTIVATION_SCOPE_MATRIX.csv')
    if len(scope) != 24:
        raise ValidationError("activation scope matrix must contain 24 rows")
    approved_scopes = {'PLANNING_REFERENCE', 'IMPLEMENTATION_CONTROL', 'PULL_REQUEST_REVIEW'}
    deferred_scopes = {'MERGE_GATE', 'RELEASE_GATE', 'OPERATIONS_REFERENCE'}
    for row in scope:
        if row.get('activation_state_after_package') != NOT_ACTIVE_PENDING_CUSTODY:
            raise ValidationError("activation scope matrix activates a guide before custody")
        if row.get('scope') in approved_scopes:
            if row.get('recommended_posture') != 'APPROVED_PENDING_EFFECTIVE_EVENT':
                raise ValidationError("approved scope missing pending effective-event posture")
            if row.get('effective_date_recommendation') != EFFECTIVE_EVENT:
                raise ValidationError("approved scope missing custody effective event")
            if row.get('grace_period') != 'NO_GRACE_PERIOD_FOR_NEWLY_AUTHORIZED_WORK':
                raise ValidationError("approved scope missing no-grace treatment")
        elif row.get('scope') in deferred_scopes:
            if row.get('recommended_posture') != 'DEFERRED_BY_FOUNDER_DISPOSITION':
                raise ValidationError("deferred scope not deferred")
            if row.get('effective_date_recommendation') != 'DEFERRED_NO_EFFECTIVE_EVENT':
                raise ValidationError("deferred scope has effective event")
        else:
            raise ValidationError(f"unknown activation scope: {row.get('scope')}")

    package_manifest = json.loads((pkg / 'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
    manifest_files = package_manifest.get('files', [])
    if not manifest_files:
        raise ValidationError("package manifest contains no files")
    if package_manifest.get("directive_id") != DIRECTIVE_ID:
        raise ValidationError("package manifest directive mismatch")
    if package_manifest.get("stage24_disposition_id") != DISPOSITION_ID:
        raise ValidationError("package manifest disposition mismatch")
    manifest_paths = {entry['path'] for entry in manifest_files}
    for rel in list(APPROVED_TOOLING_SOURCES) + list(APPROVED_DISPOSITION_SOURCES) + [ADOPTED_PROFILE]:
        if rel not in manifest_paths:
            raise ValidationError(f"package manifest missing required file: {rel}")
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

    source_sums = (pkg / 'SOURCE_SHA256SUMS.txt').read_text(encoding='utf-8')
    for rel, expected in {**APPROVED_TOOLING_SOURCES, **APPROVED_DISPOSITION_SOURCES}.items():
        expected_line = f"{expected['sha256']}  {package_repo_path(rel)}"
        if expected_line not in source_sums:
            raise ValidationError(f"source SHA-256 ledger missing approved source: {rel}")
    if f"{adopted_sha}  {package_repo_path(ADOPTED_PROFILE)}" not in source_sums:
        raise ValidationError("source SHA-256 ledger missing adopted profile")

    source_register = (pkg / 'SOURCE_REGISTER.md').read_text(encoding='utf-8')
    authority_rows = {row['source_id']: row for row in read_csv(pkg / 'SOURCE_AUTHORITY_MATRIX.csv')}
    for rel, expected in {**APPROVED_TOOLING_SOURCES, **APPROVED_DISPOSITION_SOURCES}.items():
        if rel not in source_register or expected['authority_class'] not in source_register:
            raise ValidationError(f"source register missing approved classification: {rel}")
        row = authority_rows.get(expected['source_id'])
        if not row:
            raise ValidationError(f"authority matrix missing approved source: {rel}")
        if row.get('authority_class') != expected['authority_class']:
            raise ValidationError(f"authority matrix approved authority mismatch: {rel}")
    adopted_row = authority_rows.get("SFCA-SRC-0062")
    if not adopted_row:
        raise ValidationError("authority matrix missing adopted profile")
    if adopted_row.get("source_status") != "founder_adopted_pending_effective_event":
        raise ValidationError("authority matrix adopted profile status mismatch")

    if enforce_git_paths:
        check_authorized_paths(git_changed_paths(root))

    return {
        'status': 'PASS',
        'package': str(pkg),
        'source_count': len(sources),
        'approved_tooling_source_count': len(APPROVED_TOOLING_SOURCES),
        'approved_disposition_source_count': len(APPROVED_DISPOSITION_SOURCES),
        'adopted_profile_sha256': adopted_sha,
        'adopted_profile_byte_length': adopted_bytes,
        'guide_count': len(REQUIRED_GUIDES),
        'finding_rows': len(findings),
        'retained_rows': len(retained),
        'readiness_rows': len(readiness),
        'scope_rows': len(scope),
        'residual_risk_rows': len(risks),
        'residual_risk_decision_rows': len(decisions),
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
