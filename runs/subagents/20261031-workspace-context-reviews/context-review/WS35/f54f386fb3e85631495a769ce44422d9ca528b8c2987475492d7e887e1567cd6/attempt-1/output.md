## REFORMULACION

**Propósito:** que el workspace muestre la ejecución y trazabilidad de una tarea: tarea de deskops, intento, conversación, resultados y decisiones, en solo lectura.

**Resultado:** vista en `frontends/mindmap/views/workspace/execution/` con tests; cada mensaje, resultado y decisión se agrupa bajo su intento y tarea, enlaza a su fuente y la evidencia abre en el lector WS13; `completed` no se presenta como aprobado/cerrado.

**Repo dueño:** `graph_ui`.

**Límites:** no hay mutación, aprobación ni cierre; depende de WS33 (agregado de vínculos) y WS27 (evidencia), con gates `G_SCION` y `G_UI_READ` aún no satisfechos. La promoción no está autorizada.

## AMBIGUEDADES

1. «Cada mensaje, resultado y decisión se muestra bajo su intento y tarea»: no define qué hacer con mensajes o resultados sin intento/tarea vinculada. Obligaría a inventar si se ocultan, se agrupan aparte o se muestran como error.
2. «la evidencia abre en el lector (WS13)»: no define el comportamiento si la evidencia no es un documento legible por WS13 (por ejemplo, un diff o artefacto). Obligaría a inventar una representación o fallback no previsto.

## DRY-RUN

**Lecturas:** nodo WS35 y aristas WS33/WS27/WS36 en `dag.yaml`; gates `G_SCION` y `G_UI_READ`; guía, brief, alcance, decisiones y cobertura. No existe todavía `task-ws35.md`.

**Cambios previstos:** crear la vista de ejecución y sus tests dentro de `output_scope`, sin tocar otros nodos.

**Dependencias:** WS33 aporta referencias y deduplicación; WS27 aporta diff/evidencia; WS13 llega vía WS27. `G_SCION` debe producirlo WS44 y `G_UI_READ` aceptarlo WS11.

**Validaciones futuras:** tests de aceptación, comprobación de agrupación y enlaces, apertura de evidencia en WS13, revisión de promoción y consumo posterior por WS36.

## FUTURO

WS44 produce `G_SCION`; WS11 resuelve `G_UI_READ`; WS07 designa al operador Scion; un humano autoriza la promoción y el TaskDoc; WS36 integrará dispatch/reply sobre esta vista. Las propuestas Pxx no se resuelven en esta revisión.
