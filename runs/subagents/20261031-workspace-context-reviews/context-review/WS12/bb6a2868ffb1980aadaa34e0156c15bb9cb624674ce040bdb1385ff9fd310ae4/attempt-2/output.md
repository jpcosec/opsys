REFORMULACION  
Propósito: cerrar el contrato técnico de operaciones y escritura del workspace documental. Resultado: `contratos/operaciones.md` con whitelist, adaptador, políticas, deltas, efectos y huecos asignados. Repo dueño: `deskops` (`desk/drawer/plans/workspace-documental/`). Límites: solo contrato y enlaces; no implementa mutaciones, APIs, modelos ni actas interrepo; depende de WS11/WS08 y de G_WRITE_POLICY.

AMBIGUEDADES  
ninguna.

DRY-RUN  
El ejecutor futuro leería `dag.yaml` (WS12), el contrato WS11, el borrador WS08, las auditorías WS02–04 por dependencia transitiva y las decisiones P03–P06. Crearía o actualizaría `deskops:desk/drawer/plans/workspace-documental/contratos/operaciones.md`, sin tocar APIs, modelos, actas ni repos remotos. Incluiría: matriz por operación/campo/modelo/canal/actor/precondición/Git/efectos/estado existente comprobado o faltante; adaptador público por operación; política de coordinador, campos protegidos, locks, fallos parciales y closeout fuera del servidor UI; comparación de captura directa a drawer y protoátomo; y mapa de cada delta a recibo/prueba. Consumiría G_WRITE_POLICY ya satisfecho y citaría paths/símbolos/commits y pruebas reales. Si falta API o contrato, registraría hueco con dueño y operación no disponible; si falla la conducta de drawer, productor Deskops explícito antes de WS25.2; raw-source en WS20/G_SOURCE; precondición de payload en WS45/G_PAYLOAD_PRECONDITION. No elegiría umbral de timeout: documentaría clasificación y dejaría la duración a la sección que se fije al preparar WS34.1/WS34.2. Validación esperada: contrato revisable, sin mutaciones, cada capacidad con evidencia real o hueco asignado, P03 intacto y G_WRITE_CONTRACT actualizado por delta solo con evidencia.

FUTURO  
WS45 inventariará y probará la precondición de payload; WS20 producirá raw-source; P01/receptor emitirá actas por delta en graph_ui, sldb y spec2viz; WS25.2, WS26, WS28 y WS34 consumirán las cláusulas del contrato; WS21 seguirá bloqueado por G_PAYLOAD_PRECONDITION y, en variante editable, G_SOURCE.
