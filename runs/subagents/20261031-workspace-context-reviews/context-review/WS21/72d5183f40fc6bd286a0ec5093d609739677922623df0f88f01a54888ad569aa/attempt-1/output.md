## REFORMULACION
WS21 es un encargo de planificación para integrar fuente y renderizado en el workspace según `source_mode`. El resultado esperado es un nodo ejecutable solo tras elegir variante, con alcance delimitado, repo dueño y aceptación comprobable. Repo: `graph_ui`; salidas en `frontends/mindmap/views/workspace/` y `tests/`. Límites: depende de WS19; con `source_mode: pending` no se prepara ni promueve; no reviso los bloques edge vecinos ni ejecuto nada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
- Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación, parámetros del DAG, nodo WS21, gates y edges de contexto.
- Cambios previstos: ninguno en repositorios; solo este informe de revisión.
- Dependencias: WS19 como prerrequisito; WS20 solo en variante `editable`; `G_UI_WRITE` y `G_WRITE_CONTRACT` en base; `G_SOURCE` solo en `editable`.
- Validaciones futuras: resolución de P04/WS07, contrato WS12, API reversible WS20 y pruebas de edición, conflicto, roundtrip y conservación de buffer; validación manual WS30. No ejecutadas.

## FUTURO
El humano o WS07 decide `source_mode` y designa actores; WS12 produce `G_UI_WRITE` y `G_WRITE_CONTRACT`; WS20 produce `G_SOURCE` si aplica; WS30 valida manualmente; WS40 aporta corpus. Son dependencias y decisiones previstas, no ambigüedades de WS21.
