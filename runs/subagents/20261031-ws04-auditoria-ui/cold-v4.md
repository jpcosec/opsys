## REFORMULACION

**Objetivo:** producir `desk/drawer/plans/workspace-documental/auditoria/ui.md`, auditoría de solo lectura verificable fila por fila, que inventaríe la UI de `graph_ui` y reconcilie el trabajo en curso: 35 nodos con `owner_repo graph_ui` más WS06/WS07/WS10/WS11 como «solo referencia», tareas externas, sesiones/solapamientos y secciones del SPEC externo.

**Alcance:** leer Board, tareas, código y git de `../UIs/graph_ui`; `reconciliacion.md`, `dag.yaml`, `cierre.md`, `brief.md`; `/home/jp/proyectos/softfactory_spec/SPEC.md`; `herdr pane list`. Escribir solo `auditoria/ui.md` y evidencia en `runs/subagents/20261031-ws04-auditoria-ui/`. No modificar código, otros repos, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas ajenas.

**Repo:** deskops (CWD); lectura en deskops, `../UIs/graph_ui` y `softfactory_spec`.

**Límites:** solo lectura fuera del entregable; sin commits ni closeout del Executor; validaciones de plan y commits del Supervisor; Tester independiente. WS05, WS06, WS08–12 y contratos quedan fuera o son tareas futuras asignadas, no lagunas de este encargo. Lo no comprobado se marca «no comprobado»; un commit solo prueba la base citada.

## AMBIGUEDADES

1. **Universo de tareas externas.** «Tarea externa = archivos de desk/tasks de graph_ui» no aclara si son todas las tareas del directorio o solo las enrutadas/referenciadas por Board y plan. Obligaría a inventar el criterio de inclusión y el conjunto a hashear.

2. **Definición operativa de sesión.** «Sesión = trabajo en curso observable en Board, git status o paneles herdr» choca con «Sesión = fila de `herdr pane list` con pane id y agente o proceso visible» y con «sin ligarlas a un pane salvo que lo muestre». Además, el solapamiento exige «git status de dos sesiones», pero no se define cómo atribuir una ruta sucia a una sesión. Obligaría a inventar esa atribución; debiera bastar «sin atribución» y no afirmar solapamiento.

3. **Entradas de Board sin archivo.** «Entradas de Board sin archivo no llevan hash y se dice», pero también se pide «cada tarea externa con path, estado observado, hash y alcance». Para una entrada sin archivo no hay path ni Scope; obligaría a inventar qué columnas completar.

## DRY-RUN

**Fuentes que leería:** TaskDoc, pills y rituales citados; `cierre.md`, `brief.md`, `reconciliacion.md`, `dag.yaml`; Board y `desk/tasks` de `graph_ui`; rutas de código citadas y su `git log`; SPEC; `git status` y HEAD de los tres repos; `herdr pane list`.

**Entregable:** `auditoria/ui.md` con encabezado (fecha ISO, HEAD completo y líneas de `git status --short` por repo leído), tabla de 35 nodos más 4 de solo referencia, tabla de tareas externas con hash y alcance, sesiones/solapamientos, filas por sección `##` del SPEC con path y SHA-256, y definiciones operativas. En el run dir: `commands.log` y `result-summary.md`.

**Comandos posteriores:** `git -C ../UIs/graph_ui rev-parse HEAD`; `git status --short | wc -l` por repo; `sha256sum` de tareas y SPEC; `git log -- <path>` y `git log -S<simbolo>`; `test -s …/ui.md`; `build_plan.py --check`; `validate_plan.py --check`; `context_review.py status` (Supervisor/Tester, no Executor).

**Resultado esperado:** `ui.md` no vacío, 39 filas de nodos sin omisiones, SPEC cubierto por secciones, rutas sucias sin atribución cuando corresponda, y ningún cambio fuera del entregable y el run dir.
