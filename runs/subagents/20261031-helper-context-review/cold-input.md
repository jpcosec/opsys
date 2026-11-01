FILE:desk/tasks/task-reparar-helper-context-review-py-del-plan-workspace.md
---
id: task-reparar-helper-context-review-py-del-plan-workspace
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-cierre-revision9/review-source.md
- desk/drawer/plans/workspace-documental/context_review.py
- desk/rituals/context-review.md
- desk/drawer/plans/workspace-documental/validate_plan.py
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
files:
- desk/drawer/plans/workspace-documental/context_review.py
- tests/test_context_review_helper.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-reparar-helper-context-review.md
closeout_evidence:
- tests
- commit
---

# Reparar helper context_review.py del plan workspace

## Rationale

_Explain why this task exists or the business driver behind it._

attempts() lanza KeyError con los recibos manuales de WS12 y WS37, el helper no permite repetir una revisión tras rechazo semántico porque devuelve answered, y la instrucción de ejecución hipotética solo existió en memoria. Autorización: runs/subagents/20261031-cierre-revision9/review-source.md, punto 3.

## Goal

_Describe the concrete result this task must produce._

Dejar desk/drawer/plans/workspace-documental/context_review.py con instrucción durable, intento nuevo tras rechazo semántico, recibo y manifest propios coherentes, y recibos históricos incompletos reconocidos sin crash, con pruebas en tests/test_context_review_helper.py.

## Scope

_State what is in scope and what is out of scope._

Solo desk/drawer/plans/workspace-documental/context_review.py y tests/test_context_review_helper.py, más evidencia en runs/subagents/20261031-helper-context-review/. No se tocan validate_plan.py, build_plan.py, dag.yaml, brief.md ni otros archivos del plan, UI, Scion ni repos hermanos. Las rutas son relativas a la raíz del repo deskops. Las firmas públicas que usa validate_plan.py se conservan: all_nodes, stale_reviews.

Requisitos:

1. Instrucción durable. La constante SYSTEM incorpora que REFORMULACION describe el encargo del nodo y no esta revisión, y que DRY-RUN describe cómo lo ejecutaría un ejecutor futuro, hipotéticamente y sin ejecutar nada: archivos, cambios concretos, consumo de dependencias y gates, errores y validación esperada. Para un agregado o paquete no ejecutable agrega: decirlo y además recorrer cómo lo cumplen sus hijos, qué transfiere cada uno al siguiente y cómo se valida el resultado conjunto; no basta listar prerrequisitos ni verificar aceptaciones. Se agrega INSTRUCTION_VERSION con valor nuevo. El texto de FILE:instruccion dentro de bundle() no cambia, porque cambiaría el hash de input de los 73 nodos.

2. Intento nuevo tras rechazo semántico. `run <ids> --new-attempt --reason <texto>`: exige ids explícitos y razón no vacía; falla sin efecto si faltan o si se combina con --stale. Crea un intento nuevo aunque exista uno answered para el mismo input. Sin ese flag sigue reutilizando answered.

3. Manifest y recibo propios de cada intento: número real de intento, argv efectivo, instruction_version, system_prompt_sha256 del prompt efectivo y, en intento forzado, retry_reason y retry_of. El recibo conserva todos los campos actuales. Cada manifest se genera para su intento, no se copia.

4. Recibos históricos incompletos. attempts() no lanza con un recibo sin technical_failure y conserva su retorno de dos valores. Un recibo incompleto no cuenta como answered ni como fallo técnico. Se expone una función que clasifica un recibo en completo, incompleto o fallo técnico, listando los campos faltantes. Sin answered completo, run crea intento nuevo. stale_reviews agrega un problema `<id>: receipt incomplete` cuando el intento registrado en dag.yaml como evidencia tiene recibo incompleto, y sigue devolviendo una lista: nada se vuelve válido en silencio. No se rellenan recibos históricos, ni PIDs, ni fechas.

Hoy los recibos de WS12 y WS37 están incompletos y son evidencia registrada: tras este cambio status los listará y validate_plan.py --check fallará por eso hasta que sus revisiones se repitan. Es el efecto esperado y declarado; lo resuelve la tarea de cierre siguiente.

Pruebas en tests/test_context_review_helper.py, sin invocar proveedor: stub de Popen o de pi, y RUN y ROOT dirigidos a tmp_path. Casos: recibo incompleto no lanza y no cuenta como answered; answered completo se reutiliza sin flag y no llama al proceso; --new-attempt crea attempt-n+1 con manifest y recibo coherentes con argv, número y razón; --new-attempt sin razón o sin ids falla; stale_reviews reporta receipt incomplete; SYSTEM contiene la cláusula de agregado y el hash de bundle no depende de SYSTEM.

Roles: el Executor edita esos dos archivos y escribe runs/subagents/20261031-helper-context-review/result-summary.md; corre solo pytest de ese archivo; sin commits ni closeout, y no corre `context_review.py run`. El Supervisor valida, hace commits y closeout. Tester independiente de solo lectura.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer desk/drawer/plans/workspace-documental/context_review.py completo y validate_plan.py para no romper su uso. 2. Implementar los cuatro requisitos con el menor cambio. 3. Escribir pruebas. 4. Dejar runs/subagents/20261031-helper-context-review/result-summary.md con diff resumido y salida de pytest.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_context_review_helper.py
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status lista exactamente WS12 y WS37 como receipt incomplete
- git diff --name-only 6d41f301..HEAD -- desk/drawer/plans/workspace-documental/validate_plan.py desk/drawer/plans/workspace-documental/build_plan.py queda vacío
- Tester independiente de solo lectura deja runs/subagents/20261031-helper-context-review/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Los cuatro requisitos cumplidos, pytest de tests/test_context_review_helper.py en verde, build --check en verde, status lista exactamente WS12 y WS37 como receipt incomplete, y un Tester independiente da PASS.

FILE:runs/subagents/20261031-cierre-revision9/review-source.md
# Revisión root del checkpoint d9877e86, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-10-31.

Aceptadas las correcciones sustantivas previas. No se libera la siguiente capa. Tres correcciones acotadas, con autorización para resolverlas con el workflow habitual y enviar checkpoint final.

Verificación root: build --check 0; validate --check 0; status all current; reconstrucción byte a byte de los 73 inputs contra bundle actual y contratos, hashes input/output/disposition contra las 73 filas del ledger: todos coinciden. Código de producto, decisiones, auditorías y validadores sin cambios desde 5f05281c. Hay 71 receipts con PID (71 distintos); WS12/WS37 no tienen ese dato. El conteo real de SYSTEM en argv es 40 original / 33 ampliado, no 39 / 34 o 35: corregir únicamente la afirmación del resumen, sin reescribir evidencia histórica.

1) Calidad del dry-run en agregados: WS33 final 1b03f9.../attempt-1 describe revisar nodo/status/aceptaciones, no cómo se produce la vinculación, dedup/procedencia y decisión por sus hijos. Con el mismo criterio, WS13 (3d32236.../attempt-1) y WS15 (add171.../attempt-1) tampoco describen ejecución hipotética sustantiva por hijos. No es incorrecto que no ejecuten ni tengan salida propia; lo insuficiente es usar eso para omitir el recorrido de trabajo/transferencias/validación. Repetir SOLO esas tres revisiones baratas en procesos frescos con instrucción explícita de agregado. Mismo contrato si sigue claro, sin pedir implementación propia ni convertir vecinos en nodos a revisar. No aceptar solo una reformulación detallada como sustituto del dry-run. Conservar intentos previos; comparación nueva y ledger actualizado. Si el nuevo revisor encuentra ambigüedad real, resolver/decomponer por escrito e invalidar solo inputs afectados.

2) WS35: el output final plantea una duda válida; la disposición la descarta extrapolando «resultados vinculados por WS33.1» a los mensajes recibidos por API. Scope WS35 distingue esas dos fuentes; no prueba que los mensajes no vinculados estén excluidos. promotion-notes ya reconoce la elección mostrar huecos/excluir. Corregir por supersesión fechada la clasificación a decisión de presentación pendiente al promover, con productor TaskDoc de WS35 y aceptación de ese caso ANTES de ejecutar. No hace falta decidir hoy la UX de Scion ni pedir producto otra vez; no mantener simultáneamente «no es ambigüedad» como aceptación vigente y una elección pendiente. Si se cambia contrato canónico, renovar solamente inputs afectados. No rescatar la evidencia barata con interpretación experta.

3) Runner/recibos: reproducido attempts('WS12', hash) y attempts('WS37', hash): KeyError 'technical_failure'. Los receipts manuales omiten technical_failure/output_sha256/pid/otros campos; manifest fue copiado del intento 1. Rompe reanudación con helper y no justifica afirmar recibo completo. Autoriza una tarea ESPECÍFICA y acotada de mantenimiento del helper (drawer commit, promoción commit, contexto fresco/executor/tester/cierre), sin tocar validadores ni UI: hacer durable la instrucción de ejecución hipotética; poder solicitar un intento nuevo tras rechazo semántico sin reutilizar answered por mismo input; producir recibo/manifest propios coherentes con argv y prompt efectivo; reconocer recibos históricos incompletos sin crash ni tratarlos silenciosamente como completos. No rellenar retrospectivamente PIDs/fechas que no fueron capturados. Verificar con pruebas pequeñas significativas de receipts incompletos y rechazo semántico/cache, sin invocar proveedor en pruebas. Antes de usar el helper reparado, respetar el preflight correspondiente. Los dos intentos manuales se conservan como evidencia histórica declarada; para crédito operativo completo a WS12/WS37 generar intentos frescos por el canal reparado, sin cambiar sus briefs por mero metadato. Conjunto a revisar de nuevo: WS13, WS15, WS33, WS12 y WS37, más solo los inputs que realmente cambien.

Orden sugerido: congelar corrección documental necesaria; reparar/verificar helper; lanzar las cinco revisiones correctamente registradas, comparar y actualizar ledger/meta final. Un cambio del helper no obliga a repetir los otros 68: declarar versiones de instrucción y recibos, sin inventar nueva vigencia universal. Leer reformulación/dry-run completo y contrato completo, no solo lista de ambigüedades. Una nueva disposición del coordinador no demuestra retroactivamente que la anterior se leyó; mantener supersesión honesta.

Cierre: build/validate/status, integridad 73 con excepciones históricas explícitas y ninguna vigente oculta, tester independiente, tarea/phase según corresponda; handoff a root con paths/commits y límites. Preservar cuatro dirty ajenos. NO WS07, WS08-12, código UI, Scion ejecución, push ni nuevas decisiones de producto. No reabre correcciones sustantivas aceptadas.

FILE:desk/drawer/plans/workspace-documental/context_review.py
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
    'FUTURO (lo que produce otro nodo o decide un humano, no ambigüedad). Máximo 350 palabras.'
)
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


def attempts(nid: str, input_sha: str) -> tuple:
    """Count this input's technical failures and return its latest answered attempt, if any."""
    failed, answered = 0, None
    base = RUN / nid / input_sha
    for path in sorted(base.glob('attempt-*/receipt.json'), key=lambda p: int(p.parent.name.split('-')[1])):
        receipt = json.loads(path.read_text())
        if not receipt['technical_failure']:
            answered = path.parent
        elif receipt.get('stdin') == 'devnull':  # Earlier receipts never reached the model.
            failed += 1
    return failed, answered


def review(d: dict, node: dict) -> dict:
    data, records = bundle(d, node)
    input_sha = sha(data)
    failed, answered = attempts(node['id'], input_sha)
    if answered:
        return {'id': node['id'], 'attempt': str(answered.relative_to(ROOT)), 'ok': True}
    if failed >= MAX_TECHNICAL:
        return {'id': node['id'], 'attempt': str((RUN / node['id'] / input_sha).relative_to(ROOT)), 'ok': False}
    version_proc = subprocess.run(['pi', '--version'], stdin=subprocess.DEVNULL, capture_output=True, text=True)
    version = (version_proc.stdout or version_proc.stderr).strip()
    for _ in range(MAX_TECHNICAL - failed):
        out = attempt_dir(node['id'], input_sha)
        out.mkdir(parents=True)
        (out / 'input.md').write_bytes(data)
        text = canonical(node)
        (out / 'contract.json').write_text(text)
        rel = str((out / 'input.md').relative_to(ROOT))
        argv = ARGV + ['@' + rel]
        neigh, _gates = neighbours(d, node)
        (out / 'manifest.json').write_text(json.dumps({
            'node_id': node['id'], 'role': 'context-reviewer', 'attempt': int(out.name.split('-')[1]),
            'input_sha256': input_sha, 'ordered_sources': records, 'node_contract_sha256': sha(text.encode()),
            'edge_contracts': [{'id': n['id'], 'sha256': sha(canonical(n).encode())} for n in neigh],
            'provider': 'deepseek', 'model': 'deepseek-flash', 'thinking': 'low', 'selection_reason': SELECTION,
            'isolation_flags': ARGV[7:14], 'argv': argv}, ensure_ascii=False, indent=1))
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
            'technical_failure': technical}, ensure_ascii=False, indent=1))
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
    return problems


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['run', 'status'])
    parser.add_argument('ids', nargs='*')
    parser.add_argument('--stale', action='store_true', help='run only nodes whose review is pending or stale')
    parser.add_argument('--jobs', type=int, default=4)
    args = parser.parse_args()
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
        for result in pool.map(lambda n: review(d, n), nodes):
            print(result['id'], 'ok' if result['ok'] else 'TECHNICAL_FAILURE', result['attempt'], flush=True)


if __name__ == '__main__':
    main()

FILE:desk/rituals/execution.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:19Z'
  authority: generated
  via: update_document
# ritual-xxx
id: ritual-execution
# Ordered prose steps; not document references
steps:
- 1. Confirm the current phase is explicit and that this task belongs to the ready
  dependency layer being executed.
- 1. Open the initialization gate by making the active task, task scope, touched files,
  and validation targets explicit.
- 1. Atomize the work into one coherent deliverable.
- 1. Audit code, docs, tests, and git state before changing anything.
- '1. Run cheap TaskDoc-only preflight under [ritual-context-review](context-review.md)
  in a fresh ephemeral no-tools process: restate objective, list ambiguities and give
  a detailed non-executing dry-run.'
- 1. Store that TaskDoc-only reformulation at `runs/subagents/<run-dir>/preflight.md`.
- 1. Pass the preflight only when the reformulation reproduces the task intent closely
  enough to execute without guesswork; if the subagent reports any ambiguity or misses
  the intended work, fix the TaskDoc before dispatching any Executor.
- '1. Run a separate cheap cold-bundle coverage review under [ritual-context-review](context-review.md):
  explicitly supply task, routed instructions/rituals, bound pills, linked atoms/files
  and validation. Require reformulation, ambiguities and detailed dry-run; no commands
  or source edits.'
- 1. The coordinator compares both outputs with owner intent. Fix the written brief,
  split oversized nodes and retry changed input in a new isolated process. Resolve
  cold-review findings before implementation; unresolved ambiguity blocks dispatch.
- 1. Sweep the board-routed pills and any task-local pills against the task scope,
  touched files, implementation path, and planned validation.
- 1. Bind every pill whose `when`, `where`, or `how_not` matches a plausible part
  of the task.
- 1. If a risky ambiguity is still uncovered, create or update a pill before implementation
  instead of proceeding on implicit assumptions.
- 1. Do not start implementation until the initialization gate confirms atomization,
  preflight comprehension, cold review, and pill coverage.
- 1. Implement only the changes required for the active task.
- 1. Keep scope tight and avoid unrelated fixes.
- 1. Prepare validation before calling the work complete.
- 1. Exit execution only by opening a handoff to testing that names the intended contract,
  relevant tests, and pill guardrails that must be proven.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:execution
---

# Execution ritual for active desk tasks

## Purpose

_Explain why this ritual exists._

Carry one active desk task through scoped implementation inside an explicit phase with task and pill binding, including a zero-context TaskDoc comprehension gate and a fresh-context coverage check strong enough to catch missing guardrails before implementation starts. Apply the [context-review ritual](context-review.md) as the cheap non-executing brief-quality gate; expert review, Executor work and independent Tester validation remain distinct.

## Trigger

_State when this ritual should start._

Start when a desk task becomes the current execution target.

## Preconditions

_List the conditions that must hold before running the ritual._

- The task exists in desk/tasks.
- The current phase or ready dependency layer is explicit.
- Dependencies are explicit.
- Required pills exist.
- The board routes the task as active.
- The active board pills are visible to the executor.
- The initialization gate is still open.
- The TaskDoc is specific enough for a fresh-context subagent to restate the work without guessing.
- Required root/package/leaf and dependency-interface reviews have passed the coordinator comparison under [ritual-context-review](context-review.md).

## Validation

_List the checks that prove the ritual was performed correctly._

- The active task is explicit.
- A cheap isolated reviewer completed TaskDoc-only preflight before Executor dispatch; provider/model/profile, exact input/hash, output and coordinator disposition are traceable under ritual-context-review.
- The preflight reformulation was stored at `runs/subagents/<run-dir>/preflight.md`.
- The preflight passed only because the subagent's reformulation reproduced the intended work and surfaced no unresolved ambiguity.
- A separate cheap isolated cold-bundle reviewer completed comprehension and guardrail coverage; expert council review does not satisfy either cheap gate.
- Required pills are named in the task.
- Cold-review ambiguities were resolved in the written contract and rerun when affected input changed; no unresolved finding was merely recorded as permission to execute.
- Each changed surface is either covered by a named pill or explicitly judged to need no pill.
- No active board pill was skipped just because it looked generic or already familiar.
- Implementation did not start before the initialization gate was satisfied.
- Changes stay within task scope.
- The work is ready for testing and has an explicit testing handoff.

## Failure Modes

_List common mistakes this ritual prevents._

- Working without an active task doc.
- Mixing unrelated concerns into one task.
- Skipping the zero-context TaskDoc comprehension gate and dispatching an Executor anyway.
- Letting the preflight pass even though the reformulation missed intent or reported ambiguity.
- Skipping the fresh-context subagent review and relying only on the primary executor's familiarity.
- Skipping pill binding when ambiguity still exists.
- Treating the task's `## Pills` list as a formality instead of a coverage checklist.
- Binding only the most obvious pill while ignoring pills implied by `when`, `where`, or `how_not`.
- Starting code changes before the initialization gate is closed.
- Handing work to closeout directly from execution without a testing gate.
- Using expert approval, a verdict token, reviewer execution, or implementation tests as a substitute for cheap non-executing comprehension.

## Completion

_Describe what completion looks like._

The implementation is complete enough to enter the testing ritual through an explicit handoff gate.

FILE:desk/rituals/testing.md
---
# ritual-xxx
id: ritual-testing
# List of step-xxx paths
steps:
- 1. Confirm the incoming handoff names the intended contract, touched surfaces, and
  pill guardrails to prove.
- 1. Check whether existing tests are stale or encode obsolete behavior.
- 1. Translate the bound pills into concrete assertions, especially the failure cases
  implied by `how_not`.
- 1. Add or update tests for the intended contract.
- 1. Run the smallest relevant test scope first.
- 1. Run broader validation when the task changes shared behavior.
- 1. Do not proceed to closeout while relevant tests fail.
- 1. Exit testing only by opening a closeout handoff that confirms passing evidence
  for the contract and the bound pills.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:testing
---

# Testing ritual for desk task closure

## Purpose

_Explain why this ritual exists._

Verify the intended task behavior with the right test scope before a task can close, while leaving shared integration or end-to-end proof for phase closeout.

## Trigger

_State when this ritual should start._

Run after implementation changes and before closeout.

## Preconditions

_List the conditions that must hold before running the ritual._

- The intended behavior is clear.
- Relevant tests or test locations are known.
- Bound pills and their guardrails are known.
- The execution-to-testing handoff gate is explicit.

## Validation

_List the checks that prove the ritual was performed correctly._

- The intended behavior is covered.
- Bound pill guardrails are covered directly by tests or by an explicit validation step.
- The relevant tests pass.
- No known failure was ignored to force completion.
- Closeout receives an explicit green handoff rather than an informal claim that the task is done.

## Failure Modes

_List common mistakes this ritual prevents._

- Treating stale tests as truth.
- Skipping tests to move faster.
- Closing with failing relevant tests.
- Passing contract tests while leaving a bound pill's `how_not` path unchecked.
- Letting work skip from execution to closeout without a testing gate.

## Completion

_Describe what completion looks like._

The task has trustworthy test evidence and can proceed to closeout, with any broader cross-task validation obligations handed forward to the phase ritual.

FILE:desk/contexts/pill-001-task-closure-commit.md
---
# pill-xxx
id: pill-001
# e.g., language:python, library:pydantic
tags:
- system:sldb
- workspace:desk
- pill-type:guardrail
- topic:git
- topic:task-closure
---

# Guardrail: close every task with its own commit

## What

_Define the context or guardrail this pill carries._

Task closure in this routine is defined by a completed change plus a dedicated closing commit in git.

## Why

_Explain why this context matters for safe execution._

If a task can be called done without a closing commit, the board and desk documents drift away from the durable execution record.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task is being finished, deleted from `desk/tasks/`, or removed from a board.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/rituals/closeout.md`, `desk/rituals/testing.md`, task closeout, and any future workspace that reuses this routine.

## How

_Describe the correct way to apply this guidance._

Keep task files active until tests, cleanup, board updates, and the closing change are ready, then create one atomic commit that closes the task.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not delete a finished task file and call it closed before the closing commit exists. Do not rely on memory or an uncommitted working tree as the record of closure.

FILE:desk/contexts/pill-005-subagent-execution.md
---
# pill-xxx
id: pill-005
# e.g., language:python, library:pydantic
tags:
- system:sldb
- workspace:desk
- pill-type:pattern
- topic:subagents
- topic:execution
---

# Pattern: execute active tasks through fresh subagents

## What

_Define the context or guardrail this pill carries._

Use one fresh subagent as the normal execution surface for each active task, with the primary session acting as coordinator, integrator, and final verifier.

## Why

_Explain why this context matters for safe execution._

Fresh task-specific contexts reduce context overload, make ambiguity easier to spot, and keep execution aligned with the task's actual bundle of files, pills, atoms, and validations instead of leaked memory from earlier work.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever an active task enters execution, especially when the board contains multiple parallel-ready tasks in the same phase.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/rituals/execution.md`, `desk/rituals/phase.md`, active task execution, and any workflow tooling that launches or simulates subagent work.

## How

_Describe the correct way to apply this guidance._

Give each task its own clean execution bundle: the task doc, routed instructions, bound pills, linked atoms, linked files, and validation targets. Let the primary session coordinate handoffs, integration, and final verification across tasks and phases.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not carry multiple unrelated tasks through one long-lived context. Do not let subagent outputs bypass the task's own validation, closeout, and commit workflow.

FILE:desk/contexts/pill-007-phase-gated-task-flow.md
---
# pill-xxx
id: pill-007
# e.g., language:python, library:pydantic
tags:
- system:sldb
- workspace:desk
- pill-type:guardrail
- topic:workflow
- topic:phase-gates
---

# Guardrail: force every task through explicit phase gates

## What

_Define the context or guardrail this pill carries._

Every desk task must pass through explicit entry, handoff, testing, and closeout gates, and every board phase must open and close explicitly instead of flowing directly from implementation intent to completion.

## Why

_Explain why this context matters for safe execution._

Agents keep skipping atomization, task scoping, test review, integration validation, or the closing commits when those obligations live only as background expectations. Phase gates turn those obligations into mandatory stop points at both the task and dependency-layer levels.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a desk task is initialized, handed from execution to testing, handed from testing to closeout, or grouped into a ready phase for parallel execution.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/rituals/phase.md`, `desk/rituals/execution.md`, `desk/rituals/testing.md`, `desk/rituals/closeout.md`, and any task that changes code, docs, or workflow state.

## How

_Describe the correct way to apply this guidance._

Open each phase by identifying the ready dependency layer and each task by confirming clarity, file scope, validation targets, and atomization. Require an execution exit gate before testing, a testing exit gate before closeout, a final task closeout gate that ends in the dedicated task commit, and a phase closeout gate that runs integration validation plus pill reconciliation before the next phase begins.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not treat implementation as the default starting point. Do not jump from “code looks done” to task deletion or board cleanup without a testing handoff and a dedicated task closing commit. Do not treat a stack of closed tasks as permission to begin the next phase without a phase-level validation and reconciliation pass.

