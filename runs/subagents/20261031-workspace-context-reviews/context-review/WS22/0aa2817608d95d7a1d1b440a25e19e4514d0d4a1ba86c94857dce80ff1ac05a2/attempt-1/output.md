## REFORMULACION
- **Propósito:** revisar WS22 como encargo de planificación, no como producto ni ejecución.
- **Resultado:** representar el Board real en tres vistas —lista, tablero por estado y dependencias del TaskDoc— abriendo el mismo TaskDoc y sus pills/átomos en el lector, sin sustituir el workflow por drag-and-drop de status.
- **Repo:** `graph_ui`.
- **Límites:** no ejecutar; no revisar los edges vecinos; `G_UI_READ` pendiente es intencional; las Pxx no están aprobadas.

## AMBIGUEDADES
1. «estados y gates leídos de deskops (Board, lifecycle)». Las fuentes no definen qué es un “gate” de deskops ni qué operación de Board/lifecycle lo expone; “gates” solo aparece como G_* de `dag.yaml`, que la propia frase excluye. Obligaría a inventar la fuente y la semántica de los gates mostrados.

## DRY-RUN
- **Lecturas:** `dag.yaml` (WS22, edges WS13/WS09/WS26/WS30 y gates), guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`.
- **Cambios previstos:** ninguno; solo este informe.
- **Dependencias:** WS13 (lector, historia y foco), WS09 (catálogo de renderizaciones), `G_UI_READ` pendiente y resuelto por WS11; WS11/WS12 cuentan como transitivas.
- **Validaciones futuras:** al promover, el TaskDoc fijará archivos, escenarios y textos; `G_UI_READ` deberá constar aceptado por el responsable de `graph_ui`; WS30 validará UF04; no hay ejecución autorizada.

## FUTURO
WS11 resuelve `G_UI_READ`; WS07 designa al actor de `graph_ui`; WS12 documenta el contrato de escritura; WS26.1 produce la autoría de dependencias/pills; WS30 ejecuta la validación humana; el solicitante decide P01/P02/P07/P08/P09. Nada de esto es ambigüedad de WS22.
