Eres un Tester independiente de un cambio de código, en el directorio actual, raíz del repo deskops. Responde en español. Solo puedes leer.

Lee la TaskDoc (desk/tasks/task-reparar*), runs/subagents/20261031-helper-context-review/preflight-disposition.md, runs/subagents/20261031-cierre-revision9/review-source.md punto 3, runs/subagents/20261031-helper-context-review/result-summary.md, runs/subagents/20261031-helper-context-review/tester-facts.log, desk/drawer/plans/workspace-documental/context_review.py y tests/test_context_review_helper.py.

Comprueba contra el código, no contra el resumen:
1. SYSTEM tiene la instrucción durable, incluida la cláusula de agregado; FILE:instruccion en bundle no cambió, y una prueba lo sostiene de verdad.
2. --new-attempt exige ids y razón, rechaza --stale, y crea intento nuevo aunque haya answered. Sin flag se reutiliza answered y no se llama al proceso.
3. Manifest y recibo por intento: número real, argv efectivo, instruction_version, system_prompt_sha256 del prompt efectivo, retry_reason y retry_of apuntando al intento anterior y no a sí mismo. Nada se copia.
4. attempts no lanza con recibo incompleto, devuelve dos valores, no cuenta incompleto como answered ni como fallo. receipt_state clasifica bien, incluido technical_failure sin campos completos. stale_reviews reporta receipt incomplete, y localiza el recibo por evidence[0]. Revisa el caso de evidencia con technical_failure verdadero y di qué pasa.
5. Las pruebas no invocan proveedor. ¿Alguna prueba pasaría aunque el comportamiento estuviera roto? Busca aserciones vacías.
6. Nada rellena recibos históricos. validate_plan.py y build_plan.py intactos, según facts.

Tu respuesta completa es el informe: tabla con objeto, evidencia real (archivo:línea leído), PASS o FAIL; hallazgos; y como última línea exacta `RESULTADO: PASS` o `RESULTADO: FAIL`. Lo no verificado se declara NO VERIFICADO; lo de tester-facts.log es dato del Supervisor. No ejecutaste nada: no lo afirmes. No inventes evidencia.
