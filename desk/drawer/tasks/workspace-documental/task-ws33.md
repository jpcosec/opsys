---
id: WS33
status: candidate
owner_repo: deskops
depends_on:
- WS32
- WS11
requires:
- G_SCION
---

# Vincular mensajes, resultados y decisiones

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

runtime/ (adaptador definido por contrato); modelos/reportes; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Referencias Hub/proyecto/conversación/mensaje/intento y revisión humana explícita; dedup y procedencia. Backend documental, independiente de editor UI.

## Aceptación

G_SCION y contrato público real; importación repetida no duplica ni atribuye conversación completa a un intento. No tocar tablas Scion.

## Dependencias

Tareas: WS32, WS11. Gates: G_SCION. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `scion` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
