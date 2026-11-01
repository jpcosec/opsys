---
id: WS13.2
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

# Explorar documentos modelados y no modelados

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: S.

frontends/mindmap/views/workspace/explorer/; rutas de lectura definidas por el contrato WS11; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Explorador sobre documentos reales del store y Markdown no modelado del desk. El árbol se obtiene de la API del store y del sistema de archivos del desk, según contrato WS11.

## Aceptación

Desde el explorador abrir un documento modelado y uno no modelado sin conocer su ID ni usar índices nuevos; al añadir un documento al store temporal de prueba, aparece sin cambiar código. Altas de documento modelado en store y Markdown no modelado en desk aparecen tras refresco explícito del catálogo sin reiniciar servidor ni cambiar código. Se permite reutilizar catálogo/filtro existente para modelados; WS11 determina API/seguridad para no modelados.

## Dependencias

Tareas: WS11, WS13.1. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS13.2/4efd748bceb06cfb46bb4836393651369d3dd9667a73e478a62c801dcdf7bb31/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
