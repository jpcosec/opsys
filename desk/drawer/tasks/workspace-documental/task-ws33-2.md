---
id: WS33.2
status: candidate
owner_repo: deskops
node_role: delivery
parent_id: WS33
depends_on:
- WS32
- WS33.1
requires:
- G_SCION
- G_WRITE_CONTRACT
---

# Registrar decisión humana explícita

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

runtime/ (adaptador definido por contrato); modelos/reportes; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Registrar la decisión humana (aprobar o pedir corrección) con actor humano identificado por el contrato WS12, asociada al intento y, por él, a su tarea. Completado lo reporta Scion; validado y cerrado son estados de deskops (testing y closeout) que este nodo no escribe. Este nodo solo escribe la decisión por la operación que fije el contrato WS12 (si falta, hueco con dueño).

## Aceptación

Una decisión humana queda registrada con actor, referencia al intento y a su tarea, y resultado explícito aprobar o pedir corrección (esta exige el texto de la corrección); completed del agente nunca se registra como aprobado.

## Dependencias

Tareas: WS32, WS33.1. Gates: G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `scion` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS33.2/3cd94d292ec9fe06772c03254e44ffc47b1b595f58ffb68c27e8b194f740462d/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
