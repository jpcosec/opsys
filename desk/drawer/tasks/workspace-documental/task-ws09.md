---
id: WS09
status: candidate
owner_repo: deskops
depends_on:
- WS07
requires:
- G_PRODUCT
---

# Precisar catálogo de renderizaciones

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

borradores/vistas.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Inventariar fuente, queries, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas existentes; ViewDoc es grafo, no contrato universal de UI.

## Aceptación

Cada fila tiene origen, contrato, renderer, acción/dueño, error y estado. Distinguir authored/derivado/preferencia local.

## Dependencias

Tareas: WS07. Gates: G_PRODUCT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
