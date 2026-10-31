## REFORMULACION

**Objetivo.** Producir `desk/drawer/plans/workspace-documental/auditoria/ui.md`: auditoría de solo lectura, verificable fila por fila, del estado actual de graph_ui (Board, tareas, código), de los nodos del plan workspace-documental que toquen graph_ui, del SPEC externo y de las sesiones en curso con sus solapamientos.

**Alcance.** Leer `../UIs/graph_ui`, `/home/jp/proyectos/softfactory_spec/SPEC.md`, `reconciliacion.md` y `dag.yaml`; inventariar tareas externas (path, estado, SHA256, alcance), mapear cada nodo graph_ui a base reutilizada/delta/ticket o ausencia explícita, registrar solapamientos y reconciliar el SPEC (coincidencias, discrepancias, ausencias). Marcar «no comprobado» con causa; no inferir.

**Repo.** Trabajo en deskops (entregable en `desk/drawer/plans/.../auditoria/ui.md`); lectura de graph_ui y softfactory_spec.

**Límites.** Solo lectura fuera del entregable; se escribe además evidencia en `runs/subagents/20261031-ws04-auditoria-ui/`. No se modifica código, otro repo, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas de otros. Sin commits, sin closeout, sin WS05/Scion, sin contratos nuevos ni implementación.

## AMBIGUEDADES

1. «mapear a deltas existentes los nodos de este plan que toquen graph_ui (tarea o entrada del Board de graph_ui, o commit que ya lo implementa)». No se define **de dónde salen los «deltas existentes»**: ¿tareas del Board de graph_ui, filas de `reconciliacion.md`, o ambos? Obliga a inventar la fuente de correspondencia.
2. «dag.yaml para listar nodos graph_ui». Falta el **criterio de filtrado** (campo, tag, path, mención textual). Obliga a inventar la regla de selección.
3. «identificar sesiones y solapamientos… archivos reclamados por dos sesiones». El Board no declara archivos reclamados; obliga a inventar cómo derivarlos (¿`files:`, ¿paths en summary?, ¿git status?).
4. «encabezado con fecha, commit HEAD de cada repo leído». No se enumeran los repos «leídos» (¿desk, graph_ui, softfactory_spec?). Obliga a inventar el conjunto.
5. «reconciliar también el SPEC externo (coincidencias, discrepancias y ausencias frente a este plan)» sin granularidad: ¿por nodo, por capacidad, por sección? Obliga a inventar la unidad de comparación.
6. «universo auditado» del encabezado no se define (¿repos, paths, IDs de nodos?).

No son lagunas: la prueba independiente del Tester, el closeout y WS05 son tareas futuras asignadas, no huecos del encargo.

## DRY-RUN

**Fuentes a leer:** `../UIs/graph_ui/desk/tasks/` y Board; `git log`/`status` de graph_ui y deskops; `frontends/mindmap/workspace_routes.py`, `deskops_routes.py`, `views/workspace/*`; `softfactory_spec/SPEC.md`; `reconciliacion.md`; `dag.yaml`.

**Entregable:** `auditoria/ui.md` con encabezado (fecha, HEAD por repo, universo) y tablas de tareas externas, mapeo de nodos graph_ui, solapamientos y reconciliación SPEC; más `commands.log` y `result-summary.md` en el run dir.

**Comandos posteriores (sin ejecutar aún):**
- `git -C ../UIs/graph_ui rev-parse HEAD` y `git -C . rev-parse HEAD` → dos SHA esperados.
- `git -C ../UIs/graph_ui status --porcelain` y `git status --porcelain` → trabajo en curso observable.
- `sha256sum` sobre cada tarea citada y `SPEC.md` → hashes para las filas.
- `herdr pane list` → lista de sesiones o ausencia registrada.
- Lectura de `dag.yaml` filtrando nodos graph_ui.
- Tras escribir: `test -s .../auditoria/ui.md` (éxito), `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status` (salida esperada verde; si falla, se reporta, no se corrige el plan).
