## REFORMULACION

**Objetivo:** corregir en `desk/drawer/plans/workspace-documental/borradores/vistas.md` las afirmaciones no sostenidas de F05, F16, F18a, F18b y F12, más las precisiones de F03/F12 y una nota final, aplicando una lista cerrada de diez ítems.

**Alcance:** una sola pasada; cotejar cada cambio con su fuente directa, no por rango. El Executor escribe solo `vistas.md` y `runs/subagents/20261101-ws09-correccion/result-summary.md`; no hace commits, revisiones ni preguntas. Autoriza `review-source.md`.

**Repo:** `/home/jp/proyectos/SLDB_1/deskops`.

**Límites:** no editar user-flows, cobertura, manual, decisiones, guía, `dag.yaml`, helper, validadores, código ni repos hermanos. No inventar progreso, StepDoc, autoavance, endpoint, semántica ni confirmación de ruta. Los estados no cambian: “23 bloqueado”.

## AMBIGUEDADES

1. **“Los estados no cambian: 23 bloqueado.”** No aclara si “23” es el número de fichas, un estado concreto o un contador que debe permanecer. Aplicarlo exige inventar qué se conserva exactamente.
2. **“NotationDoc se clasifica por su origen real según infraestructura.md, sin cambiarlo por reflejo.”** No indica la clasificación esperada ni el pasaje exacto. Obliga a inferir la clase si la fuente no es unívoca.
3. **“F05 Origen y Campos deben nombrar esos pasos de prosa.”** No fija redacción ni estructura exacta de ambos campos; puede llevar a inventar formulaciones.
4. **“Corregir los campos Evidencia de las fichas tocadas, y Clase o Renderer solo si el cambio lo exige.”** “Si el cambio lo exige” es un límite subjetivo; obliga a decidir sin criterio cerrado.
5. **“Tester focal PASS sobre los bytes congelados antes del closeout”** y **“revisión afectada renovada”**. No define mecanismo de congelación, artefacto de revisión ni quién los produce; el Executor tiene prohibido revisar.

## DRY-RUN

Un ejecutor futuro abriría la tarea, `review-source.md`, `ritual.py:65-67`, `testing.md`, `execution.md`, `infraestructura.md:115,121`, `deskops.md:113,266`, `user-flows.md:179` y `dag.yaml:1222-1224`. Luego editaría solo `vistas.md`: quitaría la frase de F05 sobre “0 StepDoc”; afirmaría que `RitualDoc.steps` son prosa inline; ajustaría F16 con el mismo criterio; en F18a separaría YAML authored de Spec/SpecNode derivados y clasificaría NotationDoc por origen; en F18b escribiría ruta “prevista, pendiente de confirmación y registro en WS18”, conservando repo owner y recibo; en F12 documentaría efectos de `atoms validate` (`ensure_workspace`, andamiaje, `tag-namespaces.yaml`), mantendría `stores check` no corroborado, acotaría F03 y precisaría `Corpus.rank`/GET y `ProjectionDoc`; añadiría “Candidaturas sin productor” sin nodos nuevos; corregiría Evidencia y solo Clase/Renderer si procede. Escribiría `result-summary.md` por ítem con fuente abierta y resultado. Ejecutaría `grep -c "^### F"` (esperado 23), `build_plan.py --check`, `validate_plan.py --check` y `context_review.py status`. Errores probables: referencias de línea desplazadas, rutas de scripts o fuente ausente. Resultado esperado: diez ítems aplicados, ninguno extra, checks en verde; el Tester queda fuera del Executor.
