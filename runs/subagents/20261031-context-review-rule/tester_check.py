"""Independent checks against actual authored sources and generated artifacts."""
from pathlib import Path
import hashlib, json, re, subprocess, sys, yaml
ROOT=Path.cwd()
RUN=ROOT/'runs/subagents/20261031-context-review-rule'
sys.path.insert(0,str(ROOT))
from deskops.models import AtomDoc, RitualDoc
from sldb.runtime.validation import extract_model_data,render_model_markdown
paths=[('desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md',AtomDoc),*[(f'desk/rituals/{name}.md',RitualDoc) for name in ('context-review','execution','phase')]]
for name,model in paths:
 text=(ROOT/name).read_text();data=extract_model_data(model,text);model.model_validate(data)
 rendered=render_model_markdown(model,data)
 assert extract_model_data(model,rendered)==data,name
 print('PASS model extraction/render/extraction equality:',name)
for name in [p for p,m in paths]+['docs/workflow-policy-reference.md','.pi/skills/deskops-task-lifecycle/SKILL.md']:
 p=ROOT/name
 for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in link or link.startswith('#') or '<' in link:continue
  assert (p.parent/link.split('#')[0]).exists(),(name,link)
 print('PASS local Markdown links:',name)
baseline=json.loads((RUN/'tester-plan-baseline.json').read_text())
dag=yaml.safe_load((ROOT/'desk/drawer/plans/workspace-documental/dag.yaml').read_text())
assert len(dag['tasks'])==44
assert dag['status']=='expert_reviewed_pending_cheap_context_reviews_and_decisions'
required={'status':'pending','required_protocol':'ritual-context-review','evidence':[]}
assert dag['hierarchy_context_review']==required
assert all(t['context_review']==required for t in dag['tasks'])
print('PASS root + 44 task reviews remain pending without invented evidence')
# Strip only authorized metadata additions, comparing the full remaining canonical plan.
new=json.loads(json.dumps(dag));old=json.loads(json.dumps(baseline))
new.pop('hierarchy_context_review');new['status']=old['status'];new['council_review']['scope']=old['council_review'].get('scope')
if 'scope' not in old['council_review']:new['council_review'].pop('scope')
for t in new['tasks']:t.pop('context_review')
assert new==old,'plan changed beyond explicitly authorized metadata'
print('PASS all product decisions, task scopes, dependencies and gates unchanged')
for t in dag['tasks']:
 text=(ROOT/t['task_file']).read_text()
 assert 'pending' in text and 'ritual-context-review' in text,t['id']
print('PASS all 44 generated task sheets materialize pending protocol')
receipt=json.loads((RUN/'receipt.json').read_text())
for item in receipt['inputs']:
 assert hashlib.sha256((RUN/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
assert receipt['model']=='deepseek-flash' and receipt['provider']=='deepseek'
for flag in ('--no-session','--no-context-files','--no-skills','--no-extensions','--no-prompt-templates','--no-tools'):
 assert flag in receipt['isolation_flags'],flag
print('PASS real cheap-review saved inputs match receipt hashes and isolation flags')
