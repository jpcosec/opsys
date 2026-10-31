Eres un Tester independiente de una matriz documental, en el directorio actual, raíz del repo deskops. Responde en español. Solo puedes leer. No leas kimun. Comprueba contra las auditorías desk/drawer/plans/workspace-documental/auditoria/ y, cuando haga falta, el código en ../UIs/graph_ui, ../sldb, ../pron y ../spec2viz.

Lee runs/subagents/20261031-ws06-reconciliacion/testing-handoff.md, la TaskDoc (desk/tasks/task-ws06*), runs/subagents/20261031-ws06-reconciliacion/preflight-disposition.md, runs/subagents/20261031-ws02-04-checkpoint/approval.md, runs/subagents/20261031-ws06-reconciliacion/result-summary.md y runs/subagents/20261031-ws06-reconciliacion/tester-facts.log. La matriz está al final de desk/drawer/plans/workspace-documental/reconciliacion.md, sección «Matriz de correspondencia WS06».

Comprueba:
1. Muestrea 12 filas «ya cubierto»: ¿la capacidad es observable en el path o símbolo citado? ¿el commit corresponde? ¿alguna atribuye más de lo que el código hace o implica aceptación ampliada?
2. Muestrea 10 filas «nuevo delta» y busca con grep si existe base o ticket reutilizable: una fila que proponga construir lo que ya existe es FAIL.
3. Las tres «extender ticket»: ¿caben en el ticket citado? ¿se propone algo paralelo a los tickets de edición y Changes, que comparten serve.py, views/workspace/ y docs/workspace-ui.md?
4. Filas dudosas: C-23, C-41, C-50, C-55, C-64. Di si su clasificación se sostiene.
5. Reglas: frontends/workspace no adoptado; ViewDoc con reutilización primero, sin evaluador de cero; expected como comparación por valor sin acreditar CAS ni frescura de API/CLI; Scion RunDoc conserva WS32/33 sin requerir WS05; responsable «no designado en P01» donde corresponde, sin inventar; operador Scion solo en ramal E; ninguna fila declara aceptado un delta. Una fila que use la palabra acepta en otro sentido no es defecto si no acepta un delta: revisa C-49.
6. Duplicados: dos filas con la misma capacidad, y filas agrupadas por nodo en vez de capacidad.
7. Cobertura: muestrea 10 nodos «sin delta» y juzga si el motivo es real.
8. runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md: cada ajuste con su evidencia real; ninguno aplicado; ¿falta alguno imprescindible o sobra alguno?

Tu respuesta completa es el informe: tabla con objeto, evidencia real (archivo:línea leído), PASS o FAIL; hallazgos; y como última línea exacta `RESULTADO: PASS` o `RESULTADO: FAIL`. FAIL si una fila contradice su fuente, propone rehacer lo existente o acepta un delta. Un defecto de cita que no cambia la conclusión es hallazgo menor. Lo no verificado se declara NO VERIFICADO; lo de tester-facts.log se declara «dato del Supervisor». No inventes evidencia.
