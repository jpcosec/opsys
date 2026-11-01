## REFORMULACION
Objetivo: completar `desk/drawer/plans/workspace-documental/borradores/user-flows.md` para que UF01–UF10 incluyan entrada, salida, operación, error, nodo y gate humano, con operaciones citadas de las auditorías y huecos marcados. Repo: `/home/jp/proyectos/SLDB_1/deskops`. Alcance: conservar textos existentes; mapear a operaciones de WS02–WS04; cubrir UF07/WS29, arranque, multidesk, schemas y modo degradado; UF02 limitada a desk/contexto local; UF08 solo lectura; delegación condicionada a G_SCION/G_EXEC. Límites: Executor escribe solo `user-flows.md` y `runs/subagents/20261101-ws08-user-flows/result-summary.md`; Supervisor valida, commitea y cierra; Tester solo lectura. Fuera: WS09, WS11, WS12, UI, Scion, push, `dag.yaml`, validadores, helper, suite general. No reabrir P01–P09.

## AMBIGUEDADES
1. «hueco» con repo dueño y productor»: no define qué identifica al «productor» (nodo, tarea, artefacto). Obligaría a inventar un productor cuando la auditoría no lo nombre.
2. «revisiones afectadas renovadas»: no enumera qué revisiones ni quién las renueva. Obligaría a inventar el conjunto o atribuir la renovación al Executor.
3. «Nodo = ID del DAG»: solo hay regla de «hueco» para operación ausente; si falta nodo no hay fallback. Obligaría a inventar un ID o usar «hueco» sin autorización explícita.
4. «cambios (UF07/WS29)» y «modo degradado (UF07, fallo de backend/dependencia)»: asigna UF07 a dos focos sin aclarar si una misma UF cubre ambos o es errata. Obligaría a decidir/inventar el mapeo.
5. «operación pendiente de confirmar en el contrato WS12; no se da por disponible»: no fija si el campo operación escribe el pendiente o «hueco». Obligaría a inventar representación si se exige cita.

## DRY-RUN
1. Leer `user-flows.md`, `validacion-humana.md`, `cobertura.md`, `decisiones.md`, `dag.yaml`, auditorías `deskops/infraestructura/ui.md` y `ws07-cobertura-efectiva.md`.
2. Conservar UF01–UF10; bajo cada UF añadir tabla o lista con entrada, salida, operación (lista citada), error, nodo y gate humano; marcar «hueco» con dueño/productor y «no definido» con productor; WS29 como prueba técnica propia; gates WS16/30/37/39 o «ninguno adicional»; respetar UF02, UF08 y delegación condicionada.
3. Escribir `result-summary.md` con citas y estado de reuso; no tocar otros archivos.
4. Validar: `grep -c "^## UF"` = 10; `build_plan.py --check`; `validate_plan.py --check`; `context_review.py status`; Tester PASS.
Errores esperables: recuento ≠10, checks no verdes, cita ausente, invención de operación/nodo, Tester FAIL. Resultado esperado: 10 UF completas, sin prometer fuera de alcance, checks verdes y PASS.
