REFORMULACION
WS12 es un nodo de planificación en deskops: cerrar el contrato de operaciones y escritura. Debe producir `contratos/operaciones.md` con whitelist de lectura/mutación por campo/modelo/operación/canal/actor, política de coordinador/Git/campos protegidos, precondición/locks, fallos parciales, permisos y closeout fuera de la UI, más matriz de efectos y huecos. No ejecuta mutaciones ni crea actas interrepo; solo contrato y enlaces. Depende de WS11/WS08; `G_WRITE_POLICY` ya está satisfecho.

AMBIGUEDADES
1. “WS12 define la representación de la precondición … distinguiendo before-image … token … y comparación o escritura pública con precondición compartida (aún no probada); no fuerza CAS…”. Falta criterio para adoptar una representación; WS45 solo verifica “lo que fije WS12”. Obligaría a inventar la elección técnica.
2. “receptor P01 registra acta en su repo al preparar ese delta”. P01 solo cubre graph_ui/SLDB/spec2viz, pero `G_WRITE_CONTRACT` incluye deltas deskops (WS32, WS34…). Obligaría a inventar receptor/acta para deskops.
3. “Solo si falta conducta de workflow se registra un productor Deskops explícito antes de WS25.2; si esa composición de llamadas cumple…”. No define “conducta de workflow” ni criterio de “cumple”; obligaría a inventar el umbral para elegir API existente o productor nuevo.

DRY-RUN
Lecturas: dag/WS12, brief, alcance, decisiones, cobertura, WS11/WS08 y auditorías WS02–04 citadas; inventarios de API SLDB/DrawerService y evidencia de precondición. Cambios: solo `contratos/operaciones.md` y enlaces en deskops; ninguna mutación. Dependencias: WS11/WS08; `G_WRITE_POLICY` satisfecho; `G_SOURCE`, `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE` y `G_SLDB_WRITE` son por delta. Validaciones: citas path/símbolo/commit, estado comprobado/faltante, productores asignados y recibos mapeados sin declararlos aceptados.

FUTURO
WS45 verificará/completará la precondición de payload; WS20 producirá raw-source/`G_SOURCE`; P01 y receptores emitirán actas por delta; WS25.2/WS19/WS21 consumirán el contrato. La aceptación por delta y cualquier decisión de producto quedan en humano/receptor, no en WS12.
