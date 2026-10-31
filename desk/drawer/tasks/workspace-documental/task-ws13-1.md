---
id: WS13.1
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS13
depends_on:
- WS11
requires:
- G_UI_READ
---

# Leer documento, contexto y enlaces

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/document/; rutas de lectura definidas por el contrato WS11; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Documento/fuente solo lectura, panel de contexto (identidad, relaciones y origen), enlaces y Code local con selección por documento/nodo. Mantener rutas del host; no requerir índices nuevos. Implementación o delta conciliado sobre el ticket workspace en draft, según acta WS11.

## Aceptación

Markdown sin modelo legible; el panel de contexto muestra identidad, las relaciones que declare el contrato WS11 y la ruta de origen reales; seguir un enlace y alternar entre texto/graph/code, en las representaciones que el catálogo WS09 (borradores/vistas.md) y el contrato WS11 declaren soportadas, preserva origen. La selección por documento/nodo fija el foco del documento abierto: seleccionar en Code, texto o graph actualiza ese foco y las demás representaciones del mismo documento lo comparten, sin abrir otra copia. No depender de conocer un ID; no crear otro workspace independiente. Si el acta de WS11 eligió integrar el ticket draft, su cierre/evidencia sustituye este delta; no suponer una base workspace ya implementada.

## Dependencias

Tareas: WS11. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS13.1/4ae5608942177cd21d60207164b42b0de574467f1f85ca1398e816c1ebf50485/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
