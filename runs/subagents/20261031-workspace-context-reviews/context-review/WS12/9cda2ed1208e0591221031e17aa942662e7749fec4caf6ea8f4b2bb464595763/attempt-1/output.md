**REFORMULACION**  
WS12 es un nodo de planificación —no agregado— en `deskops`. Encargo: cerrar el contrato público de operaciones y escritura en `contratos/operaciones.md`: whitelist por operación/campo/modelo/canal/actor, campos protegidos, precondición de escritura, efectos/errores/Git/closeout, política de coordinador, captura a drawer/protoátomo, huecos con dueño y sección de timeout para deltas Scion. Resultado: contrato y matriz de capacidades, sin implementar, mutar, crear API/modelo/wrapper ni actas interrepo. Límites: P03 exige lectura/handoff con otro coordinador escritor; lock solo UI no basta; raw-source pertenece a WS20/G_SOURCE; precondición de payload a WS45/G_PAYLOAD_PRECONDITION; captura a WS46; no habilita mutaciones.

**AMBIGUEDADES**  
Ninguna.

**DRY-RUN**  
El ejecutor futuro leería `dag.yaml`, `contratos/navegacion.md` de WS11, `borradores/user-flows.md` de WS08, inventarios WS02–04 y código/API existente citado. Escribiría únicamente `desk/drawer/plans/workspace-documental/contratos/operaciones.md` y enlaces en deskops: matriz operación/campo/canal/actor/revisión/Git/efectos/errores, decisión justificada de precondición (`expected`, token o CAS), política coordinador, captura drawer/protoátomo, secciones de timeout de WS34.1/34.2 y huecos asignados a WS20/45/46/47/48. Consumiría `G_WRITE_POLICY` ya satisfecho y las salidas de WS11/WS08. Si falta API, contrato o evidencia, registraría hueco con dueño; no inventaría sustituto. No crearía actas ni mutaciones. Validaría que cada “comprobado” cite path/símbolo/commit o prueba real, que la matriz distinga existente/faltante, que no haya aceptación conjunta y que el cierre no requiera habilitar mutaciones. `G_WRITE_CONTRACT` quedaría evaluable por delta.

**FUTURO**  
WS45 verifica la precondición de payload; WS46 prueba/completa captura; WS47 protege contenido no declarado; WS48 aporta admisión de escritura; WS20 produce G_SOURCE. El receptor P01 emite actas por delta en graph_ui/sldb/spec2viz. WS34.1/34.2 fijarán después su umbral de timeout en la sección correspondiente. Los consumidores quedan bloqueados por sus gates hasta sus recibos.
