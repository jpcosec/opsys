# Executor comparison — WS27.1

State: requires_contract_correction_rereview

## Reformulación examinada

REFORMULACION
- Propósito: encargo de planificación para un nodo `implementation` en `graph_ui` que añada a la vista de TaskDoc un diff Git y un historial read-only por repo y tarea.
- Resultado: diff real e historial read-only; base en commits de `TaskDoc.references` y rutas de `TaskDoc.files`; sin commits, working tree contra HEAD limitado a esas rutas; una sección por repo alcanzado, “con el repo declarado”.
- Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/diff/` y `tests/`.
- Límites: no escribir ni revertir; no mostrar hallazgos de integridad del store (WS29); asociación a intento queda para WS35; promoción `not_authorized`; depende de WS13/WS12 y `G_UI_READ` pendiente.

## Comparación con intención / hallazgos

1 historial limitado a commits TaskDoc.references orden fecha y files, sin refs se declara ausencia y diff working tree HEAD. 2 repo/aliases/root resuelve WS11 y si no resoluble queda no disponible, sin escritura cruzada.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
