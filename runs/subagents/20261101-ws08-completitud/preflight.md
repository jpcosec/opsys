## REFORMULACION

**Objetivo:** completar los productores ausentes en los campos **Nodo** y **Operación** de las UF de WS08 y reflejarlos en `cobertura.md`, con una matriz que demuestre la cobertura.

**Alcance:** una pasada documental sobre `desk/drawer/plans/workspace-documental/borradores/user-flows.md` y `desk/drawer/plans/workspace-documental/cobertura.md`; matriz en `runs/subagents/20261101-ws08-completitud/completeness-matrix.md`; resumen en `runs/subagents/20261101-ws08-completitud/result-summary.md`.

**Repo:** `/home/jp/proyectos/SLDB_1/deskops`.

**Límites:** solo lista cerrada de cambios; no añadir aristas, tareas ni gates; no cambiar textos UF ni gates humanos; no editar `manual.md`, `decisiones.md`, guía, `dag.yaml`, helper, validadores ni código; no commits; no preguntar; WS09, WS11/WS12 como tareas, UI, Scion, push y suite general fuera de alcance.

## AMBIGUEDADES

1. **“añadir un hueco: renderer de RitualDoc/StepDoc y procedimientos (`ui.md:68`); dueño graph_ui, productor WS23.”** No se define qué es un “hueco” ni su sintaxis exacta dentro de **Operación:**. Obliga a inventar formato, ubicación y redacción.

2. **“una fila por cada WS citado en Operación o Error”** frente a **“Un agregado cubre a sus hijos.”** Si se cita `WS13.3` y también un agregado `WS13`, no queda claro si debe haber fila propia para `WS13.3` o si la cubre `WS13`. Obliga a inventar la granularidad de la matriz.

3. **“se anota en result-summary.md para el Supervisor”**: no hay esquema ni campos exigidos para ese resumen. Obliga a inventar su estructura.

## DRY-RUN

1. Leer la tarea, las 10 UF, `cobertura.md` y las referencias de auditoría.
2. En `user-flows.md`, aplicar únicamente las adiciones indicadas en **Nodo:** (UF03, UF05, UF06, UF07, UF09, UF10) y en **Operación:** (UF05: `deskops list rituals`/`show ritual` y el “hueco” del renderer). No tocar UF01, WS22 ni el gate WS16.
3. En `cobertura.md`, modificar solo las filas y columnas indicadas: UF03, UF05, UF06, UF07, UF08, UF09 y UF10; en UF06 añadir `; WS38 publicación` al gate.
4. Crear la matriz con una tabla por UF y columnas ID, dónde se cita, clase, en Nodo, en cobertura. Aplicar la regla de agregado; si la granularidad es ambigua, documentar la interpretación elegida.
5. Escribir `result-summary.md`; si aparece otro productor necesario ausente, anotarlo sin editar.
6. Errores esperables: recuento de UF distinto de 10, matriz vacía, fallo de `build_plan.py --check` o `validate_plan.py --check` por formato, o cambios fuera de lista. Resultado esperado: lista aplicada sin extras, matriz completa, validaciones en verde y Tester independiente PASS.
