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
# Cheap review state is checked against current inputs; pending is never reported as reviewed.
sys.path.insert(0,str(B))
import context_review as cr
assert d['status'] in ('expert_reviewed_pending_cheap_context_reviews_and_decisions','cheap_context_reviewed_pending_decisions','final_plan_pending_current_reviews','final_plan_reviewed')
assert d['execution_authorized'] is False
h=d['hierarchy'];pk={p['id']:p for p in h['packages']}
assert h['root']['id']=='ROOT' and h['root']['children']==list(pk)
members=[c for p in h['packages'] for c in p['children']]
assert sorted(members)==sorted(f'WS{i:02d}' for i in range(1,1+max(int(t['id'][2:]) for t in d['tasks'] if '.' not in t['id']))),'package membership must be unique and cover WS01-WS44'
for t in ts.values():
    assert t['node_role'] in ('delivery','aggregate'),t['id']
    if t['node_role']=='aggregate':
        assert t['children'] and set(t['children'])<=set(t['depends_on']),t['id']
        assert all(ts[c]['parent_id']==t['id'] for c in t['children']),t['id']
    if t.get('parent_id'):
        assert t['id'] in ts[t['parent_id']]['children'] and t['parent_id'] not in t['depends_on'],t['id']
review_problems=cr.stale_reviews(d)
if d['status'] in ('cheap_context_reviewed_pending_decisions','final_plan_reviewed'):
    assert not review_problems,review_problems
assert 'expert' in d['council_review']['scope'].lower() and 'cheap' in d['council_review']['scope'].lower()

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
    if g.get('evaluation')=='per_delta':
        assert set(g.get('accepted_scope_nodes',[])) <= set(g['scope_nodes']),name
        if g['state']=='satisfied':assert set(g['accepted_scope_nodes'])==set(g['scope_nodes']), (name,'global satisfied requires every delta receipt')
        receipts=g.get('verified_delta_receipts',{})
        for nid in g['accepted_scope_nodes']:
            receipt=receipts.get(nid,{})
            assert all(receipt.get(k) for k in ('actor','date','commit','blob','scope','effect','repo')), (name,nid,'delta lacks exact receipt')
            repo=(R/d['repo_roots'][receipt['repo']]).resolve()
            for ref in (receipt['commit'],receipt['blob']):
                subprocess.run(['git','-C',str(repo),'cat-file','-e',ref],check=True,capture_output=True)
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
completed={t['id'] for t in ts.values() if t.get('covered_work',{}).get('state')=='documented_not_task_closed'}
def gate_holds(gid,nid):
    g=gs[gid]
    return g['state']=='satisfied' or (g.get('evaluation')=='per_delta' and nid in g.get('accepted_scope_nodes',[]))
for nid in completed:
    refs=ts[nid]['covered_work']['evidence']
    assert isinstance(refs,list) and refs, 'coverage must have verifiable sources'
    for ref in refs:
        assert hashlib.sha256((R/ref['path']).read_bytes()).hexdigest()==ref['sha256'],nid
ready=[];blocked={}
for t in ts.values():
    reasons=[p for p in t['depends_on'] if p not in completed]+[g for g in t['requires'] if not gate_holds(g,t['id'])]
    for condition in ([t['enabled_when']] if t.get('enabled_when') else []) + [v['when'] for v in t.get('variants',[])]:
        param=d['parameters'][condition['parameter']]['value']
        if param=='pending':reasons.append('decision:'+condition['parameter'])
    for variant in t.get('variants',[]):
        if d['parameters'][variant['when']['parameter']]['value']==variant['when']['equals']:
            reasons += [x for x in variant['depends_on'] if x not in completed] + [x for x in variant['requires'] if not gate_holds(x,t['id'])]
    if t['id'] in completed:continue
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
review_counts={}
for n in cr.all_nodes(d):review_counts[n['context_review']['status']]=review_counts.get(n['context_review']['status'],0)+1
lines=['STRUCTURE/COHERENCE: PASS',f'Context review states: {review_counts}; stale or pending problems: {len(review_problems)}',f'{len(ts)} candidate nodes; {len(gs)} explicit gates; no cycles (including gate producers).',
'Generated README/table/task files/diagram spec match canonical YAML.',
'Council APTO is expert planning review only; structural PASS is not execution-ready. execution_authorized=false.',
'Planning candidates preparable after documentary coverage verification: '+', '.join(ready),
'Execution authorized: NONE. Pending decisions and external/human gates do not pass by file existence.',
'Currently blocked candidates: '+str(len(blocked)),*evidence_checks,*refs,
'No product code changed; this validates planning artifacts, not user journeys or functionality.']
text='\n'.join(lines)+'\n'
if args.check:
    assert (B/'validation.txt').read_text()==text,'validation.txt is stale'
else:
    (B/'validation.txt').write_text(text)
print('\n'.join(lines))
