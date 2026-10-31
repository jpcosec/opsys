## REFORMULACION

Propósito: entregar en `graph_ui` un explorador que liste y permita abrir documentos reales del store, tanto modelados como Markdown no modelado del desk, sin exigir conocer IDs ni crear índices. Resultado: vista bajo `frontends/mindmap/views/workspace/explorer/`, usando las rutas de lectura del contrato WS11 y pruebas en `tests/`. Repo dueño: `graph_ui`. Límites: depende de WS11 y WS13.1; `G_UI_READ` está pendiente; `integration_mode` exige delta o ticket existente tras WS06 y prohíbe duplicado paralelo; no hay ejecución autorizada.

## AMBIGUEDADES

1. «La organización del contenido procede de documentos/consultas» — no se identifica qué documentos/consultas ni si existe infraestructura de consulta. WS11 aporta rutas de lectura, no necesariamente el mecanismo de listado. Obligaría a inventar el origen del árbol.
2. «el listado no es inventario hardcodeado» — no define cómo comprobarlo. Obligaría a inventar el criterio y la prueba de aceptación (por ejemplo, alta/baja de un documento).
3. «Explorador sobre documentos reales del store y Markdown no modelado del desk» — no nombra corpus, ruta concreta ni dependencia de WS40; la aceptación exige abrir ambos tipos. Obligaría a inventar fixtures.
4. `integration_mode: "delta_or_existing_ticket_only_after_WS06; never_parallel_duplicate"` — WS06 no figura en `depends_on`. Obligaría a decidir si es prerrequisito efectivo o solo referencia.

## DRY-RUN

Lecturas previstas: nodo WS13.2, contrato WS11, WS13.1, gates y guía. Cambios previstos: carpeta del explorador y tests; sin ejecución. Dependencias: WS11 y WS13.1; `G_UI_READ` pendiente; WS06 solo citado en `integration_mode`; WS40 no consta como dependencia. Validaciones futuras: acta WS11 con `scope_nodes`, apertura de un documento modelado y otro no modelado sin ID ni índices nuevos, listado derivado y preflight task-only.

## FUTURO

WS11 produce el contrato de navegación/identidad y resuelve `G_UI_READ`; WS06/WS07 designan actores y correspondencias; WS40 aporta corpus; el humano resuelve las Pxx aplicables; WS13 cierra como agregado cuando cierren sus hijos.
