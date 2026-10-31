# Executor comparison — WS13.3

State: accepted_old_input_superseded

## Reformulación examinada

## REFORMULACION

Propósito: revisar WS13.3 como encargo de planificación, no como producto ni ejecución. Resultado esperado: un nodo de implementación en `graph_ui` que añada pestañas documentales, dos documentos en divisiones, foco por documento e historia de navegación local. Repo dueño: `graph_ui`; `output_scope` limita a `frontends/mindmap/views/workspace/layout/`, rutas de lectura del contrato WS11 y `tests/`. Límites: depende de WS11 (contrato de navegación/identidad) y WS13.1 (lectura); requiere G_UI_READ por delta; la disposición es local y no se exige persistir tras recargar; no es documento compartido ni crea workspace paralelo.

##

## Comparación con intención / hallazgos

Hallazgos 1/2 descartados como diseño futuro expresamente asignado: scope exige pestañas/divisiones e historia y depends_on WS11, cuyo contrato fija foco/enlaces/historia. La guía dice «El TaskDoc de promoción fija archivos, escenarios de prueba y textos de pantalla dentro de lo que la aceptación del nodo pide». No se exige aquí un layout UI concreto; abrir/cambiar/cerrar/volver conservando foco/origen es comprobable. Al promover, TaskDoc debe fijar interacción cierre/historia contra contrato WS11; no permiso para improvisar producto.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
