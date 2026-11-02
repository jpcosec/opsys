## REFORMULACION

Propósito: producir el paquete de planificación del workspace documental de Deskops sobre Mindmap/SLDB/Deskops, cubriendo lector temprano, autoría/operación manual, manual publicado, extensiones independientes y ramal Scion opcional. Resultado: conjunto integrado de auditorías, contratos, vistas, recorridos, manual y evidencias de aceptación, con identidad/origen compartidos y sin duplicar código existente. Repo dueño: `deskops`. Límites: ROOT es agrupación sin ejecución propia; no autoriza tareas, no añade aristas, no implementa UI ni modifica otros repos; extras y Scion no bloquean el núcleo; las actas y recepciones por delta quedan fuera del plan.

## AMBIGUEDADES

1. «dry-run hipotético describe orden/aristas y transferencia entre hijos: PK01 audita base y reconcilia deltas; PK02 convierte decisiones registradas en flows/vistas/contratos; …». El input no expone aristas formales `depends_on` entre PK01–PK08; solo una secuencia narrativa. Obligaría a inventar qué PK es prerrequisito formal de cuál, si PK07/PK08 dependen de PK06 y qué artefacto exacto transfiere cada uno.

## DRY-RUN

Ejecución hipotética según el scope: PK01 lee brief/alcance/decisiones/dag y produce auditorías WS02–WS04, matriz de deltas WS06 e inventario Scion WS05. PK02 consume esa matriz y el registro de decisiones; entrega UFs WS08, convención manual WS10, catálogo de vistas WS09, navegación WS11 y whitelist por delta WS12. PK03 consume WS11/WS08 y WS40; entrega lector, búsqueda, errores, corpus Taller y lectura multidesk; WS16 integra acta humana. PK04 consume WS11/WS40/WS13/WS09; entrega índices, Board, procedimientos y conocimiento; WS18 es opcional tras `G_SPEC_VIEW`. PK05 consume WS12, WS17, WS22/WS24; produce edición WS19/20/45/21, intake WS25, tareas WS26, diff WS27, handoff WS28 y conocimiento WS42; WS30 integra acta UF02–05. PK06 consume WS30 y WS17; WS43 publica entradas reales y WS31 reúne el manual versionado. PK07 ejecuta WS29/WS39 por separado. PK08 solo tras WS05 y operador/acceso designados: WS44 produce `G_SCION`, WS32–WS36 implementan, WS37 acepta y WS38 publica capítulo.

Gates/dependencias: `G_PRODUCT`, `G_SOURCE`, `G_WRITE_CONTRACT`, `G_HUMAN_READ`, `G_PAYLOAD_PRECONDITION`, `G_CLOSEOUT`, `G_EXEC/G_SCION`. Si falta contrato, API, dato o permiso: detener, registrar hueco con repo dueño y no sustituir. Validación conjunta: actas WS16/30/37, publicación WS43/31, identidad/origen, APIs públicas, guardas/canales, manual trazado y ausencia de dependencias opcionales sobre el núcleo.

## FUTURO

Actas humanas WS16/30/37; recepción técnica por delta en graph_ui/SLDB/spec2viz; designación de operador/acceso Scion; publicación real WS43 y manual WS31; receipts con actor, alcance, fecha y commit/blob en repos receptores.
