REFORMULACION
Propósito: revisar si WS25.2 se entiende como encargo de planificación. Resultado: nodo de captura en drawer/protoátomo, owner `graph_ui`, salida acotada a `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. Límites: no evalúo producto, no ejecuto, no reviso contratos vecinos ni resuelvo Pxx; la promoción sigue no autorizada.

AMBIGUEDADES
1. «Captura interna de drawer/protoátomo mediante operaciones permitidas por contrato»: «protoátomo» no está definido en las fuentes suministradas e «interna» no aclara si la captura ocurre dentro del drawer, dentro del protoátomo o en la UI. Obligaría a inventar cuál es el artefacto destino y qué hace «interna».
2. «una captura persiste tras recargar con origen»: «origen» no define campo, valor ni formato comprobable —documento, nodo, usuario u otro—. Obligaría a inventar qué dato debe persistirse y cómo verificarlo en la recarga.

DRY-RUN
Lecturas previstas: contrato/whitelist de WS12, acta de WS16, evidencia de `G_UI_WRITE`/`G_WRITE_CONTRACT` y `task-ws25-2.md`. Cambios previstos: UI de captura en la ruta de `output_scope` y pruebas; llamadas solo a endpoints autorizados; persistencia con origen y sin tarea implícita. Dependencias: WS12 y WS16; gates pendientes. Validaciones futuras: recarga real, origen conservado, ausencia de tarea implícita y permisos del contrato aplicados. Sin ejecución.

FUTURO
WS12 produce contrato/whitelist y acepta los deltas de `G_UI_WRITE` y `G_WRITE_CONTRACT`; WS16 produce `G_HUMAN_READ`; WS07 designa al responsable de `graph_ui`. La promoción requiere preflight, task receptora y autorización humana; no es ambigüedad de este nodo.
