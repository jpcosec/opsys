---
id: WS30
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS17
- WS21
- WS22
- WS23
- WS24
- WS25
- WS26
- WS28
- WS42
requires: []
---

# Validar autoría y revisión manual completas

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

runs/subagents/workspace-documental-acceptance/manual/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Persona recorre UF02/03 edición/04/05; integra conocimiento y tarea en ejemplo; los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md. Incluye explícitamente UF01 usando entradas authored WS17 materializadas por generador WS40, además de edición/operación; no limitarlo a búsqueda.

## Aceptación

Registro humano bajo protocolo; un fallo de guion bloquea el gate y el responsable del repo dueño abre tarea en el nodo que lo causó; una observación solo se registra. No llamar ready a un flujo solo por tests.

## Dependencias

Tareas: WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28, WS42. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS30/8e894d58c0242c7279b69314a4e4e9ff7780312efe04c2774b7a9fb344166770/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
