---
id: WS34.2
status: candidate
owner_repo: deskops
node_role: delivery
parent_id: WS34
depends_on:
- WS33
- WS12
- WS34.1
requires:
- G_EXEC
- G_SCION
- G_WRITE_CONTRACT
---

# Exponer respuesta autorizada

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

runtime/; cli/commands/runtime.py o API definida; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Adaptador público restringido para reply vinculado al intento, con timeout/errores y autoridad del coordinador.

## Aceptación

G_SCION/G_EXEC pasan; agente real demuestra respuesta vinculada al intento correcto y un timeout se reporta como fallo sin confirmación, con el umbral del contrato WS12. No mandar mensajes en la tarea de planificación.

## Dependencias

Tareas: WS33, WS12, WS34.1. Gates: G_EXEC, G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS34.2/32d7c2e2adf5b34d3a953d3219c37830a73c67469f71027f23de6567a1760835/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
