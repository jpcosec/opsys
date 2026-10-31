## REFORMULACION
**Propósito:** publicar en el deskops real la navegación documental validada. **Resultado:** README, mapa/índices y átomos de acuerdos durables, enlazando repos conocidos sin escribir en ellos, con acta y commit. **Repo:** deskops. **Límites:** no publicar solo el ejemplo Taller; no modificar repos hermanos; no crear entradas externas sin tarea de repo; ubicación/modelo y escritura dependen de P09, WS11 y G_WRITE_CONTRACT.

## AMBIGUEDADES
1. «Repos a enlazar = todos los de `deskops list repositories`» frente a «el mapa publicado corresponde a las entradas/índices validados en Taller». Taller/WS40 solo materializa dos desks; no se define cómo representar repos listados sin entrada validada. Obliga a inventar si se omiten, se enlazan sin validar o se replica el ejemplo.
2. «Enlazar repos conocidos por identidad/origen y su entrada existente» no cubre repos sin entrada existente; junto con «Escribir una entrada dentro de otro repo requiere su tarea y acuerdo de alcance», no se sabe si quedan fuera del mapa, se enlazan a su root o se bloquea. Obliga a inventar el criterio.
3. «commit por `deskops closeout commit`» usa un canal de cierre, pero `requires` no incluye G_CLOSEOUT, que cobertura.md asocia a commits de promoción/cierre. No se sabe si el commit de publicación queda autorizado solo con G_WRITE_CONTRACT o requiere ese gate. Obliga a decidir commit o bloqueo.

## DRY-RUN
**Lecturas:** dag.yaml (nodo, aristas y gates), guía, brief, alcance, decisiones, cobertura y contratos de WS17/WS30 como vecinos. **Cambios previstos:** desk/README.md, mapa/índices según P09/WS11, átomos de acuerdos, acta en runs/.../publicacion/acta.md y commit. **Dependencias:** WS17 (plantillas), WS30 (validación humana), G_PRODUCT (P08/P09), G_HUMAN_MANUAL, G_WRITE_CONTRACT; transitivas WS11/WS12/WS40. **Validaciones futuras:** P08/P09 resueltas, contrato de navegación, links/roots que resuelvan a paths existentes, mapa no reducido al ejemplo, acta y commit verificables.

## FUTURO
WS07 registra P01/P02/P07/P08/P09 con actor y fecha; WS11 publica contratos/navegacion.md; WS12 produce operaciones.md y G_WRITE_CONTRACT; WS30 produce G_HUMAN_MANUAL y su acta; el humano designado en P08 ejecuta la aceptación; WS31 consume el acta de WS43. La promoción fija paths exactos, modelo/contrato, pills/átomos y preflight.
