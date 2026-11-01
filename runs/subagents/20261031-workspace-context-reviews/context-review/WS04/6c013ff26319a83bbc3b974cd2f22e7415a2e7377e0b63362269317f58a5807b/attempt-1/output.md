REFORMULACION
WS04 es un nodo de planificación, no de ejecución. Propósito: inventariar la UI de graph_ui y reconciliar el trabajo en curso con este plan. Resultado: `auditoria/ui.md` con tareas externas (path, estado, hash, alcance), solapamientos y sesiones, reconciliación del SPEC externo y tabla de cada nodo graph_ui con base reutilizada, delta, ticket o ausencia explícita. Repo dueño: deskops; salida en `desk/drawer/plans/workspace-documental/auditoria/ui.md`; lectura de `../UIs/graph_ui` y `SPEC.md`. Límites: solo lectura e inventario; no cambia tareas ni Board, no ejecuta; una sesión es coordinación, no autoridad; un commit solo prueba la base citada.

AMBIGUEDADES
1. «Cada tarea externa con path, estado observado, hash y alcance» frente a «mapear a deltas existentes los nodos de este plan que toquen graph_ui»: no queda fijado si el inventario cubre todas las tareas del Board o solo las vinculadas a nodos del plan. Obliga a inventar el universo y la completitud exigida.
2. «SPEC externo = /home/jp/proyectos/softfactory_spec/SPEC.md» y «reconciliar también el SPEC externo ... con path y hash»: no indica qué hacer si el archivo no existe, no es legible o no permite hash. Obliga a inventar si se falla, se registra ausencia o se continúa.
3. «cada nodo graph_ui» / «nodos de este plan que toquen graph_ui»: no define si incluye nodos con `owner_repo` graph_ui, nodos que producen deltas UI desde otro repo o validaciones sin delta. Obliga a inventar el criterio de inclusión.

DRY-RUN
Leería Board, tareas, código, `git status`/HEAD de `../UIs/graph_ui`, commits `a1b2b22/f16fcd1/134a665`, paneles herdr y `SPEC.md`; consumiría WS01 (brief/glosario). Escribiría `auditoria/ui.md` con inventario, solapamientos, reconciliación SPEC y tabla de mapeo. Sin gates propios. Errores esperables: SPEC ausente, herdr no disponible, tarea sin archivo/hash, sesión no observable, commit no alcanzable; deben registrarse, no suplirse. Validación: cada tarea con path/estado/hash/alcance; cada solapamiento; SPEC con coincidencias, discrepancias y ausencias con path/hash; cada nodo con base/delta/ticket o ausencia explícita; sin modificar Board ni tareas; commit sin sobreafirmar aceptación.

FUTURO
WS06 consumirá `auditoria/ui.md` para su matriz de correspondencia y clasificación por repo. La promoción de WS04 sigue `not_authorized`: un humano o coordinador decide TaskDoc, archivos, pills, evidencia y preflight task-only. La aceptación de la auditoría y la coordinación con sesiones corresponde al solicitante/coordinador.
