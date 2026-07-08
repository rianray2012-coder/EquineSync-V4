from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RF14Row:
    key: str
    area: str
    status: str
    evidence: str
    next_action: str


FOUNDER_DECISIONS = [
    {
        "decision": "Confirm canonical legal-signature source.",
        "status": "requires founder review",
        "phase": "RF14, RF18",
        "notes": "Recommended: keep DocuSign-backed document-signature workflows canonical for legal signature claims; keep Digital Forms as local acknowledgement/readiness only.",
    },
    {
        "decision": "Confirm guardian/minor signer policy.",
        "status": "requires founder review",
        "phase": "RF14, RF18",
        "notes": "RF14 enforces guardian IDs for guardian-required requests; founder/legal should confirm under-13 and 13-17 signing posture before UAT acceptance.",
    },
    {
        "decision": "Confirm provider/trainer document scope.",
        "status": "requires founder review",
        "phase": "RF10, RF14, RF18",
        "notes": "Provider-facing document visibility and signature scope remain deferred until relationship grants and signer rules are accepted.",
    },
    {
        "decision": "Confirm production storage provider and retention.",
        "status": "requires founder review",
        "phase": "RF14, RF18",
        "notes": "RF14 records scan upload intents only; production storage, retention, signed-document archival, and deletion SLAs need owner acceptance.",
    },
    {
        "decision": "Confirm live DocuSign timing.",
        "status": "requires founder review",
        "phase": "RF14, BN22A, RF18",
        "notes": "RF14 does not send live envelopes. Sandbox/live provider activation should wait for credentials, legal approval, app-store/native posture, and UAT evidence.",
    },
]


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _status_counts(rows: Iterable[RF14Row]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def build_rf14_documents_signatures_storage_consolidation(root: Path = ROOT) -> Dict[str, object]:
    backlog = _read(root, "backend/routes/backlog.py")
    document_signatures = _read(root, "backend/routes/document_signatures.py")
    workflows = _read(root, "backend/core/document_workflows.py")
    forms_ui = _read(root, "frontend/src/pages/FormsSignatures.jsx")
    rf6_doc = _read(root, "BUILD_NEXT_6A_SIGNATURE_CONNECTOR_PREP_README.md")
    rf7_doc = _read(root, "docs/RF7_OWNER_GUARDIAN_CLIENT_PORTAL_HARDENING.md")
    rf10_doc = _read(root, "docs/RF10_SERVICE_PROVIDER_CARE_PARTNER.md")
    rf14_plan = _read(root, "docs/RF14_DOCUMENTS_SIGNATURES_STORAGE_CONSOLIDATION_PLAN.md")
    rf14_tests = _read(root, "backend/tests/test_rf14_documents_signatures_storage_consolidation.py")

    rows = [
        RF14Row(
            key="canonical_document_workflow_matrix",
            area="Canonical document/signature workflow matrix",
            status="ready"
            if _contains_all(
                workflows,
                [
                    "WORKFLOW_PROVIDER_SIGNATURE",
                    "WORKFLOW_IN_HOUSE_ACKNOWLEDGEMENT",
                    "PROVIDER_DOCUSIGN",
                    "DOCUMENT_TYPE_MATRIX",
                    "signer_requirements_for_subject",
                ],
            )
            else "blocked",
            evidence="Document workflow helpers distinguish DocuSign provider-signature workflows from in-house acknowledgement workflows.",
            next_action="Founder/legal should accept which document types are legal signatures before production legal claims.",
        ),
        RF14Row(
            key="guardian_required_request_enforcement",
            area="Guardian/minor signer enforcement",
            status="ready"
            if _contains_all(
                document_signatures,
                [
                    "SIGNER_GUARDIAN in signer_roles",
                    "guardian_user_ids is required for guardian-required document requests",
                ],
            )
            and _contains_all(
                rf14_tests,
                [
                    "test_guardian_required_document_request_requires_guardian_user_ids",
                    "assert db.document_requests.rows == []",
                    'assert body["signer_roles"] == ["guardian", "subject"]',
                ],
            )
            else "blocked",
            evidence="Guardian-required document requests reject missing guardian IDs before creating a local request row.",
            next_action="RF18 should UAT seeded under-13, 13-17, adult, guardian, and owner signer paths after founder/legal acceptance.",
        ),
        RF14Row(
            key="provider_references_hidden_from_projection",
            area="Provider reference projection",
            status="ready"
            if _contains_all(
                workflows,
                [
                    "PRIVATE_DOCUMENT_FIELDS",
                    "PROVIDER_REF_FIELDS",
                    "include_provider_refs: bool = False",
                    "if key in PROVIDER_REF_FIELDS and not include_provider_refs",
                ],
            )
            and _contains_all(
                rf14_tests,
                [
                    '"required_signer_user_ids" not in body',
                    '"provider_envelope_id" not in body',
                ],
            )
            else "blocked",
            evidence="Document request projections hide raw signer ID lists and provider envelope/signature/certificate references by default.",
            next_action="Keep provider references server-side unless a future legal/admin surface explicitly needs them.",
        ),
        RF14Row(
            key="digital_forms_local_acknowledgement_truth",
            area="Digital Forms legal-signature truth",
            status="ready"
            if _contains_all(
                backlog,
                [
                    "def _normalize_digital_form_data",
                    'normalized["signature_scope"] = "local_acknowledgement_only"',
                    'normalized["legal_signature_status"] = "not_legal_signature"',
                    'normalized["signature_scope"] = "provider_readiness_only"',
                    'normalized["legal_signature_status"] = "provider_not_sent"',
                    '"signed_claim": "local_acknowledgement_not_legal_signature"',
                ],
            )
            and _contains_all(
                rf14_tests,
                [
                    "test_forms_signature_records_are_local_or_provider_readiness_truth",
                    "test_owner_form_acknowledgement_is_scoped_and_not_legal_signature",
                ],
            )
            else "blocked",
            evidence="Digital Forms records and owner acknowledgements now carry explicit local-acknowledgement or provider-readiness truth fields.",
            next_action="If founder/legal wants Digital Forms to become legal signatures, route that through the canonical provider-signature workflow instead of reusing local acknowledgement labels.",
        ),
        RF14Row(
            key="forms_ui_truth_labels",
            area="Forms & Signatures UI truth labels",
            status="ready"
            if _contains_all(
                forms_ui,
                [
                    "local acknowledgement records",
                    "signature-provider readiness",
                    "ready locally",
                    "acknowledged locally",
                    "Mark ready locally",
                    "Record acknowledgement",
                ],
            )
            else "blocked",
            evidence="Forms & Signatures UI copy no longer implies live provider delivery or legal completion for local records.",
            next_action="RF17 should hide or further demote readiness-only surfaces if founder wants fewer prelaunch controls visible.",
        ),
        RF14Row(
            key="document_scan_storage_intent_only",
            area="Document scan storage boundary",
            status="ready"
            if _contains_all(
                backlog,
                [
                    '"status": "upload_intent_ready"',
                    '"storage_claim": "upload_intent_only_no_external_file_mutation_by_rf14"',
                    "Upload intent only. Store through upload_url only when a real storage provider is configured",
                ],
            )
            and _contains_all(
                rf14_tests,
                [
                    "test_document_scan_prepare_upload_is_upload_intent_only",
                    '"upload_intent_only_no_external_file_mutation_by_rf14"',
                ],
            )
            else "blocked",
            evidence="Document scan preparation returns an upload-intent manifest and explicitly does not claim an external file mutation by RF14.",
            next_action="Founder should accept production storage provider, retention, deletion, and signed-document archival requirements before launch claims.",
        ),
        RF14Row(
            key="owner_document_visibility_boundary",
            area="Owner document visibility boundary",
            status="ready"
            if _contains_all(
                rf7_doc,
                [
                    "Owner and guardian portal horse lists",
                    "Owner-safe backend horse contract",
                    "Media, forms, and health-document feeds continue to use stable owner/user/horse clauses.",
                ],
            )
            and _contains_all(
                backlog,
                [
                    "@router.get(\"/owner-portal/forms\")",
                    "@router.post(\"/owner-portal/forms/{record_id}/sign\")",
                    "_owner_account_clauses",
                ],
            )
            else "blocked",
            evidence="Owner form listing and acknowledgement routes remain relationship-scoped through stable owner account clauses.",
            next_action="RF18 should browser/UAT owner, guardian, leasee, and cross-barn document visibility once seeded data exists.",
        ),
        RF14Row(
            key="provider_document_scope_deferred",
            area="Provider/trainer document scope",
            status="deferred"
            if _contains_all(
                rf10_doc,
                [
                    "Provider documents and legal signatures",
                    "RF14 owns legal document/signature/storage truth.",
                    "deferred",
                ],
            )
            and _contains_all(
                rf14_plan,
                [
                    "Decide provider document scope.",
                    "Confirm whether service providers can view/upload/sign documents and under which horse/provider grants.",
                ],
            )
            else "blocked",
            evidence="RF14 records provider/trainer document scope as founder-decision work instead of broadening access.",
            next_action="Founder should accept provider/trainer document visibility and signer grants before implementation or UAT claims.",
        ),
        RF14Row(
            key="live_provider_boundary_preserved",
            area="No-provider-call boundary",
            status="ready"
            if _contains_all(
                rf14_plan,
                [
                    "record storage/provider boundaries without calling",
                    "DocuSign, Google Drive, S3, Vercel, Render, MongoDB Atlas, or UAT systems.",
                    "RF14 must not:",
                    "call DocuSign, Google Drive, S3, Vercel, Render, MongoDB Atlas, Resend,",
                    "auto-mark founder decisions accepted.",
                ],
            )
            and _contains_all(
                rf6_doc,
                [
                    "No provider API calls.",
                    "No signed document storage.",
                ],
            )
            else "blocked",
            evidence="RF14 keeps legal signature and storage provider work as evidence/proof only and does not call DocuSign or storage providers.",
            next_action="Provider activation needs a later founder-approved credentials, legal, native, and UAT gate.",
        ),
    ]

    counts = _status_counts(rows)
    return {
        "phase": "RF14",
        "title": "RF14 Documents, Signatures, and Storage Consolidation",
        "overall_status": "ready" if counts.get("blocked", 0) == 0 and counts.get("missing", 0) == 0 else "blocked",
        "status_counts": counts,
        "rows": rows,
        "founder_decisions": FOUNDER_DECISIONS,
    }


def _table(headers: List[str], rows: List[List[str]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out.extend("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def render_rf14_report(report: Dict[str, object]) -> str:
    rows: List[RF14Row] = report["rows"]  # type: ignore[assignment]
    founder_decisions: List[Dict[str, str]] = report["founder_decisions"]  # type: ignore[assignment]

    return "\n".join([
        "# RF14 Documents, Signatures, and Storage Consolidation Report",
        "",
        "Phase: `RF14`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Status Rows",
        "",
        _table(
            ["Key", "Area", "Status", "Evidence", "Next Action"],
            [[row.key, row.area, row.status, row.evidence, row.next_action] for row in rows],
        ),
        "",
        "## Founder Decision Rows",
        "",
        _table(
            ["Decision", "Status", "Phase", "Notes"],
            [[item["decision"], item["status"], item["phase"], item["notes"]] for item in founder_decisions],
        ),
        "",
        "## RF14 Boundary",
        "",
        "- RF14 consolidates document/signature/storage truth without enabling live provider behavior.",
        "- RF14 keeps DocuSign-backed document-signature workflows as the legal-signature readiness path and Digital Forms as local acknowledgement/provider-readiness records.",
        "- RF14 enforces guardian IDs for guardian-required document requests and keeps signer/provider references out of default projections.",
        "- RF14 records document scan storage as upload-intent-only evidence.",
        "- RF14 does not call DocuSign, Stripe, Apple, Google, Resend, MongoDB Atlas, Vercel, Render, S3, Google Drive, UAT systems, or external storage/signature providers.",
        "- Current launch claims may say EquineSync has document/signature/storage readiness evidence, local acknowledgement truth labels, guardian-required request enforcement, and upload-intent storage manifests. They must not claim live legal signature delivery, universal signed-document storage, provider document access, or production storage retention/deletion workflows implemented by RF14.",
        "",
    ])
