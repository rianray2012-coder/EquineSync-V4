#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, re, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def read_csv(name):
    with (ROOT/name).open(newline='',encoding='utf-8') as f:
        return list(csv.DictReader(f))

def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

checks=[]
def check(name, ok, detail): checks.append({'check':name,'result':'PASS' if ok else 'FAIL','detail':detail})

required=[
'00_PACKAGE_README.md','01_AUTHORITY_AND_SCOPE.md','02_OPC_REV_006_FOUNDER_APPROVAL_CARRY_FORWARD.md',
'03_FINDING_TREATMENT_AND_GATE_REALIGNMENT_REGISTER.csv','04_SOURCE_ACCESSION_AND_FREEZE_REGISTER.csv',
'05_SOURCE_CONFLICT_AND_SUPERSESSION_REGISTER.csv','06_CROSS_PIA_CONTRACT_INDEX.csv',
'07_OPC_CROSS_PIA_FIELD_CONTRACTS.csv','08_OPC_CROSS_PIA_FIELD_CONTRACTS.json','09_OPC_CROSS_PIA_CONTRACTS.md',
'10_ADR_REGISTER.csv','21_OPC_DATA_FLOW_AND_TRUST_BOUNDARY_MODEL.md','22_OPC_THREAT_MISUSE_REVIEW.csv',
'23_OPC_THREAT_MISUSE_REVIEW.md','24_OPC_OPERATIONAL_TARGET_AND_PROCEDURE_GATE_REGISTER.csv',
'25_OPC_LIFECYCLE_EVIDENCE_CONDITION_REGISTER.csv','26_OPC_PEER_ATTACHMENT_INITIAL_SCOPE_DECISION.md',
'27_OPC_V0_2_DESIGN_APPROVAL_READINESS_REVIEW.md','28_ITEM_10_OPC_V0_2_FOUNDER_DESIGN_APPROVAL_AND_FINDINGS_DISPOSITION_TEMPLATE.md',
'29_ITEM_10_OPC_V0_2_PENDING_EXECUTION_RECEIPT.md','30_OPC_V0_2_DESIGN_APPROVAL_READINESS.xlsx',
'34_SOURCE_AND_AUTHORITY_LIMITATION_RECORD.md']
check('required_files',all((ROOT/x).is_file() for x in required),[x for x in required if not (ROOT/x).is_file()])
findings=read_csv('03_FINDING_TREATMENT_AND_GATE_REALIGNMENT_REGISTER.csv')
check('finding_population',len(findings)==7,len(findings))
check('opc_rev_006_founder_approved',any(r['finding_id']=='OPC-FIND-P1-006' and 'FOUNDER_APPROVED' in r['proposed_disposition'] for r in findings),'carry-forward')
sources=read_csv('04_SOURCE_ACCESSION_AND_FREEZE_REGISTER.csv')
check('source_population',len(sources)==21,len(sources))
contracts=read_csv('06_CROSS_PIA_CONTRACT_INDEX.csv')
fields=read_csv('07_OPC_CROSS_PIA_FIELD_CONTRACTS.csv')
check('contract_population',len(contracts)>=10,len(contracts))
check('field_contract_rows',len(fields)>=30,len(fields))
check('field_contract_required_values',all(all(r.get(k,'').strip() for k in ['contract_id','field_key','source_authority','minimum_read_conditions','portal_write_or_action_boundary','linked_requirements']) for r in fields),'all required fields populated')
adrs=read_csv('10_ADR_REGISTER.csv')
check('adr_population',len(adrs)>=10,len(adrs))
check('adr_files',all((ROOT/r['file']).is_file() for r in adrs),[r['file'] for r in adrs if not (ROOT/r['file']).is_file()])
threats=read_csv('22_OPC_THREAT_MISUSE_REVIEW.csv')
check('threat_population',len(threats)>=36,len(threats))
ops=read_csv('24_OPC_OPERATIONAL_TARGET_AND_PROCEDURE_GATE_REGISTER.csv')
check('operational_gate_population',len(ops)>=20,len(ops))
lc=read_csv('25_OPC_LIFECYCLE_EVIDENCE_CONDITION_REGISTER.csv')
check('lifecycle_population',len(lc)>=8,len(lc))
all_text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in ROOT.rglob('*.md'))
check('no_implementation_authority_claim','implementation authorized: `true`' not in all_text.lower() and 'implementation authority: true' not in all_text.lower() and '`IMPLEMENTATION_AUTHORIZED`' not in all_text,'documentary-only language')
check('v02_hashes_present','c68746f3eb2e1463fca17f81bebce416d420a2f2da7d8b6ba24d9987aff9c09a' in all_text and 'f4a1cf6b7dc66895c943e6aeee80d4812d7d80e1d9a87878249976ffc0244cd5' in all_text,'both source hashes')
check('peer_attachment_deferred','Peer-to-peer attachments are excluded' in (ROOT/'26_OPC_PEER_ATTACHMENT_INITIAL_SCOPE_DECISION.md').read_text(),'explicit scope decision')
overall='PASS' if all(x['result']=='PASS' for x in checks) else 'FAIL'
report={'overall':overall,'checks':checks,'metrics':{'sources':len(sources),'contracts':len(contracts),'field_contract_rows':len(fields),'adrs':len(adrs),'threats':len(threats),'operational_controls':len(ops),'lifecycle_conditions':len(lc)}}
(ROOT/'32_VALIDATION_REPORT.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
lines=['# OPC V0.2 Design-Approval Readiness Validation Report','',f'Overall: `{overall}`','', '## Metrics','']
for k,v in report['metrics'].items(): lines.append(f'- {k}: **{v}**')
lines += ['', '## Checks','', '| Check | Result | Detail |','|---|---|---|']
for c in checks: lines.append(f"| {c['check']} | {c['result']} | {str(c['detail']).replace('|','/')} |")
(ROOT/'33_VALIDATION_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(overall)
sys.exit(0 if overall=='PASS' else 1)
