"""Draft-only AI extraction service for EquineSync.

This module is deliberately conservative: it returns review-required draft
payloads and never writes product records. Routes persist the draft job result;
approval/rejection workflow remains separate and human-confirmed.
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx


DEFAULT_MODEL = os.environ.get("OPENAI_EXTRACTION_MODEL", "gpt-4.1-mini")
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_FILES_URL = "https://api.openai.com/v1/files"


AI_SOURCE_TYPES = {
    "invoice",
    "service_invoice",
    "ride_data",
    "lesson_schedule",
    "training_note",
    "voice_transcript",
    "health_observation",
    "photo_inventory",
}

AI_ALLOWED_MIME = {
    "application/pdf",
    "application/json",
    "text/plain",
    "text/csv",
    "text/markdown",
    "image/jpeg",
    "image/png",
    "image/webp",
}

AI_IMAGE_MIME = {"image/jpeg", "image/png", "image/webp"}
AI_TEXT_MIME = {"application/json", "text/plain", "text/csv", "text/markdown"}
AI_MAX_BYTES = 20 * 1024 * 1024
PDF_TEXT_MIN_CHARS = 40
PDF_IMAGE_FALLBACK_MAX_PAGES = 3
COMMON_REVIEW_FIELDS = {
    "review_summary": None,
    "confidence": None,
    "missing_information": [],
}
AI_BLOCKED_ACTIONS = [
    "official_record_save",
    "ai_autonomous_mutation",
]
HEALTH_REVIEW_BLOCKED_ACTIONS = [
    "diagnosis",
    "treatment_recommendation",
    "treatment_decision",
    "medication_change",
    "emergency_triage",
    "participant_notification",
    "provider_message_send",
]
INVENTORY_REVIEW_STATUSES = {"needs_review", "candidate_only"}
INVENTORY_CANDIDATE_TEMPLATE = {
    "item_name": None,
    "category": None,
    "quantity": None,
    "unit": None,
    "storage_location": None,
    "horse_or_barn_assignment": None,
    "source_confidence": None,
    "review_status": "needs_review",
    "reorder_candidate": None,
    "notes": [],
}

SERVICE_HISTORY_CANDIDATE_TEMPLATE = {
    "provider": None,
    "service_type": None,
    "horse": None,
    "service_date": None,
    "amount": None,
    "payment_status_candidate": "review_required",
    "review_status": "needs_review",
    "source_confidence": None,
    "notes": [],
}

INVOICE_CANDIDATE_TEMPLATE = {
    "vendor_or_provider": None,
    "invoice_or_order_reference": None,
    "invoice_date": None,
    "subtotal": None,
    "tax": None,
    "total": None,
    "payment_status_candidate": "review_required",
    "review_status": "needs_review",
    "source_confidence": None,
    "notes": [],
}

INVOICE_PAYMENT_REVIEW_TEMPLATE = {
    "candidate_status": "review_required",
    "confidence": None,
    "basis": [],
    "matched_processor_event": None,
    "matched_manual_payment_record": None,
    "requires_human_confirmation": True,
    "official_payment_status_change_allowed": False,
    "invoice_finalization_allowed": False,
    "subscription_entitlement_change_allowed": False,
}

SCHEDULE_REVIEW_BOUNDARY_TEMPLATE = {
    "candidate_status": "review_required",
    "requires_human_confirmation": True,
    "official_calendar_change_allowed": False,
    "participant_notification_allowed": False,
    "automated_send_allowed": False,
    "recipient_opt_in_review_required": True,
    "privacy_safe_copy_review_required": True,
}

WORK_TICKET_CANDIDATE_TEMPLATE = {
    "title": None,
    "category": None,
    "details": None,
    "priority": "standard",
    "due_date": None,
    "assigned_role": None,
    "review_status": "needs_review",
    "source_confidence": None,
    "notes": [],
}


def normalize_source_type(value: str) -> str:
    source_type = (value or "").strip().lower()
    if source_type not in AI_SOURCE_TYPES:
        raise ValueError("Unsupported AI source type")
    return source_type


def validate_ai_source(*, source_type: str, mime_type: str, byte_size: int) -> str:
    normalize_source_type(source_type)
    normalized_mime = (mime_type or "").strip().lower()
    if normalized_mime not in AI_ALLOWED_MIME:
        raise ValueError("Unsupported AI source mime type")
    if byte_size <= 0 or byte_size > AI_MAX_BYTES:
        raise ValueError("AI source size out of bounds")
    if source_type == "photo_inventory" and normalized_mime not in AI_IMAGE_MIME:
        raise ValueError("Photo inventory sources must be images")
    return normalized_mime


def private_ai_storage_key(*, barn_id: str, source_id: str, filename: str) -> str:
    extension = ""
    if "." in (filename or ""):
        raw_extension = filename.rsplit(".", 1)[-1].lower()
        safe_extension = "".join(c for c in raw_extension if c.isalnum())[:12]
        if safe_extension:
            extension = f".{safe_extension}"
    return f"{barn_id}/ai-draft-sources/{source_id}/source{extension}"


def draft_system_instruction() -> str:
    return (
        "Return JSON only. This is EquineSync staging/draft extraction. "
        "All outputs must include draft_only=true and review_required=true. "
        "Do not diagnose, mark payment status, send messages, save records, "
        "identify private people, or make safety, billing, legal, messaging, "
        "or access-control decisions. If unclear, use null and add a "
        "review_questions entry."
    )


def output_schema_hint(source_type: str) -> str:
    if source_type in {"invoice", "service_invoice"}:
        return json.dumps({
            "draft_only": True,
            "review_required": True,
            "source_category": source_type,
            **COMMON_REVIEW_FIELDS,
            "vendor_or_provider": None,
            "document_type": None,
            "order_date": None,
            "merchant_order_reference": None,
            "line_items": [],
            "draft_inventory_candidates": [INVENTORY_CANDIDATE_TEMPLATE],
            "draft_service_history_candidates": [SERVICE_HISTORY_CANDIDATE_TEMPLATE],
            "draft_invoice_candidates": [INVOICE_CANDIDATE_TEMPLATE],
            "draft_expense_candidates": [],
            "draft_payment_status_candidate": {
                "status": "review_required",
                "basis": [],
                "official_payment_status_change_allowed": False,
            },
            "draft_payment_review": INVOICE_PAYMENT_REVIEW_TEMPLATE,
            "draft_reconciliation_questions": [],
            "review_questions": [],
            "blocked_actions": [
                *AI_BLOCKED_ACTIONS,
                "inventory_record_create",
                "payment_status_change",
                "invoice_finalization",
                "charge_money",
                "refund_or_credit",
                "subscription_entitlement_change",
            ],
        })
    if source_type == "photo_inventory":
        return json.dumps({
            "draft_only": True,
            "review_required": True,
            "source_category": "photo_inventory",
            **COMMON_REVIEW_FIELDS,
            "room_or_area": None,
            "visible_storage_state": None,
            "visible_inventory_categories": [],
            "visible_count_estimates": [],
            "draft_inventory_candidates": [INVENTORY_CANDIDATE_TEMPLATE],
            "organization_or_reorder_suggestions": [],
            "not_counted_or_uncertain": [],
            "review_questions": [],
            "blocked_actions": [*AI_BLOCKED_ACTIONS, "inventory_record_create"],
        })
    if source_type == "ride_data":
        return json.dumps({
            "draft_only": True,
            "review_required": True,
            "source_category": "ride_data",
            **COMMON_REVIEW_FIELDS,
            "draft_ride_summary": {
                "horse": None,
                "rider": None,
                "date": None,
                "duration": None,
                "distance": None,
                "speed": None,
                "heart_rate": None,
                "gps_or_route_notes": None,
                "training_focus": [],
                "observations": [],
            },
            "draft_training_candidates": [],
            "review_questions": [],
            "blocked_actions": ["official_record_save", "health_diagnosis"],
        })
    if source_type == "lesson_schedule":
        return json.dumps({
            "draft_only": True,
            "review_required": True,
            "source_category": "lesson_schedule",
            **COMMON_REVIEW_FIELDS,
            "draft_schedule_candidates": [{
                "date": None,
                "start_time": None,
                "duration": None,
                "rider": None,
                "horse": None,
                "trainer": None,
                "location": None,
                "conflicts_or_capacity_notes": [],
            }],
            "draft_itinerary_candidates": [],
            "draft_notification_preview": {
                "channels": [],
                "recipients": [],
                "message": None,
                "privacy_safe_copy_required": True,
                "send_allowed": False,
            },
            "calendar_review_boundary": SCHEDULE_REVIEW_BOUNDARY_TEMPLATE,
            "review_questions": [],
            "blocked_actions": [
                *AI_BLOCKED_ACTIONS,
                "calendar_event_create",
                "calendar_event_update",
                "calendar_event_delete",
                "calendar_mutation",
                "participant_notification",
                "automated_notification_send",
                "push_send",
                "sms_send",
                "email_send",
            ],
        })
    if source_type == "training_note":
        return json.dumps({
            "draft_only": True,
            "review_required": True,
            "source_category": "training_note",
            **COMMON_REVIEW_FIELDS,
            "draft_training_note": {
                "horse": None,
                "rider_or_handler": None,
                "trainer": None,
                "date": None,
                "work_summary": None,
                "progress_notes": [],
                "next_steps": [],
                "follow_up_tasks": [],
            },
            "review_questions": [],
            "blocked_actions": ["official_record_save", "medical_or_safety_decision"],
        })
    if source_type == "voice_transcript":
        return json.dumps({
            "draft_only": True,
            "review_required": True,
            "source_category": "voice_transcript",
            **COMMON_REVIEW_FIELDS,
            "voice_capture_context": {
                "hands_free": True,
                "screen_locked_or_multitasking": None,
                "source_quality": None,
            },
            "draft_tasks": [],
            "draft_work_ticket_candidates": [WORK_TICKET_CANDIDATE_TEMPLATE],
            "draft_inventory_candidates": [INVENTORY_CANDIDATE_TEMPLATE],
            "draft_inventory_notes": [],
            "draft_invoice_candidates": [INVOICE_CANDIDATE_TEMPLATE],
            "draft_invoice_notes": [],
            "draft_schedule_candidates": [],
            "draft_schedule_notes": [],
            "draft_training_notes": [],
            "review_questions": [],
            "blocked_actions": ["official_record_save", "ai_autonomous_mutation", "participant_notification", "payment_status_change"],
        })
    if source_type == "health_observation":
        return json.dumps({
            "draft_only": True,
            "review_required": True,
            "source_category": "health_observation",
            **COMMON_REVIEW_FIELDS,
            "not_diagnosis": True,
            "draft_health_observation": {
                "horse": None,
                "observer": None,
                "observed_at": None,
                "appetite": None,
                "water_intake": None,
                "manure_or_urine_notes": None,
                "behavior_or_attitude": None,
                "gait_or_movement": None,
                "vitals_if_provided": {
                    "temperature": None,
                    "heart_rate": None,
                    "respiration_rate": None,
                },
                "symptoms_or_signs": [],
                "injury_or_lameness_flags": [],
                "pain_or_comfort_observations": [],
                "trend_notes": [],
                "recommended_review_role": None,
            },
            "draft_health_score_candidate": {
                "score": None,
                "scale": None,
                "basis": [],
                "confidence": None,
                "requires_human_confirmation": True,
                "official_health_score_save_allowed": False,
            },
            "reviewer_boundary": {
                "candidate_only": True,
                "no_diagnosis": True,
                "vet_or_manager_escalation_decided_by_human": True,
                "do_not_notify_or_save": True,
            },
            "review_questions": [],
            "blocked_actions": [*AI_BLOCKED_ACTIONS, *HEALTH_REVIEW_BLOCKED_ACTIONS],
        })
    return json.dumps({
        "draft_only": True,
        "review_required": True,
        "source_category": source_type,
        **COMMON_REVIEW_FIELDS,
        "draft_records": [],
        "review_questions": [],
        "blocked_actions": ["official_record_save"],
    })


def normalize_draft_payload(parsed: Dict[str, Any], *, source_type: str) -> Dict[str, Any]:
    parsed["draft_only"] = True
    parsed["review_required"] = True
    parsed["source_category"] = source_type

    if not isinstance(parsed.get("review_questions"), list):
        parsed["review_questions"] = []
    if not isinstance(parsed.get("missing_information"), list):
        parsed["missing_information"] = []
    if "review_summary" not in parsed:
        parsed["review_summary"] = None
    if "confidence" not in parsed:
        parsed["confidence"] = None

    blocked_actions = parsed.get("blocked_actions")
    if not isinstance(blocked_actions, list):
        blocked_actions = []
    parsed["blocked_actions"] = blocked_actions
    for action in AI_BLOCKED_ACTIONS:
        if action not in parsed["blocked_actions"]:
            parsed["blocked_actions"].append(action)

    if source_type == "health_observation":
        parsed["not_diagnosis"] = True
        if not isinstance(parsed.get("draft_health_observation"), dict):
            parsed["draft_health_observation"] = {}
        if not isinstance(parsed.get("draft_health_score_candidate"), dict):
            parsed["draft_health_score_candidate"] = {
                "score": None,
                "scale": None,
                "basis": [],
                "confidence": None,
                "requires_human_confirmation": True,
                "official_health_score_save_allowed": False,
            }
        parsed["draft_health_score_candidate"]["requires_human_confirmation"] = True
        parsed["draft_health_score_candidate"]["official_health_score_save_allowed"] = False
        if not isinstance(parsed.get("reviewer_boundary"), dict):
            parsed["reviewer_boundary"] = {}
        parsed["reviewer_boundary"].update({
            "candidate_only": True,
            "no_diagnosis": True,
            "vet_or_manager_escalation_decided_by_human": True,
            "do_not_notify_or_save": True,
        })
        for action in HEALTH_REVIEW_BLOCKED_ACTIONS:
            if action not in parsed["blocked_actions"]:
                parsed["blocked_actions"].append(action)
    if source_type == "lesson_schedule":
        for action in [
            "calendar_event_create",
            "calendar_event_update",
            "calendar_event_delete",
            "calendar_mutation",
            "participant_notification",
            "automated_notification_send",
            "push_send",
            "sms_send",
            "email_send",
        ]:
            if action not in parsed["blocked_actions"]:
                parsed["blocked_actions"].append(action)
        if not isinstance(parsed.get("draft_schedule_candidates"), list):
            parsed["draft_schedule_candidates"] = []
        if not isinstance(parsed.get("draft_itinerary_candidates"), list):
            parsed["draft_itinerary_candidates"] = []
        if not isinstance(parsed.get("draft_notification_preview"), dict):
            parsed["draft_notification_preview"] = {}
        notification_preview = dict(parsed["draft_notification_preview"])
        if not isinstance(notification_preview.get("channels"), list):
            notification_preview["channels"] = []
        if not isinstance(notification_preview.get("recipients"), list):
            notification_preview["recipients"] = []
        notification_preview["privacy_safe_copy_required"] = True
        notification_preview["send_allowed"] = False
        parsed["draft_notification_preview"] = notification_preview
        if not isinstance(parsed.get("calendar_review_boundary"), dict):
            parsed["calendar_review_boundary"] = {}
        calendar_boundary = dict(SCHEDULE_REVIEW_BOUNDARY_TEMPLATE)
        calendar_boundary.update(parsed["calendar_review_boundary"])
        calendar_boundary["requires_human_confirmation"] = True
        calendar_boundary["official_calendar_change_allowed"] = False
        calendar_boundary["participant_notification_allowed"] = False
        calendar_boundary["automated_send_allowed"] = False
        calendar_boundary["recipient_opt_in_review_required"] = True
        calendar_boundary["privacy_safe_copy_review_required"] = True
        parsed["calendar_review_boundary"] = calendar_boundary
    if source_type == "voice_transcript":
        for action in ["participant_notification", "payment_status_change"]:
            if action not in parsed["blocked_actions"]:
                parsed["blocked_actions"].append(action)
    if source_type in {"invoice", "service_invoice", "photo_inventory", "voice_transcript"}:
        _normalize_inventory_candidates(parsed)
        if "inventory_record_create" not in parsed["blocked_actions"]:
            parsed["blocked_actions"].append("inventory_record_create")
    if source_type in {"invoice", "service_invoice"}:
        for action in [
            "payment_status_change",
            "invoice_finalization",
            "charge_money",
            "refund_or_credit",
            "subscription_entitlement_change",
        ]:
            if action not in parsed["blocked_actions"]:
                parsed["blocked_actions"].append(action)
        if not isinstance(parsed.get("draft_payment_status_candidate"), dict):
            parsed["draft_payment_status_candidate"] = {
                "status": "review_required",
                "basis": [],
                "official_payment_status_change_allowed": False,
            }
        parsed["draft_payment_status_candidate"]["official_payment_status_change_allowed"] = False
        if not isinstance(parsed.get("draft_payment_review"), dict):
            parsed["draft_payment_review"] = {}
        payment_review = dict(INVOICE_PAYMENT_REVIEW_TEMPLATE)
        payment_review.update(parsed["draft_payment_review"])
        if not isinstance(payment_review.get("basis"), list):
            payment_review["basis"] = [] if payment_review.get("basis") in (None, "") else [str(payment_review["basis"])]
        payment_review["requires_human_confirmation"] = True
        payment_review["official_payment_status_change_allowed"] = False
        payment_review["invoice_finalization_allowed"] = False
        payment_review["subscription_entitlement_change_allowed"] = False
        parsed["draft_payment_review"] = payment_review
        if not isinstance(parsed.get("draft_reconciliation_questions"), list):
            parsed["draft_reconciliation_questions"] = []
    if source_type == "voice_transcript":
        for key in ["draft_work_ticket_candidates", "draft_schedule_candidates"]:
            if not isinstance(parsed.get(key), list):
                parsed[key] = []

    return parsed


def _normalize_inventory_candidates(parsed: Dict[str, Any]) -> None:
    candidates = parsed.get("draft_inventory_candidates")
    if not isinstance(candidates, list):
        candidates = []
    normalized = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        item = dict(INVENTORY_CANDIDATE_TEMPLATE)
        item.update(candidate)
        if not isinstance(item.get("notes"), list):
            item["notes"] = [] if item.get("notes") in (None, "") else [str(item["notes"])]
        if item.get("review_status") not in INVENTORY_REVIEW_STATUSES:
            item["review_status"] = "needs_review"
        normalized.append(item)
    parsed["draft_inventory_candidates"] = normalized


@dataclass
class StoredSourceBytes:
    bytes_value: bytes
    mime_type: str


class AIStorageClient:
    """Private S3/R2 client for AI source bytes and presigned upload URLs."""

    def __init__(self):
        self.endpoint_url = os.environ.get("AI_STORAGE_ENDPOINT_URL") or os.environ.get("STORAGE_ENDPOINT_URL")
        self.region = os.environ.get("AI_STORAGE_REGION") or os.environ.get("STORAGE_REGION") or "auto"
        self.bucket = os.environ.get("AI_STORAGE_BUCKET") or os.environ.get("STORAGE_BUCKET_NAME") or os.environ.get("STORAGE_BUCKET")
        self.access_key = os.environ.get("AI_STORAGE_ACCESS_KEY_ID") or os.environ.get("STORAGE_ACCESS_KEY_ID")
        self.secret_key = os.environ.get("AI_STORAGE_SECRET_ACCESS_KEY") or os.environ.get("STORAGE_SECRET_ACCESS_KEY")
        self._client = None

    def configured(self) -> bool:
        return all([self.endpoint_url, self.bucket, self.access_key, self.secret_key])

    def _s3(self):
        if not self.configured():
            raise RuntimeError("Private AI storage is not configured")
        if self._client is None:
            import boto3

            self._client = boto3.client(
                "s3",
                endpoint_url=self.endpoint_url,
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
            )
        return self._client

    def presigned_put(self, *, key: str, mime_type: str, ttl_seconds: int = 900) -> str:
        return self._s3().generate_presigned_url(
            "put_object",
            Params={"Bucket": self.bucket, "Key": key, "ContentType": mime_type},
            ExpiresIn=ttl_seconds,
        )

    def read_bytes(self, *, key: str, mime_type: str) -> StoredSourceBytes:
        response = self._s3().get_object(Bucket=self.bucket, Key=key)
        return StoredSourceBytes(bytes_value=response["Body"].read(), mime_type=mime_type)


class OpenAIDraftExtractor:
    """OpenAI-backed extractor. Tests should inject a fake extractor."""

    def __init__(self, *, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model

    def configured(self) -> bool:
        return bool(self.api_key)

    async def extract(
        self,
        *,
        source_type: str,
        prompt: str,
        text: Optional[str] = None,
        file_bytes: Optional[bytes] = None,
        mime_type: Optional[str] = None,
        filename: str = "source",
    ) -> Dict[str, Any]:
        if not self.configured():
            raise RuntimeError("OpenAI extraction is not configured")
        source_type = normalize_source_type(source_type)
        mime_type = (mime_type or "text/plain").lower()
        if text is not None:
            return await self._extract_text(source_type=source_type, prompt=prompt, text=text)
        if not file_bytes:
            raise RuntimeError("No source content provided for extraction")
        if mime_type in AI_IMAGE_MIME:
            return await self._extract_image(
                source_type=source_type,
                prompt=prompt,
                file_bytes=file_bytes,
                mime_type=mime_type,
            )
        if mime_type in AI_TEXT_MIME:
            decoded = file_bytes.decode("utf-8", errors="replace")
            return await self._extract_text(source_type=source_type, prompt=prompt, text=decoded)
        if mime_type == "application/pdf":
            return await self._extract_pdf(
                source_type=source_type,
                prompt=prompt,
                file_bytes=file_bytes,
                filename=filename,
            )
        raise RuntimeError(f"Unsupported extractor mime type: {mime_type}")

    async def _responses(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                OPENAI_RESPONSES_URL,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    def _parse_output(self, response: Dict[str, Any], *, source_type: str) -> Dict[str, Any]:
        text = response.get("output_text") or ""
        if not text:
            for item in response.get("output") or []:
                for content in item.get("content") or []:
                    if content.get("type") == "output_text":
                        text += content.get("text") or ""
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")
            if start < 0 or end <= start:
                raise RuntimeError("AI output was not valid JSON")
            parsed = json.loads(text[start:end + 1])
        return normalize_draft_payload(parsed, source_type=source_type)

    async def _extract_text(self, *, source_type: str, prompt: str, text: str) -> Dict[str, Any]:
        response = await self._responses({
            "model": self.model,
            "input": [{
                "role": "user",
                "content": [{
                    "type": "input_text",
                    "text": (
                        f"{draft_system_instruction()}\nTask: {prompt}\n"
                        f"Required JSON shape: {output_schema_hint(source_type)}\n"
                        f"Source text:\n{text}"
                    ),
                }],
            }],
            "temperature": 0.1,
            "max_output_tokens": 1800,
        })
        return self._parse_output(response, source_type=source_type)

    async def _extract_image(
        self,
        *,
        source_type: str,
        prompt: str,
        file_bytes: bytes,
        mime_type: str,
    ) -> Dict[str, Any]:
        image_url = f"data:{mime_type};base64,{base64.b64encode(file_bytes).decode('ascii')}"
        response = await self._responses({
            "model": self.model,
            "input": [{
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            f"{draft_system_instruction()}\nTask: {prompt}\n"
                            f"Required JSON shape: {output_schema_hint(source_type)}"
                        ),
                    },
                    {"type": "input_image", "image_url": image_url, "detail": "low"},
                ],
            }],
            "temperature": 0.1,
            "max_output_tokens": 1800,
        })
        return self._parse_output(response, source_type=source_type)

    async def _extract_pdf(
        self,
        *,
        source_type: str,
        prompt: str,
        file_bytes: bytes,
        filename: str,
    ) -> Dict[str, Any]:
        attempted_methods = ["openai_file"]
        try:
            parsed = await self._extract_pdf_file(
                source_type=source_type,
                prompt=prompt,
                file_bytes=file_bytes,
                filename=filename,
            )
            return self._with_fallback_metadata(parsed, attempted_methods)
        except Exception:
            pass

        attempted_methods.append("pdf_text")
        text = self._extract_pdf_text(file_bytes)
        if len(text.strip()) >= PDF_TEXT_MIN_CHARS:
            try:
                parsed = await self._extract_text(
                    source_type=source_type,
                    prompt=(
                        f"{prompt}\nFallback context: Direct PDF extraction failed. "
                        "Use this extracted text cautiously and ask review questions "
                        "for missing, garbled, or uncertain fields."
                    ),
                    text=text,
                )
                return self._with_fallback_metadata(parsed, attempted_methods)
            except Exception:
                pass

        attempted_methods.append("pdf_page_images")
        page_images = self._render_pdf_pages_as_data_urls(file_bytes)
        if page_images:
            try:
                parsed = await self._extract_pdf_images(
                    source_type=source_type,
                    prompt=(
                        f"{prompt}\nFallback context: Direct PDF and text extraction "
                        "failed. Review these rendered PDF page images cautiously and "
                        "ask review questions for missing or uncertain fields."
                    ),
                    page_image_urls=page_images,
                )
                return self._with_fallback_metadata(parsed, attempted_methods)
            except Exception:
                pass

        return self._manual_pdf_review_payload(
            source_type=source_type,
            attempted_methods=attempted_methods,
        )

    async def _extract_pdf_file(
        self,
        *,
        source_type: str,
        prompt: str,
        file_bytes: bytes,
        filename: str,
    ) -> Dict[str, Any]:
        safe_filename = filename
        if mimetypes.guess_type(safe_filename)[0] != "application/pdf":
            safe_filename = f"{safe_filename.rsplit('.', 1)[0]}.pdf"
        async with httpx.AsyncClient(timeout=90) as client:
            upload = await client.post(
                OPENAI_FILES_URL,
                headers={"Authorization": f"Bearer {self.api_key}"},
                data={"purpose": "user_data"},
                files={"file": (safe_filename, file_bytes, "application/pdf")},
            )
            upload.raise_for_status()
            file_id = upload.json()["id"]
            try:
                response = await client.post(
                    OPENAI_RESPONSES_URL,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": self.model,
                        "input": [{
                            "role": "user",
                            "content": [
                                {"type": "input_file", "file_id": file_id},
                                {
                                    "type": "input_text",
                                    "text": (
                                        f"{draft_system_instruction()}\nTask: {prompt}\n"
                                        f"Required JSON shape: {output_schema_hint(source_type)}"
                                    ),
                                },
                            ],
                        }],
                        "temperature": 0.1,
                        "max_output_tokens": 1800,
                    },
                )
                response.raise_for_status()
                parsed = self._parse_output(response.json(), source_type=source_type)
                return parsed
            finally:
                await self._delete_openai_file(client, file_id)

    def _extract_pdf_text(self, file_bytes: bytes) -> str:
        try:
            import pymupdf
        except Exception:
            return ""
        try:
            chunks = []
            with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
                for page in doc:
                    chunks.append(page.get_text("text") or "")
            return "\n\n".join(chunk.strip() for chunk in chunks if chunk.strip())
        except Exception:
            return ""

    def _render_pdf_pages_as_data_urls(self, file_bytes: bytes) -> list[str]:
        try:
            import pymupdf
        except Exception:
            return []
        try:
            urls = []
            with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
                for page_index in range(min(len(doc), PDF_IMAGE_FALLBACK_MAX_PAGES)):
                    page = doc[page_index]
                    pixmap = page.get_pixmap(
                        matrix=pymupdf.Matrix(1.5, 1.5),
                        alpha=False,
                    )
                    png_bytes = pixmap.tobytes("png")
                    encoded = base64.b64encode(png_bytes).decode("ascii")
                    urls.append(f"data:image/png;base64,{encoded}")
            return urls
        except Exception:
            return []

    async def _extract_pdf_images(
        self,
        *,
        source_type: str,
        prompt: str,
        page_image_urls: list[str],
    ) -> Dict[str, Any]:
        content = [{
            "type": "input_text",
            "text": (
                f"{draft_system_instruction()}\nTask: {prompt}\n"
                f"Required JSON shape: {output_schema_hint(source_type)}"
            ),
        }]
        content.extend(
            {"type": "input_image", "image_url": url, "detail": "low"}
            for url in page_image_urls
        )
        response = await self._responses({
            "model": self.model,
            "input": [{"role": "user", "content": content}],
            "temperature": 0.1,
            "max_output_tokens": 1800,
        })
        return self._parse_output(response, source_type=source_type)

    def _with_fallback_metadata(
        self,
        parsed: Dict[str, Any],
        attempted_methods: list[str],
    ) -> Dict[str, Any]:
        parsed["extraction_status"] = "draft_ready"
        parsed["fallback_used"] = attempted_methods[-1] if len(attempted_methods) > 1 else None
        parsed["attempted_methods"] = attempted_methods
        return parsed

    def _manual_pdf_review_payload(
        self,
        *,
        source_type: str,
        attempted_methods: list[str],
    ) -> Dict[str, Any]:
        payload = json.loads(output_schema_hint(source_type))
        payload.update({
            "draft_only": True,
            "review_required": True,
            "extraction_status": "manual_review_required",
            "fallback_used": None,
            "attempted_methods": attempted_methods,
            "review_questions": [
                "This PDF could not be read automatically. Please upload a clearer copy or enter the key details manually.",
            ],
            "blocked_actions": [
                *AI_BLOCKED_ACTIONS,
                "automatic_extraction",
            ],
        })
        return payload

    async def _delete_openai_file(self, client: httpx.AsyncClient, file_id: str) -> bool:
        try:
            response = await client.delete(
                f"{OPENAI_FILES_URL}/{file_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            return response.is_success
        except Exception:
            return False
