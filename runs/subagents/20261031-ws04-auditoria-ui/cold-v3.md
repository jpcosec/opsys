## REFORMULACION

**Objetivo.** Producir `desk/drawer/plans/workspace-documental/auditoria/ui.md`: auditoría de solo lectura del estado actual, verificable fila por fila.

**Alcance.** (a) Tabla de 35 nodos `owner_repo: graph_ui` (lista exacta en el TaskDoc) más WS06/07/10/11 como «solo referencia», con ID, base/delta/ticket o ausencia explícita, path o símbolo y commit observado. (b) Tareas externas de `../UIs/graph_ui/desk/tasks` con path, estado, SHA-256 y alcance. (c) Solapamientos (misma tarea o misma ruta en `files`/git status). (d) Sesiones observables (`herdr pane list`, git status, Board). (e) Una fila por sección `##` de `SPEC.md` frente al plan, con path y hash. Encabezado: fecha, HEAD completo y nº de líneas de `git status --short` por repo leído.

**Repo.** Trabajo en `deskops`; lectura de `../UIs/graph_ui` y `/home/jp/proyectos/softfactory_spec/SPEC.md`.

**Límites.** Solo se escribe la auditoría y evidencia en `runs/subagents/20261031-ws04-auditoria-ui/`. Sin commits, sin closeout, sin tocar código, `dag.yaml`, `reconciliacion.md`, Board ajeno ni tareas de otros. Lo no comprobado se marca «no comprobado» con causa. Commits base: a1b2b22, f16fcd1, 134a665.

## AMBIGUEDADES

1. «commit observado: el de git log sobre el path citado» junto a «path o símbolo». Un símbolo no es ruta: obligaría a inventar si usar `git log -S`, `git blame` o grep del símbolo.
2. «Sesiones: paneles de `herdr pane list`» y «misma ruta … en git status de dos sesiones». No se define qué campo del panel identifica una sesión ni cómo se le atribuye una ruta sucia; obligaría a inventar atribución que el propio texto prohíbe («sin atribuir autoría»).
3. «Ampliar historia solo cuando una referencia actual apunta a un commit fuera de los tres citados», frente a `reconciliacion.md`, que cita 59244c9 y 1fefa97. Obligaría a decidir si esas citas fuerzan ampliar historia (y en qué repo).
4. «una fila por sección `##` de SPEC.md con coincidencias, discrepancias y ausencias frente al plan»: «el plan» no se delimita (¿`cierre.md`, `dag.yaml`, `brief.md`?). Obligaría a inventar el corpus de comparación.
5. «cada tarea externa con … y alcance»: «alcance» no se define (¿`## Scope` del TaskDoc, `files`, tamaño?). Obligaría a elegir un criterio.
6. «Encabezado: fecha»: sin formato fijado; menor, obligaría a elegir ISO o texto libre.

No son lagunas: WS05, WS06, WS08-12, Tester y validaciones de plan aparecen como tareas/roles futuros asignados, no como huecos del encargo.

## DRY-RUN

**Fuentes a leer:** `dag.yaml` (filtrar `owner_repo: graph_ui`), `reconciliacion.md`, `brief.md`, `cierre.md`, `../UIs/graph_ui/desk/tasks/Board.md` y sus `desk/tasks/*.md`, `SPEC.md`, salida de `herdr pane list`, `git status --short` y `git log` de ambos repos.

**Entregable:** `auditoria/ui.md` (encabezado + tablas de nodos, tareas externas, solapamientos, sesiones y SPEC) y en el run dir `commands.log` y `result-summary.md`.

**Comandos previstos (no ejecutados):**
- `git -C ../UIs/graph_ui rev-parse HEAD` → esperado `134a665…` completo.
- `git -C ../UIs/graph_ui status --short | wc -l` → entero; si >0, hashes SHA-256 de los archivos citados.
- `git -C . rev-parse HEAD`, idem status → HEAD de deskops.
- `git -C ../UIs/graph_ui log --format=%H -- <path>` por cada path citado → commits observados.
- `herdr pane list` → paneles; sin coincidencia, «no comprobado» o «sin sesión».
- `grep -n '^## ' SPEC.md` y `sha256sum SPEC.md` → filas de sección y hash.
- `sha256sum` de cada TaskDoc externo → columna hash; entradas de Board sin archivo, sin hash declarado.
