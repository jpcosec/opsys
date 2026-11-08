# CC32 — Gates de activación de cada tipo de tarea como RuleDoc (produce G_CONSUMER)

Worker: robocop2-cc32-worker. Worktree `deskops-wt-cc32`, rama `wt/cc32`, base `origin/main 3cd46be8`.
Logs en `~/proyectos/SLDB_1/coord2-ccconfig/cc32/`. Commits: ver §Commits.

## Resumen

Cada tipo de fábrica tiene una RuleDoc `on_transition` sembrada managed en `desk/lifecycle/rule-activation-<tipo>.md`
desde `deskops/data/rules/`, con subject `model <= <Clase>`, `where current_node = "ritual-execution"`, severity
`error` y un mensaje en español que nombra el tipo. `deskops advance` pasa la tarea como `document=` a
`sldb.api.edges_holding`; sin arista en holding y con error de regla, el mensaje lista los findings de
`sldb.api.edges_blocked` (regla, nodo, cláusula, valor visto, testigo). `show` y `next` imprimen los mismos
findings. `__activation_receipts__` ya no existe en `deskops/`. El test de integración G_CONSUMER pasa en sus tres
pasos (`tests/test_activation_rules.py::test_g_consumer_activation_gate_in_three_steps`).

## Tabla de reglas por tipo

Forma de la cláusula de recibo: `R(k)` = `any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "k")`.
Cláusula de dependencias: `D` = `all(depends_on: status = "closed")`.

| Regla (desk/lifecycle/) | Subject | Condition | Message |
|---|---|---|---|
| `rule-activation-task-code.md` | `model <= TaskCodeDoc` | `R(preflight) and R(bundle) and D` | Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. |
| `rule-activation-task-docs.md` | `model <= TaskDocsDoc` | `R(preflight) and D` | Una tarea task.docs se activa con un recibo preflight aceptado e intacto y sus dependencias cerradas. |
| `rule-activation-task-debug.md` | `model <= TaskDebugDoc` | `R(preflight) and R(reproduction) and D` | Una tarea task.debug se activa con recibos preflight y reproduction aceptados e intactos y sus dependencias cerradas. |
| `rule-activation-task-refactor.md` | `model <= TaskRefactorDoc` | `R(goldens)` | Una tarea task.refactor se activa, además de lo que pide task.code, con un recibo goldens aceptado e intacto. |
| `rule-activation-task-decision.md` | `model <= TaskDecisionDoc` | `R(owner) and D` | Una tarea task.decision se activa con un recibo owner aceptado e intacto y sus dependencias cerradas. |
| `rule-activation-task-aggregate.md` | `model <= TaskAggregateDoc` | `D` | Una tarea task.aggregate se activa con sus dependencias cerradas. |
| `rule-activation-task-external.md` | `model <= TaskExternalDoc` | `R(preflight) and D` | Una tarea task.external se activa con un recibo preflight aceptado e intacto y sus dependencias cerradas. |

Decisiones de forma:

- **Orden de las hojas dentro de `any`**: `anchor_state` va primero. sldb elige como testigo de un `any` falso el
  primer elemento alcanzado (rules.md §9.5), y `seen` son las hojas de la primera rama falsa sobre ese testigo. Con
  `kind` primero, el testigo (la review `bundle-1`, que ordena antes que `preflight-1`) daba `seen: {"kind":"bundle"}` y
  el paso 3 de G_CONSUMER no mostraba `anchor_state = changed`. Con `anchor_state` primero el finding del paso 3 termina en
  `(witness: ReviewDoc:review-<task>-bundle-1 {"anchor_state":"changed"})`. La cláusula sigue nombrando
  `any(^subject: ...)` y `kind = "preflight"`; el test fija ese texto (b3). Es el mismo orden que usa sldb en su ejemplo
  (rules.md §10).
- **task.refactor sin `D`**: a5 dice que su regla «solo suma la cláusula de goldens» porque la de task.code ya le aplica
  por familia (`TaskRefactorDoc <= TaskCodeDoc`); repetir `D` daría dos findings idénticos por la misma dependencia.
  b1 («toda RuleDoc lleva `D`») se lee para los tipos que no heredan otra regla. Si el coordinador prefiere la lectura
  literal de b1, es una línea en `deskops/data/rules/rule-activation-task-refactor.md`.
- **task.aggregate** (b1): solo `D`; la cláusula de hijos va en §Hipótesis.

## Aceptación, línea por línea

1. **Test G_CONSUMER en tres pasos** — `tests/test_activation_rules.py::test_g_consumer_activation_gate_in_three_steps`.
   - Paso 1 (sin recibos): `deskops advance` exit 1, salida
     `Message: Gate ritual-execution is blocked by its rules: error: [rules/rule-activation-task-code] TaskCodeDoc:<id>: Una tarea task.code se activa con recibos preflight y bundle aceptados e intactos y sus dependencias cerradas. | any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight") (seen: {})`;
     `sldb rules explain` devuelve `holds: false` con esa misma `clause`.
   - Paso 2 (preflight y bundle accepted, pinneados `@sha256:` e intactos): exit 0, `Advanced to ritual-testing via task_activates.`
   - Paso 3 (`deskops edit task <id> goal ...`): exit 1, el finding termina en `(witness: ReviewDoc:review-<id>-bundle-1 {"anchor_state":"changed"})`.
   - Resultado del archivo: 10 passed sobre el HEAD final (`cc32/shm_test_activation_rules.log`, 41 s desde `/dev/shm`; antes,
     en el SSD, 8 passed + 2 passed en dos corridas por el tiempo de máquina).
2. **Tests por tipo** (mismo archivo):
   - `test_task_debug_requires_reproduction_and_not_bundle`: con preflight+bundle bloquea nombrando `kind = "reproduction"` y sin mencionar la regla de task.code; con reproduction activa.
   - `test_task_refactor_inherits_task_code_and_adds_goldens`: sin recibos bloquean las dos reglas (task.code por familia y task.refactor); con preflight+bundle solo queda `kind = "goldens"`; con goldens activa.
   - `test_desk_subtype_inherits_the_rules_and_a_desk_rule_adds_a_clause`: desk temporal (`deskops init` + `desk/models/cli_types.py` con `TaskCliDoc(TaskCodeDoc)` + `desk update --apply`); una tarea `task.code.cli` bloquea por `rules/rule-activation-task-code` sin código nuevo; una RuleDoc propia del desk (`model <= TaskCliDoc`, kind owner, creada con `sldb.api.transaction`) suma su cláusula; con owner activa.
   - `test_open_dependency_blocks_activation_and_the_finding_names_it`: con recibos y `depends_on` abierta, el finding trae `all(depends_on: status = "closed")` y `witness: TaskCodeDoc:<dependencia> {"status":"draft"}`.
   - `test_task_aggregate_needs_only_its_dependencies_closed`: activa sin recibos.
3. **`grep -rn __activation_receipts__ deskops/`** vacío (y `task_type_activation_receipts` también); test `test_no_activation_receipts_attribute_remains_in_the_package`.
4. **Copia del desk de deskops** (`coord2-ccconfig/cc32/deskcopy.sh`, salida en `cc32/deskcopy/`):
   - `desk update --apply` (1): `Lifecycle graph: wrote desk/lifecycle/rule-activation-task-{code,docs,debug,refactor,decision,aggregate,external}.md` y `Lifecycle graph: tracked ...` para las siete; exit 0.
   - `desk update --apply` (2): `Desk is up to date.`, exit 0 (`cc32/deskcopy/update.txt`).
   - `sldb rules check --store <copia>/.sldb` (sin `--subject`): `rules check: sin hallazgos`, exit 0.
   - `sldb rules explain RuleDoc:rule-activation-task-code TaskCodeDoc:task-cc32-...`: finding `holds: false`, `clause: any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight")`, exit 1 (`cc32/deskcopy/rules-explain.txt`).
   - Hallazgos de la copia no atribuibles a la rama: «Lifecycle documents to rewrite» (los tres RelationDoc del desk difieren del paquete, también con main) y «Stale document hashes» de `runs/` y `sldb/relation_types/` (la copia lleva solo `desk/` y `.sldb/`).
5. **Tests de a uno** (`cc32/run-tests.summary`, logs `cc32/<archivo>.log`): 

   Corridas en serie, un archivo por vez (`cc32/run-tests.sh`, `run-tail.sh`, `run-rerun.sh`, `run-shm.sh`; resumen en
   `cc32/run-tests.summary`, un log por archivo). La tanda final, sobre el HEAD `2a53f07b`, corrió desde una copia detached del
   worktree en `/dev/shm/deskops-cc32` (pedido del overlord: las corridas desde el SSD saturaban el disco; la copia se borró al
   terminar).

   | Archivo | Resultado | Dónde |
   |---|---|---|
   | `tests/test_activation_rules.py` (nuevo) | 10 passed (41 s) | shm |
   | `tests/test_task_types.py` | 16 passed | SSD (HEAD 1bf958d7, archivo sin cambios después) |
   | `tests/test_lifecycle_graph.py` | 9 passed | SSD, re-ejecutado tras 2a53f07b |
   | `tests/test_lifecycle_end_to_end.py` | 5 passed | SSD |
   | `tests/test_closeout_gates.py` | 7 passed | SSD |
   | `tests/test_scaffold_golden.py` | 2 failed antes de `--update-golden` (esperado: las 7 reglas), 3 passed después, 3 passed sin flag | SSD |
   | `tests/test_cli.py` | 101 passed (2 min) | shm (y 101 passed en SSD antes de 2a53f07b) |
   | `tests/test_desk_sync.py` | 8 passed | SSD, re-ejecutado tras 2a53f07b |
   | `tests/test_output_goldens.py` (ayuda + salida, sin `--update-golden`) | 7 passed | shm (y 7 passed en SSD) |
   | `tests/test_cli_help_examples.py` | 11 passed | SSD, re-ejecutado tras 2a53f07b |
   | `tests/test_operational.py` | 10 passed | SSD, re-ejecutado tras 2a53f07b |
   | `tests/test_desk_view.py` | 9 passed, 1 skipped (31 s) | shm; en el SSD agotó 1800 s y 2400 s dos veces (ver nota IO) |
   | `tests/test_doc_io.py` | 8 passed | SSD |
   | `tests/test_review_doc.py` | 13 passed, 1 xfailed (preexistente) | SSD |
   | `tests/test_review_command.py` | 12 passed | SSD |
   | `tests/test_promotion_nesting.py` | 2 passed | SSD |
   | `tests/test_cli_escape_hatches.py` | 9 passed | SSD |

   No corrí la suite completa (regla de máquina). Fallas conocidas de main no tocadas: `test_board_portable_references`,
   `test_skill_cli_drift`.

   **Nota IO** (pedido del overlord): desde el worktree del SSD `test_desk_view` tardaba >30 min y pasó en 31 s desde `/dev/shm`;
   `test_cli` bajó de 11 a 2 min. Tests que leen el repo real (no desks temporales): `test_taskdoc_read_without_overlay`
   (`rglob` sobre `desk/tasks` y `desk/drawer/tasks` del repo), `test_review_command` (`desk/drawer/plans/gates-por-tipo` del repo),
   y `test_doc_io`, `test_task_types`, `test_activation_rules` (`rglob("*.py")` sobre `deskops/`, chico). Ninguno recorre `.venv`
   ni `runs/` (`extract_sources` ya no existe en main). La lentitud del SSD venía del conjunto de corridas simultáneas (doctor de
   6 desks + pytest), no de un test que camine el repo entero.
6. **doctor y desk update en los 6 desks** (a13, `cc32/doctor6.sh` = plantilla de CC35a más `desk update --apply` ×2 con la rama
   y ×1 con main, y doctor tras el update; salida en `cc32/doctor/`, `run.log`; código main `a152d5e0` = `3cd46be8` en `deskops/`):
   - **doctor, copias sin tocar**: idéntico main vs rama en los 6 desks (`deskops: identical` ... `graph_ui: identical`).
   - **desk update --apply (1ª)**: idéntico en spec2viz y graph_ui (en ambos lados falla igual: `'sldb stores check' failed ... exit code 1`,
     desks legacy con `1 validation error for AtomDoc`, preexistente). DIFF en deskops, scion, pron y sldb: la rama suma las 7 líneas
     `Lifecycle graph: wrote desk/lifecycle/rule-activation-task-*.md` (y `tracked ...` donde el store existe); el resto del diff es del
     arnés (el `deskops` de main se extrae sin `.sldb`, así que main «registra los modelos directamente» mientras la rama ve
     `deskops-wt-cc32/.sldb` como store propietario y «hereda»; en sldb y pron además miles de líneas `Sections rebuild: ... missing`
     de documentos fuera de `desk/`), ver `cc32/doctor/diff-update-*.txt`.
   - **desk update --apply (2ª, rama)**: `Desk is up to date.` en deskops, sldb y pron. spec2viz y graph_ui: misma falla preexistente.
     scion: «Unregistered models ...» porque la 1ª saltó el registro (`Warning: ... already links 'deskops' to .../B/deskops/.sldb, not to
     .../deskops-wt-cc32/.sldb. Skipping model registration`). **Verificado que es del arnés**: el código de main con su `.sldb`
     presente hace exactamente lo mismo sobre scion (`cc32/scion-check.sh`, `cc32/doctor/mainowner-update*-scion.txt`,
     `mainowner-doctor-after-update-scion.txt`: mismo Warning, mismo «Unregistered models», doctor exit 1).
   - **doctor tras el update (rama)**: deskops y pron exit 0; sldb, spec2viz, graph_ui y scion exit 1 con los mismos errores que
     main antes del update (modelos no importables de sldb, desks legacy, modelos sin registrar en scion). Las dos líneas nuevas de
     sldb (`ArchitectureNarrativeDoc`, `StoreReadmeDoc` no importables) también aparecen con el código de main tras el update
     (`cc32/sldb-check.sh`, `mainowner-doctor-after-update-sldb.txt`).
   - **Alertas nuevas tras el update, en ambos lados**: `ReviewDoc:review-...: subject -> TaskCodeDoc:...: lost` (16 en deskops,
     21 en sldb, idénticas con main y con la rama): el reindexado con el sldb actual (GO07) expone que ningún recibo existente está
     pinneado (§CC35a). No son de la rama; son el estado real de los desks.
   - Sin hallazgos nuevos atribuibles a la rama, salvo las reglas trackeadas.
7. **wc -l antes y después**: §wc.
8. **CHANGELOG** (`## [Unreleased]` → Added y Changed) y `docs/workflow-policy-reference.md` (§Task types con la columna de recibos y la nueva sección «Activation rules» con la tabla de reglas por tipo).

## a3 — inventario de CC38

El inventario de CC38 no asigna ningún chequeo entre documentos a CC32 (9 a CC33, 0 a CC32); la frase del scope no
tiene objeto y el único código viejo borrado es `__activation_receipts__` (b2).

## a9 — recibos sin comando

`deskops review` produce `preflight`, `bundle` y `node`. `reproduction`, `goldens` y `owner` no tienen comando y la
gramática del CLI no cambia (invariante 2). Con las reglas instaladas, una tarea `task.debug`, `task.refactor` o
`task.decision` real no se activa hasta que exista una vía para esos recibos (hoy solo `sldb.api.transaction`, como hacen
los tests). Tareas en `ritual-execution` por desk y tipo (`cc32/a9-tasks.txt`, 2026-11-08):

| Desk | Tipo | Tareas | Afectadas por a9 |
|---|---|---|---|
| deskops | task.code | 2 (cc32, cc35a) | no (preflight y bundle tienen comando) |
| deskops | task.refactor | 3 (cc30, cc36, cc38) | **sí**: piden `goldens` |
| sldb | task.code | 1 (gd27) | no |
| sldb | task.docs | 2 (diseño-jerarquía-de-modelos, diseño-set-bootstrap) | no |
| graph_ui | `code` (legacy → task.code tras `desk update --apply`) | 2 | no |
| spec2viz, scion, pron | — | 0 | — |

Total: 10 tareas en ritual-execution en los 6 desks; 3 (los task.refactor de deskops) necesitan un recibo sin comando.

## a10 — efecto sobre el desk de deskops

Copia tras `desk update --apply` (`cc32/deskcopy/a10.txt`). Las 5 tareas en `ritual-execution` quedan bloqueadas:

| Tarea | Modelo | Findings (código → cláusula que decide) |
|---|---|---|
| task-cc30-limpieza-previa-... | TaskRefactorDoc | `rule-activation-task-code` → `R(preflight)`; `rule-activation-task-refactor` → `R(goldens)` |
| task-cc32-gates-de-activación-... | TaskCodeDoc | `rule-activation-task-code` → `R(preflight)` |
| task-cc35a-transacción-... | TaskCodeDoc | `rule-activation-task-code` → `R(preflight)` |
| task-cc36-plantillas-del-desk-... | TaskRefactorDoc | `rule-activation-task-code` → `R(preflight)`; `rule-activation-task-refactor` → `R(goldens)` |
| task-cc38-invariantes-de-documento-... | TaskRefactorDoc | `rule-activation-task-code` → `R(preflight)`; `rule-activation-task-refactor` → `R(goldens)` |

En todas el testigo es la review existente con `{"anchor_state":"lost"}`: los recibos que hoy hay en `desk/reviews/`
(preflight y bundle, varios `accepted`) no están pinneados (ver §CC35a). Es decir, ninguna tarea del desk de deskops se
activa con `deskops advance` hasta que sus recibos se reescriban por una vía que pinnee.

## CC35a prerrequisito operativo (d2)

Evidencia (sandbox `/mnt/ssd/proyectos/SLDB_1/.tmp-cc32-exp`, scripts `scratchpad/exp1.py`, `exp2.py`, `exp3.py`;
y la copia del desk de deskops, §a10):

1. **Vía de escritura de deskops en main** (`doc_io.DocTransaction.write`: `render_model_markdown` + `track_document_file`,
   sin `save_document_payload`). `ReviewService._write_review(kind=preflight|bundle, subject="doc:TaskCodeDoc:task-exp-alpha", verdict=pending)` y luego
   `ReviewService.dispose(..., "accepted", "ok")` dejan `subject: doc:TaskCodeDoc:task-exp-alpha` **sin `@sha256:`**.
   `edges_blocked(..., document="TaskCodeDoc:task-exp-alpha")` sigue devolviendo la arista con
   `any(^subject: ...) (seen: {}) (witness: ReviewDoc:review-task-exp-alpha-bundle-1 {"kind":"bundle"})`; `anchor_state` del
   recibo es `lost` (anchoring.md: ancla sin hash = `lost`). En el desk real, todos los recibos existentes dan
   `{"anchor_state":"lost"}` (§a10).
2. **`sldb.api.transaction.update`** sobre esos mismos recibos (sin cambiar el payload) los pinnea:
   `subject: doc:TaskCodeDoc:task-exp-alpha@sha256:0133c90e...` → `edges_holding` devuelve la arista (`holding=1 blocked=0`).
3. **`deskops edit task task-exp-alpha goal "new goal"`** → `holding=0 blocked=1`, testigo `{"anchor_state":"changed"}`.

Conclusión: la regla es correcta y sldb calcula el estado como GO07 lo fija; lo que falta en main es que la escritura de
`deskops review` / `review dispose` pase por `save_document_payload`, que es exactamente lo que CC35a hace (toda
escritura por `sldb.api.transaction`). Por a1 este nodo no toca `doc_io.py` ni la capa de escritura de `doc_access`;
los tests escriben recibos con `sldb.api.transaction` (b8, `tests/activation_receipts.py`: `create` + `update`, porque
`create_document` no pinnea y la siguiente escritura sí). Hasta que CC35a esté integrado, un desk con las reglas
instaladas no activa ninguna tarea con recibos escritos por `deskops review`: CC35a es prerrequisito operativo de CC32.

## a11 — texto propuesto de la nota a sldb (no enviada)

```
deskops message send --to sldb --kind notice --title "G_CONSUMER: deskops consume RuleDoc on_transition + anchors (CC32, <hash>)" --body "..."
```

Cuerpo propuesto:

> **G_CONSUMER cumplido por deskops** (plan deskops-como-config, nodo CC32, commit integrado `<hash>`).
> deskops ya consume el grafo operable de sldb tal como GO06/GO07/GO08/GO09 lo entregan:
> - Siete `RuleDoc` `on_transition` (una por tipo de tarea de fábrica, subject `model <= <TaskXDoc>`, where
>   `current_node = "ritual-execution"`) viven en `desk/lifecycle/rule-activation-*.md` de cada desk, sembradas por
>   `deskops desk update --apply` y registradas con `sldb.api.add_model("sldb.models.rule_doc:RuleDoc")`.
> - Las condiciones usan `any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")` sobre
>   `ReviewDoc.__doc_anchors__ = ["subject"]` y `all(depends_on: status = "closed")`.
> - `deskops advance` llama `edges_holding(store, "RitualDoc:ritual-execution", payload, include_linked=False, document="<Model>:<task>")`
>   y, bloqueado, `edges_blocked(...)`; imprime `Finding.level/code/subject/what` tal cual (mensaje | cláusula (seen) (witness)).
>   `show`/`next` usan `transition_findings`.
> - Test de integración en tres pasos: sin recibos falla nombrando la cláusula; con recibos pinneados activa; `goal` editado
>   bloquea con `{"anchor_state":"changed"}` (`tests/test_activation_rules.py`).
>
> Observaciones para sldb (hipótesis, no bloqueantes):
> 1. **Testigo de un `any` falso** = primer elemento alcanzado. Para que el finding muestre `anchor_state = changed` hubo que
>    poner `anchor_state` como primera hoja de la conjunción interna; con `kind` primero el testigo era la review de otro
>    kind y `seen` era `{"kind":"bundle"}`. Sería más útil que el testigo de un `any` falso fuese el elemento que llega más
>    lejos en la conjunción (o que `seen` incluyera todas las hojas evaluadas del testigo).
> 2. **`create_document` no pinnea anclas** (anchoring.md): un recibo creado y nunca reescrito queda `lost` aunque su
>    destino exista. deskops lo resuelve con `create` + `update` en la misma transacción; convendría que `create` pinnee o
>    que exista una operación `pin`.
> 3. **`sldb anchors check` sobre un índice anterior a GO07** devuelve `doc_anchors: []` (desk de deskops tal como está en main),
>    mientras el lenguaje ya lee esos `subject` sin hash como `lost`; tras `deskops desk update --apply` (reindexado) `deskops doctor`
>    reporta 16 alertas `lost` en deskops y 21 en sldb. Conviene que `anchors check` avise cuando el índice no trae estados de ancla
>    (o que los calcule al vuelo), para que las dos lecturas coincidan.
> 4. **`sldb stores check` tarda ~28 s** en un store recién creado por `deskops init` (medido en el sandbox); `deskops desk update`
>    lo ejecuta en cada corrida, por eso tarda minutos.
> 5. **`rule_graph` cuesta ~3,2 s** por llamada (store de ~30 documentos): `edges_holding(document=...)` y `transition_findings`
>    lo construyen cada vez; `deskops view board` lo amortiza con un snapshot propio. Un caché por proceso o por
>    `store_fingerprint` en sldb evitaría que cada consumidor lo reinvente.
> 6. **`children`** no existe como campo de TaskDoc: la cláusula `all(children: status = "closed")` de task.aggregate queda
>    pendiente de que exista el campo (hipótesis en deskops, no pide nada a sldb).

## a12 — rituales

Ningún ritual de `desk/` nombra `deskops advance` ni los recibos como gate ejecutado por sldb; `desk/rituals/execution.md`
describe el gate de inicialización (preflight, cold-bundle) como disciplina del coordinador. Para que el ritual nombre el
comportamiento nuevo, el coordinador puede agregar un paso con `deskops edit ritual` sobre el desk (no sobre este
worktree). Propuesta: insertar, antes de «Implement only the changes required for the active task.», el paso

> 1. Activate the task with `deskops advance task <id>`: the type's activation RuleDoc (`desk/lifecycle/rule-activation-<type>.md`) requires its review receipts `accepted` and `intact` and its dependencies closed; a blocked advance, `deskops show task <id>` and `deskops next <id>` name the clause that fails.

Comando exacto (la lista completa de `steps` actual más el paso nuevo en la posición 14):

```
deskops edit ritual ritual-execution steps '["1. Confirm the current phase is explicit and that this task belongs to the ready dependency layer being executed.", "1. Open the initialization gate by making the active task, task scope, touched files, and validation targets explicit.", "1. Atomize the work into one coherent deliverable.", "1. Audit code, docs, tests, and git state before changing anything.", "1. Run cheap TaskDoc-only preflight under [ritual-context-review](context-review.md) in a fresh ephemeral no-tools process: restate objective, list ambiguities and give a detailed non-executing dry-run.", "1. Store that TaskDoc-only reformulation at `runs/subagents/<run-dir>/preflight.md`.", "1. Pass the preflight only when the reformulation reproduces the task intent closely enough to execute without guesswork; if the subagent reports any ambiguity or misses the intended work, fix the TaskDoc before dispatching any Executor.", "1. Run a separate cheap cold-bundle coverage review under [ritual-context-review](context-review.md): explicitly supply task, routed instructions/rituals, bound pills, linked atoms/files and validation. Require reformulation, ambiguities and detailed dry-run; no commands or source edits.", "1. The coordinator compares both outputs with owner intent. Fix the written brief, split oversized nodes and retry changed input in a new isolated process. Resolve cold-review findings before implementation; unresolved ambiguity blocks dispatch.", "1. Sweep the board-routed pills and any task-local pills against the task scope, touched files, implementation path, and planned validation.", "1. Bind every pill whose `when`, `where`, or `how_not` matches a plausible part of the task.", "1. If a risky ambiguity is still uncovered, create or update a pill before implementation instead of proceeding on implicit assumptions.", "1. Do not start implementation until the initialization gate confirms atomization, preflight comprehension, cold review, and pill coverage.", "1. Activate the task with `deskops advance task <id>`: the type activation RuleDoc (`desk/lifecycle/rule-activation-<type>.md`) requires its review receipts accepted and intact and its dependencies closed; a blocked advance, `deskops show task <id>` and `deskops next <id>` name the clause that fails.", "1. Implement only the changes required for the active task.", "1. Keep scope tight and avoid unrelated fixes.", "1. Prepare validation before calling the work complete.", "1. Exit execution only by opening a handoff to testing that names the intended contract, relevant tests, and pill guardrails that must be proven."]' --root .
```

Y, opcionalmente, en `validation`: `deskops edit ritual ritual-execution validation '[... lista actual ..., "`deskops advance task <id>` activated the task: its receipts were accepted and intact and its dependencies closed."]' --root .`

## Hipótesis para sldb

- **H-CC32-1 (testigo)**: ver nota a sldb, punto 1. Mientras tanto la conjunción interna lleva `anchor_state` primero.
- **H-CC32-2 (`create` no pinnea)**: ver punto 2. Afecta a cualquier productor de recibos que use `create_document` una sola vez.
- **H-CC32-3 (`anchors check` e índice anterior a GO07)**: ver punto 3 de la nota; mientras el store no se reindexa, `anchors check`
  calla y el lenguaje ya bloquea.
- **H-CC32-4 (children)**: `all(children: status = "closed")` para task.aggregate no se escribe porque `children` no es campo de
  `TaskDoc` (GC09 pendiente); cuando exista, la regla de task.aggregate suma esa cláusula (una línea en
  `deskops/data/rules/rule-activation-task-aggregate.md`).
- **H-CC32-6 (costo de `rule_graph`)**: `sldb.api.transition_findings` y `edges_holding(document=...)` construyen `rule_graph(store)`
  en cada llamada (~3,2 s en un store de ~30 documentos; `edges_from` tarda 0,04 s). deskops lo amortiza en su `ReadSnapshot`;
  sldb podría cachear el `RuleGraph` por proceso (o por `store_fingerprint`) y ofrecer `transition_findings(..., graph=)`.
- **H-CC32-5 (dependencia cerrada)**: una dependencia cerrada ya no existe como documento (DC6) y sldb la omite del conjunto
  de `all(depends_on: ...)`; verificado indirectamente (`all` sobre vacío es `true`: task.aggregate sin `depends_on` activa).

## Desvíos y notas

- **`deskops/cli/commands/operations.py`** tocado con autorización del coordinador (d1): `_format_task_detail` imprime
  `  blocked by: <finding>` bajo cada gate y `_print_next_action_report` imprime `Blocked by:`; más el import de
  `finding_line`. Nada más de ese archivo cambió.
- **`cli/commands/desk.py`**: una línea (`lifecycle.ensure_rule_model(root)` antes de `apply_desk_includes`): sin ella,
  `desk update --apply` en un desk sin `RuleDoc` registrado no puede trackear las reglas (b7 preveía tocarlo solo por la
  salida; la salida ya la dan las líneas `Lifecycle graph: tracked ...`). `deskops init` lo cubre `write_lifecycle_graph`.
- **`tests/test_lifecycle_graph.py::test_write_lifecycle_graph_is_idempotent`**: la expectativa del árbol de
  `desk/lifecycle/` ahora incluye `deskops/data/rules/*.md` (la aceptación siembra las reglas ahí). La aserción
  `write_lifecycle_graph(...) == []` no cambió.
- **`tests/fixtures/golden/scaffold/`** (`init.json`, `update.json`): regenerados con `--update-golden` (corrida previa roja en
  `cc32/test_scaffold_golden_before.log`, 2 failed). El diff contra la base es solo la suma de las siete reglas: 7 entradas
  `desk/lifecycle/rule-activation-task-*.md` en `init.json`, y en `update.json` las mismas 7 entradas del árbol más 14 líneas
  del informe (`Lifecycle graph: wrote ...` y `Lifecycle graph: tracked ...` por regla). Nada más cambió (28 líneas añadidas, 0 quitadas).
- **Goldens de salida y de ayuda**: idénticos. `test_output_goldens.py` (que incluye `test_help_goldens` y
  `test_command_output_goldens`) pasa sin `--update-golden` (7 passed); `show_task.text/json` no cambian porque el desk de los
  goldens no tiene grafo (sus `lifecycle_gates` son `[]`) y la sección de findings solo aparece cuando hay findings.
- **Shape de `lifecycle_gates`**: cada gate suma la clave `findings` solo cuando hay findings; sin reglas aplicables (ritual-testing,
  ritual-closeout) el dict es el de antes, así `test_show_task_reports_the_gates_leaving_the_current_node` y
  `show_task.json` no cambian. El informe de `next` lleva siempre `findings` (lista, vacía si no hay); `next` no tiene JSON.
- **Tarea no trackeada**: `lifecycle.task_document` devuelve None y no corre ninguna regla (comportamiento de hoy), lo que
  mantiene `test_promotion_nesting` (tarea escrita a mano, sin store).
- **`models/task.py`** no se tocó; la descripción de `status` («typically active or blocked») sigue vieja: seguimiento (a7).
- **`tests/test_review_doc.py::test_sldb_edges_show_links_the_review_to_the_task_by_subject`** está `xfail(strict=True)`
  por GO07: sigue `xfailed` (13 passed, 1 xfailed): `sldb edges show` todavía no lista la arista `subject`
  review→tarea como ese test la espera. Preexistente en main; no lo toqué (el test no es de este nodo).
- **Rendimiento** (`scratchpad/view_time.py`, sandbox de 1 tarea): `show_task` pasó de 0,04 s a 3,4 s porque
  `sldb.api.transition_findings` carga el grafo de reglas entero (`rule_graph`: 3,2 s) en cada llamada. Dentro de un
  `read_snapshot` (lo que usa `deskops view board`) `lifecycle.transition_findings` carga el grafo una vez y lo comparte:
  4 `show_task` pasan de 37 s a 4,1 s y `DeskView.board` con 4 tareas tarda 4,1 s (medido con el doctor de 6 desks corriendo
  en paralelo). Un `show`/`next`/`advance` suelto sigue pagando una carga (~3 s); es costo de sldb (hipótesis H-CC32-6).
- **`tests/test_cli_help_examples.py`**: el flujo típico de `deskops --help` termina en `deskops advance task task-fix-thing`,
  que ahora bloquea sin recibos; el runner del test escribe los recibos (sldb.api) antes de cada ejemplo `advance task`, con
  comentario. El texto de la ayuda no cambia (invariante 2: goldens de ayuda idénticos). Consecuencia para el dueño: el flujo
  impreso ya no corre tal cual sin `deskops review preflight/bundle` + `review dispose` (y sin CC35a ni siquiera así, §CC35a);
  actualizar el epílogo cambia 1 golden de ayuda, decisión fuera de este nodo.
- **`tests/test_operational.py::test_advance_task_exact_selector_wins_over_prefix`**: escribe los recibos de `task-foo` antes
  del `advance`; sus aserciones no cambian.
- **`tests/test_desk_sync.py`** (2 tests): la lista de includes esperada suma `RuleDoc: desk/lifecycle/rule-activation-*.md` y
  el filtro de pendientes sin store excluye también `RuleDoc`.
- Sandboxes usados: `/mnt/ssd/proyectos/SLDB_1/.tmp-cc32-{exp,smoke,deskcopy,view,time,doctor}`; borrados al terminar.

## wc -l antes → después

| Archivo | antes (3cd46be8) | después |
|---|---|---|
| `deskops/data/desk_declaration.yaml` | 178 | 206 |
| `deskops/models/task_types.py` | 182 | 168 |
| `deskops/models/review.py` | 145 | 145 |
| `deskops/lifecycle.py` | 267 | 371 |
| `deskops/services/tasks.py` | 338 | 354 |
| `deskops/cli/commands/desk.py` | 428 | 429 |
| `deskops/cli/commands/operations.py` | 328 | 335 |
| `docs/workflow-policy-reference.md` | 227 | 245 |
| `CHANGELOG.md` | 160 | 162 |
| `tests/test_task_types.py` | 371 | 363 |
| `tests/test_cli.py` | 3140 | 3145 |
| `tests/test_lifecycle_end_to_end.py` | 540 | 545 |
| `tests/test_lifecycle_graph.py` | 186 | 197 |
| `tests/test_operational.py` | 200 | 203 |
| `tests/test_desk_view.py` | 221 | 223 |
| `tests/test_doc_io.py` | 248 | 250 |
| `tests/test_desk_sync.py` | 276 | 279 |
| `tests/test_cli_help_examples.py` | 128 | 136 |
| `tests/activation_receipts.py` (nuevo) | 0 | 91 |
| `tests/test_activation_rules.py` (nuevo) | 0 | 295 |
| `runs/subagents/cc32-worker-report.md` (nuevo) | 0 | 280 |
| `deskops/data/rules/rule-activation-task-aggregate.md` (nuevo) | 0 | 10 |
| `deskops/data/rules/rule-activation-task-code.md` (nuevo) | 0 | 13 |
| `deskops/data/rules/rule-activation-task-debug.md` (nuevo) | 0 | 13 |
| `deskops/data/rules/rule-activation-task-decision.md` (nuevo) | 0 | 12 |
| `deskops/data/rules/rule-activation-task-docs.md` (nuevo) | 0 | 12 |
| `deskops/data/rules/rule-activation-task-external.md` (nuevo) | 0 | 12 |
| `deskops/data/rules/rule-activation-task-refactor.md` (nuevo) | 0 | 12 |

## Commits

- `2a53f07b` CC32: grafo de reglas cacheado en el ReadSnapshot; tests ajustados a las reglas sembradas
- `31caac72` CC32: test de activación (G_CONSUMER y por tipo), tabla de reglas en docs, CHANGELOG e informe
- `1bf958d7` CC32: gates de activación por tipo como RuleDoc semilla; advance/next/show muestran los findings
- (este informe: el commit que lo cierra, ver `git log wt/cc32`)
