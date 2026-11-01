## REFORMULACION

**Propósito:** WS15 agrupa la entrega de errores de lectura/modo degradado (WS15.1) y orientación de proyecto sin desk (WS15.2) en el lector workspace.

**Resultado:** agregado no ejecutable; se considera cumplido cuando WS15.1 y WS15.2 cumplen su aceptación. Sus dependientes siguen dependiendo del ID WS15.

**Repo dueño:** graph_ui. Salidas bajo `frontends/mindmap/views/workspace/errors/` y `orientation/`, con rutas de lectura fijadas por el contrato WS11 y tests.

**Límites:** solo lectura; reutiliza la lectura Markdown de WS13.1 y no implementa otro lector ni guardado; no promete funcionamiento offline; nunca inicializa un desk por GET; requiere G_UI_READ por delta; promoción no autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor futuro no ejecuta WS15 directamente: prepara y promueve sus dos hijos, que dependen de WS13 y no tienen arista entre sí.

- **WS15.1:** consume la lectura Markdown y pestañas/foco/historia de WS13, el contrato de errores de API/red de WS11 (transitivo vía WS13) y su recibo G_UI_READ. Produce el panel de errores bajo `views/workspace/errors/` y pruebas que distinguen backend ausente de fallo CDN; reintento conserva pestañas/foco/historia; fallo CDN se declara límite sin exigir recuperación offline.
- **WS15.2:** consume las mismas rutas de lectura y su recibo G_UI_READ. Produce orientación bajo `views/workspace/orientation/`: muestra ruta absoluta y `deskops init <ruta>` sin mutar; tras init externo, refrescar muestra el desk real.

Al no haber dependencia entre hermanos, no se transfieren nada: la integración conjunta se valida porque ambos escriben bajo `views/workspace/` sin solaparse y comparten las rutas de WS11. Si falta contrato, API o recibo, el ejecutor se detiene y registra el hueco con repo dueño, sin crear sustituto. La aceptación conjunta del agregado solo se comprueba cuando ambas aceptaciones hijas existen.

## FUTURO

WS16 realizará la validación humana con el corpus WS40. WS11 producirá el contrato de navegación/errores. El receptor P01 emitirá actas por delta en graph_ui. La promoción fijará TaskDoc, archivos y pruebas. G_HUMAN_READ no bloquea este trabajo de solo lectura.
