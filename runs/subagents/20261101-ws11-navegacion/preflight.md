## REFORMULACION
**Encargo:** crear `desk/drawer/plans/workspace-documental/contratos/navegacion.md` con 13 secciones ordenadas sobre identidad, origen, resolución repo/store, foco, enlaces, multidesk read-only, errores de lectura, ViewDoc, authored/derivado, huecos y deltas de `graph_ui`, citando APIs verificadas por lectura real en los commits `graph_ui 134a665` y `sldb 77bd6d00`.  
**Alcance:** solo ese contrato y `runs/subagents/20261101-ws11-navegacion/result-summary.md`; lectura de auditorías, borradores, decisiones, reconciliación, DAG y código real.  
**Repo:** workspace documental deskops; repos hermanos solo lectura.  
**Límites:** sin commits, UI, Scion vivo, WS12, push, `dag.yaml`, helper, validadores ni suite general; autorización global sigue en false; no preguntar al solicitante.

## AMBIGUEDADES
1. «aliases y roots autorizados» no enumera cuáles son. Obligaría a inventar la lista de aliases/roots permitidos.
2. «rutas seguras» no define criterio. Obligaría a inventar la política de validación de rutas.
3. «mapear recepción requerida por delta en graph_ui (actor P01, IDs y efectos)» no da los IDs ni el catálogo de gates. Obligaría a inventar IDs o nombres de gate.
4. «si WS13.1 o el catálogo lo comprometen» no identifica dónde están esos compromisos ni su criterio. Obligaría a inventar qué constituye un compromiso.
5. «G_SPEC_VIEW se obtiene separadamente» no indica fuente, formato ni responsable. Obligaría a inventar su origen.
6. «frontends/workspace/ no adoptado no es base» no aclara si puede citarse como evidencia negativa. Obligaría a decidir si se menciona o se omite.
7. Validation exige un `tester-result-summary.md`, pero Roles solo asigna al Executor dos archivos. No queda claro quién lo crea ni cuándo. Obligaría a atribuir una escritura no autorizada al Executor.

## DRY-RUN
1. Leer las referencias listadas y los nodos consumidores; localizar `runs/subagents/20261101-ws09-vistas/result-summary.md` para trazabilidad.
2. Abrir en `../UIs/graph_ui` y `../sldb` los archivos/símbolos citados por auditorías; registrar `path:línea`, símbolo y commit.
3. Redactar `navegacion.md` con las 13 secciones exactas; tablas de foco, huecos (instancia/vínculo/consulta/API/renderer) y deltas (`ID`, efecto, actor P01, gate, «sin acta registrada»). No inventar actas ni APIs.
4. Redactar `result-summary.md` con decisiones, evidencias y huecos.
5. Ejecutar `test -s`, `build_plan.py --check`, `validate_plan.py --check` y `context_review.py status`.  
**Errores previsibles:** archivos o commits ausentes, símbolos no verificables, referencias a WS13.1/catálogo inexistentes, o helper marcando revisiones.  
**Resultado esperado:** contrato no vacío, checks en verde, huecos clasificados y deltas bloqueados hasta recibo; Tester independiente PASS; sin commits.
