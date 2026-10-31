## REFORMULACION
- **Propósito:** encargo de planificación para que `graph_ui` represente el Board real como trabajo navegable, reutilizando el lector y leyendo estados/gates de deskops.
- **Resultado:** nodo `implementation` con `output_scope` en `frontends/mindmap/views/workspace/board/; tests/`, aceptación declarada y promoción no autorizada.
- **Repo dueño:** `graph_ui`.
- **Límites:** no reemplazar workflow con drag-and-drop de status; no duplicar tareas; no presentar predicado satisfecho como test aprobado; `promotion: not_authorized`; requiere `G_UI_READ`.
- **Dependencias:** WS13 (lector, historia y foco) y WS09 (catálogo de renderizaciones).

## AMBIGUEDADES
1. **“Representar Board real como lista, como tablero y con dependencias”** frente a una aceptación que solo exige: **“Selección y links comunes con lector; estados y gates leídos de deskops (Board, lifecycle), no de dag.yaml; no duplicar tareas…”**. No queda claro si las tres representaciones son obligatorias ni cómo se comprueban; obligaría a inventar si basta una o si deben entregarse todas y con qué evidencia.
2. **“como tablero y con dependencias”** no define qué agrupación usa el tablero ni qué dependencias deben mostrarse (¿`depends_on`, gates, solapamiento de archivos?). Obligaría a inventar el modelo de representación y su fuente.

## DRY-RUN
- **Lecturas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md` y bloques `WS22`, `WS13`, `WS09`, `WS26`, `WS30` y `G_UI_READ` de `dag.yaml`.
- **Cambios previstos:** ninguno; no se ejecuta ni se modifica el plan.
- **Dependencias:** WS13 y WS09 como prerrequisitos; `G_UI_READ` resuelto por WS11; matriz WS06 llega transitivamente.
- **Validaciones futuras:** aceptación del nodo, pruebas en `tests/`, verificación de que estados/gates provienen de deskops y no de `dag.yaml`, y satisfacción de `G_UI_READ`.

## FUTURO
- WS11 produce el acta de `G_UI_READ`; WS09 entrega la fila del catálogo relativa a Board.
- El TaskDoc de promoción fijará archivos, pills, átomos, evidencia y preflight.
- El humano resuelve P01/P02/P07/P08/P09 y designa al responsable de `graph_ui`.
- WS30 valida manualmente; WS26.2 y otros dependientes consumen WS22.
