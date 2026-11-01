REFORMULACION
Propósito: integrar en el lector una vista de Changes e impacto comprobable sobre el ticket Changes existente. Resultado: ante una mutación real en un store temporal, mostrar documento afectado, relaciones entrantes/salientes a 1 hop según la API de grafo de sldb y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, agrupados por comando y enlazados al comando documentado; reparar no es automático. Repo dueño: graph_ui. Límites: no CST ni árbol Kimun; no bloquea lector/manual básico; promoción no autorizada; gate G_UI_READ por delta; rutas de integridad sujetas al contrato WS11.

AMBIGUEDADES
1. «Comparte `serve.py`, `views/workspace/` y `docs/workspace-ui.md` con C-14: en serie.» Frente a `depends_on: [WS15, WS24]`, no se declara dependencia ni orden respecto de WS19/C-14. Obliga a inventar si WS29 espera a la tarea de edición o cómo serializa archivos compartidos.
2. «Una mutación real en el store temporal muestra documento afectado, relaciones alcanzadas (...) y errores.» No define cómo se obtiene el «documento afectado» cuando un hallazgo de `doctor` o `drift check` es global o afecta a varios documentos. Obliga a inventar el mapeo hallazgo→documento o a decidir que algunos hallazgos no se muestran.
3. «Una mutación real en el store temporal muestra...» no precisa si la mutación la ejecuta la prueba o la propia vista. Obliga a decidir si se añade una acción de escritura, excediendo el encargo de lectura y G_UI_READ.

DRY-RUN
Lecturas: dag.yaml, referencia externa Changes con SHA, contrato WS11, salidas de WS15/WS24, código actual de `views/workspace/` y tests. Cambios previstos: crear `frontends/mindmap/views/workspace/changes/`, rutas que fije WS11 y tests; no reparar ni introducir CST/Kimun. Dependencias: WS15, WS24 y G_UI_READ con acta del delta concreto. Errores esperados: contrato WS11 ausente → detenerse y registrar hueco; gate pendiente; ticket Changes aún draft; solapamiento con C-14 sin orden declarado. Validación futura: store temporal real, mutación controlada, documento afectado visible, relaciones a 1 hop, hallazgos agrupados por comando y enlaces correctos.

FUTURO
El receptor P01 emite el acta G_UI_READ; WS11 produce el contrato de rutas; la promoción fija TaskDoc, archivos, pruebas y textos; un humano decide la aceptación y el orden con la tarea de edición.
