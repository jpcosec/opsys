## REFORMULACION
**Propósito:** verificar con un probe real, de solo lectura, que la API pública de Scion es accesible y cubre las capabilities exigidas por WS32/WS33, con Hub e identidad del operador designado. **Resultado:** `auditoria/scion-probe.md` que sustenta G_SCION. **Repo dueño:** deskops (registro); el probe ocurre contra la instalación Scion existente del operador. **Límites:** sin crear agentes, enviar mensajes, cambiar configuración ni exponer secretos; sin ese registro de acceso en WS07 no se ejecuta; si falta mapeo de capabilities, se detiene y registra hueco; no cierra como unverified ni habilita WS32.

## AMBIGUEDADES
1. «Tras cambio de Hub/API/credencial, repetir y invalidar recibo previo.» No se nombra quién detecta el cambio ni con qué mecanismo, ni cuándo ese control deja de ser responsabilidad del operador. El ejecutor tendría que inventar una vigilancia o un disparador de revalidación. Cita: «Tras cambio de Hub/API/credencial, repetir y invalidar recibo previo.»
2. «identidad del operador y Hub, fecha, capabilities y actor registrados.» «Actor» e «identidad del operador» pueden ser el mismo dato; la aceptación no distingue si el actor es quien ejecuta el probe o quien autoriza el acceso. Obligaría a decidir por cuenta propia qué campo distinto registrar. Cita: «identidad del operador y Hub, fecha, capabilities y actor registrados.»

## DRY-RUN
**Lecturas previstas:** guía de revisión; nodo WS44 y contratos vecinos WS05/WS07 y gates; `auditoria/scion.md` (inventario WS05 y mapeo de capabilities); `decisiones.md` (P01, operador y acceso read-only); configuración Scion existente sin secretos; `alcance.md`, regla común ante contrato ausente.
**Cambios previstos:** únicamente escribir `desk/drawer/plans/workspace-documental/auditoria/scion-probe.md`.
**Dependencias:** WS05 cerrado con inventario; WS07 con G_PRODUCT y designación/registro de acceso del operador Scion.
**Validaciones futuras:** G_SCION resuelto por WS44 con respuesta real; WS32 permanece bloqueado hasta el recibo; repetir probe e invalidar recibo anterior cuando proceda.

## FUTURO
WS07 (humano) designa operador y registra acceso read-only; WS05 entrega inventario y mapeo de capabilities; WS32/WS33 consumen el recibo; un humano decide la revalidación ante cambios de Hub/API/credencial. Este nodo no ejecuta el probe.
