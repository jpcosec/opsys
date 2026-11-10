FILE:desk/tasks/task-cc33b-reglas-de-cierre-ruledocs-por-tipo-sobre-task-completes-y-reglas-de-campo-se-borran-los-hechos.md
---
sldb:
  by: agent
  at: '2026-11-10T18:56:19Z'
  authority: generated
  via: create_document
id: task-cc33b-reglas-de-cierre-ruledocs-por-tipo-sobre-task-completes-y-reglas-de-campo-se-borran-los-hechos
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
- deskops/data/rules/
- deskops/data/lifecycle/
- deskops/models/task_types.py
- deskops/operations.py
- deskops/cli/commands/operations.py
- deskops/services/tasks.py
- deskops/services/closeout_gates.py
- deskops/services/closure.py
- deskops/lifecycle.py
- deskops/atom_tags.py
- deskops/domain_tree.py
- deskops/services/atoms.py
- tests/
- docs/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC33b: Reglas de cierre - RuleDocs por tipo sobre task_completes y reglas de campo; se borran los hechos y gates viejos

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC33b del plan deskops-como-config, dag rev 4: partes (2), borrado de (3) y regla de evidencia (DA5) del agregado CC33. Depende de CC33a (en main, 6d133045). Gates G_GO06 y G_GO08 satisfied.

## Goal

_Describe the concrete result this task must produce._

El cierre de cada tipo de tarea lo decide una RuleDoc semilla on_transition sobre task_completes que exige los recibos evidence de CC33a; las reglas de campo son RuleDocs alert; se borran __closeout_evidence__, closeout_evidence_verified, pill_graduation_verified y _add_closeout_facts; los chequeos de CC38 asignados a CC33 pasan a RuleDoc o quedan con razón.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/data/rules/, deskops/data/lifecycle/, deskops/models/task_types.py, deskops/operations.py, deskops/cli/commands/operations.py, deskops/services/tasks.py, deskops/services/closeout_gates.py, deskops/services/closure.py, deskops/lifecycle.py, deskops/atom_tags.py, deskops/domain_tree.py, deskops/services/atoms.py, tests/, docs/, CHANGELOG.md, desk/rituals vía deskops. Fuera: grafo (CC33c), selectores y escrituras, tags por API de sldb (DO7).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 4, CC33b). SCOPE: Partes (2), el borrado de (3) y la regla de evidencia (DA5) del scope de CC33: por tipo, una RuleDoc semilla on_transition sobre la arista task_completes (where current_node = "ritual-testing") que exige los recibos evidence de CC33a (atom|materialization como or de dos); los __closeout_evidence__ de GC01 se borran; las reglas sobre campos pasan a RuleDocs on_check/on_write alert (vocabulario de closeout_evidence, código implícito, python_changes_without_declared_tests, forma de URL, graduación de pills); se borran _add_closeout_facts y su limpieza, closeout_evidence_verified, pill_graduation_verified y has(closeout_evidence_verified); los 9 chequeos entre documentos que el inventario de CC38 asigna a CC33 pasan a RuleDoc y su chequeo viejo se borra en el mismo paso (DK6).

ACCEPTANCE: sin recibo commit accepted, la arista task_completes aparece en edges_blocked con la cláusula fact = "commit"; editar goal tras verificar vuelve a bloquear; grep de closeout_evidence_verified, pill_graduation_verified, _add_closeout_facts y __closeout_evidence__ en deskops/ vacío; los 9 chequeos de CC38 como RuleDoc con su función vieja borrada; tests de closeout verdes; goldens idénticos; deskops doctor sin hallazgos nuevos en los 6 desks; docs/workflow-policy-reference.md; ritual closeout vía deskops; CHANGELOG.

OUTPUT_SCOPE: deskops/data/rules/, deskops/models/task_types.py, deskops/operations.py, deskops/services/tasks.py, deskops/services/closeout_gates.py, deskops/lifecycle.py, tests/, docs/workflow-policy-reference.md, desk/rituals (vía deskops), CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-10, coordinador del plan; base origin/main 6d133045; CC33a en main, CC33c pendiente de integración):
a1 (recibos de CC33a): closeout verify (CLI) escribe ReviewDoc kind evidence con fact en {tests, commit, atom, materialization, document, external}, value, verdict y reason, nombre evidence-<fact>-<n>, subject anclado al contrato de la tarea (deskops/services/closure.py, write_receipts=True solo desde el CLI). La regla de cierre por tipo exige any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted") por cada kind de __closeout_evidence__ del tipo (deskops/models/task_types.py:41-105); atom|materialization como or de las dos.
a2 (DO6, decisiones.md): hoy closeout commit (_gate_outcome) y la vista del board llaman a verify sin escribir recibos. Este nodo decide y deja escrito en el TaskDoc si closeout commit escribe los recibos antes de evaluar la regla (si no, la regla bloquea tareas que solo pasaron por closeout commit). DO6 b: cuando el link gate pasa sin documento enlazante (desk exento, solo follow-up o guard-test de skill) no hay recibo atom ni materialization: la regla lo contempla (p. ej. or con el caso exento) o pide otro value; la elección va en el TaskDoc.
a3 (kinds sin productor): __closeout_evidence__ de task.refactor incluye goldens y el de task.aggregate children; CC33a no produce fact goldens ni children. goldens: la regla usa el recibo kind goldens de deskops review record (follow-up de CC32) si existe, si no hipótesis en el TaskDoc. children: no existe campo children (igual que en CC32); hipótesis en el TaskDoc y el tipo no tiene cláusula de hijos hasta que exista.
a4 (arista y semilla): deskops/data/lifecycle/closeout-task_completes.md tiene condition status = "ready_for_testing" and has(closeout_evidence_verified); al borrar el hecho, la condición de la arista queda sin has(...) y la exigencia de recibos pasa a las RuleDocs por tipo (on_transition, where current_node = "ritual-testing"), semillas en deskops/data/rules/ escritas en desk/lifecycle/ por desk update --apply, como las rule-activation-* de CC32.
a5 (borrado, grep de aceptación): closeout_evidence_verified y pill_graduation_verified en services/tasks.py:202-203 y :307, services/closure.py:836-837; __closeout_evidence__ en models/task_types.py, services/closure.py:1094 y cli/commands/operations.py:44 (el tipo pasa a leer sus kinds de la RuleDoc o de una tabla de datos; nada de atributo de clase). grep de los cuatro nombres en deskops/ vacío.
a6 (inventario de CC38, runs/subagents/cc38-worker-report.md filas 3, 5, 13, 14, 15, 18, 24, 25): cada una pasa a RuleDoc o queda con razón escrita. #3 (namespace en tag-namespaces.yaml) y #5 (prefijos de domain path con crossroad) chocan con DO7 (CC35d cortado; sldb H1-H2 en el drawer de sldb 6b34cd5f): si la RuleDoc necesita la API de tags de sldb, quedan como hipótesis con referencia a DO7; si se expresan con el lenguaje de reglas sin esa API, se escriben aquí. Las que lean el filesystem o la ruta (#13, #14, #18, #24) y el lenguaje no las exprese quedan como hipótesis y nota a sldb (regla común 7).
a7 (archivos): files suma deskops/data/lifecycle/, deskops/cli/commands/operations.py, deskops/services/closure.py, deskops/atom_tags.py, deskops/domain_tree.py, deskops/services/atoms.py y docs/ a los del nodo. desk/rituals vía deskops.
a8 (4 pasos): el coordinador corre los 4 pasos del workflow de deskops en clon limpio (los 90 archivos de test de a uno). Cada comando deskops tarda unos 30 s hasta que la lectura indexada de sldb entre.

## Validation

_List the checks required before this task can close._

- Sin recibo commit accepted, task_completes en edges_blocked con fact = "commit"; editar goal tras verificar vuelve a bloquear
- grep de closeout_evidence_verified, pill_graduation_verified, _add_closeout_facts y __closeout_evidence__ en deskops/ vacío
- Tests de a uno, test_cli y goldens desde /dev/shm
- deskops doctor sin hallazgos nuevos en los 6 desks
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

sin recibo commit accepted, la arista task_completes aparece en edges_blocked con la cláusula fact = "commit"; editar goal tras verificar vuelve a bloquear; grep de closeout_evidence_verified, pill_graduation_verified, _add_closeout_facts y __closeout_evidence__ en deskops/ vacío; los 9 chequeos de CC38 como RuleDoc con su función vieja borrada; tests de closeout verdes; goldens idénticos; deskops doctor sin hallazgos nuevos en los 6 desks; docs/workflow-policy-reference.md; ritual closeout vía deskops; CHANGELOG.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-cc33b-reglas-de-cierre-ruledocs-por-tipo-sobre-task-completes-y-reglas-de-campo-se-borran-los-hechos: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

