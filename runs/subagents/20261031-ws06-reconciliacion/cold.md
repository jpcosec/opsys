## REFORMULACION

- **Objetivo:** añadir a `reconciliacion.md`, sin cambiar el texto existente, la sección «Matriz de correspondencia WS06»: una fila `C-nn` por capacidad o delta único (no por nodo), agrupada por repo dueño, con nodos DAG que remiten, clasificación, path/símbolo y commit observado, destino, responsable P01 y límites de evidencia; más una tabla de cobertura de los 63 nodos de `dag.yaml`.
- **Alcance:** solo esa edición; el Executor escribe además `canonical-adjustments.md` y `result-summary.md` en el run-dir; no hay commits ni closeout suyos.
- **Repo:** `deskops`; las rutas `../` se leen desde su raíz y el código de `graph_ui` se abre solo para confirmar una fila, sin reauditar.
- **Límites:** no produce aceptación ni permiso interrepo; los recibos los emite el receptor P01 y WS11/12 solo enlazan contrato; Scion queda para el ramal E con designación posterior; no se notifica, despacha ni toca el Board; no se reabren P01–P09; lo imprescindible fuera de scope solo se lista, no se aplica. Tareas futuras asignadas, no lagunas: descomposición Scion WS32/33 sin WS05, ajuste canónico de `dag.yaml` por el Supervisor, y WS05/WS07/WS08–12/código UI fuera de alcance.

## AMBIGUEDADES

1. «ID estable C-nn»: no fija criterio de numeración (por repo, por orden de `dag.yaml` o de aparición). Obliga a inventar una convención; Executor y Tester podrían numerar distinto.
2. «una tabla con los 63 nodos de dag.yaml y su fila C-nn, o el motivo por el que no generan delta» frente a «Ningún nodo queda sin fila»: obliga a inventar un valor centinela (¿`C-00`, `N/A`?) para nodos de planificación, validación humana o agregado, que no encajan en las tres clasificaciones.
3. «ticket o delta destino» con «extender ticket existente (incluido un draft del Board)»: no se enumeran tickets de `sldb`, `spec2viz` ni `deskops`; obliga a inventar identificadores o a dejar la celda vacía sin regla escrita.
4. «path o símbolo y commit observado»: no define qué commit ni de qué repo cuando hay varios (HEAD de `deskops`, `134a665` de `graph_ui`, hashes de auditoría). Obliga a inventar el criterio.
5. «frontends/workspace ... fila con ese estado, sin reclamo en Board o TaskDoc, sin commit»: «sin reclamo» no fija el texto exigido; ambiguo si prohíbe citarlo como base o solo afirmar adopción aprobada.

## DRY-RUN

- **Fuentes a leer:** TaskDoc, `approval.md`, `reconciliacion.md`, `dag.yaml`, `decisiones.md`, `alcance.md`, las tres auditorías y los rituales/pills enlazados; código citado solo para confirmar filas.
- **Entregable:** esta reformulación (sin editar); después, sección matriz + cobertura + `canonical-adjustments.md` + `result-summary.md`.
- **Comandos posteriores y resultado esperado:** `test -s .../reconciliacion.md` → 0; `python build_plan.py --check` → 0; `python context_review.py status` → exactamente los 25 nodos declarados como «input changed»; `git diff --stat 3e1c24f0..HEAD -- deskops/ tests/ docs/ dag.yaml brief.md auditoria/` → vacío; Tester deja `tester-result-summary.md` con PASS.
