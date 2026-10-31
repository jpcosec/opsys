---
id: WS29
status: candidate
owner_repo: graph_ui
depends_on:
- WS15
- WS24
requires:
- G_UI_READ
---

# Integrar Changes e impacto comprobable

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/changes/; rutas integridad; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Delta sobre tarea Changes actual; stores check/doctor/drift y relaciones comprobadas. No CST ni árbol Kimun supuesto.

## Aceptación

Mutaciones reales muestran soporte/alcance/errores. Reparar no es automático: acción documentada o tarea explícita. Esta extensión no bloquea lector/manual básico.

## Dependencias

Tareas: WS15, WS24. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `changes` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
