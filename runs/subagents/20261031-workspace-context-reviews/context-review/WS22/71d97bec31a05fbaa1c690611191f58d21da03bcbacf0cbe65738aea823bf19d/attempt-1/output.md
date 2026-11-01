## REFORMULACION
WS22 encarga representar el Board real como trabajo navegable en el lector del workspace: lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc. Resultado esperado: las tres representaciones abren el mismo TaskDoc, comparten selección/enlaces con el lector y muestran estados/lifecycle leídos de deskops, sin duplicar tareas ni convertir un predicado satisfecho en test aprobado. Repo dueño: graph_ui; salida prevista en `frontends/mindmap/views/workspace/board/; tests/`. Límite explícito: no reemplazar el workflow con drag-and-drop de status.

## AMBIGUEDADES
1. «tablero agrupado por estado» junto a «estados y condiciones de lifecycle leídos de deskops (Board, lifecycle)». No fija qué campo o conjunto de estados agrupa las columnas; el ejecutor tendría que inventar si usa status del TaskDoc, `current_node` del lifecycle, gates u otra combinación.
2. `output_scope: frontends/mindmap/views/workspace/board/; tests/` frente a «selección y links comunes con lector». Si la selección y los enlaces comunes viven fuera de `board/`, el ejecutor debe exceder el output_scope declarado o incumplir la aceptación.
3. «no duplicar tareas» no aclara si prohíbe crear tareas desde esta vista, repetir una misma tarea en varias representaciones o duplicar datos; obliga a inventar la conducta esperada.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml` (WS22, WS13, WS09), `reconciliacion.md`, `decisiones.md`, `alcance.md`, el catálogo `vistas.md` de WS09 y las rutas de deskops que exponen Board/lifecycle. Crearía componentes de vista y tests bajo `board/` y reutilizaría la identidad de TaskDoc y los enlaces del lector WS13. Consumiría G_UI_READ mediante acta per-delta del receptor P01; si falta el acta, o WS09 no aporta la fila de Board, se detendría y registraría el hueco, sin sustituto. Validaría con pruebas que lista, tablero y dependencias abren el mismo TaskDoc, que selección/enlaces son comunes, que los estados vienen de deskops y no de `dag.yaml`, y que no se crean ni duplican tareas. La ambigüedad 2 obliga a decidir antes si puede tocar archivos del lector o solo consumir su API.

## FUTURO
WS09 produce el catálogo de renderizaciones; WS13 termina cuando terminan sus hijos y aporta el lector; el receptor P01 emite el acta G_UI_READ del delta; WS30 valida UF04/05 con Board navegable. Nada de eso es ambigüedad del encargo.
