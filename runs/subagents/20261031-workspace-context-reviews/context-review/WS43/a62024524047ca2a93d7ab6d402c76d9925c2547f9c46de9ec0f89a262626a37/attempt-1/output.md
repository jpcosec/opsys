## REFORMULACION
**Propósito:** publicar en el repo real `deskops` la navegación documental validada en Taller, aplicando entradas/índices authored y preservando el registry como inventario derivable. **Resultado:** `desk/README.md`, mapa de ecosistema/índices según P09 y el contrato de navegación, átomos de acuerdos durables enlazados, acta de publicación y commit por `deskops closeout commit`. **Repo dueño:** `deskops`. **Límites:** no escribir en repos hermanos; enlazar no equivale a escribir; una entrada en otro repo exige tarea y acuerdo de alcance; no imponer modelos nuevos; no publicar solo el ejemplo como ecosistema real. **Dependencias:** WS17, WS30; gates G_HUMAN_MANUAL, G_PRODUCT, G_WRITE_CONTRACT; contrato `contratos/navegacion.md` (WS11, transitivo).

## AMBIGUEDADES
1. «Enlazar repos conocidos por identidad/origen y su entrada existente» — no define qué hacer si un repo de `deskops list repositories` carece de entrada existente: omitirlo, bloquear la publicación o abrir tarea. Obliga a inventar el resultado para ese repo.
2. «los acuerdos durables aplicados al mapa (Pxx aceptadas y contratos aplicables)» — «contratos aplicables» no fija criterio ni lista; obliga a inventar si comprende solo `navegacion.md`, también `operaciones.md` u otros de `contratos/`.

## DRY-RUN
- **Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, nodo WS43, contratos edge WS17/WS30 y gates.
- **Cambios previstos:** `desk/README.md`; mapa/índices authored; átomos enlazados; acta `deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md`; commit de cierre.
- **Dependencias:** WS17 aporta plantillas/índices; WS30 aporta validación humana y G_HUMAN_MANUAL; WS11/WS12 aportan contratos; WS07 resuelve P09/G_PRODUCT.
- **Validaciones futuras:** links y roots verificables; correspondencia con entradas/índices validados en Taller; registro de acuerdos aceptados; commit y acta; preflight en frío exigido por promoción.

## FUTURO
- WS07: resoluciones humanas P01/P09 y G_PRODUCT.
- WS11/WS12: contrato de navegación y contrato técnico de operaciones.
- WS30: acta manual y G_HUMAN_MANUAL.
- WS40: corpus regenerado del ejemplo.
- P08: participante humano designado para recorrer Markdown y UI real.
