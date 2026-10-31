---
id: WS32.2
status: candidate
owner_repo: deskops
node_role: delivery
parent_id: WS32
depends_on:
- WS05
- WS12
- WS32.1
requires:
- G_CLOSEOUT
- G_SCION
- G_WRITE_CONTRACT
---

# Hacer idempotente manifiesto y cierre

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

deskops/runtime/scion.py; models/run.py; services/closure.py; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Manifiesto, RunDoc y cierre consistentes e idempotentes sobre el intento correcto (el identificado por el id de intento que cita el cierre, nunca por agente o slug). Manifiesto = registro canónico por intento que materializa RunDoc y registros de closeout, según el ticket de external_references.scion (campos mínimos: id de intento, identidad de agente, identidad de run si la API la expone, timestamps, hash de sesión, evidencia y commit de cierre).

## Aceptación

Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos; manifiesto, RunDoc y registros de closeout coinciden en id de intento, hash de sesión y evidencia.

## Dependencias

Tareas: WS05, WS12, WS32.1. Gates: G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `scion` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS32.2/4819deb2d5062bb72ddd5010cdaa360fa84a62ef6b42209826f776346121f225/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
