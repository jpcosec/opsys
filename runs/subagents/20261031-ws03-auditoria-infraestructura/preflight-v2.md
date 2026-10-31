## REFORMULACION

**Objetivo:** producir una auditoría de solo lectura, verificable fila por fila, del estado actual de persistencia, consultas y notaciones en sldb, pron y spec2viz, para alimentar WS06 y WS08-12.

**Alcance:** cinco capacidades (fuente/payload; conflictos y concurrencia; referencias documentales; búsquedas e índices; notaciones/renderers y alcance real de ViewDoc). Una sección por capacidad; filas con columnas capacidad, repo, ubicación, operación expuesta, estado (comprobado/ausente/hueco) y evidencia. CAS y locks son hipótesis a comprobar, no hechos.

**Repo/entregable:** únicamente `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` y evidencia en `runs/subagents/20261031-ws03-auditoria-infraestructura/` (commands.log, result-summary.md). Lectura en `../sldb`, `../pron`, `../spec2viz`; Kimun excluido del universo.

**Límites:** solo lectura fuera del entregable; sin commits ni closeout (Executor); no tocar código, dag.yaml, reconciliacion.md, Board ajeno ni otras tareas. Hash = SHA-256; encabezado con fecha, HEAD completo y rutas sucias por repo leído; archivo sucio citado lleva su SHA-256.

## AMBIGUEDADES

1. «estado (comprobado/ausente/hueco)»: no define la diferencia entre «ausente» y «hueco»; obliga a inventar el criterio de clasificación.
2. «una fila por repo y mecanismo»: no aclara si se registran filas de mecanismos inexistentes o solo de los hallados; obliga a decidir la cobertura mínima.
3. «notaciones = notaciones y renderers de spec2viz, con el alcance real de ViewDoc»: ViewDoc no se define ni ubica; obliga a inventar qué entidad cuenta como ViewDoc.
4. «Precisiones comunes»: remite a precisiones no incluidas en el archivo; obliga a inventar su contenido o a localizarlas.
5. «Kimun solo referencia» frente a «Kimun no se lee ni entra al universo»: tensión sobre si puede citarse; obliga a decidir si se menciona.
6. «operación expuesta»: no define qué cuenta como expuesta (API pública, CLI, símbolo); obliga a inventar el criterio.
7. «Tester independiente muestrea filas»: sin criterio de muestreo; es tarea futura asignada al Tester, no laguna del Executor, pero su alcance queda indefinido.

*(No son lagunas: commits/closeout del Supervisor y muestreo del Tester son tareas futuras asignadas.)*

## DRY-RUN

**Fuentes que leería:** `git rev-parse HEAD` y `git status --porcelain` en `../sldb`, `../pron`, `../spec2viz`; árboles y búsquedas dirigidas (persistencia, payload, lock, CAS, índice, search, renderer, ViewDoc); planes citados (cierre.md, dag.yaml, brief.md, activation.md) solo como contexto.

**Entregable:** infraestructura.md con encabezado y filas; commands.log; result-summary.md.

**Comandos después de escribir (sin ejecutar):**
- `test -s desk/drawer/plans/workspace-documental/auditoria/infraestructura.md` → salida 0.
- `python desk/drawer/plans/workspace-documental/build_plan.py --check` → plan consistente.
- `python desk/drawer/plans/workspace-documental/validate_plan.py --check` → validación OK.
- `python desk/drawer/plans/workspace-documental/context_review.py status` → sin errores.
- Luego: Tester muestrea filas contra la fuente y deja tester-result-summary.md; Supervisor commitea y cierra.

No ejecuto nada.
