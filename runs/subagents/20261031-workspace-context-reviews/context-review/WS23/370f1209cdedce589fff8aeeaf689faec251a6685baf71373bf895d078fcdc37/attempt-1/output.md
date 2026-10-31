## REFORMULACION

**Propósito:** fijar el encargo de una vista de procedimiento —RitualDoc/StepDoc/lifecycle— en graph_ui, en modo representación y solo lectura, apoyada en el lector de WS13 y en el catálogo de renderizaciones de WS09.

**Resultado:** un procedimiento abre sus documentos y soporte; pasos y fuentes navegables; transiciones solo representadas, nunca accionables; el estado de cada paso se lee de deskops y esta vista no lo escribe ni lo infiere al abrir.

**Repo:** graph_ui; `output_scope` acota a `frontends/mindmap/views/workspace/procedure/` y `tests/`, con `output_base` en la raíz del repo.

**Límites:** sin mutaciones ni cambios de estado; sin duplicar el ticket workspace (`never_parallel_duplicate`); `G_UI_READ` pendiente; `promotion: not_authorized`.

## AMBIGUEDADES

Ninguna. Los términos RitualDoc/StepDoc/lifecycle están glosados en brief.md; origen, contrato, renderer, error y estado de la fila de ritual corresponden a WS09; la falta de contrato o permiso se resuelve con la regla común de alcance.md; `G_UI_READ` pendiente es estado intencional, no defecto.

## DRY-RUN

- **Lecturas:** input completo (guía, brief, alcance.md, decisiones.md, cobertura.md, reconciliacion.md, nodo WS23 y gates/aristas vecinas). Sin herramientas ni ejecución.
- **Cambios previstos:** ninguno; es revisión de solo lectura, no se edita `dag.yaml` ni se promueve el nodo.
- **Dependencias:** WS13 (agregado: WS13.1–13.3 y WS11); WS09 (fila de ritual con su ficha); `G_UI_READ` con resolver WS11; para pruebas, corpus WS40 o store temporal real.
- **Validaciones futuras:** abrir documentos y soporte del procedimiento; comprobar que leer no marca pasos; comprobar que las transiciones no son accionables; ejecutar pruebas solo sobre WS40 o store temporal; aceptación humana dentro de WS30.

## FUTURO

WS11 produce el acta de `G_UI_READ` con el responsable graph_ui que designe WS07 y la tarea receptora sin solapamiento; WS09 fija la ficha de la fila de ritual; el TaskDoc de promoción concreta archivos, escenarios y textos de pantalla; WS30 registra el recorrido humano; el solicitante resuelve P01/P04 y autoriza cualquier promoción.
