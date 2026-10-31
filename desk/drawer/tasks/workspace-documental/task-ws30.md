---
id: WS30
status: candidate
owner_repo: graph_ui
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

Persona recorre UF02/03 edición/04/05; integra conocimiento y tarea en ejemplo; errores, teclado, dos ventanas y conflictos, con historial. Incluye explícitamente UF01 usando entradas authored WS17 materializadas por generador WS40, además de edición/operación; no limitarlo a búsqueda.

## Aceptación

Registro humano bajo protocolo; problemas implican tareas de corrección de la misma capa. No llamar ready a un flujo solo por tests.

## Dependencias

Tareas: WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28, WS42. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
