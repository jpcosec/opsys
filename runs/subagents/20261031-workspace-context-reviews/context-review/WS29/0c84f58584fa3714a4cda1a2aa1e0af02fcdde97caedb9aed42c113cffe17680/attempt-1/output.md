REFORMULACION
Propósito: integrar Changes con impacto comprobable de una mutación del store. Resultado: un delta sobre la tarea Changes actual en graph_ui que muestra documento afectado, relaciones entrantes/salientes a 1 hop y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, agrupados y enlazados a su documentación; sin reparación automática y con pruebas en store temporal real. Repo dueño: graph_ui. Límites: no CST/árbol Kimun, no duplicar Changes, no bloquea lector/manual; promotion no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: TaskDoc WS29, contrato WS11, API de grafo de sldb/auditoría, documentación de los tres comandos, tarea Changes y código de workspace/tests. Cambios previstos: vista en `frontends/mindmap/views/workspace/changes/` y tests; rutas de integridad según contrato WS11. Dependencias: WS15 (errores/degradado), WS24 (grafo/backlinks), G_UI_READ por delta, contrato WS11 y API de grafo de sldb. Validaciones futuras: crear store temporal real, mutarlo, comprobar documento afectado, relaciones a 1 hop y hallazgos agrupados con enlace al comando correspondiente; comprobar que no repara automáticamente ni usa CST/Kimun.

FUTURO
WS11 produce contrato y recibo G_UI_READ de WS29; WS24/WS03 aportan API de grafo; WS15 aporta tratamiento de errores/degradación; WS06/TaskDoc fijan ticket receptor, archivos, pills y pruebas; el humano acepta el delta por efecto concreto. Nada de esto autoriza implementación.
