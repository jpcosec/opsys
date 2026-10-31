## REFORMULACION

WS19.2 es un nodo de implementación para habilitar el alta y baja de relaciones permitidas por contrato, usando API real y before-image. El resultado esperado es que ambas operaciones persistan y se confirmen tras recargar, y que una relación no permitida o una revisión obsoleta se rechace con error visible. El repo dueño es `graph_ui`; los límites son `frontends/mindmap/views/workspace/relations/`, los endpoints autorizados por el contrato WS12 y `tests/`. No debe crear semántica de relaciones en el componente. La promoción no está autorizada.

## AMBIGUEDADES

ninguna

## DRY-RUN

- Lecturas previstas: nodo WS19.2 y gates; contrato/whitelist producido por WS12; aceptación de WS16; ticket o matriz de integración indicada por WS11/WS12; código existente de relaciones en `graph_ui`; `task-ws19-2.md`.
- Cambios previstos: alta/baja de relaciones dentro del `output_scope`, consumo de endpoints autorizados y pruebas en `tests/`.
- Dependencias: WS12 debe entregar contrato, endpoints y aceptación de mutación; WS16 debe aportar la validación humana de lectura. Aplican `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`.
- Validaciones futuras: persistencia tras recarga; rechazo visible de relación no permitida; rechazo visible por revisión obsoleta; ausencia de semántica de relaciones creada en el componente.

## FUTURO

WS12 produce la whitelist, capacidades, endpoints y aceptaciones de escritura. WS16 produce el acta de lectura humana. El solicitante humano designa responsables y aprueba gates. La promoción fijará archivos exactos, pruebas y textos de pantalla. Nada de esto es ambigüedad del nodo: son entregas de otros nodos o decisiones humanas.
