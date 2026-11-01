---
id: WS13.3
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS13
depends_on:
- WS11
- WS13.1
requires:
- G_UI_READ
---

# Abrir documentos en pestañas y divisiones con historia

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: S.

frontends/mindmap/views/workspace/layout/; rutas de lectura definidas por el contrato WS11; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Pestañas, dos documentos lado a lado, foco e historia de navegación; disposición como estado local según P07, no como documento compartido. Foco es el elemento seleccionado dentro de un documento; origen es su soporte y ruta real. Cambiar de pestaña o división cambia el documento activo sin alterar el foco guardado de cada documento; volver restaura documento, foco y origen. Disposición por sesión de navegador; no se exige persistir tras recargar.

## Aceptación

Abrir, cambiar y cerrar pestañas; abrir dos documentos en divisiones, alternar el documento activo y volver conservando foco e historia. Volver sigue el orden inverso de navegación.

## Dependencias

Tareas: WS11, WS13.1. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS13.3/2fcc4a9e6a1e6a45a3f3cc17db284a3ca5736e62370dae9a7d3783521d8975bf/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
