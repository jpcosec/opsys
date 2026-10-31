## REFORMULACION

- **Propósito**: entregar, en `graph_ui`, la orientación para un proyecto sin desk dentro del lector del workspace.
- **Resultado**: al abrir un proyecto sin desk se muestra orientación, la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`; nunca se inicializa por GET; tras un `init` externo real, refrescar lectura muestra el desk real.
- **Repo dueño**: `graph_ui` (`frontends/mindmap/views/workspace/orientation/`; rutas de lectura según contrato WS11; `tests/`).
- **Límites**: no crear desks desde UI; solo orientación y handoff al CLI; sin mutaciones; aceptación pendiente de recibo G_UI_READ por delta; implementación no autorizada aún.

## AMBIGUEDADES

Ninguna.

El resultado y la aceptación son comprobables (proyecto sin desk → orientación/destino sin mutar; `init` externo + refresco → desk real). El repo y el actor del `init` están definidos; las rutas de lectura remiten a WS11, que es productor nombrado con regla de hueco en alcance.md; WS13 cubre el lector como prerrequisito directo. “Nunca inicializar por GET” y alcance.md cierran el límite. Los textos exactos de pantalla y casos de prueba quedan al TaskDoc, y el gate G_UI_READ pendiente es intencional (`evaluation: per_delta`, sin recibos aún).

## DRY-RUN (sin ejecutar)

- **Lecturas previstas**: `dag.yaml` (WS13, WS15, gates), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`; luego código existente del workspace (`workspace_routes.py`, `workspace-view.js`, errores de store inexistente) para situar la vista `orientation/`.
- **Cambios previstos**: nueva vista/carpeta de orientación y pruebas de la doble condición de aceptación; consumo de rutas de lectura existentes, sin endpoint de escritura.
- **Dependencias**: WS13 (agregado) y, transitivamente, WS11 (contrato de rutas); G_UI_READ por delta.
- **Validaciones futuras**: prueba técnica con proyecto temporal sin desk; verificación de no mutación; `deskops init` externo y refresco; guion humano WS16 sobre corpus WS40.

## FUTURO

- **WS11**: produce el contrato de rutas de lectura y el acta de recepción G_UI_READ por delta.
- **Humano (solicitante)**: firma el recibo del delta en repo receptor; ejecuta `init` externo en la prueba.
- **WS16**: valida el recorrido UF10 sobre corpus WS40.
- **WS40**: aporta corpus e instrucciones de arranque cuando exista.
