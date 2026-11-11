# resby-worker: closeout resolved-by de una tarea que el modelo rechaza

TaskDoc: task-closeout-resolved-by-cierra-una-tarea-que-el-modelo-rechaza-leyendo-su-frontmatter-como-retire-y-sup (task.debug).
Base: main 60f1ec37. Rama wt/resby.

## Causa raíz (confirmada antes del arreglo)

`ClosureService.close_resolved_by` (deskops/services/closure.py) carga la tarea con el modelo,
sin respaldo: `payload = doc_access.read_doc(task_path, TaskDoc)`. Lo necesita para leer `files`
(compuerta de `--test`) y para escribir `status: resolved` con `doc_access.write_doc`. Una tarea
heredada que el validador de ciclo de vida de `TaskDoc` rechaza (p. ej. `status: draft` con
`history [task_activates, task_hands_to_closeout]`) hace que `read_doc` levante
`ValidationError`; la excepción no se captura en el servicio y el CLI la imprime como
`Validation error: ... lifecycle is inconsistent: status: 'draft' does not follow history
'task_hands_to_closeout'; expected 'ready_for_testing'` con rc 1.

`close_superseded` ya tiene la rama de respaldo (captura el fallo de `read_doc`, lee el
frontmatter, escribe status e history con `workspace.rewrite_task_fields`, que revalida con
`TaskDoc` y restaura si falla; con store rechaza antes si `_other_invalid_tasks` no está vacía).
`close_retired` lee siempre por frontmatter. `close_resolved_by` nunca recibió esa rama.

Confirmación: el test de reproducción del coordinador
(`test_repro_resolved_by_invalid.py`) sobre 60f1ec37 da rc 1 con ese mensaje
(log: `~/proyectos/SLDB_1/coord2-ccconfig/resby/repro-before.log`).

## Arreglo (r1-r3)

- `ClosureService._read_closing_task(task_path) -> (payload, model_reads)`: lee con `TaskDoc`; si el
  modelo rechaza la tarea, lee el frontmatter.
- `ClosureService._record_closing_status(..., verb, status, event)`: con el modelo, `write_doc`
  (restaura si falla). Sin el modelo: con store, `_other_invalid_tasks` (la tarea que se cierra
  no cuenta) → `_blocked_by_invalid_tasks(task_id, verb, blocking)` antes de escribir nada; si no,
  `workspace.rewrite_task_fields` con `status` e `history [..., event]` (revalida con `TaskDoc`
  y restaura byte a byte si falla).
- `close_superseded` usa ambos (sin cambio de comportamiento). `close_resolved_by` usa ambos:
  `files` del frontmatter alimenta la compuerta de `--test` (r2: compuertas de ref y test iguales,
  aplicadas antes de escribir), luego status `resolved` + evento `resolved-by` (disposición 1).
  El commit sale del mismo `_close` con los mismos trailers (Task-Id, Closeout-Mode: resolved-by,
  Closeout-Reason, Closeout-Ref por ref, Closeout-Test por test).
- `_blocked_by_invalid_tasks` (texto común de supersede, retire y resolved-by) suma
  `This is sldb H2 (note 3895e9f7): sldb re-extracts the whole model on every write.` y la vía
  manual (`... or decide each by hand, or close it with deskops closeout supersede or retire once
  it is the only invalid task; then <verb> again.`).
- `deskops/cli/commands/closeout.py` y `deskops/workspace.py`: sin cambios (no hizo falta).

## Casos probados

| Caso | Test | Resultado |
|---|---|---|
| Repro del coordinador (draft tras task_hands_to_closeout, sin store) | test_repro_resolved_by_invalid.py (copia temporal, no commiteada) | rc 1 en 60f1ec37 (`repro-before.log`), rc 0 con el arreglo (`repro-after.log`) |
| Inválida sin store vs válida: mismo asunto, trailers, archivos del commit (Board, tarea, index.jsonl), entrada de índice, status `resolved`, árbol limpio; history = la suya + `resolved-by` | test_closeout_resolved_by.py::test_resolved_by_closes_a_task_the_model_rejects_like_a_valid_one | pasa |
| Con store, una sola inválida: cierra, trailers, árbol limpio, `sldb stores check` rc 0 | test_legacy_task_states.py::test_resolved_by_closes_the_only_invalid_task_and_the_store_checks | pasa |
| Con store, dos inválidas: rc 1, `Cannot resolved-by <id> yet`, nombra la otra y no la propia, `sldb H2 (note 3895e9f7)`, vía manual, árbol y HEAD intactos | test_legacy_task_states.py::test_resolved_by_refuses_while_another_task_is_invalid_and_names_sldb_h2 | pasa |
| supersede/retire con store y otra inválida (texto común cambiado) | test_legacy_task_states.py (tests existentes, aserciones por subcadena) | pasan |
| Ruta válida de resolved-by y sus rechazos | test_closeout_resolved_by.py (19 existentes) | pasan |

## Aceptación línea por línea

- **Validation: test nuevo, resolved-by de una tarea que el modelo rechaza cierra con Closeout-Mode: resolved-by, sin store y con store (stores check rc 0)** — los dos tests de arriba; logs en `~/proyectos/SLDB_1/coord2-ccconfig/resby/suite/test_closeout_resolved_by.log` (20 passed) y `test_legacy_task_states.log` (35 passed).
- **Validation: test nuevo, con dos inválidas, rechazo limpio que nombra sldb H2, árbol intacto** — test_resolved_by_refuses_while_another_task_is_invalid_and_names_sldb_h2, en test_legacy_task_states.log.
- **Validation: test_closeout, test_closeout_resolved_by, test_legacy_task_states y goldens de salida verdes, de a uno** — desde la copia `/dev/shm/deskops-resby` (HEAD 093e849e), sin `--update-golden`: test_closeout 59 passed, test_closeout_resolved_by 20, test_legacy_task_states 35, test_closeout_gates 3, test_retire_cli 13, test_output_goldens 7, test_cli 101. A pedido del coordinador, además la suite completa de a un archivo: 97 archivos, todos rc 0, 969 passed y 1 xfailed (test_review_doc, ya existía). Resumen: `~/proyectos/SLDB_1/coord2-ccconfig/resby/suite/SUMMARY`.
- **Validation: 4 pasos del CI en clon limpio** — los corre el coordinador. Yo corrí `bash scripts/ci-knowledge-check.sh .`: rc 0 (`resby/ci-knowledge-check.log`); sus hallazgos de drift son de archivos del desk que no toqué y no hacen fallar el CI.
- **Done When: r1-r5 hechos** — r1-r3: ver Arreglo. r4: tests de arriba; golden de doctor (UNMIGRATABLE_SUGGESTION) sin cambio, porque el texto H2 no aparece en ningún golden (`grep` en tests/fixtures/golden): **ningún golden cambió**. r5: tests existentes verdes (arriba).
- **Done When: causa raíz escrita antes del arreglo** — commit 8309caf1, antes del arreglo e94a2f0b.
- **Done When: docs y CHANGELOG** — operator-manual (sección resolved-by: tarea que el modelo rechaza, H2 y vía manual), workflow-policy-reference (estados cerrados por closeout), CHANGELOG (### Fixed).

## Hipótesis para sldb

- Ninguna nueva. El caso con dos inválidas sigue dependiendo de H2 (nota 3895e9f7): cualquier
  escritura re-extrae el modelo entero y cae en la otra tarea inválida.

## Desvíos

- **El mensaje está en inglés.** La disposición pide sumar el texto 'sldb H2 (nota 3895e9f7): sldb re-extrae el modelo entero en cada escritura'. La salida del CLI está en inglés, así que va traducido: `sldb H2 (note 3895e9f7): sldb re-extracts the whole model on every write`.
- **Verbo en el rechazo.** Con resolved-by, el rechazo dice `Cannot resolved-by <id> yet`, porque usa el verbo de la disposición: `_blocked_by_invalid_tasks(task_id, 'resolved-by', ...)`.
- **sldb hermano viejo en el worktree.** `test_legacy_task_states.py` (y otros) meten `../sldb/src` en `sys.path[0]`. Desde el worktree en el SSD ese hermano es `/mnt/ssd/proyectos/SLDB_1/sldb`, que está en 1d475bcd y no tiene `sldb.api.edges.referrers` (GD22). Por eso el test con store daba rc 3 (`ModuleNotFoundError`) al correr desde el worktree. Desde la copia en /dev/shm no hay hermano y manda `/dev/shm/sldb-main`, así que pasa. No lo toqué: es del entorno, pero puede morder a otros workers.
- **Atoms.** AGENTS.md pide capturar en atoms una regla nueva antes de cambiar los docs. El brief prohíbe tocar `desk/`, así que la regla de resolved-by sobre tareas inválidas queda en los docs sin atom. Si hace falta, que la capture el coordinador.
- **Esperas.** Mi primera tanda usaba la guarda global de pytest del brief y quedó parada unas 2 h por pytest ajenos. A pedido del coordinador la corté y relancé en serie, sin espera global.
