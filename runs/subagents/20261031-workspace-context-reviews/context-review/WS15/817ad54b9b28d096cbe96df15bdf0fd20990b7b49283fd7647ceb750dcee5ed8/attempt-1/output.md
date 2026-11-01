## REFORMULACION

WS15 es un nodo **aggregate** de planificación, no ejecutable, en `graph_ui`. Propósito: cubrir errores de lectura/modo degradado (WS15.1) y orientación de proyecto sin desk (WS15.2). Resultado: ambos hijos con su aceptación cumplida; WS15 no produce código propio y su `output_scope` agrega las salidas de sus hijos. Depende de WS13 (lector base), de sus hijos y de G_UI_READ (per_delta). Límites: no duplica implementación, no infiere cierre por commit (`reconciliation`) y su promoción no está autorizada.

## AMBIGUEDADES

1. «node_role: aggregate» / «Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación» frente a `requires: [G_UI_READ]` y `scope_nodes` del gate que enumera WS15 con `accepted_scope_nodes: []`. Obligaría a inventar si el cierre de WS15 exige acta propia o basta el recibo de cada hijo; la guía («Cada nodo usa solo su recibo; ausencia de otro delta no bloquea este») apunta a lo segundo, pero el gate no lo dice.

## DRY-RUN

No se ejecuta: es agregado. Un verificador futuro recorrería:

- **WS15.1**: panel de errores en `frontends/mindmap/views/workspace/errors/` y `tests/`; consume el contrato WS11 (errores de API, red sin respuesta, fallo CDN) y reutiliza la lectura Markdown de WS13.1. Valida reintento conservando pestañas/foco/historia y diagnóstico CDN sin prometer offline.
- **WS15.2**: `frontends/mindmap/views/workspace/orientation/` y `tests/`; ruta absoluta, comando `deskops init <ruta>` documentado, sin mutar por GET y refresco tras init externo.

Dependencias consumidas: WS13 y recibos G_UI_READ por delta concreto. Si falta un recibo o el contrato WS11, se detiene y registra el hueco con repo dueño `graph_ui`, sin sustituto. Validación conjunta: ambas aceptaciones probadas con pruebas de comportamiento; entonces WS15 cierra.

## FUTURO

El receptor P01 emite las actas por delta en el repo receptor; WS16 ejecuta la validación humana de lectura/diagnóstico/arranque consumiendo WS15; WS29 depende de WS15. Si las pruebas fallan, el supervisor del repo receptor atribuye la causa y abre la corrección; ninguna decisión de este nodo autoriza implementación ni mutaciones.
