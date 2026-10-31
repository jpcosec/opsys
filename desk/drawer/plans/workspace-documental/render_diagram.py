"""Generate a diagram projection; dag.yaml remains the authored task graph."""
from pathlib import Path
import yaml

base = Path(__file__).resolve().parent
data = yaml.safe_load((base / 'dag.yaml').read_text())
tasks = data['tasks']
spec = {'id': 'workspace-documental-dag', 'title': 'Workspace documental: DAG de entregables', 'type': 'component', 'version': '0.1', 'data': {
    'nodes': {t['id']: {'label': t['id'] + ': ' + t['title'], 'kind': 'core'} for t in tasks},
    'edges': [{'from': dep, 'to': t['id'], 'relation': 'prerequisite', 'label': ''} for t in tasks for dep in t['depends_on']]}}
(base / 'dag.diagram.yaml').write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False))
