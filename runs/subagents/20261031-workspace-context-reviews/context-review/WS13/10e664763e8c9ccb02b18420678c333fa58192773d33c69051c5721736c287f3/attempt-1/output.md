## REFORMULACION

**Propósito:** integrar en graph_ui el lector del workspace con lectura de documento/fuente, contexto, enlaces, pestañas/divisiones, historia y foco por documento/nodo, más explorador de documentos modelados y Markdown no modelado.

**Resultado:** agregado de las salidas de WS13.1, WS13.2 y WS13.3; no produce artefacto propio.

**Repo dueño:** graph_ui, sobre el workspace integrado a1b2b22.

**Límites:** nodo agregado no ejecutable; sin índices nuevos ni workspace independiente; reutiliza registry y Code local; depende del contrato WS11 y de G_UI_READ por delta; la base a1b2b22 no acredita la aceptación ampliada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor futuro no editaría código en WS13: leería el nodo y sus hijos, el contrato WS11, reconciliacion.md y workspace_routes.py citado; comprobaría que cada hijo aporta su parte.

- WS13.1 entregaría documento/fuente solo lectura, contexto, enlaces y foco compartido; transfiere identidad y foco del documento.
- WS13.2 entregaría explorador de modelados/no modelados con refresco de catálogo; transfiere apertura sin conocer ID.
- WS13.3 entregaría pestañas, divisiones e historia; consume la identidad de WS13.1/13.2 y preserva foco al volver.

**Cambios previstos:** solo los de los hijos bajo `views/workspace/` (node, explorer, layout).

**Dependencias y gates:** WS11 debe proveer APIs/rutas y resolución; sin contrato o API, se detiene y registra el hueco. G_UI_READ es per_delta: cada hijo espera su recibo; ausente uno, se bloquea ese delta, no los demás.

**Validación conjunta:** abrir documento modelado y no modelado, ver fuente y render, seguir enlaces, alternar representaciones, abrir dos documentos y volver conservando foco/historia, sin segundo workspace ni regresión de Code. Si un hijo no cumple, el agregado no cierra.

## FUTURO

El receptor P01 en graph_ui emite el acta por delta; WS11 fija el contrato de navegación; WS09 el catálogo de representaciones; WS16 la validación humana con corpus WS40. WS14, WS15, WS22, WS24 y WS41 consumen este agregado; WS17 aporta índices. Nada de eso se ejecuta aquí.
