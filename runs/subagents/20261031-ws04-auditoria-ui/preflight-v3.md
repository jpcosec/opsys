**REFORMULACION**

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/ui.md` como auditoría de solo lectura, verificable fila por fila.

**Alcance:** leer Board, tareas y código actuales de `../UIs/graph_ui`; mapear los 35 nodos con `owner_repo graph_ui` y WS06/WS07/WS10/WS11 como «solo referencia»; registrar sesiones y solapamientos observables; reconciliar `SPEC.md` externo. Entregable único: `ui.md`; evidencia en `runs/subagents/20261031-ws04-auditoria-ui/`.

**Repo:** trabajo en `deskops`; lectura de `../UIs/graph_ui` y `/home/jp/proyectos/softfactory_spec/SPEC.md`; se declaran repos leídos: deskops, graph_ui y softfactory_spec.

**Límites:** solo lectura fuera del entregable y evidencia; no se modifica código, otro repo, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas ajenas; fuera de alcance WS05, contratos nuevos e implementación. El Executor escribe entregable y evidencia, sin commits ni closeout; el Supervisor corre validaciones, hace commits y closeout; un Tester independiente verifica. Tareas futuras asignadas, no lagunas: `commands.log`, `result-summary.md` y `tester-result-summary.md`.

**AMBIGUEDADES**

1. «si el código cumple parte de su alcance citando path o símbolo»: «parte» no fija umbral; obligaría a inventar cuándo un path basta para marcar delta y cuándo procede ausencia explícita.
2. «ampliar historia solo cuando una referencia actual apunta a un commit fuera de los tres citados»: no define qué es «referencia actual» ni su vigencia; obligaría a inventar si cuentan Board, ticket, `reconciliacion.md` o código.
3. «si un archivo citado como evidencia está sucio, se agrega su SHA-256»: no delimita «citado como evidencia»; obligaría a inventar si incluye Board, tareas, SPEC o reconciliación.
4. «misma ruta en campos files de TaskDoc o en git status de dos sesiones» junto con «sin atribución»: no explica cómo ligar una ruta sucia a una sesión o reclamo; obligaría a inventar atribución, que el texto prohíbe.
5. «Hash = SHA256 del archivo de tarea»: no aclara si es por cada tarea externa o solo el TaskDoc propio; obligaría a inventar el universo hasheado.
6. «Registrar comandos usados en .../commands.log»: no fija formato; obligaría a inventar columnas o esquema.

**DRY-RUN**

**Fuentes que leería:** el TaskDoc; `Board.md` y `desk/tasks` de graph_ui; código de graph_ui; `reconciliacion.md` y `dag.yaml`; `SPEC.md`; `git status --short`, `git rev-parse HEAD` y `git log -- <path>` en repos leídos; `herdr pane list`; commits `a1b2b22`, `f16fcd1`, `134a665`.

**Entregable:** `ui.md` con encabezado, tabla por nodo y tabla por sección `##` del SPEC; además `commands.log` y `result-summary.md`.

**Comandos que correría después:** `git -C ... rev-parse HEAD`; `git -C ... status --short`; `git -C ... log -- <path>`; `herdr pane list`; `sha256sum`; `test -s desk/drawer/plans/workspace-documental/auditoria/ui.md`; `python .../build_plan.py --check`; `python .../validate_plan.py --check`; `python .../context_review.py status`; muestreo del Tester.

**Resultado esperado:** `ui.md` no vacío, checks de plan sin error, estado de contexto reportado y `tester-result-summary.md` del Tester. No ejecutado.
