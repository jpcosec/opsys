# Executor comparison — WS35, final per-effect contract input

State: accepted_current

## Reformulación examinada

REFORMULACION
Propósito: revisar WS35 como encargo de planificación para una vista de lectura de ejecución y trazabilidad. Resultado: UI en `graph_ui` que muestra mensajes, resultados y decisiones bajo intento/tarea, enlaza fuentes y abre evidencia en el lector WS13, sin traducir `completed` en aprobado/cerrado. Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/execution/` y `tests/`. Límites: lectura; no mutaciones, dispatch, cierre ni aprobación; sujeto a `G_SCION` y `G_UI_READ`; archivos, pruebas y textos concretos quedan al TaskDoc de promoción.

## Hallazgos/disposición contra intención

Backend WS33.1 ahora suministrado marca no vinculados como huecos de procedencia y prohíbe atribuir conversación completa a intento. «cada mensaje bajo su intento/tarea» aplica a mensaje vinculado con origen resoluble, no autoriza esconder ni fabricar vínculo; estado de hueco se muestra como tal en tratamiento de errores/contrato WS11. Forma/lista visual se concreta TaskDoc. Dry-run identifica ambos datos y futura prueba de no vinculados. Conversación es procedencia de mensajes definida por WS33.1; orden/agrupación visual se fija TaskDoc, sin nuevo modelo. Decisión explícita es de WS33.2 (scope WS33 agregado la nombra); WS32 aporta intento, no aprobación. Sin intento no se fabrica decisión vinculada ni aprobación; reglas backend/contrato WS12 conservan hueco de procedencia.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
