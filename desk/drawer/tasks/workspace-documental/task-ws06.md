---
id: WS06
status: candidate
owner_repo: deskops
depends_on:
- WS02
- WS03
- WS04
requires: []
---

# Registrar acuerdos de alcance con repos dueños

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

reconciliacion.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Una matriz por implementación: ya cubierto, extender ticket existente o nuevo delta. Proponer atomización a dueño graph_ui sin despachar ni modificar su Board.

## Aceptación

Matriz propuesta con correspondencia ticket/delta y responsable por designar; no produce gates de aceptación ni aprueba deltas que aún no están definidos. WS11/12 obtienen aceptación específica por repo receptor.

## Dependencias

Tareas: WS02, WS03, WS04. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
