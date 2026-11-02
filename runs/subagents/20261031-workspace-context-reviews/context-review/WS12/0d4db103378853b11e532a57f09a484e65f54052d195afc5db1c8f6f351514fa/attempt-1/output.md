## REFORMULACION
**Propósito:** cerrar en `deskops` el contrato técnico de operaciones y escritura del workspace documental, publicado en `desk/drawer/plans/workspace-documental/contratos/operaciones.md`.
**Resultado:** whitelist por operación/campo/canal/actor/precondición/Git/efectos; adapter público o hueco con dueño; política de coordinador/P03, campos protegidos, fallos parciales, permisos y closeout fuera de la UI; comparación de captura directa a drawer y protoátomo; representación de la precondición de payload y mapeo de recibos por delta.
**Repo dueño:** `deskops`. Solo contrato y enlaces; no mutaciones ni actas interrepo.
**Límites:** no diseña API nueva por reflejo, no habilita mutaciones, no crea actas, no fija ahora el umbral de timeout, no fuerza CAS/hash ni cierra `G_UI_WRITE`/`G_SLDB_WRITE`.

## AMBIGUEDADES
1. **Consumo de WS08 no declarado.** Cita: «depends_on: - WS11 - WS08» y «Contrastar inventarios WS02–04 y contrato WS11». Ni `scope` ni `acceptance` indican qué tomar de los user-flows. Obliga a inventar si la whitelist debe cubrir todas las operaciones de UF01–UF10 o solo las inventariadas, y si WS08 es prerrequisito real o sobra.

## DRY-RUN
Nodo de planificación, no agregado: produce un documento, no código.
**Lecturas:** `dag.yaml`, guía, brief, alcance, decisiones, cobertura; salidas de WS11 y WS08; auditorías WS02–04; código citado de `sldb.api.create_document`, `DrawerService`, `/save`, `expected`, `version`/`content_hash`, closeout y `advance`.
**Cambios:** crear/actualizar `contratos/operaciones.md` con matriz de capacidades/efectos, whitelist, adapter, precondición, política de coordinador, captura, huecos y enlaces; sin código.
**Dependencias/gates:** consume WS11/WS08 y `G_WRITE_POLICY` satisfecho; no consume `G_UI_WRITE`/`G_SLDB_WRITE`; `G_WRITE_CONTRACT` queda pendiente/per_delta y no se marca aceptado.
**Errores:** falta WS11/WS08 → detener y registrar hueco con dueño; API o prueba no citada → marcar faltante, no inventar; composición de captura sin origen/tarea/colisiones → registrar productor WS46; campo protegido no definido → hueco a WS02/modelo; precondición no justificable → elegir y dejar verificación a WS45.
**Validación:** revisión del contrato con path/símbolo/commit, matriz de huecos asignados, mapeo de recibos, ausencia de mutaciones/actas y secciones para WS48.

## FUTURO
WS45 verifica la precondición; WS46 prueba la captura; WS47 la guarda de contenido; WS48 la admisión en modo manual exclusivo; P01/receptor emite actas `G_UI_WRITE`/`G_SLDB_WRITE` por delta. WS34.1/2 requieren la política/umbral de timeout y se detienen si falta. WS21 queda bloqueado por `G_PAYLOAD_PRECONDITION`; WS19, WS25, WS26, WS28, WS32, WS39 y WS42 consumen el contrato.
