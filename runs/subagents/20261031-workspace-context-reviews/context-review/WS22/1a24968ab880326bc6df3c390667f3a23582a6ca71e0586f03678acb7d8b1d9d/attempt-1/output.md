REFORMULACION
Propósito: encargo de planificación para que WS22 implemente en graph_ui una representación navegable del Board real. Resultado: tres representaciones —lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc— que abren el mismo TaskDoc y sus pills/átomos en el lector, con selección y links comunes; estados y lifecycle se leen de deskops, no de dag.yaml. Repo: graph_ui; salida en `frontends/mindmap/views/workspace/board/` y `tests/`. Límites: no duplicar tareas, no presentar predicado satisfecho como test aprobado, no reemplazar workflow con drag-and-drop de status; promoción no autorizada; depende de WS13 y WS09 y requiere G_UI_READ.

AMBIGUEDADES
1. «con las dependencias declaradas en el TaskDoc» / «Las tres representaciones (lista, tablero y dependencias) abren el mismo TaskDoc»: no se define qué debe mostrar la representación de dependencias (aristas, lista, dirección, agrupación) ni qué hacer si el TaskDoc no las declara. Obliga a inventar el resultado y permite aceptar una vista vacía.
2. «no duplicar tareas ni presentar predicado satisfecho como test aprobado»: «predicado» no está definido en las fuentes. Obliga a inventar qué elemento de Board/lifecycle es predicado y cómo comprobar que no se confunde con un test aprobado.
3. «matriz WS06 llega de forma transitiva por WS11/WS12»: WS12 no figura en `depends_on` ni en la cadena visible (WS22→WS13→WS11; WS22→WS09). Obliga a decidir si falta una dependencia o si la matriz no es requisito de este nodo.

DRY-RUN
Lecturas: nodo WS22, guía, brief, alcance, decisiones, cobertura y reconciliación; WS13/WS09 solo como contratos. No se ejecuta nada. Cambios previstos: renderers de lista, tablero y dependencias en graph_ui, enlaces al lector y lectura de Board/lifecycle de deskops; `tests/`. Dependencias: WS13, WS09, G_UI_READ pendiente de WS11; matriz WS06 por verificar. Validaciones futuras: que las tres representaciones abran el mismo TaskDoc; estados/lifecycle desde deskops; no duplicación; no confundir predicado con test; promoción no autorizada y preflight task-only.

FUTURO
WS13 produce lector, foco e historia. WS09 produce el catálogo con contrato/error/estado de Board. WS11 resuelve G_UI_READ y acepta el delta; WS07 designa al responsable graph_ui. WS30 ejecuta la validación humana. La promoción y el TaskDoc los fija el flujo de promoción; el humano decide Pxx y autoriza o no.
