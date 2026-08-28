from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from services.ai_draft_extractor import (
    OpenAIDraftExtractor,
    ai_live_extraction_verification_snapshot,
    openai_api_key_mode,
)


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "backend" / "scripts" / "ai_live_extraction_verification.py"


def test_ai_live_extraction_snapshot_is_redacted_and_gated():
    snapshot = ai_live_extraction_verification_snapshot(env={
        "OPENAI_API_KEY": "sk-proj-secret-should-not-render",
        "OPENAI_EXTRACTION_MODEL": "gpt-4.1-mini",
        "RUN_AI_LIVE_EXTRACTION_PROOF": "0",
    })

    assert snapshot == {
        "provider": "openai",
        "activation_target": "live_extraction_verification",
        "api_key_mode": "project_secret_configured",
        "model": "gpt-4.1-mini",
        "proof_enabled": False,
        "api_key_configured": True,
        "ready_to_run_live_proof": False,
        "draft_only": True,
        "review_required": True,
        "official_record_save_enabled": False,
        "autonomous_mutation_enabled": False,
    }
    assert "sk-proj-secret-should-not-render" not in json.dumps(snapshot)


def test_ai_live_extraction_snapshot_can_be_ready_without_save_authority():
    snapshot = ai_live_extraction_verification_snapshot(env={
        "OPENAI_API_KEY": "sk-test-shape-only",
        "OPENAI_EXTRACTION_MODEL": "gpt-4.1-mini",
        "RUN_AI_LIVE_EXTRACTION_PROOF": "1",
    })

    assert snapshot["api_key_mode"] == "secret_configured"
    assert snapshot["ready_to_run_live_proof"] is True
    assert snapshot["official_record_save_enabled"] is False
    assert snapshot["autonomous_mutation_enabled"] is False


def test_openai_key_mode_never_returns_secret_material():
    assert openai_api_key_mode("") == "missing"
    assert openai_api_key_mode("sk-proj-abc123") == "project_secret_configured"
    assert openai_api_key_mode("sk-abc123") == "secret_configured"
    assert "abc123" not in openai_api_key_mode("sk-proj-abc123")


def test_ai_output_parse_forces_draft_flags_and_blocked_actions():
    extractor = OpenAIDraftExtractor(api_key="test-key")
    parsed = extractor._parse_output({
        "output_text": json.dumps({
            "draft_records": [{"title": "Candidate"}],
            "blocked_actions": ["billing_status_change"],
        })
    }, source_type="voice_transcript")

    assert parsed["draft_only"] is True
    assert parsed["review_required"] is True
    assert parsed["source_category"] == "voice_transcript"
    assert "official_record_save" in parsed["blocked_actions"]
    assert "ai_autonomous_mutation" in parsed["blocked_actions"]
    assert "billing_status_change" in parsed["blocked_actions"]


def test_ai_live_proof_script_is_blocked_without_explicit_enablement():
    env = os.environ.copy()
    env.pop("OPENAI_API_KEY", None)
    env["RUN_AI_LIVE_EXTRACTION_PROOF"] = "0"

    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        env=env,
        check=True,
        text=True,
        capture_output=True,
        timeout=30,
    )
    body = json.loads(result.stdout)
    assert body["status"] == "blocked"
    assert body["snapshot"]["ready_to_run_live_proof"] is False
    assert body["snapshot"]["official_record_save_enabled"] is False
    assert body["snapshot"]["autonomous_mutation_enabled"] is False
    assert "OPENAI_API_KEY" in body["reason"]
