**REFORMULACION**
WS21 es un nodo `implementation` de `graph_ui`, no agregado. Propósito: integrar en `frontends/mindmap/views/workspace/` y `tests/` la alternancia fuente/render bajo `source_mode=editable` (P04). Resultado: mismo origen, buffer sucio conservado con confirmación explícita antes de descartarlo, guardado fuente autorizado y guardado por campos con precondición; la composición escribe solo en el documento dueño o queda read-only declarada. Límites: no implementa otros repos, no crea API fuente, ejecuta solo la variante elegida y depende de WS19, WS20, WS12 y gates.

**AMBIGUEDADES**
1. «Alternar fuente/render con mismo origen, revisión y dirty buffer»: «revisión» no se asigna explícitamente a `G_PAYLOAD_PRECONDITION` ni a `G_SOURCE`; obligaría a inventar qué precondición gobierna la alternancia y si hay una o dos revisiones.

**DRY-RUN**
Un ejecutor futuro leería WS21, `source_mode=editable`, variantes, WS19, WS20, WS12, `G_SOURCE`, `G_PAYLOAD_PRECONDITION`, `G_WRITE_CONTRACT`, `G_UI_WRITE`, brief/alcance y `editing`. Cambios previstos: en `views/workspace/`, conmutador fuente/render con foco y buffer; al cambiar, conservar buffer y pedir confirmación; guardar fuente vía API autorizada de WS20 y campos con precondición; resolver composición por documento dueño; fallback read-only. Pruebas en `tests/`: roundtrip, conflicto, campos protegidos, buffer/confirmación y composición. Consume WS19 como base de edición, WS20 como productor de API/G_SOURCE y WS45 del gate de payload. Validación futura: gates y recibo por delta; si falta contrato, API o gate, detenerse, registrar hueco con repo dueño y no sustituir. Sin ejecutar.

**FUTURO**
WS20 produce API/G_SOURCE; WS45 produce `G_PAYLOAD_PRECONDITION`; WS12 produce `G_WRITE_CONTRACT`; el receptor P01 emite `G_UI_WRITE` por delta; WS30 etiqueta el alcance. La confirmación de descarte corresponde al humano en uso, no a esta revisión.
