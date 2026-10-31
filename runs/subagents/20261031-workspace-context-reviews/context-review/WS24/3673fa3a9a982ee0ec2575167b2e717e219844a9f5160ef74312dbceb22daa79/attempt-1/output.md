## REFORMULACION
**Propósito:** WS24 es un encargo de implementación en `graph_ui` para integrar conocimiento y grafo local reutilizando el gráfico actual y una vista de documento genérica registrada en `shell/registry.js`, aplicable a átomos, protoátomos, crossroads, materializaciones, pills, clasificación, backlinks y vecindad de hasta 2 hops.
**Resultado:** navegación ida/vuelta por fuentes y backlinks, soporte Markdown no modelado visible con su ruta de origen, clasificación por tipo/tags y vecindad; sin renderer nuevo obligatorio por clase.
**Repo dueño:** `graph_ui`.
**Límites:** preservar Code local de `a1b2b22`; no crear segundo lector para Markdown no modelado; no inferir clasificación ficticia; ViewDoc WS18 es opcional y no bloquea; no duplicar implementación; no ejecutar.

## AMBIGUEDADES
**ninguna.**
Las referencias a WS09, WS03, WS11 y al comportamiento ante contrato ausente tienen productor nombrado o quedan cubiertas por las reglas comunes de `alcance.md`; no obligan al ejecutor a inventar.

## DRY-RUN
**Lecturas previstas:** guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS24, contratos vecinos WS13/WS09/WS29/WS30/WS42 y gates.
**Cambios previstos:** registrar/reutilizar la vista genérica en `shell/registry.js`; extender el panel Context existente; consumir backlinks de la API de grafo de SLDB; pruebas en `tests/`.
**Dependencias:** WS13 (lector/explorador), WS09 (catálogo), transitivas WS03 (auditoría de grafo) y WS11 (contrato), más `G_UI_READ`.
**Validaciones futuras:** aceptación por delta con acta de P01; comparar backlinks con la API; comprobar Markdown sin modelo y sin tags inventados; verificar clasificación y vecindad; confirmar que no se exige un renderer por clase.

## FUTURO
WS09 produce el catálogo de renderizaciones; WS03 la auditoría de infraestructura de grafo; WS11 el contrato de navegación. P01 emite el acta `G_UI_READ` del delta concreto. WS06/reconciliación decide integración o ticket receptor; el TaskDoc de promoción fija archivos, pills y evidencias. WS18 solo se conecta tras `G_SPEC_VIEW`. WS30 valida UF03.
