"""Validate this planning DAG; never infer dispatch authorization from acyclicity."""
from pathlib import Path
import argparse
import hashlib
import re
import subprocess
import sys
import yaml
parser=argparse.ArgumentParser()
parser.add_argument('--check',action='store_true',help='check without writing validation.txt')
args=parser.parse_args()
B=Path(__file__).resolve().parent
R=B.parents[3]
d=yaml.safe_load((B/'dag.yaml').read_text())
ts={t['id']:t for t in d['tasks']};gs=d['gates']
assert len(ts)==len(d['tasks']), 'duplicate task IDs'
assert not set(ts)&set(gs), 'task/gate collision'
subprocess.run([sys.executable,str(B/'build_plan.py'),'--check'],check=True)
for t in ts.values():
    assert t['owner_repo'] in ('deskops','graph_ui','sldb','spec2viz'), t['id']
    assert all(p in ts for p in t['depends_on']),t['id']
    assert all(p in gs for p in t['requires']),t['id']
    assert (R/t['task_file']).is_file(),t['id']
    for variant in t.get('variants',[]):
        assert variant['when']['parameter'] in d['parameters']
        assert all(x in ts for x in variant['depends_on'])
        assert all(x in gs for x in variant['requires'])
    assert t.get('output_base'),t['id']
    assert t['estimate'] in ('S','M') and t['acceptance'] and t['output_scope'],t['id']
    assert t['status']=='candidate', 'this plan cannot authorize execution'
for param in d.get('parameters',{}).values():
    assert param['value'] in param['allowed'],param
for name,g in gs.items():
    if 'scope_nodes' in g: assert set(g['scope_nodes'])=={t['id'] for t in ts.values() if name in t['requires']},name
    assert g['state'] in ('pending','blocked','unverified','satisfied') and g['evidence'],g
    if g.get('produced_by'): assert g['produced_by'] in ts
    if g['state']=='satisfied':assert g.get('verified_evidence'), 'satisfied gate lacks receipt'
# Include gate producer edges in structural cycle detection.
spec=yaml.safe_load((B/'dag.diagram.yaml').read_text())['data']
remaining=set(spec['nodes']);closed=set();layers=[]
while remaining:
    ready=sorted(n for n in remaining if all(e['from'] in closed for e in spec['edges'] if e['to']==n))
    assert ready, 'cycle including gate production'
    layers.append(ready);closed.update(ready);remaining.difference_update(ready)
# Internal planning readiness only: tasks are not complete simply because files exist.
completed={t['id'] for t in ts.values() if t['status']=='complete'}
ready=[];blocked={}
for t in ts.values():
    reasons=[p for p in t['depends_on'] if p not in completed]+[g for g in t['requires'] if gs[g]['state']!='satisfied']
    for condition in ([t['enabled_when']] if t.get('enabled_when') else []) + [v['when'] for v in t.get('variants',[])]:
        param=d['parameters'][condition['parameter']]['value']
        if param=='pending':reasons.append('decision:'+condition['parameter'])
    for variant in t.get('variants',[]):
        if d['parameters'][variant['when']['parameter']]['value']==variant['when']['equals']:
            reasons += [x for x in variant['depends_on'] if x not in completed] + [x for x in variant['requires'] if gs[x]['state']!='satisfied']
    if t.get('enabled_when') and d['parameters'][t['enabled_when']['parameter']]['value'] not in ('pending',t['enabled_when']['equals']):
        blocked[t['id']]=['not_in_selected_delivery'];continue
    if reasons:blocked[t['id']]=reasons
    else:ready.append(t['id'])
evidence_checks=[]
for name,g in gs.items():
    if g.get('evidence_ref'):
        ref=g['evidence_ref'];repo=(R/d['repo_roots'][ref['repo']]).resolve()
        assert not Path(ref['path']).is_absolute() and '..' not in Path(ref['path']).parts,name
        result=subprocess.run(['git','-C',str(repo),'check-ignore','--no-index',ref['path']],capture_output=True,text=True)
        assert result.returncode==1,f'gate evidence ignored or unverifiable: {name}: {result.stdout}{result.stderr}'
        evidence_checks.append(name+': receipt location versionable under current gitignore')
refs=[]
for name,ref in d['external_references'].items():
    p=R/ref['path'];exists=p.is_file()
    same=exists and hashlib.sha256(p.read_bytes()).hexdigest()==ref['sha256']
    refs.append(f'{name}: '+('observed path/hash unchanged' if same else 'CHANGED/MISSING; reconcile before promotion'))
# Check local Markdown links in authored/generated docs, excluding archived reviews.
for p in [B/'README.md',*B.glob('borradores/*.md'),*Path(R/'desk/drawer/tasks/workspace-documental').glob('*.md')]:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in link or link.startswith('#'):continue
        assert (p.parent/link.split('#')[0]).exists(),f'broken link {p}: {link}'
lines=['STRUCTURE/COHERENCE: PASS',f'{len(ts)} candidate deliveries; {len(gs)} explicit gates; no cycles (including gate producers).',
'Generated README/table/task files/diagram spec match canonical YAML.',
'Planning candidates with no prerequisite: '+', '.join(ready),
'Execution authorized: NONE. Pending decisions and external/human gates do not pass by file existence.',
'Currently blocked candidates: '+str(len(blocked)),*evidence_checks,*refs,
'No product code changed; this validates planning artifacts, not user journeys or functionality.']
text='\n'.join(lines)+'\n'
if args.check:
    assert (B/'validation.txt').read_text()==text,'validation.txt is stale'
else:
    (B/'validation.txt').write_text(text)
print('\n'.join(lines))
