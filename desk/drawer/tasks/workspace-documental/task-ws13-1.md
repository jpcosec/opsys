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

frontends/mindmap/views/workspace/ (reutilizar node/workspace-view.js y componentes Document/Graph/Code/contexto existentes); rutas de lectura contrato WS11; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Documento/fuente solo lectura, panel de contexto (identidad, relaciones y origen), enlaces y Code local con selección por documento/nodo. Mantener rutas del host; no requerir índices nuevos. Implementación o delta conciliado sobre el workspace integrado a1b2b22, según contrato WS11 y recibo externo del delta. Foco = elemento/nodo seleccionado dentro del documento; documento activo identifica pestaña. Compartir foco solo donde exista correspondencia real de origen definida WS11; no inventar mapeo texto→código.

## Aceptación

Markdown sin modelo tiene render de lectura y fuente cruda íntegra legibles (ambas), con mismo origen; el panel de contexto muestra identidad, las relaciones que declare el contrato WS11 y la ruta de origen reales; seguir un enlace y alternar entre texto/graph/code, en las representaciones que el catálogo WS09 (borradores/vistas.md) y el contrato WS11 declaren soportadas, preserva origen. La selección por documento/nodo fija el foco del documento abierto: seleccionar en Code, texto o graph actualiza ese foco y las demás representaciones del mismo documento lo comparten, sin abrir otra copia. No depender de conocer un ID; no crear otro workspace independiente.  La base a1b2b22 es punto de partida reutilizable; el cierre de este delta exige SU evidencia de aceptación ampliada Markdown no modelado/fuente, enlaces y foco. Ni cierre f16fcd1 ni commit previo sustituyen esa evidencia. Una copia es instancia documental con mismo origen, no cada representación.

## Dependencias

Tareas: WS11. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS13.1/793f1a6e84597102d83c8bada9af43c16ac49626f4aebf9d78496d21831ee9cf/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
