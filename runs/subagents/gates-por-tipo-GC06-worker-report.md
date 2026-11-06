# Informe del worker GC06 (gates-por-tipo)

Worktree: `/home/robocop/proyectos/SLDB_1/deskops-wt-gates` (rama `wt/gates-por-tipo`).
Sin commit, sin `git add`, sin tocar `sldb/`, sin escrituras a mano en `desk/` ni `.sldb/`.

## 1. Archivos cambiados/creados

Modificados:

- `deskops/cli/registry.py` — se retira el argumento `--to` de `advance task` (y su ayuda).
- `deskops/services/tasks.py` — `advance_task(task_id)` deja de aceptar `target_node` y se elimina la rama de transición forzada.
- `deskops/operations.py` — `_TASK_OWNED_FIELDS` y rechazo en `edit_artifact_field` para `status`, `current_node`, `history`, `task_type`, `closeout_evidence`; `advance_task` sin `target_node`.
- `deskops/cli/commands/operations.py` — `advance` llama `operations.advance_task(args.task_id)`.
- `docs/operator-manual.md` — el párrafo de `--to` se reemplaza por la regla sin escape (advance bloqueado + closeout commit/supersede/retire).
- `CHANGELOG.md` — dos entradas **breaking** en `[Unreleased] / Changed`.
- `tests/fixtures/golden/help/deskops_advance_task.txt` — golden regenerado con `--update-golden`.
- `tests/test_inbox_promote_cli_gaps.py` — se eliminan los tests de `advance_task(..., target_node=...)`, ya obsoletos al retirar la opción (y el import que quedaba sin uso).

Creados:

- `tests/test_cli_escape_hatches.py` — tests nuevos de las vías de escape cerradas.
- `runs/subagents/gates-por-tipo-GC06-worker-report.md` — este informe.

No se tocaron `desk/`, `.sldb/`, `sldb/`, `docs/faq.md` ni `deskops/data/faq.md` (no contenían usos de `advance --to`; el espejo FAQ sigue idéntico: `diff -q` sin diferencias).

## 2. Done When → test

| Condición de Done When | Test | Resultado |
|---|---|---|
| `deskops advance task-x --to ritual-testing` falla con error de uso (exit 2) | `tests/test_cli_escape_hatches.py::test_advance_to_is_a_usage_error` | Pasa |
| El help de `advance` no menciona `--to` | `tests/test_cli_escape_hatches.py::test_advance_help_does_not_mention_to` y `tests/test_output_goldens.py::test_help_goldens` | Pasa |
| `edit task ... status closed` falla con exit 1 y el mensaje nombra `closeout commit` | `tests/test_cli_escape_hatches.py::test_edit_task_refuses_lifecycle_fields[status-closed-...]`, `::test_edit_task_status_names_closeout_commit` | Pasa |
| Lo mismo para `current_node` | `tests/test_cli_escape_hatches.py::test_edit_task_refuses_lifecycle_fields[current_node-...]` | Pasa |
| Lo mismo para `task_type` | `tests/test_cli_escape_hatches.py::test_edit_task_refuses_lifecycle_fields[task_type-...]` | Pasa |
| Lo mismo para `closeout_evidence` | `tests/test_cli_escape_hatches.py::test_edit_task_refuses_lifecycle_fields[closeout_evidence-...]` | Pasa |
| Lo mismo para `history` | `tests/test_cli_escape_hatches.py::test_edit_task_refuses_lifecycle_fields[history-...]` | Pasa |
| `edit task task-x goal "..."` sigue funcionando | `tests/test_cli_escape_hatches.py::test_edit_task_keeps_ordinary_fields_editable` | Pasa |
| El golden del help se actualiza | `tests/test_output_goldens.py::test_help_goldens` (regenerado con `--update-golden`) | Pasa |
| `tests/test_cli.py` y `tests/test_cli_help_examples.py` pasan | `tests/test_cli.py`; `tests/test_cli_help_examples.py` | Pasa |
| CHANGELOG con entrada breaking | Revisión manual: dos entradas en `[Unreleased] / Changed` | Cumple (sin test automático) |
| `docs/operator-manual.md` sin `--to` (de advance) | `tests/test_operator_manual.py` ejecuta los bloques runnable | Pasa; queda solo el `--to` de `message send`, que es otra opción |

Mensajes exactos implementados (precisión 1), con `Error: ` que añade la CLI y exit 1:

- `status` → `deskops advance (transition effects) and deskops closeout commit`
- `current_node` → `deskops advance`
- `history` → `deskops advance and deskops closeout (append-only)`
- `task_type` → `deskops add task --task-type (create a new task to change the type)`
- `closeout_evidence` → `the task type, and deskops add task --evidence at creation`

## 3. Última línea de pytest de cada corrida

- `tests/test_cli_escape_hatches.py tests/test_inbox_promote_cli_gaps.py`: `29 passed, 1 warning in 70.22s (0:01:10)`
- `tests/test_output_goldens.py::test_help_goldens --update-golden`: `1 passed, 1 warning in 173.42s (0:02:53)`
- `tests/test_cli.py`: `101 passed, 1 warning in 528.44s (0:08:48)`
- `tests/test_cli_help_examples.py tests/test_lifecycle_graph.py tests/test_packaging.py tests/test_task_types.py tests/test_review_doc.py tests/test_inbox_promote_cli_gaps.py tests/test_cli_escape_hatches.py`: `88 passed, 1 xfailed, 1 warning in 603.98s (0:10:03)`
- `tests/test_lifecycle_end_to_end.py`: `5 passed, 1 warning in 360.83s (0:06:00)`
- `tests/test_operator_manual.py`: `1 passed, 1 warning in 235.71s (0:03:55)`
- `tests/test_output_goldens.py` (suite completa del archivo): `7 passed, 1 warning in 280.54s (0:04:40)`
- `tests/e2e_agent/test_agent_scenarios.py -k "reference_solutions or checks_need_the_work"`: `6 passed, 3 deselected, 1 warning in 327.15s (0:05:27)`
- `tests/test_desk_replace.py` (encontrado por grep de "edit task"): `7 passed, 1 warning in 173.93s (0:02:53)`

Nota: un primer intento de correr en un solo comando `test_cli.py + test_cli_help_examples.py + lifecycle_end_to_end + lifecycle_graph + operator_manual + packaging + task_types + review_doc + inbox + escape` agotó el timeout del wrapper a 1800 s (no fue un fallo de pytest); se repitió dividido en las corridas de arriba. No se corrió la suite completa, según el encargo. El fallo conocido de main (`tests/test_board_portable_references.py::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions`) no se tocó ni se ejecutó.

## 4. Usos de `advance --to` reemplazados

- `docs/operator-manual.md:436-438` (párrafo `--to <node>` como override manual) → reemplazado por la regla sin escape: la transición solo dispara con su condición; tarea bloqueada se queda donde está y `advance` nombra el gate; cierre con `deskops closeout commit`, `closeout supersede` o `closeout retire`. Motivo: `--to` ya no existe.
- `tests/fixtures/golden/help/deskops_advance_task.txt:1,11-14` → golden regenerado por pytest (`--update-golden`), ya sin la línea de usage ni la opción. Motivo: el help cambió.
- `tests/test_inbox_promote_cli_gaps.py:163-231` (pruebas de `advance_task(..., target_node=...)`) → eliminadas y sustituidas por `tests/test_cli_escape_hatches.py`, que verifica la ausencia de la opción y el rechazo de campos. Motivo: la API forzada ya no existe.
- No había `advance --to` en `docs/faq.md`, `deskops/data/faq.md`, `README.md`, `deskops/about.py`, help/epílogos restantes, `.opencode/`, `.pi/skills/` ni `tests/e2e_agent/scenarios/` (grep sin resultados). Los `--to` que quedan en esos archivos son de `deskops message send --to <repo>`.
- `desk/drawer/plans/gates-por-tipo/{brief,dag,decisiones,alcance}.md`, `desk/drawer/plans/workspace-documental/**` y artefactos históricos bajo `runs/` mencionan `--to`, pero son datos de plan/evidencia, no superficies documentales activas; no se tocaron (regla: no escribir a mano en `desk/`).
- `docs/diagrams/process/current-agent-workflow-and-automation.{md,mmd}` dice que “a forced transition to the terminal node is refused”; no usa `--to` y es una proyección generada de Spec2viz, así que no se editó a mano. Queda como posible ajuste de GC08/spec2viz.

## 5. Lo que no hice y por qué

- **No hice el ack de la nota 20261029-213633** (precisión 4): es escritura en `desk/` y lo hace el coordinador con el CLI en main.
- **No toqué `desk/`** (rituales, board, inbox, plan): GC08 actualiza rituales; el ack es del coordinador.
- **No toqué `sldb/`**, no ejecuté `deskops` contra el desk real del worktree y no usé `desk/` para pruebas.
- **No agregué ninguna bandera de escape** (`--force` o equivalente), conforme D2.
- **No corrí la suite completa** (`pytest tests`), solo las corridas enumeradas.
- **No hice commit, push ni `git add`.**
- **No edité los diagramas generados ni los planes del drawer** que mencionan `--to`; se justifica en la sección 4.
