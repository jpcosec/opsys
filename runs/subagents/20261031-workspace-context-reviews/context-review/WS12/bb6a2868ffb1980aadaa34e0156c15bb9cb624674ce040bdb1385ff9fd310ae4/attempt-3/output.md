REFORMULACION
WS12 es un nodo `planning` en `deskops` que cierra el contrato de operaciones y escritura en `contratos/operaciones.md`. Debe fijar la whitelist de lectura/mutación por campo/modelo/operación/canal/actor/revisión/Git/efectos, la representación de la precondición, el adapter público existente, campos protegidos, captura a drawer/protoátomo, política y umbral de timeout del ramal E, mapa de recibos/pruebas por delta y huecos con dueño. Resultado: contrato y enlaces en `deskops`, con matriz de capacidades/efectos y estado comprobado/faltante. Límites: solo escribe contrato y enlaces; no ejecuta mutaciones, no crea actas interrepo, no inventa API/modelo ni habilita funciones; respeta P03/P05/P06 y los gates por delta.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería `dag.yaml`, esta guía, decisiones/owner-decisions, inventarios WS02–04, contrato WS11, user-flows WS08 y el repo `deskops` para citar APIs/servicios/documentos existentes. Cambios previstos: redactar `contratos/operaciones.md` con tablas de whitelist y efectos, adapter y huecos, precondición elegida y justificada, captura drawer/protoátomo, sección del ramal E y matriz de capacidades; enlazar evidencia `path`/símbolo/commit y mapear G_WRITE_CONTRACT/G_UI_WRITE/G_SLDB_WRITE por ID/efecto. Dependencias: G_WRITE_POLICY satisfecho, WS11 y WS08; si falta inventario, API o evidencia, registrar hueco con dueño, sin sustituirlo. Para el ramal E no fijar el umbral ahora: dejar la sección y remitir a la preparación de WS34.1/WS34.2. Errores esperados: evidencia no citable, ausencia de WS11 o inventario, intento de crear API/modelo; detener y registrar. Validación: contrato sin mutaciones ni actas, cada operación con canal/actor/revisión/efectos/estado, huecos asignados, recibos por delta y cierre núcleo L/M posible sin habilitar mutaciones. Es nodo `delivery`, no agregado.

FUTURO
WS45 verifica o completa la precondición de payload y G_PAYLOAD_PRECONDITION; WS20 produce G_SOURCE; el receptor P01 emite actas por delta; la preparación de WS34.1/WS34.2 fija el umbral de timeout; los nodos consumidores aplican el contrato.
