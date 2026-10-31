# Testing handoff — task-ws04-inventariar-ui-y-reconciliar-trabajo-en-curso

Contrato: `desk/tasks/task-ws04-inventariar-ui-y-reconciliar-trabajo-en-curso.md` (scope, done_when) y `runs/subagents/20261031-ws04-auditoria-ui/preflight-disposition.md`, que obliga también al Tester.
Entregable congelado: `desk/drawer/plans/workspace-documental/auditoria/ui.md`, sha256 `2496605cdf1ad252dd8d907bdb7287c82e181f8044c94a91258672f001ca2351`.
Evidencia del Executor: `runs/subagents/20261031-ws04-auditoria-ui/result-summary.md`, `commands.log` y anexos.
Pills a sostener: pill-005 (Tester independiente), pill-001 (cierre con commit propio), pill-007 y pill-ready-phases (capa sin solapamiento).

Tester con herramientas read, grep, find y ls: sin bash ni escritura. Lo que requiere comando viene en `runs/subagents/20261031-ws04-auditoria-ui/tester-facts.log`, recolectado por el Supervisor y marcado como no independiente.

Comprobaciones obligatorias:
1. Confirmar 39 filas: los 35 nodos con owner_repo graph_ui (lista en tester-facts.log) más WS06, WS07, WS10 y WS11, ninguno omitido ni marcado entregado.
2. Muestrear 12 filas con base reutilizada: abrir path o símbolo en ../UIs/graph_ui; el historial está en tester-facts.log. Un commit prueba solo la base citada.
3. Muestrear 6 filas de ausencia explícita: buscar un contraejemplo con grep en código, Board y tickets.
4. Comparar los sha256 del entregable con tester-facts.log.
5. Verificar: los dos tickets draft comparten serve.py, views/workspace/ y docs/workspace-ui.md y sus tests no existen; frontends/workspace/ está sin commit y su index.html apunta a /app.js que no existe ahí; la cabecera de SPEC dice 44 candidatas y revisión 5 mientras hoy son 63 y revisión 8; hay un enlace roto; 6.1 y 6.2 aparecen abiertas pero el plan las resolvió.

El Supervisor ya corrió build_plan.py --check, validate_plan.py --check y context_review.py status; no son tu prueba de contenido.

Ronda 2: entregable corregido, sha256 `8f4cc1caddda8160b0b80170e6f90eade0eaff199cbda94002d08a392c1727e8`, verificado por tester-result-summary.md; tester-v1-result-summary.md conserva la ronda 1.
