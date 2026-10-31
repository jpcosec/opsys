---
id: WS01
status: candidate
owner_repo: deskops
node_role: delivery
depends_on: []
requires: []
---

# Fijar brief y glosario autosuficientes

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

brief.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Editar brief.md en sitio: acuerdos textuales y distinciones documento/nodo/vista/renderer/consulta/foco; ningún requisito remite a un chat invisible.

## Aceptación

Un review barato sin historial reformula el producto solo con brief.md. Cada acuerdo (cita o frase de autorización) de la sección «Encargo y acuerdos explícitos» cita al solicitante y cada propuesta del registro Pxx remite a decisiones.md.

## Dependencias

Tareas: ninguna. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS01/3a9efb5dd5e8a15aab4649cf0b9dd3cbd577b711abf23395fb010f18d0d53a23/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
