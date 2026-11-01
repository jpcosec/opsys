## REFORMULACION
Propósito: revisar como encargo de planificación el paquete “Ramal Scion opcional”, que delega la futura integración Scion sin ejecución propia. Resultado sustantivo: un ramal verificable con identidad de intento/manifiesto/RunDoc/cierre idempotente, mensajes con procedencia/dedup, dispatch intent/confirmed separado, adaptador autorizado, trazabilidad en workspace, intervención humana, acta real WS37 y capítulo WS38; G_SCION solo nace del probe público real de WS44. Repo dueño: deskops para la agrupación y el manual; graph_ui para WS35–WS37. Límites: no ejecuta, no autoriza tareas ni añade aristas; sin acceso real el ramal queda bloqueado; ningún permiso de núcleo se convierte en dispatch; no duplica pipeline Scion.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas: WS05 (`auditoria/scion.md`), WS07, WS12, WS11, `autorizaciones/scion.md`, WS27/WS30/WS31 y WS28. Hipotético: WS44 ejecuta probe read-only y produce G_SCION; si falla, se detiene. Con G_SCION, WS32 unifica intento/cierre; su salida alimenta WS33 (mensajes/decisiones), que alimenta WS34 (adaptador) y WS35 (trazabilidad), en paralelo cuando sus gates lo permitan. WS36 integra UI tras WS34+WS35. WS37 valida recorrido real con agente y acta humana; WS38 publica el capítulo usando WS37 y el manual básico WS31. Cambios previstos: solo artefactos de hijos (`auditoria/scion-probe.md`, registros de intento/mensajes, adaptador, vistas, acta, manual), ninguno ahora. Dependencias: G_PRODUCT, G_SCION, G_EXEC, G_WRITE_CONTRACT, G_CLOSEOUT, G_UI_READ, G_UI_WRITE, G_HUMAN_DELEGATE, más WS05/07/11/12/27/28/30/31. Validaciones futuras: pruebas locales de identidad/idempotencia/dedup, contrato dispatch intent/confirmed, no autoaprobación en WS36, recorrido UF06 en WS37 y enlaces/acta en WS38. Sin ejecutar.

## FUTURO
WS05 produce inventario; el solicitante designa operador/acceso y registra `autorizaciones/scion.md`; WS44 produce G_SCION. G_EXEC lo autoriza un humano externo. WS12/WS11/WS27/WS28/WS30/WS31 producen contratos, evidencia, handoff, acta manual y manual básico. WS37 produce acta humana y WS38 capítulo; G_HUMAN_DELEGATE lo decide el humano.
