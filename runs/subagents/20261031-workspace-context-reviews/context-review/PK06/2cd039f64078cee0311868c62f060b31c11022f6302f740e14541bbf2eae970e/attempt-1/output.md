## REFORMULACION

**Propósito:** cerrar la publicación básica del workspace documental sobre recorridos ya demostrados, no habilitar producto nuevo.

**Resultado sustantivo:** un paquete documental verificable compuesto por (a) entradas e índices authored aplicados al deskops real —`desk/README.md`, mapa de ecosistema, átomos de acuerdos durables y acta de publicación— y (b) un manual de usuario versionado en `docs/workspace-user-manual.md`, con instrucciones enlazadas a actas, versión/commit, contratos y límites explícitos.

**Repo dueño:** `deskops`; la validación humana proviene de `graph_ui` vía WS30.

**Límites:** no escribe repos hermanos, no impone modelos, no promete Scion/modelos/Changes no demostrados, no ejecuta UI ni sustituye actas; la agrupación no autoriza tareas ni añade aristas.

## AMBIGUEDADES

1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada»: no se define qué integración ni quién la valida conjuntamente. WS31 tiene Tester para el manual y WS43 un participante para el mapa real, pero no se asigna la comprobación cruzada manual↔mapa publicado. Obligaría a inventar el criterio y el actor de aceptación integrada.

## DRY-RUN

Orden hipotético: WS10 y WS17 pueden avanzar en paralelo según sus dependencias; WS30 valida en Taller las entradas WS17 materializadas por WS40 y emite acta con paths/hashes y recorridos; WS43 consume esa acta y el contrato de navegación WS11, publica el mapa/README real con átomos y acta+commit; WS31 reúne WS10, acta WS30 y acta/versión WS43, redacta el manual y crea átomos de decisiones/contratos.

Transferencias: plantillas WS17 → corpus WS40 → acta WS30 → correspondencia de publicación WS43 → referencias del manual WS31. Validación integrada futura: resolver cada link del manual y del mapa contra paths/commit publicados; contrastar paths/hashes WS30 con la correspondencia WS43; verificar procedencia átomo→documento y etiquetas «propuesto» para Scion/modelos/Changes. Sin ejecutar.

## FUTURO

Producen otros nodos: acta WS30, publicación/acta/commit WS43, manual WS31, evidencia WS29/WS38. Decide un humano: P08 y recibos G_HUMAN_MANUAL/G_PRODUCT/G_WRITE_CONTRACT por delta.
