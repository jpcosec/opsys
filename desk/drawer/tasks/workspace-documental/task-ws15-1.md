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

Referencia rota, documento ausente, modelo no importable, backend caído y fuente no editable; error mostrado en el panel afectado sin borrar historial ni fingir vacío. Fallos de CDN visibles como límite actual.

## Aceptación

Leer Markdown existente cuando el soporte lo permita, informar límites reales y tras reintento manual recuperar conexión sin perder pestañas, foco ni historia. Errores distinguidos por la respuesta de la API, según contrato WS11. Si las dependencias CDN no cargan, la pantalla lo dice y un test lo cubre; empaquetado offline queda fuera.

## Dependencias

Tareas: WS13. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS15.1/9ec2d5d02a2ad973a6ad8437fdd724353a4d5a2a28332cc1302d3c6c12d39558/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
