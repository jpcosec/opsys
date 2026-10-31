## REFORMULACION
**Propósito:** comprobar mediante un probe read-only real que la API pública de Scion y el acceso del operador permiten las capacidades e identidad necesarias para intento y mensajes, y registrar evidencia para G_SCION.
**Resultado:** `auditoria/scion-probe.md` con actor, fecha, Hub/endpoint, identidad y capabilities; G_SCION satisfecho o WS44 bloqueada.
**Repo:** `deskops`.
**Límites:** no crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos; sin API o acceso no se cierra ni se avanza WS32.

## AMBIGUEDADES
1. «Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33.» WS05 produce ese inventario, pero su contrato solo obliga a señalar «capacidades que requieren API real», no a mapearlas como requeridas por WS32/WS33. Si faltan, WS44 tendría que inventar qué capabilities probar y para qué nodo.
2. «El solicitante registra en WS07 qué acceso read-only tiene el operador.» WS07 exige designar identidad/fecha del operador y declara que «no concede permiso G_EXEC», pero no obliga a registrar el nivel de acceso read-only. WS44 tendría que inventar si el acceso está autorizado y con qué alcance.
3. «verifica capacidades/identidad necesarias para intento y mensajes» / «identidad/fecha/capabilities y actor registrados». No se define si «identidad» es la del operador, el Hub/tenant, el agente remitente o el principal de API; el ejecutor tendría que elegir cuál evidenciar.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (nodo y gates), `auditoria/scion.md` de WS05, `decisiones.md` de WS07, configuración Scion sin secretos y API pública documentada. Sin probe vivo.
**Cambios previstos:** crear `auditoria/scion-probe.md`; registrar actor, fecha, Hub, endpoint, identidad y capabilities; actualizar el recibo de G_SCION si procede; invalidar recibo previo ante cambio de Hub/API/credencial.
**Dependencias:** WS05 (inventario) y WS07 (G_PRODUCT, operador y acceso). WS32/WS33 consumen G_SCION.
**Validaciones futuras:** respuesta pública real no simulada; contraste de capabilities con el inventario; revisión humana del recibo; repetición tras cambio.

## FUTURO
WS07 registra operador y acceso; WS05 entrega `auditoria/scion.md`; el operador humano ejecuta el probe y firma la evidencia; WS32/WS33 consumen G_SCION; un humano decide la invalidación por cambio de Hub o credencial.
