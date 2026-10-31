---
id: WS08
status: candidate
owner_repo: deskops
depends_on:
- WS07
requires:
- G_PRODUCT
---

# Precisar user-flows y criterios observables

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

borradores/user-flows.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Mapear UF a operaciones de WS02/03/04; cubrir manual, captura, revisión, cambios, arranque, multidesk, schemas y modo degradado. UF02 responder significa dentro del desk/contexto autorizado local; ack local disponible según contrato. UF08 es lectura; envío interdesk fuera de baseline, sin excepción implícita a P07.

## Aceptación

Cada UF tiene entrada/salida, operación, error, nodo y gate humano; no prometer función fuera de alcance.

## Dependencias

Tareas: WS07. Gates: G_PRODUCT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
