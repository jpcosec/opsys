REFORMULACION
Propósito: publicar en el deskops real la navegación documental ya validada en el ejemplo, sin tocar repos hermanos. Resultado: `desk/README.md`, mapa/índices según P09 y `contratos/navegacion.md` (WS11), átomos de acuerdos durables, acta y commit. Repo dueño: deskops. Límites: no modificar repos enlazados, no imponer modelos, no publicar solo el ejemplo; escribir en otro repo exige tarea y acuerdo de alcance.

AMBIGUEDADES
1. «Registrar conocimiento durable en átomos antes de docs» / «los acuerdos durables aplicados al mapa quedan en átomos enlazados desde él». No se define qué acuerdos son «durables» ni el criterio de «aplicados al mapa». WS31 sí fija una regla (Pxx aceptadas y contratos), pero WS43 no remite a ella. Obligaría a inventar el conjunto de átomos y si incluye contratos o solo decisiones aceptadas.
2. «Aplicar entradas/índices authored validados en Taller al deskops real» / «el mapa publicado corresponde a las entradas/índices validados en Taller». WS17 entrega plantillas de ejemplo y WS30 las valida, pero no se define qué parte es plantilla reutilizable y qué debe reescribirse con los repos reales. Obligaría a inventar el mapeo ejemplo→ecosistema real.

DRY-RUN
Lecturas: nodo, brief, alcance, decisiones, cobertura, aristas WS17/WS30 y gates. Cambios previstos: aplicar plantillas/índices al deskops real; escribir README y mapa; crear/enlazar átomos; enlazar todos los repos de `deskops list repositories` sin escribirlos; generar acta y commit con `deskops closeout commit`. Dependencias: contrato WS11, plantillas WS17, acta WS30, P08/P09/P01 vía G_PRODUCT, G_WRITE_CONTRACT, G_HUMAN_MANUAL, registry. Validaciones futuras: links/roots resuelven a paths existentes; mapa coincide con lo validado; todos los repos enlazados; átomos enlazados; acta/commit; recorrido humano; cold preflight.

FUTURO
WS07 registra P01/P02/P07/P08/P09 y G_PRODUCT; WS30 produce G_HUMAN_MANUAL; WS12 produce G_WRITE_CONTRACT; WS11 el contrato de navegación; WS17 las plantillas; WS31 usará el acta de WS43; la promoción fija paths, átomos, evidencia y preflight. No es ambigüedad.
