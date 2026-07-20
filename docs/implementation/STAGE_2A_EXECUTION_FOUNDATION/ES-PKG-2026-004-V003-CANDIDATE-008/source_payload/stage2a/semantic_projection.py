#!/usr/bin/env python3
"""Independent, non-secret semantic projection for captured command output.

This module deliberately does not import or call the evidence redactor.  It
parses sensitive slots independently and preserves every non-sensitive byte so
that over-redaction changes the projection and fails closed.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass


SENSITIVE_KEYS = (
    "authorization",
    "access_token",
    "client_secret",
    "password",
    "api_key",
    "api-key",
    "token",
    "secret",
    "credential",
    "bearer",
)
KEY_PATTERN = "|".join(re.escape(key) for key in sorted(SENSITIVE_KEYS, key=len, reverse=True))
AUTHORIZATION_BEARER = re.compile(
    r"(?i)(?P<prefix>(?:[\"']?authorization[\"']?\s*[:=]\s*)(?:Bearer\s+))"
    r"(?P<value><REDACTED>|[^\s,;]+)"
)
QUOTED_ASSIGNMENT = re.compile(
    rf"(?i)(?P<prefix>[\"']?(?P<key>{KEY_PATTERN})[\"']?\s*[:=]\s*)(?P<quote>[\"'])(?P<value>.*?)(?P=quote)"
)
UNQUOTED_ASSIGNMENT = re.compile(
    rf"(?im)(?P<prefix>(?<![A-Za-z0-9_-])(?P<key>{KEY_PATTERN})(?![A-Za-z0-9_-])\s*[:=]\s*)"
    r"(?P<value>[^\s,;]+)"
)
BARE_BEARER = re.compile(
    r"(?i)(?P<prefix>(?<![A-Za-z0-9_-])Bearer\s+)(?P<value><REDACTED>|[^\s,;]+)"
)
PLACEHOLDER = "<REDACTED>"


@dataclass(frozen=True)
class Projection:
    sha256: str
    sensitive_slot_count: int
    placeholder_slot_count: int
    unredacted_sensitive_count: int
    unexpected_placeholder_count: int
    sensitive_class_counts: dict[str, int]
    serialization: str


def _spans(value: str) -> list[tuple[int, int, int, int, str]]:
    """Return non-overlapping value spans without retaining sensitive values."""
    candidates: list[tuple[int, int, int, int, str, int]] = []
    patterns = (
        (AUTHORIZATION_BEARER, "authorization_bearer", 0),
        (QUOTED_ASSIGNMENT, None, 1),
        (UNQUOTED_ASSIGNMENT, None, 2),
        (BARE_BEARER, "bearer", 3),
    )
    for pattern, fixed_class, priority in patterns:
        for match in pattern.finditer(value):
            key = fixed_class or str(match.groupdict().get("key", "sensitive")).lower()
            candidates.append((match.start(), match.end(), match.start("value"), match.end("value"), key, priority))
    selected: list[tuple[int, int, int, int, str]] = []
    occupied: list[tuple[int, int]] = []
    for start, end, value_start, value_end, key, priority in sorted(candidates, key=lambda row: (row[0], row[5], -(row[1] - row[0]))):
        if any(start < other_end and end > other_start for other_start, other_end in occupied):
            continue
        selected.append((start, end, value_start, value_end, key))
        occupied.append((start, end))
    return sorted(selected, key=lambda row: row[2])


def project_stream(stream: str, value: str, *, sanitized: bool) -> Projection:
    spans = _spans(value)
    pieces: list[str] = [f"STREAM:{stream}\n"]
    cursor = 0
    slot_count = 0
    placeholder_count = 0
    unredacted_count = 0
    class_counts: dict[str, int] = {}
    covered_placeholders: list[tuple[int, int]] = []
    for _start, _end, value_start, value_end, key in spans:
        sensitive_value = value[value_start:value_end]
        pieces.append(value[cursor:value_start])
        pieces.append(f"<SENSITIVE:{key}>")
        cursor = value_end
        slot_count += 1
        class_counts[key] = class_counts.get(key, 0) + 1
        if sensitive_value == PLACEHOLDER:
            placeholder_count += 1
            covered_placeholders.append((value_start, value_end))
        elif sanitized:
            unredacted_count += 1
    pieces.append(value[cursor:])
    unexpected = 0
    for match in re.finditer(re.escape(PLACEHOLDER), value):
        if not any(match.start() >= start and match.end() <= end for start, end in covered_placeholders):
            unexpected += 1
    serialization = "".join(pieces)
    return Projection(
        sha256=hashlib.sha256(serialization.encode()).hexdigest(),
        sensitive_slot_count=slot_count,
        placeholder_slot_count=placeholder_count,
        unredacted_sensitive_count=unredacted_count,
        unexpected_placeholder_count=unexpected,
        sensitive_class_counts=dict(sorted(class_counts.items())),
        serialization=serialization,
    )


def project_outputs(stdout: str, stderr: str, *, sanitized: bool) -> Projection:
    out = project_stream("stdout", stdout, sanitized=sanitized)
    err = project_stream("stderr", stderr, sanitized=sanitized)
    serialization = out.serialization + err.serialization
    counts = dict(out.sensitive_class_counts)
    for key, count in err.sensitive_class_counts.items():
        counts[key] = counts.get(key, 0) + count
    return Projection(
        sha256=hashlib.sha256(serialization.encode()).hexdigest(),
        sensitive_slot_count=out.sensitive_slot_count + err.sensitive_slot_count,
        placeholder_slot_count=out.placeholder_slot_count + err.placeholder_slot_count,
        unredacted_sensitive_count=out.unredacted_sensitive_count + err.unredacted_sensitive_count,
        unexpected_placeholder_count=out.unexpected_placeholder_count + err.unexpected_placeholder_count,
        sensitive_class_counts=dict(sorted(counts.items())),
        serialization=serialization,
    )


def safe_projection_metadata(projection: Projection) -> dict[str, object]:
    """Return persistable metadata; the serialization is intentionally omitted."""
    return {
        "sha256": projection.sha256,
        "sensitive_slot_count": projection.sensitive_slot_count,
        "placeholder_slot_count": projection.placeholder_slot_count,
        "unredacted_sensitive_count": projection.unredacted_sensitive_count,
        "unexpected_placeholder_count": projection.unexpected_placeholder_count,
        "sensitive_class_counts": projection.sensitive_class_counts,
    }


def canonical_metadata(value: dict[str, object]) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()
