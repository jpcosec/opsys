## REFORMULACION

**Objetivo:** completar `desk/drawer/plans/workspace-documental/borradores/vistas.md` con 20 fichas (F01–F20, orden de las dos tablas: 12 + 8) en sección nueva «Fichas por fila», cada una con los 14 campos obligatorios (propósito, origen, identidad, contrato/«sin contrato», campos y relaciones, renderer, navegación, acción/dueño, destino de escritura, error, estado, clase, UF, evidencia con cita archivo:línea).

**Alcance:** inventariar las filas existentes; estado ∈ {disponible, propuesto, bloqueado} con ninguna disponible (sin actas); clase por componente (authored/derivado/preferencia local); «no definido» con productor (WS11/WS12 o nodo DAG real, o «sin productor en el DAG» y repo dueño); errores condicionados, nunca inventados; UFs de UF01–UF10 o «ninguna» con motivo; filas compuestas por listas o sufijo a/b solo con delta evidenciado.

**Repo:** `deskops` (rutas `desk/...` y `runs/...`). Otros repos hermanos fuera.

**Límites:** el Executor escribe solo `vistas.md` y `runs/subagents/20261101-ws09-vistas/result-summary.md`; sin commits, sin revisiones, sin UI/WS11/WS12/Scion/dag.yaml/validadores; sin preguntar; reutilizar texto/tablas existentes sin reescribir por estilo; `execution_authorized` global false.

## AMBIGUEDADES

1. **«Leer ... `reconciliacion.md`»** (Implementation Path) no figura en `references` ni en el bundle; obligaría a inventar ruta o contenido si no existe.
2. **Definiciones de estado** remiten a `borradores/manual.md`, no incluido en el bundle; el criterio «bloqueado si hay dependencia o contrato identificado pendiente, y propuesto si no» no aclara el caso «sin contrato» con renderer base existente → fuerza a inventar la frontera propuesto/bloqueado.
3. **«con sufijo a/b»** solo admite dos componentes; si tres componentes difieren en evidencia/estado, no hay regla (¿a/b/c?).
4. **Clases «authored/derivado/preferencia local»** no están definidas en el bundle; riesgo de inventar criterio de asignación.
5. **Sección existente «Ficha de cada vista (pendiente de completar)»**: no se indica si se conserva o sustituye al añadir «Fichas por fila».
6. **`dag.yaml`** citado como fuente de productores pero ausente del bundle; el Executor deberá leerlo (no bloqueante, pero es hueco de cobertura).

## DRY-RUN

Un Executor futuro: (1) leería completos `vistas.md`, `user-flows.md`, `manual.md`, `decisiones.md`, `dag.yaml` y las tres auditorías con Read, anotando líneas; (2) contaría las filas (12 + 8) y redactaría `### F01`…`### F20` bajo «## Fichas por fila», sin tocar tablas previas; (3) para cada ficha rellenaría los 14 campos, marcando «no definido» + productor donde falte evidencia, y citaría `archivo:línea`; (4) escribiría `result-summary.md` con reuso, huecos y límites; (5) ejecutaría `grep -c "^### F"`, `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`.

**Errores esperables:** `reconciliacion.md` inexistente; grep ≠ 20 si el parser cuenta encabezados duplicados; fallo de build/validate por sección nueva o frontmatter; citas de línea inválidas si no se leyó la celda completa. **Resultado esperado:** 20 fichas, validaciones en verde y Tester independiente PASS.
