## REFORMULACION
WS44 es una validación read-only del acceso público a Scion: el operador designado en WS07 comprueba identidad, Hub/endpoint y capabilities necesarias para intento y mensajes, sin crear agentes, enviar mensajes, cambiar configuración ni exponer secretos. Produce `auditoria/scion-probe.md` en `deskops` como evidencia de G_SCION. Si falta API o acceso, queda bloqueada; ante cambios de Hub/API/credencial debe repetir e invalidar el recibo anterior.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
- **Lecturas previstas:** `auditoria/scion.md` de WS05, registro/designación de WS07 y G_PRODUCT, configuración existente de Scion indicada por el operador, respuesta real de la API pública.
- **Cambios previstos:** crear `auditoria/scion-probe.md` con actor, fecha, Hub, endpoint, identidad y capabilities verificadas; registrar o invalidar el recibo de G_SCION según corresponda.
- **Dependencias:** WS05 debe aportar el inventario; WS07 debe designar operador y registrar el acceso read-only; el operador debe indicar el Hub. Sin esos elementos, no se ejecuta el probe.
- **Validaciones futuras:** comprobar respuesta pública real, capabilities mínimas marcadas por `auditoria/scion.md` para WS32/WS33, ausencia de secretos y repetición tras cambio de Hub/API/credencial.

## FUTURO
WS07 y el solicitante humano designan al operador y confirman el acceso read-only; WS05 entrega el inventario de API/identidad; el operador aporta el Hub desde su configuración. WS32/WS33 consumen las capabilities verificadas. Cualquier cambio de Hub, API o credencial exige nueva revalidación humana/operativa y no se presume aprobado por este nodo.
