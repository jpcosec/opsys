**REFORMULACION**  
Propósito: precisar el catálogo de renderizaciones de WS09. Resultado: `borradores/vistas.md` con cada fila de las tablas y su ficha, indicando origen, contrato o «sin contrato», renderer, acción/dueño, error y estado; distinguiendo authored/derivado/preferencia local y marcando campos sin evidencia como no definidos. Repo: deskops (`output_scope: borradores/vistas.md`). Límites: no ejecutar, no inventar actor/API disponible, no crear UI ni contrato, no convertir ViewDoc en contrato universal; estado según WS10 y disponibilidad actual según `auditoria/ui.md` (WS04).

**AMBIGUEDADES**  
1. «Campo sin evidencia se marca no definido con productor WS11/12 o futura implementación». Cuando un campo —incluido «renderer/actor/campos/relaciones»— no tiene productor WS11/12 ni nodo del DAG, el input no nombra qué nodo o repo constituye «futura implementación»; el ejecutor tendría que inventar el productor o elegir un repo dueño no fijado.

**DRY-RUN**  
Leería guía, brief, alcance, decisiones, cobertura, `dag.yaml` (WS09), `vistas.md`, las definiciones de estado de WS10, las UFs de WS08, el registro de WS07 y las auditorías WS02–04. Actualizaría solo `borradores/vistas.md`: completaría cada fila y ficha, marcaría «sin contrato», «no definido» con productor, estado y disponibilidad actual, errores condicionados y clasificación por componente; añadiría o separaría filas solo si hay evidencia/estado independiente. Consumiría G_PRODUCT ya satisfecho por WS07; no hay otro gate. Si faltara WS10, WS08 o una auditoría, se detendría y registraría el hueco con repo dueño, sin sustituto. Validaría que ninguna fila invente actor/API, que «disponible» no se afirme sin evidencia humana y que estado/disponibilidad sigan sus fuentes.

**FUTURO**  
WS10 aporta taxonomía de estados y ejemplo del manual; WS08, las UFs; WS11, navegación, identidad y selección mínima para ViewDoc; WS18, ViewDocs concretos; WS22/WS23/WS24 consumen el catálogo para Board, procedimiento y conocimiento. La promoción/TaskDoc de WS09 y cualquier decisión nueva quedan fuera de este nodo; P01 y G_PRODUCT ya están registrados.
