---
id: WS32
status: candidate
owner_repo: deskops
depends_on:
- WS05
- WS12
requires:
- G_CLOSEOUT
- G_SCION
- G_WRITE_CONTRACT
---

# Unificar identidad de intento y cierre Scion

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

deskops/runtime/scion.py; models/run.py; services/closure.py; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Refinar ticket existente, sin segundo pipeline: intento no es slug, dispatch intent/confirmed separado, manifiesto/RunDoc/cierre consistentes e idempotentes.

## Aceptación

G_CLOSEOUT pasa; dos intentos mismo agente, dispatch fallido y finalización repetida conservan identidades/evidencia; schema mediante SLDB.

## Dependencias

Tareas: WS05, WS12. Gates: G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `scion` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
