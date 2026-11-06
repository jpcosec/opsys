# Estado del coordinador 2: plan gates-por-tipo (deskops)

Coordinador: robocop2-coordinator2 (robocop2). Serie: GC01 → GC02 → GC06 → GC03, en un solo worktree `deskops-wt-gates`, rama `wt/gates-por-tipo`. Nada se pushea a main salvo los commits de desk (TaskDoc, preflight, disposición) que hace el ciclo.

## GC01: Tipos de tarea como modelos con jerarquía y evidencia de cierre declarada en el tipo

Estado: **implementado y verificado en la rama; pendiente de closeout (supervisor)**.

### Commits
- main de deskops (desk):
  - `fd1dd11a`: promoción (`deskops add task --task-type code`, files con `deskops edit task`).
  - `13b73ff6`: preflight TaskDoc-only (attempt-1, technical_ok) y su disposición como precisiones (1)-(7) del scope con `deskops edit task`. Incluye `dag.yaml` rev 2: `gates.G_TYPES.evidence` decía que `model <= TaskCodeDoc` incluye `task.debug`, contra brief.md §Tipos y GC01; corregido a "y no a task.debug".
  - `918ae111`: `files` de GC01 ampliado con los archivos que la ejecución necesitó (ver Desvíos).
- rama `wt/gates-por-tipo`: `d0e7bb05` GC01 (código, tests, docs, `.sldb/core/models/Task*Doc.yaml`, informe del worker).

### Disposición del preflight (resumen; el detalle está en el scope del TaskDoc)
1. Tabla de tipos copiada al TaskDoc. 2. `__contract__` inerte hasta que sldb lea GO02 (e). 3. `children`/`goldens` declarados; el cierre falla nombrándolos como aún no verificables. 4. Migración: `task.*` se conserva; valor desconocido → `task.code` con reporte; `closeout_evidence` existente se conserva. 5. `--evidence` como piso. 6. `closeout_evidence` no vacío reemplaza la evidencia del tipo; `add task` lo escribe solo si `--evidence` agrega. 7. G_TYPES se satisface al cerrar GC01.

### Aceptación, línea por línea
| Línea de Done When | Evidencia |
|---|---|
| `add task --task-type task.code` crea `TaskCodeDoc:<id>` con `task_type task.code` | `tests/test_task_types.py::test_add_task_with_task_type_tracks_under_the_type_model` ✔ |
| `--task-type foo` falla nombrando los tipos registrados | `::test_add_task_with_an_unregistered_type_lists_the_types` ✔ |
| sin `--task-type` → `task.code` con aviso | `::test_add_task_without_task_type_defaults_to_code_with_a_note` ✔ |
| `desk/models/local_types.py` con `TaskCliDoc(TaskCodeDoc)` se registra con `desk update --apply` y `add task --task-type task.code.cli` funciona | `::test_desk_update_apply_registers_a_local_type_and_add_task_uses_it` ✔ (extendido por el coordinador: el cierre usa la evidencia del subtipo local) |
| `model <= TaskCodeDoc` devuelve task.code y task.refactor, no task.docs ni task.debug | `::test_model_family_query_includes_refactor_and_not_debug_or_docs` ✔ |
| `closeout verify` de `task.docs` exige commit y document sin `closeout_evidence` | `::test_closeout_verify_reads_evidence_from_the_type` ✔ |
| `--evidence` que quite un kind falla y uno que agregue se guarda | `::test_add_task_evidence_can_add_but_not_remove_a_type_kind` ✔ |
| legado `implementation` → `task.code` con `desk update --apply`, segunda corrida sin cambios | `::test_legacy_task_type_migrates_idempotently` ✔ |
| grep `TASK_TYPE_EVIDENCE` en deskops/ vacío | grep exit 1 (coordinador) y `::test_task_type_evidence_mapping_is_gone` ✔ |
| `model_contract_hashes.json` actualizado | `tests/test_model_contract_snapshot.py` ✔ |
| CHANGELOG y `docs/workflow-policy-reference.md` con la tabla de tipos | diff de `d0e7bb05` |

### Tests (corridos por el coordinador en el worktree)
- `tests/test_task_types.py`: `15 passed` (con la corrección del coordinador).
- `test_board_portable_references, test_closeout_declared_evidence, test_cli_help_examples, test_output_goldens, test_federated_models, test_model_contract_snapshot, test_operator_manual, test_packaging`: `1 failed, 48 passed`. El fallo es `test_board_portable_references.py::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions`, **previo**: falla igual en main `fd1dd11a` sin GC01.
- Worker (informe en `runs/subagents/gates-por-tipo-GC01-worker-report.md`): closeout 49, closeout atomless/skills/templates 34, cli 112, lifecycle e2e + from_drawer 8, operational/desk_sync/federated 19, e2e_agent reference solutions 6: todos verdes.
- Suite completa: pendiente; se corre al cerrar la serie (GC03).

### Correcciones del coordinador sobre el trabajo del worker
1. `_declared_closeout_evidence` mapeaba cualquier tipo no de fábrica a `task.code`: un subtipo local que suma evidencia cerraba con la del ancestro. Ahora busca primero el nombre registrado.
2. El worker dio por previos los dos fallos de `test_board_portable_references.py`; uno lo causaba GC01 (`--task-type docs`). Ronda 2: corregido, y además todos los usos de `--task-type` legado en about, README, faq (y su espejo), operator-manual, quickstart, skills de .opencode/.pi, epílogos de closeout en registry y escenarios e2e.

### Desvíos (registrados en `files` del TaskDoc con `deskops edit task`)
- `.sldb/core/models/Task*Doc.yaml` y `store_index.yaml` del worktree: registro de los siete modelos con `sldb models add` (CLI; sin él `inherit_model` falla en desks nuevos).
- `deskops/cli/commands/desk.py` (handler de `desk update`).
- Docs, about y escenarios con `--task-type` legado (ver arriba). `deskops/bootstrap.py` no cambió (`MODEL_REFS` ya toma `deskops.models.__all__`).

### Hipótesis
- Verificada: sldb registra una subclase cuya base es un modelo federado y `base_models`/`model <= X` la resuelven por el MRO (evidencia en el informe del worker §4). Para tipos locales, `sldb find` necesita `--pythonpath <desk>`.

### Para el supervisor
- Merge de `wt/gates-por-tipo` a main y closeout de GC01 (`deskops closeout commit`); G_TYPES queda satisfecho con ese cierre.
- Conflicto previsible con `wt/deskops-ui` en `deskops/cli/registry.py` y en `tests/fixtures/golden/help/deskops.txt`.
- `desk/rituals/closeout.md` y otros rituales aún nombran el `--task-type` legado: es desk/ y se actualiza en GC08 con `deskops edit ritual`, como dicta la regla común 4.
- `deskops add task` avisó que faltan los archivos de dos notas del inbox que el índice nombra: `20261029-213633-unclear-advance-to-superseded…` (GC06 debía cerrarla con ack) y `20261104-222852-suggestion-closeout-las-pruebas…`.
- Fallo previo en main: `test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions`.
- Pendiente del dueño (decisiones.md): `--evidence` como piso quedó implementado como superconjunto de la evidencia del tipo.

## GC02: ReviewDoc como recibo anclado al contrato de la tarea

Estado: **implementado y verificado en la rama; pendiente de closeout (supervisor)**.

### Commits
- main (desk): `29fbf2b9` promoción; `fa4042d1` preflight (attempt-1, technical_ok, 6 ambigüedades) y disposición; `4e5f1a72` files de GC02 tras su ejecución y promoción de GC06 (suma `deskops/cli/commands/desk.py` a files).
- rama: `6284c43d` GC02.

### Disposición del preflight (detalle en el scope del TaskDoc)
1. **Cambio de aceptación**: el sldb actual no resuelve `doc:Model:name` en `__references__` (`sldb/store/edge_index/declared_references.py:84`, `is_export_id` lo lee como store `doc`). `subject` va solo en `__doc_anchors__`; "sldb edges show lo enlaza por subject" pasa a un test `xfail(strict=True, reason="G_SLDB_ANCHORS: sldb GO07")` que se vuelve rojo cuando GO07 dé la arista. Corregidos done_when y validation.
2. subject XOR subject_ref, con patrones. 3. `edit review` (sujeto nuevo `artifact.review`) rechaza verdict/reason/disposed_at/disposed_by. 4. El id es la autoridad; la ruta `desk/reviews/<task>/<kind>-<n>.md` se compone. 5. subject se valida solo por forma. 6. Tipos de fechas y `run_dir` como RunDoc.

### Aceptación
| Línea | Evidencia |
|---|---|
| ida y vuelta render/extract | `tests/test_review_doc.py::test_review_doc_roundtrips_a_payload` ✔ |
| kind fuera de vocabulario falla | `::test_review_kind_outside_the_closed_vocabulary_fails` ✔ |
| accepted sin reason falla | `::test_review_accepted_without_reason_fails` ✔ |
| subject `task-x` falla / `doc:TaskCodeDoc:task-x` valida | `::test_review_subject_without_the_doc_prefix_fails`, `::test_review_subject_with_doc_prefix_validates` ✔ |
| guardado con doc_io queda `ReviewDoc:<id>` | `::test_review_doc_is_tracked_as_review_doc_in_a_temporary_desk` ✔ |
| edges show por subject (xfail hasta GO07) | `::test_sldb_edges_show_links_the_review_to_the_task_by_subject` xfailed (con `--runxfail` falla en la arista ausente) |
| `edit review verdict` falla remitiendo a review dispose | `::test_edit_review_refuses_the_disposition_fields[*]` ✔ |
| hashes de contrato | `tests/test_model_contract_snapshot.py` ✔ |
| CHANGELOG | diff de `6284c43d` |

### Tests
- Coordinador: `test_review_doc, test_command_registry, test_model_contract_snapshot, test_cli_help_examples` → `29 passed, 1 xfailed`.
- Worker: test_cli 101 ✔, test_task_types 15 ✔, test_output_goldens 7 ✔, desk_sync/replace/extension/doctor* 42 ✔, packaging/doc_io 15 ✔ (informe `runs/subagents/gates-por-tipo-GC02-worker-report.md`).

### Notas
- Sin `add review` (GC03 escribe los recibos): el sujeto se marca `create: False`. `desk/reviews` no entra en `_MODELED_DESK_TOP_LEVEL_DIRS`: el tracking lo hará GC03 por id, no por nombre de archivo.
- Archivos fuera de files: `deskops/cli/commands/desk.py` (registrado luego en files), `tests/test_cli_help_examples.py` y `tests/test_command_registry.py` (bajo `tests/`).

## GC06: cierre de las vías de escape (advance --to y edit task sobre campos del ciclo de vida)

Estado: **implementado y verificado en la rama; pendiente de closeout (supervisor)**.

### Commits
- main (desk): `4e5f1a72` promoción; `427e33af` preflight (attempts 1-3 timeout por saturación de deepseek, no cuentan; attempt-4 technical_ok, 6 ambigüedades) y disposición.
- rama: `f612d762` GC06.

### Disposición del preflight (detalle en el scope del TaskDoc)
1. Mapeo campo→escritor y texto `Error: <campo> is not editable with edit task; it is written by <escritor>.` con exit 1. 2. `blocked` no gana camino nuevo en `advance`. 3. El resto de campos sigue editable. 4. El ack del inbox lo hace el coordinador con el CLI (no el worker). 5. `closeout commit`/`closeout supersede` ya existen. 6. `task_activates` sigue sin condición hasta GC05.

### Aceptación
| Línea | Evidencia |
|---|---|
| `advance task-x --to ritual-testing` → exit 2 | `tests/test_cli_escape_hatches.py::test_advance_to_is_a_usage_error` ✔ |
| help de advance sin `--to` | `::test_advance_help_does_not_mention_to`, golden `deskops_advance_task.txt` regenerado ✔ |
| `edit task status closed` exit 1 nombrando closeout commit | `::test_edit_task_refuses_lifecycle_fields[status…]`, `::test_edit_task_status_names_closeout_commit` ✔ |
| ídem current_node, task_type, closeout_evidence, history | `::test_edit_task_refuses_lifecycle_fields[*]` ✔ |
| `edit task goal` sigue funcionando | `::test_edit_task_keeps_ordinary_fields_editable` ✔ |
| test_cli y test_cli_help_examples | worker: 101 ✔; coordinador: help_examples ✔ |
| CHANGELOG breaking, operator-manual sin `advance --to` | diff de `f612d762`; grep de `advance … --to` en docs/README/deskops/skills vacío (coordinador) |
| ack de inbox 20261029-213633 | **no hecho**: `deskops message ack 20261029-213633-… --root .` en main responde `Unknown message`; el `.md` no existe y solo queda `.sldb/core/documents/InboxNoteDoc/20261029-213633-….yaml`. No se toca a mano: pasa al supervisor. |

### Tests
- Coordinador: `test_cli_escape_hatches, test_inbox_promote_cli_gaps, test_cli_help_examples, test_command_registry` → `43 passed`.
- Worker (informe `runs/subagents/gates-por-tipo-GC06-worker-report.md`): test_cli 101, goldens 7, lifecycle e2e 5, operator_manual 1, e2e_agent reference 6, desk_replace 7, conjunto help/lifecycle_graph/packaging/task_types/review_doc 88 + 1 xfailed: verdes.

### Notas
- `tests/test_inbox_promote_cli_gaps.py`: se borraron los tests de `advance_task(target_node=…)` (API retirada).
- `docs/diagrams/process/current-agent-workflow-and-automation.{md,mmd}` menciona "forced transition"; es proyección de Spec2viz, no se editó (posible ajuste en GC08).

## GC03: comando deskops review

Estado: **implementado, verificado e integrado en main (squash `9df4c82a`); pendiente de closeout**.

### Commits
- main (desk): `d5523aa1` promoción; `5de22525` preflight (attempt-1, technical_ok, 9 ambigüedades) y disposición, precisiones (1)-(13).
- rama: `e80fdef5` GC03 tras el rebase sobre `991709f6` (UI01). En el rebase, los conflictos de `.sldb/core/store_index.yaml` se resolvieron tomando main y regenerando con `sldb models add/update`; `deskops.txt` y `test_cli.py` tomaron main, se volvió a agregar `review` y los goldens se regeneraron.
- main: `9df4c82a`, squash de `wt/gates-por-tipo` (GC01+GC02+GC06+GC03). Conflictos con el perf del closeout (`4a9a4bbb`): en `operations.py` y CHANGELOG se conservan ambos lados; store_index regenerado por CLI.
- main (desk): `271d76c1` desk update --apply (5 tareas → task.code, perfil runtime-pi-deepseek-flash, desk/reviews, untrack de las notas 20261029-213633 y 20261104-222852 sin .md); `a1a938c4` drawer remove de los context_review.py de workspace-documental y gates-por-tipo.

### Aceptación
| Línea | Evidencia |
|---|---|
| preflight escribe attempt-1 con los cinco archivos y review-task-x-preflight-1 | `tests/test_review_command.py::test_preflight_writes_attempt_evidence_and_receipt` ✔ |
| segunda corrida sin cambios no llama al modelo; status reviewed | `::test_unchanged_second_run_is_reviewed_and_does_not_call_the_model` ✔ |
| editar goal → stale y nuevo sha | `::test_edited_goal_is_stale_and_next_run_uses_a_new_sha` ✔ |
| bundle con rituales del Board, pills y files en orden | `::test_bundle_includes_rituals_pills_and_files_in_order` ✔ |
| node sobre gates-por-tipo: ReviewDoc por nodo con subject_ref | `::test_node_writes_one_review_doc_per_node` ✔ |
| dispose y segunda dispose falla | `::test_dispose_writes_the_verdict_and_a_second_dispose_fails` ✔ |
| tercer intento a nivel de plan falla sin --force | `::test_third_good_attempt_on_the_same_key_fails_without_force` ✔ |
| pi con exit 1 → technical_ok false, incomplete | `::test_transport_failure_leaves_technical_failure_and_incomplete` ✔ |
| grep context_review.py en desk/drawer | retirados los de workspace-documental y gates-por-tipo (`a1a938c4`); queda `desk/drawer/plans/deskops-ui/context_review.py`, fuera de este encargo |
| CHANGELOG, operator-manual | squash `9df4c82a` |

### Tests (por archivo, con MemoryMax=2G y uno a la vez, por pedido del supervisor; la suite completa la corre él)
- Rama tras el rebase: review_command 12, review_doc 13+1 xfailed, contract_snapshot 2, task_types 15, cli_escape_hatches 9, command_registry 3, cli_help_examples 11, output_goldens 7, inbox_promote_cli_gaps 20, operator_manual 1, packaging 5, add_task_from_drawer 3, closeout_declared_evidence 19, desk_replace 7, lifecycle_end_to_end 5, operational 10, cli 101, e2e_agent scenarios 6 + 3 skipped: todos verdes. board_portable_references: 1 failed (la falla previa conocida de main), 1 passed.
- Squash en main antes del commit: contract_snapshot, command_registry, task_types, closeout_declared_evidence, closeout_gates 7, review_command, review_doc, cli_escape_hatches, output_goldens, cli_help_examples, desk_view 9+1 skipped: todos verdes.

### Pendiente
- Nota a sldb ("deskops review cubre grafo-operable/context_review.py"): `deskops message send --to sldb` falla porque `desk/registry/repo-sldb.md` apunta a `/home/jp/proyectos/SLDB_1/sldb`, y con `--root ../sldb` falla porque sldb no se registra a sí mismo en su registry. No se escribió nada en sldb.
- Closeout de GC01, GC02, GC06 y GC03 (supervisor).

## Plan congelado
Por decisión del dueño (`deskops-como-config-arbol.md`, T0.2), gates-por-tipo queda congelado tras GC03: no se promueven ni despachan más nodos GC. Lo que falta de tipos y compuertas se rehace como reglas declaradas en P3 (T3.2, T3.3).
