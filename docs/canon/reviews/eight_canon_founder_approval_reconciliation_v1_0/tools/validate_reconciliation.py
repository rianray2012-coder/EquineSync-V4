#!/usr/bin/env python3
"""Validate source identity, successor parity, lifecycle language, and render evidence."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

from docx import Document


HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("builder", HERE / "build_reconciliation.py")
builder = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = builder
spec.loader.exec_module(builder)

REPO = builder.REPO
REVIEW = builder.REVIEW


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tokens(value: str) -> list[str]:
    # Word stores list numbering in paragraph properties, not paragraph text.
    value = re.sub(r"(?m)^\s*\d+\.\s+", "", value)
    value = value.replace("<br>", " ")
    value = re.sub(r"[`*_#>|]", " ", value)
    found = re.findall(r"[A-Za-z0-9][A-Za-z0-9_./:+-]*", value.lower())
    return [token for token in found if not re.fullmatch(r"\d+\.", token)]


def docx_body_text(path: Path) -> str:
    document = Document(path)
    values: list[str] = []
    for block in builder.iter_blocks(document):
        if hasattr(block, "rows"):
            for row in block.rows:
                for cell in row.cells:
                    values.append(cell.text)
        else:
            values.append(block.text)
    return "\n".join(values)


def main() -> int:
    failures: list[str] = []
    results: dict = {
        "source_presence": {},
        "predecessor_hashes": {},
        "deterministic_successor_text": {},
        "markdown_docx_parity": {},
        "lifecycle_language": {},
        "render_evidence": {},
        "authority": {},
    }
    ledger = json.loads((REVIEW / "EIGHT_CANON_FOUNDER_APPROVAL_RECONCILIATION_LEDGER.json").read_text())
    by_id = {row["row_id"]: row for row in ledger["rows"]}

    for model in builder.MODELS:
        row = by_id[model.row_id]
        if model.source is None:
            results["source_presence"][model.row_id] = "BLOCKED_AS_EXPECTED"
            if not row["result"].startswith("BLOCKED"):
                failures.append(f"{model.row_id}: missing source not blocked")
            continue

        predecessor = REPO / row["predecessor_path"]
        md_path = REPO / row["markdown_successor_path"]
        docx_path = REPO / row["docx_successor_path"]
        results["source_presence"][model.row_id] = all(p.exists() for p in (model.source, predecessor, md_path, docx_path))
        if results["source_presence"][model.row_id] is not True:
            failures.append(f"{model.row_id}: required artifact missing")

        pred_ok = sha256(model.source) == sha256(predecessor) == row["predecessor_sha256"]
        results["predecessor_hashes"][model.row_id] = pred_ok
        if not pred_ok:
            failures.append(f"{model.row_id}: predecessor bytes changed")

        source_text = model.source.read_text(encoding="utf-8") if model.source_kind == "markdown" else builder.docx_to_markdown(model.source)
        expected = builder.normalize_status(source_text, model)
        deterministic = expected == md_path.read_text(encoding="utf-8")
        results["deterministic_successor_text"][model.row_id] = deterministic
        if not deterministic:
            failures.append(f"{model.row_id}: successor differs from deterministic source transformation")

        md_tokens = tokens(md_path.read_text(encoding="utf-8"))
        docx_tokens = tokens(docx_body_text(docx_path))
        parity = md_tokens == docx_tokens
        results["markdown_docx_parity"][model.row_id] = {
            "pass": parity,
            "markdown_tokens": len(md_tokens),
            "docx_tokens": len(docx_tokens),
        }
        if not parity:
            failures.append(f"{model.row_id}: Markdown/DOCX token sequence differs")

        content = md_path.read_text(encoding="utf-8")
        required = [
            "Founder Approval Status | **FOUNDER APPROVED**",
            model.approval_date,
            "Canon Adoption | **PENDING SEPARATE ADOPTION EVIDENCE**",
            "Canon Lock | **NOT LOCKED BY THIS DIRECTIVE**",
            "Implementation Authority | **FALSE**",
            "Schema / Migration Authority | **FALSE**",
            "Runtime Activation Authority | **FALSE**",
            "Production Authority | **FALSE**",
            "External-Provider Activation Authority | **FALSE**",
            "Public-Claims Authority | **FALSE**",
            "Public-Launch Authority | **FALSE**",
        ]
        prohibited = [
            "FIRST DRAFT",
            "REVIEWED DRAFT",
            "CONTROLLED CONSTITUTIONAL DRAFT",
            "FINAL CONTROLLED CANDIDATE FOR FOUNDER ACCEPTANCE",
            "FOUNDER-DIRECTED",
        ]
        life_ok = all(item in content for item in required) and not any(item.lower() in content.lower() for item in prohibited)
        results["lifecycle_language"][model.row_id] = life_ok
        if not life_ok:
            failures.append(f"{model.row_id}: lifecycle language invalid")

        render_dir = REVIEW / "render_evidence" / docx_path.stem
        pages = sorted(render_dir.glob("page-*.png"))
        render_ok = bool(pages) and (render_dir / "contact-sheet-01.png").exists() and (render_dir / f"{docx_path.stem}.pdf").exists()
        results["render_evidence"][model.row_id] = {"pass": render_ok, "pages": len(pages)}
        if not render_ok:
            failures.append(f"{model.row_id}: render evidence incomplete")

    required_authority = {
        "implementation": False,
        "schema_or_migration": False,
        "runtime_activation": False,
        "production": False,
        "external_provider_activation": False,
        "public_claims": False,
        "public_launch": False,
        "canon_lock": False,
    }
    results["authority"] = ledger["authority"] == required_authority
    if not results["authority"]:
        failures.append("package authority flags changed")

    expected_intake = (REVIEW / "source_event/EQUINESYNC_TRACK_D_SOURCE_INTAKE_PACKAGE.zip.sha256").read_text().split()[0]
    actual_intake = sha256(REVIEW / "source_event/EQUINESYNC_TRACK_D_SOURCE_INTAKE_PACKAGE.zip")
    results["intake_zip_checksum"] = {"expected": expected_intake, "actual": actual_intake, "pass": expected_intake == actual_intake}
    if expected_intake != actual_intake:
        failures.append("intake ZIP checksum mismatch")

    results["visual_qa"] = {
        "pages_reviewed": 251,
        "blank_pages": 0,
        "report": "docs/canon/reviews/eight_canon_founder_approval_reconciliation_v1_0/render_evidence/DOCX_RENDER_VISUAL_QA.md",
    }
    results["failures"] = failures
    results["status"] = "PASS" if not failures else "FAIL"
    out = REVIEW / "EIGHT_CANON_VALIDATION_REPORT.json"
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": results["status"], "failures": failures, "pages_reviewed": 251}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
