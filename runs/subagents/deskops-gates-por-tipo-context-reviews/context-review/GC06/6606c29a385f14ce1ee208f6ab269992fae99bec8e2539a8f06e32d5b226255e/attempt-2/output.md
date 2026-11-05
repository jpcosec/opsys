REFORMULACION
GC06 es un nodo `delivery` de deskops (padre PC02 agregado; `depends_on: GC01`). Propósito: cerrar las vías de escape del ciclo de vida retirando `advance --to` y haciendo que `edit task` rechace `status`, `current_node`, `task_type`, `closeout_evidence` e `history`. Resultado: CLI sin `--to`, error de dominio exit 1 para esos campos, help/golden y manual actualizados, CHANGELOG breaking y ack del inbox 20261029-213633; el resto de campos sigue editable. Límites: no toca sldb, no añade banderas de salto, no cambia la autoridad de `closeout commit`; los archivos son los del `output_scope`.

AMBIGUEDADES
1. “cada uso documentado se reemplaza” frente a `output_scope` limitado a “docs/operator-manual.md”: obliga a inventar si se editan quickstart/rituales u otros documentos fuera del alcance o se dejan usos sin reemplazar.
2. “con un error que dice quién escribe cada campo (advance y closeout; add task para task_type)” no asigna autor para `current_node`, `closeout_evidence` ni `history`; la aceptación solo precisa que `status` nombre `closeout commit` y añade “lo mismo para…”. Obliga a inventar el mensaje y el actor de esos campos.
3. “blocked → nada que escribir” y DC4 “blocked deja de ser un status guardado” no dicen qué hacer con tareas existentes en `status: blocked`; obliga a inventar migración, limpieza o dejarlas guardadas.
4. “cerrar → closeout commit; superseded → closeout supersede” no define existencia ni efecto de `closeout supersede`; el brief solo afirma que `closeout commit` es la única puerta de cierre. Si no existe, obliga a inventar el reemplazo.

DRY-RUN
Lecturas: `deskops/cli/registry.py`, `deskops/services/tasks.py` (179-192), `deskops/operations.py` (`edit_artifact_field`), `deskops/cli/commands/operations.py`, tests y goldens de help, `docs/operator-manual.md`, inbox citado. Cambios previstos: quitar `--to` y sus ramas; añadir guardas de campo con error de dominio exit 1; actualizar help/goldens, tests, CHANGELOG, manual y ack. Dependencia: GC01 cerrado; ninguna de sldb. Validaciones futuras: `pytest tests/test_cli.py tests/test_cli_help_examples.py`, help sin `--to`, manual sin `--to`, prueba manual de `edit task goal`.

FUTURO
GC05 aportará `edges_blocked` y la explicación de `blocked`; GC08 alineará rituales/quickstart; el dueño decide `--evidence`, DC7, `task.external` y Scion; un humano dispone la revisión. `G_CONSUMER` no corresponde a GC06.
