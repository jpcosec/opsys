---
id: WS28
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS27
- WS12
requires:
- G_CLOSEOUT
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Integrar verificación y handoff de cierre

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/review/; endpoints; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Verificar con `deskops closeout verify` por el canal del contrato WS12, diagnosticar faltantes y ofrecer handoff explícito con evidencia: a `deskops closeout commit` por CLI en modo manual, o al coordinador si está activo (P03). No commit/close desde HTTP en baseline. G_HUMAN_READ aplica porque es una acción de escritura del baseline.

## Aceptación

UF05 termina cuando `deskops show task` y el commit de closeout confirman el cierre externo y se refresca el estado desde deskops; El diagnóstico muestra los faltantes que reporta `deskops closeout verify`; comando o solicitud no equivalen a cierre. Sin terminal embebido genérico.

## Dependencias

Tareas: WS27, WS12. Gates: G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS28/cf26fc5b867bd80c53d26080c5c8e5d1b000b7cc43542497641525b74e6fcba9/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
