---
id: WS07
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS06
requires: []
---

# Mantener registro trazado de decisiones acordadas

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

decisiones.md; `baseline_proposal` y parameters.source_mode en dag.yaml

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Reutilizar decisiones.md y owner-decisions.json: respuestas humanas literales 0–2, mapeo P01–P09, actor/fecha/fuente. P07/P09 son defaults técnicos delegados, no firmas humanas. source_mode=editable condicionado a G_SOURCE. Responsabilidad producto/recepción graph_ui/sldb/spec2viz es del solicitante; operador y permisos Scion se designan al abordar E sin bloquear L/M. baseline_proposal es el string raíz de dag.yaml suministrado: conservar base acordada y actualizar solo ante nueva decisión explícita con fuente verificable. Cobertura documental se refiere a decisiones.md + owner-decisions.json y covered_work de este nodo, no sustituye cobertura de UFs ni auditorías WS06.

## Aceptación

Registro concreto de cada Pxx con tipo humano/técnico, actor, fuente y nodos/gates. No repetir preguntas ya resueltas ni inferir aceptación de API/UI o permiso Scion. Verificar y reutilizar cobertura documental ya producida; actualizar solo por cambio real de decisión.

## Dependencias

Tareas: WS06. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS07/14937e6d9d2dc0bb7ad5eeae6d3e2265a6e424bd1bebcaa5a2f8761e4ebc67fd/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
