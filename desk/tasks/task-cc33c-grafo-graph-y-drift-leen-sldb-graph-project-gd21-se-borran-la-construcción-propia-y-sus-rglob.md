---
sldb:
  by: agent
  at: '2026-11-10T14:18:41Z'
  authority: generated
  via: save_document_payload
id: task-cc33c-grafo-graph-y-drift-leen-sldb-graph-project-gd21-se-borran-la-construcción-propia-y-sus-rglob
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-008-kgdb-sldb-boundary.md
- desk/contexts/pill-009-source-file-graph-traceability.md
- desk/contexts/pill-010-graph-runtime-output-policy.md
- desk/contexts/pill-011-self-reflection-noise-control.md
- desk/contexts/pill-drift-checks-are-review-surfaces-not-mutators.md
files:
- deskops/graph/
- deskops/cli/commands/graph.py
- deskops/cli/commands/drift.py
- tests/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC33c: Grafo - graph y drift leen sldb graph project (GD21); se borran la construcción propia y sus rglob

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC33c del plan deskops-como-config, dag rev 4: parte (4), grafo, del agregado CC33. Depende de CC38 (en main). Gate G_GD21, satisfied.

## Goal

_Describe the concrete result this task must produce._

deskops graph build|neighbors|missing|reflect y drift leen el grafo de proyecto de sldb (GD21) con la configuración de desk_graph.py; se borran snapshot.py como construcción propia, el rglob de checks.py y los de self_reflection.py; neighbors y missing dan lo mismo que el oráculo v1 y después tests/graph_oracle_v1/ se borra.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/graph/, deskops/cli/commands/graph.py, deskops/cli/commands/drift.py, tests/ y CHANGELOG.md. Fuera: closeout (CC33a/CC33b), selectores y escrituras.

## Implementation Path

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 4, CC33c). SCOPE: Parte (4) del scope de CC33: deskops graph build|neighbors|missing|reflect y drift leen sldb graph project (GD21) con la configuración de grafo de deskops declarada como dato en project_graph; se borran graph/snapshot.py (construcción propia), graph/checks.py (rglob → missing de GD21) y los rglob de graph/self_reflection.py; tests/graph_oracle_v1/ se conserva hasta la aceptación y luego se borra. El enlace atom/materialization que usa el closeout (CC33a) se lee de ese grafo cuando este nodo entra.

ACCEPTANCE: deskops graph neighbors y missing dan lo mismo que el oráculo v1 sobre el desk real de deskops y después tests/graph_oracle_v1/ se borra; grep de rglob en deskops/graph/ vacío; goldens de ayuda y salida idénticos; deskops doctor sin hallazgos nuevos en los 6 desks; líneas de graph/ antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/graph/, deskops/cli/commands/graph.py, deskops/cli/commands/drift.py, tests/, CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-10, coordinador del plan; base origin/main 3951bb04):
a1 (lo que ya está en main): desde 4a9a4bbb, deskops/graph/desk_graph.py (212 líneas) es la configuración del desk para sldb.api.edges.project_graph (GD21: ProjectGraphConfig, DocumentSurface, DeclaredFileTargets, FileExclusions), y checks.find_missing_graph_references ya lee extract_declared_edges de ahí. extract_docs/extract_edges/extract_sources están congelados en tests/graph_oracle_v1/ como oráculo (lo usan tests/closeout_graph_oracle.py y tests/graph_oracle_v1/).
a2 (lo que falta, inventario en main): deskops/graph/snapshot.py (364 líneas; build_graph_snapshot :128, write_graph_snapshot, read_graph_neighbors) arma su propio snapshot. deskops/graph/checks.py :151 hace rglob("*.md") por superficie. deskops/graph/self_reflection.py (433 líneas) y cli/commands/graph.py (167 líneas: _build, _neighbors, ...) y cli/commands/drift.py (29) leen ese snapshot. Este nodo pasa graph build|neighbors|missing|reflect y drift a sldb.api.project_graph (o sldb graph project) con la configuración de desk_graph.py, y borra la construcción propia y los rglob.
a3 (oráculo): neighbors y missing tienen que dar lo mismo que el oráculo v1 sobre el desk real de deskops (copia en /dev/shm). Recién después se borra tests/graph_oracle_v1/, en un commit propio que nombra la comparación.
a4 (la decisión revisable de main-en-verde-2): graph missing no reporta un target declarado que existe como archivo dentro del root (deskops/graph/checks.py, declared_target_is_a_file, tests/test_graph_missing_existing_files.py). Este nodo decide si el grafo de sldb ya crea esos nodos (.yaml del drawer, fixtures .json). Si los crea, se borra la excepción y su test cambia a «aparece como nodo». Si no, la excepción queda y se anota como hipótesis para sldb.
a5 (verificación): los 4 pasos del workflow de deskops en un clon limpio (los corre el coordinador) más deskops doctor en los 6 desks. Archivos de test de a uno: test_graph_* y closeout_graph_oracle, test_cli y test_output_goldens desde /dev/shm, sin --update-golden.
a6 (rendimiento): cada comando CLI tarda unos 30 s mientras el arreglo de rule_graph de sldb espera el CI verde de sldb. Los archivos largos se corren por nodo.

PRECISIONES DEL PREFLIGHT Y DEL COLD-BUNDLE (preflight-1 y bundle-1, 2026-11-10):
b1 (CC38): CC38 está cerrada en main (47ab1102). Una dependencia cerrada no se lista (DC6). depends_on vacío no bloquea nada.
b2 (interfaz): la API Python sldb.api.project_graph(store), que ya usa desk_graph.py. No se llama al CLI sldb graph project desde deskops.
b3 (decidir a4): la evidencia es el resultado de project_graph sobre la copia del desk real. Si entre sus nodos están desk/drawer/plans/deskops-como-config/dag.yaml y tests/fixtures/model_contract_hashes.json (los casos de main-en-verde-2), el grafo los «crea»: se borra declared_target_is_a_file y su test pasa a «es un nodo del grafo». Si no están, la excepción queda y el informe la anota como hipótesis para sldb.
b4 (closeout): este nodo no toca closeout ni CC33a. Si el enlace atom/materialization del closeout ya lee desk_graph (closure._closeout_link_gate), no cambia. Si leía snapshot.py, el informe lo dice y se coordina con CC33a/b. No se edita closure.py.
b5 (oráculo): «lo mismo» es igualdad semántica, el mismo conjunto de (source, target, kind) en neighbors y de findings en missing, sobre una copia en /dev/shm del desk real de deskops (desk/ y .sldb/ de main al despachar). El orden no cuenta. El oráculo se borra en un commit propio dentro de este nodo, después de la comparación verde.
b6 (goldens): los de ayuda quedan idénticos. Los de salida también. Si alguno cambia porque la fuente del grafo es otra, el worker para y avisa con el diff; no lo regenera (manda «idénticos»).
b7 (4 pasos del workflow): los de .github/workflows de deskops: sldb stores build --store .sldb; python -m pytest tests -q (el coordinador, un proceso por archivo); sldb stores build --check --store .sldb; bash scripts/ci-knowledge-check.sh . Los corre el coordinador sobre un clon limpio.
b8 (drift): deskops drift check corre drift_check_role_docs y drift_check_runtime_bindings (materializers) y el chequeo de superficies de conocimiento. Este nodo solo cambia lo que lea el snapshot propio de graph/snapshot.py o haga rglob en deskops/graph/. Las comprobaciones de materializers no cambian.

PRECISIONES DE READINESS (2026-11-10, coordinador Scion sobre origin/main ba982a45):
b9 (build y reflect): la aceptación de equivalencia con el oráculo v1 aplica a `neighbors` y `missing`. `graph build` y `graph reflect` conservan su contrato actual de CLI y de salida: no se les exige una comparación nueva contra el oráculo, sólo que sus tests existentes y los goldens sigan verdes y que no aparezca una segunda fuente de verdad (siguen leyendo project_graph de sldb).
b10 (drift): el worker inspecciona `cli/commands/drift.py`; si no lee `graph/snapshot.py` ni hace `rglob`, no lo cambia y lo deja documentado en el informe. Si lee alguno de los dos, lo migra a project_graph con el mismo criterio de b9.
b11 (líneas antes/después): el informe lleva una tabla `archivo | antes | después` con `wc -l` por archivo de `deskops/graph/` y los comandos de graph/drift tocados. No hay umbral de reducción; el dato es evidencia.
b12 (base y copia del desk): la base es origin/main `ba982a45` y la copia real para el oráculo se toma de ese mismo commit en `/dev/shm`, con `.sldb/` incluido. El informe registra el SHA.
b13 (doctor): el baseline son las salidas de `deskops doctor` en los 6 desks con origin/main `ba982a45`; «sin hallazgos nuevos» significa que el conjunto de errores/alertas no agrega ninguno que no estuviera en ese baseline.
b14 (a4 y rglob): primero se corre `sldb.api.project_graph` sobre la copia de b12 y se registran los nodos de `desk/drawer/plans/deskops-como-config/dag.yaml` y `tests/fixtures/model_contract_hashes.json`. Si ambos aparecen como nodos, se borra `declared_target_is_a_file` y su test cambia a «es un nodo del grafo»; entonces el grep de `rglob` en `deskops/graph/` debe quedar vacío. Si no aparecen, el worker NO borra la excepción ni su test: PARA y avisa al coordinador con la evidencia de project_graph; la excepción queda como hipótesis para sldb y el grep se evalúa excluyendo esa única función, que se documenta en el informe.
b15 (precedencia de b14): b14 manda sobre la frase general «se borra el rglob de checks.py». Si b14 ordena PARAR porque project_graph no crea los dos nodos, el worker no borra `declared_target_is_a_file`, no borra ese rglob, deja el test como está y avisa con la evidencia; la aceptación de grep se evalúa excluyendo esa única función, documentada en el informe. Si b14 confirma los dos nodos, el borrado sí es incondicional y el grep debe quedar vacío.
b16 (precedencia de b10): b10 manda sobre la frase de scope para drift. Si `drift.py` no lee `snapshot.py` ni hace `rglob`, no se cambia y se documenta; no se inventa una migración de drift que no corresponde.
b17 (interfaz única): la única interfaz es `sldb.api.project_graph(store)` (b2). No se invoca el CLI `sldb graph project` desde deskops.
b18 (orden del oráculo): primero se implementa la migración y se prueba la paridad semántica; luego un commit de implementación con tests verdes; después un commit propio que borra `tests/graph_oracle_v1/` y actualiza sus referencias, sin cambiar código de producción en ese segundo commit.

## Validation

_List the checks required before this task can close._

- Comparación con el oráculo v1 sobre copia del desk real (a3)
- grep -rn rglob deskops/graph/ vacío
- Tests de a uno (a5), test_cli y goldens desde /dev/shm
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

graph neighbors y missing iguales al oráculo v1 sobre el desk real; tests/graph_oracle_v1/ borrado; grep de rglob en deskops/graph/ vacío; goldens idénticos; doctor sin hallazgos nuevos en 6 desks; 4 pasos del workflow verdes; CHANGELOG.
