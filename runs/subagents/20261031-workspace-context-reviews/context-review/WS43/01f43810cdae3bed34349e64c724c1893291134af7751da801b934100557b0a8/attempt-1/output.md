## REFORMULACION
**Propósito:** publicar en el deskops real la navegación documental validada en Taller, reutilizando entradas/índices authored y el registry como inventario derivable.  
**Resultado:** `desk/README.md`, mapa/índices, átomos de acuerdos durables y acta de publicación con correspondencia verificable.  
**Repo dueño:** `deskops`.  
**Límites:** no escribir repos hermanos sin tarea/acuerdo; no fabricar entradas interrepo ni omitir repos listados; no imponer modelos nuevos; operar solo por canales autorizados; el commit se hace por `deskops closeout commit`.

## AMBIGUEDADES
Ninguna. Las referencias a contratos y gates tienen productor identificado (WS11/WS12/WS30) y las reglas comunes cubren su ausencia; archivos exactos, modelo opcional y textos quedan a la promoción. La aceptación es comprobable mediante links/roots resolubles, correspondencia paths/hashes con el acta WS30, acta y commit.

## DRY-RUN
**Lecturas previstas:** acta WS30; plantillas/entradas WS17; contrato `navegacion.md` WS11; contrato `operaciones.md`/G_WRITE_CONTRACT WS12; `deskops list repositories`; registry `desk/registry/repo-*.md`; decisiones P01–P09; README y átomos existentes.  
**Cambios previstos:** `desk/README.md`, mapa/índices del ecosistema, átomos de acuerdos durables y `runs/subagents/workspace-documental-acceptance/publicacion/acta.md`.  
**Dependencias:** WS17 y WS30; gates G_HUMAN_MANUAL, G_PRODUCT y G_WRITE_CONTRACT.  
**Validaciones futuras:** resolver cada link/root contra un path existente del repo enlazado; contrastar paths/hashes de WS17 con el acta WS30; verificar que el mapa no sustituye el registry ni publica solo el ejemplo; comprobar reutilización de átomos; commit por closeout; no modificar repos hermanos.

## FUTURO
WS17 entrega las plantillas/entradas; WS30 produce el acta y satisface G_HUMAN_MANUAL; WS11 produce el contrato de navegación; WS12 verifica G_WRITE_CONTRACT por delta, incluido WS43; el participante P08 realiza el recorrido humano; el cierre se ejecuta por el workflow Deskops; WS31 consume esta publicación para el manual. Nada de ello es ambigüedad del encargo.
