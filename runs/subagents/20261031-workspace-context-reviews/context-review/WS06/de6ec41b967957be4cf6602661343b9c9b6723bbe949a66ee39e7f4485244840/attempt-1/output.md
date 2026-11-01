REFORMULACION
WS06 es un encargo documental de planificación, no un agregado: propone la correspondencia entre el alcance del plan y los repos dueños. Resultado: una matriz en `reconciliacion.md`, con una fila por delta/capacidad única agrupada por repo, que cite path/símbolo/commit, clasifique como ya cubierto, extender ticket o nuevo delta, indique ticket/delta y responsable según P01, conserve la fila Scion RunDoc/cierre y su descomposición WS32/33 sin ejecutar WS05, y registre la atomización. Repo dueño: deskops; `output_scope`: `reconciliacion.md`. Límites: no notifica, despacha ni modifica el Board de graph_ui; no crea firmas, gates, recibos ni recepción; WS11/12 solo enlazan actas externas del receptor P01; no aprueba deltas indefinidos.

AMBIGUEDADES
1. El scope fija tres categorías: «ya cubierto (capacidad observable en código implementado, citando path/símbolo y commit observado), extender ticket existente (incluido un draft del Board) o nuevo delta», pero `reconciliacion.md` usa «no adoptado» para C-29. Si se regenera la matriz, no queda claro si C-29 se conserva como cuarta categoría, se reclasifica o se omite; cualquiera de esas opciones exige una regla no escrita.

DRY-RUN
Un ejecutor futuro leería WS02–WS04 (`auditoria/deskops.md`, `infraestructura.md`, `ui.md`), brief, alcance, decisiones, cobertura, `reconciliacion.md` y `dag.yaml`, y actualizaría solo `reconciliacion.md`. No tocaría Board, tareas, código, gates ni actas. Consumiría los inventarios de WS02–WS04; si falta un dato o evidencia, se detendría y registraría el hueco con repo dueño, sin sustituto. Validaría después: fila única por delta/capacidad y repo, no por nodo; path/símbolo/commit observado; ticket existente o delta nuevo; responsables según P01; fila Scion conservada; atomización registrada; ninguna recepción, gate o notificación producida; WS11/12 solo enlace.

FUTURO
WS02–WS04 deben entregar y aceptar sus inventarios; WS11/12 enlazarán las actas del receptor P01 por delta; el receptor humano P01 produce esas actas externas al preparar cada delta. WS07 reutilizará el registro de decisiones. La promoción de WS06 a tarea no está autorizada y requiere preflight task-only.
