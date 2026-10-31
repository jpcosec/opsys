---
id: WS32.1
status: candidate
owner_repo: deskops
node_role: delivery
parent_id: WS32
depends_on:
- WS05
- WS12
requires:
- G_CLOSEOUT
- G_SCION
- G_WRITE_CONTRACT
---

# Separar identidad de intento y dispatch

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

deskops/runtime/scion.py; models/run.py; services/closure.py; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Refinar el ticket de external_references.scion, sin segundo pipeline: intento no es slug; dispatch intent (intención registrada) y confirmed (Scion aceptó) como hechos separados del RunDoc; ambos se registran en el registro por intento que WS32.2 vuelve manifiesto canónico. Confirmed = respuesta de la API pública de Scion con la identidad que exponga, a comprobar en WS05/WS44.

## Aceptación

Dos intentos del mismo agente y un dispatch fallido (rechazo de la API o timeout) conservan identidades distintas, evidenciadas por ids de intento propios, generados por deskops antes del dispatch; cambios de RunDoc por el flujo SLDB de modelos (registro y edición de documento trackeado con CLI sldb), no edición ad hoc.

## Dependencias

Tareas: WS05, WS12. Gates: G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `scion` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS32.1/71f96d632110f2bc5ceba73997b2b1e68ce6d3e060522e5df93bac926bced593/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
