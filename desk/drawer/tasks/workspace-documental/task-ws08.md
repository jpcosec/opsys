---
id: WS08
status: candidate
owner_repo: deskops
node_role: delivery
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

Mapear UF a operaciones de WS02/03/04; cubrir manual, captura, revisión, cambios (UF07/WS29), arranque, multidesk, schemas y modo degradado (UF07, fallo de backend/dependencia). UF02 responder significa dentro del desk/contexto autorizado local; ack local: operación pendiente de confirmar en el contrato WS12; no se da por disponible. UF08 es lectura; envío interdesk fuera de baseline, sin excepción implícita a P07. Las operaciones vienen de auditoria/{deskops,infraestructura,ui}.md, disponibles por dependencia transitiva vía WS06/WS07.

## Aceptación

Cada UF tiene entrada/salida, operación, error, nodo y gate humano; no prometer función fuera de alcance. Nodo = ID del DAG. Una operación ausente se marca hueco, sin inventarla. Cubrir todas UF01–UF10; operación/nodo/gate admiten listas completas, no elegir nodo principal. Distinguir gate humano WS16/30/37/39 de prueba técnica propia WS29; si no hay gate humano adicional escribir ninguno adicional. Delegación se documenta condicionada a G_SCION/G_EXEC, sin habilitarla.

## Dependencias

Tareas: WS07. Gates: G_PRODUCT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS08/35bb9f3186c36265ca392d1cda2b8e0a1613aad5c74b08c1cd7e30c08472dd87/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
