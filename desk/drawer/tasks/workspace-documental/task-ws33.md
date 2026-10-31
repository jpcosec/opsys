---
id: WS33
status: candidate
owner_repo: deskops
node_role: aggregate
children:
- WS33.1
- WS33.2
depends_on:
- WS32
- WS11
- WS33.1
- WS33.2
requires:
- G_SCION
---

# Vincular mensajes, resultados y decisiones

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

Agregado: salidas de WS33.1, WS33.2

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Referencias Hub/proyecto/conversación/mensaje/intento y decisión humana explícita (WS33.2); dedup y procedencia. Backend documental, independiente de editor UI.

## Aceptación

Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación. Sus dependientes siguen dependiendo de este ID.

## Dependencias

Tareas: WS32, WS11, WS33.1, WS33.2. Gates: G_SCION. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `scion` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS33/02cca2e66c67e64a1e426f496c6dbdc1b07637c6ccb6fa6ad6ba0e8348cd8d07/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
