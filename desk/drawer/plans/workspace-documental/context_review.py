"""Run cheap isolated context reviews of plan nodes under ritual-context-review.

Writes evidence only under runs/subagents/20261031-workspace-context-reviews/.
`run` launches one fresh Pi process per node and attempt; `status` compares current inputs
with recorded reviews without calling any model.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

import yaml

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
RUN = ROOT / 'runs/subagents/20261031-workspace-context-reviews/context-review'
PLAN = B.relative_to(ROOT)
MAX_TECHNICAL = 3
TIMEOUT = 150
SYSTEM = (
    'Revisor barato aislado de un encargo de planificación. Trabajas solo con el input explícito: '
    'sin herramientas, historial ni otras fuentes. No ejecutas nada. Responde en español con estas '
    'secciones exactas: REFORMULACION (propósito, resultado, repo, límites), AMBIGUEDADES (numeradas, '
    'cada una con cita textual del input y qué obligaría a inventar; escribe "ninguna" si no hay), '
    'DRY-RUN (lecturas, cambios previstos, dependencias y validaciones futuras, sin ejecutar), '
    'FUTURO (lo que produce otro nodo o decide un humano, no ambigüedad). '
    'REFORMULACION describe el encargo del nodo, no esta revisión. DRY-RUN describe cómo lo ejecutaría '
    'un ejecutor futuro, hipotéticamente y sin ejecutar nada: archivos, cambios concretos, consumo de '
    'dependencias y gates, errores y validación esperada. Si el nodo es un agregado o paquete no '
    'ejecutable, dilo y además recorre cómo lo cumplen sus hijos, qué transfiere cada uno al siguiente '
    'y cómo se valida el resultado conjunto; no basta listar prerrequisitos ni verificar aceptaciones. '
    'Máximo 350 palabras.'
)
INSTRUCTION_VERSION = 'v2-ejecucion-hipotetica'  # Attempts without this field used the original SYSTEM.
ARGV = ['pi', '--provider', 'deepseek', '--model', 'deepseek-flash', '--thinking', 'low', '--offline',
        '--no-session', '--no-context-files', '--no-skills', '--no-extensions', '--no-prompt-templates',
        '--no-tools', '--system-prompt', SYSTEM, '--print']
SELECTION = 'deepseek-flash: perfil barato verificado en esta máquina por ritual-context-review; no se afirma precio mínimo global'
BASE_SOURCES = ['context-review-guide.md', 'brief.md', 'alcance.md', 'decisiones.md', 'cobertura.md']


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def contract(node: dict) -> dict:
    return {k: v for k, v in node.items() if k != 'context_review'}


def canonical(node: dict) -> str:
    return json.dumps(contract(node), sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def all_nodes(d: dict) -> list:
    return [d['hierarchy']['root'], *d['hierarchy']['packages'], *d['tasks']]


def sources_for(node: dict) -> list:
    paths = list(BASE_SOURCES)
    nid = node['id']
    if node.get('kind') == 'validation' or nid in ('WS08', 'WS30', 'WS16'):
        paths += ['validacion-humana.md', 'borradores/user-flows.md']
    if node.get('overlap_with') or nid in ('WS04', 'WS06', 'PK01'):
        paths.append('reconciliacion.md')
    if nid in ('WS09',):
        paths.append('borradores/vistas.md')
    if nid in ('WS10', 'WS31', 'WS38', 'PK06'):
        paths.append('borradores/manual.md')
    if nid == 'WS07':
        paths.append('validacion-humana.md')
    if nid in ('WS01', 'ROOT'):
        paths.append('borradores/vision.md')
    return list(dict.fromkeys(paths))


def neighbours(d: dict, node: dict) -> tuple:
    tasks = {t['id']: t for t in d['tasks']}
    pk = {p['id']: p for p in d['hierarchy']['packages']}
    nid = node['id']
    ids = []
    if nid == 'ROOT':
        ids = list(node['children'])
    elif nid in pk:
        ids = list(node['children'])
        inside = set(ids)
        for c in list(ids):
            ids += [x for x in tasks[c]['depends_on'] if x not in inside and '.' not in x]
    else:
        ids = list(node['depends_on'])
        ids += [v['depends_on'][0] for v in node.get('variants', []) if v['depends_on']]
        ids += [t['id'] for t in d['tasks'] if nid in t['depends_on']]
        if node.get('parent_id'):
            ids.append(node['parent_id'])
    ids += node.get('review_context_nodes', [])
    ids = list(dict.fromkeys(i for i in ids if i != nid))
    gate_ids = list(node.get('requires', []))
    for v in node.get('variants', []):
        gate_ids += v['requires']
    gate_ids += [g for g, v in d['gates'].items() if v.get('produced_by') == nid]
    gate_ids += [g for g in d['gates'] if g in str(contract(node))]
    gate_ids = list(dict.fromkeys(gate_ids))
    return [tasks.get(i) or pk[i] for i in ids], {g: d['gates'][g] for g in gate_ids}


def bundle(d: dict, node: dict) -> tuple:
    """Return exact input bytes and the ordered source records of the manifest."""
    parts = []
    records = []

    def add(label: str, text: str, projection: str) -> None:
        parts.append(f'FILE:{label}\n{text.rstrip()}\n')
        records.append({'path': label, 'sha256': sha(text.encode()), 'projection': projection})

    for rel in sources_for(node):
        add(str(PLAN / rel), (B / rel).read_text(), 'whole_file')
    dump = lambda o: yaml.safe_dump(o, allow_unicode=True, sort_keys=False)
    neigh, gates = neighbours(d, node)
    if node.get('overlap_with'):
        key=node['overlap_with']
        add(str(PLAN / 'dag.yaml') + '#external_reference:'+key, dump({key:d['external_references'][key]}), 'external_reference')
    if node['id']=='WS07':
        add(str(PLAN / 'dag.yaml') + '#baseline_proposal', dump({'baseline_proposal':d['baseline_proposal']}), 'baseline_proposal')
    if 'source_mode' in dump(contract(node)):
        add(str(PLAN / 'dag.yaml') + '#parameters', dump(d['parameters']), 'parameters')
    add(str(PLAN / 'dag.yaml') + f'#node:{node["id"]}', dump(contract(node)), 'node_contract')
    keep = ('id', 'title', 'kind', 'owner_repo', 'node_role', 'parent_id', 'children', 'scope', 'acceptance',
            'output_scope', 'depends_on', 'requires')
    for n in neigh:
        add(str(PLAN / 'dag.yaml') + f'#edge:{n["id"]}', dump({k: n[k] for k in keep if k in n}), 'edge_contract')
    if gates:
        add(str(PLAN / 'dag.yaml') + '#gates', dump(gates), 'gate_contracts')
    parts.append(
        f'FILE:instruccion\nRevisa el nodo {node["id"]} siguiendo context-review-guide.md. ' + ('Para ROOT/PK, reformula el RESULTADO SUSTANTIVO del paquete y da DRY-RUN HIPOTETICO de ejecucion de hijos en orden, entradas/salidas entre ellos e integracion/validacion. No describas solo como revisar hashes/status/disposition: eso es gate de comprension, no el trabajo del paquete. No ejecutes nada. ' if node['id']=='ROOT' or node['id'].startswith('PK') else '') + 'Los bloques edge son '
        'contratos de sus vecinos; no los revises. No ejecutes nada.\n')
    return ''.join(p + '\n' for p in parts).encode(), records


def attempt_dir(nid: str, input_sha: str) -> Path:
    base = RUN / nid / input_sha
    n = 1
    while (base / f'attempt-{n}').exists():
        n += 1
    return base / f'attempt-{n}'


def utc() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat()


RECEIPT_FIELDS = ('argv', 'cwd', 'stdin', 'pi_version', 'start', 'end', 'pid', 'returncode', 'input_sha256',
                  'output_sha256', 'technical_failure')


def receipt_state(receipt: dict) -> tuple:
    """Classify a receipt as complete, incomplete or technical_failure, with its missing fields."""
    missing = [k for k in RECEIPT_FIELDS if k not in receipt]
    if receipt.get('technical_failure') is True:
        return 'technical_failure', missing
    return ('incomplete' if missing else 'complete'), missing


def attempts(nid: str, input_sha: str) -> tuple:
    """Count this input's technical failures and return its latest complete answered attempt, if any."""
    failed, answered = 0, None
    base = RUN / nid / input_sha
    for path in sorted(base.glob('attempt-*/receipt.json'), key=lambda p: int(p.parent.name.split('-')[1])):
        receipt = json.loads(path.read_text())
        state = receipt_state(receipt)[0]
        if state == 'complete':
            answered = path.parent
        elif state == 'technical_failure' and receipt.get('stdin') == 'devnull':  # Earlier receipts never reached the model.
            failed += 1
    return failed, answered


def review(d: dict, node: dict, reason: str = '') -> dict:
    data, records = bundle(d, node)
    input_sha = sha(data)
    failed, answered = attempts(node['id'], input_sha)
    if answered and not reason:
        return {'id': node['id'], 'attempt': str(answered.relative_to(ROOT)), 'ok': True}
    if failed >= MAX_TECHNICAL and not reason:
        return {'id': node['id'], 'attempt': str((RUN / node['id'] / input_sha).relative_to(ROOT)), 'ok': False}
    version_proc = subprocess.run(['pi', '--version'], stdin=subprocess.DEVNULL, capture_output=True, text=True)
    version = (version_proc.stdout or version_proc.stderr).strip()
    for i in range(max(1, MAX_TECHNICAL - failed)):
        out = attempt_dir(node['id'], input_sha)
        prev = sorted(out.parent.glob('attempt-*'), key=lambda p: int(p.name.split('-')[1]))[-1:]
        out.mkdir(parents=True)
        (out / 'input.md').write_bytes(data)
        text = canonical(node)
        (out / 'contract.json').write_text(text)
        rel = str((out / 'input.md').relative_to(ROOT))
        argv = ARGV + ['@' + rel]
        extra = {'instruction_version': INSTRUCTION_VERSION,
                 'system_prompt_sha256': sha(argv[argv.index('--system-prompt') + 1].encode())}
        retry = {'retry_reason': reason, 'retry_of': str(prev[0].relative_to(ROOT)) if prev else None} if reason else {}
        neigh, _gates = neighbours(d, node)
        (out / 'manifest.json').write_text(json.dumps({
            'node_id': node['id'], 'role': 'context-reviewer', 'attempt': int(out.name.split('-')[1]),
            'input_sha256': input_sha, 'ordered_sources': records, 'node_contract_sha256': sha(text.encode()),
            'edge_contracts': [{'id': n['id'], 'sha256': sha(canonical(n).encode())} for n in neigh],
            'provider': 'deepseek', 'model': 'deepseek-flash', 'thinking': 'low', 'selection_reason': SELECTION,
            'isolation_flags': ARGV[7:14], 'argv': argv, **extra, **retry}, ensure_ascii=False, indent=1))
        start = utc()
        proc = subprocess.Popen(argv, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        timed_out = False
        try:
            stdout, stderr = proc.communicate(timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            timed_out = True
        (out / 'output.md').write_text(stdout)
        (out / 'stderr.log').write_text(stderr)
        technical = timed_out or proc.returncode != 0 or not stdout.strip()
        (out / 'receipt.json').write_text(json.dumps({
            'argv': argv, 'cwd': str(ROOT), 'stdin': 'devnull', 'pi_version': version, 'start': start, 'end': utc(), 'pid': proc.pid,
            'returncode': proc.returncode, 'input_sha256': input_sha, 'output_sha256': sha(stdout.encode()),
            'technical_failure': technical, **retry}, ensure_ascii=False, indent=1))
        if not technical:
            return {'id': node['id'], 'attempt': str(out.relative_to(ROOT)), 'ok': True}
    return {'id': node['id'], 'attempt': str(out.relative_to(ROOT)), 'ok': False}


def stale_reviews(d: dict) -> list:
    problems = []
    for node in all_nodes(d):
        cr = node['context_review']
        if cr['status'] == 'pending':
            problems.append(f'{node["id"]}: pending')
            continue
        data, _ = bundle(d, node)
        if cr.get('input_sha256') != sha(data):
            problems.append(f'{node["id"]}: input changed')
        elif cr.get('contract_sha256') != sha(canonical(node).encode()):
            problems.append(f'{node["id"]}: contract changed')
        elif not (ROOT / cr['evidence'][0] / 'disposition.md').is_file():
            problems.append(f'{node["id"]}: disposition missing')
        else:
            path = ROOT / cr['evidence'][0] / 'receipt.json'
            state = receipt_state(json.loads(path.read_text()))[0] if path.is_file() else 'incomplete'
            if state != 'complete':
                problems.append(f'{node["id"]}: receipt ' + state.replace('_', ' '))
    return problems


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['run', 'status'])
    parser.add_argument('ids', nargs='*')
    parser.add_argument('--stale', action='store_true', help='run only nodes whose review is pending or stale')
    parser.add_argument('--jobs', type=int, default=4)
    parser.add_argument('--new-attempt', action='store_true', help='force a new attempt after a semantic rejection')
    parser.add_argument('--reason', default='', help='why the new attempt is needed')
    args = parser.parse_args()
    if args.new_attempt and (args.command != 'run' or not args.ids or not args.reason.strip() or args.stale):
        parser.error('--new-attempt needs run, explicit ids, a non-empty --reason and no --stale')
    if args.reason and not args.new_attempt:
        parser.error('--reason requires --new-attempt')
    d = yaml.safe_load((B / 'dag.yaml').read_text())
    if args.command == 'status':
        problems = stale_reviews(d)
        print('\n'.join(problems) or 'all reviews current')
        return
    nodes = all_nodes(d)
    if args.ids:
        nodes = [n for n in nodes if n['id'] in args.ids]
    if args.stale:
        stale = {p.split(':')[0] for p in stale_reviews(d)}
        nodes = [n for n in nodes if n['id'] in stale]
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        for result in pool.map(lambda n: review(d, n, args.reason.strip()), nodes):
            print(result['id'], 'ok' if result['ok'] else 'TECHNICAL_FAILURE', result['attempt'], flush=True)


if __name__ == '__main__':
    main()
