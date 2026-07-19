#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT/'PACKAGE_MANIFEST.json'

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    errors=[]
    # Parse all JSON files.
    for p in ROOT.rglob('*.json'):
        try:
            json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            errors.append(f'Invalid JSON {p.relative_to(ROOT)}: {e}')
    if not MANIFEST.exists():
        errors.append('Missing PACKAGE_MANIFEST.json')
    else:
        m=json.loads(MANIFEST.read_text(encoding='utf-8'))
        listed={x['path']:x for x in m['files']}
        for rel, item in listed.items():
            p=ROOT/rel
            if not p.exists():
                errors.append(f'Missing manifest file: {rel}')
                continue
            if p.stat().st_size != item['bytes']:
                errors.append(f'Byte count mismatch: {rel}')
            if sha256(p) != item['sha256']:
                errors.append(f'Hash mismatch: {rel}')
        actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name not in {'PACKAGE_MANIFEST.json','SHA256SUMS.txt'} and not str(p.relative_to(ROOT)).startswith('validation/')}
        missing=actual-set(listed)
        extra=set(listed)-actual
        if missing: errors.append('Unlisted files: '+', '.join(sorted(missing)))
        if extra: errors.append('Manifest entries without files: '+', '.join(sorted(extra)))
    if errors:
        print('PACKAGE VALIDATION FAILED')
        for e in errors: print('- '+e)
        return 1
    print('PACKAGE VALIDATION PASSED')
    return 0

if __name__=='__main__':
    sys.exit(main())
