---
sldb:
  by: agent
  at: '2026-11-09T19:48:43Z'
  authority: generated
  via: save_document_payload
id: task-cc33a-recibos-de-evidencia-closeout-verify-escribe-reviewdoc-kind-evidence-y-queda-como-orquestador
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
- deskops/services/closeout_gates.py
- deskops/services/closure.py
- deskops/models/review.py
- deskops/cli/commands/closeout.py
- tests/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC33a: Recibos de evidencia - closeout verify escribe ReviewDoc kind evidence y queda como orquestador

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC33a del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 4: parte (1), recibos de evidencia, del agregado CC33 (L, partido en la rev 4), en PF2, árbol T3.3. Depende de CC32 y CC38, los dos en main. Gates: G_GO06 y G_GO08, satisfied. Se promueve el 2026-11-09 con preflight y cold-bundle dispuestos; el worker se despacha cuando el overlord habilite la cuota.

## Goal

_Describe the concrete result this task must produce._

deskops closeout verify corre los productores de hechos de git y archivos y escribe, por cada kind de evidencia verificado, un ReviewDoc kind evidence (fact, value, verdict accepted o rejected, subject anclado al contrato de la tarea), sin duplicar recibos en una verificación repetida sin cambios. verify_task_closeout queda como orquestador y devuelve el mismo envelope que hoy. El gate de cierre todavía no cambia: lo cambia CC33b.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/services/closeout_gates.py (solo productores de hechos), deskops/services/closure.py (verify_task_closeout y los productores que viven ahí: _closeout_link_gate, _skill_guard_test_evidence, _generated_artifact_source_finding), deskops/models/review.py (kind evidence y sus campos), deskops/cli/commands/closeout.py (si la salida de verify lo necesita), tests/ y CHANGELOG.md. Fuera: RuleDocs de cierre, borrado de _add_closeout_facts y __closeout_evidence__ (CC33b), el grafo (CC33c), close_superseded, close_retired, close_with_run y close_resolved_by.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 4, CC33a, hijo del agregado CC33). SCOPE: Partes (1) y la mitad orquestadora de (3) del scope de CC33. closeout_gates.py queda solo con los productores de hechos de git y archivos (reference_points_to_commit, reference_points_to_test, reference_points_to_document, el enlace atom/materialization, _skill_guard_test_evidence, _generated_artifact_source_finding). deskops closeout verify corre los productores y escribe, por cada kind de evidencia verificado, un ReviewDoc kind evidence con fact = <kind> (tests | commit | atom | materialization | document | external), value, verdict accepted o rejected con reason y subject anclado al contrato de la tarea; una verificación repetida sin cambios no crea recibo nuevo (mismo input_sha256). verify_task_closeout queda como orquestador (corre productores, escribe recibos, devuelve el mismo envelope que hoy). Las reglas que leen esos recibos son de CC33b; hasta entonces el gate de cierre sigue siendo el de hoy.

ACCEPTANCE: closeout verify sobre una tarea task.code con commit en HEAD, test existente y atom enlazado escribe tres recibos evidence accepted y devuelve el mismo envelope que el golden previo; sin commit, el recibo commit queda rejected; una segunda verify sin cambios no crea recibos; editar goal deja los recibos changed (anchor_state); tests de test_closeout*.py verdes con los mismos escenarios; goldens de ayuda y salida idénticos; líneas de closeout_gates.py antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/services/closeout_gates.py, deskops/services/closure.py (solo la llamada a verify), deskops/models/review.py, deskops/cli/commands/closeout.py, tests/, CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-09, coordinador del plan; base origin/main con dag rev 4):
a1 (dónde está el código hoy; las líneas del dag son de antes de CC30): verify_task_closeout vive en deskops/services/closure.py:578 (operations.py:186 solo delega). Los productores están en closure.py: _closeout_link_gate :773, _skill_guard_test_evidence :880 y _generated_artifact_source_finding :925. Los de referencias están en closeout_gates.py (293 líneas): reference_points_to_url :127, _document :131, _test :148 y _commit :183. reference_points_to_atom está en services/atoms.py:71. Por eso closure.py entra en files completo para verify y sus productores, no solo «la llamada a verify». close_* no se toca.
a2 (modelo del recibo): ReviewKind (models/review.py:33) no tiene «evidence». Se agrega «evidence» y dos campos opcionales al ReviewDoc, fact (Literal tests|commit|atom|materialization|document|external, vacío salvo en kind evidence) y value (str). Un validador del modelo (DK6) exige fact cuando kind = evidence y lo prohíbe en los demás kinds. Los recibos existentes no cambian de forma: los campos nuevos son opcionales, con default vacío.
a3 (escritura del recibo): por la vía de escritura de deskops sobre sldb (CC35a), como _write_review de services/review.py, sin llamar al modelo. engine «deskops-closeout», subject doc:<Modelo>:<task> (el pin llega en la primera reescritura; ver H-CC32-2: create_document no pinnea), input_sha256 = sha256 del valor verificado (fact + value + el hash de contenido del archivo o el id de commit). Repetir la verificación sin cambios encuentra el mismo input_sha256 y no escribe nada. Un input distinto escribe un recibo nuevo (n+1) y deja el anterior.
a4 (envelope): el JSON y el texto de closeout verify quedan idénticos a hoy (goldens de salida). Los recibos son un efecto adicional. Si un golden de salida cambia, el worker para y avisa.
a5 (paralelo): closeout resolved-by (wt/closeout-resolved-by) agrega close_resolved_by en closure.py; si se integra antes, el worker rebasea. CC35b cambia la resolución de documentos en doc_access/services: CC33a no la toca.
a6 (reglas de activación sin aplicar en el desk de deskops): el runtime siembra desk/lifecycle/rule-activation-*.md sin trackear. No se commitea nada de desk/ ni de .sldb/.
a7 (tests, de a uno): un test nuevo por cada caso de la aceptación (tres recibos accepted; commit rejected; segunda verify sin recibos nuevos; goal editado → anchor_state changed tras reescribir el recibo); test_closeout.py, test_closeout_atomless.py, test_closeout_declared_evidence.py, test_closeout_skill_links.py, test_closeout_gates.py, test_closeout_test_paths.py y test_review_doc.py; test_cli y test_output_goldens desde una copia en /dev/shm, sin --update-golden.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1) Y DEL COLD-BUNDLE (review-...-bundle-1), 2026-11-09:
b1 (accepted o rejected por kind): solo reciben recibo los kinds que exige el tipo de la tarea más su closeout_evidence. Cada kind queda accepted si su productor de hoy encuentra evidencia, y rejected si no:
- tests: alguna referencia pasa reference_points_to_test;
- commit: reference_points_to_commit;
- atom y materialization: el enlace de _closeout_link_gate;
- document: reference_points_to_document;
- external: reference_points_to_url.
reason es el texto que hoy da el gate cuando falta ese kind.
b2 (value e input_sha256): value es lo que pasó, ordenado y con rutas POSIX, unido con «\n». Para tests, las referencias; para commit, el id completo; para atom/materialization, los ids o rutas enlazados; para document, las rutas; para external, las URLs. input_sha256 = sha256 de «fact\nvalue\n» seguido, por cada ruta de archivo de value, del sha256 de sus bytes; para commit, el sha completo. Es determinista.
b3 (closure.py): manda a1. En closure.py se editan verify_task_closeout y sus productores; los close_* no.
b4 (anchor_state): no es un campo del modelo. Lo calcula sldb (GO07) comparando el @sha256 pinneado en ReviewDoc.subject con el hash de contrato actual de la tarea. Los tests lo leen por sldb, como los de CC32 (tests/test_activation_rules.py: el finding con anchor_state, o check_doc_anchors).
b5 (CC35a): está en main (8d0e23fe, cerrado); por eso depends_on está vacío. La vía de escritura es doc_access.create_doc/write_doc sobre la transacción de sldb, la que usa _write_review.
c1 (pin al nacer): como un recibo evidence nace con veredicto y no pasa por dispose, se escribe pinneado. create y, en la misma transacción, una reescritura sin cambios del payload que dispara save_document_payload y pinnea el subject (como tests/activation_receipts.py de CC32, H-CC32-2). El test lo verifica: subject con @sha256 tras verify.
c2 (cuándo no se escribe): se salta la escritura solo si ya existe un recibo evidence del mismo fact para la tarea con el mismo input_sha256 y anchor_state intact. Si el contrato cambió (goal editado → changed), una verify nueva escribe un recibo nuevo (n+1) aunque el input_sha256 sea el mismo. El recibo viejo queda como está.
c3 (_write_review): está en deskops/services/review.py (en el repo; el worker lo lee). Arma el payload del ReviewDoc y llama a doc_access.create_doc(root, path, ReviewDoc, payload, review_id). «Sin llamar al modelo» quiere decir sin LLM; la validación del modelo ReviewDoc sí corre. Si reusar _write_review exige tocar review.py más allá de lo mínimo, el worker escribe su propio helper en closure.py con la misma llamada a doc_access.

## Validation

_List the checks required before this task can close._

- Tests nuevos por caso de la aceptación (a7)
- Goldens de salida y ayuda idénticos
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_closeout*.py, test_review_doc; test_cli y test_output_goldens desde /dev/shm
- wc -l de closeout_gates.py y closure.py antes y después
- CHANGELOG

## Done When

_Name the observable condition that makes the task complete._

closeout verify escribe recibos evidence accepted o rejected por kind, sin duplicarlos en una verificación repetida, y devuelve el mismo envelope (goldens idénticos). ReviewDoc admite kind evidence con fact y value. Tests de closeout y de review_doc verdes, más los nuevos. Líneas de closeout_gates.py antes y después. CHANGELOG.
