# Executor comparison — WS36

State: accepted_old_input_superseded

## Reformulación examinada

## REFORMULACION
- **Propósito:** integrar en el workspace la delegación e intervención humanas sobre ejecuciones, sin autoaprobación ni simulación.
- **Resultado:** vista/UI en `graph_ui` que invoca únicamente el adaptador WS34 para dispatch/reply, registra decisiones con WS33.2 y muestra actor humano y evidencia enlazada de WS33.1/WS33.2; la ausencia de API o permisos aparece como error en pantalla.
- **Repo:** `graph_ui`; fuera: `frontends/mindmap/views/workspace/execution/`, ruta fina al adaptador autorizada por contrato WS12 y `tests/`.
- **Límites:** solo adaptador WS34; no canales alternativos, no autoaprobación, no simulación. Los gates pendientes son intencionales; no habilitan por sí mismos ejecución ni Scion.

##

## Comparación con intención / hallazgos

Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
