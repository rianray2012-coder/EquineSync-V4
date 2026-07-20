#!/usr/bin/env python3
"""Bounded command used only to validate evidence capture semantics."""
from __future__ import annotations

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("result", choices=["pass", "intentional-fail"])
args = parser.parse_args()
print(f"stage2a foundation example: {args.result}")
raise SystemExit(0 if args.result == "pass" else 7)
