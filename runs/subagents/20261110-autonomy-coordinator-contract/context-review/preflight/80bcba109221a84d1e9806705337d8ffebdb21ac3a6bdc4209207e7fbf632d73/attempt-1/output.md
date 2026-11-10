**REFORMULACION**

- **Resultado:** contrato fuente coherente para que Scion, sin prompts del padre, recupere el estado actual configurado, progrese trabajo autorizado rutinario, seleccione una hoja ready revisada y sin dueño, despache ejecutor y tester independiente, y reconcilie el cierre antes de continuar. Incluye RoleDoc corregido vía SLDB —permite mutaciones CLI modeladas, no implementación del supervisor—, `--context-file`, entorno/volumen, modo tester, identidad determinista, RunDoc de intención, reconciliación y límites de reintento.
- **Repo/superficie:** `deskops/runtime/scion.py`, `deskops/cli/registry.py`, `deskops/cli/commands/runtime.py`, `desk/roles/deskops-supervisor.md`, átomo de workflow, tests/goldens, `docs/operator-manual.md` y `CHANGELOG.md`.
- **Límites:** sin motor de ciclo de vida ni scheduler nuevo, sin decisiones automáticas de política, sin pi-subagents ni tareas CC no relacionadas; sin secretos en contexto; sin duplicar hijos; sin sobrescribir evidencia; sin attempt 3.

No apruebo: reformulo el contrato completo, no una parte.

**AMBIGUEDADES**

1. No se define `workspace_root`, pese a ser el límite de rutas y el volumen: “context keys project, workspace_root, desk_root, source_root, sldb_root are absolute paths within workspace_root except project”. Falta decidir su origen/derivación.
2. La aceptación final exige “the declared setup runtime task”, pero no se identifica cuál es ni aparece en `depends_on`, que solo lista `task-scion-autonomy-review-status`. Falta decidir esa dependencia.
3. Se exige “auto-detect tester RoleDoc” y “role-deskops-tester/--mode tester”, pero `files` solo incluye `desk/roles/deskops-supervisor.md`. Falta decidir si el RoleDoc tester ya existe o debe crearse, y su ruta.

**DRY-RUN**

No ejecuté comandos ni modifiqué archivos.

- **Lecturas hipotéticas:** task Markdown, RoleDoc supervisor, `runtime/scion.py`, `cli/registry.py`, `cli/commands/runtime.py`, tests/goldens, átomo y docs.
- **Cambios hipotéticos:** corregir RoleDoc vía SLDB; añadir `--context-file` y kwarg de contexto; generar entorno/volumen; añadir modo/detección tester; helper de nombres/labels; documentar átomo y operador; ampliar tests.
- **Validaciones hipotéticas:** `pytest tests/test_scion_runtime.py`; goldens de help si cambia `--mode`; rechazo de contexto inválido antes de generar salida; digest canónico, nombres/labels/attempt; preservación sin contexto; ejemplos CLI completos; integración viva.

**FUTURO**

Comprobar en implementación, no como ambigüedad: que omitir contexto preserve entorno/CLI; que todas las rutas sean absolutas dentro de `workspace_root`; que `PYTHONPATH` sea exactamente `source_root + os.pathsep + sldb_root`; que no haya secretos; que la identidad use `hash_fields_with_map` y `contract_hash`; que los cambios de status/history/references no alteren identidad; que la reconciliación cubra running/stopped/completed/conflictivo sin duplicar; que el orden del Board sea el desempate; que ambos límites sean 2 intentos totales; y que la integración real use la tarea de setup cuando exista.
