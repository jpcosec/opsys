## REFORMULACION

**Propósito:** que el lector del workspace muestre el Board real como trabajo navegable, sin sustituir el workflow.

**Resultado:** tres representaciones —lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc— que abren el mismo TaskDoc y sus pills/átomos referenciados, con selección y links comunes con el lector. Estados y condiciones de lifecycle se leen de deskops (Board, lifecycle), no de `dag.yaml`.

**Repo dueño:** `graph_ui`; salida prevista en `frontends/mindmap/views/workspace/board/` y `tests/`.

**Límites:** no reemplazar workflow con drag-and-drop de status; no duplicar tareas; no presentar un predicado satisfecho como test aprobado. Depende de WS13 (agregado lector) y WS09 (catálogo de renderizaciones); requiere G_UI_READ por delta.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas (sin ejecutar):** `dag.yaml` del nodo WS22 y vecinos WS13/WS09/WS26/WS30 y gate G_UI_READ; `brief.md`, `alcance.md`, `decisiones.md`, `reconciliacion.md`, `cobertura.md`; al promover, TaskDoc receptor y Board del repo `graph_ui`.

**Cambios previstos:** implementar en `graph_ui` las vistas lista/tablero/dependencias sobre APIs de lectura de deskops; enlazar selección y apertura al lector existente; añadir pruebas en `tests/`. No se modifica `dag.yaml` ni se promociona nada.

**Dependencias:** WS13 debe entregar lector, selección e historia; WS09 debe fijar el contrato/fila del Board o declarar «sin contrato»; WS11/WS12 llegan transitivamente. G_UI_READ exige acta por delta con actor, alcance, efecto y commit/blob en repo receptor.

**Validaciones futuras:** que las tres representaciones abran el mismo TaskDoc; que selección/links coincidan con el lector; que estados/lifecycle provengan de deskops; que no se dupliquen tareas ni se confunda predicado con prueba; que el acta per_delta exista antes de promocionar.

## FUTURO

WS09 produce el catálogo de renderizaciones; WS13 y sus hijos producen el lector integrado; WS11 produce el contrato de navegación; el receptor de `graph_ui` emite el recibo G_UI_READ del delta. La promoción fija archivos, pruebas y textos exactos. WS30 valida el recorrido UF04. La aceptación de producto/implementación la decide el humano solicitante, no este revisor.
