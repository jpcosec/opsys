---
id: WS32
status: candidate
owner_repo: deskops
node_role: aggregate
children:
- WS32.1
- WS32.2
depends_on:
- WS05
- WS12
- WS32.1
- WS32.2
requires:
- G_CLOSEOUT
- G_SCION
- G_WRITE_CONTRACT
---

# Unificar identidad de intento y cierre Scion

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

Agregado: salidas de WS32.1, WS32.2

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Refinar el candidato de drawer de external_references.scion (no es ticket del Board), sin segundo pipeline: intento no es slug, dispatch intent/confirmed separado, manifiesto/RunDoc/cierre consistentes e idempotentes. WS32.1/32.2 validan identidad/registro/idempotencia local sin dispatch/reply de red; estados Hub reales se prueban y correlacionan en WS34/37 bajo G_EXEC, sin mocks ni eventos inventados.

## Aceptación

Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación. Sus dependientes siguen dependiendo de este ID.

## Dependencias

Tareas: WS05, WS12, WS32.1, WS32.2. Gates: G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `scion` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS32/6065616d09e10896296ef81f54465d7e0454550f54ad67def1e2c7c8ecaa8827/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
