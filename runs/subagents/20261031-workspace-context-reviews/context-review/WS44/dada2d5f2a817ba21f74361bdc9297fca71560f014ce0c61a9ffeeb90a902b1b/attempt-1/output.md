## REFORMULACION
WS44 encarga una validación read-only en `deskops`: comprobar acceso público real a Scion y registrar evidencia para `G_SCION` en `auditoria/scion-probe.md`. El resultado debe incluir respuesta pública real, identidad del operador, Hub, fecha y capabilities requeridas por WS32/WS33 según `auditoria/scion.md`. Límites: no crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos; no ejecutar sin el registro de acceso en `autorizaciones/scion.md`; no cerrar como verificado si falta API/acceso ni avanzar WS32. Tras cambio de Hub/API/credencial, repetir e invalidar el recibo anterior.

## AMBIGUEDADES
ninguna

## DRY-RUN
WS44 es un nodo hoja de validación, no un agregado; no tiene hijos que recorrer. Un ejecutor futuro leería `dag.yaml` (nodo, aristas y gates), `decisiones.md`, `alcance.md`, la salida WS05 `auditoria/scion.md` y el registro del solicitante `autorizaciones/scion.md`; consultaría la configuración Scion existente solo para obtener el Hub, sin secretos. Verificaría que `G_PRODUCT` ya está satisfecho por WS07 y que WS05/WS07 están disponibles.

Cambios previstos: escribir únicamente `auditoria/scion-probe.md` con actor, fecha, Hub, endpoint, identidad y capabilities, evidencia de respuesta pública real y límites observados. No modificaría configuración, agentes ni mensajes.

Dependencias y gates: consumiría el inventario WS05 para el mapeo de capabilities por WS32/WS33 y el registro WS07 de decisiones; `G_SCION` solo quedaría satisfecho con evidencia completa. Errores esperados: si falta `autorizaciones/scion.md` o no registra acceso read-only, detenerse sin probe; si `auditoria/scion.md` no mapea capabilities por nodo, detenerse y registrar el hueco antes del probe; si API o acceso no responden, dejar WS44 bloqueada y no cerrar `unverified`. Validación esperada: respuesta pública real, identidad del operador, Hub, fecha y capabilities registrados; sin secretos; repetición obligatoria tras cambio de Hub/API/credencial.

## FUTURO
El solicitante debe designar al operador de Scion y registrar su acceso read-only en `autorizaciones/scion.md`; el operador aporta el Hub desde configuración existente. WS05 ya produce el inventario y WS32/WS33 fijan las capabilities requeridas. WS32 no puede avanzar hasta que `G_SCION` tenga evidencia real.
