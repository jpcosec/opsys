## REFORMULACION

**Objetivo:** corregir en una sola pasada documental la completitud de los campos **Nodo** de las 10 UF y de la tabla de `cobertura.md`, añadiendo solo productores ya existentes que el propio flujo cita, y demostrarlo con una matriz de completitud.

**Alcance:** lista cerrada de ediciones en UF03, UF05, UF06, UF07, UF08, UF09, UF10 (Nodo y, en UF05, Operación) más filas correspondientes de `cobertura.md` (incluido el Gate de UF06). Se escribe además `completeness-matrix.md`, una tabla por UF con una fila por WS citado en Operación/Error.

**Repo:** `/home/jp/proyectos/SLDB_1/deskops`, sobre `desk/drawer/plans/workspace-documental/borradores/user-flows.md`, `.../cobertura.md` y `runs/subagents/20261101-ws08-completitud/`.

**Límites:** sin aristas, tareas ni gates nuevos; sin tocar textos UF, gates humanos, `manual.md`, `decisiones.md`, guía, `dag.yaml`, helper, validadores ni código; sin commits, push, Scion, WS09/11/12 ni suite general; sin preguntar al solicitante. Autoriza `review-source.md`.

## AMBIGUEDADES

1. «Si la matriz muestra otro productor necesario ausente, NO se edita: se anota en result-summary.md» frente a Done When «matriz sin productor necesario ausente». Obliga a inventar si un hueco detectado invalida la aceptación o solo se reporta.
2. «una fila por cada WS citado en Operación o Error» frente a «No se enumeran […] IDs citados solo para decir que quedan fuera», coexistiendo con la clase «fuera de alcance». Obliga a decidir si WS22/WS12-base llevan fila.
3. «`list ritual`/`show ritual` pasa a `deskops list rituals`/`show ritual`». No queda explícito si el segundo término queda como `deskops show ritual`.
4. Validación exige Tester y `tester-result-summary.md`, pero Roles dice «No hay commits ni corrida de revisiones del Executor». Obliga a decidir si el Executor invoca al Tester o solo entrega.

## DRY-RUN

1. Leer las 10 UF y `cobertura.md`; verificar que cada anclaje textual existe antes de editar.
2. Aplicar en `user-flows.md` las 7 líneas **Nodo:** y las 2 de **Operación:** de UF05, sin otra variación. Control: UF01 Nodo intacto.
3. Sincronizar en `cobertura.md` las filas UF03/05/06/07/08/09/10, incluido el Gate de UF06 (`; WS38 publicación`).
4. Construir `completeness-matrix.md` leyendo Operación y Error de cada UF; clasificar y marcar presencia en Nodo/cobertura.
5. Escribir `result-summary.md` con huecos no editables detectados.
6. Errores previsibles: anclaje textual ausente, recuento de UF distinto de 10, `build_plan.py --check` o `validate_plan.py --check` en rojo, `context_review.py status` no `current`.
7. Resultado esperado: diff limitado a dos documentos más matriz y resumen; checks en verde; sin productor necesario ausente salvo lo anotado para el Supervisor.
