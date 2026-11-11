---
sldb:
  by: agent
  at: '2026-11-11T03:26:57Z'
  authority: generated
  via: save_document_payload
id: task-cc35c-referencias-entrantes-referrers-y-rewrite-references-dentro-de-la-transacción-menciones-en-pro
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/
- deskops/atom_references.py
- deskops/graph/desk_graph.py
- tests/
- docs/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC35c: Referencias entrantes - referrers y rewrite_references dentro de la transacción; menciones en prosa como MentionPattern

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC35c del plan deskops-como-config: parte (3) del agregado CC35. Depende de CC35a (transacción, en main) y CC33c (grafo de proyecto con la configuración de deskops, en main). Gate G_GD22 satisfied.

## Goal

_Describe the concrete result this task must produce._

atoms delete/split/merge, retire, drawer remove y closeout buscan y reescriben las referencias entrantes con referrers y rewrite_references de sldb dentro de la misma transacción; las menciones en prosa se ven por los MentionPattern de la configuración de grafo; se borran las búsquedas propias.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/services/, deskops/atom_references.py, deskops/graph/desk_graph.py, tests/, docs/, CHANGELOG.md. Fuera: la API de tags (CC35d resto, DO7) y las vistas (CC34).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml, CC35c). SCOPE: Parte (3) del scope de CC35. atoms delete/split/merge, retire, drawer remove y closeout usan referrers/rewrite_references (GD22) dentro de la misma transacción. Las menciones atom:<id> en prosa y los bullets del drawer se declaran como MentionPattern en la configuración de grafo de deskops que deja CC33. Por eso depende de CC33: esa parte queda en este nodo y no se movió a CC33.

ACCEPTANCE: grep -rn "_find_inbound_atom_references\|_rewrite_inbound_atom_references\|_inbound_references" deskops/ vacío; retire de una pill la quita del Board y de las tareas en una sola transacción; atoms merge reescribe menciones atom:<id> en prosa; goldens de ayuda y salida idénticos; tests de los archivos tocados verdes; deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/services/, deskops/atom_references.py, deskops/graph/desk_graph.py (MentionPattern), tests/, CHANGELOG.md

INVARIANTE (alcance.md):
1. **El formato del desk no cambia.** Los archivos que hoy existen en `desk/` (Board, tareas, rituales, pills, átomos, drawer, inbox, `desk/lifecycle/`, `desk/reviews/`, `tag-namespaces.yaml`, `config.json`) conservan su ruta, su modelo y su forma. Un nodo puede agregar documentos nuevos en carpetas que ya existen (`RuleDoc` en `desk/lifecycle/`; las `ViewDoc` viven solo en el paquete, sin `desk/views/`, DA4), siempre escritos por `deskops desk update --apply` y nunca a mano; no reescribe los existentes salvo los que ya eran gestionados por deskops (`desk/lifecycle/`).
2. **La gramática del CLI no cambia.** Los goldens de ayuda (`tests/fixtures/golden/help/*.txt`, 120 archivos, `test_output_goldens.py:316 test_help_goldens`) y de salida (`tests/fixtures/golden/output/`, `test_command_output_goldens` :669) quedan iguales. Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`), que entra con GC06 antes de este plan.
3. **Cada superficie borra su código viejo en el mismo paso.** Un nodo que cambia una superficie a sldb borra en el mismo commit el código de deskops que la implementaba, con un grep en su aceptación. No hay periodo con dos caminos.
4. **En cada paso**, los tests de los archivos tocados verdes, `deskops doctor` y `deskops view board` correctos en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), y la suite completa del repo tocado sin fallas nuevas contra main (la corre el supervisor sobre el resultado integrado; ver regla 3).

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos. Las revisiones en frío (preflight, cold-bundle con `deskops review`) las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`. Nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de deskops por nodo o grupo de nodos que el coordinador fije.
3. Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor una vez sobre el resultado integrado, sin fallas nuevas contra main. Un nodo no cierra con tests rojos ni saltados.
4. Antes de cambiar una superficie, el nodo captura sus goldens de salida (si no existen) sobre un desk de prueba; después del cambio deben ser idénticos, salvo lo que su aceptación nombre.
5. Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`; los rituales del desk que nombran el comportamiento cambiado se actualizan con `deskops` en el mismo nodo.
6. Compatibilidad de desks: lo que un nodo agrega o reescribe en `desk/` lo escribe `deskops desk update --apply` de forma idempotente (segunda corrida sin cambios), probado.
7. Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-11, coordinador del plan; base origin/main b990c49e, con CC33a, CC33b y CC33c cerrados):
a1 (lo que hay hoy): deskops/services/atoms.py _find_inbound_atom_references (:767) y _rewrite_inbound_atom_references (:788), que usan atoms delete, split y merge (:222, :309, :389-393). deskops/services/retire.py _inbound_references (:212), que usa retire (:96). Los números de línea son orientativos; se localiza por nombre.
a2 (API de sldb, GD22): sldb.api.edges.referrers(store, target) y sldb.api.edges.rewrite_references(store, target, replacement, transaction=..., dry_run=...). Se llaman dentro de la misma desk_transaction (CC35a) que hace la escritura principal, así que un fallo revierte todo.
a3 (menciones en prosa): la configuración de grafo de deskops/graph/desk_graph.py ya declara MentionPattern ATOM (atom-<slug>), TASK_OR_ISSUE y SOURCE_PATH (CC33c). Este nodo comprueba que referrers de sldb ve las menciones atom:<id> en prosa y los bullets del drawer a través de esa configuración. Si no las ve, el MentionPattern que falte se suma ahí; si sldb no admite el caso, hipótesis y nota a sldb.
a4 (drawer remove y closeout): se localizan las vías que hoy quitan referencias entrantes a un documento borrado. Si no tienen, se deja escrito en el informe; no se inventan.
a5 (aceptación de retire de una pill): un test sobre tmp_path con una pill ligada en el Board y en dos tareas. `deskops retire` (o el comando que retire pills hoy) la quita de los tres en una sola transacción y deja un solo commit o una sola escritura atómica. Si se fuerza un fallo a mitad, nada cambia en disco.
a6 (DO8): el grafo se arma con ProjectGraph(root, desk_graph_config()) en proceso, no con sldb.api.project_graph(store).
a7 (files): deskops/services/, deskops/atom_references.py, deskops/graph/desk_graph.py, tests/, docs/, CHANGELOG.md.
a8 (4 pasos): sldb stores build --store .sldb; pytest, un proceso por archivo de tests/; sldb stores build --check --store .sldb; bash scripts/ci-knowledge-check.sh . Los corre el coordinador en clon limpio.

DISPOSICIÓN DE PREFLIGHT-1 Y BUNDLE-1 (2026-11-11, coordinador del plan; decisiones revisables):
b1 (formas de mención): en el desk hay dos formas, `atom:atom-<slug>` (con prefijo de kind) y el id pelado `atom-<slug>`, a veces entre backticks. MentionPattern ATOM ya captura la segunda; la primera la cubre el target "atom:{0}". El test de atoms merge usa las dos y comprueba que las dos se reescriben. Si una no la ve referrers, se suma el patrón que falte en desk_graph.py.
b2 (criterio para la nota a sldb): si con el MentionPattern declarado `sldb.api.edges.referrers` no devuelve la mención de una de las dos formas sobre un desk de tmp_path, es caso de sldb: hipótesis en el informe con el desk mínimo que lo reproduce. El coordinador abre la nota.
b3 (drawer remove y closeout): las vías son `deskops drawer remove` (services/drawer.py remove_entry) y los cierres de closeout que borran la tarea (commit, supersede, retire, resolved-by). Si alguna hoy no toca referencias entrantes, sigue sin tocarlas (no se suma comportamiento). Cuando borra un documento que tiene referrers, reporta los que quedan colgando con un alert que nombra cada referrer, sin reescribir. Se prueba en un caso.
b4 (retire de una pill): el comando es `deskops retire <path> --reason --ref` (acepta pills). Lo que se exige y prueba es una sola desk_transaction: Board y tareas se reescriben en la misma transacción, y un fallo forzado a mitad deja el disco sin cambios. El commit no es parte de retire.
b5 (líneas antes y después): tabla en el informe runs/subagents/cc35c-worker-report.md con `wc -l` de cada archivo tocado de deskops/services/, deskops/atom_references.py y deskops/graph/desk_graph.py, antes (base) y después.
b6 (docs/): sí entra. docs/operator-manual.md, en las secciones de atoms delete/split/merge, retire y drawer remove, si cambia lo que el operador ve.

## Validation

_List the checks required before this task can close._

- grep -rn "_find_inbound_atom_references\|_rewrite_inbound_atom_references\|_inbound_references" deskops/ vacío
- retire de una pill la quita del Board y de las tareas en una sola transacción (a5)
- atoms merge reescribe menciones atom:<id> en prosa
- Goldens de ayuda y salida idénticos; tests de los archivos tocados verdes
- deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

grep -rn "_find_inbound_atom_references\|_rewrite_inbound_atom_references\|_inbound_references" deskops/ vacío; retire de una pill la quita del Board y de las tareas en una sola transacción; atoms merge reescribe menciones atom:<id> en prosa; goldens de ayuda y salida idénticos; tests de los archivos tocados verdes; deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después; CHANGELOG.
