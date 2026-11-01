## REFORMULACION
**Propósito:** encargar la representación navegable del Board real dentro del lector workspace. **Resultado:** lista, tablero agrupado por estado y dependencias declaradas, abriendo el mismo TaskDoc; selección/enlaces comunes con el lector; estados y lifecycle leídos de deskops, no de `dag.yaml`. **Repo:** graph_ui, con `output_scope` en `frontends/mindmap/views/workspace/board/; tests/`. **Límites:** no reemplazar workflow con drag-and-drop; no duplicar tareas; no presentar predicado satisfecho como test aprobado. **Dependencias:** WS13 (lector) y WS09 (catálogo de renderizaciones); gate G_UI_READ por delta.

## AMBIGUEDADES
1. «selección y links comunes con lector» frente a `output_scope: frontends/mindmap/views/workspace/board/; tests/`. Obliga a inventar si “comunes” exige modificar archivos del lector fuera del alcance declarado o solo reutilizar su comportamiento sin tocarlos.
2. «abriendo en el lector los mismos TaskDoc y sus pills/átomos referenciados». La aceptación solo exige abrir el mismo TaskDoc; no define qué significa abrir un pill/átomo, en qué superficie ni con qué renderer, y WS24 (vista de conocimiento) no figura como dependencia. Obliga a inventar esa interacción o a exceder el resultado comprobable.
3. «con las dependencias declaradas en el TaskDoc». No se especifica el campo fuente (`depends_on`, `references`, `files`) ni la representación esperada; obliga a inventar qué dependencia se dibuja y cómo se valida.

## DRY-RUN
**Lecturas previstas:** nodo WS22, guía, brief, alcance, decisiones, cobertura, reconciliación y referencia externa de `workspace_routes.py`; `task_file` al promover. **Cambios previstos:** componentes de lista/tablero/dependencias bajo `board/` y pruebas; sin ejecutar. **Dependencias:** WS13 aporta lector, foco/historia y enlaces; WS09 aporta filas de renderización; deskops aporta lectura de Board/tarea/lifecycle. **Validaciones futuras:** tres representaciones abren el mismo TaskDoc; estados desde deskops; sin duplicados; sin drag-and-drop; recibo G_UI_READ por delta; prueba en corpus/Board real.

## FUTURO
WS09 produce el catálogo; WS13, el lector integrado. El receptor P01 emite el acta G_UI_READ del delta concreto. WS30 valida el recorrido humano. La promoción fija archivos, pruebas y textos dentro de esta aceptación. WS26 depende de WS22.
