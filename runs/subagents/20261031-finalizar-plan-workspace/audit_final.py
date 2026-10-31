from pathlib import Path
import sys,yaml,json,hashlib,copy,subprocess,datetime
B=Path('desk/drawer/plans/workspace-documental');R=Path('runs/subagents/20261031-finalizar-plan-workspace');sys.path.insert(0,str(B));import context_review as c
D=yaml.safe_load((B/'dag.yaml').read_text());rows=[];seen=set();pids=set()
logs=['runner-final.log','runner-round2.log','runner-round3.log','runner-macro-sequence.log','runner-contract-final.log']
versions=json.loads((R/'runner-source-versions.json').read_text())
for log in logs:
 for line in (R/log).read_text().splitlines():
  nid,ok,path=line.split(' ',2);a=Path(path);assert ok=='ok' and path not in seen,(log,line);seen.add(path)
  m=json.loads((a/'manifest.json').read_text());r=json.loads((a/'receipt.json').read_text())
  assert not r['technical_failure'] and r['returncode']==0 and r['stdin']=='devnull'
  assert r['pid']>0 and r['pid'] not in pids;r['pid'] and pids.add(r['pid'])
  version_observation=json.loads((R/'pi-version-provenance.json').read_text())
  assert r['pi_version'] or version_observation['version']=='0.67.3'
  for flag in ['--offline','--no-session','--no-context-files','--no-skills','--no-extensions','--no-prompt-templates','--no-tools']:assert flag in r['argv'],(nid,flag)
  assert '--resume' not in r['argv'] and '--continue' not in r['argv']
  assert m['provider']=='deepseek' and m['model']=='deepseek-flash' and m['thinking']=='low'
  assert r['argv']==m['argv'] and r['argv'][-1]=='@'+str(a/'input.md')
  assert c.sha((a/'input.md').read_bytes())==m['input_sha256']==r['input_sha256']==a.parent.name
  assert c.sha((a/'output.md').read_bytes())==r['output_sha256'] and (a/'output.md').stat().st_size>0
  assert (a/'disposition.md').is_file()
  # Supplied sources are plan authored text/canonical fragments, no prior review/output or oral fixes.
  for source in m['ordered_sources']:
   assert not any(x in source['path'] for x in ('/context-review/','output.md','disposition.md','preflight','cold-')),(nid,source)
  v=versions['versions'][versions['logs'][log]]
  supplement={'audit_at':datetime.datetime.now(datetime.UTC).isoformat(),'kind':'post-run runner-source provenance supplement; original receipt unchanged','batch_log':str(R/log),'runner_source':v,'node_id':nid,'input_sha256':r['input_sha256']}
  supplement['pi_version_observation']=str(R/'pi-version-provenance.json')
  supplement_path=a/'runner-source-receipt.json'
  if supplement_path.exists():
   prior=json.loads(supplement_path.read_text());assert prior['node_id']==nid and prior['input_sha256']==r['input_sha256'] and prior['runner_source']==v
  else:supplement_path.write_text(json.dumps(supplement,ensure_ascii=False,indent=2))
  rows.append({'node':nid,'path':path,'log':log,'input_sha256':r['input_sha256'],'pid':r['pid'],'technical_failure':False})
assert len(rows)==243,len(rows)
assert not c.stale_reviews(D),c.stale_reviews(D)
for n in c.all_nodes(D):
 a=Path(n['context_review']['evidence'][0]);data,_=c.bundle(D,n)
 assert str(a) in seen and (a/'input.md').read_bytes()==data,n['id']
 assert n['context_review']['status']=='reviewed' and 'State: accepted_current' in (a/'disposition.md').read_text(),n['id']
 assert n['context_review']['contract_sha256']==c.sha(c.canonical(n).encode())
E=copy.deepcopy(D)
for n in c.all_nodes(E):n['context_review']={'status':'pending','evidence':['metadata-only-audit']}
for x,y in zip(c.all_nodes(D),c.all_nodes(E)):
 assert c.bundle(D,x)[0]==c.bundle(E,y)[0] and c.canonical(x)==c.canonical(y),x['id']
assert D['status']=='final_plan_reviewed' and D['execution_authorized'] is False
T={t['id']:t for t in D['tasks']};assert len(T)==63 and len(c.all_nodes(D))==72
assert all(t['status']=='candidate' for t in T.values())
assert D['parameters']['source_mode']['value']=='editable' and D['gates']['G_SOURCE']['state']=='pending'
assert all(D['gates'][g]['state']=='pending' for g in ('G_HUMAN_READ','G_HUMAN_MANUAL','G_HUMAN_MODEL','G_HUMAN_DELEGATE','G_EXEC'))
assert D['gates']['G_SCION']['state']=='unverified'
assert all(D['gates'][g]['state']=='satisfied' for g in ('G_PRODUCT','G_WRITE_POLICY','G_CLOSEOUT'))
assert 'WS18' not in T['WS24']['depends_on'] and not any(n in T['WS31']['depends_on'] for n in ('WS29','WS39','WS37'))
for n in ('WS33','WS33.1','WS33.2'):assert 'G_WRITE_CONTRACT' in T[n]['requires'] and n in D['gates']['G_WRITE_CONTRACT']['scope_nodes']
for g in D['gates'].values():
 if g.get('evaluation')=='per_delta':assert g['accepted_scope_nodes']==[]
cmd=json.loads((R/'tester-closeout-command.json').read_text());assert cmd['exit_code']==0
assert '23 passed, 3 deselected' in (R/'tester-closeout-pytest.log').read_text()
summary={'new_attempts':len(rows),'current_nodes':len(c.all_nodes(D)),'stale':0,'technical_failures':0,'unique_pids':len(pids),'provider':'deepseek','model':'deepseek-flash','thinking':'low','stdin':'devnull','execution_authorized':False,'candidate_nodes':len(T),'review_logs':{log:sum(x['log']==log for x in rows) for log in logs},'attempts':rows}
(R/'final-review-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
source_paths=[p for p in B.rglob('*') if p.is_file() and '__pycache__' not in p.parts and 'reviews' not in p.parts]+list(Path('desk/drawer/tasks/workspace-documental').glob('*.md'))
(R/'final-frozen-sources.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.UTC).isoformat(),'files':{str(p):c.sha(p.read_bytes()) for p in source_paths}},ensure_ascii=False,indent=2))
print('PASS semantic/audit: 243 real new model receipts; 72 current accepted node inputs, zero stale/failures; exact hashes, distinct pids, isolation/DEVNULL and no prior outputs supplied.')
print('PASS limits: 63 candidates, execution_authorized=false, no technical reception fabricated, G_SOURCE/Scion/human use pending; WS33 own per-effect contract required.')
print('PASS metadata: changing only context_review does not change any current node input/contract; no invalidation bug.')
print('G_CLOSEOUT: independent targeted tester 23 passed/3 deselected exit0; no global-suite claim.')
