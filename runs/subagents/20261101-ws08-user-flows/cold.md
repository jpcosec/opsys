## REFORMULACION
Objetivo: completar `desk/drawer/plans/workspace-documental/borradores/user-flows.md` para que UF01–UF10 incluyan entrada, salida, operación, error, nodo y gate humano, citando operaciones de `auditoria/{deskops,infraestructura,ui}.md` y marcando huecos sin inventar capacidades.

Alcance: conservar textos y precisiones existentes; añadir por UF tabla/lista con los seis campos. Operación será lista completa con cita; si falta, «hueco» con repo dueño y productor; error «no definido» con productor. Gate humano solo WS16/30/37/39 o «ninguno adicional»; WS29 se anota como prueba técnica propia. También escribir `runs/subagents/20261101-ws08-user-flows/result-summary.md`.

Repo: `deskops`; superficie documental `desk/drawer/plans/workspace-documental/`. El Executor solo edita esos dos archivos. El Supervisor valida, commitea, revisa y cierra. Tester independiente solo lectura.

Límites: no reabrir P01–P09, no preguntar al solicitante, no afirmar capacidades sin cita, no tocar WS09/11/12, código UI, Scion, `dag.yaml`, validadores, helper ni suite general. `execution_authorized` global sigue false; G_PRODUCT no es aceptación de producto/API/UI. No hay arista con WS10.

## AMBIGUEDADES
1. «Gate humano = WS16, WS30, WS37 o WS39, o “ninguno adicional”» frente a `cobertura.md`, que para UF01 incluye «WS43 publicación real». Obligaría a inventar si WS43 es gate humano, hito de publicación o dato omitido; afecta la columna gate de UF01.
2. «escribir “hueco” con repo dueño y productor, y en error “no definido” con productor». «Productor» no está definido: ¿task, nodo, repo, autor o sistema? Obligaría a inventar el identificador exigido en cada hueco/error.
3. «Revisiones afectadas renovadas» en Done When. No se enumeran revisiones ni criterio de afectación; obligaría a inventar qué actas/revisiones root deben renovarse, en tensión con «No reabrir decisiones P01-P09» y la autorización acotada.

## DRY-RUN
Un ejecutor futuro leería `user-flows.md`, `validacion-humana.md`, `cobertura.md`, `decisiones.md` y las tres auditorías. Por cada UF01–UF10 conservaría el texto y añadiría una tabla con: entrada, salida, operación (lista con cita `auditoria/*.md`), error, nodo DAG y gate humano. Mapearía gates desde `validacion-humana.md`/`cobertura.md`, anotaría WS29 como prueba técnica y dejaría «hueco»/«no definido» donde no haya cita. Escribiría `result-summary.md` con citas y estado de reuso.

Errores esperables: operación sin cita → marcar hueco, no completar por memoria; nodo dudoso → no elegir uno principal; gate WS43 → resolver ambigüedad antes de editar; `grep -c "^## UF"` distinto de 10 → corregir estructura. El Supervisor ejecutaría build/validate/status; fallos por referencias rotas obligan a corregir solo el borrador. Resultado esperado: 10 UF con seis campos, huecos explícitos, checks verdes y Tester PASS.
