## REFORMULACION
- **Propósito:** encargar en `graph_ui` la apertura de documentos en pestañas y en dos divisiones, con foco e historia de navegación.
- **Resultado:** pestañas que se abren, cambian y cierran; dos documentos lado a lado; alternancia de documento activo; “volver” que conserva documento, foco, origen e historia; disposición local de sesión, sin persistencia tras recargar.
- **Repo:** `graph_ui`, en `frontends/mindmap/views/workspace/layout/`, rutas de lectura del contrato WS11 y `tests/`.
- **Límites:** depende de WS11 y WS13.1; gate `G_UI_READ` pendiente por delta; no duplica el workspace ni exige persistencia; no se ejecuta nada.

## AMBIGUEDADES
1. “alternar el documento activo y volver conservando foco e historia. Volver sigue el orden inverso de navegación”.
   Obliga a inventar qué acciones generan entradas de historia: ¿abrir/cambiar pestaña, cambiar de división, cambiar el documento activo o cambiar el foco? Sin esa lista, no se puede comprobar qué restaura exactamente “volver”.

2. “Abrir, cambiar y cerrar pestañas; abrir dos documentos en divisiones, alternar el documento activo y volver conservando foco e historia”.
   Obliga a inventar el efecto de cerrar una pestaña: si elimina sus entradas de historia, si “volver” puede reabrirla y qué documento/foco queda activo al cerrar la pestaña activa.

3. “Pestañas, dos documentos lado a lado […] Cambiar de pestaña o división cambia el documento activo”.
   Obliga a inventar si las pestañas son globales o pertenecen a cada división, y cómo se combinan pestañas y divisiones al cambiar el documento activo.

## DRY-RUN
- **Lecturas:** nodo WS13.3, contratos vecinos WS11/WS13.1, guía, brief, alcance, decisiones, cobertura y reconciliación.
- **Cambios previstos:** componentes de pestañas/divisiones en `layout/`, estado local de foco/historia/disposición, rutas de lectura según WS11 y pruebas.
- **Dependencias:** contrato de navegación de WS11; lectura de documento de WS13.1; `G_UI_READ` por delta.
- **Validaciones futuras:** abrir/cambiar/cerrar pestañas, dos documentos en divisiones, alternancia y “volver” conservando foco e historia; acta de recepción por delta. Sin ejecutar.

## FUTURO
WS11 produce el contrato de navegación; WS13.1 aporta la lectura de documento; el receptor P01 en `graph_ui` emite el acta `G_UI_READ` de este delta. La promoción fija TaskDoc, archivos, textos y casos de prueba. WS06 decide integración o ticket existente.
