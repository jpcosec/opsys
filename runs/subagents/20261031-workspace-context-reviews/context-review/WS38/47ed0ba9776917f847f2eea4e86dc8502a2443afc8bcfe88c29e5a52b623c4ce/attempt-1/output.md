## REFORMULACION
Propósito: añadir al manual la operación de delegación y la revisión trazable demostradas en WS37. Resultado: capítulo publicado en `docs/workspace-user-manual.md` y átomos vinculados en `desk/atoms/`, con cada paso referido al acta de WS37 y a operaciones reales, fallos registrados documentados y mención de que `G_EXEC` es necesario para operar. Repo dueño: `deskops`. Límites: solo documentación; depende de WS37 y WS31; requiere `G_HUMAN_DELEGATE`; no autoriza ejecución ni promoción.

## AMBIGUEDADES
1. «output_scope: docs/workspace-user-manual.md; desk/atoms/ vinculados» — no se fija qué átomos crear ni con qué criterio quedan «vinculados»; la aceptación no menciona átomos. Obligaría al ejecutor a inventar la lista y el criterio de enlace, y a decidir si basta un átomo por capítulo o por acuerdo. Podría resolverse en la promoción si esta fija archivos, pero no se declara que los átomos sean detalle delegado.

## DRY-RUN
Lecturas previstas: `dag.yaml` (WS38, aristas WS37/WS31, gates `G_HUMAN_DELEGATE`/`G_EXEC`), `context-review-guide.md`, `brief.md`, `alcance.md`, `borradores/manual.md`, acta de WS37 en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md` y manual publicado por WS31. Cambios previstos: edición de `docs/workspace-user-manual.md` (capítulo de delegación/revisión trazable) y creación de átomos vinculados. Dependencias: WS37 aporta acta y satisface `G_HUMAN_DELEGATE`; WS31 aporta manual base con capítulo Scion marcado propuesto; `G_EXEC` se documenta como requisito, no se satisface aquí. Validaciones futuras: cada paso enlaza al acta y a operaciones reales; fallos del acta aparecen documentados; se declara `G_EXEC`; etiquetas, links y relación átomo→documento verificados; sin promoción ni ejecución.

## FUTURO
WS37 produce el acta y resuelve el gate; WS31 entrega el manual base y su capítulo propuesto; un humano decide la promoción y el TaskDoc con archivos, textos y escenarios; WS37 puede exponer fallos que condicionen el contenido; WS29/WS39 y el ramal Scion quedan fuera de este nodo.
