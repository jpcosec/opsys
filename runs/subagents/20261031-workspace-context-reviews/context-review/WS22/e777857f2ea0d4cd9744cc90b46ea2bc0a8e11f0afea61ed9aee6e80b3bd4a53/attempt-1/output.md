REFORMULACION
WS22 es un nodo de implementación, no agregado, en graph_ui. Debe representar el Board real de deskops como trabajo navegable: lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc, abriendo el mismo TaskDoc y sus pills/átomos en el lector. Resultado: vistas en `frontends/mindmap/views/workspace/board/` y tests, con identidades, selección y links comunes con el lector; estados/lifecycle desde deskops, no dag.yaml. Límites: lectura, sin drag-and-drop que sustituya workflow, sin duplicar tareas ni presentar predicado satisfecho como test. Depende de WS13 y WS09; requiere G_UI_READ por delta.

AMBIGUEDADES
1. «abriendo en el lector los mismos TaskDoc y sus pills/átomos referenciados». WS13 declara lector de documento/fuente, contexto, enlaces, tabs/historia y explorador, no representación de conocimiento/pills/átomos; WS24 sí. Como WS24 no figura en `depends_on` (solo WS13 y WS09), el ejecutor debe inventar si implementa ese renderizado, lo deja en handoff o lo omite, y cómo validarlo.

DRY-RUN
Un ejecutor futuro leería dag.yaml (WS22, WS13, WS09, G_UI_READ), guía, brief, alcance, decisiones, cobertura, reconciliación, salida de WS09 y entrega/contrato de WS13, y las rutas deskops de Board/task/gates/next. Cambios: crear en `frontends/mindmap/views/workspace/board/` las vistas lista, tablero por estado y dependencias, con tests; reutilizar identidades, selección y links de WS13; leer estados/lifecycle de deskops; no usar dag.yaml como estado. Consumiría WS13/WS09 y el acta per-delta de G_UI_READ. Validaría con store temporal real o corpus WS40: mismo TaskDoc desde las tres vistas, selección/links comunes, estados/lifecycle coincidentes con deskops y ningún gate/predicado presentado como test. Si faltan WS13, WS09, acta o soporte para pills/átomos, se detendría y registraría el hueco con repo dueño, sin sustituto.

FUTURO
WS09 entrega filas del catálogo; WS13 entrega lector, selección/links y contrato WS11; P01 emite el acta G_UI_READ del delta; el TaskDoc de promoción fija archivos, pills y evidencia; WS16/WS30 validan lectura/operación. La promoción sigue no autorizada y el gate pendiente es intencional.
