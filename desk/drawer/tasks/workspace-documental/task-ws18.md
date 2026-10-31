---
id: WS18
status: candidate
owner_repo: spec2viz
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

sldb/views/ (nombres confirmados por contrato); tests/

Base explícita: `spec2viz:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

ViewDoc/NotationDoc para selecciones y notación ya soportadas; no crear UI pages declarativas ficticias.

## Aceptación

Vista portable evaluada sobre store real y documentación de qué selecciona; tareas receptoras en spec2viz se promueven por dueño. Gate receptor G_SPEC_VIEW requerido; no modificar su repo desde este plan.

## Dependencias

Tareas: WS09, WS11. Gates: G_SPEC_VIEW. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
