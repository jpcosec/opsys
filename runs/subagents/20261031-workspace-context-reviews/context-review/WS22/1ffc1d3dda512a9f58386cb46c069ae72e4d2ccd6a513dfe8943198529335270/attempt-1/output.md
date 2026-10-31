## REFORMULACION

**Propósito:** entregar en `graph_ui` el Board real como trabajo navegable en tres representaciones —lista, tablero agrupado por estado y dependencias del TaskDoc— que abran en el lector el mismo TaskDoc y sus pills/átomos referenciados.

**Resultado:** deltas y tests en `frontends/mindmap/views/workspace/board/; tests/`.

**Repo dueño:** graph_ui. **Dependencias:** WS13 y WS09; requisito G_UI_READ (pendiente). Promoción no autorizada.

**Límites:** no reemplazar workflow con drag-and-drop de estado; estados y condiciones de lifecycle leídos de deskops, no de dag.yaml; no duplicar tareas; no presentar predicado satisfecho como test aprobado.

## AMBIGUEDADES

1. «como tablero agrupado por estado y con las dependencias declaradas en el TaskDoc» — la tercera representación no define qué muestra (aristas, dirección, profundidad, agrupación, layout). Obligaría a inventar el diseño de la vista de dependencias; la aceptación solo exige que abra el mismo TaskDoc.
2. «abriendo en el lector los mismos TaskDoc y sus pills/átomos referenciados» — no se define qué cuenta como átomo referenciado por un TaskDoc ni cómo resolverlo. Obligaría a inventar el criterio de vinculación. (La guía excluye pills; no el criterio de átomos.)
3. «no duplicar tareas» — con tres representaciones simultáneas del mismo Board, no queda claro si prohíbe repetir una tarea entre lista y tablero o solo crear registros duplicados. Obligaría a decidir cuál de las dos lecturas aplicar.
4. «estados y condiciones de lifecycle leídos de deskops (Board, lifecycle), no de dag.yaml» — no se nombra qué canal/API las expone ni quién lo garantiza; `depends_on` solo incluye WS09 (que inventaría Board/ritual) y WS13. Obligaría a inventar la fuente o asumir disponibilidad.

## DRY-RUN

- **Lecturas previstas:** dag.yaml (nodo y gates), context-review-guide, alcance.md, cobertura.md (UF04), reconciliacion.md, contrato del lector WS13, inventario `borradores/vistas.md` de WS09, Board/lifecycle de deskops.
- **Cambios previstos:** vistas de lista, tablero y dependencias bajo el `output_scope`, más tests.
- **Dependencias:** acta G_UI_READ de WS11 con responsable graph_ui designado (P01/WS07); lector WS13; filas de WS09.
- **Validaciones futuras:** revisión manual WS30 (UF04); acta de gate; TaskDoc de promoción fija archivos, textos y escenarios. Sin ejecución.

## FUTURO

WS11 produce el acta G_UI_READ; el solicitante designa responsable graph_ui (P01/WS07); WS09 fija la ficha de la fila Board; WS30 valida humanamente; WS26 consume la representación para enrutamiento; la promoción concreta archivos y pills.
