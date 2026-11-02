REFORMULACION
WS43 es un nodo de entrega documental, no agregado. Su encargo es publicar en el deskops real la navegación documental ya validada en Taller: aplicar entradas/índices authored, actualizar desk/README.md, crear el mapa de ecosistema según P09 y el contrato WS11, registrar acuerdos durables en átomos enlazados y dejar acta de publicación. Repo dueño: deskops. Límites: preservar registry como inventario derivable; enlazar repos por identidad/origen; no escribir en repos hermanos sin tarea y acuerdo; no fabricar entradas interrepo; no publicar solo el ejemplo como ecosistema real.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: nodo y gates; contratos/navegacion.md de WS11; plantillas ejemplo/nav/ de WS17; acta de WS30 con paths/hashes; decisiones.md; `deskops list repositories`; registry repo-*.md; átomos existentes. Cambios previstos: editar desk/README.md; crear/actualizar mapa e índices; crear átomos de P01/P02/P07/P09 y contratos aplicables, reutilizando equivalentes; crear acta en runs/subagents/workspace-documental-acceptance/publicacion/acta.md; commit por `deskops closeout commit`. Dependencias: WS17 entrega plantillas/índices; WS30 entrega acta y G_HUMAN_MANUAL; G_PRODUCT está satisfecho; G_WRITE_CONTRACT necesita recibo per_delta de WS43. Si falta contrato, acta o recibo: detenerse y registrar hueco con repo dueño. Validación futura: el participante P08 recorre Markdown y UI real; cada link/root resuelve a path existente; todos los repos de `deskops list repositories` quedan enlazados o con follow-up; el mapa coincide con lo validado por WS30; el acta registra correspondencia. Errores: link roto, repo sin entrada, inconsistencia WS17/WS30 o contrato ausente: registrar y no sustituir.

FUTURO
WS31 usa el acta de WS43 para publicar el manual; el humano P08 realiza la aceptación de publicación; WS12 emite el recibo de G_WRITE_CONTRACT para WS43 y WS30 produce G_HUMAN_MANUAL. Nada de eso corresponde inventarlo al ejecutor de WS43.
