---
id: WS27
status: candidate
owner_repo: graph_ui
depends_on:
- WS13
- WS12
requires:
- G_UI_READ
---

# Integrar revisión de cambios y evidencia

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/review/; rutas git read-only; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Diff Git y artefactos de evidencia junto al encargo, historial read-only; diferenciar cambios de código de integridad del store.

## Aceptación

Diff real scoped al repo y tarea (la asociación a intento se añade en WS35), sin execute/revert genérico. Mostrar declarada/encontrada/verificada y abrir soporte; no inventar CommentDoc antes de contrato.

## Dependencias

Tareas: WS13, WS12. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
