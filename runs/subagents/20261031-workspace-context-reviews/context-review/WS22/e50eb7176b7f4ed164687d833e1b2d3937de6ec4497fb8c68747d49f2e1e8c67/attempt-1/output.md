## REFORMULACION

**Propósito:** que el lector del workspace muestre el Board real como trabajo navegable, no como una lista aislada ni como sustituto del workflow.

**Resultado:** tres representaciones —lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc— que abren el mismo TaskDoc en el lector, con selección y enlaces comunes, y que muestran sus pills/átomos referenciados. Los estados y condiciones de lifecycle se leen de deskops, no de `dag.yaml`.

**Repo y límites:** `owner_repo: graph_ui`; salidas en `frontends/mindmap/views/workspace/board/; tests/`. No implementar drag-and-drop de status, no duplicar tareas y no presentar un predicado satisfecho como test aprobado. La promoción sigue no autorizada.

## AMBIGUEDADES

1. **“como lista, como tablero agrupado por estado y con las dependencias declaradas en el TaskDoc”** frente a **“Las tres representaciones (lista, tablero y dependencias)”**. El alcance usa “con las dependencias”, lo que puede leerse como panel integrado en lista/tablero; la aceptación exige tres representaciones. Obliga a inventar si “dependencias” es una tercera vista independiente o un panel compartido, y con ello la estructura y la selección que debe validarse.

## DRY-RUN

Un ejecutor futuro leería: la fila de Board en `vistas.md` de WS09; la salida/contrato de navegación de WS13 y WS11; el payload real de Board, TaskDoc y lifecycle expuesto por deskops; y los patrones de `views/workspace/` y tests existentes en graph_ui.

Cambios previstos: crear el módulo de Board bajo `frontends/mindmap/views/workspace/board/`, consumir las rutas públicas de Board/tarea/lifecycle, enlazar selección y foco con el lector, y añadir tests de las tres representaciones. No tocaría status ni implementaría promoción.

Dependencias y gates: WS13 y WS09 deben estar disponibles; G_UI_READ exige recibo `per_delta` del delta concreto, no aceptación conjunta. Si falta contrato o ruta, se detiene y registra el hueco con repo dueño.

Validación esperada: tests de que lista, tablero y dependencias abren el mismo TaskDoc; estados/lifecycle provenientes de deskops; links y selección comunes; ausencia de mutación de status. La aceptación humana revisa el resultado, no solo la suite.

## FUTURO

El TaskDoc de promoción fijará archivos, textos y escenarios de prueba. El receptor P01 emitirá el acta G_UI_READ del delta en graph_ui. WS26 y otros consumidores no forman parte de este nodo.
