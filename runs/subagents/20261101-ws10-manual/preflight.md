## REFORMULACION

- **Objetivo:** completar `desk/drawer/plans/workspace-documental/borradores/manual.md` con esquema conceptual por capítulo —propósito, entradas, salidas, etiqueta y evidencia—, definiciones de disponibilidad y ejemplo fijo P08, sin redactar el manual.
- **Alcance:** conservar índice 1–17 y numeración; reutilizar texto existente; contrastar con auditorías WS02–WS04; remitir CLI a `docs/operator-manual.md`; no incluir pasos, capturas ni nombres de controles.
- **Repo:** `/home/jp/proyectos/SLDB_1/deskops`. Executor escribe solo `manual.md` y `runs/subagents/20261101-ws10-manual/result-summary.md`.
- **Límites:** fuera WS09/WS11/WS12, UI, Scion, push, `dag.yaml`, validadores, helper y suite general; no reabrir P01–P09; `execution_authorized` global sigue `false`.

## AMBIGUEDADES

1. **“lo no auditado queda como hueco con dueño”**: no define quién es el dueño ni cómo nombrarlo. Obligaría a inventar responsables o un criterio de asignación.
2. **“contrastados con las auditorías WS02-WS04”** y **“WS03/WS04 llegan de forma transitiva por WS06/WS07”**: no hay mapa explícito entre WS02–WS04 y `auditoria/deskops.md`, `infraestructura.md`, `ui.md`. Obligaría a inventar la correspondencia.
3. **“Añadir por capítulo propósito, entradas y salidas, y una etiqueta con su evidencia”**: no aclara si se aplica a los 17 capítulos ni cómo etiquetar capítulos conceptuales sin capacidad. Obligaría a decidir sin regla.
4. **“ejemplo fijo acordado P08: Taller... productor WS40”**: no fija su etiqueta. Al ser corpus futuro y depender de WS40, podría ser `bloqueado` o `propuesto`. Obligaría a inventar el criterio.
5. **“Las capacidades del CLI se remiten a docs/operator-manual.md”**: no indica si esos capítulos llevan esquema completo o solo remisión. Obligaría a elegir.

## DRY-RUN

Ejecutor futuro: leer `manual.md`, `docs/operator-manual.md`, `decisiones.md` y auditorías; editar solo `manual.md`, preservando índice y texto, añadiendo definiciones, ejemplo P08 y bloques por capítulo con etiqueta/evidencia; escribir `result-summary.md`. Supervisor ejecutará `test -s`, `build_plan.py --check`, `validate_plan.py --check` y `context_review.py status`; Tester de solo lectura dejará `tester-result-summary.md`.

Errores previsibles: falta de auditoría o mapa, etiqueta `disponible` sin acta, renumeración, edición de archivos prohibidos, o fallo de `build/validate`. Resultado esperado: manual completado sin pasos ni capturas inventados, checks en verde y Tester PASS.
