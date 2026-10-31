"""Materialize planning projections from dag.yaml. No product or other-repo writes."""
from pathlib import Path
import argparse
import yaml

B = Path(__file__).resolve().parent
ROOT = B.parents[3]
D = yaml.safe_load((B / 'dag.yaml').read_text())
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
outputs = {}
rows = []
for t in D['tasks']:
    outputs[ROOT / t['task_file']] = ('---\n' + yaml.safe_dump({k: t[k] for k in ('id', 'status', 'owner_repo', 'node_role', 'parent_id', 'children', 'depends_on', 'requires') if k in t}, allow_unicode=True, sort_keys=False)
        + '---\n\n# ' + t['title'] + '\n\nCandidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).\n\n'
        + '## Entregable y archivos previstos\n\nRepo único: `' + t['owner_repo'] + '`. Tamaño relativo: ' + t['estimate'] + '.\n\n' + t['output_scope']
        + '\n\nBase explícita: `' + t['output_base'] + '`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.\n\n## Alcance\n\n' + t['scope'] + '\n\n## Aceptación\n\n' + t['acceptance']
        + '\n\n## Dependencias\n\nTareas: ' + (', '.join(t['depends_on']) or 'ninguna') + '. Gates: ' + (', '.join(t['requires']) or 'ninguno adicional') + '. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.\n'
        + ('\nSolapamiento: `' + t['overlap_with'] + '` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.\n' if t.get('overlap_with') else '')
        + ('\n## Variante\n\n' + yaml.safe_dump({k:t[k] for k in ('enabled_when','variants') if k in t},allow_unicode=True,sort_keys=False) if ('enabled_when' in t or 'variants' in t) else '')
        + '\n## Review barato de comprensión\n\nEstado: `' + t['context_review']['status'] + '`. Protocolo requerido: `' + t['context_review']['required_protocol'] + '`. Evidencia: ' + str(t['context_review']['evidence']) + '. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.\n'
        + '\n## Gate de promoción\n\nAuthorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.\n')
    rows.append('| ' + t['id'] + ' | [' + t['title'] + '](../../tasks/workspace-documental/' + Path(t['task_file']).name + ') | ' + (', '.join(t['depends_on']) or '—') + ' | ' + (', '.join(t['requires']) or '—') + ' | ' + t['owner_repo'] + ' | ' + t['estimate'] + ' |')
_nodes = [D['hierarchy']['root']] + D['hierarchy']['packages'] + D['tasks']
_counts = {}
for _n in _nodes:
    _counts[_n['context_review']['status']] = _counts.get(_n['context_review']['status'], 0) + 1
review_summary = ', '.join(f'{k}: {v}' for k, v in sorted(_counts.items()))
hierarchy_rows = ['- **' + p['id'] + ' ' + p['title'] + '**: ' + ', '.join(p['children']) for p in D['hierarchy']['packages']]
gate_rows = ['| ' + k + ' | ' + v['state'] + ' | ' + v['title'] + ' | ' + v['resolver'] + ' |' for k, v in D['gates'].items()]
outputs[B / 'README.md'] = '''# Workspace documental — plan revisado por concilio

Revisión ''' + str(D['revision']) + '''. Estado: ''' + D['status'] + '''. Propuesta de planificación, no activación ni ejecución de producto.

## Reviews baratos

El concilio conserva APTO COMO PLAN como revisión experta; no acredita contexto cero barato. Estado por nodo (raíz, paquetes y candidatas): ''' + review_summary + '''. Evidencia en `runs/subagents/20261031-workspace-context-reviews/context-review/`; protocolo `ritual-context-review`. Un review vigente prueba comprensión del encargo: no promueve nodos ni satisface gates. `execution_authorized=false`.

## Jerarquía de revisión

ROOT y PK agrupan la revisión; no son dependencias. Un nodo `aggregate` no se ejecuta y termina con sus hijos.

''' + '\n'.join(hierarchy_rows) + '''

## Entrada

- [Brief y glosario](brief.md): requisitos autosuficientes, sin chat ni memoria privada necesaria.
- [Decisiones](decisiones.md): alternativas, humano responsable y evidencia requerida; pendientes explícitas.
- [Alcance](alcance.md): lector, autoría manual, Scion opcional y exclusiones.
- [Reconciliación](reconciliacion.md): cómo integrar trabajo activo sin duplicarlo.
- [Cobertura de user-flows](cobertura.md) y [validación humana](validacion-humana.md).

Baseline propuesta: sldb/pron + Deskops + Mindmap existentes; Kimun es referencia, no migración ni dependencia de este DAG. El humano resuelve las propuestas en WS07 antes de código afectado. El plan no se apoya en decisiones que solo estén en la memoria de un agente.

## Documentos que podemos escribir ahora

[Visión](borradores/vision.md), [user-flows](borradores/user-flows.md), [catálogo de vistas](borradores/vistas.md) e [índice del manual](borradores/manual.md) tienen semilla de intención. WS01 aclara vocabulario/fuentes y WS02–05 auditan; WS08–10 convierten intención en contratos contrastados. Un borrador existente no equivale a tarea cerrada, aprobación humana o función disponible.

## DAG y candidatas

[dag.yaml](dag.yaml) es la única fuente de IDs/aristas/gates/metadatos. Esta tabla, las fichas de candidatas y las proyecciones se generan. No corregir dependencias solo en README o Mermaid. Las fichas están en drawer y requieren promoción formal en su repo dueño antes de ejecución. Tamaños S/M son relativos, no promesas de horas.

| ID | Entregable | Depende de tareas | Gates adicionales | Repo dueño | Tamaño |
|---|---|---|---|---|---|
''' + '\n'.join(rows) + '''

## Gates externos y humanos

| Gate | Estado observado | Significado | Resolver |
|---|---|---|---|
''' + '\n'.join(gate_rows) + '''

Cada output_scope se resuelve respecto de su output_base explícito; las actas de uso viven en repo dueño. Los productores de gates también se declaran en dag.yaml, sin aristas ocultas en generador. source_mode determina la variante WS21 y si WS20 pertenece a la entrega; pending bloquea ambos. Los gates se satisfacen con el tipo de evidencia declarado, nunca por existencia del archivo. El validador comprueba referencias, ausencia de ciclos y coherencia de proyecciones; muestra por separado candidatas de preparación, bloqueos y autorización. Cero nodos tienen ejecución de producto autorizada. Las capas topológicas no son fases operativas: falta aprobar gates, no solapamiento, TaskDoc y cierre de cada fase. Las observaciones de referencias tienen hash para detectar movimiento, no para aprobar trabajo.

## Entregas y gates de uso

WS13–16 y WS40/41 dan lector con búsqueda y errores antes de edición o índices nuevos. WS40 produce corpus temporal y WS17 aporta solo plantillas de entradas authored. WS19–28, WS42 y WS30 dan autoría/revisión manual; WS31 publica su manual. WS29 (Changes) y WS39 (Schema) son extensiones con aceptación propia, no prerrequisitos del lector o manual básico. WS32–38 son el ramal de Scion con permisos de ejecución explícitos. El cierre baseline usa handoff verificado al CLI/coordinador, no commit desde HTTP.

## Reproducción y revisión

`python desk/drawer/plans/workspace-documental/build_plan.py` genera tabla/fichas/spec del diagrama. `python desk/drawer/plans/workspace-documental/validate_plan.py` verifica coherencia. `python desk/drawer/plans/workspace-documental/render_diagram.py` genera Mermaid y HTML mediante spec2viz. El modo `build_plan.py --check` no escribe y detecta proyecciones obsoletas.

[Diagrama interactivo](dag.diagram.graph.html) · [Mermaid](dag.diagram.mmd) · [Validación](validation.txt). El diagrama incluye gates como nodos; leer flechas de prerequisito a dependiente, sin confundir estado pendiente con implementación.

Revisiones independientes y resolución de hallazgos en [reviews](reviews/README.md). Los IDs antiguos A1–H2 se conservan en legacy_mapping de dag.yaml para trazabilidad, no como otro DAG activo. No se modificaron tareas ajenas ni el Board de graph_ui.
'''
# Draw evidence gates explicitly, including their producer when internal.
producers = {k:v['produced_by'] for k,v in D['gates'].items() if v.get('produced_by')}
nodes = {t['id']: {'label': t['id'] + ': ' + t['title'], 'kind': 'core'} for t in D['tasks']}
nodes.update({k: {'label': k + ' [' + v['state'] + ']', 'kind': 'boundary'} for k, v in D['gates'].items()})
edges = [{'from': p, 'to': t['id'], 'relation': 'prerequisite', 'label': ''} for t in D['tasks'] for p in t['depends_on'] + t['requires']]
edges += [{'from': v, 'to': k, 'relation': 'evidence', 'label': 'evidencia'} for k, v in producers.items()]
for t in D['tasks']:
    for variant in t.get('variants', []):
        label = variant['when']['parameter'] + '=' + variant['when']['equals']
        edges += [{'from': dep,'to': t['id'],'relation': 'conditional','label': label} for dep in variant['depends_on'] + variant['requires']]
spec = {'id': 'workspace-documental-dag', 'title': 'Workspace documental: entregables y gates', 'type': 'component', 'version': '0.1', 'data': {'nodes': nodes, 'edges': edges}}
outputs[B / 'dag.diagram.yaml'] = yaml.safe_dump(spec, allow_unicode=True, sort_keys=False)
if args.check:
    stale = [str(p.relative_to(ROOT)) for p, text in outputs.items() if not p.exists() or p.read_text() != text]
    if stale:
        raise SystemExit('STALE: ' + ', '.join(stale))
    print('Generated table/task files/diagram spec match dag.yaml')
else:
    for p, text in outputs.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    print(f'Generated {len(outputs)} planning projections')
