REFORMULACION
Propósito: fijar el contrato técnico de operaciones y escritura del workspace (whitelist por operación/campo/canal/actor/revisión/Git/efectos, adapter público, precondición, fallos, permisos, closeout y captura drawer). Resultado: `contratos/operaciones.md` con matriz de capacidades/efectos y huecos asignados. Repo dueño: deskops. Límites: no implementa ni ejecuta mutaciones, no crea actas interrepo, no aprueba API/modelo por reflejo, no habilita Scion, no sustituye WS20/WS45 y no fija la duración del timeout.

AMBIGUEDADES
ninguna. Las decisiones abiertas tienen criterio, productor o regla de hueco; los recibos y duraciones son trabajo futuro.

DRY-RUN
Lecturas previstas: dag.yaml y guía; brief, alcance, decisiones, cobertura; contratos WS11 y borradores WS08; auditorías WS02–04; código/API real y tests de sldb (`create_document`, DrawerService, `POST /save`) y deskops (Board/TaskDoc, `closeout verify`); owner-decisions.
Cambios previstos: crear/actualizar el contrato y sus enlaces; sin código ni actas.
Dependencias: WS11 y WS08; G_WRITE_POLICY satisfecho; G_CLOSEOUT; por delta G_SLDB_WRITE/G_UI_WRITE; productores WS20/G_SOURCE y WS45/G_PAYLOAD_PRECONDITION; P01.
Validaciones futuras: revisión de G_WRITE_CONTRACT por delta; inventario/pruebas de WS45; roundtrip/conflicto de WS20; actas P01; preflight del TaskDoc.

FUTURO
WS45 verifica/completa la precondición de payload; WS20 produce raw-source; WS34.1/WS34.2 fijan la duración del timeout al prepararse; receptores P01 emiten actas por delta; WS19/25/26/28/39/42 implementan; el TaskDoc fija archivos/pills y el humano decide aprobación de implementación/API/uso.
