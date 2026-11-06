# GC01, ronda 2 del worker (correcciones del coordinador)

Mismas reglas que en gates-por-tipo-GC01-worker-brief.md: no commit, no git add, no tocar sldb, no escribir en desk/ ni .sldb/, nada de deskops/sldb contra el desk del worktree.

## Ya corregido por el coordinador (no lo deshagas)
- deskops/operations.py `_declared_closeout_evidence`: busca primero el nombre tal cual en `registered_task_types()` y solo después `canonical_task_type_name`; antes, un tipo local (task.code.cli) cerraba con la evidencia de task.code aunque declarara más. tests/test_task_types.py::test_desk_update_apply_registers_a_local_type_and_add_task_uses_it lo prueba ahora (TaskCliDoc declara además `document`).

## Lo que tienes que corregir
1. Tu informe dice que los 2 fallos de tests/test_board_portable_references.py son previos. No es así: en main falla solo `test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions`; `test_local_graph_next_show_and_retirement_accept_portable_context` falla por GC01 (usa `--task-type docs`). Corrígelo a `task.docs`.
2. Quedan usos de los nombres legados de --task-type que GC01 rompe o deja describiendo una semántica que ya no existe. Actualízalos a los nombres de tipo (task.code, task.docs, task.external) y, donde la prosa explica la evidencia, a la semántica nueva (la evidencia la declara el tipo; --evidence solo agrega kinds a los del tipo; sin --task-type el default es task.code con aviso; un tipo no registrado falla). Cambios mínimos, sin reescribir secciones:
   - tests/e2e_agent/scenarios/stuck-task-gate.yaml, first-task-to-closeout.yaml, inbox-to-task.yaml
   - deskops/about.py (líneas 18-19 y lo que dependa)
   - README.md:171
   - docs/faq.md:127 y deskops/data/faq.md:127 (son espejo: deben quedar iguales; hay test de paridad si existe, búscalo)
   - docs/operator-manual.md (393, 398, 469, 537) y docs/quickstart.md (83, 91, 131)
   Busca además con `grep -rnE -- "--task-type ['\"]?(code|docs|spec|design|external|implementation|test)\b"` y `grep -rn "fills the task's closeout_evidence\|fills --evidence"` en tests/, deskops/, docs/, README.md por si queda alguno más, y corrígelo.
3. Corre de nuevo: tests/test_task_types.py, tests/test_board_portable_references.py (debe quedar solo el fallo previo), los tests que lean about.py, faq o README (búscalos con grep), tests/test_cli_help_examples.py, tests/test_output_goldens.py, y si existe un runner barato de los escenarios e2e que no llame a un modelo, valida al menos que los YAML siguen parseando.

## Informe
Agrega una sección "Ronda 2" al final de runs/subagents/gates-por-tipo-GC01-worker-report.md con archivos tocados, la lista de reemplazos y la línea final de pytest de cada corrida; y resúmelo en tu respuesta.
