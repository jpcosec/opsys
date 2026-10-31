## REFORMULACION
Propósito: comprobar y revalidar acceso público real a Scion mediante un probe read-only, sin crear agentes, enviar mensajes, cambiar configuración ni exponer secretos. Resultado: `auditoria/scion-probe.md` con respuesta pública, identidad del operador, Hub, fecha y capabilities. Repo dueño: `deskops`. Límites: solo lectura; no satisface G_SCION sin probe real; si falta API/acceso, queda bloqueada y no habilita WS32. Depende de WS05, WS07 y G_PRODUCT; el operador y su acceso read-only deben constar en `autorizaciones/scion.md`.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Lecturas previstas: `autorizaciones/scion.md` para confirmar operador y acceso read-only; `auditoria/scion.md` de WS05 para capabilities requeridas por WS32/WS33; configuración existente para identificar el Hub. Cambios previstos: únicamente registrar el resultado en `auditoria/scion-probe.md`; no se modifica configuración ni se contacta nada en este dry-run. Dependencias: WS05 y WS07, más G_PRODUCT ya satisfecho; el probe no se ejecuta sin el registro de autorización. Validaciones futuras: respuesta pública real; actor del probe; Hub, fecha y capabilities; ausencia de secretos; bloqueo si falta API o acceso; invalidación y repetición tras cambio de Hub/API/credencial.

## FUTURO
El solicitante designa al operador Scion y registra su acceso read-only; WS05 produce el inventario y el mapeo de capabilities; WS32/WS33 consumen esas capabilities. La ejecución real del probe y la eventual repetición corresponden a WS44 cuando exista designación y autorización. G_SCION permanece `unverified` hasta que exista evidencia real; no se cierra como verificado por el inventario ni por el acuerdo de producto.
