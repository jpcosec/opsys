## REFORMULACION
Propósito: que el lector del workspace muestre errores de lectura y degradación sin fingir vacío ni perder estado. Resultado: error en el panel afectado, distinguido por la respuesta de la API según WS11; fallo CDN visible; reintento manual que conserva pestañas, foco e historia; tests. Repo: `graph_ui`. Límites: solo `frontends/mindmap/views/workspace/errors/`, rutas definidas por WS11 y `tests/`; sin empaquetado offline ni mutaciones; `G_UI_READ` se recibe por delta.

## AMBIGUEDADES
ninguna. Las referencias al contrato WS11 y a las rutas de lectura tienen productor identificado y regla de parada en `alcance.md`; `G_UI_READ` pendiente es intencional y `per_delta`; los detalles de archivos, textos y pruebas quedan al TaskDoc de promoción.

## DRY-RUN
Lecturas: `dag.yaml` (WS15.1, WS13, WS15, `G_UI_READ`), guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `reconciliacion.md`. Cambios previstos, sin ejecutar: estados/componentes de error y degradación dentro del `output_scope`, más tests. Dependencias: WS13 aporta lector, foco e historia; WS11 aporta contrato/rutas y el recibo `G_UI_READ` por delta. Validaciones futuras: referencia rota, documento ausente, modelo no importable, backend caído, fuente no editable, fallo CDN simulado y reintento que conserva pestañas/foco/historia; distinción de errores por respuesta API; acta de recepción por delta.

## FUTURO
WS11 produce el contrato de navegación/rutas y el recibo `G_UI_READ`; WS13 entrega el lector con foco e historia; WS15 cierra cuando WS15.1 y WS15.2 cumplan; el solicitante humano acepta el delta; WS16 valida el diagnóstico con el corpus WS40. Si falta contrato o permiso, se registra el hueco y la operación queda no disponible.
