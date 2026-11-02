Eres un Tester independiente, en el directorio actual, raíz del repo deskops. Responde en español. Solo puedes leer. No ejecutaste nada: no lo afirmes ni declares comportamiento probado. No corrijas nada. Eres uno de dos Testers sin solape. Esto es revisión de bloques afectados, no de las 65 filas: declara exactamente qué cubriste.

Separa LECTURA PROPIA de DATO DEL SUPERVISOR (runs/subagents/20261102-ws12-correccion/tester-facts.log).

Autoridad: runs/subagents/20261102-ws12-correccion/review-source.md. Contrato: desk/drawer/plans/workspace-documental/contratos/operaciones.md. Diffs: runs/subagents/20261102-ws12-correccion/patch-contrato.diff y runs/subagents/20261102-ws12-correccion/patch-dag.diff. Prefijos: GU/ = ../UIs/graph_ui/frontends/mindmap/ (tests ../UIs/graph_ui/tests/), SL/ = ../sldb/src/sldb/ (tests ../sldb/tests/), DK/ = raíz. Esas rutas existen: ábrelas. Abre cada cita en su línea real. Negaciones con grep.

TU PARTE: hallazgos 7 y 8, decisiones A a E de la autoridad, y la propuesta en desk/drawer/plans/workspace-documental/dag.yaml (revisión 10).

7. HO-11, HO-11b, §7, X02, X03: ¿WS25.2 no se cumple declarando no disponible? ¿WS46 prueba primero la composición pública?
8. HO-10, §8.3, §10.1: tres planos separados; ¿bloqueo global del ack?; WS33.2 conserva su requisito.
A. HO-05: baja frente a quitar referencia; backend local no equivalente; WS19.2. Abre U01 y S03 y los tests citados.
B. HO-07: tres garantías; ¿el encaje WS47 frente a WS45 está justificado? Lee WS45.
C. HO-03 y WS48: ¿es solo contrato de admisión, sin servicio de identidad, autenticación ni coordinación? ¿Hay dependencia accidental hacia WS19.1?
D. WS46: ¿pruebas separadas por destino?, ¿sin imponer wrapper ni modelo?
E. §9.5 ruta por ruta contra GU/serve.py, GU/deskops_routes.py; HO-04, HO-06, HO-09, HO-18.

DAG: WS46, WS47, WS48 contra la forma de los nodos vecinos; depends_on existentes, sin ciclos; scope_nodes de G_WRITE_CONTRACT, G_UI_WRITE y G_SLDB_WRITE contra quien declara el gate; ¿cambió algún compromiso humano de desk/drawer/plans/workspace-documental/decisiones.md (P03, P04, P05, P06, T-P03.1)?; ¿el diff toca `context_review` de un nodo existente?; `promotion` sigue not_authorized; ¿el texto de los nodos coincide con el contrato?

Informe: tabla con objeto, evidencia real archivo:línea, PASS o FAIL; lista final de FAIL con la corrección implicada; cobertura exacta y qué no pudiste verificar. Última línea exacta `RESULTADO: PASS` o `RESULTADO: FAIL`.
