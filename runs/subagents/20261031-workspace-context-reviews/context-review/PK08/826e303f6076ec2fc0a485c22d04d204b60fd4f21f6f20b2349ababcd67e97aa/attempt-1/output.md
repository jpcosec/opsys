## REFORMULACION
**Propósito:** agrupar el ramal Scion opcional, sin ejecución propia. **Resultado sustantivo:** delegación Scion posterior con intentos, mensajes, decisiones, permisos, trazas e intervención humana verificables, sin duplicar el pipeline Scion ni convertir permisos del núcleo en dispatch. **Repo dueño:** deskops. **Límites:** PK08 no autoriza tareas ni añade aristas; sin acceso real el ramal queda bloqueado; WS44 solo produce G_SCION mediante probe read-only real; G_EXEC y permisos son explícitos; completed no equivale a aprobación.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Ejecución hipotética por aristas y gates: WS05 alimenta WS44; WS44, con operador/acceso designados, produce `auditoria/scion-probe.md` y G_SCION antes de WS32. WS32 consume WS05, WS12 y G_SCION; entrega identidad de intento/registro/idempotencia local y alimenta WS33. WS33 consume WS32 y WS11; entrega referencias, dedup, procedencia y decisiones, y alimenta WS34 y WS35. WS34 consume WS33 y WS12, con G_EXEC/G_SCION, y entrega el adaptador restringido dispatch/reply. WS35 consume WS33, WS27 y G_UI_READ, y entrega la vista de ejecución/trazabilidad. WS34 y WS35 pueden avanzar en paralelo; WS36 consume ambos y entrega la UI de delegación/intervención que invoca solo WS34 y registra decisiones vía WS33.2. WS37 consume WS36, WS30 y G_EXEC/G_SCION; ejecuta el recorrido real UF06 y produce acta en `runs/subagents/workspace-documental-acceptance/delegacion/`. WS38 consume WS37 y WS31; publica el capítulo verificado y átomos vinculados en el manual. Integración: WS37 prueba el recorrido extremo a extremo sin mocks; WS38 lo documenta remitiendo al acta real. La aceptación de PK08 exige coherencia e idempotencia intento/manifiesto/RunDoc/cierre, procedencia/dedup, dispatch intent/confirmed separados, permisos explícitos y acta humana.

## FUTURO
WS05 produce inventario; WS07, WS11, WS12, WS27, WS30 y WS31 aportan registros/contratos/prerrequisitos. Un humano designa operador y acceso Scion, autoriza G_EXEC y acepta el recorrido WS37. WS37 genera el acta y WS38 el capítulo/átomos; la aceptación de producto corresponde al solicitante.
