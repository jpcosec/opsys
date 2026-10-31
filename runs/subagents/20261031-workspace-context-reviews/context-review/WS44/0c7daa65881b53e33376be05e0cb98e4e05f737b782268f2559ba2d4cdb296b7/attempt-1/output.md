## REFORMULACION
WS44 es un nodo de validación, `owner_repo: deskops`, cuyo propósito es comprobar mediante un probe read-only que la API pública de Scion es accesible y permite verificar identidad y capacidades necesarias para intento y mensajes. Produce `auditoria/scion-probe.md` y es el único productor de `G_SCION`. Límites explícitos: no crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos; si API o acceso faltan, permanece bloqueada y no habilita WS32. Depende de WS05, WS07 y de `G_PRODUCT`.

## AMBIGUEDADES
1. **Quién confirma el permiso de acceso read-only.** Citas: «con acceso ya autorizado»; «appoint responsible operator and confirm read-only permission before probe»; y en WS07: «no requiere configurar/ejecutar Scion ni concede permiso G_EXEC». El nodo no nombra al actor que confirma ese acceso. Obligaría a inventar si basta la designación de P01, si el operador se autoconfirma o si hace falta acta del solicitante.
2. **Qué capabilities mínimas cuentan como comprobadas para intento y mensajes.** Citas: «verifica capacidades/identidad necesarias para intento y mensajes»; «identidad/fecha/capabilities». WS05 inventaría la API, pero WS44 no define el conjunto mínimo ni el umbral de respuesta válida. Obligaría a inventar qué endpoints/respuestas satisfacen el gate.
3. **Hub/endpoint concreto a probar.** Cita: `G_SCION` exige evidencia con «fecha/Hub/endpoint/identidad/capabilities», pero WS44 no identifica el Hub ni la fuente para resolverlo. Obligaría a inventar si se descubre leyendo configuración existente o si debe indicarlo otro actor.

## DRY-RUN
Lecturas previstas: `dag.yaml`, guía, brief, alcance, decisiones, cobertura, validación humana e inventario de WS05. Cambio previsto: crear únicamente `auditoria/scion-probe.md`, sin mutar configuración ni secretos. Dependencias: inventario WS05, designación del operador en WS07 y `G_PRODUCT`. Validaciones futuras: respuesta pública real; registrar actor, fecha, Hub/endpoint, identidad y capabilities; ausencia de secretos; verificar que un fallo deja WS44 bloqueada y no avanza WS32; invalidar recibo previo ante cambio de Hub/API/credencial.

## FUTURO
WS07 designa operador y resuelve P01/`G_PRODUCT`; WS05 entrega inventario; un humano u operador confirma el permiso read-only; WS44 ejecuta el probe y produce `G_SCION`; WS32 queda a la espera de ese gate; cualquier cambio de Hub/API/credencial exige repetir el probe e invalidar el recibo.
