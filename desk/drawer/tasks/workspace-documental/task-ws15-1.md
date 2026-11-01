---
id: WS15.1
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS15
depends_on:
- WS13
requires:
- G_UI_READ
---

# Mostrar errores de lectura y modo degradado

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: S.

frontends/mindmap/views/workspace/errors/; rutas de lectura definidas por el contrato WS11; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Referencia rota, documento ausente, modelo no importable y backend caído se muestran en panel afectado sin borrar historial ni fingir vacío. Fuente sin permiso/capacidad de edición es límite read-only visible, no fallo de lectura. Fallos CDN se declaran límite actual sin prometer offline.

## Aceptación

Reutilizar lectura Markdown de WS13.1 donde siga disponible; no implementar otro lector ni guardado. Contrato WS11 define errores de API y estados de red sin respuesta, incluido fallo de carga CDN; pruebas distinguen ambos sin inventar respuesta del backend ausente. Reintentar backend tras restaurarlo recupera lectura conservando pestañas/foco/historia; fallo CDN tiene diagnóstico visible y prueba de no carga, sin exigir recuperación offline. Empaquetado offline fuera.

## Dependencias

Tareas: WS13. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS15.1/de82c3ab6c7fa0599e1baf449a181b89e222f614e596946002fe485de6736297/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
