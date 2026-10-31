---
id: WS13
status: candidate
owner_repo: graph_ui
depends_on:
- WS11
requires:
- G_UI_READ
---

# Integrar lector workspace con historia y foco

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/; shell/router.js; rutas de lectura

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Implementación o delta conciliado sobre ticket workspace en draft: documento/fuente solo lectura, contexto, enlaces, tabs/historia y selección por documento/nodo. Mantener Code local y rutas del host; no requerir índices nuevos. Incluir explorador de documentos modelados/no modelados, dos documentos lado a lado y tabs/historia. Registro de renderer en código permitido; organización de contenido procede de documentos/consultas.

## Aceptación

Abrir dos documentos, cambiar texto/graph/code donde soporte existe y volver preserva origen. Markdown sin modelo legible; sin crear otro workspace independiente. Desde explorador abrir dos documentos en divisiones, alternar foco y volver; no depender de conocer un ID ni de índices nuevos. Si el acta de WS11 eligió integrar ticket draft, su cierre/evidencia sustituye ese delta; no suponer una base workspace ya implementada.

## Dependencias

Tareas: WS11. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
