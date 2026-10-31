---
id: WS18
status: candidate
owner_repo: spec2viz
node_role: delivery
depends_on:
- WS09
- WS11
requires:
- G_SPEC_VIEW
---

# Declarar proyecciones de grafo reutilizables

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `spec2viz`. Tamaño relativo: S.

sldb/views/ (rutas confirmadas por el dueño de spec2viz al promover); tests/

Base explícita: `spec2viz:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

ViewDoc con su NotationDoc (la notación que el ViewDoc referencia) para selecciones y notación ya soportadas por spec2viz; no crear UI pages declarativas ficticias.

## Aceptación

Vista portable (el mismo ViewDoc sin código específico del host) renderiza sobre un store real la selección declarada, coincide con ella y el ViewDoc documenta qué selecciona; tareas receptoras en spec2viz se promueven por dueño. Gate receptor G_SPEC_VIEW requerido; no modificar su repo desde este plan.

## Dependencias

Tareas: WS09, WS11. Gates: G_SPEC_VIEW. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS18/98641d44392a5c7f1671142e13a7001e10ed1d57e43076eeeb87459d3ef02e82/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
