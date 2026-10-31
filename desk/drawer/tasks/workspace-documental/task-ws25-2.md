---
id: WS25.2
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS25
depends_on:
- WS12
- WS16
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Capturar en drawer o protoátomo

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: S.

frontends/mindmap/views/workspace/capture/; endpoints autorizados por el contrato WS12; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Captura interna con destino elegido explícitamente por la persona usuaria —candidato de drawer o protoátomo— mediante operaciones permitidas por el contrato WS12, sin exigir tarea; cada destino se prueba por separado.

## Aceptación

UF02: una captura persiste tras recargar en el destino elegido, con origen y sin tarea implícita. Permisos del contrato aplicados. Origen = referencia tipada al soporte del que nace la captura (ruta o mensaje), con representación fijada por el contrato WS12; los orígenes ruta y mensaje se registran y se muestran tras recargar.

## Dependencias

Tareas: WS12, WS16. Gates: G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS25.2/9ca33231431e3e554141bbec8ab970439e37332552fd9c00fb943624b0bb7bf7/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
