REFORMULACION
WS04 es un nodo de planificación (`kind: planning`, `owner_repo: deskops`) que produce `auditoria/ui.md`: inventario del Board, tareas, sesiones y código actual de graph_ui; mapeo de los nodos del plan que tocan graph_ui a tarea/entrada del Board/commit existente o ausencia explícita; y reconciliación del SPEC externo. Límites: solo lectura; no cambia tareas, no notifica ni despacha, no modifica el Board; un commit solo prueba la base citada, no aceptación ampliada.

AMBIGUEDADES
1. «Cada tarea externa con path, estado observado, hash y alcance» frente a «mapear a deltas existentes los nodos de este plan que toquen graph_ui»: no fija si el inventario abarca todas las tareas del Board de graph_ui o solo las vinculadas a nodos del plan. Obligaría a inventar el criterio de inclusión y, con él, la exhaustividad exigida.
2. «cada solapamiento (misma tarea o archivos reclamados por dos sesiones)»: no define de dónde se obtiene que un archivo esté «reclamado» (TaskDoc, git status, herdr o declaración). Obligaría a inventar la fuente de los claims y el método de comparación.

DRY-RUN
Lecturas: HEAD/Board de graph_ui, task files, git status, paneles herdr, `SPEC.md`, dag y documentos del plan. Cambios previstos: crear `auditoria/ui.md` con inventario (path, estado, SHA256, alcance), tabla de mapeo por nodo graph_ui (base/delta/ticket/ausencia, path/símbolo, commit), filas de solapamiento, sección SPEC (coincidencias/discrepancias/ausencias, path/hash) y registro de encargo y sesiones (presentes/ausentes). Dependencias: WS01 y lectura de graph_ui; `requires: []`; sin gates propios. Validaciones futuras: SHA256 por tarea, tabla sin nodos omitidos, solapamientos con dos sesiones, SPEC con path/hash. Errores: graph_ui o SPEC ausente, tarea sin archivo o herdr no observable → registrar hueco con repo dueño y detenerse según reglas comunes, sin sustituto.

FUTURO
WS06 consume `auditoria/ui.md` para `reconciliacion.md` y la matriz por repo dueño. El coordinador/solicitante decide la disposición de solapamientos y autorizaciones; WS11/WS12 podrán enlazar actas externas, pero WS04 no produce recepción, gates ni permiso de implementación.
