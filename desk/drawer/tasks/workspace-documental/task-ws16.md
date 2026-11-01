---
id: WS16
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS14
- WS15
- WS08
- WS40
- WS41
requires: []
---

# Validar con humano lectura y descubrimiento

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

runs/subagents/workspace-documental-acceptance/lectura/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Gate humano temprano para UF01/UF03 lectura/UF07 diagnóstico y UF08 lectura; consume el manifiesto de WS40 y sigue el protocolo de validacion-humana.md, sin crear corpus propio. Incluye UF10 arranque/ausencia de desk y UF08 lectura del segundo desk real, sin mutación interdesk.

## Aceptación

Humano real realiza recorrido; agente no sustituye aprobación. Ante un fallo, WS16 lo registra y supervisor del repo receptor atribuye el fallo por evidencia; si aún no se aísla causa, registra incidente/diagnóstico en repo/superficie antes de asignar nodo y abrir corrección; WS16 no la implementa. Reportar tiempos y pruebas técnicas por separado. Preparar corpus por WS40; G_HUMAN_READ habilita uso de mutaciones del baseline en UI, no bloquea desarrollo/pruebas aisladas API. Renderizaciones read-only pueden desarrollarse en paralelo sin afirmar aceptación de usuario. Mide aperturas y búsquedas; guardados no aplican hasta WS30. Superar objetivos P08 de apertura/búsqueda/arranque es fallo medido: registrar y mantener gate pendiente hasta corrección o revisión explícita del objetivo por humano con razón/evidencia, nunca rebajar umbral silenciosamente.

## Dependencias

Tareas: WS14, WS15, WS08, WS40, WS41. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS16/85f641442b323c36066a66d89cd239dd911279fea16d8c6425201c7298cf1664/attempt-2']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
