## REFORMULACION

Encargo de WS15.2 («Orientar proyecto sin desk», delivery, repo graph_ui): cubrir UF10 mostrando, ante un proyecto sin desk, una orientación con la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`. Resultado: pantalla de orientación dentro del lector y refresco que muestra el desk real tras un init ejecutado fuera de la UI. Límites: nunca inicializar por GET ni mutar nada; salidas en `frontends/mindmap/views/workspace/orientation/`, rutas de lectura fijadas por el contrato WS11 y `tests/`. Depende de WS13 (lector agregado, no ejecutable por sí mismo) y del gate G_UI_READ, `per_delta`.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Lecturas previas (sin ejecutar): nodo y aristas en `dag.yaml`; `reconciliacion.md` y Board de graph_ui para no duplicar C-12 ni el 503 de C-06; `workspace_routes.py`, `workspace-view.js`, `workspace.mjs`; documentación del comando `deskops init`. El ejecutor no adoptaría `frontends/workspace/` (C-29).

Cambios previstos: vista bajo `views/workspace/orientation/`, registrada en el lector; ruta de lectura que comunique ausencia de desk, reutilizando el manejo de errores existente y sin confundirla con backend caído; textos, archivos exactos y tests los fija el TaskDoc de promoción dentro de la aceptación. Integración con `views/workspace/` en serie con C-14/C-28 si comparten archivos.

Dependencias y gates: WS13 aporta lector, foco e historia; WS11 (transitiva, vía WS13) fija las rutas de lectura. G_UI_READ se consume con el acta del receptor P01 correspondiente a este delta, no con la de otros nodos. Si la ruta contratada no distingue «sin desk», el ejecutor se detiene y registra el hueco con repo dueño (graph_ui), sin crear sustituto.

Errores y validación esperada: proyecto temporal sin desk; abrir la UI no crea desk ni dispara GET mutante; ejecutar `deskops init <ruta>` por CLI; refrescar y comprobar nodos reales; revisar por separado sin-desk, backend ausente y ruta ilegible.

## FUTURO

El receptor P01 emite el acta G_UI_READ con commit/blob; no la escribe el Executor. Una persona o el CLI ejecuta `deskops init` fuera de la UI. El TaskDoc de promoción fija archivos, textos y escenarios, y WS16 valida en Taller.
