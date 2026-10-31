## REFORMULACION
Propósito: proponer la correspondencia entre el alcance del plan y los repos dueños, dejando constancia en `reconciliacion.md`. Resultado: una matriz por delta o capacidad, agrupada por repo, con estado «ya cubierto», «extender ticket existente» o «nuevo delta». Repo dueño: `deskops`; salida: `reconciliacion.md`. Límites: no notificar, despachar ni modificar el Board de `graph_ui`; no producir gates ni aprobar deltas indefinidos; no requiere WS05; Scion solo para el ramal E; WS11/12 aceptan por delta.

## AMBIGUEDADES
1. «una fila por delta o capacidad única (varios nodos pueden remitir a la misma fila)»: no fija cuándo un nodo se divide en varias capacidades ni cuándo dos capacidades comparten fila. Obligaría a inventar la granularidad, y la aceptación «una fila por delta o capacidad propuesta» quedaría no comprobable.
2. «agrupada por repo dueño»: no hay regla para un delta que afecte a más de un repo (por ejemplo, `graph_ui` y `sldb`). Obligaría a inventar si se duplica la fila, se elige un repo principal o se descompone.
3. «Registrar en reconciliacion.md la atomización propuesta»: no define qué contiene esa atomización —¿lista de tareas, IDs, dependencias, formato?— y la aceptación no la verifica. Obligaría a inventar su contenido y representación.

## DRY-RUN
Lecturas previstas: `auditoria/deskops.md` (WS02), `auditoria/infraestructura.md` (WS03), `auditoria/ui.md` (WS04), `reconciliacion.md` actual y fuentes de límites (`brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`). Cambios previstos: editar únicamente `reconciliacion.md` para incorporar o ajustar la matriz; sin tocar Board, tareas ni repos externos. Dependencias: WS02–WS04 deben aportar path/símbolo/hash o marcar «no comprobado» con causa; si falta una auditoría, registrar el hueco sin sustituirlo. Validaciones futuras: cada fila con repo dueño, estado, evidencia o causa; correspondencia con P01; ausencia de gates o aprobaciones nuevas; WS11/12 obtienen aceptación específica por repo receptor. No se ejecuta nada.

## FUTURO
WS11/12 obtienen la aceptación específica por delta del responsable designado en P01. WS07 reutiliza el registro de decisiones. WS32/33 conservan el tratamiento ya registrado de Scion RunDoc/cierre. El TaskDoc de promoción fijará archivos y pruebas; el operador Scion se designará al abordar el ramal E. Nada de ello es ambigüedad de este nodo.
