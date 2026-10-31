# Testing handoff — task-ws02-inventariar-superficies-y-operaciones-deskops

Contrato: `desk/tasks/task-ws02-inventariar-superficies-y-operaciones-deskops.md` (scope, done_when) y `runs/subagents/20261031-ws02-auditoria-deskops/preflight-disposition.md`, que obliga también al Tester.
Entregable congelado: `desk/drawer/plans/workspace-documental/auditoria/deskops.md`, sha256 `e4b2ee57274b5d3adfc3f059f68d1f1551a53645082d7857bf176f0c25010f59`.
Evidencia del Executor: `runs/subagents/20261031-ws02-auditoria-deskops/result-summary.md`, `commands.log` y anexos.
Pills a sostener: pill-005 (Tester independiente), pill-001 (cierre con commit propio), pill-007 y pill-ready-phases (capa sin solapamiento).

Tester con herramientas read, grep, find y ls: sin bash ni escritura. Lo que requiere comando viene en `runs/subagents/20261031-ws02-auditoria-deskops/tester-facts.log`, recolectado por el Supervisor y marcado como no independiente.

Comprobaciones obligatorias:
1. Con el registro leído en deskops/cli/registry.py, comprobar que no falta ningún comando en el entregable y que los modelos del store figuran.
2. Muestrear 15 filas de comandos elegidas por ti, repartidas entre lectura y mutación; abrir la cita y comprobar efecto y efecto Git.
3. Verificar leyendo código: el constructor de DeskopsOperations escribe .deskops.log; validate_atoms llama ensure_workspace y puede crear andamiaje; retire no hace commit; closeout commit borra el archivo de la tarea; 2 de 8 materializaciones de store.yaml no están en el índice local.
4. Elegir 10 filas de file-inventory.tsv y comprobar el modelo contra .sldb/store.yaml. Los hashes los verificó el Supervisor: 192 filas, 0 distintos.
5. Señalar filas «comprobado» sin evidencia. commands.log fue reconstruido a mano según el Executor: decide si invalida algo y dilo.

El Supervisor ya corrió build_plan.py --check, validate_plan.py --check y context_review.py status; no son tu prueba de contenido.

Ronda 2: entregable corregido, sha256 `14fc6c94a6b7642492743ec3ccf554ba57bf1c06a44d8ced302c665e6754d890`, verificado por tester-result-summary.md; tester-v1-result-summary.md conserva la ronda 1.
