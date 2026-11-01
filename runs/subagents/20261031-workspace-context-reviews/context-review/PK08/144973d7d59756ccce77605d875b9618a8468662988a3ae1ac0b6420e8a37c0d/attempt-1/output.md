REFORMULACION
Propósito: agrupar el ramal E (Scion opcional) para que delegación, intentos, trazas e intervención humana sean verificables sin duplicar el pipeline Scion. Resultado sustantivo: un paquete cuyos hijos producen identidad de intento/cierre, vínculo mensajes-resultados-decisiones, adaptador dispatch/reply, vista de ejecución, UI de intervención, validación con agente real y capítulo de manual. Repo dueño: deskops; hijos en deskops y graph_ui. Límites: agregado no ejecutable; no autoriza tareas ni añade aristas; sin acceso real el ramal queda bloqueado; ningún permiso de núcleo se convierte en dispatch; no duplica pipeline; la revisión de comprensión no equivale a producto entregado.

AMBIGUEDADES
ninguna.

DRY-RUN
Hipotéticamente: WS05 produce el inventario (auditoria/scion.md) y WS44, con operador/acceso registrados por el solicitante, ejecuta el probe read-only y produce auditoria/scion-probe.md → G_SCION. Si falta registro o acceso, se detiene y WS32–WS37 siguen bloqueados. WS32 (WS32.1/32.2) consume WS05, WS12, G_SCION y G_CLOSEOUT; entrega identidad intento/manifiesto/RunDoc/cierre idempotente. WS33 consume WS32 y WS11; entrega vínculos mensaje/resultado/decisión con dedup y procedencia. WS34 consume WS33 y WS12; entrega adaptador restringido dispatch/reply con timeout/errores. WS35 consume WS33 y WS27; entrega vista de trazas en graph_ui. WS36 consume WS34 y WS35; entrega intervención humana contra el adaptador. WS37 consume WS36 y WS30; ejecuta UF06 real y deja acta en runs/subagents/workspace-documental-acceptance/delegacion/. WS38 consume WS37 y WS31; publica capítulo en docs/workspace-user-manual.md con átomos vinculados. Validación integrada: acta WS37, enlaces a fuente, G_EXEC/G_SCION/G_HUMAN_DELEGATE; errores se registran con repo dueño y no se sustituyen.

FUTURO
WS05 entrega inventario; el solicitante designa operador y registra acceso Scion, y WS44 produce G_SCION; G_EXEC lo autoriza un humano externo; WS30 aporta acta de validación manual; WS31 el manual básico; WS07 el registro de decisiones; WS12 el contrato de operaciones; WS27 evidencia; WS11 navegación.
