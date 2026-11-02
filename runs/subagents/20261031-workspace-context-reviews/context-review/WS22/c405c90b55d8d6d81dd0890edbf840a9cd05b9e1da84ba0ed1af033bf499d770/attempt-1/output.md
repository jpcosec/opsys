REFORMULACION

WS22 es un nodo de implementación en `graph_ui`: representar el Board real de deskops como trabajo navegable mediante lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc, abriendo en el lector el mismo TaskDoc y sus pills/átomos referenciados. Resultado: tres representaciones con identidades de tarea coherentes, selección/enlaces comunes con el lector y estados/lifecycle leídos de deskops. Repo: `graph_ui`; `output_scope`: `frontends/mindmap/views/workspace/board/` y `tests/`. Límites: no reemplazar el workflow con drag-and-drop de status, no duplicar tareas ni usar `dag.yaml` como fuente de estados; G_UI_READ per-delta pendiente es intencional y la promoción no está autorizada.

AMBIGUEDADES

1. «selección y links comunes con lector»: obligaría a inventar qué significa «comunes» —si se comparte foco, URL/historia, resolución de enlaces o las tres— y mediante qué contrato concreto de WS13 se integra el Board en el lector. El input no define esa integración ni la operación que debe consumirse.

DRY-RUN

Leería `deskops_routes.py` (`GET /api/desk/board`, `/api/desk/task`), `deskops-view.js`, el lector de `views/workspace/` y el modelo TaskDoc/Board. Consumiría de WS13 selección, historia y enlaces del lector; de WS09, el catálogo de renderizaciones. Crearía componentes en `views/workspace/board/` para lista, tablero por estado y dependencias, más tests. No tocaría status ni crearía TaskDocs. Gate: G_UI_READ por delta; sin acta no habilitaría el delta. Si WS09 o WS13 no entregan su contrato, pararía y registraría el hueco. Validaría que las tres representaciones abren el mismo TaskDoc, que estados y condiciones vienen de deskops, que no hay tareas duplicadas y que un predicado satisfecho no se muestra como test aprobado.

FUTURO

WS13 produce el lector con foco/historia/enlaces; WS09 el catálogo de renderizaciones; el receptor P01 emite el acta G_UI_READ por delta; WS30 realizará la validación humana; WS26 consumirá WS22 para autoría/enrutado. La promoción fijará archivos, pruebas y textos.
