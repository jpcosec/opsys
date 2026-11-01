---
id: WS33.1
status: candidate
owner_repo: deskops
node_role: delivery
parent_id: WS33
depends_on:
- WS32
requires:
- G_SCION
- G_WRITE_CONTRACT
---

# Vincular mensajes y resultados al intento

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

runtime/ (adaptador definido por contrato); modelos/reportes; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Referencias Hub/proyecto/conversación/mensaje/intento y resultados, con deduplicación y procedencia. Backend documental, independiente de editor UI. Clave de deduplicación: Hub + proyecto + conversación + id de mensaje. Los resultados se identifican por intento y por el identificador que exponga la fuente, a comprobar en WS05/WS44, y se deduplican por Hub + proyecto + intento + id de fuente, conservando procedencia. Solo se vinculan mensajes y resultados con referencia a un id de intento existente; un mensaje con varios intentos o sin intento resoluble no se vincula y registra la procedencia como hueco.

## Aceptación

Con contrato público real, una importación repetida (mismo Hub/proyecto y conversación) no duplica mensajes ni resultados ni atribuye una conversación completa a un intento; los mensajes no vinculados quedan como hueco de procedencia. No tocar tablas Scion.

## Dependencias

Tareas: WS32. Gates: G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `scion` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS33.1/dadf265d4cba029d2ab6a76928a19f2efa6d1efa0b15bf3725e33816de415857/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
