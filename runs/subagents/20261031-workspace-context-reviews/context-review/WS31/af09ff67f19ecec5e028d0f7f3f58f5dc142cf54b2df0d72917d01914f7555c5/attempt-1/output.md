## REFORMULACION
**Propósito:** publicar el manual documental básico ya probado, incorporando el índice y convención de `borradores/manual.md`, capturas y limitaciones en `docs/workspace-user-manual.md`.
**Resultado:** manual publicado con instrucciones trazables a las actas de WS30/WS43, átomos por acuerdos durables aceptados y contratos, etiquetas/links/atom→doc verificados y capítulo Scion solo como propuesto.
**Repo:** `deskops` (`output_base: deskops:repository_root/`).
**Límites:** no prometer Scion antes de WS38; no atomizar Pxx pendientes; personalización/impacto solo con G_HUMAN_MODEL/WS29 o etiqueta propuesta; no ejecutar.

## AMBIGUEDADES
1. «por cada contrato en contratos/ (navegacion.md, operaciones.md u otros de WS11/WS12)»: el conjunto «u otros» es abierto y `contratos/` no indica repo ni ruta base; obliga a inventar qué contratos existen y dónde leerlos.
2. «un átomo por acuerdo durable ya aceptado por humano en decisiones.md»: «acuerdo durable» no está definido y `decisiones.md` no registra aceptaciones; obliga a decidir qué acuerdos cuentan y cuáles no.
3. «comprobar G_HUMAN_MODEL/WS29 o mantener etiqueta propuesta»: «comprobar WS29» no fija criterio (¿inicio, cierre, acta?) para pasar de propuesta a verificado; obliga a inventar la condición de comprobación.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (nodo y vecinos), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`, contratos de WS11/WS12, acta de WS30, acta y mapa de WS43, átomos existentes.
**Cambios previstos:** `docs/workspace-user-manual.md`, `docs/assets/workspace-user-manual/`, `desk/atoms/` vinculados.
**Dependencias:** WS30 (acta/G_HUMAN_MANUAL), WS10 (índice), WS43 (publicación, G_PRODUCT, G_WRITE_CONTRACT), contratos WS11/WS12.
**Validaciones futuras:** preflight task-only y TaskDoc de promoción; etiquetas, links y atom→doc; contraste con actas; aprobación humana.

## FUTURO
- WS10 entrega el índice/convención; WS30 produce acta y G_HUMAN_MANUAL; WS43 produce acta de publicación, mapa y satisface G_PRODUCT/G_WRITE_CONTRACT.
- WS11/WS12 producen los contratos referenciados.
- WS38 añade el capítulo Scion verificado; WS29/WS39 sustentan impacto/modelos.
- El humano resuelve Pxx; la promoción fija archivos, pills y pruebas exactas.
