# Executor comparison — WS34.1, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
**Propósito:** encargo de implementación de un adaptador público restringido para *dispatch* Scion en `deskops`, con confirmación entendida como respuesta de la API de Scion, identidad de intento, timeout/errores y autoridad del coordinador según el contrato WS12.

**Resultado:** adaptador en `runtime/`, comando `cli/commands/runtime.py` o la API que fije WS12, y pruebas en `tests/`. Sin shell arbitrario ni duplicación de transporte.

**Repo dueño:** `deskops`. Depende de WS33 —vínculos de mensajes/resultados/decisiones— y WS12 —contrato de operaciones—. Requiere G_EXEC, G_SCION y G_WRITE_CONTRACT. Estimación M.

**Límites:** no ejecutar en planificación; promoción no autorizada; la aceptación exige agente real con un dispatch aceptado y otro rechazado o vencido por timeout. Los gates pendientes son intencionales.

##

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
