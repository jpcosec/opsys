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
