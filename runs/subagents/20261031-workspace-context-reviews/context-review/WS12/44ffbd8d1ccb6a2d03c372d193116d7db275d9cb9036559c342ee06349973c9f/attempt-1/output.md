REFORMULACION
Propósito: cerrar el contrato de operaciones y escritura que la UI invocará sobre Deskops/SLDB. Resultado: `contratos/operaciones.md` en deskops con whitelist lectura/mutación por operación/campo/canal/actor/revisión/Git/efectos, adapter público existente o hueco con dueño, estado comprobado/faltante, mapa recibo/prueba por delta, matriz de capacidades/efectos y enlaces a recibos. Repo: deskops. Límites: solo escribe contrato y enlaces; no ejecuta mutaciones, no crea actas interrepo, no diseña adapters ni listas universales, no habilita mutaciones ni aprueba API/Scion.

AMBIGUEDADES
1. «policy coordinador, Git, workflow-protected fields, CAS/locks, fallos parciales, permisos y closeout fuera del servidor UI». Obligaría a inventar qué constituye un «fallo parcial», su granularidad y su reflejo en efectos/errores, porque la aceptación exige whitelist y matriz, pero no concreta ese comportamiento.

DRY-RUN
Lecturas: `dag.yaml` (WS12, WS11/WS08 y gates), `decisiones.md`, `brief.md`, `alcance.md`, `cobertura.md`, auditorías WS02–04 y contrato WS11. Cambios previstos: redactar/actualizar `deskops:desk/drawer/plans/workspace-documental/contratos/operaciones.md` y enlaces; sin mutaciones ni actas. Dependencias: WS11 y WS08; G_WRITE_POLICY ya satisfecho; inventarios WS02–04 transitivos; G_WRITE_CONTRACT, G_UI_WRITE y G_SLDB_WRITE por delta; G_CLOSEOUT para autoría/cierre; WS20 como productor de raw-source/G_SOURCE. Validaciones futuras: citar path/símbolo/commit y evidencia real de API/prueba; contrastar inventarios; comprobar whitelist por operación/campo y matriz de efectos; verificar adapter existente o hueco asignado; confirmar que no se habilita ninguna mutación.

FUTURO
P01 produce las actas por delta en el repo dueño al preparar/promover cada uno; WS20 produce la API/G_SOURCE o registra su hueco; WS21 queda bloqueado por G_SOURCE. Los recibos G_WRITE_CONTRACT/G_UI_WRITE/G_SLDB_WRITE llegan por delta, no conjuntamente. G_HUMAN_READ habilita el uso de mutaciones en UI; G_CLOSEOUT cubre autoría/cierre; G_SCION/G_EXEC quedan fuera. El TaskDoc de promoción fija archivos, escenarios y textos.
