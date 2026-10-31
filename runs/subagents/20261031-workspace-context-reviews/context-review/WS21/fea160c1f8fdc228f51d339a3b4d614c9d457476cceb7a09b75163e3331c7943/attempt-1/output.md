## REFORMULACION
Propósito: integrar en el workspace la alternancia fuente/render con el mismo origen, revisión y dirty buffer, usando el guardado fuente autorizado y escribiendo composición solo sobre origen trazable soportado. Resultado: delta de UI en graph_ui, ejecutando solo la variante que elija P04. Repo dueño: graph_ui (`output_scope: frontends/mindmap/views/workspace/; tests/`). Límites: `pending` bloquea preparación; en `read_only` no se exige G_SOURCE y no se declara edición fuente; promoción no autorizada; no duplicar ticket.

## AMBIGUEDADES
1. Semántica de los variants. El bloque base declara `depends_on: - WS19` y `requires: - G_UI_WRITE - G_WRITE_CONTRACT`, mientras la variante `read_only` declara `depends_on: []` y `requires: []`. No se dice si la variante sustituye o suma. Si sustituye, `read_only` perdería WS19 y los gates pese a su aceptación «edición por campos probada»; si suma, las listas vacías no significan nada. Obliga a inventar la regla de combinación.
2. «Composición escribe solo origen trazable soportado.» No se define «composición» ni qué es «soportado», y la aceptación solo menciona «edición/conflicto/roundtrip» y campos. Obliga a inventar si composición entra en alcance y cómo se comprueba.

## DRY-RUN
Lecturas: guía, `dag.yaml` (WS21, WS19, WS20, WS30 y gates), brief, alcance, decisiones, cobertura y reconciliación. Cambios previstos: ninguno; esta revisión no modifica archivos. Dependencias: WS19 agregado (WS19.1/19.2); G_UI_WRITE y G_WRITE_CONTRACT pendientes de WS12; en `editable`, WS20 y G_SOURCE; P04/WS07 selecciona `source_mode`. Validaciones futuras: preflight de promoción; prueba de roundtrip/conflicto y campos protegidos en `editable`; fuente read-only y edición por campos en `read_only`; aceptación manual WS30; cierre de gates.

## FUTURO
El humano/WS07 resuelve P04 y designa actores; WS12 produce G_UI_WRITE y G_WRITE_CONTRACT; WS20 produce G_SOURCE si `editable`; WS19 cierra la edición de campos; WS30 registra la validación humana. Nada de esto es ambigüedad de WS21.
