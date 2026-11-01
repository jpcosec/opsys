REFORMULACION
Encargo: que un proyecto sin desk, abierto en el host graph_ui, muestre una orientación de solo lectura con la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`, sin inicializar por GET. Resultado: vista/servicio de orientación en `frontends/mindmap/views/workspace/orientation/`, rutas de lectura según contrato WS11 y pruebas; tras init externo y refresco, el lector muestra el desk real. Repo dueño: graph_ui. Límites: solo lectura; no crear desk, store ni mutar; depende de WS13 y de G_UI_READ por delta; no sustituye los errores de lectura de WS15.1.

AMBIGUEDADES
ninguna

DRY-RUN
Nodo de implementación, no agregado. Lecturas: contrato WS11 (rutas de lectura), base WS13 en graph_ui (`workspace_routes.py`, `workspace-view.js`, `workspace.mjs`), semántica existente de `deskops init <ruta>` y recibo G_UI_READ del delta. Cambios previstos: módulo de orientación bajo output_scope, enganche en el shell del workspace para el estado sin desk, ruta de lectura que exponga ruta absoluta/estado y tests; sin escrituras. Dependencias: WS13 aporta el host lector; WS11 las rutas; G_UI_READ el acta del receptor P01. Si falta WS11 o el recibo, detenerse y registrar el hueco con repo dueño; no crear sustituto. Validación esperada: proyecto temporal sin desk muestra orientación, ruta absoluta y comando sin crear desk/store ni efecto por GET; se ejecuta `deskops init` por CLI externa y, tras refrescar, aparece el desk real. Comprobar además que un store no disponible no se confunde con «sin desk» y que las pruebas no mutan nada.

FUTURO
WS11 produce el contrato de rutas de lectura; el receptor P01 emite el acta G_UI_READ del delta concreto; WS15 cierra cuando WS15.1 y WS15.2 cumplen; WS16 valida UF10 con el corpus. La promoción decide el ticket receptor y evita duplicar implementación.
