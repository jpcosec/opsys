REFORMULACION
WS06 es un nodo delivery de planificación (no agregado) del repo deskops, con salida en reconciliacion.md. Debe convertir los inventarios WS02–WS04 en una matriz por delta o capacidad única, agrupada por repo dueño, clasificando cada fila como ya cubierto, extender ticket existente o nuevo delta, con path/símbolo y commit observado, y añadir una atomización propuesta. Límites: no notifica, despacha ni modifica el Board de graph_ui; no firma gates ni recepción; WS11/WS12 solo enlazan actas del receptor P01. Depende de WS02, WS03 y WS04.

AMBIGUEDADES
1. «Registrar en reconciliacion.md la atomización propuesta»: el input ya incluye reconciliacion.md con la matriz completa y esa atomización. No se define si el ejecutor debe crearla, actualizarla o preservar sus filas; obliga a inventar si el contenido existente cuenta como resultado y cómo tratar su tabla de cobertura de 64 nodos.
2. «ya cubierto (capacidad observable en código implementado, citando path/símbolo y commit observado), extender ticket existente (incluido un draft del Board) o nuevo delta»: el reconciliacion.md suministrado usa una cuarta clase, «no adoptado», para código sin commit (frontends/workspace). El nodo no cubre código no versionado ni permite citar commit; obliga a inventar una categoría o forzar esa fila en las tres.

DRY-RUN
Leería brief.md, alcance.md, decisiones.md, cobertura.md, dag.yaml, auditoria/deskops.md, auditoria/infraestructura.md, auditoria/ui.md, approval.md y el reconciliacion.md actual. Único cambio previsto: reconciliacion.md; ningún código, Board, tarea ni repo ajeno. Consume los inventarios WS02–04; no hay gate de entrada específico ni produce gates. Si falta un inventario o una fila carece de owner, clasificación o evidencia, se detendría y registraría el hueco según las reglas comunes, sin sustituto. Validación esperada: revisión humana de cobertura, clasificación y evidencia por fila, y de que la atomización no crea tareas.

FUTURO
WS07 reutiliza la matriz para el registro de decisiones; WS11 y WS12 la usan como fuente para clasificar huecos de lectura/escritura y enlazar actas; el receptor humano P01 emite el acta por delta en el repo dueño al prepararlo. La promoción posterior exige preflight del TaskDoc y no autoriza modificar el Board.
