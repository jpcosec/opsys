---
id: WS27.1
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS27
depends_on:
- WS13
- WS12
requires:
- G_UI_READ
---

# Mostrar diff Git por repo y tarea

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/diff/; rutas de lectura definidas por el contrato WS11; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Diff Git e historial read-only junto a la TaskDoc. Base: commits listados en TaskDoc.references y rutas en TaskDoc.files (campos del modelo TaskDoc de deskops); sin commits, working tree contra HEAD limitado a esas rutas. Historial baseline = commits de TaskDoc.references resolubles y ordenados por fecha de commit, limitados a TaskDoc.files; sin commits se declara que no hay historial referenciado y se usa diff working tree→HEAD. Repo/rutas se resuelven por contrato WS11 con registry/aliases, presentando root repo explícito; ruta sin repo resoluble queda no disponible, no adivinar ni escribir cruzado.

## Aceptación

Diff real e historial read-only acotados al repo y tarea (la asociación a intento se añade en WS35), sin escribir ni revertir nada; la vista no muestra hallazgos de integridad del store, que son de WS29. Se muestra una sección por cada repo alcanzado por TaskDoc.files, con el repo declarado.

## Dependencias

Tareas: WS13, WS12. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS27.1/f2df862dd4ca0a9401e12826062efa7dfcae22746e1cf90200eada90d8651ae6/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
