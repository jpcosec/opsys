## REFORMULACION

WS12 es un encargo de planificación en `deskops`: cerrar el contrato de operaciones y escritura en `contratos/operaciones.md`, publicando whitelist por operación/campo/canal/actor/revisión/Git/efectos, comparación del adapter público existente, política de coordinador/Git/campos protegidos/precondición/locks/fallos/permisos/closeout, y matriz de capacidades, efectos y huecos con dueño. Depende de WS11 y WS08; G_WRITE_POLICY ya está satisfecho. Límites: solo contrato y enlaces en deskops; no mutaciones, actas interrepo, APIs/modelos nuevos ni aprobación de captura; P03 no cambia; el núcleo L/M cierra sin la sección de timeout del ramal E.

## AMBIGUEDADES

ninguna.

## DRY-RUN

Un ejecutor futuro leería `contratos/navegacion.md` de WS11, `borradores/user-flows.md` de WS08, auditorías WS02–04, `dag.yaml` y G_WRITE_POLICY satisfecho. Crearía o editaría `desk/drawer/plans/workspace-documental/contratos/operaciones.md` y enlaces permitidos, con whitelist, comparación de adapter/API, política de escritura, matriz de capacidades/efectos y huecos asignados, citando path/símbolo/commit. No ejecutaría mutaciones ni escribiría actas. G_WRITE_CONTRACT queda pendiente por delta y no marcaría `accepted_scope_nodes`; no tocaría G_UI_WRITE/G_SLDB_WRITE. Errores: falta contrato WS11 o inventario → detener y registrar hueco con repo dueño; adapter ausente → hueco/dueño; conducta de workflow ausente → productor Deskops explícito antes de WS25.2; raw-source → WS20/G_SOURCE; precondición de payload → WS45/G_PAYLOAD_PRECONDITION. Validación esperada: matriz completa, evidencia real citada, sin aprobar APIs ni mutaciones, y contrato núcleo L/M cerrable.

## FUTURO

WS34.1/WS34.2 fijarán al prepararse la política, umbral de timeout y clasificación; WS45 verificará la precondición de payload; P01 y los repos receptores emitirán actas por delta; WS20 producirá G_SOURCE; WS25.2 usará el hueco/productor si falta conducta de workflow.
