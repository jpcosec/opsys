**REFORMULACION**
El nodo WS08 pide, en el repo dueño `deskops`, actualizar `borradores/user-flows.md` para que UF01–UF10 queden como encargo de planificación: entrada/salida, operaciones reales de auditorías WS02–04, errores, nodos del DAG y gates humanos, marcando huecos sin inventar. Límites: no implementa ni valida producto; UF08 es solo lectura y sin envío interdesk; delegación condicionada a G_SCION/G_EXEC sin habilitarla; ack local pendiente de WS12; no promete funciones fuera de alcance. Depende de WS07 y G_PRODUCT.

**AMBIGUEDADES**
1. «cubrir manual, captura, revisión, cambios (UF07/WS29), arranque, multidesk, schemas y modo degradado» frente a `output_scope: borradores/user-flows.md` y una aceptación centrada en UF01–UF10. No queda claro si «manual» es la operación manual cubierta por las UF o un entregable de manual aparte; obligaría a decidir si se añade contenido de manual a `user-flows.md` o se omite.
2. «Cada UF tiene entrada/salida, operación, error, nodo y gate humano» junto a «Una operación ausente se marca hueco, sin inventarla». Si falta la operación, no se especifica qué poner en `error` (¿hueco, «no definido», error esperado?); obligaría a inventar el criterio.

**DRY-RUN**
No es agregado. Lectura: dag.yaml, brief, alcance, decisiones, cobertura, validación humana, `borradores/user-flows.md`, auditorías `deskops/infraestructura/ui` y contratos disponibles. Cambio previsto: editar solo `borradores/user-flows.md`; por cada UF ajustar entrada, salida, operación(es), error, nodo(s) y gate humano; listar operaciones ausentes como hueco con dueño; UF08 lectura; delegación marcada condicionada. Dependencias: G_PRODUCT satisfecho vía WS07; auditorías por WS06/WS07; ack local pendiente de WS12. Validación futura: completitud UF01–UF10, no prometer fuera de alcance, listas completas de operación/nodo/gate y distinción entre WS29 y gates humanos. Errores: faltante de auditoría/contrato se registra como hueco, sin sustituirlo; no se ejecutan pruebas ni se mutan otros repos.

**FUTURO**
WS08 produce el borrador revisado; WS09/WS11/WS12 consumen operaciones, errores y gates; WS16/30/37/39 validan uso; WS29 prueba técnica propia; un humano decide la aceptación de gates. WS12 confirmará ack local y operaciones; WS40 aporta el corpus para validaciones.
