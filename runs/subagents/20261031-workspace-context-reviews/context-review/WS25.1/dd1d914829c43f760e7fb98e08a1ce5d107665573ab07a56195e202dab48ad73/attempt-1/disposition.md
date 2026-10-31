# Executor comparison — WS25.1, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

REFORMULACION
- **Propósito**: dotar al workspace de una vista de inbox que permita leer mensajes del desk y registrar acuse (ack) o respuesta local, usando solo operaciones autorizadas por el contrato WS12.
- **Resultado**: UI en `graph_ui` que muestra mensajes, persiste el ack tras recargar junto al mensaje origen y, solo si WS12 define la operación, registra respuesta local; en caso contrario la declara no disponible. No crea tareas implícitas ni cron de triage.
- **Repo dueño**: `graph_ui` (`output_base: graph_ui:repository_root/`), con salida en `frontends/mindmap/views/workspace/inbox/`, endpoints autorizados por WS12 y `tests/`.
- **Límites**: mismo desk, sin envío interdesk; ack ≠ aprobación; permisos del contrato aplicados; mutaciones de UI sujetas a `G_HUMAN_READ`; desarrollo y pruebas aisladas de API pueden avanzar sin acta humana de lectura.

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
