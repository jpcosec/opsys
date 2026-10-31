# Testing handoff — task-ws03-inventariar-persistencia-consultas-y-notaciones

Contrato: `desk/tasks/task-ws03-inventariar-persistencia-consultas-y-notaciones.md` (scope, done_when) y `runs/subagents/20261031-ws03-auditoria-infraestructura/preflight-disposition.md`, que obliga también al Tester.
Entregable congelado: `desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`, sha256 `97fb8ae9c6182990d55d051fc63aad652596893244fb5c27903a182341c8d8bd`.
Evidencia del Executor: `runs/subagents/20261031-ws03-auditoria-infraestructura/result-summary.md`, `commands.log` y anexos.
Pills a sostener: pill-005 (Tester independiente), pill-001 (cierre con commit propio), pill-007 y pill-ready-phases (capa sin solapamiento).

Tester con herramientas read, grep, find y ls: sin bash ni escritura. Lo que requiere comando viene en `runs/subagents/20261031-ws03-auditoria-infraestructura/tester-facts.log`, recolectado por el Supervisor y marcado como no independiente.

Comprobaciones obligatorias:
1. Muestrear 20 filas repartidas entre todas las capacidades, con énfasis en concurrencia; abrir cada archivo:línea en ../sldb, ../pron o ../spec2viz y comprobar que dice lo afirmado.
2. Verificar leyendo código: la API y el CLI de sldb no verifican revisión al guardar; el lock de archivo cubre solo índices y no la escritura del Markdown; SAVE_LOCK es solo de proceso; un escritor externo se pierde sin aviso; el único chequeo está en HTTP y compara el payload completo (save_plan.py:50); pron compara hash_c del índice y no del archivo; ViewDoc existe solo como modelo en spec2viz/sldb_models.py sin evaluador, ausente en sldb y pron.
3. Buscar un contraejemplo a cada afirmación de ausencia con grep y find: chequeo, lock, CLI de corpus o consulta guardada. El código de spec2viz está en ../spec2viz/spec2viz, no en src/.
4. Distinguir lo leído de lo ejecutado: los comportamientos de concurrencia están deducidos del código. No leer kimun.

El Supervisor ya corrió build_plan.py --check, validate_plan.py --check y context_review.py status; no son tu prueba de contenido.

Rondas 2 y 3: entregable corregido, sha256 `6bcdbeefb7984aecbc14f25c08e449050f6e5054f253f5102a5636ad27804ed3`, verificado por tester-result-summary.md; tester-v1 y tester-v2-result-summary.md conservan las rondas previas.
