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

sldb/views/ (ruta y registro confirmados según el contrato al promover; con output_base spec2viz (raíz del repo) puede ser spec2viz/sldb/views/ y el prefijo textual no cambia el dueño); tests/

Base explícita: `spec2viz:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Autoría de ViewDoc y NotationDoc concretos (la notación que el ViewDoc referencia) para selecciones y notación ya soportadas por spec2viz, y su comprobación sobre stores reales reutilizando el evaluador evaluate_view y las rutas /api/views de graph_ui (fila C-37 de reconciliacion.md) y la notación de spec2viz resolve_documents (fila C-49). ViewDoc es datos sin ruta de store y el evaluador recibe el store por petición, así que no se pide portabilidad genérica, ni servicio, CLI o runtime fuera de graph_ui, ni extraer o compartir el evaluador. No crear UI pages declarativas ficticias. Selecciones concretas y notación requerida vienen de catálogo WS09 y contrato WS11, contrastados con capacidades WS03; si catálogo no fija selección mínima, detener promoción y corregir ese contrato antes de elegir una. No inventar selección aquí.

## Aceptación

Los ViewDoc y NotationDoc concretos definidos por WS09/WS11 se evalúan con el camino existente de graph_ui sobre un store real, la selección coincide con la declarada en catálogo WS09 y contrato WS11, que son la fuente; el ViewDoc la repite y el ViewDoc documenta qué selecciona; no se alega que una prueba con dos stores demuestre el mismo payload completo (cambia filtros); tareas receptoras en spec2viz se promueven por dueño. Gate receptor G_SPEC_VIEW requerido; este paquete documental deskops no escribe en spec2viz; la futura TaskDoc de WS18 se promueve y ejecuta en spec2viz por su supervisor/Executor, con recepción G_SPEC_VIEW para ese delta.

## Dependencias

Tareas: WS09, WS11. Gates: G_SPEC_VIEW. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS18/be67fa9b84c43a6c41d8791d1e3c1bcace288ea97a9c71d2fda5c19d1407d27f/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
