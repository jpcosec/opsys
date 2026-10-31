---
id: WS03
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS01
requires: []
---

# Inventariar persistencia, consultas y notaciones

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

auditoria/infraestructura.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Auditoría de solo lectura de sldb/pron/spec2viz: fuente/payload, conflictos y límites de locks (control de concurrencia real de sldb/pron: CAS por revisión/hash, locks de archivo o DB; a auditar), referencias documentales, búsquedas (índices o consultas expuestas) y alcance real ViewDoc. Kimun solo referencia.

## Aceptación

Una salida documental, sin cambios interrepo; distinguir API comprobada (lectura citada del estado actual), ausencia y hueco.

## Dependencias

Tareas: WS01. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS03/f5662403884ad5dd0d8f215f737d0d263bd0ad85173ba35b590fd1fa978241be/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
