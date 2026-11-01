## REFORMULACION

**Propósito:** integrar en el workspace de graph_ui la alternancia fuente/renderizado según `source_mode=editable`, con mismo origen, revisión y buffer sucio; el guardado usa solo la API fuente autorizada; una composición escribe únicamente en el documento dueño de cada campo o queda declarada de solo lectura.

**Resultado:** delta en `frontends/mindmap/views/workspace/` y `tests/` de graph_ui.

**Repo dueño:** graph_ui.

**Límites:** solo la variante editable fijada por P04; no implementa el guardado fuente (WS20) ni define el contrato de operaciones (WS12); no convierte la composición en escritura sin soporte; no hace commit ni cierre; no activa la variante read_only.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura, reconciliación y fragmentos de `dag.yaml` de WS21, WS19, WS20 y gates. Los bloques de vecinos se tratan como contratos, no se revisan.
- **Cambios previstos:** en graph_ui, alternancia fuente/render dentro de `views/workspace/`, conservación de buffer sucio con confirmación y consumo de la API de guardado autorizada; pruebas en `tests/`.
- **Dependencias:** WS19 (agregado de edición de campos/conflicto) y, por la variante editable, WS20. Gates: `G_SOURCE`, `G_WRITE_CONTRACT`, `G_PAYLOAD_PRECONDITION` y `G_UI_WRITE`; los pendientes son intencionales.
- **Validaciones futuras:** edición/conflicto/roundtrip real, campos protegidos, buffer conservado al alternar, composición con origen dueño o declaración read-only, y recepción por delta. Todo sin ejecutar.

## FUTURO

- WS12 debe producir el contrato de operaciones y composición que WS21 consume.
- WS20 produce `G_SOURCE` y la API reversible de guardado fuente.
- WS45 produce `G_PAYLOAD_PRECONDITION` para guardado por campos.
- El receptor P01 emite las actas por delta de `G_UI_WRITE` y `G_WRITE_CONTRACT`.
- WS30 realizará la validación humana del manual y la autoría; P04 ya está decidido y no se repite.
