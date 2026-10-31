---
id: WS16
status: candidate
owner_repo: graph_ui
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

Gate humano temprano para UF01/UF03 lectura/UF07 diagnóstico y UF08 lectura; desk ejemplo y protocolo en validacion-humana.md. Incluye UF10 arranque/ausencia de desk y UF08 lectura del segundo desk real, sin mutación interdesk.

## Aceptación

Humano real realiza recorrido; agente no sustituye aprobación. Fallos abren correcciones antes de edición. Reportar tiempos y pruebas técnicas por separado. Preparar corpus por WS40; G_HUMAN_READ es requisito de toda mutación del baseline. Renderizaciones read-only pueden desarrollarse en paralelo sin afirmar aceptación de usuario.

## Dependencias

Tareas: WS14, WS15, WS08, WS40, WS41. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
