---
id: WS15.2
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS15
depends_on:
- WS13
requires:
- G_UI_READ
---

# Orientar proyecto sin desk

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: S.

frontends/mindmap/views/workspace/orientation/; rutas de lectura definidas por el contrato WS11; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

UF10: un proyecto sin desk muestra orientación, la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`; nunca inicializar por GET. Tras init externo real, refrescar lectura.

## Aceptación

Abrir un proyecto sin desk muestra orientación y destino sin mutar nada; tras ejecutar init fuera de la UI, refrescar muestra el desk real.

## Dependencias

Tareas: WS13. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS15.2/a69095aeb84ca6027590a482a8902f47de097b522ffa1bbf3d4d4901e3343be0/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
