# Encargo del worker: GC06 del plan gates-por-tipo (deskops)

Eres un worker de implementación. No ves la conversación del coordinador: todo está aquí y en los archivos nombrados. Trabajas SOLO en el worktree `/home/robocop/proyectos/SLDB_1/deskops-wt-gates` (rama `wt/gates-por-tipo`), que ya contiene GC01 (tipos de tarea) y GC02 (ReviewDoc).

## Entorno
```
export PATH=$HOME/proyectos/SLDB_1/.venv/bin:$HOME/.local/node/current/bin:$HOME/.local/bin:$PATH
cd /home/robocop/proyectos/SLDB_1/deskops-wt-gates
PYTHONPATH=$PWD python -m pytest -q tests/<archivo>
```
El `deskops` del PATH es el checkout principal: en los tests usa el código del worktree (`python -m deskops` con PYTHONPATH, como los tests existentes).

## Lee primero (entero)
1. El TaskDoc (contrato), en el checkout principal: `/home/robocop/proyectos/SLDB_1/deskops/desk/tasks/task-gc06-cierre-de-las-vías-de-escape-advance-to-y-edit-task-sobre-campos-del-ciclo-de-vida.md`. Goal, Scope con las **Precisiones del preflight (1)-(6)** (mandan), Implementation Path, Validation, Done When.
2. Plan: `/home/robocop/proyectos/SLDB_1/deskops-wt-gates/desk/drawer/plans/gates-por-tipo/decisiones.md` (D2, DC4) y el nodo GC06 de `dag.yaml`.
3. Código: `deskops/cli/registry.py` (advance, edit task), `deskops/services/tasks.py` (advance_task, ~179-205), `deskops/operations.py` (edit_artifact_field; GC02 ya agregó ahí un rechazo de campos para `edit review`: sigue el mismo patrón), `deskops/cli/commands/operations.py`.

## Qué entregar
- `deskops advance` sin `--to`: usarla falla con error de uso de argparse (exit 2); el help de advance no la menciona.
- `edit task` rechaza status, current_node, task_type, closeout_evidence e history con exit 1 y el mensaje de la precisión (1); el resto de campos sigue editable (`edit task <t> goal "..."` funciona).
- Todo uso documentado de `advance --to` en docs/, README, help/epílogos, about, faq (`docs/faq.md` y su espejo `deskops/data/faq.md` deben quedar idénticos), skills de `.opencode/` y `.pi/`, y escenarios `tests/e2e_agent/scenarios/` se reemplaza por closeout commit / closeout supersede / nada (precisión 5). Busca con grep `--to` cerca de advance. No toques `desk/` (los rituales los actualiza GC08).
- Tests que usen `advance --to` o `edit task ... status|current_node|...` se adaptan; tests nuevos para cada línea de Done When.
- Goldens de help regenerados con el mecanismo del repo (`pytest tests/test_output_goldens.py::test_help_goldens --update-golden`), nunca a ojo.
- CHANGELOG con entrada **breaking**; `docs/operator-manual.md` sin `--to`.
- NO hagas el ack de la nota del inbox (precisión 4: lo hace el coordinador).

## Reglas (no negociables)
- No tocar sldb. No escribir a mano en `desk/` ni `.sldb/`; no correr deskops contra el desk del worktree.
- Ninguna bandera para saltar un gate (D2): no agregues `--force` ni equivalente.
- No commit, no push, no git add.
- Solo archivos de `files` del TaskDoc más los de docs/skills/escenarios que usen `--to`; justifica cualquier otro en el informe.
- No corras la suite completa. Corre tus tests y vecinos: tests/test_cli.py, tests/test_cli_help_examples.py, tests/test_output_goldens.py, tests/test_lifecycle_end_to_end.py, tests/test_lifecycle_graph.py, tests/test_operator_manual.py, tests/test_packaging.py, tests/test_task_types.py, tests/test_review_doc.py, tests/e2e_agent/test_agent_scenarios.py -k "reference_solutions or checks_need_the_work", y los que encuentres con grep de "--to" o "edit task".
- Fallo previo en main, no tuyo: tests/test_board_portable_references.py::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions. Cualquier otro fallo es tuyo hasta que pruebes lo contrario corriéndolo en `/home/robocop/proyectos/SLDB_1/deskops` (main).

## Informe final (en tu respuesta y en runs/subagents/gates-por-tipo-GC06-worker-report.md)
1. Archivos cambiados/creados. 2. Cada línea de Done When → test (archivo::nombre) y si pasa. 3. Línea final de pytest de cada corrida. 4. Lista de usos de `--to` reemplazados (archivo:línea → por qué). 5. Lo que no hiciste y por qué.
