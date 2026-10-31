---
id: WS02
status: candidate
owner_repo: deskops
depends_on:
- WS01
requires: []
---

# Inventariar superficies y operaciones Deskops

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

auditoria/deskops.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Modelos y Markdown no modelado; inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs; firmas públicas, efectos Git y cierre.

## Aceptación

Cada fila incluye archivo/código/operación y estado comprobado; no inferir modelo por carpeta.

## Dependencias

Tareas: WS01. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
