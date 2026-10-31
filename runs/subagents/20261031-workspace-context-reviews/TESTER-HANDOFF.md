# Handoff del tester independiente

Eres el tester de la tarea desk/tasks/task-revisar-dag-workspace-con-agentes-baratos.md, en el repo /home/jp/proyectos/SLDB_1/deskops. No participaste en el trabajo. Lee esa TaskDoc entera: es tu contrato. Tus únicos otros insumos son los archivos de este repo.

No edites el plan, ni desk/, ni código. Tampoco uses git para escribir. Solo escribes dos archivos en runs/subagents/20261031-workspace-context-reviews/: validation.log (comandos, exit y resultados legibles) y result-summary.md (veredicto, muestras, límites y fallos). Tus verificaciones no cuentan como review barato ni como revisión experta.

## Comprueba

1. Comandos, desde la raíz del repo:
   - python desk/drawer/plans/workspace-documental/build_plan.py --check
   - python desk/drawer/plans/workspace-documental/validate_plan.py --check
   - python desk/drawer/plans/workspace-documental/context_review.py status
2. Cobertura: en dag.yaml hay ROOT, 8 PK, WS01–WS44 y sus hijos WSxx.n; cada candidata original está en exactamente un PK; cada nodo tiene context_review.status=reviewed y evidencia existente.
3. Integridad, por script de solo lectura sobre TODOS los nodos: en evidence hay input.md, manifest.json, contract.json, output.md, stderr.log, receipt.json y disposition.md; el SHA256 de input.md coincide con la carpeta y con input_sha256; el SHA256 de contract.json coincide con contract_sha256; receipt.input_sha256 y output_sha256 coinciden; technical_failure=false.
4. Aislamiento: argv con --offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools, deepseek-flash, thinking low; sin --continue ni --resume. input.md no contiene output ni disposición de reviews anteriores.
5. Límites: execution_authorized=false; todas las tareas status=candidate; ningún gate en satisfied; source_mode=pending; decisiones.md sigue PENDING_OWNER; ningún Pxx resuelto. Compara con `git show HEAD:desk/drawer/plans/workspace-documental/dag.yaml` que los gates no cambiaron salvo scope_nodes. `git status --short` solo muestra cambios del plan, de su tarea en desk/tasks y del run-dir, además de lo que ya hubiera ajeno.
6. Rúbrica, leyendo de verdad output.md, disposition.md y contrato, en: ROOT, los 8 PK, todos los hijos WSxx.n, y WS01, WS07, WS11, WS12, WS16, WS20, WS21, WS28, WS30, WS32, WS40, WS41, WS43, WS44. Por cada uno, ¿la reformulación identifica propósito, resultado, repo y límites? ¿El dry-run respeta autoridad y secuencia de dependencias? ¿La aceptación es comprobable? ¿Queda alguna decisión de encargo sin dueño? ¿Cada hallazgo de output.md tiene disposición, y cada error_reviewer trae cita real del input de ese nodo (compruébala en su input.md) o argumento verificable?
7. Evidencia técnica: rounds/technical-failure-root-cause.md explica 216 intentos fallidos. Confirma que ninguno se usa como evidencia de review.
8. Si `pytest` se puede correr en menos de 8 minutos, córrelo; registra el resultado y los fallos que no provengan de esta tarea, sin arreglar nada. Si no, di por qué no.

## Veredicto

Escribe en result-summary.md PASS o FAIL, y por cada fallo: nodo, qué falla, evidencia. No suavices: una cita falsa o una disposición ausente es FAIL de ese nodo. Registra además referencias externas que validate_plan.py marque CHANGED sin tratarlas como fallo tuyo. Al terminar responde solo: LISTO PASS o LISTO FAIL <número de fallos>.
