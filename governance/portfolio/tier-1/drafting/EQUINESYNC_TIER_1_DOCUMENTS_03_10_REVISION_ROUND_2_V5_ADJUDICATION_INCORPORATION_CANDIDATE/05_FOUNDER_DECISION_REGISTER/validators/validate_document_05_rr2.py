#!/usr/bin/env python3
from pathlib import Path
import sys

doc = Path(__file__).resolve().parents[1]
required = [p for p in doc.iterdir() if p.suffix in {'.csv', '.json', '.md'}]
if not required:
    print('DOCUMENT_05_VALIDATION_FAIL no artifacts')
    raise SystemExit(1)
print('DOCUMENT_05_VALIDATION_PASS artifacts=' + str(len(required)))
