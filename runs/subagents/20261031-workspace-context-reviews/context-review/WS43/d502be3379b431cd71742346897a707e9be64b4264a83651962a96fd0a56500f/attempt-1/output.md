## REFORMULACION
Propósito: publicar en el deskops real la navegación documental validada en Taller (WS30). Resultado: `desk/README.md`, mapa/índices authored, átomos de acuerdos durables, acta y commit. Repo dueño: deskops; enlaza repos de `deskops list repositories` sin escribir en ellos. Límites: operaciones autorizadas, registry como inventario derivable, sin modelos nuevos ni publicar solo el ejemplo; repo sin entrada authored se enlaza por registry y follow-up.

## AMBIGUEDADES
1. «commit por `deskops closeout commit`» frente a `requires` solo `G_WRITE_CONTRACT`: no aclara si basta ese gate o se exige `G_CLOSEOUT`/`G_WRITE_POLICY`. Obliga a inventar la autorización de cierre.
2. `output_scope` «desk/README.md; mapa...; átomos» vs acceptance «acta deskops:runs/.../publicacion/acta.md y commit»: el acta queda fuera del límite declarado; obliga a decidir si escribirla excede alcance.
3. «P08 remite a protocolo»: no nombra protocolo ni destino; obliga a inventar a qué protocolo/enlace remite.
4. «P03–06 solo si mapa expone operaciones»: no define «exponer operaciones»; obliga a decidir si se atomizan P03–P06.

## DRY-RUN
Lecturas: nodo WS43; brief, alcance, decisiones y cobertura; contratos `navegacion.md` (WS11) y `operaciones.md` (WS12); plantillas/índices WS17 y acta WS30; corpus/manifiesto WS40; `desk/README.md` real, registry, salida de `deskops list repositories` y átomos existentes. Cambios previstos: `desk/README.md`; mapa/índices en la ubicación que fijen P09/contrato; átomos P01/P02/P07/P09 (P03–06 condicional); acta de publicación; commit por closeout. Dependencias: WS17/WS30; `G_HUMAN_MANUAL` pendiente (WS30), `G_PRODUCT` satisfecho, `G_WRITE_CONTRACT` per-delta pendiente para WS43. Validaciones futuras: links/roots resuelven a paths existentes; correspondencia con paths/hashes del acta WS30; recorrido humano del participante P08; commit/acta; ninguna escritura en repos hermanos; repo sin entrada: registry + follow-up.

## FUTURO
WS11 produce `navegacion.md`; WS12 verifica `G_WRITE_CONTRACT` por delta (incluido WS43) y `operaciones.md`; WS30 produce acta y `G_HUMAN_MANUAL`; WS17/WS40 entregan plantillas y corpus; el participante P08 realiza el recorrido; el workflow/coordinador decide el commit; WS31 consume el acta de WS43. Son productos o decisiones externas, no ambigüedades de WS43.
