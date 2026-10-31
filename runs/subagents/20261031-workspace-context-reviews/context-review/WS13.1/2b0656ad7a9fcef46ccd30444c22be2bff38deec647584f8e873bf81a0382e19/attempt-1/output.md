## REFORMULACION

**Propósito:** revisar WS13.1 como encargo de planificación: lector de documento/fuente en solo lectura, panel de contexto, enlaces y Code local con selección por documento/nodo.
**Resultado:** nodo `implementation` en `graph_ui`, delta o integración conciliada sobre el ticket workspace en draft.
**Repo dueño:** `graph_ui`; `output_scope` acota `frontends/mindmap/views/workspace/document/`, rutas del contrato WS11 y `tests/`.
**Límites:** no crear otro workspace ni exigir índices nuevos; mantener rutas del host; mutaciones fuera (WS16/WS12); promoción `not_authorized`.

## AMBIGUEDADES

1. «seguir un enlace y cambiar texto/graph/code … preserva origen»: «cambiar» admite dos lecturas — alternar entre representaciones o modificar el contenido. La segunda contradice «Documento/fuente solo lectura» y obligaría a inventar si el nodo incluye edición.
2. «el panel de contexto muestra identidad, relaciones y origen reales»: no se enuncia qué relaciones ni con qué fuente se obtienen. WS11 cubre identidad/resolución y clasificación de huecos, pero no se declara allí el inventario del panel; el ejecutor tendría que inventar el conjunto de relaciones y el significado operativo de «origen».

## DRY-RUN

**Lecturas (sin ejecutar):** guía de revisión, brief, alcance, decisiones, cobertura, reconciliación, bloques WS13.1/WS13/WS11 y gate G_UI_READ.
**Cambios previstos:** ninguno; esta revisión no modifica `dag.yaml` ni el task file.
**Dependencias identificadas:** acta WS11 (rutas de lectura, representaciones soportadas, posible integración del ticket draft); matriz WS09; designación del responsable `graph_ui` en WS07; G_UI_READ pendiente.
**Validaciones futuras:** comprobar que la aceptación sea verificable una vez WS11 enumere representaciones y rutas; verificar no solapamiento con el ticket draft y ausencia de duplicación paralela.

## FUTURO

- WS11 decide si se integra el ticket draft («su cierre/evidencia sustituye este delta») y publica las rutas/representaciones soportadas.
- WS07 designa al responsable `graph_ui`; G_UI_READ queda pendiente hasta su acta con identidad y fecha.
- WS09 aporta la matriz de representaciones.
- Un humano autoriza o no la promoción y la tarea receptora.
