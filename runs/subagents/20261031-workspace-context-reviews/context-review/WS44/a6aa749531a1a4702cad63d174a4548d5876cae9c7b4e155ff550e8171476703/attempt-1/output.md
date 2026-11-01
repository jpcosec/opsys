REFORMULACION
WS44 es un nodo de validación, no agregado, del repo `deskops`. Encargo: con operador y acceso read-only registrados por el solicitante en `autorizaciones/scion.md`, ejecutar un probe read-only de la API pública de Scion contra el Hub indicado por el operador, verificar identidad del actor, Hub y capabilities mínimas que `auditoria/scion.md` marque para WS32/WS33, y dejar evidencia en `auditoria/scion-probe.md` para resolver G_SCION. Límites: no crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos; si falta el registro de acceso o el mapeo de capabilities, no ejecuta y registra el hueco; si API/acceso no existe, queda bloqueado. Tras cambio de Hub/API/credencial, repite e invalida recibo.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: `task-ws44.md`; `auditoria/scion.md` de WS05; `autorizaciones/scion.md`; configuración existente del Hub sin secretos; documentación/endpoint público de Scion. Comprobaciones previas: G_PRODUCT satisfecho, operador designado y acceso read-only registrado, capabilities mapeadas por nodo. Cambio previsto: solo `auditoria/scion-probe.md`, con respuesta pública real, actor, Hub, fecha y capabilities; sin mutaciones. Dependencias: consume WS05 y el registro de WS07/G_PRODUCT; no consume WS32/WS33, solo verifica lo que ellos requerirán. Gates: G_SCION queda satisfecho solo con ese recibo; G_PRODUCT ya está satisfecho. Errores: falta `autorizaciones/scion.md` → no ejecutar; falta mapeo en `auditoria/scion.md` → detenerse y registrar hueco antes del probe; API/acceso ausente → bloqueado, no cerrar `unverified`. Validación esperada: revisar que el informe no contenga secretos y que identifique respuesta real, identidad, Hub, fecha y capabilities.

FUTURO
El solicitante debe designar operador y registrar su acceso read-only; WS32/WS33 consumirán después las capabilities verificadas. Un cambio de Hub/API/credencial obliga a repetir el probe e invalidar el recibo; la promoción sigue no autorizada hasta designación y permiso.
