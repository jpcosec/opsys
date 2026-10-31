REFORMULACION
Propósito: integrar en graph_ui un delta sobre la tarea Changes que haga comprobable el impacto de una mutación del store. Resultado: vista que muestra documento afectado, relaciones entrantes/salientes a 1 hop vía API de grafo de sldb y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, agrupados por comando, con enlace a reparación documentada; sin reparación automática ni CST/Kimun. Repo: graph_ui; salida en `frontends/mindmap/views/workspace/changes/`, rutas de integridad según WS11 y tests. Límites: solo lectura (G_UI_READ), pruebas en store temporal real, extensión independiente que no bloquea lector/manual; promoción no autorizada.

AMBIGUEDADES
1. «errores = hallazgos de esos tres comandos, agrupados por comando»: no define cómo obtiene graph_ui esos hallazgos (ejecución CLI, API existente, artefacto) ni contrato de formato/severidad. Con owner_repo graph_ui y salida solo frontend, obligaría a inventar el canal y el parser, o a suponer una API no nombrada.
2. «Una mutación real en el store temporal muestra documento afectado […] y errores»: no define cómo se atribuye cada hallazgo de los tres comandos al documento afectado; pueden ser hallazgos de store. Obligaría a inventar el criterio de atribución y, con ello, la aceptación comprobable.

DRY-RUN
Lecturas previstas: dag.yaml, contratos WS15/WS24, WS11, API de grafo de sldb, documentación de los tres comandos, tarea Changes actual y código `changes/`. Cambios previstos: vista/frontend, rutas según WS11 y tests; sin reparación ni backend nuevo. Dependencias: WS15 y WS24, con WS11/WS12/WS03 transitivos; G_UI_READ por delta. Validaciones futuras: prueba con store temporal real (mutación, documento, vecindad 1 hop, hallazgos agrupados y enlaces), caso degradado y acta humana. Nada ejecutado.

FUTURO
- WS11 produce el contrato de navegación/rutas que WS29 consume; WS03/WS24 aportan API de grafo e inventario; WS15 la superficie de error; WS06/WS12 fijan la integración con el ticket Changes.
- El solicitante decide la aceptación G_UI_READ del delta y la promoción; WS40 puede aportar corpus. No son ambigüedades de este encargo.
