## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/ui.md`, auditoría de solo lectura verificable fila por fila: mapeo de cada nodo graph_ui a base reutilizada/delta/ticket o ausencia, tareas externas con hash, solapamientos entre sesiones y reconciliación del SPEC externo.

**Alcance:** leer Board (`../UIs/graph_ui/desk/tasks/Board.md`), tareas de graph_ui, git y `herdr pane list`; escribir solo `auditoria/ui.md` y evidencia en `runs/subagents/20261031-ws04-auditoria-ui/`.

**Repo:** deskops (cwd) como ejecutor; lecturas en graph_ui y softfactory_spec.

**Límites:** sin commits, sin closeout, sin tocar código, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas de otros. Nada no comprobado se infiere: se marca «no comprobado» con causa. WS05, contratos e implementación quedan fuera.

## AMBIGUEDADES

1. «los 35 con owner_repo graph_ui en dag.yaml» — `dag.yaml` no está en el bundle frío ni se adjunta; el número y los IDs no son verificables. Obligaría a inventar la lista del universo.
2. «los que mencionan graph_ui sin ser suyos (WS06, WS07, WS10, WS11)» — no define qué cuenta como «mencionar» (referencia estructurada, texto, dependencia). Obligaría a inventar el criterio de inclusión.
3. «base reutilizada/delta/ticket o ausencia explícita» para filas «solo referencia» — no dice qué valor corresponde a nodos no propios. Obligaría a inventar una convención de columnas.
4. «commit observado» — no fija precedencia entre `a1b2b22`, `f16fcd1`, `134a665` ni qué hacer si hay varios. Obligaría a inventar cuál se registra.
5. «Sesión = trabajo en curso observable en Board, git status o paneles herdr» — no hay identidad de sesión ni regla de atribución; `git status` no asigna autoría. Obligaría a inventar límites de sesión y, por tanto, solapamientos.
6. «una fila por sección ## de SPEC.md» — no aclara si las subsecciones cuentan ni el SPEC está en el bundle. Obligaría a inventar granularidad.
7. `files` enumera solo `auditoria/ui.md`, pero Implementation Path exige `commands.log` y `result-summary.md`. Obligaría a inventar si `files` es exhaustivo. El Tester independiente, los commits y el closeout del Supervisor son encargos futuros asignados, no lagunas.

## DRY-RUN

**Leería:** TaskDoc, `dag.yaml`, `Board.md`, tareas de `desk/tasks` de graph_ui, `reconciliacion.md`, `SPEC.md`, metadatos git de deskops/graph_ui y `herdr pane list`.

**Entregable:** `auditoria/ui.md` con encabezado (fecha, HEAD completo y rutas sucias por repo, SHA-256 de archivos citados sucios), tabla de nodos, tareas externas, solapamientos, sesiones y tabla SPEC. Evidencia: `commands.log`, `result-summary.md`.

**Comandos después (no ejecutados):** `git -C ../UIs/graph_ui rev-parse HEAD`; `git status --porcelain` por repo; `sha256sum` de fuentes; `herdr pane list`; `test -s …/ui.md`; `python …/build_plan.py --check`; `validate_plan.py --check`; `context_review.py status`.

**Resultado esperado:** archivo no vacío; checks de plan sin errores o con salida registrada; Tester muestrea filas. Baseline de validadores desconocido: no se presume verde.
