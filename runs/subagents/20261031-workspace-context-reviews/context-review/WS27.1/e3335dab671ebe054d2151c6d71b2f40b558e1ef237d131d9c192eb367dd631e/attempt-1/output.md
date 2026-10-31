REFORMULACION
- Propósito: encargo de planificación para un nodo `implementation` en `graph_ui` que añada a la vista de TaskDoc un diff Git y un historial read-only por repo y tarea.
- Resultado: diff real e historial read-only; base en commits de `TaskDoc.references` y rutas de `TaskDoc.files`; sin commits, working tree contra HEAD limitado a esas rutas; una sección por repo alcanzado, “con el repo declarado”.
- Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/diff/` y `tests/`.
- Límites: no escribir ni revertir; no mostrar hallazgos de integridad del store (WS29); asociación a intento queda para WS35; promoción `not_authorized`; depende de WS13/WS12 y `G_UI_READ` pendiente.

AMBIGUEDADES
1. “Diff real e historial read-only acotados al repo y tarea”: no define qué commits, ventana, filtro u orden componen el “historial” de la tarea. Obliga a inventar el alcance y el criterio comprobable del historial, salvo que se reduzca a los commits de `TaskDoc.references`.
2. “Se muestra una sección por cada repo alcanzado por TaskDoc.files, con el repo declarado”: no indica dónde se declara el repo ni cómo resolver ruta→repo cuando `TaskDoc.files` pueda abarcar varios. Obliga a inventar esa resolución y el agrupamiento, que afectan a la aceptación.

DRY-RUN
- Lecturas previstas: nodo WS27.1, modelo TaskDoc (`references`, `files`), contrato de rutas WS11 y contrato de operaciones WS12; `G_UI_READ` como gate per-delta.
- Cambios previstos: solo vista/tests en `graph_ui` bajo `frontends/mindmap/views/workspace/diff/`; ninguna escritura Git.
- Dependencias: WS13 aporta lector/historia/foco; WS12, operaciones y límites; WS11, rutas de lectura declaradas.
- Validaciones futuras: diff real, historial read-only, ausencia de mutación/reversión, sección por repo, exclusión de hallazgos WS29 y recibo `G_UI_READ` del delta.

FUTURO
- WS35 añade la asociación a intento; WS29, integridad del store; WS11/WS12 entregan contratos y WS11 emite el recibo `G_UI_READ` por delta.
- La promoción fijará archivos, pills, evidence y preflight; WS27 cierra como agregado cuando lo hagan sus hijos.
