REFORMULACION
- **Propósito:** que graph_ui presente errores de lectura y modo degradado, y oriente un proyecto sin desk.
- **Resultado:** agregado no ejecutable; se cumple cuando WS15.1 y WS15.2 cumplen su aceptación.
- **Repo:** `graph_ui`.
- **Límites:** delta o ticket existente solo tras WS06, nunca duplicado paralelo; `G_UI_READ` pendiente; sin empaquetado offline; nunca inicializar por GET; depende de WS13 y de sus hijos.

AMBIGUEDADES
1. «proyecto sin desk muestra orientación, destino explícito e init CLI» y «muestra orientación y destino sin mutar nada». No se define qué es “destino”: ruta del desk, URL, comando o documento de handoff. Obliga a inventar el contenido mostrado y el criterio para comprobar que el destino es explícito.
2. «modelo no importable, backend caído» no identifica qué modelo ni cómo distinguir ambos fallos. Obliga a inventar la taxonomía de errores y la detección que decide cuál se muestra.

DRY-RUN
- **Lecturas previstas:** dag.yaml (WS15 y aristas citadas), guía, brief, alcance, decisiones, cobertura y reconciliación.
- **Cambios previstos:** ninguno; solo revisión de encargo, sin ejecutar código ni mutar estado.
- **Dependencias:** WS13, WS15.1 y WS15.2; `G_UI_READ` pendiente, resuelto por WS11; WS16 depende de WS15.
- **Validaciones futuras:** aceptación de ambos hijos, evidencia del gate con responsable designado, no solapamiento paralelo y ausencia de inicialización por GET. No ejecutadas.

FUTURO
WS11 produce la aceptación `G_UI_READ`; WS07 designa al responsable de graph_ui; WS06 propone la correspondencia con tareas existentes; WS16 realiza validación humana. La promoción del nodo queda para un nodo posterior o decisión humana, no para esta revisión.
