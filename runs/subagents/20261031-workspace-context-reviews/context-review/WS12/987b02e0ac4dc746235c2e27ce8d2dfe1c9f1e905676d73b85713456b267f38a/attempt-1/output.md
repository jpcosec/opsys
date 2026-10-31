REFORMULACION
- Propósito: cerrar el contrato de operaciones y escritura de WS12: whitelist de lectura/mutación por campo/modelo, adapter público CLI/API, políticas de coordinador, Git, campos protegidos, CAS/locks, fallos parciales, permisos y closeout fuera del servidor UI; registrar capabilities para los nodos consumidores.
- Resultado: `contratos/operaciones.md` y `G_WRITE_CONTRACT`; `G_UI_WRITE` y, si `source_mode=editable`, `G_SLDB_WRITE`.
- Repo: `deskops`.
- Límites: no diseñar un adapter ausente; no implementar WS20; no asumir que el lock UI protege escritores CLI; toda operación sin contrato queda no disponible; autoría/cierre bloqueados por `G_CLOSEOUT`; promoción no autorizada; depende de WS11/WS08 y `G_WRITE_POLICY`.

AMBIGUEDADES
Ninguna.

DRY-RUN
- Lecturas: nodo WS12, WS11 y WS08; gates `G_WRITE_POLICY`, `G_WRITE_CONTRACT`, `G_UI_WRITE`, `G_SLDB_WRITE`, `G_CLOSEOUT`, `G_SOURCE`; `parameters.source_mode`; decisiones P03–P06 y P04; `alcance.md`, `brief.md`, `cobertura.md`; auditoría de deskops vía WS06/07 y modelo/CLI del repo `deskops`.
- Cambios previstos: redactar `contratos/operaciones.md`; no hay cambios de código. Las actas de aceptación de graph_ui y, si aplica, sldb son evidencia de gates, no implementación.
- Dependencias: `G_WRITE_POLICY` resuelto por WS07; WS11/WS08 cerrados; `source_mode` resuelto antes de WS12 por vía transitiva de `G_PRODUCT`; responsables de graph_ui/sldb designados por P01/WS07. `G_CLOSEOUT`, `G_SOURCE` y `G_SCION` pueden dejar operaciones declaradas no disponibles.
- Validaciones futuras: `G_WRITE_POLICY` verificado; capabilities con operación/canal/efectos para los consumidores listados; clasificación de APIs existentes/comprobadas o faltantes; aceptación del delta en graph_ui y, solo si editable, en sldb; ninguna operación sin contrato se anuncia disponible; no se presume lock UI compartido.

FUTURO
WS07 decide P03–P06/P01/P04 y designa responsables; WS20 produce `G_SOURCE` y la capacidad raw-source; WS44/`G_SCION` confirman la API Scion; el cierre externo produce `G_CLOSEOUT`; graph_ui y sldb aceptan sus deltas; el TaskDoc de promoción fija archivos y pruebas. Nada de esto es ambigüedad del nodo.
