## REFORMULACION

**Propósito:** publicar en el desk real la navegación documental ya validada en Taller, sin sustituir el registry ni imponer modelos nuevos.

**Resultado:** `desk/README.md` actualizado; mapa/índices según P09 y contratos de WS11/WS12; átomos de acuerdos durables enlazados; acta en `deskops:runs/subagents/workspace-documental-acceptance/publicacion/acta.md`; commit vía `deskops closeout commit`.

**Repo dueño:** `deskops`. **Límites:** enlazar todos los repos de `deskops list repositories` sin escribir en ellos; escribir en otro repo exige tarea y acuerdo; no publicar solo el ejemplo; no modificar repos hermanos. Depende de WS17, WS30 y gates `G_HUMAN_MANUAL`, `G_PRODUCT`, `G_WRITE_CONTRACT`; contratos transitivos WS11/WS12.

## AMBIGUEDADES

Ninguna. Las referencias a P08/P09, contratos pendientes y ubicación/modelo exacto quedan cubiertas por gates, dependencias transitivas, reglas comunes y promoción; no obligan a inventar resultado ni aceptación.

## DRY-RUN

**Lecturas:** input completo, guía, brief, alcance, decisiones, cobertura, nodo WS43 y contexto de WS17/WS30/gates.

**Cambios previstos:** editar `desk/README.md`; crear/actualizar mapa e índices; crear y enlazar átomos; escribir acta; ejecutar commit de cierre.

**Dependencias:** WS17 aporta plantillas; WS30/G_HUMAN_MANUAL validación humana; WS11/WS12 contratos de navegación/operaciones y G_WRITE_CONTRACT; G_PRODUCT exige P09/P08 resueltas.

**Validaciones futuras:** links/roots resolubles a paths existentes; mapa correspondiente a lo validado en Taller; recorrido humano; acta y commit; ausencia de escritura en otros repos y de registry duplicado; preflight frío de promoción. Sin ejecución.

## FUTURO

WS17 produce las plantillas; WS30 produce el acta de `G_HUMAN_MANUAL`; WS07 registra P01/P02/P07/P08/P09 en `G_PRODUCT`; WS11/WS12 producen contratos y `G_WRITE_CONTRACT`; el humano designado por P08 realiza el recorrido; la promoción fija paths, modelo, átomos/pills y evidencia; `deskops closeout commit` materializa el cierre.
