# Resultado WS06 — matriz de correspondencia

Editado: `desk/drawer/plans/workspace-documental/reconciliacion.md` (sección «Matriz de correspondencia WS06» añadida al final; el texto previo queda byte a byte igual, verificado contra una copia previa). Escritos además `canonical-adjustments.md` y este resumen. Sin commits, `git add`, closeout ni comandos mutadores de deskops; no se tocaron dag.yaml, brief.md ni auditorías; no se corrió `context_review.py run`.

## Conteos

- Filas: 68 (graph_ui 37, sldb 10, spec2viz 3, deskops 18).
- Por clasificación: ya cubierto 33, nuevo delta 32, extender ticket 2, no adoptado 1.
- Extender ticket: edición contextual y Changes (drafts del Board de graph_ui). C-64 (Scion) reclasificada a nuevo delta con el candidato del drawer como fuente. No adoptado: `frontends/workspace/`.
- Cobertura: los 63 nodos de dag.yaml aparecen en la tabla de cobertura (comprobación Python de solo lectura: 63/63, sin faltantes ni extras; todo C-nn referenciado tiene fila y toda fila tiene al menos un nodo). 20 nodos van como «sin delta» con motivo (planificación, auditoría entregada, validación humana, documentación, contratos); 9 agregados remiten por sus hijos.
- Correcciones post-Tester: C-50 acotada a portabilidad, C-64 reclasificada, C-28 con límite de doctor/drift, ajuste 1 precisado.
- Ajustes canónicos: 5 (CAS/revisión, captura directa a drawer, ViewDoc y alcance de WS18, texto «acepta por delta» de WS06, revisiones de contexto de 25 nodos).

## Decisiones de clasificación dudosas

- C-64 (Scion RunDoc/cierre): reclasificada tras el Tester a nuevo delta; el destino es un candidato diferido del drawer, no un ticket. Se conserva la descomposición WS32/33.
- C-55 (captura directa a drawer): nuevo delta con productor deskops; podría resolverse componiendo `message send` más `promote inbox-to-drawer-task`. Se deja a WS12.
- C-23 (capa lista): ninguna auditoría muestra un comando que la calcule; se propone derivarla en graph_ui desde `depends_on` y `files`.
- C-41 (CAS por revisión): se marca nuevo delta en sldb sin ticket; ningún nodo lo produce (ver ajuste 1).
- C-57 (enrutado con `edit board`): ya cubierto, pero la auditoría no ejercitó el caso de una tarea ya existente.
- C-50 (ViewDoc portable): nuevo delta; el alcance exacto (compartir el evaluador de graph_ui o consumirlo) se decide al promover.
- WS43 va como «sin delta» (documentación con operaciones existentes).

## No comprobado

- Nada se ejecutó: las filas se apoyan en código leído por las auditorías. Se confirmaron por lectura solo la existencia de símbolos en graph_ui (`workspace_routes.py`, `workspace.mjs`, `deskops_routes.py`, `projection_views.py`, `persistence.py` 409), `DeskopsOperations` (`verify_task_closeout`, `split_atom`, `merge_atom`), `record_scion_run` y el estado de `frontends/workspace/` (0 archivos versionados).
- Los commits por fila son los de la auditoría; para sldb, spec2viz y deskops, que no citan commit por fila, se usó el HEAD auditado marcado como HEAD. El HEAD actual de deskops (b027a2f2) es posterior al auditado (215bf624).
- Scion: WS05 no existe; ninguna fila afirma una API o campo de Scion. Los tickets de sldb y spec2viz se miraron solo por título; ninguno cubre CAS ni ViewDoc.
- `build_plan.py --check`, `context_review.py status` y la verificación del Tester no se corrieron (corresponden al Supervisor y al Tester).
