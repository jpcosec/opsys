---
id: WS10
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS02
- WS07
requires:
- G_PRODUCT
---

# Precisar índice y convención del manual

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

borradores/manual.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Índice y capítulos conceptuales, ejemplo fijo y etiqueta de disponibilidad; reutilizar manual CLI. Usa auditoria WS02–WS04; WS03/WS04 llegan de forma transitiva por WS06/WS07.

## Aceptación

Definiciones verificables de disponible/propuesto/bloqueado; no escribir pasos ni capturas ficticios.

## Dependencias

Tareas: WS02, WS07. Gates: G_PRODUCT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS10/1a815c3a51d42fbe540fac61b0f7e9c5f5331fbf26ae474bc090733833670fa3/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
