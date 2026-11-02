REFORMULACION

WS09 (deskops, planning, no agregado) debe precisar el catálogo de renderizaciones en `borradores/vistas.md`: inventariar cada fila de las tablas —fuente, queries, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas existentes— con origen, contrato o «sin contrato», renderer, acción/dueño, error y estado, y completar una ficha por fila. Debe distinguir authored/derivado/preferencia local, marcar no definido con productor WS11/12 o futura implementación y no inventar actores/APIs. Límite: ViewDoc es grafo, no contrato universal de UI; no implementa. Repo: deskops.

AMBIGUEDADES

1. «Campo sin evidencia se marca no definido con productor WS11/12 o futura implementación». Para un campo sin nodo planificado, «futura implementación» no identifica nodo ni repo; obligaría a inventar un productor o a usar una categoría no prevista («sin productor en el DAG», como hace el borrador).

2. «Cada fila inventaría ... estado desde auditorías WS02–04/decisiones y UFs WS08» frente a «Estado = disponible/propuesto/bloqueado según WS10». No fija precedencia ni qué hacer si una fila no tiene UF; obligaría a inventar la regla de estado (el borrador resuelve «ninguna» y deriva todo de `manual.md`).

DRY-RUN

Lecturas: `dag.yaml`, brief/alcance/decisiones/cobertura, auditorías WS02–04, WS08 (user-flows), WS10 (manual/estado) y `vistas.md`. Cambios: reescribiría `borradores/vistas.md`; completaría tablas y fichas F01–F20 (a/b solo con evidencia/estado propio) con origen, identidad, contrato, campos/relaciones, renderer, navegación, acción/dueño, destino, error, estado, clase, UF y evidencia. Dependencias: G_PRODUCT satisfecho; consumiría UFs y definiciones de estado. Gates: ninguno adicional; G_PRODUCT no autoriza implementación. Errores: si falta WS08/WS10 o una auditoría, detenerse y registrar hueco con repo dueño; no inventar. Validación: cada fila con campos, «sin contrato» explícito, estado según WS10, sin actor/API inventados, listas en filas compuestas y contraste con auditorías/UFs.

FUTURO

WS11 usará el catálogo para navegación/identidad; WS12 para operaciones/errores; WS18 para selección ViewDoc; WS22/23/24/25/27/29/39/42 consumen fichas. WS08 y WS10 aportan UFs y definiciones. La promoción exige TaskDoc, archivos/pills/evidencia y preflight; la aceptación humana posterior queda fuera de este nodo.
