## REFORMULACION

**Propósito:** agrupar la entrega de edición del workspace integrado: campos con conflicto visible y relaciones permitidas, reutilizando editores/API existentes.

**Resultado:** agregado no ejecutable; queda cumplido cuando WS19.1 y WS19.2 cumplen su aceptación. No produce artefacto propio distinto de sus hijos.

**Repo dueño:** `graph_ui` (`output_base: graph_ui:repository_root/`).

**Límites:** delta sobre `a1b2b22`; no duplicar implementación ni inferir cierre por commit; sin semántica nueva de relaciones; campos workflow-protected no editables por este canal; mutaciones UI solo con `G_HUMAN_READ`, aunque desarrollo/pruebas aisladas de API pueden avanzar. Depende de WS12, WS19.1 y WS19.2.

## AMBIGUEDADES

Ninguna.

El `scope` del agregado enumera las mismas capacidades que reparten sus hijos y su `acceptance` declara que no se ejecuta; no obliga a inventar un resultado adicional. La ausencia de recibos de `G_UI_WRITE`/`G_WRITE_CONTRACT` es un gate `per_delta` pendiente, no una indefinición. WS12 tiene productor y contrato nombrados; si falta, aplica la regla común de detención.

## DRY-RUN

**Lecturas previstas:** nodo WS19 en `dag.yaml`; aristas WS12, WS19.1, WS19.2, WS21, WS42 y gates; `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`.

**Cambios previstos:** ninguno directo. WS19 es `aggregate` y no se ejecuta; el trabajo corresponde a WS19.1 (campos) y WS19.2 (relaciones).

**Dependencias:** WS12 debe publicar whitelist y contrato técnico por operación; WS19.1/WS19.2 consumen endpoints autorizados. Los gates se evalúan por delta concreto, sin aceptación conjunta. WS06 integra el delta en ticket receptor vigente o tarea atómica sin solapamiento.

**Validaciones futuras:** aceptación de cada hijo (guardar/recargar, conflicto con texto local conservado, alta/baja persistente, rechazo visible); recibos de `G_UI_WRITE` y `G_WRITE_CONTRACT` para los IDs correspondientes; acta `G_HUMAN_READ` antes de habilitar mutaciones UI; comprobación de no duplicar la base existente.

## FUTURO

- **WS12:** contrato técnico y whitelist por campo/operación; recibos por delta.
- **WS19.1/WS19.2:** implementación y pruebas en `graph_ui`.
- **WS16:** acta humana de lectura.
- **Solicitante humano:** aceptación de deltas y actas en repo receptor.
- **WS06:** reconciliación/promoción contra Board y ticket receptor.
- **WS21/WS42:** consumidores posteriores; no forman parte de este encargo.
