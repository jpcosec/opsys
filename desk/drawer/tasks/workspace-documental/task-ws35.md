---
id: WS35
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS33
- WS27
requires:
- G_SCION
- G_UI_READ
---

# Mostrar ejecución y trazabilidad en workspace

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/execution/; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Lectura tarea-intento-conversación-resultados-decisión: tarea de deskops, intento y decisión de WS32/WS33, mensajes de Scion por su API y resultados vinculados por WS33.1.

## Aceptación

Cada mensaje, resultado y decisión se muestra bajo su intento y tarea; cada uno enlaza a su fuente; la evidencia abre en el lector (WS13). completed no se traduce en aprobado/cerrado.

## Dependencias

Tareas: WS33, WS27. Gates: G_SCION, G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS35/1ee9ece7e3b114ed062f995c8d22e025f459fa94004bd83fa73463ba3f81acc6/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
