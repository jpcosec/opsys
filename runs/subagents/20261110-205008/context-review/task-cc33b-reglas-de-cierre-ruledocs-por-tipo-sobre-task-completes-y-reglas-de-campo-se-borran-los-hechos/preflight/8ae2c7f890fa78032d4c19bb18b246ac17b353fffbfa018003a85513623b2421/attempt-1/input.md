FILE:desk/tasks/task-cc33b-reglas-de-cierre-ruledocs-por-tipo-sobre-task-completes-y-reglas-de-campo-se-borran-los-hechos.md
---
sldb:
  by: agent
  at: '2026-11-10T20:49:33Z'
  authority: generated
  via: save_document_payload
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

DISPOSICIÓN DE PREFLIGHT-1 Y BUNDLE-1 (2026-11-10, coordinador del plan; decisiones revisables):
b1 (cuántos chequeos): el inventario de CC38 (runs/subagents/cc38-worker-report.md) asigna a CC33 8 filas: 3, 5, 13, 14, 15, 18, 24 y 25. El «9» del contrato es la estimación del plan. La fuente es el informe y no hay que buscar un noveno.
b2 (a2, closeout commit): closeout commit NO escribe recibos. Evalúa la regla sobre los recibos que ya escribió `deskops closeout verify`. Si faltan o no están intactos, el bloqueo muestra los findings de edges_blocked y dice que se corra `deskops closeout verify`. El ritual de closeout (vía deskops) queda en este orden: verify, luego commit. La vista del board sigue sin escribir.
b3 (DO6 b, link exento): cuando el link gate pasa sin documento enlazante (desk exento, solo follow-up o guard-test de skill), verify escribe un recibo evidence fact = "atom", verdict accepted, value "exempt: <motivo del gate>". Así la cláusula atom|materialization de la regla no necesita un caso especial. Es un cambio a CC33a dentro de services/closure.py, con test.
b4 (a3): el recibo goldens existe en main: `deskops review record --kind goldens` (seguimiento de CC32, cerrado). La regla de task.refactor exige any(^subject: kind = "goldens" and anchor_state = "intact" and verdict = "accepted") en lugar de un fact goldens. children: TaskAggregateDoc no tiene campo children, así que se deja hipótesis en el TaskDoc y la regla de aggregate no tiene cláusula de hijos (igual que CC32).
b5 (criterio de expresividad, a6): una fila pasa a RuleDoc si se expresa en el lenguaje de reglas de sldb, es decir con campos del documento, refs a otros documentos, any/all sobre aristas y has()/exists. Se comprueba con `sldb rules explain` sobre un caso bueno y uno malo. Lo que necesita el filesystem, la ruta o el nombre del archivo, o un archivo que no es documento del store, queda en el código con su razón: #3 tag-namespaces.yaml, #13 nombre de archivo, #14 provenance en disco, #18 desk/config.json y #24 artefacto renderizado. Se agrupa en una sola nota de inbox a sldb. #5 (prefijos con crossroad) depende de H1 de sldb (anchored_by con valor sin namespace, drawer de sldb 6b34cd5f) y queda por DO7. #15 (typed_as existe) y #25 (referencia a documento existente) se intentan como RuleDoc; si no salen, hipótesis.
b6 (aceptación de los chequeos): «los chequeos de CC38 como RuleDoc con su función vieja borrada» vale para los que pasan a RuleDoc. Los que quedan por b5 se listan en el informe con su razón y se eximen del grep, como p10 de CC38.
b7 (reglas de campo): cada RuleDoc alert traduce la condición del chequeo Python actual. Se localiza por nombre, porque los números de línea de a5 pueden haberse movido: el vocabulario de closeout_evidence, la alerta de código implícito, python_changes_without_declared_tests, la forma de URL y la graduación de pills (operations.py). Mismo texto de mensaje que hoy. Si una no se expresa, hipótesis y queda en el código.
b8 (goldens): los de ayuda (tests/fixtures/golden/help/*.txt) y los de salida (tests/fixtures/golden/output/), con test_output_goldens.py sin --update-golden. Si un golden tiene que cambiar (por ejemplo el mensaje de cierre bloqueado), el worker para y avisa con el diff.
b9 (doctor): la línea base es `deskops doctor` en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui) con la base del worktree, antes de cambiar nada. Después, el conjunto de errores y alertas no suma ninguno. Las dos capturas van al informe.

DISPOSICIÓN DE PREFLIGHT-2 Y BUNDLE-2 (2026-11-10, coordinador del plan; decisiones revisables):
c1 (8 contra 9): b1 manda sobre el número del contrato. La aceptación se cumple con las 8 filas del inventario; no se busca un noveno chequeo.
c2 (forma de la RuleDoc): la plantilla son las rule-activation-task-*.md de deskops/data/rules/ (CC32). Un archivo por tipo, rule-closeout-task-<tipo>.md. Frontmatter:
- subject "model <= <Clase del tipo>" (por ejemplo TaskCodeDoc), que liga la regla al tipo por la familia del modelo;
- where current_node = "ritual-testing";
- moment on_transition;
- severity error;
- condition: una cláusula any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted") por cada kind; atom|materialization va como or de dos any;
- message en español que nombra el tipo.
Se aplica a la arista task_completes igual que las de activación se aplican a la suya; ver cómo lo resuelve lifecycle/advance para las rule-activation.
c3 (de dónde lee el tipo sus kinds): de una tabla de datos, deskops/data/rules/closeout-evidence.yaml (task_type -> lista de kinds), no de la RuleDoc. La leen closure.py (qué productores corre verify) y cli/commands/operations.py. Un test comprueba que las cláusulas de cada rule-closeout-* coinciden con la tabla.
c4 (gates viejos): son los atributos __closeout_evidence__ de las clases de task_types.py y has(closeout_evidence_verified) en la arista. Los productores de closeout_gates.py se quedan: son los hechos de git y archivos de CC33a.
c5 (DA5, decisiones.md): la evidencia de cierre es solo por tipo. `--evidence` (closeout_evidence de la tarea) solo suma kinds, nunca quita. Un kind extra de la tarea se verifica, se escribe su recibo y, si falla, se reporta como alert sin bloquear.
c6 (goldens): la regla es «idénticos». b8 es el procedimiento si alguno pareciera tener que cambiar: el worker para y avisa, y el coordinador decide. No hay contradicción.
c7 (4 pasos del workflow de deskops, .github/workflows): sldb stores build --store .sldb; pytest, un proceso por archivo de tests/; sldb stores build --check --store .sldb; bash scripts/ci-knowledge-check.sh . Los corre el coordinador en clon limpio. El worker corre los tests de los archivos que toca.
c8 (condición y mensaje de cada fila): el inventario está en main, en runs/subagents/cc38-worker-report.md, y cada fila apunta al archivo y la línea de su chequeo. La regla traduce esa condición y conserva el mensaje del chequeo.
c9 (ritual): desk/rituals/closeout.md. Se edita vía deskops (edit ritual) para que los pasos digan: verify escribe los recibos y commit evalúa la regla (b2).

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

