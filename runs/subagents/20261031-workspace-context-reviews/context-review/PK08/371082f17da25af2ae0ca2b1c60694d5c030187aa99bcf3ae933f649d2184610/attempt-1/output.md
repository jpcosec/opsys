REFORMULACION
Propósito: revisar PK08 como encargo de planificación agregado del ramal Scion. Resultado: veredicto sobre si su aceptación permite comprobar la revisión vigente o el bloqueo explícito de cada hijo directo sin inventar criterios. Repo: deskops para el plan; hijos con owner_repo deskops/graph_ui. Límites: no revisar los bloques edge de los vecinos, no ejecutar `context_review.py`, no evaluar calidad de producto, no resolver Pxx ni dar gates por satisfechos.

AMBIGUEDADES
Ninguna. La aceptación remite a `context_review.py status`, a input/contrato actuales y a disposición guardada; los gates pendientes son intencionales según la guía. PK08 no requiere `owner_repo` propio por ser agrupación de revisión.

DRY-RUN
Lecturas: input, guía, nodo PK08, edges de WS32–38/WS44, decisiones.md, alcance.md y cobertura.md. Cambios previstos: ninguno; solo el veredicto de revisión. Dependencias: estado de context_review de cada hijo directo; WS05/WS07/WS44 para identidad, inventario, probe y bloqueo Scion. Validaciones futuras: cada hijo debe tener revisión vigente con input y contrato actuales, o `blocked` con responsable y dependencia en su disposición; no se ejecuta nada.

FUTURO
WS07 designa al operador Scion y resuelve Pxx; WS05 produce inventario; WS44 produce el probe y G_SCION; los revisores de cada hijo guardan su disposición; la promoción/cierre de PK08 verifica el estado con `context_review.py`. El humano decide las propuestas pendientes.
