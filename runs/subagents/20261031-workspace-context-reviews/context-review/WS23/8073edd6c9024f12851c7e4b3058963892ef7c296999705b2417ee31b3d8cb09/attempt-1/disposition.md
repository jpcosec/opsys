# Executor comparison — WS23, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

REFORMULACION
Propósito: implementar en graph_ui la vista de procedimiento que renderiza RitualDoc/StepDoc/lifecycle desde referencias reales, con pasos y fuentes navegables y transiciones solo representadas. Resultado: vista de solo lectura que abre documentos/soporte y muestra el estado de pasos proveniente de deskops, sin escribirlo ni auto-marcarlos. Repo dueño: graph_ui; salida en `frontends/mindmap/views/workspace/procedure/` y `tests/`. Límites: no acciones de transición, no escritura de estado; pruebas con corpus WS40 o store temporal; depende de WS13/WS09 y G_UI_READ por delta; promoción no autorizada.

## Hallazgos/disposición contra intención

Corregido: pasos authored son inertes salvo campo/API real inventariado WS02/09/11. Transiciones muestran origen/destino/condición lifecycle; sin controles de avance y prueba de no escrituras. No inventar progreso.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
