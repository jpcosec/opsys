## REFORMULACION

WS29 encarga a graph_ui un delta sobre el ticket Changes draft: mostrar en el workspace, agrupados por comando, hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, y el impacto de una mutación real en un store temporal: documento afectado y relaciones entrantes/salientes a 1 hop según la API de grafo de sldb. Salida: rutas de integridad según contrato WS11, vista en `frontends/mindmap/views/workspace/changes/` y tests. Límites: reparación solo por enlace al comando documentado de su repo dueño, sin CST/Merkle Kimun, sin duplicar el ticket ni ejecución paralela con edición, y no bloquea lector/manual. Requiere G_UI_READ por delta; depende de WS15 y WS24. Nodo delivery, no agregado.

## AMBIGUEDADES

1. «Una mutación real en el store temporal muestra documento afectado»: no define cómo se identifica el documento afectado ni qué mutación usar. Obliga a inventar si es entrada del usuario, diff o hash stale, y cuál es el resultado observable.
2. «y errores» / «errores = hallazgos de esos tres comandos, agrupados por comando»: no fija si el pase exige hallazgos de los tres comandos, de al menos uno, o admite cero. Obliga a inventar la condición de aceptación.

## DRY-RUN

Leería el draft Changes (sha 433ecb51…), `workspace_routes.py`, `workspace-view.js`, `views/workspace/`, la API de grafo de sldb y el contrato WS11. Extendería el ticket Changes (no tarea paralela); añadiría rutas de integridad según WS11; una vista bajo `views/workspace/changes/` agrupada por comando, con enlaces a la documentación de sldb/deskops; y tests con store temporal real que muten y comprueben documento afectado, vecindad 1 hop y hallazgos. Consume WS15 (errores/degradación), WS24 (vista genérica/grafo) y G_UI_READ (recibo por delta). Si falta la ruta/contrato WS11 o la API de grafo: detenerse, registrar el hueco con repo dueño y dejar la operación no disponible; sin reparación automática. Validación futura: tests con store temporal y acta del delta.

## FUTURO

El receptor P01 emite el acta G_UI_READ por delta; WS06 promueve/ajusta el ticket Changes; WS11 fija las rutas de integridad; el TaskDoc de promoción fija archivos, escenarios y textos; la validación humana del delta es externa.
