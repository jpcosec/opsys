## REFORMULACION

- **Objetivo:** completar `vistas.md` con 20 fichas (F01–F20, una por fila de sus dos tablas, 12+8) en sección nueva «Fichas por fila», con 13 campos obligatorios (Propósito, Origen, Identidad, Contrato, Campos y relaciones, Renderer, Navegación, Acción/dueño, Destino de escritura, Error, Estado, Clase, UF, Evidencia), citando auditorías y UFs; nada inventado.
- **Alcance:** inventariar fuente, queries, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas existentes; reutilizar textos existentes; basarse en auditorías WS02–04, decisiones y UFs WS08. Fuera: WS11, WS12, UI, Scion, push, `dag.yaml`, otras fuentes, helpers, validadores, suite general.
- **Repo:** `deskops` (cwd `/home/jp/proyectos/SLDB_1/deskops`).
- **Límites:** el Executor escribe solo `desk/drawer/plans/workspace-documental/borradores/vistas.md` y `runs/subagents/20261101-ws09-vistas/result-summary.md`; sin commits ni revisiones; sin preguntar; `execution_authorized` global sigue `false`.

## AMBIGUEDADES

1. Scope dice «Fuera de alcance: … helper, validadores, suite general», pero Validation exige `validate_plan.py --check` y `build_plan.py --check`. Obliga a inventar si ejecutar validadores está permitido o prohibido.
2. Implementation Path manda leer `reconciliacion.md`, ausente de `references`, `files` y del fuera-de-alcance. Obliga a inventar su ubicación/validez.
3. «El campo «aceptación mediante user-flow» de la ficha original es esto»: no hay ficha original ni plantilla. Obliga a inventar semántica del campo UF.
4. Evidencia exige «cita archivo:línea … y de user-flows.md», pero la regla de campos sin evidencia no cubre cómo rellenar Evidencia vacía. Obliga a inventar placeholder o cita.
5. «Si ningún nodo lo produce: «sin productor en el DAG» y repo dueño»: no define cómo identificar «repo dueño». Obliga a inventar mapeo.
6. «propuesto si no [hay dependencia o contrato pendiente]»: no define qué cuenta como «dependencia identificada». Obliga a juicio no pautado.

## DRY-RUN

- **Archivos:** añadir sección «Fichas por fila» tras las tablas de `vistas.md` sin borrar/reescribir lo previo; crear `runs/subagents/20261101-ws09-vistas/result-summary.md`.
- **Cambios:** con Read completo de `vistas.md`, `user-flows.md`, `manual.md`, `decisiones.md` y auditorías, emitir `### F01`…`### F20` (con sufijo `a/b` si procede) con los 13 campos; usar «no definido» + productor (WS11/WS12/nodo DAG/repo dueño); citar `archivo:línea`; Estado nunca `disponible` (sin actas).
- **Errores esperables:** `grep -c "^### F"` ≠ 20 por fila omitida o encabezado distinto; validadores en rojo si se rompe formato; evidencia inventada o cita truncada si se usa `cut`; conflicto si se ejecutan validadores pese al fuera-de-alcance.
- **Resultado esperado:** 20 fichas completas, validadores en verde (o justificación del conflicto), `tester-result-summary.md` PASS y `result-summary.md` con reuso, huecos y límites.
