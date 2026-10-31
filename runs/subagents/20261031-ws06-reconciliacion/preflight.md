## REFORMULACION

- **Objetivo:** agregar a `reconciliacion.md` una matriz de correspondencia por capacidad o delta único, agrupada por repo dueño, con evidencia citada, y una tabla de cobertura de los 63 nodos del DAG. No se aceptan deltas ni se produce permiso interrepo.
- **Alcance:** solo documentación. Añadir la sección «Matriz de correspondencia WS06» conservando el texto existente; escribir `runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md` y `result-summary.md`.
- **Repo:** `deskops`; las rutas `../` son relativas a su raíz.
- **Límites:** el Executor edita solo `reconciliacion.md` y escribe los dos archivos indicados; sin commits ni closeout. No toca código, `dag.yaml`, `brief.md`, auditorías, Board de `graph_ui`, WS05 ni WS07-12. El Tester es de solo lectura. Son tareas futuras asignadas —no lagunas—: recibos externos en WS11/12, validaciones/commit/closeout del Supervisor, ajuste canónico de `dag.yaml` y descomposición WS32/33.

## AMBIGUEDADES

1. **Cobertura: fila obligatoria vs. motivo sin fila.** Cita: «su fila C-nn, o el motivo por el que no generan delta (planificación, validación humana, agregado). Ningún nodo queda sin fila». Obligaría a inventar si los nodos de planificación/validación/agregado deben tener igualmente un `C-nn` o pueden quedar solo con motivo, y cómo contarlos en la cobertura.
2. **Validador esperado: `build_plan.py` vs. `validate_plan.py`.** Cita: «`validate_plan.py --check` falla por eso» frente a «`python .../build_plan.py --check`» en Validation. Obligaría a decidir cuál comando ejecutar, cuál debe fallar y si `build_plan.py --check` debe pasar o fallar.
3. **Clasificación de `frontends/workspace`.** Cita: «fila con ese estado, sin reclamo en Board o TaskDoc, sin commit». La columna Clasificación solo admite «ya cubierto, extender ticket, nuevo delta». Obligaría a inventar cuál de las tres aplica y cuál es el ticket/delta destino.

## DRY-RUN

**Fuentes que leería:** este encargo; `approval.md`; `auditoria/deskops.md`, `infraestructura.md`, `ui.md`; `dag.yaml`; `decisiones.md`; `alcance.md`; `reconciliacion.md`; pills indicadas. Abriría código citado solo para confirmar filas, sin reauditar.

**Entregable:** sección «Matriz de correspondencia WS06» con subtítulos por repo dueño y tabla `C-nn | capacidad/delta | nodos DAG | clasificación | path/símbolo y commit | ticket/delta destino | responsable | límites`, más tabla de cobertura de 63 nodos; `canonical-adjustments.md`; `result-summary.md`.

**Comandos posteriores y resultado esperado, sin ejecutar:**
- `test -s desk/drawer/plans/workspace-documental/reconciliacion.md` → éxito.
- `python desk/drawer/plans/workspace-documental/build_plan.py --check` → resultado sujeto a ambigüedad 2.
- `python desk/drawer/plans/workspace-documental/context_review.py status` → exactamente los 25 nodos declarados como «input changed».
- `validate_plan.py --check` → fallo esperado por esos 25 nodos, no corregido en WS06.
- `git diff --stat 3e1c24f0..HEAD -- deskops/ tests/ docs/ .../dag.yaml .../brief.md .../auditoria/` → vacío.
