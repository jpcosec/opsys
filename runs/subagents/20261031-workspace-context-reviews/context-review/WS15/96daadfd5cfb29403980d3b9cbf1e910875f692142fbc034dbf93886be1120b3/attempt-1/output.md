# WS15 — Revisión de encargo

## REFORMULACION
Propósito: agregar en el lector workspace de graph_ui dos capacidades de honestidad y arranque: mostrar errores de lectura/modo degradado (WS15.1) y orientar un proyecto sin desk (WS15.2). Resultado: un agregado no ejecutable que se cumple cuando ambos hijos cumplen su aceptación; sus dependientes (WS16, WS29) siguen dependiendo de este ID. Repo dueño: graph_ui. Límites: no implementa otro lector ni guardado; reutiliza la lectura Markdown de WS13.1; el contrato WS11 fija errores de API y estados de red; CDN se declara límite actual sin prometer offline; nunca inicializa por GET.

## AMBIGUEDADES
Ninguna. El título «modo degradado» está definido en el glosario de brief.md; el contrato WS11 y el corpus WS40 tienen productor nombrado; los gates per_delta pendientes son intencionales y no bloquean desarrollo aislado.

## DRY-RUN
Al ser `aggregate`, WS15 no se ejecuta: termina cuando terminan sus hijos, que sí lo cumplen.

- WS15.1 produce `views/workspace/errors/`, tipificación HTTP/red/JSON en `shell/api.js` (conservando `error.body`) y tests; consume la lectura de WS13.1, el contrato WS11 y su recibo G_UI_READ. Transfiere: paneles de error que no borran historial, reintento que preserva pestañas/foco/historia y diagnóstico CDN con prueba de no carga.
- WS15.2 produce `views/workspace/orientation/` y tests; consume el contrato WS11, el comando `deskops init` (ya existente, solo documentado en pantalla) y su recibo G_UI_READ. Transfiere: orientación con ruta absoluta sin mutar y refresco que muestra el desk tras init externo.
- Validación conjunta sobre el workspace integrado: backend caído → error declarado y recuperación al restaurarlo; proyecto sin desk → orientación sin mutación y lectura real tras init; fallo CDN → diagnóstico visible. Errores de validación se registran por hijo con su repo; el agregado no añade prueba propia ni duplica implementación.

## FUTURO
WS11 publica el contrato de errores/estados; el receptor P01 emite actas G_UI_READ por delta (WS15.1 y WS15.2 por separado); WS16 ejecuta la validación humana de UF10/UF07 sobre el corpus WS40; WS29 consume después. Nada de esto autoriza promoción ni implementación.
