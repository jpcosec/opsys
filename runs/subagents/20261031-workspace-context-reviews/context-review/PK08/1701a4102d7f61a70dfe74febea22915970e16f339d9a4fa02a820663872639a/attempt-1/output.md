## REFORMULACION
Propósito: revisar PK08 como encargo de planificación del ramal Scion opcional, sin ejecutarlo. Resultado sustantivo: un paquete que permita delegación Scion posterior con intentos, mensajes, decisiones, permisos y trazabilidad verificables, incluido probe real y acta humana. Repo dueño: `deskops`; hijos en `deskops` y `graph_ui`. Límites: PK08 es agrupación sin ejecución propia; sin acceso real el ramal queda bloqueado; ningún permiso de núcleo se convierte en dispatch; no duplicar pipeline Scion ni simular aprobación.

## AMBIGUEDADES
ninguna

## DRY-RUN
Ejecución hipotética por hijos: WS05 produce `auditoria/scion.md`; WS44, tras WS05/WS07 y con operador/acceso registrados, ejecuta probe read-only y produce `auditoria/scion-probe.md` y G_SCION. Luego WS32, con G_SCION/G_CLOSEOUT/G_WRITE_CONTRACT, fija identidad intento/cierre, manifiesto/RunDoc idempotente y pruebas locales WS32.1/32.2. WS33 consume esa identidad y WS11 para vincular mensajes, resultados y decisión humana, con dedup/procedencia. WS34 consume WS33/WS12 y produce adaptador público restringido dispatch/reply con confirmación, timeout/errores y autoridad del coordinador; requiere G_EXEC. WS35 consume WS33/WS27 y produce vista de ejecución/trazas en `graph_ui`. WS36 consume adaptador WS34 y vista WS35 para integrar intervención humana, registrando decisiones WS33.2; requiere G_EXEC. WS37 consume WS36/WS30 y ejecuta recorrido real UF06 con agente, dejando acta en `runs/subagents/workspace-documental-acceptance/delegacion/`. WS38 consume acta WS37 y manual WS31 para publicar capítulo verificado y átomos vinculados.

Integración: salida WS32 alimenta WS33; WS33 alimenta WS34/WS35; WS34+WS35 alimentan WS36; WS36 alimenta WS37; acta WS37 alimenta WS38. Validación integrada: pruebas locales de identidad/idempotencia en WS32, prueba real WS37 con G_SCION/G_EXEC y acta humana, y comprobación WS38 de que cada paso remite al acta y a operaciones reales. Dependencias externas: G_EXEC lo autoriza un humano; WS27/WS30/WS31 aportan evidencia, validación manual y manual básico.

## FUTURO
WS05 entrega inventario; un humano designa operador Scion y autoriza G_EXEC; WS44 produce o mantiene bloqueado G_SCION; WS37 genera acta humana; WS38 publica el capítulo. Nada de esto se ejecuta aquí.
