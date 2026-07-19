#!/usr/bin/env python3
from pathlib import Path
import argparse

DIRS = [
 '00_authorization','01_frozen_package/source_materials','02_drafting_agent','03_segregated_review',
 '04_adversarial_challenge','05_machine_validation/logs','06_evidence_custodian','07_domain_review',
 '08_synthetic_golden_path','09_executable_reproduction/logs','09_executable_reproduction/screenshots',
 '09_executable_reproduction/audit_evidence','09_executable_reproduction/failure_evidence',
 '10_remediation','11_verification','12_founder_disposition','13_closure'
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cycle-id', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    root = Path(args.output) / args.cycle_id
    if root.exists():
        raise SystemExit(f'Refusing to overwrite existing review cycle: {root}')
    for d in DIRS:
        (root/d).mkdir(parents=True, exist_ok=True)
    (root/'REVIEW_CYCLE_ID').write_text(args.cycle_id+'\n', encoding='utf-8')
    print(root)

if __name__ == '__main__':
    main()
