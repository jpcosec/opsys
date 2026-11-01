REFORMULACION  
Propósito: cerrar el contrato técnico de operaciones y escritura del workspace documental: whitelist lectura/mutación por operación/campo/modelo/canal/actor, adapter público, política de coordinador/Git/campos protegidos, precondición, locks, fallos parciales, permisos y closeout fuera del servidor UI. Resultado: `contratos/operaciones.md` y enlaces en deskops, con matriz de capacidades/efectos y huecos asignados. Repo dueño: deskops. Límites: solo contrato y enlaces; no ejecutar mutaciones, no crear API/modelo por reflejo, no escribir actas interrepo ni habilitar funciones; closeout depende de G_CLOSEOUT; raw-source de WS20/G_SOURCE; precondición de payload de WS45/G_PAYLOAD_PRECONDITION; recibos de P01 por delta.

AMBIGUEDADES  
ninguna

DRY-RUN  
Lecturas: contrato WS11, user-flows WS08, inventarios WS02–04, decisiones/gates, APIs/CLI y pruebas existentes de SLDB/Deskops; citar path/símbolo/commit. Cambios previstos: redactar whitelist y matriz, clasificar cada capacidad como comprobada/faltante con productor, fijar adapter y representación de precondición, mapear deltas a recibos. Dependencias: WS11, WS08 y G_WRITE_POLICY satisfecho; consumidores WS19/20/25/26/28/32/34/39/42/45. Validaciones futuras: revisión del contrato, G_WRITE_CONTRACT por delta, pruebas de WS45 y WS20, recibos G_UI_WRITE/G_SLDB_WRITE.

FUTURO  
WS45 verifica/completa la precondición de payload; WS20 produce G_SOURCE; P01 emite actas por delta en repos receptores; si la composición existente no preserva origen, no crea tarea activa o no controla colisiones, queda registrado un productor Deskops antes de WS25.2; WS34 opera dispatch/reply bajo G_EXEC/G_SCION; el TaskDoc de promoción fija archivos, pruebas y textos.
