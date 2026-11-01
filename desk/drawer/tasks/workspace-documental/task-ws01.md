---
id: WS01
status: candidate
owner_repo: deskops
node_role: delivery
depends_on: []
requires: []
---

# Fijar brief y glosario autosuficientes

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

brief.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Brief/glosario ya authored y cubiertos por recibo covered_work. Al promover auditorías verificar hash/alcance; no reescribir si no cambió decisión/contrato. Si cambia realmente el encargo, editar solo brief.md con acuerdos textuales y vocabulario documento/nodo/vista/renderer/consulta/foco; sin chat invisible.

## Aceptación

brief.md enlaza decisiones.md como registro Pxx completo; no editar decisiones.md desde este nodo. Acuerdos textuales tienen actor/fuente y distinciones glosario legibles. Coordinator compara reformulación/dry-run de review barato aislado ritual-context-review con intención y explicita hallazgos/disposición; APTO no basta. Cobertura documental actual satisface elaboración del brief, no lifecycle cerrado ni autorización producto.

## Dependencias

Tareas: ninguna. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS01/96fb3f6cf136addd87f848f41fea6cccaa8bb80971bcea6beeea4578d3977f2e/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
