## REFORMULACION
WS22 encarga, en `graph_ui`, representar el Board real dentro del lector como lista, tablero agrupado por estado y vista de dependencias declaradas en el TaskDoc, abriendo los mismos TaskDoc y sus pills/átomos referenciados. El resultado son tres representaciones navegables sobre una selección y enlaces comunes con el lector, tomando estados y condiciones de lifecycle de deskops —no de `dag.yaml`—, sin duplicar tareas ni presentar un predicado satisfecho como test aprobado. Repo dueño: `graph_ui` (`frontends/mindmap/views/workspace/board/; tests/`). Límites: no sustituir el workflow con drag-and-drop de status; lectura sujeta a `G_UI_READ`; depende de WS13 y WS09.

## AMBIGUEDADES
1. «tablero agrupado por estado» junto a «estados y condiciones de lifecycle leídos de deskops (Board, lifecycle)»: no fija si la agrupación usa el status de la tarea del Board, el `current_node`/lifecycle u otro campo, ni qué hacer cuando ambos difieren. Obliga a inventar la clave de agrupación y su precedencia.
2. «Representar Board real» no identifica qué Board: el del desk actual, uno seleccionado o varios en lectura multidesk (P07/WS41). Obliga a inventar el alcance de lectura y la resolución del desk origen.

## DRY-RUN
Un ejecutor futuro leería el nodo WS22, su TaskDoc `task-ws22.md`, las salidas de WS13 (lector) y WS09 (catálogo), las rutas existentes de deskops (`GET /api/desk/board`, `/task`) y los componentes actuales de `views/workspace/`. Cambiaría únicamente `views/workspace/board/` y tests: añadiría lista, tablero y dependencias, reutilizando selección/enlaces del lector. Consumiría `G_UI_READ` como recibo por delta del receptor P01; sin él se detendría. Validaría que las tres representaciones abren el mismo TaskDoc, que la selección/links coinciden con el lector, que no duplica tareas y que los estados vienen de deskops. Errores esperados: Board o lifecycle ausente, enlaces a TaskDoc/pills no resolubles y estado de agrupación no definido; se registrarían como hueco o modo degradado, sin inventar datos.

## FUTURO
WS09 entrega el catálogo de renderizaciones; WS13, el lector y su contrato de navegación; el receptor P01 emite el acta `G_UI_READ` por delta. La promoción fijará archivos, evidencias y pruebas concretas. WS30 validará el recorrido humano.
