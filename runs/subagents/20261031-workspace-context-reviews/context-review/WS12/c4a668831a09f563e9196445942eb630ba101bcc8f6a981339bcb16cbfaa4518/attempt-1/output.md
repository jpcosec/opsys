REFORMULACION
Propósito: cerrar el contrato de operaciones y escritura de WS12, con whitelist por campo/modelo/operación, canal/actor, política de coordinador, Git, campos protegidos, precondición, locks, fallos parciales, permisos y closeout fuera de la UI. Resultado: `contratos/operaciones.md` y enlaces en deskops, más matriz de capacidades/efectos y huecos asignados. Repo dueño: deskops. Límites: solo planificación y contrato; no ejecuta mutaciones, no crea actas interrepo, no diseña APIs sustitutas, no aprueba Scion ni promoción.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: `dag.yaml` (WS12 y aristas), guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, auditorías WS02–04, contrato WS11 e inventarios/código citables de deskops/sldb. Cambios previstos: redactar/actualizar `contratos/operaciones.md` y enlaces en deskops; ningún cambio de código ni mutación. Dependencias: WS11 y WS08, con WS02–07 transitivas; `G_WRITE_POLICY` ya satisfecho por WS07. Validaciones futuras: revisar que la whitelist cubra operaciones/campos/canales/actores/efectos, cite path/símbolo/commit, distinga before-image/token/CAS, mapee recibos por delta y registre huecos con productor. No se ejecutará nada.

FUTURO
WS45 producirá la verificación de la precondición de payload y `G_PAYLOAD_PRECONDITION`. WS20 producirá raw-source y `G_SOURCE`. El receptor humano P01 emitirá actas por delta en el repo dueño para `G_SLDB_WRITE`, `G_UI_WRITE` y `G_WRITE_CONTRACT`; WS12 solo enlaza. Los nodos consumidores (WS19/21/25/26/28/32/34/39/42/43) usarán su propio recibo; ningún delta queda aceptado por este nodo. La promoción de WS12 sigue no autorizada y requiere TaskDoc/preflight.
