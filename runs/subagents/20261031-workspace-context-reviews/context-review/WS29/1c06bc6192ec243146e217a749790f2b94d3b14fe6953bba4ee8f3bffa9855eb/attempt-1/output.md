REFORMULACION  
WS29 es un nodo de implementación (delivery, no agregado) en graph_ui. Propósito: extender la tarea Changes actual para integrar Changes e impacto comprobable. Resultado: vista/rutas en `frontends/mindmap/views/workspace/changes/` y tests que muestren, ante una mutación real en store temporal, el documento afectado, relaciones entrantes/salientes a 1 hop vía API de grafo de sldb y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check` agrupados por comando, enlazando cada hallazgo al comando documentado. Límites: no reparación automática, no CST/Merkle Kimun, no bloquea lector/manual, no duplica el ticket Changes; promoción no autorizada. Depende de WS15/WS24 y requiere G_UI_READ; rutas según contrato WS11.

AMBIGUEDADES  
Ninguna. Las referencias a WS11, a los comandos y a la documentación de repo dueño nombran productor/destino; archivos y pruebas detallados quedan al TaskDoc de promoción.

DRY-RUN  
Lecturas: `dag.yaml`, `task_file`, borrador externo Changes, contrato WS11, matriz WS06/reconciliación, salidas de WS15/WS24, documentación de los tres comandos y API de grafo de sldb. Cambios previstos: crear la vista Changes en el `output_scope`, integrar la ruta de integridad que fije WS11 y añadir tests; no reparar. Dependencias/gates: consumir WS15, WS24 y WS11; G_UI_READ se recibe por delta concreto de WS29 (`per_delta`), sin exigir otros. Si falta contrato/API/dato: detener y registrar hueco con repo dueño, sin sustituto. Validación esperada: mutación real en store temporal; documento afectado; relaciones entrantes/salientes a 1 hop; hallazgos agrupados por comando y enlace al comando documentado; pruebas en store temporal real (o corpus WS40 si existe).

FUTURO  
WS11 produce las rutas/contrato de integridad; WS15 y WS24 sus deltas de lectura/errores y conocimiento/grafo; WS06 mantiene la matriz; WS40 puede aportar corpus. El receptor humano P01 emite el acta G_UI_READ por delta. La promoción no autorizada decide TaskDoc, archivos, pills, evidencia y preflight; el ticket Changes se prepara/promueve en su repo.
