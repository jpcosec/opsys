## REFORMULACION

**Propósito:** entregar una vista de solo lectura de ejecución y trazabilidad en el workspace, jerarquizando tarea, intento, mensajes, resultados y decisiones.

**Resultado:** cada mensaje, resultado y decisión aparece bajo su intento y tarea, enlaza a su fuente y permite abrir la evidencia en el lector WS13; el estado `completed` no se presenta como aprobación o cierre.

**Repo:** `graph_ui`, con salidas en `frontends/mindmap/views/workspace/execution/` y `tests/`.

**Límites:** no ejecuta dispatch/reply ni escrituras de intervención (WS36); no sustituye contratos de WS33/WS27 ni la API de Scion; no autoriza promoción ni implementación por estar el nodo en estado candidato.

## AMBIGUEDADES

Ninguna. Las referencias a WS32/WS33, WS33.1, WS27, WS13 y a la API de Scion identifican productores o dependencias; los gates pendientes son intencionales y las ausencias de contrato se rigen por las reglas comunes de ejecución.

## DRY-RUN

**Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura y bloques de `dag.yaml` del nodo, vecinos y gates.

**Cambios previstos:** ninguno; esta revisión no modifica archivos ni ejecuta pruebas.

**Dependencias:** WS33 (agregado WS33.1/WS33.2) y WS27 (agregado WS27.1/WS27.2), con arrastre de WS11/WS12/WS13. Gates: G_SCION no verificado, producido por WS44; G_UI_READ pendiente `per_delta`, producido por WS11.

**Validaciones futuras:** prueba de anidamiento bajo intento y tarea, enlaces a fuente, apertura de evidencia en WS13 y ausencia de traducción de `completed` a aprobado/cerrado; recibo del delta de lectura y probe de Scion antes de promover.

## FUTURO

WS33.1 produce resultados vinculados; WS33.2, decisiones humanas; WS32, intentos; WS44, el probe de Scion; WS11, el recibo de lectura; WS27, la evidencia; WS13, el lector. La autorización de promoción y la aceptación del delta corresponden al humano.
